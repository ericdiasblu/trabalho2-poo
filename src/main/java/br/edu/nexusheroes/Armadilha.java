package br.edu.nexusheroes;

import java.util.Objects;

/** A armadilha aplica os 20 HP de dano e sinaliza o evento por exceção. */
public final class Armadilha implements ElementoMapa {
    private static final int DANO = 20;

    public Armadilha() { }

    @Override
    public boolean interagir(Personagem personagem) throws TrapDamageException {
        Objects.requireNonNull(personagem, "personagem").receberDano(DANO);
        throw new TrapDamageException(DANO);
    }
}
