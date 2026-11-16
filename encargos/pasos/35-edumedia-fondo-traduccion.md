Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) el artículo de reserva del fondo de EduMedia-IAG con clave {FECHA}, con el mismo criterio que las ediciones (mira el último de ediciones{SUF}/ como modelo):

1. ediciones/{FECHA}.json → ediciones{SUF}/{FECHA}.json: misma estructura, mismos `id`, `seccion`, `importancia`, `grupo`, `mensaje`, `herramienta` y `fondo`; traduce antetitulo (el equivalente natural de «Del fondo de EduMedia»), titular, entradilla, cuerpo (conserva los enlaces Markdown y las negritas), ilustracion_alt y los títulos de fuentes (con {MARCAS} si la fuente no está en {LENGUA}). Los nombres de las herramientas no se traducen. Campos internos (comprobado, repaso, motivo, descartado, ilustracion), en castellano.
2. ilustraciones/{FECHA}-<id>.svg de esa pieza → ilustraciones{SUF}/ con los <text> en {LENGUA}, de largo parecido.

Comprueba que el JSON y el SVG son válidos. No toques nada más. Responde con lo traducido en una línea por archivo.

Sigue el libro del traductor, `encargos/traduccion.md` (el apartado general y el de tu lengua), y el libro de estilo, `encargos/estilo.md`.
