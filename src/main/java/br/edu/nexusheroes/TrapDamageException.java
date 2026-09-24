package br.edu.nexusheroes;

/** Sinaliza que uma armadilha foi acionada; o dano já foi aplicado. */
public final class TrapDamageException extends Exception {
    private final int dano;

    public TrapDamageException(int dano) {
        super("Armadilha acionada: " + dano + " pontos de dano");
        if (dano <= 0) {
            throw new IllegalArgumentException("Dano deve ser positivo");
        }
        this.dano = dano;
    }

    public int getDano() {
        return dano;
    }
}
