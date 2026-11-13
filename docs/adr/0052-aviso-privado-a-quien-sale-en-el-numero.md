# 52. Aviso privado a quien ha aportado algo que sale en el número

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

Quien ve su trabajo en el diario suele compartirlo, y eso trae lectores; pero nadie avisaba a las
personas cuyo recurso o documento salía en un número. Juanjo lo pidió el 13-11-2026 «para fomentar su
lectura y el interés», por privado y con un mensaje corto. Descartó la alternativa del agente de
mencionarlas en el aviso de cada grupo.

## Decisión

- **El diario dice a quién avisar; el bot escribe.** `scripts/avisos-personas.py`, que lanza
  `publicar-nas.sh` tras la cabecera de los avisos, añade a `avisos/<fecha>.json` una lista `personas`:
  el id de Telegram de cada una y las piezas que la cuentan, con su titular y su enlace en los cinco
  idiomas. Sin IA, con los datos del bot (`/bot-datos`):
  - Biblioteca: quien subió el documento (el «Aportado por Nombre (@usuario)» del mensaje del bot, o
    quien lo publicó si fue una persona). El diario no la nombra, pero el aviso le dice que su aportación
    tiene artículo.
  - Recursos del repositorio de VCE, en los artículos del repositorio o entre las fuentes de una pieza
    del redactor: quien lo dio de alta con el bot (`catalogo.json`).
  - Piezas del redactor: quien escribió el mensaje, solo si la pieza lo nombra en lo que se publica
    (titular, entradilla o cuerpo), es decir, si es el autor del recurso. A quien opina o pregunta el
    diario no lo nombra, así que no se le avisa. También el autor que nombra un anuncio de alta del bot.
  - «Hace un año» no avisa: cuenta lo que pasó entonces.
- **Un mensaje por persona y día**, con todas sus piezas, y un botón para no recibirlos más (ADR 0036 del bot).
- **Solo a quien ha hablado alguna vez con el bot**: Telegram no deja a un bot escribir primero a nadie.
  Quien sube documentos o da de alta recursos ya lo ha hecho, por privado con el bot.

## Consecuencias

- El diario sigue sin nombrar a quien solo sube un documento.
- Un nombre de Telegram distinto del que firma en el diario impide reconocer al autor de una pieza del
  redactor, salvo que el recurso esté en el catálogo; para Juan José de Haro hay una equivalencia fija.
