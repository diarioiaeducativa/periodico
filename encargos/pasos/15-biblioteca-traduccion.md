Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al catalán (estándar del IEC, natural, periodístico; «el professorat», «l'alumnat») los artículos de la Biblioteca digital del {FECHA}, con el mismo criterio que las ediciones (mira el último de ediciones-ca/ como modelo):

1. biblioteca/{FECHA}.json → biblioteca-ca/{FECHA}.json: misma estructura, mismos `id`, `seccion`, `importancia`, `grupo`, `mensaje` y `documento.url`; traduce antetitulo, titular, entradilla, cuerpo (conserva los enlaces Markdown y las negritas), ilustracion_alt, `documento.idioma`, `documento.licencia` si es texto, y los títulos de fuentes (con «(en castellà)» o «(en anglès)» si la fuente no es en catalán). `documento.titulo` queda en su idioma original. Las citas entre comillas de un documento en catalán se dejan tal cual; las de otro idioma, traducidas como en el castellano. Campos internos (comprobado, repaso, ilustracion), en castellano.
2. ilustraciones/{FECHA}-<id>.svg de esas piezas → ilustraciones-ca/ con los <text> en catalán, de largo parecido.

Comprueba que el JSON y los SVG son válidos. No toques nada más. Responde con lo traducido en una línea por archivo.
