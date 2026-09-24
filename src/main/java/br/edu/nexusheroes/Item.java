package br.edu.nexusheroes;

import java.util.Objects;

/** Item coletável; cada subtipo define seu efeito. */
public abstract class Item implements ElementoMapa {
    private final String nome;

    protected Item(String nome) {
        if (nome == null || nome.isBlank()) {
            throw new IllegalArgumentException("Nome do item inválido");
        }
        this.nome = nome;
    }

    public final String getNome() { return nome; }

    @Override
    public final boolean interagir(Personagem personagem) {
        Objects.requireNonNull(personagem, "personagem");
        personagem.coletar(this);
        return true;
    }

    public abstract void aplicarEm(Personagem personagem);
}
