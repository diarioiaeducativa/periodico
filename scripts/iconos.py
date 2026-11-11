# SPDX-License-Identifier: AGPL-3.0-or-later
"""Los iconos del diario (ADR 0048): Tiza y Algoritmo cogidos de la mano, el dibujo de la imagen
de vista previa (vineta.py) sobre el papel del diario, con los trazos engrosados para que se lea en pequeño.
La pestaña del navegador sigue con favicon.svg, más sencillo, que se reconoce mejor a 16 px.

    python3 scripts/iconos.py

Escribe en estaticos/ los de la web instalable y el iPhone, y en android/fitxa/icono-512.png el de la ficha
de Google Play, que es también el avatar de la organización en GitHub. Necesita rsvg-convert. La app de
Android toma los suyos de la web publicada al hacer `bubblewrap update` (ADR 0042)."""
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PAPEL, TINTA, AZUL, TIZA = "#fbfbf9", "#16181d", "#1c3faa", "#ffffff"
GROSOR = 2.2          # cuántas veces más gruesos que en la viñeta
CENTRO = (223, 249)   # centro del dibujo, en las coordenadas de la imagen de vista previa


def personajes(k=GROSOR):
    """Los dos personajes, con las mismas formas y posiciones que en la imagen de vista previa."""
    t = f'fill="none" stroke="{TINTA}" stroke-width="{2.5*k:g}" stroke-linecap="round" stroke-linejoin="round"'
    a = f'fill="none" stroke="{AZUL}" stroke-width="{2.5*k:g}" stroke-linecap="round" stroke-linejoin="round"'
    return f'''
<g transform="translate(150 332) scale(1.18) translate(0 -332)">
  <path {t} d="M-9 314 L-11 332 L-19 332 M9 314 L11 332 L19 332"/>
  <path fill="{TIZA}" stroke="{TINTA}" stroke-width="{2.5*k:g}" stroke-linejoin="round" d="M-21 304 L-21 194 Q-21 184 -13 186 L-6 182 L2 187 L9 183 L17 188 Q21 188 21 196 L21 304 Q21 314 11 314 L-11 314 Q-21 314 -21 304 Z"/>
  <g transform="translate(2 216)">
    <circle fill="{TINTA}" cx="-9" cy="0" r="{2.6*min(k, 1.6):g}"/><circle fill="{TINTA}" cx="9" cy="0" r="{2.6*min(k, 1.6):g}"/>
    <path fill="none" stroke="{TINTA}" stroke-width="{2.2*k:g}" stroke-linecap="round" d="M-8 12 Q0 21 8 12"/>
  </g>
  <path {t} d="M-21 252 Q-31 272 -29 290 M21 252 L53 236 M53 236 L61 233"/>
</g>
<g transform="translate(270 332) scale(-1.18 1.18) translate(0 -332)">
  <path fill="none" stroke="{AZUL}" stroke-linecap="round" stroke-dasharray="{4*k:g} {5*k:g}" stroke-width="{2*k:g}" d="M-18 314 L18 314 M-10 323 L10 323"/>
  <rect fill="{AZUL}" x="-28" y="216" width="56" height="86" rx="7"/>
  <g transform="translate(2 244)">
    <circle fill="{PAPEL}" cx="-9" cy="0" r="7.5"/><circle fill="{PAPEL}" cx="9" cy="0" r="7.5"/>
    <circle fill="{TINTA}" cx="-9" cy="0" r="3"/><circle fill="{TINTA}" cx="9" cy="0" r="3"/>
    <path fill="none" stroke="{PAPEL}" stroke-width="{2.2*k:g}" stroke-linecap="round" d="M-8 13 Q0 22 8 13"/>
  </g>
  <path {a} d="M-28 264 L-44 234 M28 264 L44 234"/>
</g>'''


def icono(escala, esquinas=0):
    """Un cuadrado de 512 con el papel de fondo y el dibujo centrado a la escala dada."""
    cx, cy = CENTRO
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" rx="{esquinas}" fill="{PAPEL}"/>'
            f'<g transform="translate(256 256) scale({escala}) translate({-cx} {-cy})">{personajes()}</g></svg>')


# Cada archivo: el tamaño y el icono. El de la web instalable lleva las esquinas redondeadas, como el
# anterior; el adaptable, el dibujo dentro de la zona segura (un círculo del 80 %), porque el sistema lo
# recorta; el del iPhone, el de Play y el de GitHub, cuadrados, porque los redondea cada uno a su manera.
NORMAL, ADAPTABLE, CUADRADO = icono(2.05, esquinas=96), icono(1.53), icono(2.05)
SALIDAS = {
    "estaticos/icono-512.png": (512, NORMAL),
    "estaticos/icono-192.png": (192, NORMAL),
    "estaticos/icono-maskable-512.png": (512, ADAPTABLE),
    "estaticos/apple-touch-icon.png": (180, CUADRADO),
    "android/fitxa/icono-512.png": (512, CUADRADO),
}

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        for ruta, (lado, svg) in SALIDAS.items():
            fuente = Path(tmp) / "icono.svg"
            fuente.write_text(svg)
            subprocess.run(["rsvg-convert", "-w", str(lado), "-h", str(lado), str(fuente), "-o", str(RAIZ / ruta)], check=True)
            print(ruta, (RAIZ / ruta).stat().st_size, "bytes")
