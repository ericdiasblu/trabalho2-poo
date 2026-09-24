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
]

NOTES = [
    ("n1", 40, 2260, 500, "Combatente: 0 ≤ vida ≤ vidaMaxima; vidaMaxima > 0; nome não vazio; posição válida."),
    ("n2", 590, 2260, 620, "Personagem: 0 ≤ mana ≤ manaMaxima; XP, moedas ≥ 0; nível ≥ 1. Ao subir nível, HP e mana voltam ao máximo e o ataque principal aumenta."),
    ("n3", 1260, 2260, 520, "Inimigo: bloqueia a passagem enquanto vivo; contra-ataca se sobreviver; recompensa em moedas entregue uma única vez."),
    ("n4", 1830, 2260, 570, "Mapa: movimento ortogonal de uma casa, dentro dos limites. Portal conclui o jogo; item coletado sai do mapa."),
    ("n5", 40, 2400, 500, "Bau: XP e HeroCoin positivos; só pode ser aberto uma vez. Seu HeroCoin pertence ao baú até a abertura."),
    ("n6", 590, 2400, 620, "Itens: bônus de vida/mana saturam no máximo. Armadilha retira 20 HP, com piso em zero, e sinaliza TrapDamageException."),
]

# Distribuição inspirada no diagrama fornecido: hierarquias de combate acima,
# itens e elementos do mapa abaixo. Main e Exception são externos ao domínio.
LAYOUT = {
    "Combatente": (1620, 70, 650),
    "Posicao": (2920, 70, 500),
    "Personagem": (550, 520, 900),
    "Inimigo": (2370, 520, 720),
    "Guerreiro": (550, 1420, 600),
    "Mago": (1210, 1420, 600),
    "Goblin": (2370, 1420, 600),
    "Golem": (3030, 1420, 600),
    "Item": (350, 1780, 650),
    "ElementoMapa": (1430, 1780, 650),
    "Mapa": (3020, 1780, 720),
    "CristalMana": (50, 2260, 550),
    "OrbeVida": (660, 2260, 550),
    "HeroCoin": (1270, 2260, 550),
    "Bau": (1880, 2260, 550),
    "Armadilha": (2490, 2260, 550),
    "Portal": (3100, 2260, 550),
    "TrapDamageException": (3710, 2260, 550),
}
NOTE_LAYOUT = {
    "n1": (1120, 80, 430, 150),
    "n2": (50, 600, 430, 180),
    "n3": (3210, 550, 430, 160),
    "n4": (3800, 1770, 430, 165),
    "n5": (1940, 2690, 510, 145),
    "n6": (650, 2690, 660, 145),
}
ABSTRACT = {"Combatente", "Personagem", "Inimigo", "Item"}
SPECIALIZATIONS = {"Guerreiro", "Mago", "Goblin", "Golem", "HeroCoin", "CristalMana", "OrbeVida"}
VALUE_TYPES = {"Posicao", "ElementoMapa"}


def colors(name):
    if name in SPECIALIZATIONS:
        return "#ffe3e7", "#c73545"
    if name in VALUE_TYPES:
        return "#d9f6e9", "#19855d"
    if name == "TrapDamageException":
        return "#f0ebff", "#7561aa"
    return "#dceeff", "#15578d"

