package br.edu.nexusheroes;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class DominioTest {
    @Test
    void construcaoUsaEstatisticasDocumentadas() {
        Personagem guerreiro = new Guerreiro("A", new Posicao(0, 0), 10, 2);
        Personagem mago = new Mago("B", new Posicao(0, 0), 10, 2);
        assertAll(
                () -> assertEquals(120, guerreiro.getVidaMaxima()),
                () -> assertEquals(40, guerreiro.getManaMaxima()),
                () -> assertEquals(25, guerreiro.getAtaqueEspada()),
                () -> assertEquals(10, guerreiro.getAtaqueMagia()),
                () -> assertEquals(80, mago.getVidaMaxima()),
                () -> assertEquals(120, mago.getManaMaxima()),
                () -> assertEquals(15, mago.getAtaqueEspada()),
                () -> assertEquals(40, mago.getAtaqueMagia()));
    }

    @Test
    void construtoresRejeitamParametrosInvalidos() {
        assertThrows(IllegalArgumentException.class, () -> new Posicao(-1, 0));
        assertThrows(IllegalArgumentException.class, () -> new Guerreiro(" ", new Posicao(0, 0), 10, 2));
        assertThrows(IllegalArgumentException.class, () -> new Mago("M", new Posicao(0, 0), 0, 2));
        assertThrows(IllegalArgumentException.class, () -> new Goblin(0, 1, 1, new Posicao(0, 0)));
        assertThrows(IllegalArgumentException.class, () -> new Golem(10, 1, 0, new Posicao(0, 0)));
        assertThrows(IllegalArgumentException.class, () -> new Bau(0, 1));
        assertThrows(IllegalArgumentException.class, () -> new HeroCoin(0));
        assertThrows(IllegalArgumentException.class, () -> new Mapa(0, 1));
    }

    @Test
    void settersEReceberDanoPreservamLimites() {
        Guerreiro guerreiro = new Guerreiro("A", new Posicao(0, 0), 10, 2);
        assertThrows(IllegalArgumentException.class, () -> guerreiro.setVida(121));
        assertThrows(IllegalArgumentException.class, () -> guerreiro.setMana(-1));
        assertThrows(IllegalArgumentException.class, () -> guerreiro.receberDano(-1));
        guerreiro.receberDano(Integer.MAX_VALUE);
        assertEquals(0, guerreiro.getVida());
        assertThrows(IllegalStateException.class,
                () -> guerreiro.coletar(new OrbeVida()));
    }

    @Test
    void itensRecuperamSemUltrapassarMaximos() {
        Mago mago = new Mago("M", new Posicao(0, 0), 10, 2);
        mago.setMana(110);
        mago.receberDano(10);
        mago.coletar(new CristalMana());
        mago.coletar(new OrbeVida());
        assertEquals(120, mago.getMana());
        assertEquals(80, mago.getVida());
    }

    @Test
    void subirNivelRestauraRecursosEAumentaAtaqueDaClasse() {
        Personagem guerreiro = new Guerreiro("G", new Posicao(0, 0), 10, 3);
        Personagem mago = new Mago("M", new Posicao(0, 0), 10, 3);
        guerreiro.receberDano(30);
        guerreiro.setMana(0);
        mago.receberDano(30);
        mago.setMana(0);
        guerreiro.ganharExperiencia(25);
        mago.ganharExperiencia(10);
        assertAll(
                () -> assertEquals(3, guerreiro.getNivel()),
                () -> assertEquals(5, guerreiro.getExperiencia()),
                () -> assertEquals(120, guerreiro.getVida()),
                () -> assertEquals(40, guerreiro.getMana()),
                () -> assertEquals(31, guerreiro.calcularDano()),
                () -> assertEquals(2, mago.getNivel()),
                () -> assertEquals(43, mago.calcularDano()),
                () -> assertEquals(15, mago.getAtaqueEspada()));
    }

    @Test
    void combateBloqueiaInimigoVivoContraAtacaEEntregaUmaRecompensa() throws Exception {
        Guerreiro guerreiro = new Guerreiro("G", new Posicao(0, 0), 10, 2);
        Goblin goblin = new Goblin(30, 7, 2, new Posicao(1, 0));
        Mapa mapa = new Mapa(2, 1);
        mapa.posicionar(new Posicao(1, 0), goblin);
        assertFalse(guerreiro.andar(mapa, new Posicao(1, 0)));
        assertEquals(new Posicao(0, 0), guerreiro.getPosicao());
        guerreiro.atacarComEspada(goblin);
        assertEquals(113, guerreiro.getVida());
        assertEquals(5, goblin.getVida());
        guerreiro.atacarComEspada(goblin);
        assertEquals(0, goblin.getVida());
        assertEquals(2, guerreiro.getMoedas());
        assertTrue(guerreiro.andar(mapa, new Posicao(1, 0)));
        assertThrows(IllegalStateException.class, () -> goblin.entregarRecompensa(guerreiro));
        assertThrows(IllegalStateException.class, () -> guerreiro.atacar(goblin));
    }

    @Test
    void bauDaXpEMoedasUmaVez() {
        Guerreiro guerreiro = new Guerreiro("G", new Posicao(0, 0), 10, 2);
        Bau bau = new Bau(10, 3);
        assertTrue(bau.interagir(guerreiro));
        assertTrue(bau.interagir(guerreiro));
        assertTrue(bau.isAberto());
        assertEquals(2, guerreiro.getNivel());
        assertEquals(3, guerreiro.getMoedas());
    }

    @Test
    void armadilhaAplicaDanoESinalizaEvento() {
        Guerreiro guerreiro = new Guerreiro("G", new Posicao(0, 0), 10, 2);
        TrapDamageException evento = assertThrows(TrapDamageException.class,
                () -> new Armadilha().interagir(guerreiro));
        assertEquals(20, evento.getDano());
        assertEquals(100, guerreiro.getVida());
    }

    @Test
    void mapaControlaPosicionamentoMovimentoColetaEPortal() throws Exception {
        Guerreiro guerreiro = new Guerreiro("G", new Posicao(0, 0), 10, 2);
        Mapa mapa = new Mapa(3, 1);
        mapa.posicionar(new Posicao(1, 0), new OrbeVida());
        mapa.posicionar(new Posicao(2, 0), new Portal());
        assertThrows(IllegalArgumentException.class, () -> guerreiro.andar(mapa, new Posicao(2, 0)));
        assertThrows(IllegalStateException.class,
                () -> mapa.posicionar(new Posicao(1, 0), new CristalMana()));
        assertTrue(guerreiro.andar(mapa, new Posicao(1, 0)));
        assertNull(mapa.getElemento(new Posicao(1, 0)));
        assertTrue(guerreiro.andar(mapa, new Posicao(2, 0)));
        assertTrue(mapa.isConcluido());
        assertThrows(IllegalStateException.class, () -> guerreiro.andar(mapa, new Posicao(1, 0)));
    }

    @Test
    void polimorfismoCalculaDanoPorSubclasse() {
        Combatente[] combatentes = {
                new Guerreiro("G", new Posicao(0, 0), 10, 2),
                new Mago("M", new Posicao(0, 0), 10, 2),
                new Goblin(15, 6, 1, new Posicao(1, 0)),
                new Golem(30, 9, 1, new Posicao(1, 0))
        };
        assertArrayEquals(new int[] {25, 40, 6, 9},
                java.util.Arrays.stream(combatentes).mapToInt(Combatente::calcularDano).toArray());
    }

    @Test
    void estadosEOperacoesProibidasSaoRejeitados() {
        Guerreiro guerreiro = new Guerreiro("G", new Posicao(0, 0), 10, 2);
        Goblin goblin = new Goblin(10, 1, 1, new Posicao(1, 0));
        assertThrows(IllegalArgumentException.class, () -> guerreiro.ganharExperiencia(0));
        assertThrows(IllegalArgumentException.class, () -> guerreiro.receberMoedas(-1));
        assertThrows(IllegalStateException.class, () -> goblin.entregarRecompensa(guerreiro));
        guerreiro.receberDano(120);
        assertThrows(IllegalStateException.class, () -> guerreiro.atacar(goblin));
        assertThrows(IllegalStateException.class,
                () -> guerreiro.andar(new Mapa(2, 1), new Posicao(1, 0)));
    }
}
