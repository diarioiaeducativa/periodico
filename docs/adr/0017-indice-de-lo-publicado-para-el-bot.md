# 17. Índice de lo publicado para el Bot de IA Educativa

Fecha: 2026-11-05 · Estado: aceptado

## Contexto

El Bot de IA Educativa publica cada mañana el aviso del número, pero no sabía qué traía: a quien
preguntaba por el diario lo mandaba a la web. El 03-11-2026 alguien le escribió «Me meto en el diario
pero solo puedo ver el número 2», y el bot no supo decirle que los demás están en la hemeroteca.
Al revisar las preguntas sin resolver, el 05-11-2026, Juanjo propuso: «quizás el diario debería
añadirse a la documentacion del bot de cada noche». Aprobó hacerlo ese mismo día.

## Decisión

- `generar.py` escribe en cada vuelta `indice/diario.json` (no está en el repositorio ni en el sitio):
  una entrada por pieza, breve, reportaje o editorial publicados, con su número, el día que cuenta y el
  día en que salió, la sección, el titular, la entradilla, el texto sin Markdown, el grupo, el enlace
  y el identificador del mensaje original, las fuentes y el enlace de la pieza en castellano y en
  catalán. Arriba, el último número y la hemeroteca.
- No lleva las notas internas de la redacción (`comprobado`, `repaso`, `descartado`): el bot solo ve
  lo que ve cualquier lector.
- `scripts/publicar-nas.sh` lo entrega al bot como `datos/diario/hemeroteca.json`, en la carpeta
  donde ya deja los avisos, solo cuando el sitio ya está subido, para que el bot no cite piezas que
  aún no están en línea. Se escribe en un temporal y se cambia de una vez.
- Cómo lo usa el bot, en su ADR 0030.

## Alternativas descartadas

- Que el bot lea la web o el `feed.xml`: el dato se toma de donde se genera, no de una copia
  publicada, y el RSS no trae el mensaje original de cada pieza.
- Publicar el índice en el sitio: no hace falta para el bot, que está en el mismo NAS.

## Consecuencias

- Una corrección hecha a mano durante el día (con `publicar.sh` desde el portátil) llega al bot con
  el número de la mañana siguiente.

## Validación

- 05-11-2026, en local: 44 entradas (32 piezas, 10 breves, un reportaje y una editorial), números
  1 a 4 y los días de prueba sin número; 21 enlaces de muestra (pieza en las dos ediciones y mensaje
  original) abren con 200.
