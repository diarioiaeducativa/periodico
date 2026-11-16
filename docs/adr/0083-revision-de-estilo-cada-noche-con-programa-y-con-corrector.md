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
   cifras (solo se pueden añadir las de una fecha, al cambiar «ayer» por el día) y los mismos campos que no son
   texto; si no, vuelve la versión del revisor. Cada cambio queda en `ediciones-borrador/FECHA-corrector.json`, con
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
