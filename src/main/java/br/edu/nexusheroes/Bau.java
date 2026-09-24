package br.edu.nexusheroes;

import java.util.Objects;

/** Baú concede XP e HeroCoin uma única vez. */
public final class Bau implements ElementoMapa {
    private final int experiencia;
    private final HeroCoin moeda;
    private boolean aberto;

    public Bau(int experiencia, int quantidadeMoedas) {
        if (experiencia <= 0) {
            throw new IllegalArgumentException("Experiência do baú deve ser positiva");
        }
        this.experiencia = experiencia;
        this.moeda = new HeroCoin(quantidadeMoedas);
    }

    public boolean isAberto() { return aberto; }

    @Override
    public boolean interagir(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        if (aberto) {
            return true;
        }
        if (!personagem.estaVivo()) {
            throw new IllegalStateException("Personagem derrotado não abre baú");
        }
        personagem.ganharExperiencia(experiencia);
        personagem.coletar(moeda);
        aberto = true;
        return true;
    }
}
