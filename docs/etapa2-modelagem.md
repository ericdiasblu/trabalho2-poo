# Etapa 2 — Modelagem de classes UML

O diagrama entregue está em [diagrama-classes.drawio](diagrama-classes.drawio), XML nativo do diagrams.net. Cada classe, atributo, método, nota e conector é uma célula editável. O script local [`tools/gerar_diagrama.py`](../tools/gerar_diagrama.py) permite recriar o arquivo após uma alteração arquitetural.

## Arquitetura

O domínio separa quatro responsabilidades: **estado e combate** (`Combatente`, `Personagem`, `Inimigo` e especializações), **efeitos coletáveis** (`Item` e especializações), **eventos de mapa** (`Bau`, `Armadilha`, `Portal`) e **navegação lógica** (`Mapa`, `Posicao`, `ElementoMapa`). `Main` apenas demonstra interações. `TrapDamageException` comunica o acionamento da armadilha depois de aplicar o dano.

### Classes, estado, construção e operações

As assinaturas completas, com tipos, visibilidade e retorno, estão nos compartimentos do diagrama. A tabela resume as responsabilidades e a correspondência com o código:

| Classe | Responsabilidade | Atributos declarados | Construtor e operações principais |
|---|---|---|---|
| `Posicao` (`record`) | Coordenada lógica imutável | `x:int`, `y:int` | `Posicao(int,int)`; `x()`, `y()`, `adjacente(Posicao):boolean`. |
| `ElementoMapa` (`interface`) | Contrato de entrada numa posição | Nenhum | `interagir(Personagem):boolean`, podendo lançar `TrapDamageException`. |
| `Combatente` (abstrata) | Vida, nome, posição e contrato de dano | `nome:String`, `vida:int`, `vidaMaxima:int`, `posicao:Posicao` | Construtor protegido; getters, `setVida`, `receberDano`, `estaVivo`, `moverPara` de pacote e `calcularDano` abstrato. |
| `Personagem` (abstrata) | Recursos, ataques, moedas, XP e níveis do herói | `mana:int`, `manaMaxima:int`, `ataqueEspada:int`, `ataqueMagia:int`, `nivel:int`, `experiencia:int`, `moedas:int`, `experienciaPorNivel:int`, `incrementoAtaque:int` | Construtor protegido; getters, `setMana`, `atacar`, `atacarComEspada`, `coletar`, `andar`, `ganharExperiencia`, `receberMoedas`; `subirNivel` privado; operação protegida abstrata `aumentarAtaque`. |
| `Guerreiro` | Herói cujo ataque principal é a espada | Nenhum novo | Construtor público fixa `120/40/25/10`; sobrescreve `calcularDano` e `aumentarAtaque`. |
| `Mago` | Herói cujo ataque principal é magia | Nenhum novo | Construtor público fixa `80/120/15/40`; sobrescreve `calcularDano` e `aumentarAtaque`. |
| `Inimigo` (abstrata) | Bloqueio, contra-ataque e recompensa única | `ataque:int`, `recompensa:HeroCoin`, `recompensaEntregue:boolean` | Construtor protegido; `getAtaque` protegido, `contraAtacar`, `entregarRecompensa`, `interagir` e `calcularDano` abstrato. |
| `Goblin`, `Golem` | Tipos identificados de inimigo | Nenhum novo | Construtores públicos com HP, ataque, moedas e posição configuráveis; ambos sobrescrevem `calcularDano`. |
| `Item` (abstrata) | Nome e contrato de efeito coletável | `nome:String` | Construtor protegido; `getNome`, `interagir` e `aplicarEm` abstrato. |
| `HeroCoin` | Concede moedas | `quantidade:int` | `HeroCoin(int)`; sobrescreve `aplicarEm`. |
| `CristalMana` | Recupera até 25 de mana | Constante privada `BONUS_MANA:int=25` | Construtor sem argumentos; sobrescreve `aplicarEm`. |
| `OrbeVida` | Recupera até 20 de vida | Constante privada `BONUS_VIDA:int=20` | Construtor sem argumentos; sobrescreve `aplicarEm`. |
| `Bau` | Entrega XP e HeroCoin uma vez | `experiencia:int`, `moeda:HeroCoin`, `aberto:boolean` | `Bau(int,int)`; `isAberto`, `interagir`. |
| `Armadilha` | Aplica 20 de dano e sinaliza o evento | Constante privada `DANO:int=20` | Construtor sem argumentos; `interagir` lança `TrapDamageException`. |
| `Portal` | Autoriza a conclusão da fase | Nenhum | Construtor sem argumentos; `interagir`. |
| `Mapa` | Posiciona elementos, valida deslocamento e registra conclusão | `largura:int`, `altura:int`, `elementos:Map<Posicao,ElementoMapa>`, `concluido:boolean` | `Mapa(int,int)`; `posicionar`, `getElemento`, `andar`, `isConcluido`; `exigirDentro` privado. |
| `TrapDamageException` | Transporta o dano do evento de armadilha | `dano:int` | `TrapDamageException(int)`; `getDano`. |
| `Main` | Simulação de console | Nenhum | Construtor privado e `main(String[]):void` estático. |

