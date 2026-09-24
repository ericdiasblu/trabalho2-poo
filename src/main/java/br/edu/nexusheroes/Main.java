package br.edu.nexusheroes;

/** Demonstração de regras de domínio; valores não documentados são apenas exemplos. */
public final class Main {
    private Main() { }

    public static void main(String[] args) throws TrapDamageException {
        // XP, incremento, atributos do inimigo e recompensas são exemplos configuráveis.
        Personagem guerreiro = new Guerreiro("Guerreiro", new Posicao(0, 0), 10, 3);
        Personagem mago = new Mago("Mago", new Posicao(0, 0), 10, 3);
        Inimigo goblin = new Goblin(35, 7, 2, new Posicao(1, 0));
        Inimigo golem = new Golem(30, 6, 4, new Posicao(1, 0));

        System.out.printf("%s: HP %d, mana %d, dano %d%n", guerreiro.getNome(),
                guerreiro.getVida(), guerreiro.getMana(), guerreiro.calcularDano());
        System.out.printf("%s: HP %d, mana %d, dano %d%n", mago.getNome(),
                mago.getVida(), mago.getMana(), mago.calcularDano());

        Mapa mapa = new Mapa(4, 1); // Trajeto didático, não representa o mapa real.
        mapa.posicionar(new Posicao(1, 0), goblin);
        mapa.posicionar(new Posicao(2, 0), new Bau(10, 3));
        mapa.posicionar(new Posicao(3, 0), new Portal());

        System.out.println("Goblin vivo bloqueia: " + !guerreiro.andar(mapa, new Posicao(1, 0)));
        guerreiro.atacarComEspada(goblin);
        System.out.printf("Contra-ataque: HP do guerreiro = %d%n", guerreiro.getVida());
        guerreiro.atacarComEspada(goblin);
        guerreiro.andar(mapa, new Posicao(1, 0));
        guerreiro.andar(mapa, new Posicao(2, 0));
        System.out.printf("Baú: nível %d, HP %d, mana %d, ataque espada %d, moedas %d%n",
                guerreiro.getNivel(), guerreiro.getVida(), guerreiro.getMana(),
                guerreiro.getAtaqueEspada(), guerreiro.getMoedas());
        guerreiro.andar(mapa, new Posicao(3, 0));
        System.out.println("Fase concluída: " + mapa.isConcluido());

        mago.atacar(golem); // Despacho polimórfico para o dano mágico do Mago.
        mago.setMana(100);
        mago.coletar(new CristalMana());
        mago.receberDano(30);
        mago.coletar(new OrbeVida());
        try {
            new Armadilha().interagir(mago);
        } catch (TrapDamageException evento) {
            System.out.printf("Armadilha: %d dano, HP do mago = %d%n",
                    evento.getDano(), mago.getVida());
        }
        System.out.printf("Mago: mana %d, moedas %d, dano %d%n", mago.getMana(),
                mago.getMoedas(), mago.calcularDano());
    }
}
