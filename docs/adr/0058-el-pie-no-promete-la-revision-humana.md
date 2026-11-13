# 58. El pie no promete la revisión humana de cada número

Fecha: 2026-11-13 · Estado: aceptado

## Contexto

El ADR 0055, de esa misma mañana, dejó en el pie de todas las páginas «Redactado con IA a partir de las
conversaciones de los grupos y revisado por una persona antes de salir», y en «Las personas», que quien
mantiene la redacción «revisa cada número antes de que salga». Lo sostenía la vista previa de las 5:00
(ADR 0025).

Por la tarde se hizo una segunda revisión del diario, a ciegas: solo con lo publicado, sin conocer el
examen anterior ni la documentación del proyecto. Su hallazgo más grave fue que un lector no puede casar esa
frase con lo que la misma página cuenta:

- «Cómo se hace cada número» no tiene ningún paso humano: la vista previa no sale (es de la red de casa), y
  el texto dice que «un programa monta la web con todo lo anterior y la publica a las 6:50».
- La página explica vías por las que un número sale sin que nadie lo apruebe: la reserva y el vigilante de
  fuera del servidor (ADR 0021 y 0028).

El propio ADR 0055 lo anotaba en sus consecuencias: si un día el número sale sin esa revisión, la frase del
pie deja de ser cierta ese día. Y la vista previa nunca retiene el número: sin respuesta, sale a su hora
(ADR 0025).

Juanjo preguntó qué se perdía quitándola (13-11-2026: «que pasa si lo eliminamos? el diario pierde
rigurosidad?») y, vista la respuesta, lo encargó («haz el cambio»).

## Decisión

- **El pie dice quién escribe y quién revisa, sin prometer la revisión humana**: «Redactado y revisado por
  agentes de IA a partir de las conversaciones de los grupos». El resto de la frase no cambia. Sigue siendo
  un solo aviso de IA para todo el diario, en el pie (ADR 0055), y el mismo texto va en los créditos de la
  edición en papel.
- **«Las personas» dice quién responde, no qué hace cada mañana**: «La redacción la diseñó y la mantiene
  Juan José de Haro, que la supervisa y responde de lo publicado».
- **En los cinco idiomas a la vez**, en `generar.py` (castellano y catalán) y en `idiomas_web.py` (gallego,
  euskera e inglés).
- **La vista previa de las 5:00 sigue igual** (ADR 0025). Lo que cambia es que el diario ya no la promete.

## Alternativas descartadas

- **Mantener la frase y añadir la vista previa a «Cómo se hace cada número»**, que era la otra corrección
  que proponía la revisión. Habría obligado a revisar todos los números, y el diseño prevé que salgan sin
  esperar a nadie (ADR 0021 y 0025).
- **Quitar también que una persona responde de lo publicado**: es lo que da un responsable al lector y no
  depende de lo que pase cada madrugada.

## Consecuencias

- Deja de ser cierto el punto del ADR 0055 «lo que afirma La redacción obliga» en lo que toca a la revisión
  de cada número. Siguen obligando las otras tres cosas: una persona responde de lo publicado, no hay
  publicidad y, cuando una pieza trata del propio diario, lo dice.
- El ADR 0055 descartó un aviso de IA al inicio de cada pieza apoyándose en la excepción del artículo 50.4
  del Reglamento europeo de IA (revisión humana y responsabilidad editorial). Esa excepción depende de lo
  que se hace, no de lo que el pie dice, y lo que se hace no cambia. Pero el diario ya no la invoca ante el
  lector: lo que ofrece es el aviso, que está en todas las páginas.

## Evidencia

- Artículo 50 del [Reglamento (UE) 2024/1689](https://www.boe.es/buscar/doc.php?id=DOUE-L-2024-81079),
  leído el 13-11-2026: el apartado 4 obliga a hacer público que un texto que informa sobre asuntos de
  interés público se ha generado con IA, salvo que haya pasado por revisión humana o control editorial y
  una persona tenga la responsabilidad editorial; el apartado 5 pide que esa información se dé «de manera
  clara y distinguible a más tardar con ocasión de la primera interacción o exposición».
- Revisión a ciegas del 13-11-2026 sobre lo publicado: 760 páginas, las 83 piezas y los 25 breves en
  castellano, tres navegadores.

## Riesgos y limitaciones

- No se ha comprobado si un aviso en el pie de cada página basta como «claro y distinguible» en el sentido
  del apartado 5. Mientras la vista previa se siga revisando, la excepción del apartado 4 cubre al diario;
  si dejara de revisarse de forma habitual, habría que volver a mirar dónde va el aviso. Hipótesis
  pendiente de validación.
- Las traducciones del pie y de «Las personas» son de IA, sin revisión de un hablante.

## Validación

- `generar.py` sin errores en los cinco idiomas, en una copia aparte; ninguna página conserva la frase
  anterior en ningún idioma (búsqueda en todo el sitio generado).
- «La redacción» abierta en Chromium y Firefox, ordenador y móvil, sin errores ni desbordamiento; el pie y
  «Las personas», leídos en los cinco idiomas.
