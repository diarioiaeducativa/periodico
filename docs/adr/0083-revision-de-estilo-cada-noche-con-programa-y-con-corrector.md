# 83. Revisión de estilo cada noche, con programa y con corrector

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

Con el libro de estilo (ADR 0078) quedó claro que muchas de sus normas no las vigilaba nadie en particular. El
revisor de cada artículo se ocupa sobre todo de los datos, y el único programa de estilo (ADR 0067) buscaba solo el
«quien» relativo y las citas sin traducir del inglés. Se vio además que los textos tenían expresiones comprimidas
que cuestan de entender, cuando el diario es para un público amplio, no para expertos.

## Decisión

1. **`scripts/revisar-estilo.py` busca más normas**, solo en castellano y fuera de citas y direcciones: «hoy»,
   «ayer» o «esta semana» (no en «Hace un año», que compara con el presente, ni en los avisos, que salen ese día);
   «pieza»; «el diario cuenta» o «contó»; «app», «online» y «link» en minúscula; «la AI»; el condicional de rumor y
   el porcentaje sin espacio. Lo que encuentra lo corrige, como antes, el agente de `encargos/pasos/29-estilo.md`,
   que deja lo que tiene otro sentido o es un nombre propio. Lo ya publicado no se toca: son normas nuevas.
2. **Un corrector de estilo con IA** (`encargos/pasos/36-corrector-estilo.md`, Opus), cada noche, después del
   revisor y antes de traducir, sobre los artículos y breves del día: los lee como un lector cualquiera y corrige lo
   que cuesta entender, la IA presentada como si pensara, el lenguaje de las empresas, el lenguaje inclusivo, el tono
   y las normas de lengua. Solo
   cambia la redacción; puede explicar en pocas palabras qué es algo si lo dice la fuente o lo ha comprobado.
   `scripts/comprobar-corrector.py` comprueba después que siguen los mismos enlaces, las mismas citas, todas las
   cifras (solo se pueden añadir las de una fecha, al cambiar «ayer» por el día, y las que ya estaban en otro texto
   del mismo artículo) y los mismos campos que no son texto. Desde el 20-11-2026, el descarte va por textos: el
   texto (titular, entradilla, cuerpo o breve) donde ha cambiado un dato vuelve a la redacción del revisor, el resto
   de cambios se queda y en el registro de cambios se marcan los descartados; solo si ha roto la edición o tocado lo
   que no es texto vuelve entera la del revisor, y solo eso es un aviso. El informe del día dice cuántos cambios se
   aplicaron y cuántos se descartaron, fuera de «Fallos y avisos». Cada cambio queda en `ediciones-borrador/FECHA-corrector.json`, con
   el antes, el después y el porqué. Solo corrige la edición del día: la Biblioteca, el Repositorio, «Hace un año» y
   el reportaje se traducen antes, en sus propios procesos.

## Consecuencias

- Los artículos del día salen escritos para un público amplio, y las traducciones parten del texto ya corregido.
- Unos minutos más cada noche, con la misma suscripción.
- El corrector está encendido desde el 16-11-2026, tras ver su primera prueba; `CORRECTOR=0` lo salta.

## Validación

- `revisar-estilo.py --todo` sobre todo lo publicado: 15 «el diario contó», 6 «pieza», 5 «hoy» o «ayer» y 4 «app»,
  además de los «quien» anteriores al 15-11-2026; ninguno se corrige hacia atrás.
- `comprobar-corrector.py` con cambios de prueba: deja pasar la redacción y una fecha añadida, y para una cifra
  nueva, un enlace cambiado, una cita tocada y una fuente cambiada.
- El corrector, en una copia, sobre los artículos del 15-11-2026: 15 cambios de redacción (siglas y términos
  explicados, frases comprimidas deshechas, «agentes de código» por «la IA que programa», fuera «potentes» y «el
  diario contó») y el comprobador confirmó que no cambió ningún dato.
- Descarte por textos (20-11-2026): en sus primeras cuatro noches, el corrector perdió todo su trabajo en tres por un
  solo cambio que tocaba una cifra; el 19-11 eran 17 cambios, y la cifra era «Genie 4», el nombre del producto, que ya
  estaba en el titular. Con la edición del 19-11 y cambios de prueba, `--arreglar` deja «Genie 4» y la redacción, y
  devuelve solo la entradilla con una cifra nueva y el breve con un enlace nuevo; vuelta a comprobar, sale limpia. Un
  campo que no es texto cambiado y un JSON roto siguen devolviendo la edición entera.
- Cargo en el diario (24-11-2026): un artículo sobre la guía de privacidad de un autor del diario lo presentaba como
  «coautor de este diario», aunque la guía no tiene nada que ver con el diario y el libro de estilo ya decía que los
  cargos solo van si tienen que ver con la noticia. Juanjo: «cuando se hablaba de temas normales no se nombraba el
  cargo»; y, donde sí vaya, «responsable», no «coautor». `revisar-estilo.py` busca ahora «autor», «responsable»,
  «creador», «fundador», «director» o «editor» «de este diario» o «del diario», salvo el aviso de participación que
  pide el reportaje («participaron los autores de este diario»), y el corrector lo quita si el artículo no trata del
  propio diario. Con `--todo`, tras corregir ese artículo, no queda ningún caso; la expresión, probada con siete
  frases (también «el editor del Diario de Navarra», que no salta).
