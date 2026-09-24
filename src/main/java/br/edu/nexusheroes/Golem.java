package br.edu.nexusheroes;

/** Estatísticas não informadas na exploração: valores são recebidos no construtor. */
public final class Golem extends Inimigo {
    public Golem(int vidaMaxima, int ataque, int moedasAoDerrotar, Posicao posicao) {
        super("Golem", vidaMaxima, ataque, moedasAoDerrotar, posicao);
    }

    @Override
    public int calcularDano() { return getAtaque(); }
}
