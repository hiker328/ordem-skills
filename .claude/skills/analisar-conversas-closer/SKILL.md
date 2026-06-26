---
name: analisar-conversas-closer
description: >-
  Analisa conversas de closers de agência (marketing/tráfego) e gera um diagnóstico
  de performance (rapport, descoberta, contorno de objeções como "agência é tudo
  igual"/"já me queimei", fechamento etc.). Aceita 3 fontes:
  (1) mensagens de WhatsApp via Evolution API, (2) texto colado direto no chat,
  (3) áudio/vídeo de call (transcreve localmente com WhisperX + diarização por
  locutor). Use quando o usuário pedir para avaliar, analisar ou dar feedback
  sobre conversas/calls de vendas, atendimento ou closers.
---

# Analisar Conversas de Closer

Esta skill avalia o desempenho de um closer/vendedor em uma conversa e entrega um
relatório com notas, pontos fortes, erros e sugestões. A análise (julgamento) é
feita por você (o agente) usando a rubrica em `references/rubrica.md`. Os scripts
cuidam só da parte mecânica: puxar mensagens e transcrever áudio/vídeo.

**Sempre que pedir uma credencial ao usuário (token do HuggingFace, dados da
Evolution, chave da OpenAI), ensine como obtê-la** — não apenas peça. O passo a
passo de cada uma está em `references/credenciais.md`. Resuma os passos relevantes
no chat e trate toda credencial como segredo (não logar, não comitar).

## Passo 1 — Identifique a fonte da conversa

Pergunte ou detecte qual das três entradas o usuário vai usar:

| Fonte | Quando | Vá para |
|-------|--------|---------|
| **WhatsApp (Evolution)** | Usuário tem instância Evolution e quer puxar conversas reais | Passo 2A |
| **Texto colado** | Usuário cola a conversa direto no chat | Passo 2B |
| **Áudio / vídeo** | Usuário tem gravação de call (ligação, Meet, Zoom) | Passo 2C |

Se o usuário não disser, pergunte. Mais de uma fonte pode ser usada na mesma análise.

## Passo 2A — WhatsApp via Evolution API

Peça ao usuário **3 dados** (e avise que a apikey é sensível). Se ele não souber
onde achar cada um, ensine com base em `references/credenciais.md` (seção 2):

1. **URL base** da Evolution (ex.: `https://evolution.seudominio.com.br`)
2. **apikey** (header `apikey`)
3. **nome da instância** (ex.: `Luiz Augusto`)

Depois pergunte **quais conversas**: um número/contato específico, ou **todas**.

Use o script `scripts/evolution_fetch.py`. Detalhes de endpoints, formato e
parâmetros em `references/evolution.md`. Fluxo típico:

```bash
# 1) Listar as conversas disponíveis (para o usuário escolher)
python scripts/evolution_fetch.py --base-url "<URL>" --apikey "<KEY>" \
  --instance "<INSTANCIA>" --list

# 2) Puxar UMA conversa (por número ou remoteJid) já formatada como transcrição
python scripts/evolution_fetch.py --base-url "<URL>" --apikey "<KEY>" \
  --instance "<INSTANCIA>" --jid "5511999999999" --out conversa.txt

# 3) Ou TODAS as conversas (uma por arquivo, na pasta de saída)
python scripts/evolution_fetch.py --base-url "<URL>" --apikey "<KEY>" \
  --instance "<INSTANCIA>" --all --out-dir conversas/
```

O script já rotula quem fala: `fromMe=true` → **Closer**; `fromMe=false` →
**Cliente**. Vá para o Passo 3.

## Passo 2B — Texto colado

O usuário cola a conversa. Se os papéis não estiverem claros (quem é closer x
cliente), pergunte ou infira pelo conteúdo. Vá para o Passo 3.

## Passo 2C — Áudio ou vídeo de call

Transcrição é **100% local e sem custo de API** via WhisperX (Whisper local +
diarização por locutor com pyannote). Setup completo, requisitos e o caso de
vídeo (ffmpeg separa o áudio) estão em `references/transcricao.md`.

**Setup: o Claude instala o que faltar — não passe isso para o usuário.** Antes
de transcrever, cheque e instale Python, ffmpeg e as deps seguindo o "Setup
automático" de `references/transcricao.md` (usa `winget` + `pip`). A única coisa
que depende do usuário é o token do HuggingFace (precisa de conta/login).

Pré-requisitos:
- Python 3.10+, `ffmpeg` no PATH, deps de `scripts/requirements.txt`
  → o Claude instala (ver `references/transcricao.md`, "Setup automático").
- Token gratuito do HuggingFace (para a diarização). Se o usuário não tiver,
  ensine a obter pela `references/credenciais.md` (seção 1) — inclui aceitar os
  termos do modelo `speaker-diarization-community-1`, senão a diarização falha.

```bash
python scripts/transcribe.py --input call.mp4 --language pt \
  --hf-token "<HF_TOKEN>" --out transcricao.txt
```

O script: (a) se for vídeo, extrai o áudio com ffmpeg; (b) transcreve com
WhisperX; (c) **diariza** e marca `[LOCUTOR_0]`, `[LOCUTOR_1]`… com timestamps.
Depois **você** mapeia qual locutor é o closer e qual é o cliente (pelo conteúdo:
quem conduz, faz perguntas de descoberta, apresenta preço = closer). Se o usuário
souber, confirme com ele. Vá para o Passo 3.

> Sem máquina boa para rodar local? Há um fallback opcional com a API Whisper da
> OpenAI em `references/transcricao.md` — mas ela **não separa locutores** e tem
> custo. WhisperX local é o padrão recomendado.

## Passo 3 — Analise e gere o relatório

1. Leia a rubrica completa em `references/rubrica.md`.
2. Garanta que a transcrição tenha papéis claros (Closer x Cliente).
3. Produza o relatório no formato definido na rubrica: tabela de notas (0–100),
   resumo, momentos-chave com citações diretas, pontos fortes, erros e sugestões
   acionáveis.
4. Baseie tudo em **citações reais** da conversa — nunca invente.

Para várias conversas, gere um relatório por conversa e, ao final, um resumo
comparativo (médias por critério, padrões recorrentes de erro/acerto).
