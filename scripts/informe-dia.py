#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""El informe del día para Juanjo (ADR 0069), sin IA: si ha salido todo, si se ha usado la reserva, a quién se ha
escrito y qué ha fallado. Lo lanza reloj.sh una vez al día, en cuanto se puede dar: entre semana, cuando ya han salido
el número, los avisos de los grupos, los privados y el carrusel de Instagram (hacia las 7:10); el domingo, además,
cuando han salido «La semana en vídeo» en Instagram y el dominical en X, Bluesky y LinkedIn.

    scripts/informe-dia.py AAAA-MM-DD            escribe el informe (la fecha de las conversaciones, como noche.sh)
    scripts/informe-dia.py AAAA-MM-DD --listo    sale con 0 si ya se puede dar, 1 si aún falta algo
    scripts/informe-dia.py AAAA-MM-DD --enviar   lo escribe y lo deja para que el Bot de IA Educativa se lo mande a Juanjo
                                                 (su ADR 0040); si no puede dejarlo, por avisar-juanjo
"""
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BOT = pathlib.Path(os.environ.get("DATOS_BOT", "/bot-datos"))
DOMINICAL = pathlib.Path(os.environ.get("DOMINICAL", "/dominical"))   # el estado del dominical, del contenedor del boletín
REDES = ("x", "bluesky", "linkedin")
AVISOS_BOT = pathlib.Path(os.environ.get("AVISOS_BOT", "/avisos-bot"))   # la carpeta que recoge el Bot de IA Educativa
LINKEDIN = "https://www.linkedin.com/in/jjdeharo/recent-activity/all/"   # LinkedIn no da el enlace de la publicación
SECCIONES = ("ediciones", "biblioteca", "repositorio", "hace-un-ano", "reportajes")


def leer(f):
    try:
        return json.loads(pathlib.Path(f).read_text())
    except (OSError, ValueError):
        return None


def existe(nombre):
    return (RAIZ / "estado" / nombre).exists()


def contenido(nombre):
    try:
        return (RAIZ / "estado" / nombre).read_text().strip()
    except OSError:
        return ""


def domingo(fecha):
    return datetime.date.fromisoformat(fecha).isoweekday() == 6   # conversaciones del sábado: el número sale el domingo


def enlace_dominical(fecha, r):
    """El enlace de lo publicado en esa red, del registro del dominical («Publicado: https://…» tras «=== red»)."""
    try:
        lineas = (DOMINICAL / f"{fecha}.log").read_text(errors="replace").splitlines()
    except OSError:
        return ""
    red, enlace = None, ""
    for l in lineas:
        m = re.search(r"=== (\w+)", l)
        if m:
            red = m.group(1)
            continue
        m = re.search(r"Publicado:\s*(https?://\S+)", l)
        if m and red == r:
            enlace = m.group(1)
    return enlace


def red_hecha(fecha, r):
    """Hecha si ha publicado o si ya ha dejado de intentarlo (dos intentos)."""
    if (DOMINICAL / f"{fecha}.{r}").exists():
        return True
    try:
        return int((DOMINICAL / f"{fecha}.{r}-intentos").read_text().strip()) >= 2
    except (OSError, ValueError):
        return False


def terminado(fecha, que):
    """Instagram («instagram» o «instagram-reel»): publicado, o intentado hace más de 15 minutos sin resultado (fallido)."""
    if existe(f"{fecha}.{que}"):
        return True
    f = RAIZ / "estado" / f"{fecha}.{que}-intento"
    return f.exists() and datetime.datetime.now().timestamp() - f.stat().st_mtime > 15 * 60


def listo(fecha):
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    if not existe(f"{fecha}.publicado") or not (BOT / "diario" / f"{publica}.publicado.json").exists():
        return False
    if (RAIZ / "instagram" / fecha).is_dir() and not terminado(fecha, "instagram"):
        return False
    if domingo(fecha):
        if (RAIZ / "instagram" / f"reel-{fecha}" / "reel.mp4").exists() and not terminado(fecha, "instagram-reel"):
            return False
        if DOMINICAL.is_dir() and not (DOMINICAL / f"{fecha}.sin-video").exists() and not all(red_hecha(fecha, r) for r in REDES):
            return False
    return True


def nombres():
    """{id de Telegram: nombre visible}, de los mensajes de los grupos."""
    out = {}
    for g in ("chatgpt", "vce", "edumedia"):
        try:
            for linea in (BOT / g / "mensajes.jsonl").open():
                try:
                    m = json.loads(linea)
                    out[int(m["autor_id"])] = m.get("autor") or (("@" + m["usuario"]) if m.get("usuario") else str(m["autor_id"]))
                except (ValueError, KeyError, TypeError):
                    continue
        except OSError:
            continue
    return out


def piezas(fecha):
    out = []
    for s in ("ediciones", "biblioteca", "repositorio"):
        d = leer(RAIZ / s / f"{fecha}.json") or {}
        if s == "ediciones" and not d.get("hay_edicion", True):
            continue
        out += [(s, p) for p in d.get("piezas") or []]
    return out


def registro(fecha):
    try:
        return (RAIZ / "registro" / f"{fecha}.log").read_text(errors="replace").splitlines()
    except OSError:
        return []


def avisos_del_registro(lineas):
    """Las líneas de ERROR y AVISO del registro de la noche, sin repetir, en corto."""
    vistas, out = set(), []
    for l in lineas:
        m = re.search(r"\b(ERROR|AVISO)\b:?\s+(\S.{2,})", l)   # «AVISO: …», no «AVISOS» ni restos sueltos
        if not m:
            continue
        t = re.sub(r"\s+", " ", m.group(2)).strip()[:160]
        if t not in vistas:
            vistas.add(t)
            out.append(t)
    return out


def informe(fecha):
    publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
    ed = leer(RAIZ / "ediciones" / f"{fecha}.json") or {}
    lineas = registro(fecha)
    quien = nombres()
    t = [f"Informe del diario · número del {datetime.date.fromisoformat(publica).strftime('%d-%m-%Y')}", ""]
    problemas = []

    # 1. El número
    ps = piezas(fecha)
    reserva = ed.get("piezas_reserva") or []
    t.append("EL NÚMERO")
    if existe(f"{fecha}.publicado"):
        t.append(f"• Publicado en la web: {len(ps)} artículo(s).")
    else:
        t.append("• No se ha publicado.")
        problemas.append("El número no se ha publicado.")
    if ed.get("reserva") == "fallo":
        t.append("• Salió con el número de reserva porque falló la redacción: las conversaciones de ayer salen mañana.")
        problemas.append("La redacción falló y salió la reserva.")
    elif ed.get("reserva") == "relleno":
        t.append("• No había conversaciones que contar: salió entero con la reserva.")
    if reserva:
        tit = ed.get("titulares_reserva") or reserva
        t.append(f"• Artículos de reserva usados: {len(reserva)}: " + "; ".join(f"«{x[:110]}»" for x in tit) + ".")
    # La maqueta, según la revisión de las 5:00 (scripts/revisar-maqueta.py, ADR 0041)
    maq = leer(RAIZ / "registro" / f"{fecha}-maqueta.json")
    if maq:
        bloques = sorted({b for f in maq for b in f.get("bloques", [])}) or ["la portada"]
        t.append(f"• Maqueta: la revisión de las 5:00 encontró huecos en {', '.join(bloques)}; se avisó entonces, con las capturas.")
        problemas.append("La maqueta tenía huecos a las 5:00.")
    vin = leer(RAIZ / "vinetas" / f"{fecha}.json") or {}
    if not vin.get("elegida"):
        t.append("• Sin viñeta.")
        problemas.append("El número salió sin viñeta.")
    elif vin.get("reserva"):
        t.append("• Viñeta: la de reserva.")
    hu = leer(RAIZ / "hace-un-ano" / f"{fecha}.json") or {}
    if hu.get("piezas"):
        adelantado = any("escrito por adelantado" in l for l in lineas) or any("Hace un año" in str(x) for x in reserva)
        t.append(f"• «Hace un año»: sí{' (escrito por adelantado)' if adelantado else ''}.")
    else:
        t.append("• Sin «Hace un año».")
    if domingo(fecha):
        rep = leer(RAIZ / "reportajes" / f"{fecha}.json") or {}
        if rep.get("hay_reportaje"):
            el = leer(RAIZ / "reportajes-borrador" / f"{fecha}-eleccion.json") or {}
            origen = "uno de reserva" if rep.get("reserva") else "el nuevo de la semana"
            t.append(f"• Reportaje: {origen}, «{rep.get('titular', '')[:90]}».")
            if el.get("elegido") and (el["elegido"] != "nuevo") != bool(rep.get("reserva")):
                t.append("  Cambiado a mano después de que lo eligiera el juez.")
            elif el.get("motivo"):
                t.append(f"  Por qué lo eligió el juez: {el['motivo'][:200]}")
        else:
            t.append("• Sin reportaje.")
            problemas.append("El domingo salió sin reportaje.")

    # 2. Los mensajes
    t += ["", "MENSAJES"]
    pub = leer(BOT / "diario" / f"{publica}.publicado.json") or {}
    grupos = {"chatgpt": "ChatGPT-IA-edu", "vce": "Vibe Coding Educativo", "edumedia": "EduMedia-IAG"}
    hechos = pub.get("grupos") or []
    faltan = [v for k, v in grupos.items() if k not in hechos]
    t.append(f"• Avisos en los grupos: {', '.join(grupos[g] for g in hechos if g in grupos) or 'ninguno'}.")
    if faltan:
        problemas.append(f"Sin aviso en: {', '.join(faltan)}.")
    privados = leer(BOT / "diario" / f"{publica}.privados.json") or []
    personas = (leer(BOT / "diario" / f"{publica}.json") or {}).get("personas") or []
    if personas:
        enviados = [quien.get(i, str(i)) for i in privados]
        t.append(f"• Avisos privados: {', '.join(enviados) if enviados else 'ninguno'}.")
        sin = [quien.get(p["id"], str(p["id"])) for p in personas if p.get("id") not in privados]
        if sin:
            t.append(f"  Sin enviar (no han hablado nunca con el bot o no quieren avisos): {', '.join(sin)}.")
    else:
        t.append("• Avisos privados: nadie que avisar.")

    # 3. Las redes
    t += ["", "REDES"]
    if existe(f"{fecha}.instagram"):
        t.append(f"• Instagram, carrusel: {contenido(f'{fecha}.instagram').splitlines()[0]}")
    elif terminado(fecha, "instagram"):
        t.append("• Instagram, carrusel: no se ha podido publicar.")
        problemas.append("El carrusel de Instagram no ha salido.")
    else:
        t.append("• Instagram, carrusel: no tocaba (sin imágenes o sin permiso).")
    if domingo(fecha):
        if existe(f"{fecha}.instagram-reel"):
            t.append(f"• Instagram, «La semana en vídeo»: {contenido(f'{fecha}.instagram-reel').splitlines()[0]}")
        elif terminado(fecha, "instagram-reel"):
            t.append("• Instagram, «La semana en vídeo»: no se ha podido publicar.")
            problemas.append("El vídeo de la semana no ha salido en Instagram.")
        if DOMINICAL.is_dir():
            if (DOMINICAL / f"{fecha}.sin-video").exists():
                t.append("• Dominical en X, Bluesky y LinkedIn: no ha salido, faltaba el vídeo.")
                problemas.append("El dominical no ha salido: faltaba el vídeo.")
            for r, nom in (("x", "X"), ("bluesky", "Bluesky"), ("linkedin", "LinkedIn")):
                if (DOMINICAL / f"{fecha}.{r}").exists():
                    enlace = enlace_dominical(fecha, r) or (f"publicado (LinkedIn no da el enlace; tu actividad: {LINKEDIN})"
                                                            if r == "linkedin" else "publicado")
                    t.append(f"• Dominical en {nom}: {enlace}")
                elif red_hecha(fecha, r):
                    t.append(f"• Dominical en {nom}: no ha salido tras dos intentos.")
                    problemas.append(f"El dominical no ha salido en {nom}.")

    # 4. Lo que ha fallado o conviene mirar
    if existe(f"{fecha}.avisado"):
        problemas.append("Tuvo que actuar el plan B de las 6:30.")
    if existe(f"{fecha}.publicar-fallo"):
        problemas.append("La publicación falló a la primera y se reintentó.")
    for nombre, texto in ((f"{fecha}-autoria.txt", "posibles atribuciones a un autor del diario de algo de otra persona"),
                          (f"{fecha}-estilo.txt", "frases de estilo sin corregir («quien» o citas solo en inglés)"),
                          (f"{fecha}-traduccion.txt", "traducciones quitadas (esas ediciones salen en castellano)")):
        f = RAIZ / "registro" / nombre
        if f.exists() and f.read_text().strip():
            problemas.append(f"{len(f.read_text().strip().splitlines())} {texto}.")
    # Los que siguen sin dibujo: un retirado que se ha vuelto a poner a mano no cuenta
    carpeta = RAIZ / "revision" / fecha / "retirados"
    retirados = [f for f in carpeta.glob("*.svg") if not (RAIZ / (f.name.split("-", 1)[0].replace("es", "ilustraciones", 1) if f.name.startswith("es-")
                 else "ilustraciones-" + f.name.split("-", 1)[0]) / f.name.split("-", 1)[1]).exists()] if carpeta.is_dir() else []
    if retirados:
        problemas.append(f"{len(retirados)} dibujo(s) retirado(s) por no pasar la revisión.")
    otros = [a for a in avisos_del_registro(lineas) if not re.search(r"Internet Archive|quedan sin subir", a)]
    t += ["", "FALLOS Y AVISOS"]
    if problemas or otros:
        t += [f"• {p}" for p in problemas]
        t += [f"• Del registro: {a}" for a in otros[:6]]
        if len(otros) > 6:
            t.append(f"  (y {len(otros) - 6} más en registro/{fecha}.log)")
    else:
        t.append("• Ninguno.")

    # 5. La reserva
    sys.path.insert(0, str(RAIZ / "scripts"))
    try:
        import reserva, reserva_reportaje, reserva_vineta, reserva_hace_un_ano   # noqa: E401, E402
        hu_n = len([d for d in reserva_hace_un_ano.RESERVA.glob("20*")])
        t += ["", "RESERVA",
              f"• {len(reserva.listas())} artículos (objetivo {reserva.OBJETIVO}), {len(reserva_reportaje.listos())} reportaje(s), "
              f"{len(reserva_vineta.listas())} viñeta(s) y {hu_n} «Hace un año» por adelantado."]
        if len(reserva.listas()) < reserva.MINIMO:
            t.append("  Menos artículos de los que necesita un número entero: se reponen uno cada mañana.")
    except Exception as ex:  # noqa: BLE001 — el informe sale igual sin este apartado
        t += ["", f"RESERVA: no se ha podido contar ({type(ex).__name__})."]
    return "\n".join(t)


def main():
    fecha = sys.argv[1]
    if "--listo" in sys.argv:
        sys.exit(0 if listo(fecha) else 1)
    texto = informe(fecha)
    print(texto)
    if "--enviar" in sys.argv:
        publica = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).isoformat()
        try:
            (AVISOS_BOT / f"{publica}.informe.txt").write_text(texto + "\n")
        except OSError:
            subprocess.run(["avisar-juanjo", "--de", "Diario de IA Educativa", texto], check=False)


if __name__ == "__main__":
    main()
