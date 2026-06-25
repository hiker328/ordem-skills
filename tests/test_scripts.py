#!/usr/bin/env python3
"""
Testes das funções puras dos scripts das skills (parsing/formatação) — sem rede.

Rodar:
    python tests/test_scripts.py          # roda direto (sem pytest)
    pytest tests/                          # ou via pytest

Requisitos: requests instalado (os scripts importam no topo).
    pip install requests
"""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fetch = _load(
    SKILLS / "analisar-conversas-closer" / "scripts" / "evolution_fetch.py",
    "ev_fetch",
)
trans = _load(
    SKILLS / "analisar-conversas-closer" / "scripts" / "transcribe.py",
    "ev_transcribe",
)
send = _load(
    SKILLS / "gerar-followup" / "scripts" / "evolution_send.py",
    "ev_send",
)


# ---- evolution_fetch ----

def test_normalize_jid_numero():
    assert fetch.normalize_jid("5511999999999") == "5511999999999@s.whatsapp.net"


def test_normalize_jid_com_simbolos():
    assert fetch.normalize_jid("+55 (11) 99999-9999") == "5511999999999@s.whatsapp.net"


def test_normalize_jid_ja_jid():
    assert fetch.normalize_jid("123@g.us") == "123@g.us"


def test_extract_text_conversation():
    assert fetch.extract_text({"message": {"conversation": "oi"}}) == "oi"


def test_extract_text_extended():
    msg = {"message": {"extendedTextMessage": {"text": "com reply"}}}
    assert fetch.extract_text(msg) == "com reply"


def test_extract_text_caption():
    msg = {"message": {"imageMessage": {"caption": "legenda"}}}
    assert fetch.extract_text(msg) == "legenda"


def test_extract_text_audio_sem_texto():
    assert fetch.extract_text({"message": {"audioMessage": {}}}) == "[áudio]"


def test_as_list_direto():
    assert fetch._as_list([1, 2, 3]) == [1, 2, 3]


def test_as_list_aninhado_records():
    data = {"messages": {"records": [{"a": 1}]}}
    assert fetch._as_list(data, "messages") == [{"a": 1}]


def test_format_transcript_papeis_e_ordem():
    msgs = [
        {"key": {"fromMe": False}, "messageTimestamp": 200,
         "message": {"conversation": "resposta cliente"}},
        {"key": {"fromMe": True}, "messageTimestamp": 100,
         "message": {"conversation": "oi do closer"}},
    ]
    out = fetch.format_transcript(msgs)
    linhas = out.splitlines()
    # ordenado por timestamp: closer primeiro
    assert "Closer: oi do closer" in linhas[0]
    assert "Cliente: resposta cliente" in linhas[1]


# ---- transcribe ----

def test_hms():
    assert trans.hms(0) == "00:00:00"
    assert trans.hms(3661) == "01:01:01"
    assert trans.hms(None) == "00:00:00"


def test_is_video():
    assert trans.is_video("call.mp4") is True
    assert trans.is_video("CALL.MOV") is True
    assert trans.is_video("audio.wav") is False


# ---- evolution_send ----

def test_normalize_number_de_jid():
    assert send.normalize_number("5511988887777@s.whatsapp.net") == "5511988887777"


def test_normalize_number_com_simbolos():
    assert send.normalize_number("+55 11 98888-7777") == "5511988887777"


def _run_all():
    fns = [v for k, v in globals().items()
           if k.startswith("test_") and callable(v)]
    falhas = 0
    for fn in fns:
        try:
            fn()
            print(f"OK  {fn.__name__}")
        except AssertionError as e:
            falhas += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{len(fns) - falhas}/{len(fns)} passaram.")
    return falhas


if __name__ == "__main__":
    import sys
    sys.exit(1 if _run_all() else 0)
