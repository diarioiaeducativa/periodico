#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Las normas públicas del diario en las otras lenguas (ADR 0085).

    scripts/normas_traducir.py pendientes            una línea por traducción que falta o se ha quedado atrás:
                                                     «origen destino huella lengua»
    scripts/normas_traducir.py comprobar ORIGEN DESTINO HUELLA
                                                     sale con 0 si la traducción vale; si no, la borra y sale con 4
    scripts/normas_traducir.py vigente ORIGEN DESTINO   sale con 0 si la traducción es de la versión actual

Los tres documentos (docs/como-se-hace.md, encargos/estilo.md, encargos/traduccion.md) se escriben en castellano,
que es como los leen los agentes. Su traducción va en docs/traducciones/<lengua>/<nombre>.md, con la huella del
original en la primera línea; scripts/normas-traducir.sh la rehace cuando el original cambia, y generar.py solo
publica la página de una lengua si su traducción es de la versión actual.
"""
import hashlib
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOCUMENTOS = ("docs/como-se-hace.md", "encargos/estilo.md", "encargos/traduccion.md")
LENGUAS = ("ca", "gl", "eu", "en")
ORIGEN = re.compile(r"^<!-- origen: ([0-9a-f]+) -->")


def huella(origen):
    return hashlib.sha256((RAIZ / origen).read_bytes()).hexdigest()[:16]


def destino(origen, c):
    return f"docs/traducciones/{c}/{pathlib.Path(origen).name}"


def vigente(origen, dest):
    f = RAIZ / dest
    if not f.exists():
        return False
    m = ORIGEN.match(f.read_text(encoding="utf-8"))
    return bool(m) and m.group(1) == huella(origen)


def forma(t):
    """Lo que tiene que coincidir entre el original y la traducción."""
    t = re.sub(r"^<!--.*?-->\n?", "", t)
    return {
        "títulos": len(re.findall(r"^#{1,4} ", t, re.M)),
        "puntos": len(re.findall(r"^(?:- |\d+\. )", t, re.M)),
        "filas de tabla": len(re.findall(r"^\|", t, re.M)),
        "código": sorted(re.findall(r"`([^`]+)`", t)),
        "enlaces": sorted(re.findall(r"\]\(([^)\s]+)\)", t)),
        "ADR": sorted(re.findall(r"\b00\d{2}\b", t)),   # los números de los registros (0001…), en cualquier lengua
    }


def comprobar(origen, dest, h):
    f = RAIZ / dest
    malos = []
    if not f.exists():
        malos.append("no está")
    else:
        t = f.read_text(encoding="utf-8")
        m = ORIGEN.match(t)
        if not m or m.group(1) != h:
            malos.append("falta la huella del original en la primera línea")
        a, b = forma((RAIZ / origen).read_text(encoding="utf-8")), forma(t)
        malos += [f"no tiene {k} iguales ({a[k] if not isinstance(a[k], list) else len(a[k])} frente a "
                  f"{b[k] if not isinstance(b[k], list) else len(b[k])})" for k in a if a[k] != b[k]]
        if len(t) < 0.6 * len((RAIZ / origen).read_text(encoding="utf-8")):
            malos.append("es demasiado corta")
    if malos:
        f.unlink(missing_ok=True)
        print(f"{dest} quitado: " + "; ".join(malos))
        return 4
    print(f"{dest}: bien")
    return 0


def main():
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "pendientes":
        for o in DOCUMENTOS:
            for c in LENGUAS:
                d = destino(o, c)
                if not vigente(o, d):
                    print(o, d, huella(o), c)
        return 0
    if orden == "comprobar" and len(sys.argv) == 5:
        return comprobar(*sys.argv[2:5])
    if orden == "vigente" and len(sys.argv) == 4:
        return 0 if vigente(*sys.argv[2:4]) else 1
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
