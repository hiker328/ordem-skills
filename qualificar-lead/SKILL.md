---
name: qualificar-lead
description: >-
  Lê uma conversa de vendas e qualifica o lead com um score (0-100) e uma faixa
  (quente/morno/frio/desqualificado), avaliando dor, fit, orçamento, decisor,
  urgência e engajamento. Aceita conversas do WhatsApp via Evolution API, texto
  colado, ou em lote (todas as conversas). Use quando o usuário quiser priorizar
  leads, fazer triagem, lead scoring, qualificação BANT/SPIN ou decidir em quem o
  closer foca primeiro.
---

# Qualificar Lead

Dá uma nota de qualificação a um lead a partir da conversa, para o time priorizar
quem atacar primeiro. O julgamento é seu (o agente), usando `references/scoring.md`;
o script só puxa as conversas.

## Passo 1 — Obtenha a(s) conversa(s)

| Fonte | Ação |
|-------|------|
| **WhatsApp (Evolution)** | `scripts/evolution_fetch.py` — ver `references/evolution.md`. Peça URL, apikey e instância (ensine via `references/credenciais.md`). |
| **Texto colado** | O usuário cola no chat. |

```bash
# uma conversa
python scripts/evolution_fetch.py --base-url "<URL>" --apikey "<KEY>" \
  --instance "<INSTANCIA>" --jid "5511999999999" --out lead.txt

# todas (triagem em lote)
python scripts/evolution_fetch.py --base-url "<URL>" --apikey "<KEY>" \
  --instance "<INSTANCIA>" --all --out-dir leads/
```

## Passo 2 — Pontue

Leia `references/scoring.md` e avalie os critérios (dor, fit/ICP, orçamento,
decisor, urgência, engajamento). Baseie cada nota em **evidência da conversa** —
sem evidência, marque como "não identificado" (não invente).

## Passo 3 — Entregue o resultado

Para **um lead**, use o formato de `references/scoring.md`: score, faixa, motivo
por critério, sinais de compra, red flags e **próxima ação recomendada**.

Para **vários leads (lote)**, gere uma **tabela ranqueada** (lead, score, faixa,
próxima ação) do mais quente ao mais frio, e destaque os 3 prioritários. Assim o
closer sabe a ordem de ataque.
