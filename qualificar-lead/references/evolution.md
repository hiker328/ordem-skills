# Evolution API — puxar conversas de WhatsApp

Método validado no fluxo "Disparo de FUPs" (Luiz Augusto). A Evolution API expõe
as conversas da instância conectada via HTTP. Autenticação é sempre pelo header
`apikey`.

## Endpoints usados

Base = a URL da instância (ex.: `https://evolution.seudominio.com.br`).

### Listar conversas
```
POST {base}/chat/findChats/{instance}
Header: apikey: <KEY>
Body: {}            # opcional; alguns deploys aceitam filtros
```
Retorna a lista de chats. Cada item traz (nomes variam por versão):
- `remoteJid` — identificador do contato (ex.: `5511999999999@s.whatsapp.net`)
- `pushName` / `name` — nome do contato
- `lastMessage` / `updatedAt` — última atividade

### Buscar mensagens de uma conversa
```
POST {base}/chat/findMessages/{instance}
Header: apikey: <KEY>
Body: { "where": { "key": { "remoteJid": "<JID>" } } }
```
Retorna as mensagens daquele contato. Campos relevantes por mensagem:
- `key.fromMe` (bool) — **true = mensagem enviada pela instância (o CLOSER)**;
  **false = mensagem do contato (o CLIENTE)**. É assim que rotulamos os papéis.
- `key.remoteJid`
- `messageTimestamp` (epoch em segundos)
- `pushName` — nome de quem enviou (quando vem do contato)
- conteúdo de texto, conforme o tipo:
  - `message.conversation` (texto simples)
  - `message.extendedTextMessage.text` (texto com contexto/reply)
  - `message.imageMessage.caption`, `message.videoMessage.caption` (legendas)
  - áudio/figurinha/documento → sem texto (o script marca como `[áudio]`, etc.)

## remoteJid x número

O usuário normalmente sabe o **número** (ex.: `5511999999999`). O script monta o
`remoteJid` automaticamente (`<numero>@s.whatsapp.net`) se você passar só o número
em `--jid`. Para grupos o JID termina em `@g.us` — use `--list` para descobrir.

## Notas de robustez

- A resposta de `findMessages` pode vir como array direto, ou aninhada em
  `messages.records` / `messages` dependendo da versão. O script trata os casos.
- `findChats` em algumas versões é `GET`; o script tenta `POST` e cai para `GET`.
- Ordene as mensagens por `messageTimestamp` antes de formatar (o script já faz).
- A `apikey` é sensível — não logue em texto, não comite. Trate como segredo.

## Formato de saída do script

Transcrição pronta para análise, uma linha por mensagem:

```
[2026-06-20 14:03] Closer: Oi João, tudo bem? Vi que você baixou o material...
[2026-06-20 14:05] Cliente: Tudo e você? Sim, baixei ontem
[2026-06-20 14:06] Closer: Show. Me conta, qual o maior desafio hoje com...
```
