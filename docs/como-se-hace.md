# Cómo se hace el Diario de IA Educativa

El [Diario de IA Educativa](https://diarioiaeducativa.github.io/) recoge cada mañana lo que se ha
hablado el día anterior en tres grupos abiertos de Telegram de docentes: ChatGPT-IA-edu (la IA en
educación en general), Vibe Coding Educativo (docentes que programan sus aplicaciones con IA) y
EduMedia-IAG (imagen, audio y vídeo con IA). Lo escriben, revisan, ilustran y traducen agentes de IA;
una persona lo supervisa y responde de lo publicado.

Este documento reúne las normas del diario y cómo se aplican, para entender cómo se elabora y poder
mejorarlo. Cómo se escribe está en el [libro de estilo](../encargos/estilo.md) y cómo se traduce, en el
[libro del traductor](../encargos/traduccion.md). El porqué de cada decisión está en los [registros de
decisiones](adr/README.md) (ADR), que se citan por su número.

Cada norma dice **quién la aplica**, **cómo se comprueba** y, si hace falta, **qué le falta**. Lo que
falta por mejorar se reúne al final.

## 1. El número

**Lo que se habla un día sale en el diario a la mañana siguiente**, a las 7:00 (hora peninsular española), en cinco idiomas:
castellano, catalán, gallego, euskera e inglés (ADR 0026).

Un número lleva:

- **Los artículos del día**: de ninguno a seis, y de ninguno a cinco breves, según lo que haya dado el
  día, en cinco secciones: Herramientas, Vibe coding, Multimedia, Debates e Instituciones y empresas.
- **Biblioteca**: un artículo por cada documento que se ha añadido ese día a la Biblioteca digital de
  ChatGPT-IA-edu (ADR 0006).
- **Repositorio**: hasta dos aplicaciones al día del Repositorio de recursos de Vibe Coding Educativo;
  los viernes, un resumen de las de la semana (ADR 0008).
- **«Hace un año»**: algo de lo que se hablaba el mismo día del año anterior, comparado con cómo está hoy
  (ADR 0040).
- **La viñeta** de Tiza y Algoritmo, sobre una de las noticias del día (ADR 0023).
- **El miércoles**, además, una columna de opinión sobre un debate de los grupos: la única pieza del diario que
  toma partido, firmada por el modelo de IA que la escribe (ADR 0092).
- **El domingo**, además, un reportaje que explica a fondo un solo tema (ADR 0004 y 0028) y «La semana en
  vídeo», un vídeo corto con lo más destacado de la semana (ADR 0016 y 0027). La noche del domingo se
  escribe también un comentario sobre lo más importante de la semana (ADR 0038).

Las normas de cada número:

| Norma | Quién la aplica | Cómo se comprueba |
| --- | --- | --- |
| **Como mínimo tres artículos.** Si faltan, se completan con artículos guardados para estos casos (la reserva, apartado 5). | Un programa, cada noche, antes de las traducciones (ADR 0068) | El programa cuenta los artículos. |
| **Como mínimo un artículo de cada grupo.** Si un grupo no da para ninguno, entra uno guardado de ese grupo. | El agente que redacta lo intenta; el que revisa convierte en artículo un breve del grupo que falte; si aun así falta, la reserva (ADR 0076 y 0077) | El revisor y el programa de la reserva. |
| **Solo lo que se ha hablado en los grupos.** Nada de noticias generales sobre IA. | El agente que redacta | El revisor compara cada artículo con los mensajes. |
| **No es noticia** la organización interna de los grupos, los saludos ni las quejas personales. Los documentos de la Biblioteca digital tienen su propia sección. | El agente que redacta | El revisor. |
| **No se repite lo ya publicado.** Si hay algo nuevo sobre un tema ya tratado, sale como breve, con un enlace al artículo anterior (ADR 0011). | El que redacta y el que revisa, con un buscador de todo lo publicado (ADR 0061) | El revisor busca cada nombre y cada titular en lo ya publicado. |
| **Nadie acapara el número**: como norma, un artículo por persona y dos por producto o empresa. | El agente que redacta | El revisor. |
| **Si un día no da para un número digno, no se rellena**: entonces salen artículos guardados. | El que redacta y la reserva | — |
| **La opinión, aparte y firmada.** Solo la columna del miércoles toma partido: va en la sección «Opinión», con la firma del modelo que la escribe y una nota que dice que el diario comprueba sus datos y que la opinión es del modelo. Discute ideas, no personas: nadie de los grupos sale nombrado. | El columnista; la firma y la nota las pone el programa que monta la web (ADR 0092) | El verificador comprueba cada dato y que no se reconozca a nadie, sin tocar la tesis; un programa, la medida y los enlaces. |

## 2. Quién hace cada cosa

Los agentes son modelos de IA de Claude, de Anthropic: Sonnet escribe y revisa cada día, Opus elige el
mejor reportaje y la mejor columna, escribe los textos largos y repara lo que falla, y Fable escribe y elige la viñeta.
La excepción es el columnista de los miércoles, GPT-6.2-Astra, de OpenAI: la opinión viene de otra voz que la del
resto del diario y la firma con su nombre (ADR 0092). **Los
agentes que escriben el diario no pueden ejecutar programas**: solo leen y escriben textos y consultan
internet. Así, nada de lo que llega en los mensajes de los grupos, que escriben otras personas, puede
llevarlos a hacer otra cosa (ADR 0002). Los mensajes son material para informar, nunca órdenes.

Solo el reparador trabaja con programas. No escribe nada del diario: actúa cuando algo falla, busca la
causa y la arregla en una copia. No puede cambiar el texto de los artículos ni de la viñeta, ni publicar, y
un programa comprueba su arreglo antes de aplicarlo (ADR 0087).

**Ningún agente revisa lo que ha escrito él mismo.** Cada texto pasa por un revisor que no lo ha
escrito, que abre cada fuente y quita lo que no puede confirmar (ADR 0001).

| Agente | Qué hace |
| --- | --- |
| Redactor y revisor | Los artículos y breves del día. |
| Documentalista y revisor | Los artículos de la Biblioteca, del Repositorio y los guardados de EduMedia. |
| Ilustrador y revisor de dibujos | Un dibujo que explica cada artículo; el revisor lo mira en su página y le devuelve el que no se entiende (ADR 0005). |
| Guionista y juez de humor | Cinco guiones para la viñeta; el juez elige uno (ADR 0023 y 0024). |
| Cronista y verificador | «Hace un año». |
| Columnista, verificador y juez de la columna | La columna de opinión del miércoles; el juez elige entre la nueva y la de reserva (ADR 0092). |
| Jefe de reportajes, reportero, verificador y juez de reportajes | El reportaje del domingo. |
| Comentarista y revisor | El comentario de la semana. |
| Guionista de vídeo | «La semana en vídeo». |
| Traductores | Uno por idioma, para cada texto. |
| Reparador | Cuando algo falla, lo arregla para que el número salga; no escribe ni cambia los textos. |
| Portavoz | Los avisos de cada mañana en los tres grupos y el texto para Instagram. |

Todos escriben con el [libro de estilo](../encargos/estilo.md), y cada tarea tiene además su propia guía.

## 3. Un día en el diario

Un programa mira cada cinco minutos qué toca hacer y apunta lo que ya ha hecho, para no repetir nada. Las horas son
peninsulares españolas: UTC+1 en invierno y UTC+2 en verano.

| Hora | Qué pasa |
| --- | --- |
| 1:00 | Se prepara el número con lo que se habló el día anterior: los artículos y su revisión, los dibujos, la viñeta, la Biblioteca, el Repositorio, «Hace un año», las comprobaciones, las traducciones y los avisos. Si falla, se intenta una segunda vez. |
| 5:00 | El número ya se puede ver antes de publicarlo, para que la persona supervisora lo revise (ADR 0025). Un programa comprueba que la página se vea bien en pantallas de distintos tamaños. |
| 6:30 | Si el número aún no está hecho, se para y sale con lo que haya o con artículos guardados. |
| 6:50 | Se publica la web y se preparan las imágenes para compartir cada artículo y los avisos de los grupos. Si algo falla, se vuelve a intentar cada 10 minutos hasta las 9:00. |
| 7:00 | El Bot de IA Educativa publica el aviso del número en cada grupo y escribe por privado a las personas cuyo recurso sale ese día (ADR 0052). La aplicación del diario para Android avisa del número nuevo (ADR 0043). |
| 7:05 | El número sale en Instagram (ADR 0015). |
| Hacia las 7:10 | La persona supervisora recibe un informe: qué ha salido, si se han usado artículos guardados y qué ha fallado (ADR 0069). |
| 8:00 | Se escribe un artículo nuevo para guardar, si hacen falta, y una columna de opinión de reserva, si no queda ninguna. |
| 9:00, domingo | «La semana en vídeo», con el reportaje al final, sale en Instagram, X, Bluesky y LinkedIn (ADR 0027). |
| Desde las 9:10 | Un programa que funciona aparte, en GitHub, comprueba que el número ha salido y, si no, lo publica con artículos guardados. Si el diario no responde, lo comprueba ya desde las 7:30 (ADR 0021). |
| Noche del martes | Con el número del miércoles se prepara la columna de opinión (ADR 0092). |
| Miércoles | Se buscan en lo publicado los enlaces que han dejado de funcionar (ADR 0056). |
| Al publicar | Se guarda una copia de cada número en el archivo de Internet Archive (ADR 0046). |

## 4. Ningún día sin número

**Siempre sale un número** (ADR 0021 y 0068). Si la preparación falla dos veces, o a las 6:30 no ha
terminado, sale con artículos guardados, todos o solo los que falten. Si la publicación falla, la hace
el programa que funciona aparte, en GitHub, y el diario no la vuelve a hacer encima.

**Lo que no salió por un fallo sale al día siguiente**: si un número salió con artículos guardados
porque falló la preparación, la noche siguiente se recoge también lo que se habló ese día, y la web lo
dice.

**Si un agente estropea un archivo del número**, se recupera la versión anterior y el agente repite su
trabajo una vez. Y si la preparación tiene que empezar de nuevo, no da por publicado lo que se escribió
en el primer intento (ADR 0076).

## 5. La reserva: artículos guardados para los días sin noticias

El diario tiene escritos de antemano artículos y otras piezas, para que nunca falte un número (ADR 0068):

| Qué | Cuántos | Se retira si no se usa en | De dónde sale |
| --- | --- | --- | --- |
| Artículos | Seis: dos de cada grupo | 60 días; los de EduMedia, 30 | Aplicaciones del Repositorio y documentos de la Biblioteca que el diario aún no había tratado, y herramientas compartidas tiempo atrás en EduMedia-IAG (ADR 0077) |
| Viñeta | Una | 60 días | Un chiste sobre un tema que no pasa de moda |
| «Hace un año» | Los de las siete noches siguientes | Esa misma noche | Se escriben por adelantado |
| Reportaje | Uno por semana | 28 días | Sobre un tema que no pasa de moda (ADR 0028) |
| Columna de opinión | Una | Se usa o se descarta el miércoles siguiente | Sobre un debate que no depende de unos días; el juez la compara con la nueva y sale la mejor (ADR 0092) |

- **Cuándo se usan**: cada noche, si el número no llega a tres artículos o le falta algún grupo, y
  siempre que falla la preparación. Primero, los de los grupos que faltan.
- **Cómo se reponen**: cada mañana se escribe uno del grupo que tenga menos guardados. Pasa por
  documentalista, revisor, ilustrador y traductores, como cualquier artículo.
- **Antes de usar uno**, un programa comprueba que la página de lo que trata sigue abierta; si no, se
  retira.

## 6. Las revisiones

**Con IA**: el revisor de cada tarea (fuentes, cifras, nombres y lo ya publicado), el revisor de dibujos,
el juez de la viñeta, el verificador del reportaje, de «Hace un año» y de la columna de opinión y, cada noche, un corrector de estilo
que lee los artículos del día como un lector cualquiera y arregla lo que cuesta entender, sin tocar los
datos (ADR 0083).

**Con programas, sin IA**, cada noche:

| Qué se comprueba | Registro de la decisión |
| --- | --- |
| Que ningún agente haya estropeado los archivos del número | ADR 0076 |
| Que no se use «quien» con el sentido de «la persona que» ni haya citas solo en inglés, «hoy» o «ayer», «app» u otras palabras que el libro de estilo desaconseja (si las hay, un agente las corrige) | ADR 0067 y 0083 |
| Que el corrector de estilo no haya cambiado ninguna cifra, enlace ni cita | ADR 0083 |
| Que no se atribuya a un autor del diario algo de otra persona que se llama igual (si pasa, un agente lo revisa) | ADR 0066 |
| Erratas que siguen una regla fija, como «y» delante de «i», y titulares demasiado largos | ADR 0059 |
| Que cada traducción tenga los mismos artículos, enlaces y dibujos que el original; si no, esa parte sale en castellano | ADR 0026 |
| Que no se haya quedado nada en castellano en una traducción | ADR 0056 |
| Que ninguna página tenga huecos en blanco, en pantallas de cualquier tamaño | ADR 0041 |
| Enlaces que han dejado de funcionar, los miércoles | ADR 0056 |

**Una persona** puede revisar el número a las 5:00 y pedir cambios antes de las 6:50, pero el diario no
lo promete: si no hay respuesta, sale a su hora (ADR 0058).

## 7. Lo que sale a partir de cada número

El número no es solo la web. A partir de él salen también:

- los **avisos en los tres grupos** y los **mensajes privados** a las personas cuyo recurso aparece;
- la **publicación en Instagram**, con su texto;
- la **imagen para compartir** cada artículo;
- el domingo, **«La semana en vídeo»** en las redes sociales.

**Si algo cambia en un número antes de que salga, se rehace todo lo que depende de ello**: si cambia la
viñeta, el aviso que habla de ella; si cambia un titular, su imagen para compartir; si cambia el
reportaje, el vídeo de la semana y sus textos.

## 8. Correcciones

- **Un dato equivocado se corrige en el artículo, con una nota al final** y en los cinco idiomas (ADR
  0055): «Corregido el…» (había un error), «Actualización del…» (el dato era cierto y ha cambiado) o
  «Nota añadida el…» (faltaba algo). Una errata que no cambia el sentido se corrige sin nota.
- Antes de corregir, se comprueba el dato en su fuente: un aviso de error también puede estar equivocado.
- **Un aviso que ya se ha enviado a un grupo se corrige** editándolo con el bot.

## 9. Personas, privacidad y transparencia

- **Para saber quién es cada persona se mira su cuenta de Telegram, no el nombre que muestra**, porque
  dos personas pueden llamarse igual (ADR 0066).
- **Solo se nombra al autor de un recurso que él mismo ha publicado**; las opiniones de los grupos no se
  atribuyen a nadie (libro de estilo). La única opinión propia del diario es la columna del miércoles, firmada
  por el modelo que la escribe (ADR 0092).
- **No se recoge nada de los lectores**: el contador de visitas solo suma, sin cookies ni datos
  personales (ADR 0033), y los comentarios solo se cargan si el lector pulsa el botón (ADR 0030). Lo
  explica la [política de privacidad](https://diarioiaeducativa.github.io/privacidad.html) (ADR 0070).
- **Un solo aviso de que el diario está hecho con IA**, en el pie de todas las páginas. La página [«La
  redacción»](https://diarioiaeducativa.github.io/redaccion.html) explica cómo se hace, quién responde de
  lo publicado y que no hay publicidad ni patrocinio (ADR 0055 y 0065).
- Los programas que hacen el diario son públicos (ADR 0019).

## 10. Lo que falta por mejorar

Lo que todavía no funciona del todo bien o depende de una sola comprobación. Es por donde se puede
mejorar el diario:

- **Una corrección no llega sola a lo que ya se ha enviado.** Si se corrige un artículo después de
  publicarlo, el aviso que ya salió en los grupos hay que cambiarlo a mano, y lo publicado en Instagram
  y en las otras redes no se cambia.
- **Los artículos de EduMedia guardados para los días sin noticias del grupo** se empezaron a escribir
  el 16 de noviembre de 2026: todavía no ha salido ninguno en un número.
- **Un artículo guardado se revisa poco antes de publicarse.** Se escriben con días o semanas de
  antelación, y justo antes de usar uno solo se comprueba que la página de la herramienta de la que
  habla sigue abierta, no si ha cambiado algo de lo que cuenta, por ejemplo si ha dejado de ser
  gratuita. Por eso los de EduMedia, sobre herramientas que cambian a menudo, se retiran al mes.
- **Mientras se escribe un artículo para guardar**, la web que se está preparando lo muestra durante
  unos minutos como si fuera un número del diario. Si justo entonces se publicara la web, saldría.
- **Si un agente estropea un archivo, se recupera solo en la preparación de cada noche**, no en la del
  reportaje, la Biblioteca o el Repositorio.
- **Las traducciones las comprueba un programa**, que mira que estén todos los artículos y que no haya
  quedado nada en castellano, pero ningún agente las revisa.
- **Cuándo se considera que un día tiene pocas aplicaciones nuevas del Repositorio**, y se rescata una
  anterior, se decidió a ojo y está por ajustar.
- **Instagram se intenta una sola vez**: si falla, hay que publicarlo a mano.
