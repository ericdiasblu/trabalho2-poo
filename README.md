# Nexus Heroes — Trabalho 2 de Programação Orientada a Objetos

Projeto acadêmico em Java que modela as regras de domínio de Nexus Heroes descritas na [Etapa 1](docs/etapa1-exploracao.md). O diagrama UML é [nativo e editável](docs/diagrama-classes.drawio). O relatório foi entregue em [Markdown](docs/relatorio-final.md), conforme solicitado, sem gerar PDF.

## Requisitos

- JDK 21 ou superior, capaz de compilar com `--release 21`.
- Maven 3.9 ou superior.
- diagrams.net para inspecionar e editar o diagrama.

## Compilar, testar e executar

No diretório `trabalho-poo`:

```bash
mvn test
mvn -q exec:java
```

O código usa a API do Java 21. O `pom.xml` define `maven.compiler.release=21`, permitindo compilação por um JDK posterior e execução por Java 21+. A classe executada é `br.edu.nexusheroes.Main`.

## Estrutura

```text
trabalho-poo/
├── README.md
├── pom.xml
├── .gitignore
├── docs/
│   ├── etapa1-exploracao.md
│   ├── etapa2-modelagem.md
│   ├── etapa3-implementacao.md
│   ├── relatorio-final.md
│   ├── conformidade.md
│   └── diagrama-classes.drawio
├── src/
│   ├── main/java/br/edu/nexusheroes/  (domínio e Main)
│   └── test/java/br/edu/nexusheroes/  (JUnit 5)
└── tools/gerar_diagrama.py
```

## Diagrama UML

Abra `docs/diagrama-classes.drawio` em [app.diagrams.net](https://app.diagrams.net/) com **Arquivo → Abrir de → Dispositivo**. O XML contém classes, linhas de atributos e métodos, notas e relacionamentos como células independentes. Para recriar o diagrama após uma alteração no modelo, execute `python tools/gerar_diagrama.py` e confira o resultado antes de entregar.

Após compilar, `python tools/validar_diagrama.py` confere o XML, sobreposições de caixas e os campos/métodos declarados no bytecode (requer `JAVA_HOME`).

## Parâmetros não informados pelo jogo

HP/ataque/recompensa de Goblin e Golem, XP por nível, incremento de ataque e recompensa do baú são argumentos dos construtores. A demonstração usa números ilustrativos identificados no código e na documentação. Eles não são apresentados como regras oficiais. O layout real do labirinto também não foi fornecido; o mapa da demonstração é didático.

## Entrega

O diretório pode ser versionado em um repositório GitHub ou compactado em ZIP. Inclua `pom.xml`, `src`, `docs`, `README.md` e `.gitignore`; `target/` é gerado pelo Maven e deve ficar de fora. Nenhum arquivo foi publicado ou enviado a serviço externo.
