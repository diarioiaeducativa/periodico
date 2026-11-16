# 76. Los JSON del número, a salvo de cada agente, y un artículo de cada grupo

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

En la noche del 15 al 16-11-2026 la redacción escribió un número normal: cuatro piezas (una de
ChatGPT-IA-edu, dos de Vibe Coding Educativo y una de EduMedia-IAG) y tres breves. Al añadir las
descripciones de los dibujos (`ilustracion_alt`), el ilustrador hizo cuatro ediciones sobre
`ediciones/2026-11-15.json` y una de ellas unió el final de la pieza de Antigravity con el
principio de la de Seedream: el archivo dejó de ser JSON válido. Con él fallaron la Biblioteca,
el Repositorio, la reserva, las traducciones (se quitaron por «no tener las mismas piezas») y el
generador, y `noche.sh` salió con error.

En el segundo intento, `publicado.py` ya había apuntado en `publicado.txt` las piezas del
primero, y la redacción las dio por publicadas: escribió un número sin piezas. La reserva lo
completó con dos piezas del fondo del repositorio, las dos de Vibe Coding. El número habría salido
sin nada de los otros dos grupos. Se recuperó a mano a las 6:00 desde las conversaciones de los
agentes.

Juanjo, al verlo: «como mínimo tiene que haber un artículo de cada grupo».

## Decisión

1. **Cada agente de `noche.sh`, con copia de los JSON del número.** `agente()` copia antes los JSON
   del día que son válidos (`json_del_dia`: `*/FECHA.json`, `*/*/FECHA.json`, `*/FECHA-*.json` y los
   avisos) y, al acabar, devuelve a la copia los que hayan quedado rotos y repite el agente una vez.
   Si los vuelve a romper, siguen como antes del agente (sin sus cambios en ellos) y se anota.
   Cubre los agentes que lanza `noche.sh` y lo que usa su `agente()` (`traducir.sh`, `dibujos.sh`);
   los scripts con su propio `agente()` (reportaje, biblioteca, repositorio…) no tocan la edición.
2. **`publicado.py --sin FECHA`** antes de la redacción y en `solo_anexos`: el día que se prepara no
   cuenta como publicado. Después de la redacción se sigue llamando sin `--sin`, para que la
   Biblioteca y el Repositorio enlacen las piezas del día.
3. **La reserva, por grupos** (`reserva.py`, ADR 0068): para llegar a `MINIMO` elige primero la pieza
   más antigua de un grupo que aún no tiene pieza en el número; y, aunque ya llegue, añade una de cada
   grupo que siga faltando si la reserva tiene de ese grupo. Esto último no se hace en un número sin
   ninguna pieza propia, que ya sale entero de la reserva.

## Consecuencias

- Un agente que rompe un JSON cuesta, como mucho, repetirlo; el número no se pierde.
- Al decidirlo, la reserva solo tenía piezas del fondo del repositorio (Vibe Coding Educativo) y de la
  Biblioteca digital (ChatGPT-IA-edu); la de EduMedia-IAG llegó el mismo día con el ADR 0077.
- Un día con muchas piezas de un solo grupo gasta una pieza más de la reserva.

## Validación

- Protección: un `claude` falso que rompe `ediciones/FECHA.json` dos veces seguidas; el archivo vuelve a
  su contenido, el agente se repite una vez y el registro lo dice (16-11-2026).
- Reserva, en una copia con la reserva real (dos piezas de VCE y una de la Biblioteca): un número con
  una sola pieza de VCE toma primero la de la Biblioteca y luego la más antigua de VCE; uno con tres
  piezas (dos de VCE y una de EduMedia) añade la de la Biblioteca.
- `noche.sh` pasa `bash -n`. La noche del 16 al 17-11 es la primera prueba real.
