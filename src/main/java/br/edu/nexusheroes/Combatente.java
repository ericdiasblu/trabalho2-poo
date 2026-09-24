package br.edu.nexusheroes;

import java.util.Objects;

/** Estado compartilhado apenas por entidades que têm vida e podem combater. */
public abstract class Combatente {
    private final String nome;
    private int vida;
    private final int vidaMaxima;
    private Posicao posicao;

    protected Combatente(String nome, int vidaMaxima, Posicao posicao) {
        if (nome == null || nome.isBlank() || vidaMaxima <= 0) {
            throw new IllegalArgumentException("Nome e vida máxima devem ser válidos");
        }
        this.nome = nome;
        this.vidaMaxima = vidaMaxima;
        this.vida = vidaMaxima;
        this.posicao = Objects.requireNonNull(posicao, "posicao");
    }

    public final String getNome() { return nome; }
    public final int getVida() { return vida; }
    public final int getVidaMaxima() { return vidaMaxima; }
    public final Posicao getPosicao() { return posicao; }

    public final void setVida(int vida) {
        if (vida < 0 || vida > vidaMaxima) {
            throw new IllegalArgumentException("Vida fora do intervalo permitido");
        }
        this.vida = vida;
    }

    public final void receberDano(int dano) {
        if (dano < 0) {
            throw new IllegalArgumentException("Dano não pode ser negativo");
        }
        setVida((int) Math.max(0L, (long) vida - dano));
    }

    public final boolean estaVivo() { return vida > 0; }

    final void moverPara(Posicao destino) {
        this.posicao = Objects.requireNonNull(destino, "destino");
    }

    public abstract int calcularDano();
}
