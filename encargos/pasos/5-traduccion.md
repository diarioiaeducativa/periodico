Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) lo del día {FECHA}, igual que en los días anteriores (mira el último de ediciones{SUF}/, vinetas{SUF}/ e ilustraciones{SUF}/ como modelo, si hay alguno):

1. ediciones/{FECHA}.json → ediciones{SUF}/{FECHA}.json: misma estructura e `id`, `seccion`, `importancia`, `grupo`, `mensaje`, `url`; traduce antetitulo, titular, entradilla, cuerpo (conserva los enlaces Markdown), texto de los breves, ilustracion_alt y títulos de fuentes (con {MARCAS} si la fuente no está en {LENGUA}). Si una fuente tiene versión oficial en {LENGUA}, compruébala con WebFetch y úsala; no inventes URL. Nombres propios de aplicaciones y obras, sin traducir. Los personajes de la viñeta se llaman en {LENGUA} {PERSONAJES}.
2. ilustraciones/{FECHA}-*.svg → ilustraciones{SUF}/ con los <text> en {LENGUA}, de largo parecido.
3. Si existe vinetas/{FECHA}.json con "elegida" no nula → vinetas{SUF}/{FECHA}.json: copia la "elegida" con el texto de bocadillos y cartelas en {LENGUA} (que conserve la gracia; bocadillos de 90 caracteres como mucho) y añade "traduccion": "{NOTA}".

Comprueba que los JSON y SVG son válidos. No toques nada más. Responde con lo traducido en una línea por archivo.
