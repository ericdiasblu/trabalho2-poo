package br.edu.nexusheroes;

import java.util.Objects;

/** Representa uma quantidade positiva de moedas recebida de um baú. */
public final class HeroCoin extends Item {
    private final int quantidade;

    public HeroCoin(int quantidade) {
        super("HeroCoin");
        if (quantidade <= 0) {
            throw new IllegalArgumentException("HeroCoin deve conter moedas");
        }
        this.quantidade = quantidade;
    }

    @Override
    public void aplicarEm(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem").receberMoedas(quantidade);
    }
}
