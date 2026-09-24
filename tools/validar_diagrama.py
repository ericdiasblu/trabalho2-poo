"""Confere XML, células editáveis, nomes UML/bytecode e sobreposição de caixas."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

base = Path(__file__).resolve().parents[1]
root = ET.parse(base / "docs" / "diagrama-classes.drawio").getroot()
cells = root.findall(".//mxCell")
by_id = {cell.get("id"): cell for cell in cells}
sources = sorted((base / "src/main/java/br/edu/nexusheroes").glob("*.java"))
class_names = {path.stem for path in sources} - {"Main"}
groups = {cell.get("id"): cell for cell in cells if cell.get("style", "").startswith("group;")}
assert class_names <= groups.keys(), sorted(class_names - groups.keys())
assert not {"Main", "Exception"} & groups.keys()


def geometry(cell):
    g = cell.find("mxGeometry")
    return tuple(float(g.get(key, "0")) for key in ("x", "y", "width", "height"))


boxes = [(name, geometry(group)) for name, group in groups.items()]
for i, (a, (ax, ay, aw, ah)) in enumerate(boxes):
    for b, (bx, by, bw, bh) in boxes[i + 1 :]:
        if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
            raise AssertionError(f"Classes sobrepostas: {a}, {b}")

for cell in cells:
    if cell.get("edge") == "1":
        assert cell.get("source") in by_id and cell.get("target") in by_id, cell.get("id")

javap = Path(os.environ.get("JAVA_HOME", "")) / "bin" / ("javap.exe" if os.name == "nt" else "javap")
if not javap.exists():
    print("XML e geometria válidos; JAVA_HOME indisponível para comparar bytecode.")
    sys.exit(0)

for name in class_names:
    result = subprocess.run(
        [str(javap), "-p", "-classpath", str(base / "target/classes"), f"br.edu.nexusheroes.{name}"],
        capture_output=True, text=True, check=True,
    )
    declared_fields = set()
    declared_methods = set()

    def normalized_type(raw):
        for prefix in ("java.lang.", "java.util.", "br.edu.nexusheroes."):
            raw = raw.replace(prefix, "")
        return re.sub(r"\s+", "", raw)

    def visibility(raw):
        return "+" if "public" in raw else "#" if "protected" in raw else "-" if "private" in raw else "~"

    for line in result.stdout.splitlines():
        line = line.strip()
        if not line.endswith(";") or line.startswith("Compiled from"):
            continue
        if "(" in line:
            before, after = line.split("(", 1)
            method = before.split()[-1].split(".")[-1]
            if method not in {"equals", "hashCode", "toString"}:
                params = tuple(normalized_type(p) for p in after.split(")", 1)[0].split(",") if p.strip())
                return_type = None if method == name else normalized_type(before.split()[-2])
                declared_methods.add((method, params, return_type, visibility(before)))
        else:
            before = line[:-1]
            field = before.split()[-1]
            type_start = re.sub(r"^(public|protected|private|static|final|transient|volatile)\s+", "", before)
            while type_start != (next_start := re.sub(r"^(public|protected|private|static|final|transient|volatile)\s+", "", type_start)):
                type_start = next_start
            field_type = type_start.rsplit(" ", 1)[0]
            declared_fields.add((field, normalized_type(field_type), visibility(before)))
    uml_fields = set()
    uml_methods = set()
    for cell in cells:
        cid = cell.get("id", "")
        value = cell.get("value", "")
        if cid.startswith(name + "-a") and re.match(r"^[+#~\-] ", value):
            field, field_type = value[2:].split(":", 1)
            uml_fields.add((field.strip(), normalized_type(field_type.split("=", 1)[0].split("{", 1)[0]), value[0]))
        if cid.startswith(name + "-m") and re.match(r"^[+#~\-] ", value):
            method, after = value[2:].split("(", 1)
            param_text, tail = after.split(")", 1)
            params = tuple(normalized_type(p.split(":", 1)[1]) for p in param_text.split(",") if p.strip())
            return_type = normalized_type(tail.split(":", 1)[1].split("{", 1)[0]) if ":" in tail else None
            uml_methods.add((method, params, return_type, value[0]))
    assert declared_fields == uml_fields, f"{name} campos: Java {declared_fields}, UML {uml_fields}"
    assert declared_methods == uml_methods, f"{name} métodos: Java {declared_methods}, UML {uml_methods}"

print(f"XML válido; {len(class_names)} classes Java conferidas; "
      f"{sum(c.get('edge') == '1' for c in cells)} relações/conectores; sem sobreposição de caixas.")
