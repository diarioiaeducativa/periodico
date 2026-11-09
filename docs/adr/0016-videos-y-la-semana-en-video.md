# 16. Vídeos en el diario y «La semana en vídeo» cada domingo

Fecha: 2026-11-05 · Estado: aceptado

## Contexto

El 05-11-2026 se publicó en Instagram (@comunidad.iaeducativa) un primer reel sobre cómo encajan
los grupos, el bot, los boletines y el diario, hecho por programa y con música propia. Juanjo, ese
día: «cada semana se puede hacer un reel resumen de la semana, estos reels, el de hoy y los
próximos, ¿cómo pueden ir en el diario?». Antes (04-11) se había hecho un prototipo de vídeo
semanal a partir de una idea de Raül Torres (`prototipos/video-semanal/`), sin voz y con música
compuesta por programa, que gustó a los dos. Juanjo también pidió que la música no se repita:
«no puede ser siempre la misma».

## Decisión

Recomendado y aceptado por Juanjo el 05-11-2026 («hazlo así»):

- **«La semana en vídeo», cada domingo.** La noche del sábado, después de la traducción,
  `scripts/reel-semana.sh` lanza un agente (Sonnet, paso 19, `encargos/reel.md`) que elige las
  piezas de la semana y escribe, en castellano y catalán, un golpe, un titular
  corto y un dato por pieza, una descripción para la web y el texto para Instagram. Después
  `scripts/reel-semana.py` monta el vídeo **sin IA**: página animada con los dibujos y los colores
  del diario → fotogramas con Chromium de Playwright → MP4 con ffmpeg.
- **Un resumen de verdad, día a día** (05-11-2026, Juanjo: «si hablamos de un resumen, tiene que
  serlo de verdad, no trozos sueltos; en cuanto a la duración se puede alargar»). Al principio
  eran de 4 a 6 piezas, unos 40 s. Ahora va como mínimo una pieza de cada número de la semana,
  la más interesante de ese día, y hasta 10 en total si algún día tuvo varias; en orden de días y
  con el día en que salió cada una («Lunes 2») en su cabecera, delante del grupo (que se quita
  si no cabe). `reel-semana.py` rechaza el guion si falta algún número y el agente lo rehace.
  Cada pieza dura tres compases: con 7 piezas, de 48 a 62 s según el tempo; con 10, de 65 a 83 s. Si un texto no cabe, el
  agente lo rehace una vez; si sigue sin caber, esa semana no hay reel y el número sale igual.
- **Música distinta en cada vídeo** (`scripts/musica.py`, numpy, sin licencias de terceros): cada
  vídeo combina tempo, tonalidad, modo, progresión, patrón de batería, timbre y arpegio; la
  combinación de tempo, tonalidad, modo y progresión no se repite nunca (se comprueba contra el
  estilo guardado en cada `videos/*.json` y el del primer reel), y tempo, tonalidad y batería
  cambian respecto al anterior.
- **En la web, alojados por el diario y no incrustados desde Instagram**, que metería los
  rastreadores de Meta. Versión de 720 × 1280 (unos 1,3 MB por cada 40 s de vídeo e idioma: de
  1,6 a 2,7 MB por vídeo semanal, y de 170 a 280 MB al año con los dos idiomas). `videos/<id>.json` guarda el título, la descripción, lo que dice en
  pantalla (para quien no puede ver el vídeo), los archivos por idioma, el enlace de Instagram y
  el estilo de la música. Desde el 9 de noviembre los vídeos van en Internet Archive y en el sitio,
  solo las portadas (ADR 0037).
  - Página **«Vídeos»** (`videos.html`), con todos, cada uno con su ancla para compartirlo,
    enlazada desde el pie junto a un enlace sencillo a la cuenta de Instagram.
  - Bloque **«La semana en vídeo»** en la portada del número del domingo, tras la viñeta.
  - En «La redacción», el guionista de vídeo figura en el equipo, en el organigrama (franja de
    los domingos: números de la semana → guionista de vídeo → vídeo) y en el proceso (06-11-2026).
  - Los demás vídeos, como el reel de la comunidad, solo en «Vídeos». Hasta el 06-11-2026 el
    de la comunidad iba también en «La redacción», tras la entradilla; Juanjo pidió quitarlo de
    allí («no me gusta ahí… que se quede en la sección de vídeos solamente»).
  - Sin reproducción automática, con portada, `playsinline` y la lista de lo que aparece en
    pantalla siempre plegada. En el bloque del domingo, en pantalla ancha,
    el vídeo alineado a la izquierda y su texto al lado; en el móvil, uno debajo de otro. La
    página «Vídeos» es una galería de tarjetas (vídeo, título, fecha y descripción). Juanjo,
    05-11-2026: la primera versión, con la lista desplegada junto a cada vídeo, «esto es horrible». Si un vídeo no tiene versión en el idioma de la página, va el
    castellano y se dice.
- **En Instagram**, solo la versión castellana (1080 × 1920), el domingo desde las 9:00 (al principio, desde las 12:00; ADR 0027), separada
  del carrusel de las 7:05 (`instagram.py reel`, ADR 0015). Un solo intento; su enlace se guarda en
  el JSON del vídeo y aparece en la web con la siguiente publicación.

## Alternativas descartadas

- **Incrustar el reel de Instagram**: rastreadores de Meta en el diario, que no tiene contadores.
- **Un servicio de vídeo de terceros (YouTube)**: misma objeción y dependencia de Google.
- **Reel diario**: la misma plantilla cada día cansa y la música tendría que cambiar a diario (ADR 0015).
- **Hacerlo con IA generativa de vídeo**: coste por vídeo y resultado sin revisar; el programa
  reproduce el estilo del diario sin coste.

## Consecuencias

- Unos 5 minutos de CPU en el portátil por vídeo con los dos idiomas (en el NAS, más), la noche
  del sábado.
- El repositorio del sitio ya no crece con los vídeos, que van en Internet Archive (ADR 0037).
- La imagen del contenedor necesita numpy (Dockerfile).

## Evidencia

- Prueba del 05-11-2026 con un guion de la semana del 30-10 al 05-11: 42 s, −13,9 LUFS, 4,4 MB en
  1080 p y 1,4 MB en 720 p por idioma, 5 minutos en el portátil; capturas de cada escena revisadas
  en los dos idiomas.
- Reel de la comunidad: https://www.instagram.com/reel/DfWeeynpc7L/

## Riesgos y limitaciones

- El agente podría elegir, de cada día, una pieza poco representativa: el encargo pide la que
  más interesa a un docente cualquiera, y Juanjo lo verá el domingo.
- Si Instagram tarda más de 10 minutos en procesar el vídeo, no se publica y se avisa.

## Validación

- `reel-semana.py --prueba` y vídeo completo con el guion de prueba; página «Vídeos», bloque del
  domingo y «La redacción» revisados en local.
- Primer reel real: domingo 08-11-2026 (pendiente).
