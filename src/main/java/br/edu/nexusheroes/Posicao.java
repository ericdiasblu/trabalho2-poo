package br.edu.nexusheroes;

import java.util.Objects;

/** Coordenadas lógicas do mapa; a projeção isométrica é apenas visual. */
public record Posicao(int x, int y) {
    public Posicao {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordenadas não podem ser negativas");
        }
    }

    public boolean adjacente(Posicao outra) {
        Objects.requireNonNull(outra, "outra");
        return Math.abs((long) x - outra.x) + Math.abs((long) y - outra.y) == 1;
    }
}
