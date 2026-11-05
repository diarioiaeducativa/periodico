Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al catalán (estándar del IEC, natural, periodístico; «el professorat», «l'alumnat») el reportaje del {FECHA}, con el mismo criterio que las ediciones (mira el último de ediciones-ca/ como modelo):

1. reportajes/{FECHA}.json → reportajes-ca/{FECHA}.json: misma estructura, mismo `id`, `mensaje` y `relacionadas`; traduce antetitulo, titular, entradilla, ladillos, párrafos (conserva los enlaces Markdown y las negritas), claves, ilustracion_alt y títulos de fuentes (con «(en castellà)» o «(en anglès)» si la fuente no es en catalán). Si una fuente tiene versión oficial en catalán, compruébala con WebFetch y úsala; no inventes URL. Nombres propios de aplicaciones, documentos y obras, sin traducir. Los campos internos (comprobado, repaso, motivo, ilustracion) pueden quedar en castellano.
2. ilustraciones/{FECHA}-<id>.svg del reportaje → ilustraciones-ca/ con los <text> en catalán, de largo parecido.

Comprueba que el JSON y el SVG son válidos. No toques nada más. Responde con lo traducido en una línea por archivo.
