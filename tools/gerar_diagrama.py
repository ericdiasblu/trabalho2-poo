"""Gera UML nativa do diagrams.net; textos e conectores são células editáveis."""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


CLASSES = [
    ("Posicao", 40, 35, 390, ["- x: int {final}", "- y: int {final}"], ["+ Posicao(x: int, y: int)", "+ x(): int", "+ y(): int", "+ adjacente(outra: Posicao): boolean"], "«record»"),
    ("ElementoMapa", 480, 35, 510, [], ["+ interagir(personagem: Personagem): boolean {throws TrapDamageException}"], "«interface»"),
    ("TrapDamageException", 1040, 35, 470, ["- dano: int"], ["+ TrapDamageException(dano: int)", "+ getDano(): int"]),
    ("Combatente", 40, 290, 500, ["- nome: String", "- vida: int", "- vidaMaxima: int", "- posicao: Posicao"], ["# Combatente(nome: String, vidaMaxima: int, posicao: Posicao)", "+ getNome(): String", "+ getVida(): int", "+ getVidaMaxima(): int", "+ getPosicao(): Posicao", "+ setVida(vida: int): void", "+ receberDano(dano: int): void", "+ estaVivo(): boolean", "~ moverPara(destino: Posicao): void", "+ calcularDano(): int {abstract}"], "{abstract}"),
    ("Personagem", 590, 290, 645, ["- mana: int", "- manaMaxima: int", "- ataqueEspada: int", "- ataqueMagia: int", "- nivel: int", "- experiencia: int", "- moedas: int", "- experienciaPorNivel: int", "- incrementoAtaque: int"], ["# Personagem(nome: String, vidaMaxima: int, manaMaxima: int, ataqueEspada: int, ataqueMagia: int, posicao: Posicao, experienciaPorNivel: int, incrementoAtaque: int)", "+ getMana(): int", "+ getManaMaxima(): int", "+ getAtaqueEspada(): int", "+ getAtaqueMagia(): int", "+ getNivel(): int", "+ getExperiencia(): int", "+ getMoedas(): int", "+ setMana(mana: int): void", "+ atacar(inimigo: Inimigo): int", "+ atacarComEspada(inimigo: Inimigo): int", "- executarAtaque(inimigo: Inimigo, dano: int): int", "+ coletar(item: Item): void", "+ andar(mapa: Mapa, destino: Posicao): boolean {throws TrapDamageException}", "+ ganharExperiencia(pontos: int): void", "+ receberMoedas(quantidade: int): void", "- subirNivel(): void", "# aumentarAtaque(incremento: int): void {abstract}", "# aumentarAtaqueEspada(incremento: int): void", "# aumentarAtaqueMagia(incremento: int): void", "- exigirVivo(): void"], "{abstract}"),
    ("Inimigo", 1300, 290, 560, ["- ataque: int", "- recompensa: HeroCoin", "- recompensaEntregue: boolean"], ["# Inimigo(nome: String, vidaMaxima: int, ataque: int, moedasAoDerrotar: int, posicao: Posicao)", "# getAtaque(): int", "+ contraAtacar(personagem: Personagem): int", "+ entregarRecompensa(personagem: Personagem): void", "+ interagir(personagem: Personagem): boolean", "+ calcularDano(): int {abstract}"], "{abstract}"),
    ("Guerreiro", 40, 1050, 570, [], ["+ Guerreiro(nome: String, posicao: Posicao, experienciaPorNivel: int, incrementoAtaque: int)", "+ calcularDano(): int {override}", "# aumentarAtaque(incremento: int): void {override}"]),
    ("Mago", 660, 1050, 570, [], ["+ Mago(nome: String, posicao: Posicao, experienciaPorNivel: int, incrementoAtaque: int)", "+ calcularDano(): int {override}", "# aumentarAtaque(incremento: int): void {override}"]),
    ("Goblin", 1280, 1050, 540, [], ["+ Goblin(vidaMaxima: int, ataque: int, moedasAoDerrotar: int, posicao: Posicao)", "+ calcularDano(): int {override}"]),
    ("Golem", 1870, 1050, 540, [], ["+ Golem(vidaMaxima: int, ataque: int, moedasAoDerrotar: int, posicao: Posicao)", "+ calcularDano(): int {override}"]),
    ("Item", 40, 1360, 500, ["- nome: String"], ["# Item(nome: String)", "+ getNome(): String", "+ interagir(personagem: Personagem): boolean", "+ aplicarEm(personagem: Personagem): void {abstract}"], "{abstract}"),
    ("HeroCoin", 590, 1360, 510, ["- quantidade: int"], ["+ HeroCoin(quantidade: int)", "+ aplicarEm(personagem: Personagem): void {override}"]),
    ("CristalMana", 1150, 1360, 510, ["- BONUS_MANA: int = 25 {static, final}"], ["+ CristalMana()", "+ aplicarEm(personagem: Personagem): void {override}"]),
    ("OrbeVida", 1710, 1360, 510, ["- BONUS_VIDA: int = 20 {static, final}"], ["+ OrbeVida()", "+ aplicarEm(personagem: Personagem): void {override}"]),
    ("Mapa", 40, 1750, 670, ["- largura: int", "- altura: int", "- elementos: Map<Posicao, ElementoMapa>", "- concluido: boolean"], ["+ Mapa(largura: int, altura: int)", "+ posicionar(posicao: Posicao, elemento: ElementoMapa): void", "+ getElemento(posicao: Posicao): ElementoMapa", "+ andar(personagem: Personagem, destino: Posicao): boolean {throws TrapDamageException}", "+ isConcluido(): boolean", "- exigirDentro(posicao: Posicao): void"]),
    ("Bau", 770, 1750, 530, ["- experiencia: int", "- moeda: HeroCoin", "- aberto: boolean"], ["+ Bau(experiencia: int, quantidadeMoedas: int)", "+ isAberto(): boolean", "+ interagir(personagem: Personagem): boolean"]),
    ("Armadilha", 1360, 1750, 530, ["- DANO: int = 20 {static, final}"], ["+ Armadilha()", "+ interagir(personagem: Personagem): boolean {throws TrapDamageException}"]),
    ("Portal", 1950, 1750, 470, [], ["+ Portal()", "+ interagir(personagem: Personagem): boolean"]),
    ("Main", 1910, 290, 500, [], ["- Main()", "+ main(args: String[]): void {static, throws TrapDamageException}"], "«utility»"),
    ("Exception", 1600, 35, 430, [], [], "«Java standard library»"),
]

