# 102. Las fechas, con el día de la semana

Fecha: 2026-11-23 · Estado: aceptado

## Contexto

La cabecera, el pie, la hemeroteca y los índices daban la fecha larga, con el día de la semana («Lunes, 23 de
noviembre de 2026»), pero el resto del diario no: el rótulo de cada artículo, las listas, los breves, la columna,
«Hace un año», los vídeos, el buscador, los comentarios y la cifra de los grupos decían «23 de noviembre». Juanjo
pidió el 23-11-2026 que siempre apareciera el día de la semana, y preguntó cómo resolverlo en el móvil, donde podía
no caber.

## Decisión

- **Todas las fechas, con su día**: `fecha_corta()` y `fecha_con_anyo()` lo ponen por defecto con `con_dia()`
  («lunes, 23 de noviembre»; en euskera, detrás, como en la fecha larga: «azaroaren 23a, astelehena»). Las fechas
  de los comentarios, que monta el navegador, usan el mismo patrón con el día (`{s}`).
- **Una excepción**: el rótulo del reportaje, que ya dice «El reportaje del domingo»; con el día quedaba
  «domingo, domingo, 22 de noviembre» (`dia=False`).
- **La cifra de los grupos** (la imagen que pueden insertar otras webs) lleva el día abreviado, con las abreviaturas
  normativas de cada lengua (RAE, IEC, RAG y Gobierno Vasco): «(dom. 22 nov. 2026)», «(dg. 22 nov. 2026)»…; y su
  texto alternativo, el día entero («a domingo, 22 de noviembre de 2026»; en euskera, en inesivo: «2026ko azaroaren
  22an, igandean»).
- **En el móvil no hace falta otro formato**: medido en 360 y 390 píxeles, en las cinco lenguas y once tipos de
  página, la fecha con el día cabe en los rótulos y en las listas va en su propia línea. Donde no cabe al lado del
  nombre de la sección, baja entera a la línea de abajo: el nombre de la sección ya no se parte nunca (en «Hace un
  año», con la fecha y el año, salía «Hace / un año»).

## Alternativas descartadas

- **El día abreviado en el móvil** («lun., 23 de nov.»): la medida no lo pide, y dos formatos según la pantalla
  complican el código y las pruebas.

## Validación

Generado en una copia aparte y medido con Playwright (fecha partida o rótulo partido, en 360 y 390 píxeles); probado
con `probar-web` en Chromium, Firefox y WebKit, y las fechas de los comentarios, con uno real, en cuatro lenguas.
