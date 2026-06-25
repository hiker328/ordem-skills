#!/usr/bin/env python3
"""
Transcreve áudio/vídeo de call com diarização por locutor (WhisperX, local).
Se a entrada for vídeo, extrai o áudio com ffmpeg antes.

Saída: segmentos agrupados por locutor com timestamps:
  [00:00:02 - 00:00:08] LOCUTOR_0: ...
  [00:00:09 - 00:00:15] LOCUTOR_1: ...

Requisitos: ver ../references/transcricao.md
  - ffmpeg no PATH
  - pip install -r requirements.txt
  - token HuggingFace (--hf-token ou env HF_TOKEN) p/ o modelo de diarização

Exemplo:
  python transcribe.py --input call.mp4 --language pt \
      --hf-token TOKEN --min-speakers 2 --max-speakers 2 --out transcricao.txt
"""
import argparse
import os
import subprocess
import sys
import tempfile

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".flv", ".wmv"}


def is_video(path):
    return os.path.splitext(path)[1].lower() in VIDEO_EXTS


def extract_audio(video_path):
    """Extrai áudio mono 16kHz wav via ffmpeg para um arquivo temporário."""
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-ac", "1", "-ar", "16000", tmp.name,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except FileNotFoundError:
        sys.exit("ffmpeg não encontrado no PATH. Veja references/transcricao.md.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ffmpeg falhou: {e.stderr.decode(errors='ignore')[:500]}")
    return tmp.name


def hms(seconds):
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def pick_device(requested):
    if requested:
        return requested
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:  # noqa: BLE001
        return "cpu"


def load_diarizer(hf_token, device):
    """O caminho de import da diarização mudou entre versões do whisperx."""
    try:
        from whisperx.diarize import DiarizationPipeline
    except Exception:  # noqa: BLE001
        from whisperx import DiarizationPipeline  # versões antigas
    return DiarizationPipeline(use_auth_token=hf_token, device=device)


def main():
    ap = argparse.ArgumentParser(description="Transcrição + diarização (WhisperX)")
    ap.add_argument("--input", required=True, help="arquivo de áudio ou vídeo")
    ap.add_argument("--out", help="arquivo de saída (.txt). Sem isso, imprime")
    ap.add_argument("--model", default="medium",
                    help="tiny|base|small|medium|large-v3 (padrão: medium)")
    ap.add_argument("--language", default=None, help="ex.: pt (padrão: autodetect)")
    ap.add_argument("--hf-token", default=os.environ.get("HF_TOKEN"),
                    help="token HuggingFace (ou env HF_TOKEN)")
    ap.add_argument("--min-speakers", type=int, default=None)
    ap.add_argument("--max-speakers", type=int, default=None)
    ap.add_argument("--device", default=None, help="cuda|cpu (autodetect)")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        sys.exit(f"Arquivo não encontrado: {args.input}")
    if not args.hf_token:
        sys.exit("Token HuggingFace ausente. Use --hf-token ou env HF_TOKEN. "
                 "Veja references/transcricao.md (Setup, passo 4).")

    try:
        import whisperx
    except ImportError:
        sys.exit("whisperx não instalado. Rode: pip install -r requirements.txt")

    device = pick_device(args.device)
    compute_type = "float16" if device == "cuda" else "int8"

    audio_path = args.input
    tmp_audio = None
    if is_video(args.input):
        print("Vídeo detectado — extraindo áudio com ffmpeg...", file=sys.stderr)
        tmp_audio = extract_audio(args.input)
        audio_path = tmp_audio

    try:
        print(f"Carregando Whisper '{args.model}' ({device})...", file=sys.stderr)
        model = whisperx.load_model(
            args.model, device, compute_type=compute_type, language=args.language
        )
        audio = whisperx.load_audio(audio_path)

        print("Transcrevendo...", file=sys.stderr)
        result = model.transcribe(audio, batch_size=16, language=args.language)
        lang = result.get("language", args.language or "pt")

        print("Alinhando timestamps...", file=sys.stderr)
        try:
            align_model, metadata = whisperx.load_align_model(
                language_code=lang, device=device
            )
            result = whisperx.align(
                result["segments"], align_model, metadata, audio, device
            )
        except Exception as e:  # noqa: BLE001
            print(f"  (alinhamento pulado: {e})", file=sys.stderr)

        print("Diarizando (separando locutores)...", file=sys.stderr)
        diarizer = load_diarizer(args.hf_token, device)
        diar_kwargs = {}
        if args.min_speakers is not None:
            diar_kwargs["min_speakers"] = args.min_speakers
        if args.max_speakers is not None:
            diar_kwargs["max_speakers"] = args.max_speakers
        diarize_segments = diarizer(audio, **diar_kwargs)
        result = whisperx.assign_word_speakers(diarize_segments, result)
    finally:
        if tmp_audio and os.path.exists(tmp_audio):
            os.remove(tmp_audio)

    # Monta a transcrição agrupando segmentos consecutivos do mesmo locutor.
    lines = []
    cur_spk, cur_start, cur_end, cur_text = None, None, None, []
    for seg in result.get("segments", []):
        spk = seg.get("speaker", "LOCUTOR_?")
        spk = spk.replace("SPEAKER_", "LOCUTOR_")
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        if spk == cur_spk:
            cur_end = seg.get("end", cur_end)
            cur_text.append(text)
        else:
            if cur_spk is not None:
                lines.append(
                    f"[{hms(cur_start)} - {hms(cur_end)}] {cur_spk}: "
                    + " ".join(cur_text)
                )
            cur_spk = spk
            cur_start = seg.get("start", 0)
            cur_end = seg.get("end", cur_start)
            cur_text = [text]
    if cur_spk is not None:
        lines.append(
            f"[{hms(cur_start)} - {hms(cur_end)}] {cur_spk}: " + " ".join(cur_text)
        )

    output = "\n".join(lines)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"OK -> {args.out} ({len(lines)} blocos de fala)", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
