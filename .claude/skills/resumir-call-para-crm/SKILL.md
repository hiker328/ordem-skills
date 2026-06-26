---
name: resumir-call-para-crm
description: >-
  Transforma uma call de vendas de agência (marketing/tráfego — gravação de
  áudio/vídeo, ou transcrição já pronta) em notas estruturadas para o CRM: dor,
  contexto, verba/fee, decisor,
  objeções, próximos passos e data de follow-up. Transcreve localmente com
  WhisperX + diarização (separa quem fala), sem custo de API. Use quando o usuário
  quiser registrar uma reunião/ligação no CRM, gerar notas de call, resumo de
  reunião comercial ou extrair próximos passos de uma conversa gravada.
---

# Resumir Call para CRM

Pega uma call gravada e devolve notas prontas para colar no CRM. A transcrição é
mecânica (script); a extração/estruturação é sua (o agente), usando
`references/formato-crm.md`.

## Passo 1 — Obtenha a transcrição

| Entrada | Ação |
|---------|------|
| **Áudio/vídeo** | Transcreva com `scripts/transcribe.py` (ver `references/transcricao.md`). |
| **Transcrição pronta** | O usuário cola o texto no chat. |

**Setup: o Claude instala o que faltar** (Python, ffmpeg, deps) seguindo o "Setup
automático" de `references/transcricao.md`. O token do HuggingFace (diarização)
depende do usuário — ensine a obter por `references/credenciais.md` (seção 1).

```bash
python scripts/transcribe.py --input call.mp4 --language pt \
  --hf-token "<HF_TOKEN>" --min-speakers 2 --max-speakers 2 --out transcricao.txt
```

A transcrição sai com locutores separados (`LOCUTOR_0`, `LOCUTOR_1`). Identifique
quem é o vendedor e quem é o cliente pelo conteúdo (ou pergunte ao usuário).

## Passo 2 — Extraia e estruture

Leia `references/formato-crm.md` e preencha os campos **só com o que apareceu na
call**. Campo sem informação → "não mencionado" (nunca invente). Cite trechos
quando ajudar.

## Passo 3 — Entregue as notas

Gere no formato de `references/formato-crm.md`: resumo de 2–3 linhas, dados de
qualificação (dor, contexto, orçamento, decisor, urgência), objeções levantadas,
**próximos passos com responsável e data**, e um sugerido de follow-up. Ofereça
também uma versão curta (1 parágrafo) para colar no campo de observações do CRM.
