# TRABALHO 2 — PROGRAMAÇÃO ORIENTADA A OBJETOS

## Capa

| Campo | Preenchimento |
|---|---|
| Instituição | [Inserir instituição] |
| Curso | [Inserir curso] |
| Disciplina | [Inserir disciplina] |
| Professor(a) | [Inserir nome] |
| Integrantes | Eric Dias; Matheus Howe Habeck |
| Cidade | [Inserir cidade] |
| Data | [Inserir data] |

**Título:** Modelagem UML e implementação orientada a objetos do domínio de *Nexus Heroes*.

## 1. Introdução

Este trabalho modela as regras de domínio do jogo Nexus Heroes e as traduz para Java. O enunciado da disciplina exige abstração, um diagrama de classes semanticamente correto, construtores válidos, encapsulamento, invariantes, herança e métodos sobrescritos. A fonte das regras concretas do jogo é a descrição manual da Etapa 1 recebida junto ao pedido. O jogo é descrito como um labirinto 3D isométrico, mas o escopo do projeto é o domínio em console, não a reprodução da interface. O [diagrama editável](diagrama-classes.drawio) e a documentação específica das [Etapas 1](etapa1-exploracao.md), [2](etapa2-modelagem.md) e [3](etapa3-implementacao.md) complementam este relatório.

## 2. Objetivos

O objetivo geral é implementar uma arquitetura de classes coesa e de baixo acoplamento para os comportamentos informados. Os objetivos específicos são identificar entidades e transições de estado; representar herança, visibilidade, construtores e relações em UML; proteger os limites de vida e mana; implementar combate, recompensas, progressão, coleta, armadilha e conclusão da fase; e validar o domínio com testes automatizados.

## 3. Etapa 1 — Exploração do ambiente

### 3.1 Dados recebidos

Foram identificados Guerreiro, Mago, Goblin, Golem, itens, HeroCoin, armadilha, baú, portal e mapa. O Guerreiro possui HP máximo 120, mana máxima 40, ATK espada 25 e MATK magia 10. O Mago possui HP máximo 80, mana máxima 120, ATK espada 15 e MATK magia 40. O cristal concede 25 de mana; o orbe, 20 HP; a armadilha, 20 de dano; o baú, XP e moedas; e o portal encerra a fase. Inimigos vivos bloqueiam o caminho, podem contra-atacar e concedem Hero Coins depois de derrotados. A subida de nível restaura HP/mana e aumenta o ataque.

### 3.2 Limite da observação

O material não fornece mapa, coordenadas, trajetos, quantidade de fases, estatísticas dos inimigos ou números da progressão. Assim, este relatório não afirma que caminhos específicos foram explorados. Os valores ausentes ficaram configuráveis, conforme confirmação do solicitante. A tabela detalhada de entidades, ações e invariantes está em [etapa1-exploracao.md](etapa1-exploracao.md).

## 4. Etapa 2 — Modelagem UML

### 4.1 Estrutura

`Combatente` abstrai nome, vida e posição. `Personagem` especializa o estado dos heróis com mana, ataques, nível, XP e moedas. `Inimigo` especializa bloqueio, contra-ataque e recompensa. Guerreiro e Mago são tipos de `Personagem`; Goblin e Golem são tipos de `Inimigo`. `Item` representa objetos coletáveis, com `HeroCoin`, `CristalMana` e `OrbeVida` como especializações. `ElementoMapa` define uma interação uniforme para inimigos, itens, baús, armadilhas e portal. `Mapa` coordena posicionamento e entrada; `Posicao` é um valor imutável. `TrapDamageException` sinaliza o acionamento da armadilha.

### 4.2 Hierarquia, relações e responsabilidades

A hierarquia corresponde ao princípio **é um**: todo Guerreiro é Personagem e Combatente; todo Goblin é Inimigo e Combatente. `calcularDano()` é declarado em `Combatente` e implementado nas quatro classes concretas. O Guerreiro usa o ataque de espada e o Mago usa o ataque mágico. Como não foi informada diferença de fórmula entre Goblin e Golem, ambos devolvem o valor de ataque configurado. O mapa agrega seus elementos sem possuir seu ciclo de vida; baú e inimigo compõem cada um a própria HeroCoin de recompensa. A ligação de combate entre personagem e inimigo é uma associação, e as chamadas de movimento e exceção são dependências. Visibilidades, assinaturas, multiplicidades e notas de invariantes aparecem no diagrama.

