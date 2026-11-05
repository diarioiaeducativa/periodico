Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al catalán (estándar del IEC, natural, periodístico; «el professorat», «l'alumnat») lo del día {FECHA}, igual que en los días anteriores (mira el último de ediciones-ca/, vinetas-ca/ e ilustraciones-ca/ como modelo):

1. ediciones/{FECHA}.json → ediciones-ca/{FECHA}.json: misma estructura e `id`, `seccion`, `importancia`, `grupo`, `mensaje`, `url`; traduce antetitulo, titular, entradilla, cuerpo (conserva los enlaces Markdown), texto de los breves, ilustracion_alt y títulos de fuentes (con «(en castellà)» o «(en anglès)» si la fuente no es en catalán). Si una fuente tiene versión oficial en catalán, compruébala con WebFetch y úsala; no inventes URL. Nombres propios de aplicaciones y obras, sin traducir. Los personajes de la viñeta se llaman en catalán Guix i Algorisme.
2. ilustraciones/{FECHA}-*.svg → ilustraciones-ca/ con los <text> en catalán, de largo parecido.
3. Si existe vinetas/{FECHA}.json con "elegida" no nula → vinetas-ca/{FECHA}.json: copia la "elegida" con el texto de bocadillos y cartelas en catalán (que conserve la gracia; bocadillos de 90 caracteres como mucho) y añade "traduccion": "automàtica amb IA".

Comprueba que los JSON y SVG son válidos. No toques nada más. Responde con lo traducido en una línea por archivo.
