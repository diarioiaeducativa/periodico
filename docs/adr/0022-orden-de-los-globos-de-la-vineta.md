# 22. El orden de los globos de la viñeta: escalera y escena más baja

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

En una viñeta con dos bocadillos, el orden se marcaba solo con la altura: el segundo globo
bajaba 30 px. Pero en un cómic se lee de izquierda a derecha antes que de arriba abajo, y cuando
hablaba primero el de la derecha (Algoritmo), la tira se leía al revés. Pasaba en 8 de los 9
números publicados hasta entonces. Juanjo lo señaló el 06-11-2026 con la viñeta de ese día
(«muchas veces se lee al revés»).

## Decisión

- **Los personajes no cambian de lado**: Tiza a la izquierda y Algoritmo a la derecha, en toda la
  tira. Moverlos según quién habla primero resultaría antinatural en un escenario (Juanjo: «no
  resulta antinatural en un escenario?»).
- **Escalera** (`vineta.py`, `globos_escalera`): si habla primero el de la derecha, su globo va
  arriba y hacia la derecha (320 px de ancho; 300 hasta el 15-11-2026) y el otro, entero debajo y a la izquierda (256 px,
  sin llegar a la cola del primero). Si habla primero el de la izquierda, como antes.
- **La escena baja 18 px** (`BAJA`): el suelo, el decorado y los personajes bajan dentro del
  marco, y debajo del suelo quedan 8 px. Así caben los globos en escalera sin acortar los textos.
  Juanjo lo prefirió a acortarlos: «ya son breves de por sí y acortarlos puede ser negativo».
- **Si aun así no caben** (dos textos largos, o con cartela), los globos van lado a lado, como
  antes: mejor un orden dudoso que un globo encima de una cabeza. `noche.sh` lo anota en el
  registro (`vineta.py --comprobar`); los textos no se tocan.
- Lo ya publicado se vuelve a dibujar con la regla nueva, porque la tira sale del guion cada vez
  que se monta la web.

## Alternativas descartadas

- Que el primero en hablar se ponga a la izquierda: los personajes saltarían de lado.
- Que el editor de humor acorte los textos que no caben: se probó y se retiró el mismo día, a
  petición de Juanjo.
- Numerar los globos: poco profesional.

## Validación

Las 18 viñetas publicadas en que habla primero el de la derecha (castellano y catalán, del 28-10
al 05-11-2026) caben en escalera con la escena bajada; sin bajarla, no cabían tres. Revisadas en
captura las nueve tiras, con todos los escenarios, y la de ese día en anchura de móvil. Caso
límite medido: sin cartela caben un texto de 90 caracteres arriba y uno de 50 abajo; con
cartela, unos 60 y 27.

Ensanche del 15-11-2026: en la viñeta del 14-11, «Te modelo en 3D cualquier máquina de la Revolución
Industrial.» (62 caracteres) ocupaba tres líneas con 300 px y la escalera no cabía por 13 px (en
castellano, catalán e inglés), así que salió lado a lado y se leía antes la respuesta de Tiza. Juanjo
lo señaló («el bocadillo de algoritmo no debería estar encima de el de tiza?»). Con 320 px cabe en dos
líneas. Medido en las 80 viñetas en escalera publicadas hasta ese día: cabe la del 14-11 en los tres
idiomas, cinco anteriores solo pierden una línea en el globo de arriba y la del 12-11 sigue sin caber.
