# 78. Libro de estilo común para los agentes

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

Cada tarea del diario tiene su guía en `encargos/` (redacción, biblioteca, repositorio, reportaje,
avisos, viñeta, vídeo, ilustraciones, enlaces y fondo de EduMedia: unas 11.000 palabras) y 41
encargos cortos por paso. Las normas de estilo estaban copiadas en cada guía, con diferencias: el
apartado «Estilo» se repetía en cinco guías, la norma del «quien» relativo y la de las citas en
inglés (15-11-2026) se habían pegado en seis, y otras (no decir «pieza» al lector, no decir que el
diario «cuenta» algo) no estaban en ninguna. Una norma nueva había que añadirla en cada sitio, y
para saber cómo escribe el diario había que leerlas todas.

Juanjo pidió el 16-11-2026 una guía de estilo («cómo escriben los agentes y qué deben tener en
cuenta») y un documento aparte con las normas del diario, para conocer cómo se elabora y poder
mejorarlo.

## Decisión

- **`encargos/estilo.md` es el libro de estilo**: lo común a todo lo que lee el público (tono,
  lengua, titulares, personas, rigor, citas, enlaces, forma, traducciones y lo que se comprueba sin
  IA). Lo leen todos los agentes que escriben, revisan, traducen o resumen, y las personas.
- **Cada guía empieza remitiendo a él** («Antes de nada, lee `encargos/estilo.md`») y se queda solo
  con lo propio de su tarea (medidas, formato, el tono de los avisos, la viñeta). Los encargos de paso
  que no tienen guía propia (comentario de la semana, «Hace un año», repasos y traducciones) lo
  citan directamente.
- **Una norma de estilo nueva se escribe solo allí.** Si no vale para una tarea, lo dice la guía de
  esa tarea.
- Las normas de los idiomas siguen en `scripts/idiomas.py`, que es lo que recibe cada traductor; el
  libro las resume y remite a él.
- Lo que no es estilo (qué es noticia, cómo se compone el número, la reserva) va en
  `docs/como-se-hace.md`.

Al juntarlas se añadieron como normas comunes las que ya eran práctica o criterio de Juanjo:
«artículo» y no «pieza» ante el lector (ADR 0065), «publica» o «recoge» y no «cuenta» (Juanjo,
14-11-2026), comillas españolas, el porcentaje con espacio, nada de cómo funciona el diario por
dentro en lo publicado y nada que dependa del día en lo que se guarda para otro.

## Consecuencias

- Una sola fuente: lo que se lee en el libro es lo que aplican los agentes.
- Los agentes leen unas 1.600 palabras más por tarea.
- Las guías han perdido lo que repetían; si un agente empeora en algo, se mira primero si el libro
  lo dice con claridad.

## Validación

La primera noche con el libro (16 al 17-11-2026) se compara con las anteriores: que el número salga,
que los repasos sigan corrigiendo lo mismo y que no aparezcan «quien» relativos, «pieza» ni «el
diario contó» en lo publicado.
