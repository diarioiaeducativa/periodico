Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) el reportaje del {FECHA}, con el mismo criterio que las ediciones (mira el último de ediciones{SUF}/ como modelo, si hay alguno):

1. reportajes/{FECHA}.json → reportajes{SUF}/{FECHA}.json: misma estructura, mismo `id`, `mensaje` y `relacionadas`; traduce antetitulo, titular, entradilla, ladillos, párrafos (conserva los enlaces Markdown y las negritas), claves, ilustracion_alt y títulos de fuentes (con {MARCAS} si la fuente no está en {LENGUA}). Si una fuente tiene versión oficial en {LENGUA}, compruébala con WebFetch y úsala; no inventes URL. Nombres propios de aplicaciones, documentos y obras, sin traducir. Los campos internos (comprobado, repaso, motivo, ilustracion) pueden quedar en castellano.
2. ilustraciones/{FECHA}-<id>.svg del reportaje → ilustraciones{SUF}/ con los <text> en {LENGUA}, de largo parecido.

Comprueba que el JSON y el SVG son válidos. No toques nada más. Responde con lo traducido en una línea por archivo.
