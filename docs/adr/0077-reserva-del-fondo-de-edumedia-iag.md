# 77. Reserva del fondo de EduMedia-IAG

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

Juanjo pidió el 16-11-2026 que cada número lleve como mínimo un artículo de cada grupo. La
redacción ya lo procura (`encargos/redaccion.md`, «Al menos una pieza de cada grupo, si es
posible», y el revisor lo comprueba), y desde el ADR 0076 la reserva completa primero los grupos
que faltan. Pero la reserva solo tenía piezas de dos fuentes: el fondo del Repositorio de VCE
(Vibe Coding Educativo) y el de la Biblioteca digital (ChatGPT-IA-edu). EduMedia-IAG no tenía
ninguna.

En los 14 primeros números de noviembre, 4 salieron sin artículo de EduMedia (los días 1, 3, 7 y
14), casi siempre porque el grupo no escribió nada publicable ese día. El grupo no tiene una fuente
propia de recursos: su web (`edumedia-iag.github.io`) solo publica el boletín semanal. Sí tiene un
historial largo: 10.750 mensajes desde julio de 2025, con unos 1.260 enlaces, sobre todo vídeos,
tutoriales y herramientas de imagen, audio y vídeo.

## Decisión

Una tercera fuente de reserva, «Del fondo de EduMedia», escrita como las otras dos:

- **Candidatos** (`scripts/edumedia_fondo.py`, sin IA): mensajes del grupo de hace más de 21 días
  con un enlace que no sea a una red social, al propio diario ni al boletín, que no esté ya en algo
  publicado y que no se haya usado ni descartado antes para la reserva. Los más comentados primero
  y, de ellos, 25 al azar, para que cada vez salgan otros.
- **Cuatro agentes** (`scripts/edumedia-fondo.sh`, encargos 32 a 35 y la guía
  `encargos/edumedia-fondo.md`): el documentalista elige uno que sirva en clase, sea gratuito o
  tenga versión gratuita, siga existiendo con las mismas condiciones y no haya salido en el diario,
  y lo comprueba en su web oficial; el revisor, que no lo ha escrito, lo vuelve a comprobar todo;
  el ilustrador hace un dibujo de lo que se consigue con él (no una captura: estas herramientas
  suelen pedir una cuenta), que pasa la revisión de dibujos; y los traductores, uno por idioma.
- **Forma**: una pieza de edición (sección Multimedia, grupo `edumedia`, antetítulo «Del fondo de
  EduMedia»), escrita con la clave provisional en `ediciones/2099-01-NN.json`, igual que la
  biblioteca escribe en `biblioteca/`: así el generador, la revisión de dibujos y la comprobación
  de las traducciones son los de siempre. `reserva.py guardar CLAVE edumedia` la pasa a
  `reserva/CLAVE/ediciones(-XX).json`, también sin pieza, para que sus descartes no se vuelvan a
  proponer. Al usarla, entra en `ediciones/FECHA.json` del día como una pieza más y el día pasa a
  tener edición.
- **Caduca a los 30 días**, no a los 60 de las otras: las herramientas de imagen y vídeo cambian
  antes de precio y de condiciones, y al usar la reserva solo se comprueba, sin IA, que su web
  (`herramienta.url`) responde.
- **Dos piezas de cada grupo** en la reserva (las seis de `OBJETIVO`): `reserva.sh` escribe cada
  mañana la del grupo que tenga menos; a la par, primero EduMedia, después la biblioteca y después
  el repositorio. Si EduMedia o la biblioteca no dan pieza, ese día se escribe una del repositorio.

## Alternativas descartadas

- **Cambiar el encargo de la redacción**: ya pide una pieza por grupo; los huecos de EduMedia son
  días en que el grupo no da material, y forzar una pieza sería rellenar, que el encargo prohíbe.
- **Capturas en lugar de dibujo**, como el repositorio: las herramientas suelen enseñar una
  pantalla de entrada o de pago.
- **Sacarla del boletín semanal del grupo**: es un resumen de la semana, no un recurso que valga
  semanas después.

## Consecuencias

- Un número sin material de EduMedia lleva igualmente un artículo del grupo mientras la reserva
  tenga.
- Más trabajo de los agentes por la mañana (una pieza de EduMedia cada vez que se gaste una), con la
  misma suscripción; sin coste nuevo.
- Mientras se escribe, la clave provisional sale en la web generada como un número más, como ya
  pasaba con las de la biblioteca y el repositorio; `guardar` la retira al acabar.

## Validación

- Candidatos con el historial real (16-11-2026): 656 posibles, 25 por tanda.
- En una copia del repositorio: una pieza de EduMedia de prueba entra en la edición de un día que
  solo tenía Vibe Coding, con su traducción y su dibujo; el generador la publica en la sección
  Multimedia con el antetítulo, en castellano y en catalán. `guardar` funciona con pieza y sin ella.
- Una pieza real escrita por los agentes en una copia dentro del contenedor del NAS, revisada antes
  de dejarlo en marcha.
- La primera pieza que salió (EyeJack Creator, número del 17-11-2026) tenía el cuerpo como un texto
  seguido y no como lista de párrafos, porque el modelo de JSON de `encargos/edumedia-fondo.md` lo
  pedía así (`"cuerpo": "…"`). La comprobación de las traducciones quitó las cuatro ediciones
  traducidas del número («no tiene los mismos párrafos») y el generador pintó en castellano una letra
  por párrafo. Se vio en la vista previa, antes de publicar: se partió el cuerpo en sus cuatro
  párrafos y se rehicieron las traducciones (`scripts/traducir-dia.sh`). Para que no se repita: el
  encargo pide la lista; `scripts/forma.py`, sin IA, parte un cuerpo que llegue como texto, tras el
  revisor en `edumedia-fondo.sh` y antes de traducir en `noche.sh`; y `cargar()` de `generar.py` lo
  parte también al leer, por si llega por otro camino. Probado con el archivo que falló: cuatro
  párrafos, lo demás idéntico, y una segunda pasada no cambia nada.
