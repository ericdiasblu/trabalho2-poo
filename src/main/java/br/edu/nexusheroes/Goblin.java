package br.edu.nexusheroes;

/** Estatísticas não informadas na exploração: valores são recebidos no construtor. */
public final class Goblin extends Inimigo {
    public Goblin(int vidaMaxima, int ataque, int moedasAoDerrotar, Posicao posicao) {
        super("Goblin", vidaMaxima, ataque, moedasAoDerrotar, posicao);
    }

    @Override
    public int calcularDano() { return getAtaque(); }
}
