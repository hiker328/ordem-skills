# A Ordem — Skills

> Coleção de **Agent Skills** (formato `SKILL.md`) para Claude Code / Cursor.
> Feito pela **A Ordem**.

---

## O que é

Um conjunto de skills que ensinam o agente de IA (Claude Code ou Cursor) a
executar tarefas especializadas de ponta a ponta, falando em português. Cada skill
é uma pasta com um `SKILL.md` (as instruções), documentação de apoio (`references/`)
e scripts utilitários (`scripts/`). O agente carrega a skill quando a tarefa bate
com a descrição dela e segue o passo a passo — incluindo instalar dependências,
rodar scripts e gerar o resultado.

Hoje o pacote contém **5 skills** que formam uma suíte de *enablement* de closer:
analisar → treinar → qualificar → recuperar → registrar.

## Por que existe

Times comerciais geram muitas conversas (WhatsApp, calls) e quase nunca têm tempo
de revisar a qualidade do que os closers fazem. Avaliar isso na mão é lento e
subjetivo. Estas skills transformam o agente numa ferramenta repetível: ele puxa a
conversa, padroniza, aplica uma rubrica consistente e devolve um diagnóstico
acionável — sempre do mesmo jeito, em escala.

## Pra quem é

- **Gestores comerciais / head de vendas** que querem auditar e treinar closers.
- **Consultorias e agências** que entregam diagnóstico de vendas para clientes.
- **Operações que usam Evolution API** (WhatsApp) e querem analisar conversas reais.

## Arquitetura

Cada skill segue o mesmo padrão de 3 camadas (*progressive disclosure*):

```
SKILL.md        →  orquestrador: o agente lê primeiro. Decide o fluxo e roteia.
references/*.md  →  conhecimento detalhado, lido só quando necessário.
scripts/*        →  trabalho mecânico/determinístico (puxar dados, transcrever).
```

Princípio central: **o julgamento é do agente; o mecânico é dos scripts.** O Claude
faz a análise (lendo a rubrica); os scripts só executam o que é frágil ou
repetitivo (chamar API, rodar ffmpeg/WhisperX). Isso mantém o `SKILL.md` enxuto e o
resultado consistente.

## As skills

### `analisar-conversas-closer`

Analisa o desempenho de um closer/vendedor numa conversa e gera um relatório com
notas (0–100), pontos fortes, erros e sugestões. Aceita **3 fontes de entrada**:

| Fonte | Como funciona |
|-------|---------------|
| **WhatsApp (Evolution API)** | O agente puxa as conversas da instância. Usuário escolhe um contato ou todas. Papéis vêm rotulados (Closer/Cliente) automaticamente. |
| **Texto colado** | O usuário cola a conversa direto no chat. |
| **Áudio/vídeo de call** | Transcrição **local e sem custo de API** com WhisperX + diarização (separa quem fala). Se for vídeo, o ffmpeg extrai o áudio. |

Docs internos: `rubrica.md`, `evolution.md`, `transcricao.md`, `credenciais.md`.

### `treinar-closer`

Treino por **role-play**: o agente encarna um cliente (frio, indeciso, agressivo,
interessado) num cenário/produto definido, conduz a conversa e, ao final, pontua o
closer com a rubrica e dá feedback acionável. Não usa scripts — é conversa guiada.
Docs internos: `perfis-cliente.md`, `rubrica.md`.

### `qualificar-lead`

Lê a conversa e dá um **score de qualificação** (0–100) e faixa (quente/morno/frio/
desqualificado) por 6 critérios (dor, fit, orçamento, decisor, urgência,
engajamento). Aceita uma conversa, texto colado ou **lote** (ranqueia todas).
Fonte de dados via Evolution. Docs internos: `scoring.md`, `evolution.md`,
`credenciais.md`.

### `gerar-followup`

Recupera conversas paradas: identifica o estágio do lead na **cadência** (FUP-1 a
FUP-6) e gera a próxima mensagem (ou a sequência inteira), personalizada pelo
contexto. Pode **enviar** pela Evolution (sempre após aprovação do texto). Docs
internos: `cadencia.md`, `evolution.md`, `credenciais.md`.