NOTES = [
    ("n1", 40, 2260, 500, "Combatente: 0 ≤ vida ≤ vidaMaxima; vidaMaxima > 0; nome não vazio; posição válida."),
    ("n2", 590, 2260, 620, "Personagem: 0 ≤ mana ≤ manaMaxima; XP, moedas ≥ 0; nível ≥ 1. Ao subir nível, HP e mana voltam ao máximo e o ataque principal aumenta."),
    ("n3", 1260, 2260, 520, "Inimigo: bloqueia a passagem enquanto vivo; contra-ataca se sobreviver; recompensa em moedas entregue uma única vez."),
    ("n4", 1830, 2260, 570, "Mapa: movimento ortogonal de uma casa, dentro dos limites. Portal conclui a fase; item coletado sai do mapa."),
    ("n5", 40, 2400, 500, "Bau: XP e HeroCoin positivos; só pode ser aberto uma vez. Seu HeroCoin pertence ao baú até a abertura."),
    ("n6", 590, 2400, 620, "Itens: bônus de vida/mana saturam no máximo. Armadilha retira 20 HP, com piso em zero, e sinaliza TrapDamageException."),
]

root = ET.Element("mxfile", {"host": "app.diagrams.net", "modified": "2026-09-24T00:00:00.000Z", "agent": "Codex", "version": "24.7.17", "type": "device"})
diagram = ET.SubElement(root, "diagram", {"id": "nexus-classes", "name": "Nexus Heroes - Classes"})
model = ET.SubElement(diagram, "mxGraphModel", {"dx": "2400", "dy": "2700", "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "2500", "pageHeight": "2700", "math": "0", "shadow": "0"})
cells = ET.SubElement(model, "root")
ET.SubElement(cells, "mxCell", {"id": "0"})
ET.SubElement(cells, "mxCell", {"id": "1", "parent": "0"})


def vertex(cid, value, x, y, w, h, style, parent="1"):
    cell = ET.SubElement(cells, "mxCell", {"id": cid, "value": value, "style": style, "vertex": "1", "parent": parent})
    ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})
    return cell


def edge(cid, source, target, style, value=""):
    cell = ET.SubElement(cells, "mxCell", {"id": cid, "value": value, "style": style, "edge": "1", "parent": "1", "source": source, "target": target})
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})


