Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) la columna de opinión del {FECHA}, con el mismo criterio que las ediciones (mira el último de ediciones{SUF}/ como modelo, si hay alguno):

columnas/{FECHA}.json → columnas{SUF}/{FECHA}.json: misma estructura, mismos `id`, `seccion`, `importancia` y `autor` (el nombre del modelo que la firma no se traduce). Traduce antetitulo, titular, entradilla, cuerpo (conserva los enlaces Markdown, también los `pieza:`, y las negritas) y los títulos de fuentes (con {MARCAS} si la fuente no está en {LENGUA}). Es opinión: conserva el tono, la tesis y la fuerza de cada argumento, sin suavizarlos ni reforzarlos. Los nombres propios no se traducen: «Vibe Coding Educativo», «ChatGPT-IA-edu» y «EduMedia-IAG» se quedan así. Campos internos (comprobado, repaso, motivo), en castellano.

Comprueba que el JSON es válido. No toques nada más. Responde con lo traducido en una línea.

Sigue el libro del traductor, `encargos/traduccion.md` (el apartado general y el de tu lengua), y el libro de estilo, `encargos/estilo.md`.
