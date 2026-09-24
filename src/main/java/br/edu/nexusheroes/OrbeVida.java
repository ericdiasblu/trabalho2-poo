package br.edu.nexusheroes;

import java.util.Objects;

/** Orbe de vida documentado na legenda: recupera até 20 pontos. */
public final class OrbeVida extends Item {
    private static final int BONUS_VIDA = 20;

    public OrbeVida() { super("Orbe de Vida"); }

    @Override
    public void aplicarEm(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        personagem.setVida((int) Math.min(personagem.getVidaMaxima(),
                (long) personagem.getVida() + BONUS_VIDA));
    }
}
