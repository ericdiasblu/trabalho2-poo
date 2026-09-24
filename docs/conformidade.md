# Checklist de conformidade

Fonte dos requisitos acadêmicos: as três páginas do PDF *Trabalho 2 Programação Orientada a Objetos*. A entrega em Markdown e `.drawio` editável segue a instrução explícita do solicitante, que substitui o formato PDF mencionado no enunciado.

| Requisito do PDF ou da entrega | Situação | Evidência e observação |
|---|---|---|
| Etapa 1: jogar e explorar todos os caminhos, cenários e interações | **Não verificável com os dados recebidos** | [Etapa 1](etapa1-exploracao.md) registra fielmente as informações manuais; o jogo e o mapa completo não foram disponibilizados. Nenhuma exploração adicional foi alegada. |
| Etapa 1: identificar classes e entidades | Atendido para os dados fornecidos | [Etapa 1](etapa1-exploracao.md), seção “Classes e entidades identificadas”. |
| Etapa 1: identificar atributos e estado | Atendido | [Etapa 1](etapa1-exploracao.md), seção “Atributos e estados”. |
| Etapa 1: identificar métodos e comportamentos | Atendido | [Etapa 1](etapa1-exploracao.md), seção “Métodos e comportamentos”. |
| Etapa 1: identificar invariantes e transições | Atendido | [Etapa 1](etapa1-exploracao.md), seção “Invariantes e transições”. |
| Etapa 2: classes, atributos e métodos de negócio | Atendido | [Diagrama](diagrama-classes.drawio) e [modelagem](etapa2-modelagem.md). |
| Etapa 2: visibilidades UML `-`, `#`, `+`, `~` | Atendido | Diagrama; `Combatente.moverPara` apresenta `~`, e os demais membros usam a visibilidade correspondente ao Java. |
| Etapa 2: construtores com estado válido | Atendido | Diagrama e construtores em `src/main/java/br/edu/nexusheroes`. |
| Etapa 2: invariantes em notas UML | Atendido | Seis notas conectadas às classes no diagrama e tabela em [modelagem](etapa2-modelagem.md). |
| Etapa 2: hierarquia é-um e generalização | Atendido | `Combatente` → `Personagem`/`Inimigo`, especializações e `Item` no diagrama e Java. |
| Etapa 2: sobrescrita evidente | Atendido | `calcularDano`, `aumentarAtaque` e `aplicarEm` no diagrama e com `@Override` no Java. |
| Etapa 3: fidelidade entre UML e código | Atendido | Classes, campos, construtores, métodos e relações conferidos; [modelagem](etapa2-modelagem.md) e [implementação](etapa3-implementacao.md). |
| Etapa 3: encapsulamento, setters validados e `final` cabível | Atendido | `Combatente.setVida`, `Personagem.setMana`, campos privados e `final` nas configurações. |
| Etapa 3: construção sem instâncias inválidas | Atendido | Validações dos construtores e testes de rejeição em `DominioTest`. |
| Etapa 3: `super()` e `@Override` | Atendido | Subclasses de personagens, inimigos e itens. |
| Etapa 3: `protected` justificado | Atendido | [Modelagem](etapa2-modelagem.md), seção de encapsulamento. |
| Etapa 3: coesão e baixo acoplamento | Atendido | Papéis das classes e contrato `ElementoMapa` em [modelagem](etapa2-modelagem.md). |
| Formato: relatório | Atendido conforme instrução atual | [Relatório final em Markdown](relatorio-final.md); **nenhum PDF foi gerado**. |
| Formato: diagrama UML com classes, atributos e relações | Atendido | [Arquivo `.drawio` nativo e editável](diagrama-classes.drawio). |
| Formato: projeto completo em repositório ou ZIP | Preparado | Diretório `trabalho-poo` contém `pom.xml`, fontes, testes, documentação e `.gitignore`, pronto para versionamento ou compactação local. Não foi publicado. |
| Critério: completude UML (30%) | Conferido | Compartimentos, construtores, métodos, relações, multiplicidades e notas no diagrama. |
| Critério: coesão e design (20%) | Conferido | Hierarquias coerentes e responsabilidades separadas. |
| Critério: fidelidade do código (15%) | Conferido | Diagrama e fontes sincronizados. |
| Critério: encapsulamento e invariantes (20%) | Conferido | Validações e testes. |
| Critério: uso da linguagem Java (15%) | Conferido | Compilação com alvo Java 21, herança, sobrescrita e JUnit 5. |

## Verificações realizadas

- `mvn test`: 11 testes, 0 falhas, 0 erros, 0 ignorados.
- `mvn -q exec:java`: execução normal da simulação de console.
- Parsing do XML de `diagrama-classes.drawio`: arquivo bem formado, com células e relações nativas.
- A exportação visual pelo aplicativo portátil diagrams.net foi tentada, mas o processo local não produziu arquivo neste ambiente, inclusive com um diagrama mínimo de controle. A validação estrutural e a comparação automatizada com o bytecode passaram; a inspeção visual no diagrams.net permanece pendente. O arquivo pode ser aberto pelo procedimento do [README](../README.md).
