#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""La viñeta diaria: Tiza y Algoritmo en una tira de tres viñetas.

Los personajes están dibujados aquí, una sola vez, con un repertorio cerrado de
expresiones, posturas y objetos. La IA solo escribe el guion (qué dicen, con qué
cara, en qué postura y con qué objeto); este módulo lo convierte en SVG. Así el
dibujo es siempre el mismo y todo el esfuerzo de la IA va al humor.

Clases de color: las de comun.css (t, a, r, fa, ft, fz) y las propias de la viñeta
(tz: cuerpo de la tiza, cara: rasgos sobre la tiza, sp: rasgos sobre el cursor)."""
import html
import textwrap

ANCHO, ALTO, SUELO = 400, 360, 332
ESCALA = 1.18   # tamaño de los personajes respecto al dibujo base

EXPRESIONES = ["neutral", "contento", "sorprendido", "preocupado", "orgulloso", "pensativo", "enfadado", "cargando",
               "agotado", "riendo", "avergonzado", "harto"]
POSTURAS = ["abajo", "senalar", "arriba", "pensar", "encoger", "sostener"]
OBJETOS = ["pizarra", "portatil", "reloj", "examenes", "papeles", "libro", "movil", "folio", "taza", "notificaciones"]
DE_FONDO = {"pizarra", "portatil", "reloj", "examenes", "papeles"}   # van en el centro; los demás, en la mano de quien «sostiene»
ESCENARIOS = ["aula", "sala_profes", "fotocopiadora", "claustro", "casa_noche", "biblioteca", "despacho", "videollamada"]


def e(t):
    return html.escape(t or "", quote=True)


# ---------- Rasgos de la cara (coordenadas relativas al centro de la cara) ----------

def cara(expr, clase, ojo_clase, ojo_r):
    """Ojos, cejas y boca. `clase` pinta los trazos; `ojo_clase` rellena los ojos."""
    o = []
    if expr == "orgulloso":
        o.append(f'<path class="{clase}" d="M-12 0 Q-9 -3 -6 0 M6 0 Q9 -3 12 0"/>')
    elif expr == "agotado":   # ojos entornados y ojeras
        o.append(f'<path class="{clase}" d="M-12 0 L-6 0 M6 0 L12 0"/><path class="{clase} fino" d="M-12 5 Q-9 8 -6 5 M6 5 Q9 8 12 5"/>')
    elif expr == "riendo":    # ojos cerrados de risa
        o.append(f'<path class="{clase}" d="M-12 2 Q-9 -4 -6 2 M6 2 Q9 -4 12 2"/>')
    elif expr == "harto":     # párpados a media asta
        o.append(f'<circle class="{ojo_clase}" cx="-9" cy="1.5" r="{ojo_r - 0.4}"/><circle class="{ojo_clase}" cx="9" cy="1.5" r="{ojo_r - 0.4}"/>'
                 f'<path class="{clase}" d="M-13 -1 L-5 -1 M5 -1 L13 -1"/>')
    elif expr == "avergonzado":   # mirada al suelo
        o.append(f'<circle class="{ojo_clase}" cx="-10" cy="2.5" r="{ojo_r}"/><circle class="{ojo_clase}" cx="8" cy="2.5" r="{ojo_r}"/>')
    elif expr == "sorprendido":
        o.append(f'<circle class="{ojo_clase}" cx="-9" cy="0" r="{ojo_r + 1.2}"/><circle class="{ojo_clase}" cx="9" cy="0" r="{ojo_r + 1.2}"/>')
    else:
        o.append(f'<circle class="{ojo_clase}" cx="-9" cy="0" r="{ojo_r}"/><circle class="{ojo_clase}" cx="9" cy="0" r="{ojo_r}"/>')
    cejas = {
        "sorprendido": "M-13 -10 Q-9 -13 -5 -10 M5 -10 Q9 -13 13 -10",
        "preocupado": "M-13 -7 L-5 -10 M13 -7 L5 -10",
        "enfadado": "M-13 -10 L-5 -6 M13 -10 L5 -6",
        "pensativo": "M5 -10 Q9 -13 13 -10",
        "avergonzado": "M-13 -7 L-5 -9 M13 -7 L5 -9",
        "agotado": "M-13 -6 L-5 -7 M13 -6 L5 -7",
    }.get(expr)
    if cejas:
        o.append(f'<path class="{clase}" d="{cejas}"/>')
    boca = {
        "neutral": "M-6 15 L6 15",
        "contento": "M-8 12 Q0 21 8 12",
        "preocupado": "M-7 18 Q0 12 7 18",
        "orgulloso": "M-6 15 Q3 19 9 11",
        "pensativo": "M-2 16 L6 14",
        "enfadado": "M-7 18 Q0 13 7 18",
        "agotado": "M-5 16 Q0 14 5 16",
        "riendo": "M-8 11 L8 11 Q0 24 -8 11 Z",
        "avergonzado": "M-5 16 Q-2 14 0 16 Q2 18 5 16",
        "harto": "M-6 16 L6 16",
    }.get(expr)
    if expr == "sorprendido":
        o.append(f'<ellipse class="{clase}" cx="0" cy="16" rx="4" ry="5"/>')
    elif expr == "cargando":
        o.append(f'<circle class="{ojo_clase}" cx="-7" cy="16" r="1.8"/><circle class="{ojo_clase}" cx="0" cy="16" r="1.8"/><circle class="{ojo_clase}" cx="7" cy="16" r="1.8"/>')
    elif boca:
        o.append(f'<path class="{clase}" d="{boca}"/>')
    if expr == "avergonzado":   # el rubor, en el rojo de corregir
        o.append('<path class="rubor" d="M-19 9 L-15 6 M-15 10 L-11 7 M11 7 L15 10 M15 6 L19 9"/>')
    return "".join(o)


# ---------- Brazos (mirando a la derecha; se reflejan si el personaje mira a la izquierda) ----------

def brazos(postura, hombro_y, medio, clase, barbilla=18):
    """Devuelve (trazos, punto de la mano delantera) para la postura. `barbilla`: cuánto sube la mano
    al pensar desde el hombro hasta la barbilla."""
    L, R, y = -medio, medio, hombro_y
    caido_izq = f"M{L} {y} Q{L - 10} {y + 20} {L - 8} {y + 38}"
    caido_der = f"M{R} {y} Q{R + 10} {y + 20} {R + 8} {y + 38}"
    mano = (R + 8, y + 38)
    if postura == "senalar":
        d = f"{caido_izq} M{R} {y} L{R + 32} {y - 16} M{R + 32} {y - 16} L{R + 40} {y - 19}"
        mano = (R + 40, y - 19)
    elif postura == "arriba":
        d = f"M{L} {y - 2} L{L - 16} {y - 32} M{R} {y - 2} L{R + 16} {y - 32}"
    elif postura == "pensar":
        d = f"{caido_izq} M{R} {y} Q{R + 10} {y - barbilla * 4 / 9} {R - 12} {y - barbilla}"
    elif postura == "encoger":
        d = f"M{L} {y + 2} L{L - 14} {y - 4} L{L - 18} {y - 14} M{R} {y + 2} L{R + 14} {y - 4} L{R + 18} {y - 14}"
    elif postura == "sostener":
        d = f"M{L} {y + 2} Q{L + 6} {y + 18} {R + 18} {y + 14} M{R} {y + 2} L{R + 20} {y + 12}"
        mano = (R + 22, y + 10)
    else:
        d = f"{caido_izq} {caido_der}"
    return f'<path class="{clase}" d="{d}"/>', mano


# ---------- Personajes ----------

def tiza(cx, mira, expr, postura):
    """Una barra de tiza con la punta gastada: el oficio de enseñar."""
    arriba, abajo, medio = SUELO - 150, SUELO - 18, 21
    cuerpo = (f'<path class="tz" d="M{-medio} {abajo - 10} L{-medio} {arriba + 12} Q{-medio} {arriba + 2} {-medio + 8} {arriba + 4} '
              f'L{-6} {arriba} L{2} {arriba + 5} L{9} {arriba + 1} L{medio - 4} {arriba + 6} Q{medio} {arriba + 6} {medio} {arriba + 14} '
              f'L{medio} {abajo - 10} Q{medio} {abajo} {medio - 10} {abajo} L{-medio + 10} {abajo} Q{-medio} {abajo} {-medio} {abajo - 10} Z"/>')
    # Las vetas, en el cuerpo y lejos de la cara (Juanjo, 07-11-2026: la que bajaba junto a la cara no le
    # gustaba), y del color oscuro del contorno, para que se vean también en tema oscuro
    vetas = f'<path class="cara" style="stroke-width:1.6" d="M{-medio + 6} {arriba + 96} L{-medio + 6} {arriba + 120} M{medio - 7} {arriba + 84} L{medio - 7} {arriba + 98}"/>'
    polvo = f'<circle class="ft polvo" cx="-14" cy="{arriba - 8}" r="1.4"/><circle class="ft polvo" cx="4" cy="{arriba - 13}" r="1.1"/><circle class="ft polvo" cx="15" cy="{arriba - 6}" r="1.3"/>'
    piernas = f'<path class="t" d="M-9 {abajo} L-11 {SUELO} L-19 {SUELO} M9 {abajo} L11 {SUELO} L19 {SUELO}"/>'
    br, mano = brazos(postura, arriba + 70, medio, "t")
    rostro = f'<g transform="translate(2 {arriba + 34})">{cara(expr, "cara", "fcara", 2.6)}</g>'
    # El brazo que cruza el cuerpo (pensar, sostener): en tema oscuro la tinta es clara como la tiza y no se
    # veía; va sobre un borde del color del papel, como el de Algoritmo (06-11-2026). En tema claro no se nota.
    borde = br.replace('class="t"', 'class="a-borde"') if postura in ("pensar", "sostener") else ""
    g = f'{piernas}{cuerpo}{vetas}{polvo}{rostro}{borde}{br}'
    return envolver(cx, mira, g), mano_abs(cx, mira, mano)


def algoritmo(cx, mira, expr, postura):
    """Un cursor de bloque que flota y parpadea: la IA, siempre dispuesta y no siempre acertada."""
    abajo, alto, medio = SUELO - 30, 86, 28
    arriba = abajo - alto
    cuerpo = f'<rect class="fz" x="{-medio}" y="{arriba}" width="{medio * 2}" height="{alto}" rx="7"/>'
    flota = f'<path class="a discontinuo" d="M-18 {abajo + 12} L18 {abajo + 12} M-10 {abajo + 21} L10 {abajo + 21}"/>'
    parpadeo = ""
    if expr == "cargando":
        parpadeo = f'<path class="a" d="M{-medio - 10} {arriba + 6} L{-medio - 18} {arriba - 2} M0 {arriba - 10} L0 {arriba - 20} M{medio + 10} {arriba + 6} L{medio + 18} {arriba - 2}"/>'
    # Al pensar, la mano a la barbilla y no al ojo (06-11-2026): el hombro está más cerca de la cara que en Tiza
    br, mano = brazos(postura, arriba + 50, medio, "a", barbilla=6)
    ojos = f'<circle class="ojo" cx="-9" cy="0" r="7"/><circle class="ojo" cx="9" cy="0" r="7"/>' if expr not in ("orgulloso", "agotado", "riendo") else ""
    if expr == "harto":   # el párpado del cursor, del mismo azul, tapa medio ojo
        ojos += '<rect class="fz" x="-17" y="-8" width="16" height="7"/><rect class="fz" x="1" y="-8" width="16" height="7"/>'
    pupilas_expr = expr if expr in ("orgulloso", "cargando") else expr
    rostro = f'<g transform="translate(2 {arriba + 28})">{ojos}{cara(pupilas_expr, "sp", "fpupila", 2.6)}</g>'
    if expr == "cargando":   # los puntos de «cargando» van en la boca, sobre el azul
        rostro = rostro.replace('class="fpupila" cx="-7" cy="16"', 'class="fsp" cx="-7" cy="16"').replace(
            'class="fpupila" cx="0" cy="16"', 'class="fsp" cx="0" cy="16"').replace('class="fpupila" cx="7" cy="16"', 'class="fsp" cx="7" cy="16"')
    # El brazo que cruza el cuerpo azul (pensar, sostener), sobre un borde del color del papel para que se vea (06-11-2026)
    borde = br.replace('class="a"', 'class="a-borde"') if postura in ("pensar", "sostener") else ""
    g = f'{flota}{cuerpo}{parpadeo}{rostro}{borde}{br}'
    return envolver(cx, mira, g), mano_abs(cx, mira, mano)


def envolver(cx, mira, g):
    sx = ESCALA if mira == "derecha" else -ESCALA
    return f'<g transform="translate({cx} {SUELO}) scale({sx} {ESCALA}) translate(0 {-SUELO})">{g}</g>'


def mano_abs(cx, mira, mano):
    x, y = mano
    x, y = x * ESCALA, SUELO + (y - SUELO) * ESCALA
    return (cx + x if mira == "derecha" else cx - x, y)


# La escena entera (suelo, decorado y personajes) baja BAJA px dentro del marco (06-11-2026): deja más
# sitio arriba para los globos sin achicar a nadie ni acortar los textos. Debajo del suelo quedan 8 px.
BAJA = 18
CABEZA = {q: BAJA + SUELO - (SUELO - y) * ESCALA for q, y in {"tiza": SUELO - 162, "algoritmo": SUELO - 30 - 86 - 6}.items()}


# ---------- Objetos ----------

def objeto(nombre, x, y):
    if nombre == "pizarra":
        return (f'<g transform="translate({x - 60} 168)"><rect class="t fa" x="0" y="0" width="120" height="78" rx="3"/>'
                f'<path class="t fino" d="M14 22 L70 22 M14 38 L92 38 M14 54 L56 54"/><path class="t" d="M30 78 L22 104 M90 78 L98 104"/></g>')
    if nombre == "portatil":
        return (f'<g transform="translate({x - 34} {SUELO - 48})"><rect class="t fa" x="6" y="0" width="56" height="38" rx="3"/>'
                f'<path class="t" d="M0 46 L68 46 L62 38 L6 38 Z"/></g>')
    if nombre == "libro":
        return f'<g transform="translate({x - 14} {y - 14})"><path class="t fa" d="M0 4 L14 0 L28 4 L28 26 L14 22 L0 26 Z"/><path class="t" d="M14 0 L14 22"/></g>'
    if nombre == "movil":
        return f'<g transform="translate({x - 9} {y - 16})"><rect class="t fa" x="0" y="0" width="18" height="30" rx="3"/><path class="t" d="M6 25 L12 25"/></g>'
    if nombre == "folio":
        return f'<g transform="translate({x - 12} {y - 18})"><path class="t tz" d="M0 0 L18 0 L24 6 L24 32 L0 32 Z"/><path class="cara fino" d="M4 12 L20 12 M4 18 L20 18 M4 24 L14 24"/></g>'
    if nombre == "taza":
        return f'<g transform="translate({x - 10} {y - 12})"><path class="t fa" d="M0 0 L18 0 L16 22 L2 22 Z"/><path class="t" d="M18 5 Q26 8 17 15 M6 -6 Q4 -10 7 -13 M12 -6 Q10 -10 13 -13"/></g>'
    if nombre == "reloj":   # en la pared, entre los dos
        return (f'<g transform="translate({x} 172)"><circle class="t fa" r="17"/><path class="t" d="M0 0 L0 -10 M0 0 L8 4"/>'
                f'<path class="t fino" d="M0 -14 L0 -12 M14 0 L12 0 M0 14 L0 12 M-14 0 L-12 0"/></g>')
    if nombre == "examenes":   # el montón de exámenes por corregir, en el suelo
        hojas = "".join(f'<rect class="t tz" x="{-26 + i}" y="{-8 * i - 8}" width="52" height="8" rx="1"/>' for i in range(5))
        return f'<g transform="translate({x} {SUELO})">{hojas}<path class="r" d="M-8 -50 L-3 -45 L8 -56"/></g>'
    if nombre == "papeles":   # papeles revueltos en el suelo
        return (f'<g transform="translate({x} {SUELO})"><path class="t tz" d="M-30 0 L-26 -14 L2 -10 L-2 0 Z"/>'
                f'<path class="t tz" d="M-6 0 L-4 -20 L22 -18 L24 0 Z"/><path class="t tz" d="M-18 -18 L2 -30 L14 -14 L-6 -4 Z"/>'
                f'<path class="cara fino" d="M-12 -18 L2 -26 M-8 -14 L6 -22"/></g>')
    if nombre == "notificaciones":   # el móvil que no para
        return (f'<g transform="translate({x - 9} {y - 16})"><rect class="t fa" x="0" y="0" width="18" height="30" rx="3"/>'
                f'<circle class="fr" cx="17" cy="1" r="6"/><path class="r" d="M24 -8 L29 -12 M26 -1 L32 -1 M24 6 L29 10"/></g>')
    return ""


# ---------- Escenarios (al fondo, con trazo suave para que manden los personajes) ----------

def escenario(nombre):
    if nombre == "aula":
        return ('<rect class="pizarra-verde" x="70" y="150" width="260" height="70" rx="3"/>'
                '<path class="tiza-linea" d="M92 172 L150 172 M92 188 L176 188 M92 204 L130 204"/>'
                '<path class="fondo" d="M70 224 L330 224"/>'
                '<path class="fondo" d="M0 296 L46 296 M8 296 L8 332 M40 296 L40 332 M354 296 L400 296 M360 296 L360 332 M392 296 L392 332"/>')
    if nombre == "sala_profes":
        return ('<rect class="corcho" x="130" y="150" width="140" height="62" rx="2"/>'
                '<rect class="nota" x="142" y="160" width="26" height="22"/><rect class="nota" x="180" y="166" width="30" height="20"/>'
                '<rect class="nota" x="224" y="158" width="28" height="26"/>'
                '<path class="fondo" d="M0 262 L60 262 L60 332 M0 262 L0 332"/>'
                '<path class="fondo" d="M18 262 L18 228 L44 228 L44 262 M22 240 L40 240 M26 250 Q31 244 36 250"/>'
                '<path class="fondo" d="M50 228 Q56 220 50 212 M42 226 Q48 218 42 210"/>')
    if nombre == "fotocopiadora":
        return ('<path class="mueble" d="M162 332 L162 238 L238 238 L238 332 Z"/>'
                '<path class="fondo" d="M156 238 L244 238 L244 226 L156 226 Z M174 262 L226 262 M174 282 L226 282 M244 236 L262 230 L262 238 L244 244"/>'
                '<circle class="fr" cx="228" cy="250" r="3.5"/>')
    if nombre == "claustro":
        return ('<path class="fondo" d="M40 228 L40 196 Q40 186 52 186 L72 186 Q84 186 84 196 L84 228 M316 228 L316 196 Q316 186 328 186 L348 186 Q360 186 360 196 L360 228"/>')
    if nombre == "casa_noche":
        return ('<rect class="ventana" x="22" y="152" width="84" height="66" rx="3"/>'
                '<path class="fondo" d="M64 152 L64 218 M22 185 L106 185"/><circle class="luna" cx="44" cy="168" r="8"/>'
                '<path class="mueble" d="M60 332 L60 264 Q60 248 78 248 L322 248 Q340 248 340 264 L340 332 Z"/>'
                '<path class="fondo" d="M48 300 L352 300 M372 332 L372 196 M356 196 L388 196 L380 170 L364 170 Z"/>')
    if nombre == "biblioteca":   # dos estanterías llenas de libros, a los lados
        return _estanteria(6) + _estanteria(330)
    if nombre == "despacho":   # el de dirección: archivadores, ventana con persiana y archivador de cajones
        lomos = "".join(f'<rect class="lomo-{"abc"[i % 3]}" x="{12 + i * 12}" y="174" width="11" height="40" rx="1"/>'
                        f'<circle class="fondo" cx="{17.5 + i * 12}" cy="204" r="2.4"/>' for i in range(5))
        lamas = "".join(f'M152 {158 + 8 * i} L248 {158 + 8 * i} ' for i in range(7))
        return (f'<path class="fondo" d="M8 214 L76 214"/>{lomos}'
                '<rect class="ventana" x="150" y="150" width="100" height="64" rx="2"/>'
                f'<path class="fondo" d="{lamas}M256 152 L256 196"/><circle class="fondo" cx="256" cy="199" r="2.5"/>'
                '<rect class="mueble" x="336" y="226" width="54" height="106" rx="2"/>'
                '<path class="fondo" d="M336 261 L390 261 M336 296 L390 296 M356 244 L370 244 M356 279 L370 279 M356 314 L370 314"/>'
                '<path class="mueble" d="M352 226 L355 210 L371 210 L374 226 Z"/>'
                '<path class="fondo" d="M363 210 Q356 196 348 194 M363 210 Q366 194 376 190 M363 210 L362 196"/>')
    if nombre == "videollamada":   # la pantalla de una formación en línea: mosaico de caras, una con la cámara apagada
        teselas = []
        for fila in range(2):
            for col in range(3):
                x, y = 145 + col * 39, 152 + fila * 39
                if (fila, col) == (1, 2):
                    teselas.append(f'<rect class="apagada" x="{x}" y="{y}" width="34" height="34" rx="2"/>')
                    continue
                teselas.append(f'<rect class="cuadro" x="{x}" y="{y}" width="34" height="34" rx="2"/>'
                               f'<circle class="fondo" cx="{x + 17}" cy="{y + 14}" r="5"/>'
                               f'<path class="fondo" d="M{x + 7} {y + 32} Q{x + 17} {y + 17} {x + 27} {y + 32}"/>')
                if (fila, col) == (0, 1):   # el micrófono silenciado
                    teselas.append(f'<path class="r" d="M{x + 25} {y + 4} L{x + 31} {y + 10}"/>')
        return ('<rect class="pantalla" x="140" y="146" width="122" height="88" rx="4"/>' + "".join(teselas)
                + '<path class="fondo" d="M190 234 L186 246 M212 234 L216 246"/>')
    return ""


def _estanteria(x0):
    """Una estantería de 64 px de ancho con tres baldas de libros de alturas distintas."""
    anchos = [7, 9, 6, 8, 10, 7, 8]
    altos = [34, 30, 36, 28, 33, 31, 35]
    partes = [f'<rect class="mueble" x="{x0}" y="158" width="64" height="174" rx="2"/>']
    for k, balda in enumerate((200, 244, 288)):
        x = x0 + 5
        for i in range(7):
            j = (i + k * 3) % 7
            if x + anchos[j] > x0 + 59:
                break
            partes.append(f'<rect class="lomo-{"abc"[(i + k) % 3]}" x="{x}" y="{balda - altos[j]}" width="{anchos[j]}" height="{altos[j]}" rx="1"/>')
            x += anchos[j] + 1
        partes.append(f'<path class="fondo" d="M{x0} {balda} L{x0 + 64} {balda}"/>')
    return "".join(partes)


def delante(nombre):
    """Lo que tapa a los personajes: la mesa del claustro."""
    if nombre == "claustro":
        return ('<rect class="mesa" x="10" y="284" width="380" height="48"/>'
                '<path class="fondo" d="M60 280 L96 276 L100 282 M262 282 L300 278"/>')
    return ""


# ---------- Bocadillos ----------

def lineas(texto, ancho_chars):
    return textwrap.wrap(texto, ancho_chars) or [""]


def bocadillo(texto, cx, punta, tipo="habla", y0=12, ancho=172):
    ls = lineas(texto, int((ancho - 10) / 9))   # Newsreader a 17 px: unas 9 unidades por letra, con margen
    alto = 18 + 20 * len(ls)
    x0 = max(8, min(ANCHO - ancho - 8, cx - ancho / 2))
    txt = "".join(f'<tspan x="{x0 + ancho / 2}" dy="{0 if i == 0 else 20}">{e(l)}</tspan>' for i, l in enumerate(ls))
    texto_svg = f'<text class="bocadillo-texto" x="{x0 + ancho / 2}" y="{y0 + 26}" text-anchor="middle">{txt}</text>'
    px, py = punta
    base = min(max(px, x0 + 24), x0 + ancho - 24)
    fondo = y0 + alto
    largo = max(1, ((px - base) ** 2 + (py - fondo) ** 2) ** 0.5)
    tope = 30 if tipo != "piensa" else 60
    if largo > tope:   # la cola apunta a quien habla, pero corta, como en los tebeos
        px, py = base + (px - base) * tope / largo, fondo + (py - fondo) * tope / largo
    if tipo == "piensa":
        forma = f'<rect class="globo" x="{x0}" y="{y0}" width="{ancho}" height="{alto}" rx="{min(alto / 2, 26)}"/>'
        cola = "".join(f'<circle class="globo" cx="{base + (px - base) * f}" cy="{y0 + alto + (py - y0 - alto) * f}" r="{r}"/>'
                       for f, r in ((0.35, 6), (0.7, 3.5)))
        return forma + cola + texto_svg, alto
    forma = f'<rect class="globo" x="{x0}" y="{y0}" width="{ancho}" height="{alto}" rx="14"/>'
    cola = (f'<path class="globo-cola" d="M{base - 9} {y0 + alto - 1} L{px} {py} L{base + 9} {y0 + alto - 1}"/>')
    return forma + cola + texto_svg, alto


# El rótulo va en una sola línea: hasta ROTULO_MAX caracteres cabe con su letra (probado el 09-11-2026 con
# 58). Los encargos piden 55; si uno se pasa, se estrecha hasta el ancho del recuadro en vez de salirse
# por la derecha, y la comprobación lo apunta en el registro.
ROTULO_MAX = 58


def cartela(texto):
    ajuste = f' textLength="{ANCHO - 24}" lengthAdjust="spacingAndGlyphs"' if len(texto) > ROTULO_MAX else ""
    return (f'<rect class="cartela" x="0" y="0" width="{ANCHO}" height="34"/>'
            f'<text class="cartela-texto" x="12" y="23"{ajuste}>{e(texto)}</text>')


# ---------- Viñeta y tira ----------

# Cuando habla primero el de la derecha, los globos van en escalera (06-11-2026): se lee de izquierda
# a derecha antes que de arriba abajo, y un globo solo un poco más alto no basta para marcar el orden.
# El primero, arriba y hacia la derecha; el segundo, entero debajo y a la izquierda, sin que su borde
# llegue a la cola del primero. Los personajes no se mueven.
ESC_ARRIBA, ESC_ABAJO, ESC_HUECO, ESC_MARGEN = 300, 256, 6, 6


def escalera(globos, pos):
    return len(globos) == 2 and pos[globos[0]["quien"]] > pos[globos[1]["quien"]]


def alto_globo(texto, ancho):
    return 18 + 20 * len(lineas(texto, int((ancho - 10) / 9)))


def punta_de(quien, pos):
    return (pos[quien] + (6 if pos[quien] < 200 else -6), CABEZA[quien])


def globos_escalera(globos, pos, y):
    a, b = globos
    arriba, _ = bocadillo(a.get("texto", ""), ANCHO - 8 - ESC_ARRIBA / 2, punta_de(a["quien"], pos), a.get("tipo", "habla"), y, ESC_ARRIBA)
    y2 = y + alto_globo(a.get("texto", ""), ESC_ARRIBA) + ESC_HUECO
    abajo, _ = bocadillo(b.get("texto", ""), 8 + ESC_ABAJO / 2, punta_de(b["quien"], pos), b.get("tipo", "habla"), y2, ESC_ABAJO)
    return [arriba, abajo]


def no_cabe(v):
    """Si una viñeta en escalera no cabe: el globo de abajo taparía la cabeza de quien habla. Devuelve
    el motivo, o None. Entonces los globos van lado a lado: los textos no se acortan."""
    pos = {q: {"izquierda": 108, "centro": 200, "derecha": 292}.get((v.get(q) or {}).get("lugar"), 108 if q == "tiza" else 292)
           for q in ("tiza", "algoritmo") if v.get(q)}
    globos = [b for b in v.get("bocadillos", []) if b.get("quien") in pos][:2]
    if not escalera(globos, pos):
        return None
    y = 44 if v.get("cartela") else 12
    a, b = globos
    fondo = y + alto_globo(a.get("texto", ""), ESC_ARRIBA) + ESC_HUECO + alto_globo(b.get("texto", ""), ESC_ABAJO)
    limite = CABEZA[b["quien"]] - ESC_MARGEN
    if fondo <= limite:
        return None
    return f"habla primero quien está a la derecha, pero uno encima del otro los globos no caben (sobran {fondo - limite:.0f} px)"


def comprobar(guion):
    vs = guion.get("vinetas", [])[:3]
    fallos = [f"Viñeta {i + 1}: {m}" for i, v in enumerate(vs) if (m := no_cabe(v))]
    if vs and not (vs[0].get("cartela") or "").strip():
        fallos.append("Viñeta 1: sin el rótulo que sitúa la escena")
    fallos += [f"Viñeta {i + 1}: el rótulo pasa de {ROTULO_MAX} caracteres y se estrecha para caber"
               for i, v in enumerate(vs) if len(v.get("cartela") or "") > ROTULO_MAX]
    return fallos


def panel(v, n, textos=None):
    """Una viñeta. `v`: {"cartela"?, "tiza": {...}, "algoritmo": {...}, "objeto"?, "bocadillos": [...]}."""
    marco = f'<rect class="marco" x="1.5" y="1.5" width="{ANCHO - 3}" height="{ALTO - 3}" rx="4"/>'
    partes = [f'<path class="t fino" d="M14 {SUELO} L{ANCHO - 14} {SUELO}"/>']
    partes.append(escenario(v.get("escenario")))
    obj = v.get("objeto")
    if obj in DE_FONDO:
        partes.append(objeto(obj, ANCHO / 2, 0))
    pos = {}
    manos = {}
    personajes = {"tiza": tiza, "algoritmo": algoritmo}
    for quien in ("tiza", "algoritmo"):
        p = v.get(quien)
        if not p:
            continue
        x = {"izquierda": 108, "centro": 200, "derecha": 292}.get(p.get("lugar"), 108 if quien == "tiza" else 292)
        mira = p.get("mira") or ("derecha" if x < 200 else "izquierda")
        expr = p.get("expresion") if p.get("expresion") in EXPRESIONES else "neutral"
        post = p.get("postura") if p.get("postura") in POSTURAS else "abajo"
        svg, mano = personajes[quien](x, mira, expr, post)
        partes.append(svg)
        pos[quien] = x
        if post == "sostener":
            manos[quien] = mano
    partes.append(delante(v.get("escenario")))
    if obj and obj not in DE_FONDO and manos:
        quien = v.get("lleva") if v.get("lleva") in manos else next(iter(manos))
        partes.append(objeto(obj, *manos[quien]))
    partes = [marco, f'<g transform="translate(0 {BAJA})">{"".join(partes)}</g>']
    y = 12
    if v.get("cartela"):
        partes.append(cartela(v["cartela"]))
        y = 44
    globos = [b for b in v.get("bocadillos", []) if b.get("quien") in pos][:2]
    # Si la escalera no cabe (lo publicado antes del 06-11-2026, o un ajuste que no bastó), los globos
    # van como antes: mejor un orden dudoso que un globo encima de la cabeza
    if escalera(globos, pos) and not no_cabe(v):
        partes += globos_escalera(globos, pos, y)
        globos_iter = []
    else:
        globos_iter = globos
    for orden, b in enumerate(globos_iter):
        # Se lee de arriba abajo: el segundo bocadillo, un poco más bajo que el primero
        y_globo = y + (30 if orden == 1 else 0)
        quien = b["quien"]
        x = pos[quien]
        if len(globos) == 2:
            x = 100 if x <= pos[[g["quien"] for g in globos if g is not b][0]] else 300
        punta = (pos[quien] + (6 if pos[quien] < 200 else -6), CABEZA[quien])
        # Si habla una sola persona, el globo se ensancha: menos líneas y no baja hasta las cabezas
        ancho = 172 if len(globos) == 2 else 236
        partes.append(bocadillo(b.get("texto", ""), x, punta, b.get("tipo", "habla"), y_globo, ancho)[0])
    # Lo que oye quien usa un lector de pantalla, en el idioma de la edición: `textos` trae cómo se dice
    # «viñeta», el nombre de cada personaje y «pensando» (generar.py); sin él, en castellano
    tx = textos or TEXTOS_ES

    def frase(s):   # con su punto final, sin doblarlo si ya lo trae
        s = (s or "").rstrip()
        return s if s[-1:] in ".!?…" else s + "."

    dichos = []
    for b in globos:
        quien = tx.get(b["quien"], b["quien"])
        if b.get("tipo") == "piensa":
            quien += " (" + tx["pensando"] + ")"
        abre, cierra = tx.get("comillas", "«»")   # en inglés, las suyas (ADR 0059)
        dicho = frase(b.get("texto"))
        # Las comillas de dentro, de segundo nivel: “…” dentro de «…» y ‘…’ dentro de “…”
        dentro = {"«": "“", "»": "”"} if abre == "«" else {"“": "‘", "”": "’"}
        for de, a in dentro.items():
            dicho = dicho.replace(de, a)
        dichos.append(quien + ": " + abre + dicho + cierra)
    desc = " ".join(dichos)
    if v.get("cartela"):
        desc = frase(v["cartela"]) + " " + desc
    return (f'<svg class="panel" viewBox="0 0 {ANCHO} {ALTO}" role="img" aria-label="{e(tx["panel"])} {n}. {e(desc)}" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(partes)}</svg>')


TEXTOS_ES = {"panel": "Viñeta", "tiza": "Tiza", "algoritmo": "Algoritmo", "pensando": "pensando"}


def tira(guion, textos=None):
    return "".join(f'<div class="vineta-panel">{panel(v, i + 1, textos)}</div>' for i, v in enumerate(guion.get("vinetas", [])[:3]))


# ---------- Variedad: lo que salió en los números anteriores ----------

def anteriores(fecha, n=3, carpeta="vinetas"):
    """Los guiones de las n viñetas publicadas antes de `fecha`, del más reciente al más antiguo."""
    import json
    from pathlib import Path
    out = []
    for f in sorted(Path(carpeta).glob("20??-??-??.json"), reverse=True):
        if f.stem >= fecha:
            continue
        try:
            g = ((json.loads(f.read_text()).get("elegida") or {}).get("guion")) or {}
        except (OSError, ValueError):
            continue
        if g.get("vinetas"):
            out.append((f.stem, g["vinetas"][:3]))
        if len(out) == n:
            break
    return out


def usados(fecha):
    """Escenarios de los tres números anteriores (None = sin escenario) y si el anterior fue sin escenario."""
    previos = anteriores(fecha)
    escs = {v.get("escenario") for _, vs in previos for v in vs}
    sin_ayer = bool(previos) and all(not v.get("escenario") for v in previos[0][1])
    return escs, sin_ayer


def recientes(fecha):
    """Resumen para el guionista y el juez (ADR 0024)."""
    from collections import Counter
    previos = anteriores(fecha)
    if not previos:
        return "No hay viñetas anteriores: puedes usar todo el repertorio.\n"
    lineas = [f"# Lo que salió en las viñetas de los {len(previos)} números anteriores a {fecha}", ""]
    caras = {"tiza": Counter(), "algoritmo": Counter()}
    objetos = Counter()
    remates = []   # quién dijo la última frase de cada tira, de la más reciente a la más antigua
    for dia, vs in previos:
        escs = ", ".join(dict.fromkeys(v.get("escenario") or "sin escenario" for v in vs))
        obj = ", ".join(dict.fromkeys(v.get("objeto") for v in vs if v.get("objeto"))) or "ninguno"
        ult = vs[-1] if vs else {}
        globos = ult.get("bocadillos") or []
        quien = globos[-1].get("quien") if globos else None
        remates.append(quien)
        fin = ", ".join(f'{n} {ult[q]["expresion"]}' for q, n in (("tiza", "Tiza"), ("algoritmo", "Algoritmo"))
                        if ult.get(q, {}).get("expresion"))
        remate = {"tiza": "Tiza", "algoritmo": "Algoritmo"}.get(quien, "nadie (remate mudo)")
        lineas.append(f"- {dia}: escenario {escs}; objetos {obj}; última frase de {remate}; acaban: {fin or 'sin cara'}")
        for v in vs:
            for q in caras:
                if v.get(q, {}).get("expresion"):
                    caras[q][v[q]["expresion"]] += 1
            if v.get("objeto"):
                objetos[v["objeto"]] += 1
    escs, sin_ayer = usados(fecha)
    libres = [e for e in ESCENARIOS if e not in escs]
    lineas += ["", "**Escenarios que no puedes usar hoy** (salvo que la noticia ocurra justo allí): "
               + ", ".join(e for e in ESCENARIOS if e in escs),
               "**Escenarios libres:** " + ", ".join(libres)]
    if sin_ayer:
        lineas.append("**El número anterior salió sin escenario: hoy la tira lleva escenario.**")
    for q, nombre in (("tiza", "Tiza"), ("algoritmo", "Algoritmo")):
        mas = ", ".join(f"{e} ({k})" for e, k in caras[q].most_common(3))
        lineas.append(f"Caras más repetidas de {nombre}: {mas}")
    sin_usar = [e for e in EXPRESIONES if not caras["tiza"][e] and not caras["algoritmo"][e]]
    lineas.append("Caras que no han salido: " + (", ".join(sin_usar) or "ninguna"))
    if len(remates) >= 2 and remates[0] and remates[0] == remates[1]:
        nombre, otro = ("Algoritmo", "Tiza") if remates[0] == "algoritmo" else ("Tiza", "Algoritmo")
        lineas.append(f"**{nombre} ha dicho la última frase en los dos números anteriores: hoy remata {otro} o el remate es mudo.**")
    if objetos:
        lineas.append("Objetos que han salido: " + ", ".join(f"{o} ({k})" for o, k in objetos.most_common()))
    return "\n".join(lineas) + "\n"


def repite(fecha, guion):
    """Avisos de variedad de la viñeta elegida, para el registro de noche.sh."""
    escs, sin_ayer = usados(fecha)
    vs = guion.get("vinetas", [])[:3]
    propios = {v.get("escenario") for v in vs if v.get("escenario")}
    avisos = [f"repite el escenario {e} de los tres números anteriores" for e in sorted(propios & escs)]
    if not propios and sin_ayer:
        avisos.append("sale sin escenario dos números seguidos")
    return avisos


if __name__ == "__main__":
    import json
    import sys
    if sys.argv[1] == "--recientes":   # vineta.py --recientes FECHA: el resumen de variedad, en Markdown
        print(recientes(sys.argv[2]), end="")
        sys.exit(0)
    if sys.argv[1] == "--repite":   # vineta.py --repite FECHA vinetas/FECHA.json: sale con 1 si repite
        d = json.load(open(sys.argv[3]))
        avisos = repite(sys.argv[2], ((d.get("elegida") or {}).get("guion")) or {})
        print("; ".join(avisos))
        sys.exit(1 if avisos else 0)
    if sys.argv[1] == "--comprobar":   # vineta.py --comprobar vinetas/FECHA.json: sale con 1 si algo no cabe o falta el rótulo
        d = json.load(open(sys.argv[2]))
        fallos = comprobar(((d.get("elegida") or {}).get("guion") or {}) if "elegida" in d else d)
        print("\n".join(fallos))
        sys.exit(1 if fallos else 0)
    g = json.load(open(sys.argv[1]))
    print(tira(g))
