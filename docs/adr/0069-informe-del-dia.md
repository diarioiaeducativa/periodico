# 69. El informe del día para Juanjo

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

Lo que pasa cada mañana estaba repartido entre el registro de la noche, los avisos sueltos por Telegram, los
archivos del bot y los del boletín. Juanjo: «quiero recibir cada día un informe para saber si se ha publicado todo, se
ha usado la reserva, a quién se le han enviado mensajes y cualquier fallo que haya o aspecto que consideres
importante. El domingo igual pero una vez publicado en redes. Los días de cada día después de las 7 pero no muy
tarde, en cuanto se pueda dar el informe».

## Decisión

- `scripts/informe-dia.py`, sin IA, reúne: si el número salió y con cuántas piezas; si se usó la reserva (entera por
  fallo o por no haber nada, o para completar; con los titulares), la viñeta y «Hace un año» (si eran de reserva o
  escritos por adelantado) y, el domingo, el reportaje (nuevo o de reserva, y por qué); los avisos de los grupos y a
  quién se escribió por privado (y a quién no se pudo); Instagram (carrusel y, el domingo, «La semana en vídeo») y el
  dominical en X, Bluesky y LinkedIn; los fallos (plan B, reintentos de publicación, autoría y estilo sin corregir,
  traducciones quitadas, dibujos que siguen retirados y las líneas de ERROR y AVISO del registro), y cómo está la reserva.
- Lo manda el Bot de IA Educativa (Juanjo: «tienes que enviarlo por el bot de IA educativa, que es el que hace este
  tipo de cosas de los grupos»): `reloj.sh` lo deja en `/avisos-bot/FECHA.informe.txt` y el bot se lo manda por privado
  (su ADR 0040); si no puede dejarlo, va por avisar-juanjo. Se genera una vez al día, en cuanto se puede dar (`--listo`): entre semana,
  cuando han salido el número, los avisos, los privados y el carrusel (hacia las 7:10); el domingo, además, cuando han
  salido el vídeo de la semana y el dominical en las tres redes (o han dejado de intentarlo). Si algo se atasca, sale
  igual a las 9:05 (el domingo, a las 11:00) diciendo qué falta.
- El estado del dominical lo deja el contenedor del boletín: se monta en el del diario, solo para leer, en `/dominical`.

## Alternativas descartadas

- **Que lo escriba un agente**: no hace falta interpretar nada; un programa no se equivoca ni gasta.
- **Nota de voz**: el informe es para mirarlo, con enlaces; los avisos de trabajo largo siguen siendo de voz.

## Validación

Con los datos del 15-11-2026: sale el número con sus tres piezas y la de reserva por su titular, el reportaje
cambiado a mano, los tres avisos privados por nombre, los enlaces de Instagram, X y Bluesky (LinkedIn no da el de la publicación: se enlaza la actividad reciente) y el aviso de castellano en las
ediciones traducidas; un dibujo retirado y vuelto a poner a mano no cuenta como retirado.
