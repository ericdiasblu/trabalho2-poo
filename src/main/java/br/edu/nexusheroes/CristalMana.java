package br.edu.nexusheroes;

import java.util.Objects;

/** Cristal de mana documentado na legenda: recupera até 25 pontos. */
public final class CristalMana extends Item {
    private static final int BONUS_MANA = 25;

    public CristalMana() { super("Cristal de Mana"); }

    @Override
    public void aplicarEm(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        personagem.setMana((int) Math.min(personagem.getManaMaxima(),
                (long) personagem.getMana() + BONUS_MANA));
    }
}
