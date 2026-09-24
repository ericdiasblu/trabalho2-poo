# Etapa 1 — Exploração e análise do domínio

## Identificação

- **Jogo:** Nexus Heroes.
- **Descrição recebida:** labirinto 3D isométrico com conceitos de programação orientada a objetos no console.
- **Integrantes informados:** Eric Dias e Matheus Howe Habeck.
- **Fonte desta etapa:** dados fornecidos manualmente no pedido. O PDF apresenta a tarefa acadêmica, mas não traz estatísticas ou um mapa do jogo.

## Introdução e objetivo

A exploração pedida pelo enunciado busca identificar entidades, estado, comportamento, interações e regras de transição. Este registro organiza apenas as observações enviadas. Não houve acesso ao executável do jogo, a capturas de tela ou a um mapa completo; portanto, não é possível afirmar que todos os caminhos e cenários foram percorridos.

## Ambiente, caminhos e cenários

O ambiente foi descrito como um **labirinto 3D isométrico**. A legenda identifica cristal de mana, orbe de vida, inimigo, armadilha, baú e portal. O texto informa que inimigos bloqueiam o caminho até serem derrotados e que alcançar o portal conclui a fase. Não foram fornecidos dimensões, coordenadas, ordem dos encontros, quantidade de fases nem trajetos específicos. A indicação de pressionar **Espaço** em combate foi registrada como comando da interface do jogo; a implementação deste trabalho modela o domínio, sem reproduzir a entrada gráfica.

## Classes e entidades identificadas

| Entidade mencionada | Evidência recebida |
|---|---|
| Personagem, Guerreiro, Mago | Dois tipos de herói com estatísticas próprias. |
| Inimigo, Goblin, Golem | Inimigos bloqueiam a passagem, combatem e podem contra-atacar. |
| Item, HeroCoin | Itens coletáveis e moedas obtidas de inimigos e baús. |
| Cristal de Mana, Orbe de Vida | Coletáveis com bônus de mana e vida. |
| Armadilha | Causa 20 pontos de dano e é associada a `TrapDamageException`. |
| Baú | Concede XP e moedas. |
| Portal | Objetivo final da fase. |
| Mapa | Espaço de posicionamento e deslocamento. |

## Atributos e estados

Os atributos citados são nome, vida, vida máxima, mana, mana máxima, ataque, nível, XP, moedas e posição. A descrição explicita dois ataques para cada herói:

| Classe | HP máximo | Mana máxima | ATK espada | MATK magia |
|---|---:|---:|---:|---:|
| Guerreiro | 120 | 40 | 25 | 10 |
| Mago | 80 | 120 | 15 | 40 |

Não foram informados os pontos de vida, o ataque e a recompensa de Goblin/Golem; o limiar de XP e o aumento de ataque por nível; nem a quantidade de XP/moedas dada pelo baú. Esses números são parâmetros explícitos do modelo. O usuário confirmou que devem continuar configuráveis.

## Métodos e comportamentos

As ações registradas na Etapa 1 são andar, atacar, atacar com espada, coletar, receber dano, alterar vida, alterar mana e subir de nível. A legenda associa cristal a `setMana()`, orbe a `setVida()` e inimigos à sobrescrita de `calcularDano()`. O baú cria ou concede `HeroCoin`. O portal encerra a fase.

## Interações observadas

| Símbolo | Origem | Interação | Consequência informada |
|---|---|---|---|
| 💎 | Personagem → cristal | Coleta | +25 mana, respeitando o máximo. |
| 🍀 | Personagem → orbe | Coleta | +20 HP, respeitando o máximo. |
| 👾 | Personagem ↔ inimigo | Combate | Inimigo bloqueia a passagem enquanto vivo e pode contra-atacar. |
| ⚠️ | Personagem → armadilha | Acionamento | −20 HP e `TrapDamageException`. |
| 📦 | Personagem → baú | Abertura | Recebe XP e Hero Coins. |
| 🌀 | Personagem → portal | Entrada | Conclui a fase. |

## Invariantes e transições

1. `0 ≤ vida ≤ vidaMáxima` e `0 ≤ mana ≤ manaMáxima` em todos os estados.
2. Inimigo vivo bloqueia a passagem; sua derrota libera o avanço e concede Hero Coins.
3. Inimigo sobrevivente pode contra-atacar; armadilhas causam dano.
4. Ao subir de nível, HP e mana são restaurados aos respectivos máximos e o ataque aumenta.
5. A entrada no portal conclui a fase.

## Limites da observação e decisões posteriores

Não há evidência sobre custo de mana de magia, fórmulas especiais de dano, inventário, mapa real ou regras distintas para Goblin e Golem. Nenhum desses comportamentos foi atribuído ao jogo. Para tornar o domínio executável, a Etapa 2 registra decisões técnicas pontuais, como coordenadas lógicas e parâmetros de progressão; elas são identificadas como decisões de modelagem, não como descobertas da exploração.

## Conclusão

Os dados recebidos sustentam um modelo de combate, coleta, progressão e conclusão de fase, com herança entre combatentes e especialização de dano. A análise cobre fielmente as informações manuais, mas não substitui uma exploração exaustiva do jogo original, pois seus caminhos e cenários não foram fornecidos.
