# 4. El reportaje del domingo

Fecha: 2026-11-03 · Estado: aceptado

## Contexto

Las piezas diarias cuentan lo que se habló ayer en los grupos, en 80-300 palabras. Algunos
temas atraviesan la semana y dan para mucho más: actores con documentos propios, normativa,
práctica de aula. Juanjo pidió añadir los domingos algo de más fondo. Un resumen de la
semana quedaba descartado de entrada: el boletín semanal de los grupos ya lo publica cada
lunes, con la semana de lunes a domingo.

## Decisión

- **Un solo tema de la semana, a fondo**, con el número del domingo (las conversaciones del
  sábado). La semana son los siete días que acaban en ese sábado. Entre 1.200 y 1.800
  palabras, en apartados con ladillo, un recuadro de claves y la lista de piezas del diario
  relacionadas. Criterios y forma, en `encargos/reportaje.md`.
- **Tabla de consulta** (07-11-2026): un apartado puede llevar `"tabla": {"titulo", "columnas",
  "filas", "nota"}`, que `generar.py` pinta tras sus párrafos como tabla y, en el móvil, como una
  ficha por fila; su texto entra en el buscador. Nació con el reportaje sobre la edad para usar IA
  en clase, para que cada docente encuentre su comunidad (Juanjo: «una tabla o similar por
  comunidades que el profesor pueda tomar como referencia, especialmente si su comunidad no dice
  nada»). Los agentes no la escriben todavía: se añade a mano cuando el tema lo pide.
- **Cinco agentes más, en serie** (`scripts/reportaje.sh`): el jefe de reportajes (Opus 5.5)
  elige tema y enfoque; el reportero (Opus 5.5) investiga fuera de los grupos y escribe; el
  verificador (Sonnet 5.5), que no ha escrito nada, abre cada fuente y quita lo que no puede
  confirmar; el ilustrador y el traductor (Sonnet 5.5) hacen la infografía y la versión
  catalana. Los mismos límites que los demás (ADR 0002): sin terminal y sin leer fuera de la
  redacción.
- **Nunca impide el número.** `noche.sh` lo lanza los sábados entre la viñeta y los avisos,
  para que los avisos del domingo lo anuncien. Si algún paso falla o el verificador no lo da
  por bueno, el domingo sale sin reportaje y se avisa a Juanjo por Telegram.
- **En el sitio**: el domingo abre la portada en una franja como la editorial, con filete azul;
  los días siguientes sigue en la portada, tras las destacadas y la viñeta, hasta que pasan siete
  días. Al principio iba antes de la viñeta; el 04-11-2026 Juanjo preguntó si estaba bien que la
  viñeta del día quedara bajo un reportaje de tres días antes, y se aceptó la propuesta de ponerla
  delante: lo de hoy va antes que lo de la semana.
  Tiene su página (`<fecha>/<id>.html`), una sección «Reportajes» en la barra, su marca en la
  hemeroteca y su entrada en el RSS y el mapa del sitio. Archivos en `reportajes/` y
  `reportajes-ca/`; la semana preparada, en `semanas/` (no se sube, como `dias/`).
- **«La redacción»** explica el reportaje y los tres agentes nuevos, con un organigrama propio
  (`ilustraciones/redaccion-organigrama.svg`) que añade la fila de los domingos. El del
  número 1 se queda como se publicó.

## Consecuencias

- La noche del sábado dura unos 15-25 minutos más, sin coste nuevo.
- Un reportaje largo con fuentes externas tiene más riesgo de error que una pieza: la única
  defensa es el verificador. Si un domingo sale algo mal, se corrige el JSON y se regenera.
- Validación: el primero se hizo el 03-11-2026 para el domingo 1 de noviembre (semana del 25
  al 31 de octubre), con el mismo guion y una configuración de Claude limpia, como en el NAS.
