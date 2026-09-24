package br.edu.nexusheroes;

/** Elemento encontrado ao tentar entrar em uma posição do mapa. */
public interface ElementoMapa {
    /** @return true se a passagem foi liberada. */
    boolean interagir(Personagem personagem) throws TrapDamageException;
}
