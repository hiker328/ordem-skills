#!/usr/bin/env python3
"""
Puxa conversas de WhatsApp da Evolution API e formata como transcrição
rotulada (Closer x Cliente) para análise.

Endpoints (auth via header `apikey`):
  POST {base}/chat/findChats/{instance}          -> lista de conversas
  POST {base}/chat/findMessages/{instance}       -> mensagens de um remoteJid
    body: {"where": {"key": {"remoteJid": "<JID>"}}}

Regra de papéis: key.fromMe == True  -> Closer (instância)
                 key.fromMe == False -> Cliente (contato)

Exemplos:
  python evolution_fetch.py --base-url URL --apikey KEY --instance INST --list
  python evolution_fetch.py --base-url URL --apikey KEY --instance INST \
      --jid 5511999999999 --out conversa.txt
  python evolution_fetch.py --base-url URL --apikey KEY --instance INST \
      --all --out-dir conversas/
"""
import argparse
import datetime as dt
import os
import re
import sys
from urllib.parse import quote

try:
    import requests
except ImportError:
    sys.exit("Faltou a lib 'requests'. Rode: pip install requests")


def _url(base, path, instance):
    return f"{base.rstrip('/')}/{path}/{quote(instance)}"


def _post_or_get(base, path, instance, apikey, body=None):
    """Tenta POST; se 404/405, cai para GET (varia por versão da Evolution)."""
    headers = {"apikey": apikey, "Content-Type": "application/json"}
    url = _url(base, path, instance)
    r = requests.post(url, headers=headers, json=(body or {}), timeout=60)
    if r.status_code in (404, 405):
        r = requests.get(url, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()


def _as_list(data, *keys):
    """Normaliza respostas que podem vir como list ou aninhadas."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in keys:
            v = data.get(k)
            if isinstance(v, list):
                return v
            if isinstance(v, dict):
                rec = v.get("records")
                if isinstance(rec, list):
                    return rec
        # fallback: primeiro valor que for lista
        for v in data.values():
            if isinstance(v, list):
                return v
    return []


def normalize_jid(jid):
    """Aceita número puro ou JID completo."""
    if "@" in jid:
        return jid
    digits = re.sub(r"\D", "", jid)
    return f"{digits}@s.whatsapp.net"


def list_chats(base, instance, apikey):
    data = _post_or_get(base, "chat/findChats", instance, apikey)
    return _as_list(data, "chats", "records")


def fetch_messages(base, instance, apikey, jid):
    body = {"where": {"key": {"remoteJid": jid}}}
    data = _post_or_get(base, "chat/findMessages", instance, apikey, body)
    return _as_list(data, "messages", "records")


def extract_text(msg):
    """Extrai texto dos tipos comuns; marca mídia sem texto."""
    m = msg.get("message") or {}
    if not isinstance(m, dict):
        return "[mensagem]"
    if m.get("conversation"):
        return m["conversation"]
    ext = m.get("extendedTextMessage")
    if isinstance(ext, dict) and ext.get("text"):
        return ext["text"]
    for k, label in (
        ("imageMessage", "[imagem]"),
        ("videoMessage", "[vídeo]"),
        ("audioMessage", "[áudio]"),
        ("documentMessage", "[documento]"),
        ("stickerMessage", "[figurinha]"),
        ("locationMessage", "[localização]"),
    ):
        part = m.get(k)
        if isinstance(part, dict):
            cap = part.get("caption")
            return cap if cap else label
    return "[mensagem não textual]"


def _ts(msg):
    t = msg.get("messageTimestamp") or msg.get("messageTimestamp".lower()) or 0
    try:
        return int(t)
    except (TypeError, ValueError):
        return 0


def format_transcript(messages):
    msgs = sorted(messages, key=_ts)
    lines = []
    for msg in msgs:
        key = msg.get("key") or {}
        role = "Closer" if key.get("fromMe") else "Cliente"
        text = extract_text(msg).replace("\n", " ").strip()
        if not text:
            continue
        ts = _ts(msg)
        when = (
            dt.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
            if ts else "??"
        )
        lines.append(f"[{when}] {role}: {text}")
    return "\n".join(lines)


def chat_label(chat):
    jid = chat.get("remoteJid") or chat.get("id") or chat.get("jid") or "?"
    name = chat.get("pushName") or chat.get("name") or ""
    return jid, name


def main():
    ap = argparse.ArgumentParser(description="Puxa conversas da Evolution API")
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--apikey", required=True)
    ap.add_argument("--instance", required=True)
    ap.add_argument("--list", action="store_true", help="lista as conversas")
    ap.add_argument("--jid", help="número ou remoteJid de uma conversa")
    ap.add_argument("--all", action="store_true", help="puxa todas as conversas")
    ap.add_argument("--out", help="arquivo de saída (modo --jid)")
    ap.add_argument("--out-dir", help="pasta de saída (modo --all)")
    args = ap.parse_args()

    if args.list:
        chats = list_chats(args.base_url, args.instance, args.apikey)
        print(f"{len(chats)} conversa(s):\n")
        for c in chats:
            jid, name = chat_label(c)
            print(f"  {jid}\t{name}")
        return

    if args.jid:
        jid = normalize_jid(args.jid)
        msgs = fetch_messages(args.base_url, args.instance, args.apikey, jid)
        transcript = format_transcript(msgs)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"OK: {len(msgs)} mensagens -> {args.out}")
        else:
            print(transcript)
        return

    if args.all:
        out_dir = args.out_dir or "conversas"
        os.makedirs(out_dir, exist_ok=True)
        chats = list_chats(args.base_url, args.instance, args.apikey)
        print(f"Puxando {len(chats)} conversa(s) para {out_dir}/ ...")
        for c in chats:
            jid, name = chat_label(c)
            if not jid or jid == "?":
                continue
            try:
                msgs = fetch_messages(
                    args.base_url, args.instance, args.apikey, jid
                )
            except Exception as e:  # noqa: BLE001
                print(f"  ! falhou {jid}: {e}")
                continue
            transcript = format_transcript(msgs)
            if not transcript.strip():
                continue
            safe = re.sub(r"[^0-9A-Za-z._-]", "_", jid)
            path = os.path.join(out_dir, f"{safe}.txt")
            with open(path, "w", encoding="utf-8") as f:
                if name:
                    f.write(f"# Contato: {name} ({jid})\n\n")
                f.write(transcript)
            print(f"  OK {jid} -> {path} ({len(msgs)} msgs)")
        return

    ap.error("informe --list, --jid <num> ou --all")


if __name__ == "__main__":
    main()
