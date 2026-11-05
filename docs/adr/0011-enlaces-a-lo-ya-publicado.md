# 11. Enlaces a lo ya publicado, continuaciones como breves y una pieza por grupo

Fecha: 2026-11-04 · Estado: aceptado

## Contexto

El número 3 salió con tres artículos. En la entrada había más: el mensaje de OpenAI sobre unir
las pestañas Chat y Work de ChatGPT, que el redactor descartó «sin fuente comprobable» sin
buscarla, y la explicación de cómo se usan las skills de motionvideo, que descartó porque la web
ya había salido el 02-11, aunque lo nuevo era el cómo. Juanjo, 04-11-2026: «si ya hay un artículo
anterior del tema, que lo enlace. Esto cada vez será más frecuente ya que el diario crece. Debe
ponerse enlaces a lo que está claramente relacionado».

## Decisión

- **Una norma común** (`encargos/enlaces.md`) para todo el que escribe (redacción, Biblioteca,
  Repositorio, reportaje): enlazar en el texto, donde se menciona, lo ya publicado que esté
  claramente relacionado (el mismo producto, documento, recurso, anuncio o debate, o lo que se
  continúa), con un texto que diga de qué trata. Como mucho tres por pieza y uno por breve.
- **Lo nuevo de un tema ya publicado sale como breve** que cuenta solo lo nuevo y enlaza la pieza
  anterior, en vez de descartarse.
- **Antes de descartar por falta de fuente, se busca** la oficial; `descartado` dice qué se buscó.
  El revisor la busca si el redactor no lo hizo.
- **Los agentes no escriben direcciones**: escriben `[texto](pieza:AAAA-MM-DD/id)` con las claves
  de `publicado.txt` (que ahora da una por pieza, también de la Biblioteca, el Repositorio y los
  reportajes) y `generar.py` lo convierte en el enlace a esa pieza en el idioma de la página. Si la
  clave no existe, queda el texto sin enlace: un error del agente no deja un enlace roto.
- **Al menos una pieza de cada grupo, si es posible** (04-11-2026, Juanjo: «hay que procurar que
  siempre haya al menos un artículo de cada grupo, si es posible. El más flojo suele ser edumedia,
  pero no siempre»). Si un grupo tiene algo publicable, lleva una pieza aunque sea corta (80-120
  palabras) en vez de quedarse en un breve; si solo tiene una continuación, la pieza cuenta lo
  nuevo y enlaza la anterior. Si no tiene nada, no se inventa y `motivo` lo dice. El revisor lo
  comprueba y puede convertir en pieza algo descartado de ese grupo que se pueda verificar.
- `publicado.txt` se rehace también tras el repaso, para que la Biblioteca, el Repositorio y el
  reportaje vean las piezas del mismo número. Los revisores comprueban que cada enlace lleva a una
  pieza que trata de verdad lo mismo.
- **La fecha que se cita es la de publicación** (05-11-2026, a raíz de la evaluación VCER). La
  clave lleva la fecha de las conversaciones y el número sale al día siguiente: dos piezas decían
  que el diario había contado algo «el 31 de octubre» y «el 2 de noviembre», cuando salió el 1 y
  el 3. `publicado.txt` pone ahora en el encabezado de cada día la fecha en que salió, y
  `encargos/enlaces.md` pide usar esa.

## Alternativas descartadas

- **Un bloque automático de «relacionados»** al final de cada pieza: ya existe «Más en esta
  sección», y decidir qué está claramente relacionado exige leer los textos. El enlace en el
  texto, además, dice por qué se enlaza.
- **Que los agentes escriban la dirección completa**: se equivocarían con el idioma y la
  profundidad de la página.

## Consecuencias

- Los números flojos tendrán más breves, cada uno con su enlace a la pieza que continúa.
- El umbral para tirar del Repositorio está en el ADR 0008 (4 piezas desde el 04-11-2026); se
  revisa con datos a principios de diciembre.

## Evidencia

- `ediciones/2026-11-03.json`, campo `descartado`, y `dias/2026-11-03.md` en el NAS.

## Riesgos y limitaciones

- Que el agente enlace por parecido de tema y no por relación clara: lo frena el revisor.

## Validación

- `generar.md()` con una clave existente (enlace a `/ca/2026-11-02/informe-mit-ia.html` en la
  página catalana) y una inexistente (queda el texto); `publicado.py` con piezas de las cuatro
  procedencias.
