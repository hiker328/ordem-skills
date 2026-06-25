# Transcrição de áudio/vídeo com diarização (WhisperX)

Objetivo: transformar uma gravação de call em uma transcrição com **quem falou o
quê**, sem custo de API. Pipeline: ffmpeg (se vídeo) → WhisperX (Whisper local) →
diarização por locutor (pyannote).

## Por que WhisperX e não a API Whisper da OpenAI

A API Whisper da OpenAI (`whisper-1`, `gpt-4o-transcribe`) **só transcreve** — não
diz quem está falando e tem custo por minuto. WhisperX roda o Whisper localmente
(via faster-whisper) **e** acopla diarização (pyannote), entregando rótulos de
locutor. Tudo local = sem gastos. É o padrão desta skill.

`whisper-diarization` (MahmoudAshraf) é uma alternativa equivalente (faster-whisper
+ NeMo). Use se preferir; o resultado e o uso pela skill são os mesmos.

## Setup automático (o Claude instala — Windows)

Antes de transcrever, **o Claude deve checar e instalar o que faltar**, sem
empurrar o trabalho para o usuário. Faça em ordem, verificando cada item antes:

1. **Python 3.10+** — cheque com `python --version`.
   - Se faltar: `winget install -e --id Python.Python.3.12`.
2. **ffmpeg** — cheque com `ffmpeg -version`.
   - Se faltar: `winget install -e --id Gyan.FFmpeg`.
   - Após instalar via winget, o PATH só vale em **novo** shell — abra um novo
     comando (ou use o caminho completo) para os próximos passos.
3. **Dependências Python** — instale as deps:
   ```bash
   pip install -r scripts/requirements.txt
   ```
   Isso instala `whisperx` (puxa torch, faster-whisper, pyannote.audio).
   - Cheque se já está instalado com `python -c "import whisperx"` antes de
     reinstalar.
   - Com GPU NVIDIA, instale o torch com CUDA antes (ver pytorch.org) para
     acelerar muito; sem GPU funciona em CPU (mais lento — use `--model small`).
   - Opcional (recomendado): criar um venv antes —
     `python -m venv .venv && .venv\Scripts\activate`.

Só o que o Claude **não consegue** fazer pelo usuário (precisa de conta/login) é o
token do HuggingFace — para isso, ensine os passos (item 4 abaixo e
`credenciais.md`).

4. **Token HuggingFace** (gratuito) — necessário **só para a diarização**
   (separar locutores). Transcrição pura não precisa de token. A diarização usa
   modelos "gated" do pyannote, daí o token:
   - Crie em huggingface.co/settings/tokens (tipo "read").
   - **Aceite os termos** do modelo (uma vez, logado):
     - huggingface.co/pyannote/speaker-diarization-community-1
   - Passe o token em `--hf-token` (ou variável `HF_TOKEN`).

   **Quer evitar o token?** Use o `whisper-diarization` (MahmoudAshraf), que faz
   a diarização com NeMo (NVIDIA) — modelos não-gated, sem token HF. O custo é um
   setup mais pesado. Funcionalmente entrega o mesmo: transcrição com locutores
   separados.

## Uso

```bash
# Vídeo (o script extrai o áudio com ffmpeg automaticamente)
python scripts/transcribe.py --input call.mp4 --language pt \
  --hf-token "<HF_TOKEN>" --out transcricao.txt

# Áudio direto
python scripts/transcribe.py --input call.m4a --language pt \
  --hf-token "<HF_TOKEN>" --out transcricao.txt

# Dicas: forçar nº de locutores melhora a diarização
python scripts/transcribe.py --input call.mp4 --language pt \
  --hf-token "<HF_TOKEN>" --min-speakers 2 --max-speakers 2 --out transcricao.txt
```

Parâmetros úteis:
- `--model` — tamanho do Whisper (`tiny`,`base`,`small`,`medium`,`large-v3`).
  Padrão `medium`. Em CPU, `small` é o melhor custo/benefício.
- `--language` — código do idioma (`pt`). Omitir = autodetecção.
- `--min-speakers` / `--max-speakers` — fixe em `2` para call closer↔cliente.
- `--device` — `cuda` ou `cpu` (autodetecta por padrão).

## Saída

Segmentos agrupados por locutor com timestamps:

```
[00:00:02 - 00:00:08] LOCUTOR_0: Oi, tudo bem? Obrigado por aceitar a call...
[00:00:09 - 00:00:15] LOCUTOR_1: Tudo, e você? Então, meu problema hoje é...
```

WhisperX não sabe o **nome** dos locutores, só os separa (`LOCUTOR_0`,
`LOCUTOR_1`). Depois, na análise, **mapeie**: normalmente o closer é quem conduz,
faz perguntas de descoberta, apresenta a solução e o preço; o cliente reage e
levanta objeções. Confirme com o usuário se houver dúvida.

## Fallback opcional — API Whisper da OpenAI (com custo, sem diarização)

Só se o usuário não puder rodar local. Perde a separação de locutores.

```bash
# extrair áudio do vídeo
ffmpeg -i call.mp4 -vn -ac 1 -ar 16000 audio.wav
# enviar para a OpenAI (requer OPENAI_API_KEY)
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.wav -F model=whisper-1 -F language=pt
```
Nesse caso, a separação closer↔cliente fica por sua conta, inferida pelo conteúdo.

## Problemas comuns

- **Erro de acesso ao modelo pyannote** → token não passado ou termos não aceitos
  (ver Setup passo 4).
- **Lentidão extrema em CPU** → use `--model small` e `--min/max-speakers 2`.
- **`ffmpeg not found`** → ffmpeg não está no PATH (ver Setup passo 2).
- **Versões do whisperx** mudam o import da diarização; o script tenta os dois
  caminhos conhecidos automaticamente.
