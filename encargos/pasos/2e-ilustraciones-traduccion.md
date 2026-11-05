Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al catalán (estándar del IEC, natural) los dibujos nuevos del {FECHA} de estas piezas: {IDS}, como en los días anteriores (mira ilustraciones-ca/ como modelo):

1. ilustraciones/{FECHA}-<id>.svg → ilustraciones-ca/{FECHA}-<id>.svg, con los <text> en catalán y de largo parecido; lo demás, igual.
2. En ediciones-ca/{FECHA}.json, añade a esas piezas su `ilustracion_alt` en catalán, traducido del de ediciones/{FECHA}.json. No cambies nada más del JSON.

Comprueba que el JSON y los SVG son válidos. No toques nada más. Responde con una línea por archivo.