### 4.3 Invariantes

Vida e mana pertencem aos intervalos fechados de zero a seus máximos. A vida recebe piso zero ao sofrer dano; bônus de coleta param no valor máximo. O construtor impede nomes vazios, estatísticas inválidas e posições negativas. O baú só remunera uma vez; o inimigo só entrega a recompensa depois da derrota e apenas uma vez. A posição não muda diante de inimigo vivo. O portal marca a fase concluída. A [documentação da modelagem](etapa2-modelagem.md) registra também decisões necessárias que não são fatos observados do jogo, como movimento ortogonal e limiar de XP parametrizado.

## 5. Etapa 3 — Implementação Java

O projeto usa Java 21 como alvo de compilação, Maven e um pacote `br.edu.nexusheroes`. A implementação acompanha as classes e assinaturas do [diagrama](diagrama-classes.drawio). Atributos mutáveis ficam privados; objetos recebem os dados obrigatórios no construtor; `final` protege referências e operações que não devem ser redefinidas. Os construtores de subclasses chamam `super(...)`, e todos os métodos sobrescritos são marcados com `@Override`. Métodos protegidos aparecem somente quando a subclasse precisa especializar o ataque.

O ataque do personagem aplica dano ao inimigo; se este sobreviver, responde; se for derrotado, entrega HeroCoin. XP acumulado pode gerar uma ou mais subidas de nível, restaurando recursos e aumentando o ataque principal. O mapa valida a entrada, consulta o elemento de destino, consome itens e registra a conclusão pelo portal. A classe `Main` oferece uma sequência didática no console, com estatísticas desconhecidas explicitamente tratadas como exemplos configuráveis. Não foi criado custo de mana para magia, pois esse valor não foi informado.

```text
Guerreiro: HP 120, mana 40, dano 25
Mago: HP 80, mana 120, dano 40
Goblin vivo bloqueia: true
Contra-ataque: HP do guerreiro = 113
Baú: nível 2, HP 120, mana 40, ataque espada 28, moedas 5
Fase concluída: true
Armadilha: 20 dano, HP do mago = 50
Mago: mana 120, moedas 4, dano 40
```

## 6. Testes e validação

Os testes JUnit 5 exercitam construção, dados inválidos, limites de vida e mana, recuperação por itens, transição de nível, bloqueio, combate, contra-ataque, recompensa única, baú, armadilha, portal, transições proibidas e polimorfismo. O comando `mvn test` executou **11 testes**, com **0 falhas e 0 erros**. `mvn -q exec:java` executou a demonstração com saída normal. O XML do `.drawio` foi analisado por parser, e a modelagem foi conferida com as declarações Java.

| Critério do enunciado | Peso | Evidência |
|---|---:|---|
| Completude UML | 30% | Classes, atributos, visibilidades, construtores, métodos, notas, generalização, realização e multiplicidades no `.drawio`. |
| Coesão e design | 20% | Separação entre combatentes, itens, eventos e navegação. |
| Fidelidade do código | 15% | Tipos e assinaturas correspondentes ao diagrama; checagem final em `conformidade.md`. |
| Encapsulamento e invariantes | 20% | Campos privados, validações e testes de limites e transições. |
| Uso da linguagem Java | 15% | Java 21, `extends`, `super`, `@Override`, `record`, interface e testes JUnit. |

## 7. Considerações finais

O projeto transforma as regras fornecidas em um domínio executável, com invariantes verificáveis e distinção explícita entre dados observados e parâmetros necessários à demonstração. O modelo permite substituir os números ainda desconhecidos por valores oficiais sem introduzir personagens ou mecânicas novas. A ausência do mapa real limita a validação da navegação em relação ao jogo original, mas não impede a avaliação da arquitetura, da implementação e das transições descritas.

## 8. Referências

- **Enunciado da atividade:** *Trabalho 2 Programação Orientada a Objetos*, PDF de três páginas fornecido pelo solicitante, consultado apenas como fonte de requisitos. O relatório solicitado foi entregue em Markdown.
- **Dados do jogo:** descrição manual da Etapa 1 de *Nexus Heroes* fornecida pelo solicitante.
