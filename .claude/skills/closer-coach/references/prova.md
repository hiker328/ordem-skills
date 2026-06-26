# Prova — Closer Coach

> Exemplo com dados FICTÍCIOS. Mostra o tipo de análise que a solução gera a partir de uma transcrição.

## Input de exemplo (colado)
```
Contexto: venda de serviço de gestão de tráfego, ticket ~R$ 4.000/mês, call de fechamento.
Transcrição (trecho):

[00:02] Closer: Oi Marina, tudo bem? Bom, deixa eu te apresentar o que a gente faz.
A gente cuida de tráfego pago, tem 6 anos de mercado, atende mais de 40 clientes...
[00:09] Marina: Legal. A gente já roda anúncio hoje, mas não sei se vale trocar.
[00:10] Closer: Vale muito, a gente é muito bom nisso. Nosso método é completo.
[00:14] Marina: É que o orçamento aqui esse trimestre tá apertado, sabe?
[00:15] Closer: Imagina, a gente dá um jeito. Então, fechando hoje, eu começo semana que vem.
[00:16] Marina: Deixa eu pensar e te falo.
[00:16] Closer: Tá certo, qualquer coisa me chama!
```

## Output esperado (trecho)
```
1. NOTA DA REUNIÃO: 3/10
Critério: a call foi de fechamento, mas o closer pulou descoberta e tratou a única
objeção real (orçamento) com uma frase solta. Terminou sem próximo passo combinado —
exatamente o que mais derruba taxa de fechamento.

2. PONTOS FORTES
- Abriu com credibilidade objetiva. Trecho [00:02]: "tem 6 anos de mercado, atende
  mais de 40 clientes". Funciona como prova social no início (etapa de autoridade).

3. ERROS COMETIDOS
- Não fez descoberta (mais grave). Trecho [00:10]: respondeu "vale muito, a gente é
  muito bom" sem uma pergunta sequer. Pulou o S e o P do SPIN. Impacto: vendeu no
  escuro, sem saber a dor da Marina — fica caro pra ela justificar o gasto.
- Ignorou a objeção de orçamento. Trecho [00:15]: "imagina, a gente dá um jeito"
  não trata o "trimestre apertado". Impacto: a objeção crítica (Budget no BANT)
  continua viva e vira o motivo do "deixa eu pensar".
- Fechou sem próximo passo. Trecho [00:16]: "qualquer coisa me chama" devolve a
  iniciativa pro lead. Impacto: a call esfria e a venda fica refém da Marina lembrar.

4. MELHORIAS ACIONÁVEIS
- Em vez de "vale muito, a gente é muito bom", diga: "Antes de te falar se vale, me
  conta: o que te fez aceitar essa conversa? O que tá te incomodando no tráfego hoje?"
- Em vez de "imagina, a gente dá um jeito", trate o orçamento: "Faz sentido olhar o
  custo. Se eu te mostrar quanto você deixa na mesa hoje por mês, a conta muda. Posso?"
- Em vez de "qualquer coisa me chama", marque o passo: "Combina assim: quinta às 15h
  eu te trago uma simulação com os seus números. Fecha na sua agenda?"

5. PRÓXIMOS PASSOS
A call terminou SEM próximo passo — prioridade. Hoje: mandar mensagem propondo data e
hora fixas pra um diagnóstico de 20 min focado no custo atual dela. Levar uma estimativa
de retorno pro ticket de R$ 4.000/mês. VERIFICAR: a transcrição não diz se a Marina é a
decisora final do orçamento — confirmar isso na próxima.
```

## Por que funciona
A análise não inventa nada: cada nota, erro e melhoria sai de um trecho real da transcrição. Os frameworks entram como lente (SPIN para a descoberta pulada, BANT para o orçamento ignorado, o arco do funil para o fechamento sem próximo passo), e a melhoria já vem como fala pronta — o closer aplica na próxima call sem traduzir teoria.
