#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Prepara la entrada del documentalista: los documentos nuevos de la Biblioteca digital (ADR 0006).

    biblioteca.py <carpeta de datos del bot> <carpeta de salida> <AAAA-MM-DD> [id ...]
    biblioteca.py <carpeta de datos del bot> <carpeta de salida> <clave> fondo

Con «fondo» prepara una pieza de reserva (ADR 0021): CANDIDATOS_FONDO documentos de la biblioteca
que el diario no ha contado, para que el documentalista elija uno que siga vigente y escriba
«Del fondo de la biblioteca».

La Biblioteca digital es el tema «Biblioteca digital» de ChatGPT-IA-edu. Cada documento es un
mensaje raíz del tema (no una respuesta) con un archivo o con una ficha de texto; la ficha puede
ir en el propio mensaje o en una respuesta de la misma persona. Escribe <salida>/<fecha>.md con
los documentos que entraron ese día (o los mensajes que se indiquen, para rehacer o recuperar
documentos anteriores) y, como contexto, la lista de toda la biblioteca, de los artículos ya
publicados en la sección y de las piezas recientes del diario, para no contar dos veces un
documento que ya salió como noticia. Sin IA: solo ordena. Termina con código 3 si no hay ningún
documento.
"""
import json
import pathlib
import sys

TEMA = "21753"            # «Biblioteca digital» en ChatGPT-IA-edu
ALIAS = "ChatGPTedu"
MINIMO = 300              # caracteres de texto para que una entrada sin archivo cuente como documento
RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIAS_RECIENTES = 30       # piezas del diario con las que se compara cada documento nuevo
CANDIDATOS_FONDO = 3      # documentos que se proponen para una pieza de reserva
DIAS_FONDO = 7            # lo que entró en la última semana no es fondo: lo cuenta el día


def entradas(base):
    msgs = [json.loads(l) for l in (base / "chatgpt" / "mensajes.jsonl").open()]
    tema = [m for m in msgs if str(m.get("tema")) == TEMA]
    respuestas = {}
    for m in tema:
        if m.get("responde_a"):
            respuestas.setdefault(m["responde_a"], []).append(m)
    out = []
    for m in tema:
        if m.get("responde_a"):
            continue
        ficha = [r for r in respuestas.get(m["id"], []) if r.get("autor_id") == m.get("autor_id")]
        texto = "\n\n".join(x for x in [(m.get("texto") or "").strip()] + [(r.get("texto") or "").strip() for r in ficha] if x)
        archivo = m.get("mime") == "application/pdf" or m.get("media") == "Document"
        if not archivo and len(texto) < MINIMO:
            continue   # un comentario o un enlace suelto, no un documento de la biblioteca
        pdf = base / "chatgpt" / "pdf-texto" / f"{m['id']}.txt"
        entero = base / "chatgpt" / "pdf-completo" / f"{m['id']}.txt"   # lo guarda el bot desde 10-2026 (su ADR 0026)
        out.append({"id": m["id"], "fecha": m["fecha"], "archivo": archivo, "texto": texto,
                    "pdf": pdf.read_text(errors="replace").strip() if pdf.exists() else "",
                    "entero": entero.read_text(errors="replace").strip() if entero.exists() else "",
                    "titulo": texto.split("\n", 1)[0].strip()[:160]})
    return out


def articulos():
    """Los documentos ya contados: id del mensaje → (fecha, id de la pieza, titular). Cuenta
    también los que no tuvieron artículo propio porque el diario ya los había contado (`ya_contado`)."""
    hechos = {}
    for f in sorted((RAIZ / "biblioteca").glob("*.json")):
        d = json.loads(f.read_text())
        for p in d.get("piezas", []):
            hechos[(p.get("mensaje") or {}).get("id")] = (f.stem, p["id"], p["titular"])
        for y in d.get("ya_contado", []):
            hechos[(y.get("mensaje") or {}).get("id")] = (y.get("fecha"), y.get("id"), y.get("titular", ""))
    return hechos


def en_reserva():
    """Los documentos que ya esperan en la reserva, o que ya se propusieron para ella y se descartaron
    (también en la retirada): no se vuelven a proponer."""
    import re
    ids = set()
    for f in list((RAIZ / "reserva").glob("*/biblioteca.json")) + list((RAIZ / "reserva" / "retiradas").glob("*/biblioteca.json")) \
            + list((RAIZ / "biblioteca").glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        for p in d.get("piezas", []) + d.get("ya_contado", []):
            ids.add((p.get("mensaje") or {}).get("id"))
        for x in d.get("descartado", []):
            ids.update(int(n) for n in re.findall(r"mensaje (\d+)", str(x)))
    return ids


def recientes(fecha):
    """Las piezas del diario de los últimos días, con sus fuentes, para reconocer un documento ya contado."""
    import datetime
    desde = (datetime.date.fromisoformat(fecha) - datetime.timedelta(days=DIAS_RECIENTES)).isoformat()
    lineas = []
    for f in sorted((RAIZ / "ediciones").glob("*.json"), reverse=True):
        if not (desde <= f.stem <= fecha):
            continue
        for p in json.loads(f.read_text()).get("piezas", []):
            fuentes = " · ".join(x.get("url", "") for x in p.get("fuentes", []) if x.get("url"))
            lineas.append(f"- fecha {f.stem}, id {p['id']} ({p.get('seccion')}): {p['titular']}"
                          + (f" — fuentes: {fuentes}" if fuentes else ""))
    return lineas


def main():
    base, out, fecha = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    fondo = sys.argv[4:] == ["fondo"]
    pedidos = set() if fondo else {int(x) for x in sys.argv[4:]}
    todas = entradas(base)
    hechos = articulos()
    if fondo:
        import datetime
        import random
        limite = (datetime.date.today() - datetime.timedelta(days=DIAS_FONDO)).isoformat()
        fuera = set(hechos) | en_reserva()
        nuevas = [e for e in todas if e["id"] not in fuera and e["fecha"][:10] <= limite]
        # Lo más reciente tiene más posibilidades de seguir vigente; un poco de azar para variar
        nuevas.sort(key=lambda e: e["fecha"], reverse=True)
        nuevas = nuevas[:CANDIDATOS_FONDO * 3]
        random.Random(fecha).shuffle(nuevas)
        nuevas = nuevas[:CANDIDATOS_FONDO]
    else:
        nuevas = [e for e in todas if (e["id"] in pedidos if pedidos else e["fecha"].startswith(fecha))]
    if not pedidos and not fondo:
        nuevas = [e for e in nuevas if e["id"] not in hechos]
    out.mkdir(parents=True, exist_ok=True)
    partes = [f"# Biblioteca digital de ChatGPT-IA-edu · documentos para el {fecha}\n"]
    if fondo:
        partes.append("## Del fondo de la biblioteca: pieza de reserva\n\n"
                      f"Estos {len(nuevas)} documentos son candidatos del fondo de la biblioteca: entraron hace tiempo y el "
                      "diario no los ha contado. **Elige uno solo**, el que siga vigente (lee el apartado «Del fondo de la "
                      "biblioteca» de encargos/biblioteca.md), y escribe su artículo. Los demás van a `descartado`, cada "
                      "uno empezando por «mensaje <id>:» y con el motivo.\n")
    for e in nuevas:
        partes.append(f"\n## Documento del mensaje {e['id']}\n")
        partes.append(f"- Entró en la biblioteca: {e['fecha'][:10]}")
        partes.append(f"- Mensaje en el grupo: https://t.me/{ALIAS}/{TEMA}/{e['id']} (campo `mensaje`: grupo chatgpt, id {e['id']})")
        partes.append(f"- Con archivo PDF en el grupo: {'sí' if e['archivo'] else 'no, es un enlace con su ficha'}")
        partes.append(f"\n### Mensaje y ficha publicados en la biblioteca\n\n{e['texto']}\n")
        if e["entero"]:
            partes.append(f"### Texto completo del PDF publicado en la biblioteca (extraído sin formato)\n\n{e['entero']}\n")
        elif e["pdf"]:
            partes.append(f"### Comienzo del PDF (solo las primeras páginas; el documento entero, en su fuente oficial)\n\n{e['pdf']}\n")
    partes.append("\n## Toda la biblioteca (para relacionar el documento con otros; no es noticia)\n")
    for e in todas:
        partes.append(f"- {e['fecha'][:10]} · {e['titulo']} · https://t.me/{ALIAS}/{TEMA}/{e['id']}")
    if hechos:
        partes.append("\n## Artículos ya publicados en la sección Biblioteca del diario\n")
        for (f, pid, tit) in hechos.values():
            partes.append(f"- {tit} → fecha {f}, id {pid}")
    previas = recientes(fecha)
    if previas:
        partes.append(f"\n## Piezas publicadas en el diario en los últimos {DIAS_RECIENTES} días "
                      "(para ver si un documento ya se ha contado)\n")
        partes.extend(previas)
    (out / f"{fecha}.md").write_text("\n".join(partes) + "\n")
    print(f"biblioteca: {len(nuevas)} documento(s) para el {fecha} ({', '.join(str(e['id']) for e in nuevas)})")
    sys.exit(0 if nuevas else 3)


if __name__ == "__main__":
    main()
