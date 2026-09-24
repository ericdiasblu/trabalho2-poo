package br.edu.nexusheroes;

import java.util.Objects;

/** Herói controlado no domínio, com progressão e dois valores de ataque. */
public abstract class Personagem extends Combatente {
    private int mana;
    private final int manaMaxima;
    private int ataqueEspada;
    private int ataqueMagia;
    private int nivel = 1;
    private int experiencia;
    private int moedas;
    private final int experienciaPorNivel;
    private final int incrementoAtaque;

    protected Personagem(String nome, int vidaMaxima, int manaMaxima, int ataqueEspada,
                        int ataqueMagia, Posicao posicao, int experienciaPorNivel,
                        int incrementoAtaque) {
        super(nome, vidaMaxima, posicao);
        if (manaMaxima < 0 || ataqueEspada < 0 || ataqueMagia < 0
                || experienciaPorNivel <= 0 || incrementoAtaque <= 0) {
            throw new IllegalArgumentException("Atributos do personagem inválidos");
        }
        this.manaMaxima = manaMaxima;
        this.mana = manaMaxima;
        this.ataqueEspada = ataqueEspada;
        this.ataqueMagia = ataqueMagia;
        this.experienciaPorNivel = experienciaPorNivel;
        this.incrementoAtaque = incrementoAtaque;
    }

    public final int getMana() { return mana; }
    public final int getManaMaxima() { return manaMaxima; }
    public final int getAtaqueEspada() { return ataqueEspada; }
    public final int getAtaqueMagia() { return ataqueMagia; }
    public final int getNivel() { return nivel; }
    public final int getExperiencia() { return experiencia; }
    public final int getMoedas() { return moedas; }

    public final void setMana(int mana) {
        if (mana < 0 || mana > manaMaxima) {
            throw new IllegalArgumentException("Mana fora do intervalo permitido");
        }
        this.mana = mana;
    }

    public final int atacar(Inimigo inimigo) {
        return executarAtaque(inimigo, calcularDano());
    }

    public final int atacarComEspada(Inimigo inimigo) {
        return executarAtaque(inimigo, ataqueEspada);
    }

    private int executarAtaque(Inimigo inimigo, int dano) {
        Objects.requireNonNull(inimigo, "inimigo");
        if (!estaVivo() || !inimigo.estaVivo()) {
            throw new IllegalStateException("Ambos os combatentes devem estar vivos");
        }
        inimigo.receberDano(dano);
        if (inimigo.estaVivo()) {
            inimigo.contraAtacar(this);
        } else {
            inimigo.entregarRecompensa(this);
        }
        return dano;
    }

    public final void coletar(Item item) {
        Objects.requireNonNull(item, "item");
        exigirVivo();
        item.aplicarEm(this);
    }

    public final boolean andar(Mapa mapa, Posicao destino) throws TrapDamageException {
        Objects.requireNonNull(mapa, "mapa");
        exigirVivo();
        return mapa.andar(this, destino);
    }

    public final void ganharExperiencia(int pontos) {
        exigirVivo();
        if (pontos <= 0) {
            throw new IllegalArgumentException("Experiência deve ser positiva");
        }
        experiencia = Math.addExact(experiencia, pontos);
        while (experiencia >= experienciaPorNivel) {
            experiencia -= experienciaPorNivel;
            subirNivel();
        }
    }

    public final void receberMoedas(int quantidade) {
        exigirVivo();
        if (quantidade <= 0) {
            throw new IllegalArgumentException("Quantidade de moedas deve ser positiva");
        }
        moedas = Math.addExact(moedas, quantidade);
    }

    private void subirNivel() {
        nivel = Math.addExact(nivel, 1);
        setVida(getVidaMaxima());
        setMana(manaMaxima);
        aumentarAtaque(incrementoAtaque);
    }

    protected abstract void aumentarAtaque(int incremento);

    protected final void aumentarAtaqueEspada(int incremento) {
        ataqueEspada = Math.addExact(ataqueEspada, incremento);
    }

    protected final void aumentarAtaqueMagia(int incremento) {
        ataqueMagia = Math.addExact(ataqueMagia, incremento);
    }

    private void exigirVivo() {
        if (!estaVivo()) {
            throw new IllegalStateException("Personagem derrotado não pode agir");
        }
    }
}
