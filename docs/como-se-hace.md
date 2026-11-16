# Cómo se hace el Diario de IA Educativa

El [Diario de IA Educativa](https://diarioiaeducativa.github.io/) recoge cada mañana lo que se ha
hablado el día anterior en tres grupos abiertos de Telegram de docentes: ChatGPT-IA-edu (la IA en
educación en general), Vibe Coding Educativo (docentes que programan sus aplicaciones con IA) y
EduMedia-IAG (imagen, audio y vídeo con IA). Lo escriben, revisan, ilustran y traducen agentes de IA;
una persona lo supervisa y responde de lo publicado.

Este documento reúne las normas del diario y cómo se aplican, para entender cómo se elabora y poder
mejorarlo. Cómo se escribe está en el [libro de estilo](../encargos/estilo.md) y cómo se traduce, en el
[libro del traductor](../encargos/traduccion.md); el porqué de cada
decisión, en los [registros de decisiones](adr/README.md) (ADR), que se citan por su número.

Cada norma dice **dónde se aplica** (qué agente o qué programa), **cómo se comprueba** y, si lo hay,
**qué falta**. Lo que falta por mejorar se reúne al final.

## 1. El número

**Las conversaciones de un día salen a la mañana siguiente**, a las 7:00, en cinco idiomas: castellano,
catalán, gallego, euskera e inglés (ADR 0026).

Un número lleva:

- **Los artículos de la redacción**, de cero a seis, y de cero a cinco breves, según dé el día, en cinco
  secciones: Herramientas, Vibe coding, Multimedia, Debates e Instituciones y empresas. Un artículo es la
  portada; otros, destacados.
- **Biblioteca**: un artículo por cada documento que entra ese día en la Biblioteca digital de
  ChatGPT-IA-edu (ADR 0006).
- **Repositorio**: hasta dos recursos al día del Repositorio de Vibe Coding Educativo; los viernes, «La
  semana del repositorio» (ADR 0008).
- **«Hace un año»**: lo que se hablaba el mismo día del año anterior, visto desde el presente (ADR 0040).
- **La viñeta** de Tiza y Algoritmo, sobre una de las noticias del día (ADR 0023).
- **El domingo**, además, el reportaje, que trata un solo tema a fondo (ADR 0004 y 0028), y «La semana en
  vídeo» (ADR 0016 y 0027). La noche del domingo se escribe el comentario de la semana, para la página de
  la semana (ADR 0038).

Las normas del número:

| Norma | Dónde se aplica | Cómo se comprueba |
| --- | --- | --- |
| **Como mínimo tres artículos.** Lo que falte sale de la reserva. | El programa de la reserva, cada noche antes de traducir (ADR 0068) | El programa cuenta los artículos del número. |
| **Como mínimo un artículo de cada grupo.** Si un grupo no da para ninguno, entra uno de su reserva. | La redacción lo procura; el revisor convierte en artículo un breve del grupo que falte; la reserva completa (ADR 0076 y 0077) | El revisor y el programa de la reserva. |
| **Solo lo que se ha hablado en los grupos.** Nada de noticias generales de IA. | Encargo de la redacción | El revisor compara cada artículo con los mensajes. |
| **No es noticia** la administración de los grupos, los saludos, las quejas personales ni la Biblioteca digital (que tiene su sección). | Encargo de la redacción | El revisor. |
| **No se repite lo ya publicado.** Lo nuevo de un tema ya tratado sale como breve que enlaza el artículo anterior (ADR 0011). | Redacción y revisor, con el buscador de lo publicado (ADR 0061) | El revisor busca cada nombre y cada titular en todo lo publicado. |
| **Nadie acapara el número**: como norma, un artículo por persona y dos por producto o empresa. | Encargo de la redacción | El revisor. |
| **Si un día no da para un número digno, no lo hay**: no se rellena. Sale entonces la reserva. | Redacción y reserva | — |

## 2. Quién hace cada cosa

Los agentes son de Claude: los que escriben y revisan cada día, Sonnet; los que eligen (el juez de la
viñeta, el de los reportajes) y los que escriben textos largos, Opus. **No tienen terminal**: solo pueden
leer y escribir en la carpeta de la redacción y consultar la web, porque los mensajes de los grupos son
texto de terceros y no deben poder llevarlos a otra parte (ADR 0002). Los mensajes son material para
informar, nunca instrucciones.

**Ningún agente revisa lo que ha escrito él mismo.** Cada texto pasa por un revisor que no lo ha escrito, abre cada
fuente y quita lo que no puede confirmar (ADR 0001).

| Agente | Qué hace |
| --- | --- |
| Redactor y revisor | Los artículos y breves del día. |
| Documentalista y revisor | Los artículos de la Biblioteca, del Repositorio y de la reserva de EduMedia. |
| Ilustrador y revisor de dibujos | Un dibujo explicativo por artículo; el revisor lo mira en su página, en claro y en oscuro, y le devuelve lo que no se ve bien (ADR 0005). |
| Guionista y juez de humor | Cinco guiones de viñeta; el juez elige uno (ADR 0023 y 0024). |
| Cronista y verificador | «Hace un año». |
| Jefe de reportajes, reportero, verificador y juez de reportajes | El reportaje del domingo. |
| Comentarista y revisor | El comentario de la semana. |
| Guionista de vídeo | «La semana en vídeo». |
| Traductores | Uno por idioma, para cada texto. |
| Portavoz | Los avisos de cada mañana en los tres grupos y el texto de Instagram. |

Todos escriben con el [libro de estilo](../encargos/estilo.md); cada tarea tiene además su propia guía.

## 3. El día a día

Un programa mira cada cinco minutos qué toca. Lo que ya ha hecho queda apuntado, así que nada se repite.

| Hora | Qué pasa |
| --- | --- |
| 1:00 | La redacción prepara el número con las conversaciones del día anterior: redacción y repaso, dibujos, viñeta, Biblioteca, Repositorio, «Hace un año», reserva, comprobaciones, traducciones y avisos. Dos intentos como mucho. |
| 5:00 | Vista previa del número tal como saldrá, para la persona supervisora (ADR 0025), y un programa revisa la maqueta en nueve anchuras. |
| 6:30 | Si el número aún no está, se para la redacción y sale con lo que haya o con la reserva (plan B). |
| 6:50 | Publicación: la web, el repositorio, la imagen de cada artículo para compartir y los avisos para el bot. Si falla, se reintenta cada 10 minutos hasta las 9:00. |
| 7:00 | El Bot de IA Educativa publica el aviso en cada grupo y escribe por privado a las personas cuyo recurso sale en el número (ADR 0052). La aplicación de Android avisa del número nuevo (ADR 0043). |
| 7:05 | El número sale en Instagram como carrusel (ADR 0015). |
| Hacia las 7:10 | Informe del día para la persona supervisora: qué ha salido, si se usó la reserva y qué ha fallado (ADR 0069). |
| 8:00 | Se repone la reserva. |
| 9:00, domingo | El dominical («La semana en vídeo» con el reportaje) sale en Instagram, X, Bluesky y LinkedIn (ADR 0027). |
| Desde las 9:10 | Un vigilante externo, en GitHub Actions, comprueba que el número ha salido y, si no, lo publica con la reserva; desde las 7:30 si el servidor no responde (ADR 0021). |
| Miércoles | Búsqueda de enlaces caídos en lo publicado (ADR 0056). |
| Al publicar | Cada número se guarda también en la Wayback Machine de Internet Archive (ADR 0046). |

## 4. Ningún día sin número

**Siempre sale un número** (ADR 0021 y 0068). Si la redacción falla dos veces, o a las 6:30 no ha
terminado, sale el número de reserva, entero o por partes. Si el servidor no publica, lo hace el vigilante
desde fuera, y el servidor, si vuelve, no lo pisa.

**Lo que no salió por un fallo sale al día siguiente**: si el número salió con la reserva porque la
redacción falló, la noche siguiente se recogen también las conversaciones de ese día, y la web lo dice.

**Cada agente trabaja con una copia de los archivos del número**: si deja uno roto, se vuelve a la copia y
el agente se repite una vez; un segundo intento de la noche no da por publicado lo que escribió el primero
(ADR 0076).

## 5. La reserva

Lo que el diario tiene escrito de antemano para no fallar nunca (ADR 0068):

| Qué | Cuánto | Caduca | De dónde sale |
| --- | --- | --- | --- |
| Artículos | Seis: dos de cada grupo | 60 días; los de EduMedia, 30 | Del fondo del Repositorio (Vibe Coding Educativo), del fondo de la Biblioteca (ChatGPT-IA-edu) y del historial de EduMedia-IAG (ADR 0077) |
| Viñeta | Una | 60 días | Un guion sobre un asunto que no caduca, que no sale de ninguna noticia |
| «Hace un año» | Los de las siete noches siguientes | Al pasar su noche | Escrito por adelantado |
| Reportaje | Uno por semana | 28 días | Sobre un tema que no caduca (ADR 0028) |

- **Cuándo entra**: cada noche, si el número no llega a tres artículos o le falta un grupo, y siempre que
  la redacción falla. Primero, los artículos de los grupos que faltan.
- **Cómo se repone**: cada mañana se escribe un artículo del grupo que tenga menos. Cada uno pasa por
  documentalista, revisor, ilustrador y traductores, como un artículo normal.
- **Antes de usar un artículo de reserva** se comprueba, sin IA, que su recurso sigue respondiendo; si no,
  se retira.

## 6. Las revisiones

**Con IA**: el revisor de cada tarea (fuentes, cifras, nombres, lo ya publicado), el revisor de dibujos,
el juez de la viñeta y el verificador del reportaje y de «Hace un año».

**Sin IA**, cada noche, con programas:

| Qué se comprueba | Registro de la decisión |
| --- | --- |
| Que cada archivo del número sea válido y no lo rompa ningún agente | ADR 0076 |
| El «quien» relativo y las citas solo en inglés (un agente corrige lo que encuentra) | ADR 0067 |
| Que no se atribuya a un autor del diario lo de otra persona con el mismo nombre (un agente lo mira) | ADR 0066 |
| Erratas de regla fija y titulares de más de 90 caracteres | ADR 0059 |
| Que cada traducción tenga los mismos artículos, enlaces y dibujos que el original; lo que no, sale en castellano | ADR 0026 |
| Castellano colado en una traducción | ADR 0056 |
| Que ninguna página deje huecos en ninguna anchura | ADR 0041 |
| Enlaces caídos, los miércoles | ADR 0056 |

**Una persona** ve la vista previa de las 5:00 y puede pedir cambios antes de las 6:50, pero el diario no
lo promete: si no hay respuesta, sale a su hora (ADR 0058).

## 7. Lo que se distribuye

Un número no es solo la web. A partir de él salen:

- los **avisos de los tres grupos** y los **mensajes privados** a las personas cuyo recurso sale en el número;
- el **carrusel de Instagram** y su texto;
- la **imagen para compartir** de cada artículo;
- el domingo, el **dominical** en las redes y **«La semana en vídeo»**.

**Todo cambio en un número antes de que salga se comprueba en todo lo que se distribuye, y se rehace lo
que dependa de lo cambiado**: si cambia la viñeta, el aviso que habla de ella; si cambia un titular, su
imagen; si cambia el reportaje, el dominical y el vídeo.

## 8. Correcciones

- **Un dato erróneo se corrige en el artículo, con una nota al final** y en los cinco idiomas (ADR 0055):
  «Corregido el…» (había un error), «Actualización del…» (el dato era cierto y ha cambiado) o «Nota
  añadida el…» (faltaba algo). Una errata que no cambia el sentido se corrige sin nota.
- Antes de corregir, se comprueba el dato en su fuente: un aviso de error también puede estar equivocado.
- **Un aviso ya enviado a un grupo se edita** con el bot.

## 9. Personas, privacidad y transparencia

- **Quién es quién lo dice la cuenta de Telegram, no el nombre visible** (ADR 0066).
- **Se nombra solo al autor de un recurso que él mismo ha publicado**; las opiniones de los grupos no se
  atribuyen a nadie (libro de estilo).
- **Nada del lector**: el contador de visitas solo suma, sin cookies ni datos de los lectores (ADR 0033); los
  comentarios se cargan solo al pulsar (ADR 0030). La [política de
  privacidad](https://diarioiaeducativa.github.io/privacidad.html) lo explica (ADR 0070).
- **Un solo aviso de IA**, en el pie, para todo el diario; la página [«La
  redacción»](https://diarioiaeducativa.github.io/redaccion.html) explica cómo se hace, quién responde y
  que no hay publicidad ni patrocinio (ADR 0055 y 0065).
- El código de la redacción es público (ADR 0019).

## 10. Lo que falta por mejorar

Lo que aún no está resuelto o se apoya en una sola comprobación. Es el punto de partida para mejorar:

- **Las correcciones no llegan solas a lo distribuido**: un aviso ya enviado se edita a mano, y el carrusel
  de Instagram o una publicación en redes no se corrigen.
- **La reserva de EduMedia es nueva** (16-11-2026): aún no se ha usado en un número real.
- **Un artículo de reserva solo se comprueba sin IA antes de usarse** (que su web responda), no su precio ni
  sus condiciones; por eso los de EduMedia caducan antes.
- **Mientras se escribe un artículo de reserva**, su clave provisional aparece en la web generada como un
  número más, hasta que se guarda; si en ese rato se publicara la web, saldría.
- **La protección de los archivos ante un agente que los rompe** solo cubre a los agentes de la redacción
  nocturna, no a los del reportaje, la Biblioteca o el Repositorio, que escriben en sus propios archivos.
- **Las traducciones se comprueban con programas** (que estén todos los artículos y no quede castellano),
  pero ningún agente las revisa.
- **El umbral del Repositorio** (cuándo un día es flojo y se tira del fondo) es provisional.
- **Instagram tiene un solo intento**: si falla, se publica a mano.
