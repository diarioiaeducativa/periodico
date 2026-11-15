# 68. El número de reserva: entero o por partes, y ningún número de menos de tres piezas

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

La reserva (ADR 0021 y 0028) tenía piezas sueltas («Del fondo del repositorio» y «Del fondo de la biblioteca») y un
reportaje, pero se usaba una sola pieza: un día sin nada que contar, o una noche que fallara, salía un número de un
artículo, sin viñeta ni «Hace un año». Juanjo, al preguntar qué saldría un día sin actividad: «creo que será mejor
hablar del concepto de número de reserva. Un número entero que pueda suplir un día completo o una parte». Decidió
además que el número de reserva no diga nada en la web («no se dice nada») y que también se use para completar los
días flojos («sí»). En los 18 números del 28-10 al 14-11-2026, dos bajaron de tres piezas (el 29-10, con una, y el
14-11, con dos).

## Decisión

- **Las partes del número de reserva**, siempre listas y escritas con antelación, en los cinco idiomas:
  - las piezas de reserva (`scripts/reserva.py`, seis: dos números enteros, para que una caída del NAS de dos días
    no la agote; antes, tres. Caducan a los 60 días);
  - una **viñeta de reserva** (`scripts/reserva_vineta.py`, `scripts/vineta-reserva.sh`, encargos `30-vineta-reserva`
    y `31-vineta-reserva-traduccion`): una tira sobre un asunto de la docencia con IA que no caduca, que no sale de
    ninguna noticia; lleva `"reserva": true` y la web no le pone «A partir de…». Caduca a los 60 días;
  - **«Hace un año» por adelantado** (`scripts/reserva_hace_un_ano.py`, `ADELANTO=1 scripts/hace-un-ano.sh`): solo
    depende de los mensajes de hace un año, así que `reserva.sh` deja escritos los de las próximas siete noches (dos
    como mucho cada mañana), en `reserva/hace-un-ano/FECHA/`. La noche de cada número, `hace-un-ano.sh` coge el suyo
    y solo revisa su dibujo, que al escribirlo no tenía página; si no está, lo escribe como siempre. Para no repetir
    tema, mira también los escritos por adelantado;
  - el reportaje de reserva (ADR 0028), uno por semana.
- **Se usa entero o por partes**, sin IA (`reserva.py usar FECHA fallo|relleno`): completa el número hasta
  `MINIMO = 3` piezas con las de reserva y, si le faltan, pone la viñeta y «Hace un año». `noche.sh` lo lanza cada
  noche con «relleno», antes de las comprobaciones y de la traducción, así que los avisos de las 7:00 ya cuentan con
  lo puesto. Un día sin piezas de la redacción (`solo_anexos`) sale con lo que den la biblioteca y el repositorio,
  su «Hace un año» y lo que falte de la reserva. Los planes B (reserva de las 6:30 y vigilante) lo lanzan con «fallo».
- **La web no dice nada** de un número completado o hecho con la reserva por relleno. Solo el de un fallo de la
  redacción lo sigue diciendo, porque las conversaciones de ese día salen al siguiente (ADR 0021).
- **Se repone cada mañana** (`reserva.sh`, desde las 8:00): lo que se haya gastado o caducado.

## Alternativas descartadas

- **Escribir un número entero cada semana**: se tiraría casi siempre sin usarse. Reponer solo lo gastado cuesta menos
  y nunca deja la reserva vieja.
- **Una tercera fuente de piezas de reserva** (temas de fondo de conversaciones antiguas) para que un número entero de
  reserva no salga solo con «Vibe coding» y «Biblioteca»: no ha pasado nunca un día así; se deja para cuando haga falta.

## Consecuencias

- Coste: en una semana normal, una o dos piezas repuestas y, de vez en cuando, una viñeta; «Hace un año» por
  adelantado sustituye al de cada noche. La primera semana se escriben dos «Hace un año» cada mañana hasta tener siete.
- `reserva.py usar` ya no escribe los avisos sin IA con «relleno» (los escribe el agente de avisos después); solo con
  «fallo». Arreglado de paso: una variable pisaba el motivo («fallo» o «relleno») con el de la comprobación de enlaces.

## Riesgos y limitaciones

- En los planes B, «Hace un año» por adelantado se pone sin revisar su dibujo (no hay revisor a esa hora).
- Un «Hace un año» escrito siete días antes dice cómo están las cosas ese día, no el de su publicación.

## Validación

En una copia del diario con los datos del 15-11-2026, sin IA: el número del 14-11 (dos piezas) pasó a tres con una de
reserva y sin marca; un día sin nada salió con tres piezas de reserva, la viñeta de reserva y «Hace un año», marcado
«relleno», sin franja en la web. La portada, en Chromium y Firefox, en escritorio y móvil, sin errores: abre con la
pieza de la Biblioteca, la viñeta sin «A partir de…» y «Hace un año» al final.
