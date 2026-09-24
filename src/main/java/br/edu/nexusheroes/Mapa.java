package br.edu.nexusheroes;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

/** Mapa lógico de posições; não modela renderização 3D/isométrica. */
public final class Mapa {
    private final int largura;
    private final int altura;
    private final Map<Posicao, ElementoMapa> elementos = new HashMap<>();
    private boolean concluido;

    public Mapa(int largura, int altura) {
        if (largura <= 0 || altura <= 0) {
            throw new IllegalArgumentException("Dimensões devem ser positivas");
        }
        this.largura = largura;
        this.altura = altura;
    }

    public void posicionar(Posicao posicao, ElementoMapa elemento) {
        exigirDentro(posicao);
        Objects.requireNonNull(elemento, "elemento");
        if (elementos.putIfAbsent(posicao, elemento) != null) {
            throw new IllegalStateException("Posição já ocupada");
        }
    }

    public ElementoMapa getElemento(Posicao posicao) {
        exigirDentro(posicao);
        return elementos.get(posicao);
    }

    public boolean andar(Personagem personagem, Posicao destino) throws TrapDamageException {
        Objects.requireNonNull(personagem, "personagem");
        exigirDentro(destino);
        exigirDentro(personagem.getPosicao());
        if (concluido || !personagem.estaVivo()) {
            throw new IllegalStateException("Movimento indisponível");
        }
        if (!personagem.getPosicao().adjacente(destino)) {
            throw new IllegalArgumentException("Destino deve ser adjacente");
        }
        ElementoMapa elemento = elementos.get(destino);
        if (elemento != null && !elemento.interagir(personagem)) {
            return false;
        }
        personagem.moverPara(destino);
        if (elemento instanceof Item) {
            elementos.remove(destino);
        }
        if (elemento instanceof Portal) {
            concluido = true;
        }
        return true;
    }

    public boolean isConcluido() { return concluido; }

    private void exigirDentro(Posicao posicao) {
        Objects.requireNonNull(posicao, "posicao");
        if (posicao.x() >= largura || posicao.y() >= altura) {
            throw new IllegalArgumentException("Posição fora do mapa");
        }
    }
}
