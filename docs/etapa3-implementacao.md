# Etapa 3 — Implementação Java

## Tecnologias e organização

- **Linguagem alvo:** Java 21 (`maven.compiler.release=21`). A validação local foi executada com JDK 23 emitindo bytecode compatível com Java 21.
- **Build:** Maven 3.9.11.
- **Testes:** JUnit Jupiter 5.11.4 com Maven Surefire 3.5.2.
- **Pacote único do domínio e demonstração:** `br.edu.nexusheroes`, sob `src/main/java`.
- **Testes:** pacote correspondente em `src/test/java`.

Não há interface gráfica, banco de dados, framework de aplicação nem conexão externa em execução. O `pom.xml` declara apenas a dependência de teste JUnit e os plugins de compilação, teste e execução.

## Correspondência entre UML e Java

O arquivo [diagrama-classes.drawio](diagrama-classes.drawio) representa as classes Java, com construtores, campos, métodos e visibilidades. `Posicao` é um `record` imutável; `ElementoMapa` é uma interface; `Combatente`, `Personagem`, `Inimigo` e `Item` são abstratas. As subclasses usam `extends` e chamam `super(...)` nos construtores; cada método sobrescrito usa `@Override`. `TrapDamageException` deriva de `Exception`. `Main` é uma classe utilitária fora da lógica de negócio.

## Encapsulamento e invariantes

Todos os atributos de estado são privados; referências e parâmetros de configuração imutáveis recebem `final`. `setVida` e `setMana` são os mutadores públicos necessários à regra descrita na Etapa 1 e recusam valores fora dos máximos. `receberDano` limita a vida a zero. `CristalMana` e `OrbeVida` aplicam os bônus de 25 e 20 com saturação. Quantidades de XP/moedas, limites de nível e dimensões do mapa são validados na construção ou antes da transição. Os construtores das subclasses concretas fixam as estatísticas documentadas para Guerreiro e Mago. O acesso `protected` restringe-se aos construtores abstratos e às operações indispensáveis para a especialização do ataque.

## Herança, polimorfismo e regras centrais

- `Combatente.calcularDano()` é resolvido dinamicamente. Guerreiro usa ATK espada, Mago usa MATK magia, e Goblin/Golem usam o ataque configurado.
- `Personagem.atacar` usa o dano principal da subclasse; `atacarComEspada` usa o ATK espada explicitamente. Na simulação determinística, se o inimigo sobreviver, contra-ataca; se morrer, entrega sua `HeroCoin` uma única vez.
- `Personagem.ganharExperiencia` acumula XP; cada limiar configurado chama a transição de nível. Ela restaura HP/mana e aumenta apenas o ataque principal, por despacho de `aumentarAtaque`.
- `Item.aplicarEm` é sobrescrito por HeroCoin, CristalMana e OrbeVida. `Bau` aplica XP e sua HeroCoin apenas na primeira abertura.
- `Mapa.andar` verifica limites, adjacência, vitalidade, bloqueio do inimigo e interação. A entrada no portal conclui a fase; um item coletado é removido do mapa.
- `Armadilha.interagir` aplica 20 de dano e lança `TrapDamageException` com a quantidade aplicada. Na simulação, a posição permanece anterior quando a exceção ocorre.

## Exemplo de execução

O comando `mvn -q exec:java` executa `Main`. A demonstração usa parâmetros **ilustrativos e configuráveis** para Goblin, Golem, XP e recompensas; não representa um mapa observado do jogo. A sequência evidencia a criação por construtores, o bloqueio por inimigo vivo, a espada do guerreiro, o contra-ataque, a recompensa, o baú, a subida de nível, o portal, o dano polimórfico do mago, os itens e a armadilha. Saída observada:

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

## Testes e resultados

`DominioTest` cobre construção válida, rejeição de parâmetros inválidos, limites de vida/mana, saturação de bônus, progressão, combate e contra-ataque, recompensa única, baú único, armadilha, navegação, portal, estados proibidos e despacho polimórfico. Com `mvn test`, foram executados **11 testes**, com **0 falhas, 0 erros e 0 ignorados**. `mvn -q exec:java` foi executado com código de saída zero. O relatório automatizado detalhado fica em `target/surefire-reports` após a execução, diretório excluído do Git.

## Limites conhecidos

O mapa didático não reproduz geometria 3D nem caminhos reais, que não foram fornecidos. A magia usa o valor MATK para dano, mas não consome mana, pois o custo não consta dos dados da Etapa 1. Os valores configuráveis devem ser preenchidos com dados oficiais se estes forem disponibilizados posteriormente; o diagrama e o código podem então ser revisados juntos.
