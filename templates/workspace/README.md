# Workspace (template)

Layout sugerido para trabalhar com as skills numa pasta organizada. Copie esta
pasta para onde for usar, renomeie e trabalhe dentro dela.

```
meu-workspace/
├── .env                 # suas credenciais (copie de .env.example) — NÃO comitar
├── entradas/            # áudios/vídeos de call e conversas coladas
├── saidas/              # relatórios, transcrições, notas de CRM gerados
└── leads/               # conversas puxadas em lote da Evolution
```

Fluxo típico:
1. Jogue a gravação da call em `entradas/`.
2. Peça ao agente para transcrever/analisar/resumir.
3. Os resultados ficam em `saidas/`.

> As pastas `entradas/`, `saidas/`, `leads/` e o `.env` já são ignoradas pelo
> `.gitignore` do repo — seus dados e segredos não vão para o git.