### `resumir-call-para-crm`

Transforma uma call gravada (áudio/vídeo) em **notas estruturadas para o CRM**:
dor, contexto, orçamento, decisor, objeções e próximos passos com data. Transcreve
local com WhisperX + diarização. Docs internos: `formato-crm.md`, `transcricao.md`,
`credenciais.md`.

## Estrutura de pastas

```
D:\Skills\
├── README.md                       # esta documentação
├── analisar-conversas-closer\
│   ├── SKILL.md
│   ├── references\  (rubrica, evolution, transcricao, credenciais)
│   └── scripts\     (evolution_fetch.py, transcribe.py, requirements.txt)
├── treinar-closer\
│   ├── SKILL.md
│   └── references\  (perfis-cliente, rubrica)
├── qualificar-lead\
│   ├── SKILL.md
│   ├── references\  (scoring, evolution, credenciais)
│   └── scripts\     (evolution_fetch.py, requirements.txt)
├── gerar-followup\
│   ├── SKILL.md
│   ├── references\  (cadencia, evolution, credenciais)
│   └── scripts\     (evolution_fetch.py, evolution_send.py, requirements.txt)
└── resumir-call-para-crm\
    ├── SKILL.md
    ├── references\  (formato-crm, transcricao, credenciais)
    └── scripts\     (transcribe.py, requirements.txt)
```

Cada skill é **auto-contida**: os docs/scripts compartilhados (Evolution,
transcrição, credenciais) ficam copiados dentro de cada uma, para poderem ser
instaladas individualmente.

## Como instalar

As skills moram em `D:\Skills`. Para o agente **carregar** uma skill, copie a pasta
dela para o diretório de skills do seu ambiente:

**Claude Code**
```powershell
# todas as skills de uma vez (pessoal, todos os projetos)
Copy-Item -Recurse "D:\Skills\*" "$env:USERPROFILE\.claude\skills\"
# ou só uma: Copy-Item -Recurse "D:\Skills\gerar-followup" "$env:USERPROFILE\.claude\skills\"
# ou por projeto: <projeto>\.claude\skills\
```

**Cursor**
```powershell
Copy-Item -Recurse "D:\Skills\*" "$env:USERPROFILE\.cursor\skills\"
# ou por projeto: <projeto>\.cursor\skills\
```

O formato `SKILL.md` é o mesmo nos dois. Depois de copiar, reinicie/abra o agente e
peça algo que case com a skill (ex.: *"analisa essa conversa de vendas"*).

### Dependências (instaladas pelo próprio agente)

Para a transcrição de áudio/vídeo, **o agente instala o que faltar** (Python,
ffmpeg, deps via `pip`) seguindo o "Setup automático" em `references/transcricao.md`.
Você só precisa fornecer credenciais que exigem conta/login (token HuggingFace
para diarização; dados da Evolution; chave OpenAI no fallback) — a skill ensina a
obter cada uma em `references/credenciais.md`.

## Como usar (exemplo)

1. Peça ao agente: *"Analisa as conversas do meu closer no WhatsApp."*
2. Ele pede os 3 dados da Evolution (URL, apikey, instância) e ensina onde achar.
3. Lista as conversas; você escolhe uma ou "todas".
4. Ele puxa, aplica a rubrica e entrega o relatório com notas e sugestões.

Para call gravada: mande o arquivo, informe o token HF (a skill ensina a pegar), e
o agente instala o ambiente, transcreve com locutores separados e analisa.

## O que isso NÃO é

- Não é um CRM — gera notas para colar no seu CRM, não armazena nada.
- Não é uma automação/cron — gera (e pode disparar manualmente) follow-ups, mas
  não roda agendamento sozinho. Para cadência automática por horário, use n8n.
- Não é um serviço em nuvem — roda local, no seu agente.
- Não substitui o gestor/closer — entrega diagnóstico e rascunhos; a decisão e o
  envio final são seus.

## Feito pela A Ordem

Criado e mantido pela **A Ordem**. Padrão de documentação inspirado no
`growth-os-skills` (Accelera 360).
