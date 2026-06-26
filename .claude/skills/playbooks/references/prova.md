# Prova — Construtor de Playbook (Vendas ou Tráfego)

> Exemplo com dados FICTÍCIOS. Mostra o tipo de saída que a solução gera. Aqui usamos o MODO VENDAS (o modo Tráfego segue a mesma lógica, com a estrutura de campanhas).

## Contexto informado (fictício)
```
Modo: A (Vendas)
Nicho: clínicas de estética de pequeno porte
Oferta: pacote de gestão de agenda + recuperação de pacientes inativos, ticket médio R$ 1.800/mês
Lead chega: anúncio no Instagram, atendido por WhatsApp
Time: 1 SDR que qualifica + 1 closer que fecha em reunião online
Maior dor: lead some depois da primeira resposta; ninguém faz follow-up de forma padronizada
Ciclo: médio (qualifica num dia, reunião em outro)
```

## Output esperado (trecho)
```
# Playbook de Vendas — clínicas de estética de pequeno porte

## 1. ICP — Perfil de Cliente Ideal
Cliente ideal: clínica com 1-3 cadeiras, dona-operadora que ainda responde o WhatsApp,
agenda cheia de buraco e base de pacientes antigos sem recompra.
NÃO é: rede grande com gestor próprio, ou clínica recém-aberta sem base.
Critérios de qualificação:
- Orçamento: fatura acima de [PERSONALIZAR] R$/mês (suporta o ticket de R$ 1.800).
- Autoridade: quem responde é a dona ou tem que chamar sócio? (definir na qualificação)
- Necessidade: tem base de inativos? Tem buraco na agenda?
- Urgência: o buraco na agenda dói esse mês ou dá pra empurrar?

## 2. Mapa de Objeções (com quebras)
Objeção: "Vou pensar e te aviso."
O que está por trás: falta clareza do retorno OU não é prioridade agora.
Como quebrar:
- Pergunta de implicação: "Enquanto você pensa, a agenda segue com buraco e os
  inativos seguem sem recompra. Quanto isso custa por mês pra você?"
- Condicional de avanço: "Se eu te mostrar agora quanto a recuperação de inativos
  traria no primeiro mês, faz sentido decidir hoje?"

Objeção: "Tá caro."
O que está por trás: comparando o custo direto, não o retorno.
Como quebrar:
- "Faz sentido. Olhando o número: com ticket de [PERSONALIZAR] por paciente, quantas
  recompras pagam os R$ 1.800? Geralmente são poucas." (faz a conta com o dado dele)

## 3. Scripts por Etapa do Funil
### Abordagem (SDR, no WhatsApp)
"Oi [nome], aqui é o [SDR] da [PERSONALIZAR — empresa]. Vi que você pediu informação
sobre [oferta]. Pra te indicar o caminho certo, posso te fazer 3 perguntas rápidas?
Leva 2 minutos."

### Qualificação (SDR)
- Necessidade: "Hoje sua agenda fica cheia ou tem buraco em alguma semana?"
- Autoridade: "A decisão de contratar é só sua ou tem sócio?"
[...comentário de autoridade após cada resposta, pra não virar interrogatório...]

### Follow-up (o que resolve a dor declarada)
Cadência fixa — o time para de improvisar:
- D+0: respondeu e sumiu -> "Ficou alguma dúvida do que conversamos?"
- D+1: "Separei um exemplo de clínica parecida com a sua, posso te mandar?"
- D+3: "Consigo segurar o horário da reunião até amanhã. Fechamos?"
- D+7: último toque -> "Vou encerrar por aqui pra não te incomodar. Se mudar de
  ideia, é só chamar." (e move pra base de reativação)

## 4. Métricas do Funil
Taxa de resposta no WhatsApp | mede a abordagem | alerta se < [PERSONALIZAR]%
Taxa de comparecimento na reunião | mede a qualificação | alerta se < [PERSONALIZAR]%
Conversão reunião -> fechamento | mede o closer | alerta se < [PERSONALIZAR]%
```

## Por que funciona
A saída sai do contexto que o usuário colou (nicho, oferta, ticket, time, dor) — não é genérica.
A dor declarada ("ninguém faz follow-up padronizado") vira a cadência fixa D+0/D+1/D+3/D+7 no
script, que é exatamente o que faltava. E todo número do negócio aparece como `[PERSONALIZAR]`,
porque a IA não inventa a meta nem o ticket do cliente — quem preenche é o time.
