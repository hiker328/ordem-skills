# Testes

Testes das **funções puras** dos scripts das skills (parsing da Evolution,
formatação de transcrição, normalização de número/JID, timestamps). Não fazem rede —
só validam a lógica que costuma quebrar quando a API muda de formato.

## Rodar

```bash
# sem pytest (roda direto)
python tests/test_scripts.py

# ou com pytest
pip install pytest requests
pytest tests/
```

Os scripts importam `requests` no topo, então tenha `requests` instalado para rodar
os testes (`pip install requests`).
