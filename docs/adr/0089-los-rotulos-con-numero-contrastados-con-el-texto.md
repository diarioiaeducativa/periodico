# 89. Los rótulos con número, contrastados con el texto

Fecha: 2026-11-17 · Estado: aceptado

## Contexto

El dibujo del artículo de la Biblioteca sobre la guía de IA del INTEF (número del 16-11-2026, escrito el 08-11 para
la reserva) apoyaba los tres perfiles de la guía (alumnado, profesorado y centro) en una base rotulada «Cuatro
ámbitos». Los cuatro ámbitos del texto son los de la alfabetización en IA (interactuar, crear, gestionar y modelar):
el dibujo los confundía con los perfiles. Juanjo lo vio: «Pone que hay 4 ámbitos pero solo aparecen 3».

El revisor visual (ADR 0005) ya debía comprobar que «las cifras y los recuentos de los rótulos son los del texto».
Aquel día leyó solo el titular y la entradilla, lo dijo en su respuesta y aun así dio el dibujo por bueno. El 13-11 se
había corregido otro dibujo por lo mismo («Set criteris» con nueve preguntas en la tabla).

## Decisión

- `scripts/recuentos.py` saca de cada SVG los rótulos con un número que puede contar algo (cifras y palabras de
  número; no años, versiones, horas, ordinales ni «3D», «MP3»…). `revisar-dibujos.py` los pone en `es.json` como
  `rotulos_numero`.
- El revisor visual (`encargos/pasos/2b-revision-dibujos.md`) responde por cada uno en `recuentos`: el rótulo, la
  frase del texto de la que sale (copiada), qué cuenta y cuántos objetos del dibujo lo representan (o `null` si no
  cuenta objetos dibujados).
- `recuentos.py comprobar FECHA`, sin IA, mira que estén todos, que la frase esté de verdad en el texto de la pieza
  (así se sabe que ha leído el cuerpo) y que, si da un número de objetos, coincida con el del rótulo. Si falta algo,
  el revisor lo mira otra vez; lo que siga sin contrastar, o no cuadre, vuelve al ilustrador con el motivo
  (`scripts/dibujos.sh`), y si tras rehacerlo sigue mal, el artículo sale sin dibujo, como hasta ahora.

## Alternativas descartadas

- Que el programa compare el número del rótulo con el texto: no sabe qué cuenta un número. En este caso el texto
  sí decía «cuatro ámbitos»; el fallo era lo dibujado junto al rótulo, y eso solo lo juzga quien entiende el dibujo.
- Confiar en el encargo del revisor tal como estaba: ya lo pedía y no lo hizo.

## Consecuencias

- El revisor no puede aprobar un dibujo con rótulos con número sin haber leído el cuerpo de la pieza.
- No es infalible: el revisor puede contar mal. Pero ya no puede saltarse un rótulo ni aprobar sin contrastarlo.
- Algo más de trabajo para el revisor en los dibujos con cifras (unos 30 de 89 en el primer mes).

## Evidencia

Registro del NAS `registro/2099-01-04.log` (08-11-2026): «No he comprobado que […] "cuatro ámbitos" salgan en el
cuerpo de la pieza: solo leí el titular y la entradilla». Corrección del dibujo en los cinco idiomas, con su nota, el
17-11-2026.

## Riesgos y limitaciones

- Si el revisor no llega a responder (límite de uso de la suscripción, fallo), el dibujo no se retira por eso: pasa
  con la comprobación del programa, como antes. Así se vio en el repaso del 17-11, cortado por el límite de uso.
- Un rótulo con un número escrito de una forma que el programa no reconoce no se contrasta (solo castellano).
- La cita se compara sin enlaces, comillas, negritas ni mayúsculas; una cita que cambie una palabra no vale.

## Validación

Ensayo con el dibujo original del INTEF (17-11-2026): sin `recuentos`, el revisor vuelve a mirarlo; con «Cuatro
ámbitos» y tres objetos, el dibujo vuelve al ilustrador; con una frase que no está en el texto, no vale. Revisión de
todos los dibujos publicados y de reserva con rótulos con número el mismo día, con el revisor de siempre.
