# A Ordem — Skills (para Agências)

> Suíte de **Agent Skills** (formato `SKILL.md`) para Claude Code / Cursor, feita
> para **agências de marketing/tráfego**: transforma o agente numa ferramenta de
> *enablement* dos closers que vendem os serviços da agência — analisar, treinar,
> qualificar, recuperar e registrar conversas comerciais.
> Feito pela **A Ordem**.

---

## O que é

Um time de skills que rodam dentro do Claude Code (ou Cursor) e executam tarefas
comerciais da **agência** de ponta a ponta, em português. Seus closers vendem
serviço (gestão de tráfego, social, performance) e essas skills auditam e elevam
esse jogo. Você pede em linguagem natural ("analisa as conversas do meu closer",
"qualifica esses leads que vieram do anúncio", "treina o closer no contorno de
'agência é tudo igual'") e o agente carrega a skill certa, puxa os dados, aplica
uma rubrica consistente e entrega o resultado — sempre do mesmo jeito, em escala.

São **5 skills** que se encaixam num fluxo:
**analisar → treinar → qualificar → recuperar (follow-up) → registrar (CRM).**

## Pra quem é

- **Donos e head comercial de agências** que querem auditar e treinar seus closers.
- **Gestores de agência** que vendem serviço recorrente (fee/retainer) e dependem
  da qualidade da conversa para fechar.
- **Operações que usam Evolution API** (WhatsApp) e querem trabalhar conversas reais
  com leads vindos de tráfego.

## Início rápido

```bash
# 1) Clona o repo numa pasta de trabalho
git clone https://github.com/hiker328/ordem-skills.git

# 2) Entra na pasta
cd ordem-skills

# 3) Abre o Claude Code aqui dentro — as skills em .claude/skills são detectadas
claude
> analisa essa conversa de vendas    # ou /analisar-conversas-closer
```

Rodando o `claude` de dentro do repo, as skills em `.claude/skills/` são
reconhecidas automaticamente como skills do projeto. Cada usuário cria a sua pasta,
clona o repo e trabalha lá dentro.

**Quer as skills disponíveis em qualquer projeto?** Copie para o diretório pessoal:

```powershell
# Claude Code
Copy-Item -Recurse "ordem-skills\.claude\skills\*" "$env:USERPROFILE\.claude\skills\"
# Cursor
Copy-Item -Recurse "ordem-skills\.claude\skills\*" "$env:USERPROFILE\.cursor\skills\"
```

## Como o conjunto é organizado

Cada skill segue o mesmo padrão de 3 camadas (*progressive disclosure*):

```
SKILL.md         →  orquestrador: o agente lê primeiro. Decide o fluxo e roteia.
references/*.md  →  conhecimento detalhado, lido só quando necessário.
scripts/*        →  trabalho mecânico/determinístico (puxar dados, transcrever).
```

Princípio central: **o julgamento é do agente; o mecânico é dos scripts.** O agente
faz a análise (lendo a rubrica); os scripts só executam o que é frágil ou repetitivo
(chamar a API, rodar ffmpeg/WhisperX). Isso mantém o `SKILL.md` enxuto e o resultado
consistente.

## As skills

### `analisar-conversas-closer`
Avalia a performance de um closer e gera relatório com notas (0–100), pontos fortes,
erros e sugestões. Fontes: **WhatsApp (Evolution)**, **texto colado** ou
**áudio/vídeo** (transcrição local com WhisperX + diarização).

### `treinar-closer`
Treino por **role-play**: o agente encarna um cliente (frio, indeciso, agressivo,
interessado) num cenário/produto, conduz a conversa e no fim pontua com a rubrica e
dá feedback. Sem scripts — conversa guiada.

### `qualificar-lead`
**Lead scoring** 0–100 e faixa (quente/morno/frio/desqualificado) por 6 critérios
(dor, fit, orçamento, decisor, urgência, engajamento). Uma conversa, texto colado ou
**lote** ranqueado. Fonte via Evolution.

### `gerar-followup`
Recupera conversas paradas: detecta o estágio na **cadência** (FUP-1..6) e gera a
próxima mensagem (ou a sequência inteira), personalizada. Pode **enviar** pela
Evolution — sempre após aprovação do texto.

### `resumir-call-para-crm`
Call gravada → **notas estruturadas de CRM** (dor, contexto, orçamento, decisor,
objeções, próximos passos com data). Transcreve local com WhisperX + diarização.

## Por que essa arquitetura é diferente

**1. Tudo em arquivos comuns. Sem banco de dados.**
Markdown e Python puro. Cabe num pendrive, abre em qualquer editor. Na prática:
- **Portátil** — a skill é só uma pasta.
- **Auditável** — cada instrução, rubrica e script é um arquivo que você lê.
- **Reversível** — `git revert` desfaz qualquer experimento que deu errado.

**2. O julgamento é separado do mecânico.**
O que exige raciocínio (análise, feedback, follow-up) fica em texto, feito pelo
agente. O que é frágil/repetitivo (API, ffmpeg, WhisperX) fica em script. Você
troca a rubrica sem mexer no código, e troca o código sem mexer no critério.

**3. Cada passo sensível é validado antes de agir.**
A skill não age às cegas: a `gerar-followup` **nunca envia** sem o texto ser
aprovado; a transcrição **confere o ambiente** (Python, ffmpeg, deps) antes de
rodar; toda nota se apoia em **citação real** da conversa, não em suposição.

**4. Local e sem custo recorrente.**
A transcrição de áudio/vídeo roda na sua máquina (WhisperX + diarização) — sem
mandar áudio pra fora e sem custo por minuto de API.

## Estrutura de pastas

```
ordem-skills/                         # raiz do repo
├── README.md
├── LICENSE
├── .gitignore
├── examples/                         # amostras fictícias de entrada e saída
├── tests/                            # testes das funções dos scripts (sem rede)
├── templates/
│   └── workspace/                    # layout sugerido de pasta de trabalho + .env.example
└── .claude/
    └── skills/
        ├── analisar-conversas-closer/
        │   ├── SKILL.md
        │   ├── references/  (rubrica, evolution, transcricao, credenciais)
        │   └── scripts/     (evolution_fetch.py, transcribe.py, requirements.txt)
        ├── treinar-closer/
        │   ├── SKILL.md
        │   └── references/  (perfis-cliente, rubrica)
        ├── qualificar-lead/
        │   ├── SKILL.md
        │   ├── references/  (scoring, evolution, credenciais)
        │   └── scripts/     (evolution_fetch.py, requirements.txt)
        ├── gerar-followup/
        │   ├── SKILL.md
        │   ├── references/  (cadencia, evolution, credenciais)
        │   └── scripts/     (evolution_fetch.py, evolution_send.py, requirements.txt)
        └── resumir-call-para-crm/
            ├── SKILL.md
            ├── references/  (formato-crm, transcricao, credenciais)
            └── scripts/     (transcribe.py, requirements.txt)
```

Cada skill é **auto-contida**: os docs/scripts compartilhados (Evolution,
transcrição, credenciais) ficam copiados dentro de cada uma, para poderem ser
instaladas individualmente.

**Pastas de apoio:**
- `examples/` — amostras fictícias de entrada e do que cada skill entrega.
- `templates/workspace/` — layout sugerido de pasta de trabalho + `.env.example`
  com as credenciais usadas pelas skills.
- `tests/` — testes das funções dos scripts (parsing/formatação, sem rede). Rode
  com `python tests/test_scripts.py` (precisa de `requests` instalado).

## Dependências (instaladas pelo próprio agente)

Para a transcrição de áudio/vídeo, **o agente instala o que faltar** (Python,
ffmpeg, deps via `pip`) seguindo o "Setup automático" de `references/transcricao.md`.
Você só fornece credenciais que exigem conta/login (token HuggingFace para
diarização; dados da Evolution; chave OpenAI no fallback) — a skill ensina a obter
cada uma em `references/credenciais.md`.

## Como usar (exemplo)

1. Peça ao agente: *"Analisa as conversas do meu closer no WhatsApp."*
2. Ele pede os 3 dados da Evolution (URL, apikey, instância) e ensina onde achar.
3. Lista as conversas; você escolhe uma ou "todas".
4. Ele puxa, aplica a rubrica e entrega o relatório com notas e sugestões.
5. Em seguida: *"treina esse closer no ponto fraco"*, *"qualifica esses leads"* ou
   *"gera o follow-up pros que ficaram parados"*.

## O que isso NÃO é

- Não é um CRM — gera notas para colar no seu CRM, não armazena nada.
- Não é uma automação/cron — gera (e dispara manualmente) follow-ups, mas não roda
  agendamento sozinho. Para cadência automática por horário, use n8n.
- Não é um serviço em nuvem — roda local, no seu agente.
- Não substitui o gestor/closer — entrega diagnóstico e rascunhos; a decisão e o
  envio final são seus.

## Feito pela A Ordem

Criado e mantido pela **A Ordem**. Estrutura e documentação inspiradas no
`growth-os-skills` (Accelera 360). Licença MIT (ver `LICENSE`).
