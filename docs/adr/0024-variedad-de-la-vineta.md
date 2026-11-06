# 24. Variedad de la viñeta: memoria de los números anteriores y tres escenarios nuevos

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

El 06-11-2026 Juanjo preguntó cuántas piezas tiene el repertorio de Tiza y Algoritmo y si
convenía añadir escenarios. Se contó lo publicado en las 27 viñetas de los 9 primeros números
(del 28-10 al 05-11-2026):

- Escenarios: sala de profesores en 14 viñetas (cuatro números seguidos, del 01-11 al 04-11),
  casa de noche en 6, aula en 4; fotocopiadora y claustro, nunca; el 05-11, sin escenario.
- Caras: «contento» en 19 de 53 apariciones; enfadado, preocupado y cargando, nunca.
- Objetos: el portátil en 9 viñetas.

El repertorio no era el límite: el guionista no veía lo de días anteriores y tiraba siempre de
lo mismo. El 05-11 sin escenario no fue un fallo: el juez lo dejó así a propósito («el portátil
en el centro basta»), porque el escenario era opcional.

## Decisión

- **Memoria de los números anteriores.** Antes del guionista, `noche.sh` escribe
  `vinetas/recientes/FECHA.md` con `vineta.py --recientes`: escenarios y objetos de los tres
  números anteriores, escenarios prohibidos y libres, caras más repetidas de cada personaje y
  las que no han salido. Lo leen el guionista (paso 3) y el juez (paso 4). Se rehace cada noche
  y no se guarda en el repositorio.
- **Regla de variedad** (`encargos/vineta.md`, «La variedad»): no repetir escenario de los tres
  números anteriores salvo que la noticia ocurra allí; sin escenario solo si el objeto ya sitúa
  la escena y nunca dos números seguidos; caras variadas; no repetir el objeto del día anterior.
  Entre los cinco guiones, al menos tres escenarios distintos. El juez corrige la elegida si no
  cumple, pero la variedad nunca decide entre dos chistes: manda la gracia.
- **Comprobación sin IA:** tras el juez, `vineta.py --repite` anota en el registro si la elegida
  repite escenario o sale sin él dos números seguidos. Solo se anota; no se rehace nada.
- **Tres escenarios nuevos** (`vineta.py`), ligados a los temas del diario: `biblioteca`
  (estanterías a los lados, deja el centro libre para los objetos), `despacho` (dirección:
  archivadores, persiana y archivador de cajones; para normativa y burocracia) y `videollamada`
  (pantalla con mosaico de caras, una con la cámara apagada y otra silenciada; para formaciones y
  reuniones en línea). Colores de las secciones ya existentes, en `estaticos/comun.css`, con
  tema claro y oscuro.

## Alternativas descartadas

- Solo añadir escenarios: con el guionista sin memoria, seguiría saliendo la sala de profesores.
- Hacer obligatorio el escenario siempre: a veces la escena vacía con el objeto en el centro
  funciona; basta con que no se repita dos días.
- Que el programa rechace la viñeta que repite: rompería la regla de que siempre hay viñeta
  (ADR 0023) por una cuestión menor.

## Validación

`--recientes` y `--repite` probados con las viñetas publicadas: el 04-11 da «repite el escenario
sala_profes»; el 05-11, nada. Los tres escenarios nuevos, dibujados sobre las tiras del 04-11 y
del 05-11 en una copia, en tema claro, oscuro y anchura de móvil.

## Riesgos

- Que el guionista fuerce un escenario que no pega para cumplir. El encargo pone la gracia por
  delante; vigilarlo en los números siguientes.