for entry in CLASSES:
    name, x, y, width, attrs, methods, *extra = entry
    stereotype = extra[0] if extra else ""
    # Cada linha é uma célula editável, dentro da moldura editável da classe.
    capacity = max(20, (width - 22) // 7)
    row_height = lambda s: 20 * max(1, (len(s) + capacity - 1) // capacity)
    attr_height = sum(row_height(s) for s in attrs)
    method_height = sum(row_height(s) for s in methods)
    height = 68 + attr_height + method_height + (10 if not attrs else 0)
    vertex(name, "", x, y, width, height, "group;connectable=1;")
    vertex(f"{name}-frame", "", 0, 0, width, height, "rounded=0;whiteSpace=wrap;fillColor=#ffffff;strokeColor=#334155;strokeWidth=2;", name)
    vertex(f"{name}-head", f"{stereotype}  {name}".strip(), 1, 1, width - 2, 36, "rounded=0;whiteSpace=wrap;fillColor=#dbeafe;strokeColor=none;fontStyle=1;fontSize=15;align=center;verticalAlign=middle;", name)
    vertex(f"{name}-attrs-bg", "", 1, 37, width - 2, max(18, attr_height + 8), "rounded=0;fillColor=#f8fafc;strokeColor=#94a3b8;strokeWidth=1;", name)
    ay = 42
    for i, line in enumerate(attrs):
        vertex(f"{name}-a{i}", line, 9, ay, width - 18, row_height(line), "text;html=0;whiteSpace=wrap;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontFamily=Consolas;fontSize=12;", name)
        ay += row_height(line)
    my = 37 + max(18, attr_height + 8)
    for i, line in enumerate(methods):
        vertex(f"{name}-m{i}", line, 9, my + 4, width - 18, row_height(line), "text;html=0;whiteSpace=wrap;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontFamily=Consolas;fontSize=12;", name)
        my += row_height(line)

for nid, x, y, w, note in NOTES:
    vertex(nid, note, x, y, w, 110, "shape=note;whiteSpace=wrap;html=0;fillColor=#fff7ed;strokeColor=#f59e0b;fontSize=14;align=left;verticalAlign=top;spacing=10;")

GENERAL = "endArrow=block;endFill=0;endSize=18;strokeColor=#334155;strokeWidth=2;edgeStyle=orthogonalEdgeStyle;rounded=0;"
IMPLEMENTS = "endArrow=block;endFill=0;endSize=18;dashed=1;strokeColor=#64748b;strokeWidth=2;edgeStyle=orthogonalEdgeStyle;rounded=0;"
ASSOC = "endArrow=none;startArrow=none;strokeColor=#475569;strokeWidth=2;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=12;"
AGG = "startArrow=diamond;startFill=0;strokeColor=#475569;strokeWidth=2;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=12;"
COMP = "startArrow=diamond;startFill=1;strokeColor=#475569;strokeWidth=2;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=12;"
DEP = "endArrow=open;dashed=1;strokeColor=#94a3b8;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=12;"

relationships = [
    ("g1", "Personagem", "Combatente", GENERAL, ""), ("g2", "Inimigo", "Combatente", GENERAL, ""),
    ("g3", "Guerreiro", "Personagem", GENERAL, ""), ("g4", "Mago", "Personagem", GENERAL, ""),
    ("g5", "Goblin", "Inimigo", GENERAL, ""), ("g6", "Golem", "Inimigo", GENERAL, ""),
    ("g7", "HeroCoin", "Item", GENERAL, ""), ("g8", "CristalMana", "Item", GENERAL, ""), ("g9", "OrbeVida", "Item", GENERAL, ""),
    ("g10", "TrapDamageException", "Exception", GENERAL, ""),
    ("i1", "Inimigo", "ElementoMapa", IMPLEMENTS, ""), ("i2", "Item", "ElementoMapa", IMPLEMENTS, ""),
    ("i3", "Bau", "ElementoMapa", IMPLEMENTS, ""), ("i4", "Armadilha", "ElementoMapa", IMPLEMENTS, ""), ("i5", "Portal", "ElementoMapa", IMPLEMENTS, ""),
    ("r1", "Mapa", "ElementoMapa", AGG, "elementos"),
    ("r2", "Bau", "HeroCoin", COMP, "moeda"),
    ("r2b", "Inimigo", "HeroCoin", COMP, "recompensa"),
    ("r3", "Combatente", "Posicao", ASSOC, "posição"),
    ("r4", "Personagem", "Inimigo", ASSOC, "combate"),
    ("d1", "Mapa", "Personagem", DEP, "movimenta"),
    ("d2", "Armadilha", "TrapDamageException", DEP, "lança"),
]
for rel in relationships:
    edge(*rel)


def multiplicity(edge_id, suffix, value, along):
    cell = ET.SubElement(cells, "mxCell", {
        "id": f"{edge_id}-{suffix}", "value": value,
        "style": "edgeLabel;html=0;align=center;verticalAlign=middle;resizable=0;fontSize=12;fillColor=#ffffff;",
        "vertex": "1", "connectable": "0", "parent": edge_id,
    })
    geometry = ET.SubElement(cell, "mxGeometry", {
        "x": str(along), "relative": "1", "width": "44", "height": "18", "as": "geometry",
    })
    ET.SubElement(geometry, "mxPoint", {"x": "0", "y": "-16", "as": "offset"})


for edge_id, source_count, target_count in [
    ("r1", "1", "0..*"), ("r2", "1", "1"), ("r2b", "1", "1"),
    ("r3", "1", "1"), ("r4", "0..*", "0..*"),
]:
    multiplicity(edge_id, "source-count", source_count, -0.9)
    multiplicity(edge_id, "target-count", target_count, 0.9)
for nid, target in [("n1", "Combatente"), ("n2", "Personagem"), ("n3", "Inimigo"), ("n4", "Mapa"), ("n5", "Bau"), ("n6", "Armadilha")]:
    edge(f"note-{nid}", nid, target, "dashed=1;endArrow=none;strokeColor=#f59e0b;edgeStyle=orthogonalEdgeStyle;rounded=0;")

output = Path(__file__).resolve().parents[1] / "docs" / "diagrama-classes.drawio"
output.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
print(output)
