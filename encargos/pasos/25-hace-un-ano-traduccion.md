Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) la pieza «Hace un año» del {FECHA}, con el mismo criterio que las ediciones (mira el último de ediciones{SUF}/ como modelo, si hay alguno):

1. hace-un-ano/{FECHA}.json → hace-un-ano{SUF}/{FECHA}.json: misma estructura, mismos `id`, `seccion`, `importancia`, `grupo`, `fecha_original` y `mensaje`. Traduce antetitulo, titular, entradilla, cuerpo (conserva los enlaces Markdown y las negritas), ilustracion_alt y los títulos de fuentes (con {MARCAS} si la fuente no está en {LENGUA}). Los nombres propios no se traducen: «Vibe Coding Educativo», «ChatGPT-IA-edu» y «EduMedia-IAG» se quedan así. Campos internos (comprobado, repaso, motivo), en castellano.
2. Si existe ilustraciones/{FECHA}-<id>.svg de esa pieza → ilustraciones{SUF}/ con los <text> en {LENGUA}, de largo parecido (el mes abreviado del rótulo de la izquierda, como se abrevia en {LENGUA}).

Comprueba que el JSON y el SVG son válidos. No toques nada más. Responde con lo traducido en una línea.
