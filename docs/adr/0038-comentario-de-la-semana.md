# 38. El comentario de la semana, uno general y uno de cada grupo

Fecha: 2026-11-09 · Estado: aceptado

## Contexto

La página de cada semana (ADR 0034) lista unas 40 piezas por titular, con el pódcast y el vídeo de
NotebookLM de cada grupo, pero no dice qué fue lo importante: quien no ha leído los números tiene que
deducirlo de la lista. Juanjo pidió (09-11-2026) un comentario que lo destaque, después del vídeo y el
pódcast, con una longitud mínima, y que fuera uno por grupo, con uno general si se quería.

## Decisión

- **Cuatro comentarios por semana**: el general, de las tres comunidades, que se ve con «Todos»; y uno de
  cada grupo con piezas esa semana, solo con lo suyo, que sustituye al general al elegir ese grupo en el
  selector (que es como llega cada grupo desde su aviso, con `?grupo=`). El reportaje no es de ningún
  grupo: solo va en el general.
- **Medida**: de 150 a 250 palabras cada uno, sin contar las direcciones de los enlaces: da para tres o
  cuatro asuntos con su porqué, y se lee en un minuto. El de un grupo con una o dos piezas en la semana
  puede quedarse en 80, para no rellenar. Como mucho seis enlaces, todos a piezas de la semana (y del grupo,
  en el de cada grupo); ninguno externo, que ya están en cada pieza.
- **Quién lo hace** (`scripts/comentario-semana.sh`): la noche del domingo al lunes, con el número que
  cierra la semana, el redactor (Opus) lo escribe a partir de los titulares y entradillas de todas las piezas
  (`scripts/comentario_semana.py entrada`), el revisor (Sonnet, que no ha escrito nada) contrasta cada
  afirmación con su pieza, y el traductor lo pasa a los otros cuatro idiomas. Después de cada paso, un
  programa comprueba sin IA la medida, los enlaces y que cada grupo con piezas tenga el suyo; si no pasa, se
  repite el repaso una vez y, si sigue sin pasar, la semana sale sin comentario. Nunca impide el número.
- **Datos**: `comentario-semana/AAAA-WW.json` (y `comentario-semana-XX/` en cada idioma), con `general` y
  `grupos`; se publican con el número del lunes.
- **En la página**, debajo del pódcast y el vídeo, con el mismo filete, y una línea que dice que lo escribe
  un agente de IA y que otro lo contrasta con cada pieza. El rótulo dice de quién es: «Lo más importante de la
  semana» con todos los grupos y «Lo más importante de la semana en ChatGPT-IA-edu» (o el grupo que sea) al
  elegir uno.

## Alternativas descartadas

- **Un solo comentario para toda la semana**: fue la primera versión, pero quien elige su grupo veía sobre
  todo lo de los otros (el de la semana 45 no decía nada de EduMedia-IAG).
- **Un agente por comentario**: cuatro redactores y cuatro revisores para textos cortos; uno solo escribe
  los cuatro y así puede evitar que el de un grupo repita el general.
- **Escribirlo a partir de los mensajes**: eso ya lo hacen el pódcast y el vídeo, con la conversación
  completa; el comentario destaca lo que el diario contó y lleva a sus piezas.

## Consecuencias

- Tres agentes más la noche del domingo (unos cinco minutos en la prueba), sin coste nuevo.
- Las semanas anteriores a la 45 no tienen comentario: la página sale como antes.
- «La redacción» presenta al comentarista en el texto del equipo y en el organigrama, en una fila que sale
  de los números de la semana y pasa por el revisor y el traductor hasta el resumen semanal.

## Validación

Semana 2026-45 generada en una copia aparte (`scripts/comentario-semana.sh 2026-45`): cuatro comentarios de
173 a 232 palabras, el repaso corrigió dos afirmaciones que no estaban en las piezas y la comprobación pasó;
traducciones en los cuatro idiomas. Página probada con `probar-web` en Chromium y Firefox, escritorio y
móvil, claro y oscuro, con «Todos» y con un grupo elegido: sin errores ni desbordamiento.
