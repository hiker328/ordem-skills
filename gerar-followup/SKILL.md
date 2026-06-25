---
name: gerar-followup
description: >-
  Gera a próxima mensagem de follow-up para conversas de vendas paradas, seguindo
  uma cadência configurável (dia 1, 3, 6, 9, 14, 17...). Lê a conversa do WhatsApp
  via Evolution API (ou texto colado), decide em que estágio de follow-up o lead
  está e escreve mensagens personalizadas pelo contexto. Opcionalmente envia pela
  Evolution. Use quando o usuário quiser recuperar leads frios, criar follow-ups,
  reativar conversas paradas ou montar uma cadência de FUP.
---

# Gerar Follow-up

Recupera conversas de vendas estagnadas: lê o histórico, identifica em que ponto da
cadência o lead está e gera a próxima mensagem de follow-up (FUP) personalizada. O
**texto** é criado por você (o agente) usando `references/cadencia.md`; os scripts
só puxam e (opcionalmente) enviam mensagens.

## Passo 1 — Obtenha a conversa

| Fonte | Ação |
|-------|------|
| **WhatsApp (Evolution)** | Use `scripts/evolution_fetch.py` (ver `references/evolution.md`). Peça URL, apikey e instância — ensine a obter por `references/credenciais.md` se preciso. |
| **Texto colado** | O usuário cola o histórico no chat. |

```bash
python scripts/evolution_fetch.py --base-url "<URL>" --apikey "<KEY>" \
  --instance "<INSTANCIA>" --jid "5511999999999" --out conversa.txt
```

Para reativar vários leads de uma vez, use `--all --out-dir conversas/` e processe
cada arquivo.

## Passo 2 — Diagnostique o estágio do lead

Leia `references/cadencia.md`. Determine:
1. **Qual foi o último contato** e **há quanto tempo** (use os timestamps).
2. **Quem mandou a última mensagem** — se foi o cliente sem resposta do closer, a
   prioridade é responder, não "follow-up genérico".
3. **Em que FUP o lead está** (FUP-1 a FUP-6) com base em quantos follow-ups já
   foram enviados sem resposta.
4. **O contexto/objeção** que travou a conversa (preço, "vou pensar", sumiu, etc.).

## Passo 3 — Gere a(s) mensagem(ns)

Siga os princípios de `references/cadencia.md`. Para cada follow-up:
- Personalize com algo **real** da conversa (nome, dor, algo que ele disse).
- Um objetivo por mensagem; sempre com um próximo passo claro (CTA).
- Tom humano, curto, sem parecer template/cobrança.
- Respeite o estágio: FUPs iniciais agregam valor; finais fazem o "corte" educado.

Apresente as mensagens prontas para o usuário aprovar. Se ele pedir, gere a
**sequência inteira** da cadência (FUP-1..6) de uma vez.

## Passo 4 — Enviar (opcional, com confirmação)

**Nunca envie sem o usuário aprovar o texto explicitamente.** Após aprovação:

```bash
python scripts/evolution_send.py --base-url "<URL>" --apikey "<KEY>" \
  --instance "<INSTANCIA>" --jid "5511999999999" --text "mensagem aprovada"
```

Para agendamento real por horário/cadência automática, isso é trabalho de uma
automação (ex.: n8n, como no fluxo "Disparo de FUPs"); esta skill gera e pode
disparar manualmente, não roda um cron sozinha.