## Relacionamentos e multiplicidades

- **Generalização, linha contínua e triângulo vazado:** `Personagem` e `Inimigo` são `Combatente`; `Guerreiro`/`Mago` são `Personagem`; `Goblin`/`Golem` são `Inimigo`; `HeroCoin`/`CristalMana`/`OrbeVida` são `Item`. `TrapDamageException` estende `Exception` da biblioteca Java.
- **Realização, linha tracejada e triângulo vazado:** `Inimigo`, `Item`, `Bau`, `Armadilha` e `Portal` implementam `ElementoMapa`.
- **Agregação, losango vazado:** um `Mapa` referencia `0..*` `ElementoMapa`. Um elemento pode existir fora do mapa, como nos testes e na demonstração.
- **Composição, losango preenchido:** cada `Bau` possui uma `HeroCoin` e cada `Inimigo` possui uma `HeroCoin` de recompensa. A moeda é criada pelo proprietário e seu valor é incorporado ao contador do herói na entrega.
- **Associação simples:** cada `Combatente` possui exatamente uma `Posicao`; a interação de combate liga `Personagem` a `Inimigo` em encontros `0..*`.
- **Dependência:** `Mapa` usa `Personagem` para mover e `Armadilha` lança `TrapDamageException`. Os parâmetros de métodos também evidenciam dependências de `Personagem` com `Mapa` e `Item`.

## Justificativa da herança e sobrescrita

`Combatente` reúne apenas estado e comportamento que heróis e inimigos realmente compartilham: nome, vida, posição, dano e sobrevivência. A relação **é um** é verdadeira para ambos. `Personagem` centraliza progressão e recursos exclusivos dos heróis; `Inimigo` centraliza bloqueio e recompensa. `Guerreiro` e `Mago` sobrescrevem `calcularDano():int` para usar, respectivamente, ATK espada e MATK magia; também especializam `aumentarAtaque(int):void` para aumentar somente o ataque principal. `Goblin` e `Golem` sobrescrevem `calcularDano():int` para devolver o ataque recebido no construtor. Não há fórmula distinta documentada para eles, por isso nenhuma foi criada. Os itens sobrescrevem `aplicarEm(Personagem):void` com efeitos específicos.

## Invariantes e regras de transição

| Classe/grupo | Invariante e transição |
|---|---|
| `Posicao`, `Mapa` | Coordenadas não negativas; dimensões positivas; posições usadas no mapa permanecem dentro dos limites. Uma posição comporta até um elemento. |
| `Combatente` | Nome não vazio, `vidaMaxima > 0`, `0 ≤ vida ≤ vidaMaxima`, posição não nula. Dano não negativo; dano excessivo limita vida a zero. |
| `Personagem` | `0 ≤ mana ≤ manaMaxima`, ataques não negativos, nível inicia em 1, XP e moedas não negativos; limiar de XP e incremento de ataque positivos. Cada limiar de XP aumenta um nível, restaura HP/mana e aumenta o ataque principal. Personagem derrotado não age. |
| `Inimigo` | Ataque não negativo, recompensa positiva. Vivo bloqueia passagem; sobrevivente contra-ataca após ataque do herói; derrotado libera passagem; a recompensa é entregue uma vez. |
| `Item` e especializações | Nome não vazio; HeroCoin positiva; cristal/orbe saturam no máximo, sem excedê-lo. Item de mapa é removido depois da coleta. |
| `Bau`, `Armadilha`, `Portal` | Baú tem XP e moedas positivos e não premia duas vezes. Armadilha aplica 20 HP com piso zero e lança exceção. Entrar no portal marca `Mapa.concluido = true`. |

## Decisões arquiteturais não observadas no jogo

O mapa usa coordenadas inteiras bidimensionais porque a projeção 3D isométrica é visual e o domínio só precisa de posição lógica. O movimento permitido é ortogonal, de uma casa por chamada, como critério mínimo de consistência; isso **não afirma** a topologia do mapa original. Numa armadilha, o dano é aplicado e a exceção impede a atualização de posição; também é uma decisão da simulação. A capacidade informada de contra-ataque foi implementada de modo determinístico: todo inimigo que sobrevive ao golpe responde. Depois da conclusão da fase, o mapa recusa movimentos. Os limiares de XP, os incrementos de ataque, as estatísticas dos inimigos e as recompensas são argumentos obrigatórios: nenhum valor ausente foi tratado como regra oficial. Não se modela custo de mana de magia, pois ele não foi informado.

## Encapsulamento, coesão e acoplamento

Os campos são privados; não há acesso direto ao estado mutável. `setVida` e `setMana` validam intervalos. Os métodos de recompensa e progressão validam quantidades, e `Math.addExact` impede transbordamento silencioso. Construtores protegidos existem somente nas bases abstratas. O acesso protegido a `getAtaque` e aos dois métodos que aumentam ataque é necessário para implementar as especializações sem abrir os campos; `moverPara` tem visibilidade de pacote para que apenas o mapa do domínio altere a posição. `ElementoMapa` evita que `Mapa` dependa de cada implementação para a interação básica. Cada classe concentra uma razão de mudança: combate, efeito de item, evento ou navegação.
