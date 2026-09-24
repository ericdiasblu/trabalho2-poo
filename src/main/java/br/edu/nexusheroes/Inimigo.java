package br.edu.nexusheroes;

import java.util.Objects;

/** Inimigo bloqueia a passagem enquanto vivo e dá moedas após a derrota. */
public abstract class Inimigo extends Combatente implements ElementoMapa {
    private final int ataque;
    private final HeroCoin recompensa;
    private boolean recompensaEntregue;

    protected Inimigo(String nome, int vidaMaxima, int ataque, int moedasAoDerrotar,
                      Posicao posicao) {
        super(nome, vidaMaxima, posicao);
        if (ataque < 0 || moedasAoDerrotar <= 0) {
            throw new IllegalArgumentException("Ataque ou recompensa inválidos");
        }
        this.ataque = ataque;
        this.recompensa = new HeroCoin(moedasAoDerrotar);
    }

    protected final int getAtaque() { return ataque; }

    public final int contraAtacar(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        if (!estaVivo() || !personagem.estaVivo()) {
            throw new IllegalStateException("Contra-ataque exige combatentes vivos");
        }
        int dano = calcularDano();
        personagem.receberDano(dano);
        return dano;
    }

    public final void entregarRecompensa(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        if (estaVivo() || recompensaEntregue) {
            throw new IllegalStateException("Recompensa indisponível");
        }
        personagem.coletar(recompensa);
        recompensaEntregue = true;
    }

    @Override
    public final boolean interagir(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        return !estaVivo();
    }

    @Override
    public abstract int calcularDano();
}
