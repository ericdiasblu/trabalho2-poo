package br.edu.nexusheroes;

/** Guerreiro: 120 HP, 40 mana, 25 espada e 10 magia. */
public final class Guerreiro extends Personagem {
    public Guerreiro(String nome, Posicao posicao, int experienciaPorNivel, int incrementoAtaque) {
        super(nome, 120, 40, 25, 10, posicao, experienciaPorNivel, incrementoAtaque);
    }

    @Override
    public int calcularDano() { return getAtaqueEspada(); }

    @Override
    protected void aumentarAtaque(int incremento) { aumentarAtaqueEspada(incremento); }
}
