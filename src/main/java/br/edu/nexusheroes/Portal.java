package br.edu.nexusheroes;

import java.util.Objects;

/** O mapa registra a vitória quando um personagem vivo entra no portal. */
public final class Portal implements ElementoMapa {
    public Portal() { }

    @Override
    public boolean interagir(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        if (!personagem.estaVivo()) {
            throw new IllegalStateException("Personagem derrotado não usa portal");
        }
        return true;
    }
}
