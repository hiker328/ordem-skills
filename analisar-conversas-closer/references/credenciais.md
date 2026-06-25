# Como obter cada credencial

Guia para o usuário pegar as chaves/dados que a skill pede. Trate todas como
**segredos**: não comite, não poste em chat público, não logue em texto.

## 1. Token do HuggingFace (para diarização no WhisperX)

Necessário **só para separar locutores** (quem é closer x cliente). Transcrição
pura não precisa. É **gratuito**.

1. Crie conta e faça login em **huggingface.co**.
2. Abra **huggingface.co/settings/tokens** (avatar → *Settings* → *Access Tokens*).
3. **Create new token** → tipo **Read** → nome (ex.: `whisperx`) → **Create**.
4. **Copie o token na hora** (formato `hf_...`). Só aparece uma vez; se perder,
   gere outro.
5. **Aceite os termos do modelo** (obrigatório, senão dá erro de acesso): logado,
   abra **huggingface.co/pyannote/speaker-diarization-community-1** e clique em
   aceitar/*Agree* (instantâneo, gratuito).
6. Use com `--hf-token hf_xxxxx` ou defina a variável de ambiente `HF_TOKEN`.

Erro "could not download / access" na diarização = token ausente ou termos do
modelo não aceitos (passo 5).

## 2. Dados da Evolution API (para puxar conversas de WhatsApp)

São 3 dados. Quem administra a instância da Evolution tem todos.

### URL base
O endereço onde a Evolution está hospedada, ex.:
`https://evolution.seudominio.com.br`. É o início da URL do painel/manager da
Evolution (sem `/manager` no final). Se você acessa o manager em
`https://evolution.seudominio.com.br/manager`, a base é a parte antes de `/manager`.

### apikey
A chave de autenticação (header `apikey`). Onde encontrar:
- **Global**: definida na variável `AUTHENTICATION_API_KEY` do `.env`/docker da
  Evolution (a chave "global" do servidor).
- **Por instância**: no **Evolution Manager**, abra a instância → a apikey/token
  dela aparece nos detalhes (ou via endpoint `GET /instance/fetchInstances`).

Use a chave que tiver permissão na instância que você vai consultar.

### nome da instância
O nome que identifica a conexão de WhatsApp dentro da Evolution (ex.:
`Luiz Augusto`). Veja no **Evolution Manager** (lista de instâncias) ou em
`GET /instance/fetchInstances`. É o que vai no fim da URL dos endpoints
(`/chat/findMessages/{instancia}`).

> Dica: rode `evolution_fetch.py ... --list` para confirmar que os 3 dados estão
> certos — ele lista as conversas da instância. Se vier erro 401/403, a apikey
> está errada ou sem permissão; 404 na instância = nome errado.

## 3. Chave da OpenAI (só para o fallback de transcrição)

Necessária **apenas** se usar o fallback da API Whisper da OpenAI (quando não dá
para rodar WhisperX local). Tem **custo por minuto** e **não** separa locutores.

1. Faça login em **platform.openai.com**.
2. Abra **platform.openai.com/api-keys** (ou *Settings* → *API keys*).
3. **Create new secret key** → copie (formato `sk-...`; só aparece uma vez).
4. Precisa ter **billing/créditos** ativos na conta para a API funcionar.
5. Use definindo a variável `OPENAI_API_KEY`.
