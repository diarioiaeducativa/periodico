# 28. El reportaje sale siempre, y las reservas caducan

Fecha: 2026-11-06 · Estado: aceptado

## Contexto

Juanjo: «el reportaje no puede faltar, siempre estará» (06-11-2026). Hasta entonces faltaba si el jefe
de reportajes decía que la semana no daba, si el verificador no lo daba por bueno, si el ilustrador
estropeaba el archivo o si fallaba la noche. Y sobre las reservas: «se actualizan de vez en cuando? no me
gustaría que pasados 6 meses saliese un artículo ya caduco». No se actualizaban: se daban por eternas.

## Decisión

- **El jefe de reportajes elige siempre un tema** (`encargos/reportaje.md`, paso 7): si la semana va
  floja, uno de semanas anteriores que siga vivo o un documento de la Biblioteca digital. Si aun así
  dice que no, se le pide otro una vez.
- **Segunda vuelta con el verificador**: si no lo da por bueno, el reportero lo corrige con su motivo y
  se verifica otra vez. El verificador sigue pudiendo rechazarlo: el rigor no se rebaja.
- **Si el ilustrador estropea el archivo**, sale el reportaje verificado sin infografía.
- **Reportaje de reserva** (`scripts/reserva_reportaje.py`, `reserva/reportajes/`): uno escrito y
  verificado con el mismo proceso (`RESERVA=1 scripts/reportaje.sh 2099-02-NN`) sobre un tema que no
  caduque en un mes. Lo usa noche.sh si el del sábado no sale, y `reserva.py usar` (plan B de las 6:30 y
  vigilante de GitHub) si el número del domingo se queda sin reportaje. Su infografía se mira con el
  programa el domingo en que sale, porque al escribirla no tiene página. Se avisa a Juanjo.
- **El mejor de los dos** (Juanjo, 06-11-2026, al ver el primero de reserva: «que alguien decida si usar
  el que se haga nuevo o este, el mejor se publica»): si el sábado hay reportaje nuevo y uno de reserva
  vigente, un juez de reportajes (Opus, paso 11b, que no ha escrito ninguno) los compara por interés y
  utilidad para un docente, rigor, escritura, actualidad y que no repita tema; en caso de duda, el nuevo.
  Si gana el de reserva, se publica ese (su infografía se revisa entonces en su página, con revisor) y el
  nuevo queda en `reportajes-borrador/FECHA-descartado.json`, sin traducir; a la mañana siguiente se
  escribe otro de reserva. La elección y su motivo van en el aviso de las 5:00 del domingo.
- **Publicar el de reserva a propósito** (Juanjo, 07-11-2026, al ampliar el de reserva con todas las
  comunidades autónomas: «He decidido publicar el reportaje de reserva este domingo»): si existe
  `estado/FECHA.reportaje-reserva` (FECHA, el sábado), `noche.sh` no escribe reportaje nuevo y sigue el
  mismo camino que cuando el reportaje falla: pone el de reserva, revisa su infografía en su página y
  continúa con el vídeo y las redes. El archivo se crea a mano en el NAS y vale solo para ese sábado.
- **Caducidad de las reservas**: una pieza de reserva sin usar se retira a los 60 días; el reportaje,
  a las 4 semanas. Lo hace `reserva.sh` cada mañana, que después escribe lo que falte (una pieza o el
  reportaje). Lo retirado queda en `reserva/retiradas/` y `reserva/reportajes/retirados/`, con el motivo.
- **Comprobación antes de usarla**, sin IA para que el plan B sea rápido: de una pieza, que cada recurso
  responda en su dirección; del reportaje, que no falle más de una de cada cinco fuentes. Si no pasa, se
  retira y se usa la siguiente.

## Alternativas descartadas

- Rebajar al verificador para que siempre apruebe: publicaría lo no confirmado.
- Reservas sin caducidad: es lo que había; un tema de hace meses puede haber cambiado.

## Validación

Sintaxis y órdenes probadas en local (`reserva.py cuantas`, `reserva_reportaje.py cuantos` y `clave`).
El primer reportaje de reserva se escribe el 06-11-2026 en el NAS para que el domingo 08-11 esté cubierto.

## Riesgos

- Cuesta un reportaje más al mes de agentes (con la suscripción) aunque no se use.
- La comprobación de enlaces no detecta un recurso que sigue en línea pero ha cambiado (por ejemplo, de
  gratuito a de pago); para eso está la caducidad.
