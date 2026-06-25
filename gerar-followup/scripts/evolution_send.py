#!/usr/bin/env python3
"""
Envia uma mensagem de texto pela Evolution API.

Endpoint:
  POST {base}/message/sendText/{instance}
  Header: apikey: <KEY>
  Body (Evolution v2): {"number": "<numero|jid>", "text": "<msg>"}
  (fallback v1):       {"number": "<numero|jid>", "textMessage": {"text": "<msg>"}}

SEGURANÇA: só rode após o usuário aprovar o texto. Por padrão pede confirmação;
use --yes para pular (ex.: quando o agente já confirmou com o usuário).

Exemplo:
  python evolution_send.py --base-url URL --apikey KEY --instance INST \
      --jid 5511999999999 --text "Oi João, ..." --yes
"""
import argparse
import re
import sys
from urllib.parse import quote

try:
    import requests
except ImportError:
    sys.exit("Faltou a lib 'requests'. Rode: pip install requests")


def normalize_number(jid):
    """Evolution aceita número puro ou JID; manda só os dígitos por segurança."""
    if "@" in jid:
        return jid.split("@", 1)[0]
    return re.sub(r"\D", "", jid)


def send(base, instance, apikey, number, text):
    url = f"{base.rstrip('/')}/message/sendText/{quote(instance)}"
    headers = {"apikey": apikey, "Content-Type": "application/json"}
    # tenta formato v2
    r = requests.post(url, headers=headers,
                      json={"number": number, "text": text}, timeout=60)
    if r.status_code >= 400:
        # fallback v1
        r = requests.post(url, headers=headers,
                          json={"number": number,
                                "textMessage": {"text": text}}, timeout=60)
    r.raise_for_status()
    return r.json()


def main():
    ap = argparse.ArgumentParser(description="Envia texto pela Evolution API")
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--apikey", required=True)
    ap.add_argument("--instance", required=True)
    ap.add_argument("--jid", required=True, help="número ou remoteJid do destino")
    ap.add_argument("--text", required=True, help="mensagem a enviar")
    ap.add_argument("--yes", action="store_true",
                    help="pula a confirmação interativa")
    args = ap.parse_args()

    number = normalize_number(args.jid)
    print(f"Destino: {number}\nMensagem:\n{args.text}\n")
    if not args.yes:
        resp = input("Enviar? (s/N) ").strip().lower()
        if resp not in ("s", "sim", "y", "yes"):
            print("Cancelado.")
            return

    out = send(args.base_url, args.instance, args.apikey, number, args.text)
    print("Enviado.", out if isinstance(out, dict) else "")


if __name__ == "__main__":
    main()
