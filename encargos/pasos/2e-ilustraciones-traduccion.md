Trabajas en la carpeta actual, la de la redacción del «Diario de IA Educativa». Traduce al {LENGUA} ({NORMA}) los dibujos nuevos del {FECHA} de estas piezas: {IDS}, como en los días anteriores (mira ilustraciones{SUF}/ como modelo):

1. ilustraciones/{FECHA}-<id>.svg → ilustraciones{SUF}/{FECHA}-<id>.svg, con los <text> en {LENGUA} y de largo parecido; lo demás, igual.
2. En ediciones{SUF}/{FECHA}.json, añade a esas piezas su `ilustracion_alt` en {LENGUA}, traducido del de ediciones/{FECHA}.json. No cambies nada más del JSON.

Comprueba que el JSON y los SVG son válidos. No toques nada más. Responde con una línea por archivo.
