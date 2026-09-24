package br.edu.nexusheroes;

/** Mago: 80 HP, 120 mana, 15 espada e 40 magia. */
public final class Mago extends Personagem {
    public Mago(String nome, Posicao posicao, int experienciaPorNivel, int incrementoAtaque) {
        super(nome, 80, 120, 15, 40, posicao, experienciaPorNivel, incrementoAtaque);
    }

    @Override
    public int calcularDano() { return getAtaqueMagia(); }

    @Override
    protected void aumentarAtaque(int incremento) { aumentarAtaqueMagia(incremento); }
}
