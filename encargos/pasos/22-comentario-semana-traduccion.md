Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) los comentarios de la semana {FECHA}, con el mismo criterio que las ediciones (mira el último de ediciones{SUF}/ como modelo, si hay alguno):

comentario-semana/{FECHA}.json → comentario-semana{SUF}/{FECHA}.json: misma estructura, mismos `semana`, `hay_comentario`, claves de `grupos` y `piezas`. En `general` y en cada grupo, traduce `titulo` y cada uno de los `parrafos`, en el mismo número y orden; conserva los enlaces Markdown con su clave `pieza:` tal cual (solo se traduce el texto del enlace) y las negritas y cursivas. Los nombres propios no se traducen: «Vibe Coding Educativo», «ChatGPT-IA-edu» y «EduMedia-IAG» se quedan así ({REPOSITORIO}). Campos internos (repaso, motivo), en castellano.

Comprueba que el JSON es válido. No toques nada más. Responde con lo traducido en una línea.