root = ET.Element("mxfile", {"host": "app.diagrams.net", "modified": "2026-09-24T00:00:00.000Z", "agent": "Codex", "version": "24.7.17", "type": "device"})
diagram = ET.SubElement(root, "diagram", {"id": "nexus-classes", "name": "Nexus Heroes - Classes"})
model = ET.SubElement(diagram, "mxGraphModel", {"dx": "4300", "dy": "3200", "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "4300", "pageHeight": "3200", "math": "0", "shadow": "0"})
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
    name, _, _, _, attrs, methods, *extra = entry
    x, y, width = LAYOUT[name]
    stereotype = extra[0] if extra else ""
    # Cada linha é uma célula editável, dentro da moldura editável da classe.
    # Consolas a 13 pt ocupa aproximadamente 8 px por caractere.
    # A margem extra evita que assinaturas longas invadam a próxima linha.
    capacity = max(20, (width - 35) // 8)
    row_height = lambda s: 24 * max(1, (len(s) + capacity - 1) // capacity)
    attr_height = sum(row_height(s) for s in attrs)
    method_height = sum(row_height(s) for s in methods)
    attr_box = max(24, attr_height + 8)
    height = 43 + attr_box + method_height + 12
    fill, stroke = colors(name)
    vertex(name, "", x, y, width, height, "group;container=1;collapsible=0;recursiveResize=0;connectable=1;")
    vertex(f"{name}-frame", "", 0, 0, width, height, f"rounded=0;whiteSpace=wrap;fillColor={fill};strokeColor={stroke};strokeWidth=1.6;", name)
    vertex(f"{name}-head", f"{stereotype}  {name}".strip(), 1, 1, width - 2, 40, f"rounded=0;whiteSpace=wrap;fillColor={fill};strokeColor={stroke};strokeWidth=1.3;fontStyle={3 if name in ABSTRACT else 1};fontSize=17;fontFamily=Arial;align=center;verticalAlign=middle;", name)
    vertex(f"{name}-attrs-bg", "", 1, 41, width - 2, attr_box, f"rounded=0;fillColor={fill};strokeColor={stroke};strokeWidth=1.1;", name)
    ay = 45
    for i, line in enumerate(attrs):
        vertex(f"{name}-a{i}", line, 11, ay, width - 22, row_height(line), "text;html=0;whiteSpace=wrap;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontFamily=Consolas;fontSize=13;", name)
        ay += row_height(line)
    my = 41 + attr_box
    vertex(f"{name}-methods-bg", "", 1, my, width - 2, height - my - 1, f"rounded=0;fillColor={fill};strokeColor={stroke};strokeWidth=1.1;", name)
    for i, line in enumerate(methods):
        vertex(f"{name}-m{i}", line, 11, my + 4, width - 22, row_height(line), "text;html=0;whiteSpace=wrap;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontFamily=Consolas;fontSize=13;", name)
        my += row_height(line)

for nid, _, _, _, note in NOTES:
    x, y, w, h = NOTE_LAYOUT[nid]
    vertex(nid, note, x, y, w, h, "shape=note;whiteSpace=wrap;html=0;fillColor=#fff4d9;strokeColor=#c18b20;strokeWidth=1.3;fontSize=15;fontFamily=Arial;align=left;verticalAlign=top;spacing=12;")
vertex("n7", "Regras do jogo: inimigos vivos bloqueiam e contra-atacam; armadilhas causam dano; derrotar inimigos concede moedas; subir de nível restaura HP e mana e aumenta o ataque; alcançar o portal conclui o jogo.", 1320, 2950, 1630, 115, "shape=note;whiteSpace=wrap;html=0;fillColor=#fff4d9;strokeColor=#c18b20;strokeWidth=1.3;fontSize=16;fontFamily=Arial;align=left;verticalAlign=top;spacing=13;")

GENERAL = "endArrow=block;endFill=0;endSize=18;strokeColor=#222222;strokeWidth=1.8;edgeStyle=orthogonalEdgeStyle;rounded=0;"
IMPLEMENTS = "endArrow=block;endFill=0;endSize=18;dashed=1;strokeColor=#444444;strokeWidth=1.6;edgeStyle=orthogonalEdgeStyle;rounded=0;"
ASSOC = "endArrow=none;startArrow=none;strokeColor=#222222;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=13;"
AGG = "startArrow=diamond;startFill=0;strokeColor=#222222;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=13;"
COMP = "startArrow=diamond;startFill=1;strokeColor=#222222;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=13;"
DEP = "endArrow=open;dashed=1;strokeColor=#555555;strokeWidth=1.3;edgeStyle=orthogonalEdgeStyle;rounded=0;fontSize=13;"

relationships = [
    ("g1", "Personagem", "Combatente", GENERAL, ""), ("g2", "Inimigo", "Combatente", GENERAL, ""),
    ("g3", "Guerreiro", "Personagem", GENERAL, ""), ("g4", "Mago", "Personagem", GENERAL, ""),
    ("g5", "Goblin", "Inimigo", GENERAL, ""), ("g6", "Golem", "Inimigo", GENERAL, ""),
    ("g7", "HeroCoin", "Item", GENERAL, ""), ("g8", "CristalMana", "Item", GENERAL, ""), ("g9", "OrbeVida", "Item", GENERAL, ""),
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
        "style": "edgeLabel;html=0;align=center;verticalAlign=middle;resizable=0;fontSize=13;fillColor=#ffffff;",
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
    edge(f"note-{nid}", nid, target, "dashed=1;endArrow=none;strokeColor=#9a6b12;edgeStyle=orthogonalEdgeStyle;rounded=0;")

output = Path(__file__).resolve().parents[1] / "docs" / "diagrama-classes.drawio"
output.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
print(output)
