# 87. Un agente reparador para cualquier fallo

Fecha: 2026-11-17 · Estado: aceptado

## Contexto

Cuando algo fallaba, el diario avisaba por Telegram y seguía con un plan B: unos 40 avisos distintos
repartidos por `nas/reloj.sh`, `scripts/noche.sh` y otros programas. El aviso llegaba de madrugada y el
arreglo esperaba a que alguien abriera una sesión. El 17-11-2026, una pieza de la reserva con el cuerpo
mal formado dejó sin traducir el número en las cuatro lenguas y rota su página en castellano; el aviso
salió a la 1:16 y se arregló a mano a las 5:45, una hora antes de publicar (ADR 0026 y 0077). El 15-11-2026,
una edición con el JSON roto hizo fallar al generador y la noche acabó sin número (ADR 0076).

Los programas cubren los fallos que ya se conocen. Lo que hacía falta para los que no están previstos es
alguien que diagnostique, y eso es lo que hizo una sesión con un agente el día 17. Se decidió que lo haga
un agente dedicado, para cualquier error y no solo el de las traducciones, y con Opus.

## Decisión

**Una sola puerta.** Lo que falla ya no se avisa directamente: se pasa a `scripts/reparador.py incidencia
"qué ha fallado"`. Entran por ahí los avisos de fallo de `reloj.sh` (el plan B, la vista previa, la
publicación, la reserva vacía, Instagram, el permiso de Instagram, la web de la semana), los de `noche.sh`
(sin número, el reportaje, la autoría dudosa, las traducciones quitadas, el castellano colado) y el de los
dibujos retirados. Además:

- cuando `noche.sh` acaba mal y sin número, `reloj.sh` abre una incidencia con `--bloqueo` y el segundo
  intento de la noche espera a que el reparador acabe;
- al terminar bien, `noche.sh` le pasa con `--sin-aviso` los AVISO y ERROR que haya dejado en su
  registro, que antes no veía nadie hasta el informe del día; y `reloj.sh`, los huecos de la maqueta.

Lo que solo informa (la vista previa lista, «ya está publicado», el informe del día) sigue yendo directo.

**El agente.** `reparador.py atender` (lo lanza la propia incidencia, aparte, y uno solo a la vez) espera a
que la noche acabe, junta las incidencias pendientes y lanza Claude Code con **Opus 5.5**
(`claude-opus-5-5`, por su nombre exacto; `MODELO_REPARADOR`), con terminal, en **una copia** de la
redacción (`/tmp/reparador/copia-…`, sin el sitio, el historial de git ni las imágenes de Instagram), con
`encargos/reparador.md`, las incidencias y las medidas del número. Su tope es de 45 minutos y, antes de
publicar, el tiempo que quede hasta las 6:40 (hasta las 6:25 si el número no está preparado, porque el
plan B salta a las 6:30). Con menos de 15 minutos no empieza: el aviso sale en el momento, el número
sale con lo que haya y el arreglo se hace después de publicar.

**Lo comprueba un programa, no el agente.** Antes de tocar el número, `reparador.py` comprueba en la copia:

1. que no ha cambiado nada de lo protegido: el propio reparador y su encargo, lo que publica o envía
   (`publicar-nas.sh`, `publicar-web.sh`, `instagram.py`, `redes/`, `avisos-personas.py`, el vigilante) y
   lo que corre fuera del contenedor (`nas/`, `.github/`, `ionos/`, `android/`);
2. que el texto que escribió la redacción es el mismo, palabra por palabra: antetítulo, titular,
   entradilla, cuerpo, breves y bocadillos de la viñeta del día (puede cambiar su forma, no su contenido);
3. que el código cambiado se puede leer (Python, Bash, JSON) y los JSON del día valen;
4. que el generador funciona y que ninguna medida ha empeorado (`reparador.py medir FECHA`: JSON rotos,
   traducciones que faltan o no valen, castellano colado, estilo, huecos de maqueta).

Si algo no se cumple, no se aplica nada. Si se cumple, lleva a la redacción solo los archivos cambiados,
y solo si allí no han cambiado mientras tanto; lo que es código lo guarda en git, con el motivo y la nota
del modelo, y lo sube. Después, según el momento: con el número sin preparar, deja que la noche se repita
(con un intento más si ya había gastado los dos); con el número preparado, rehace el sitio; con el número
ya publicado, vuelve a publicar la web (`publicar-web.sh`). El agente no publica nada: si hay que repetir
la publicación, Instagram o la reserva, lo pide y el programa le quita al reloj la marca de «ya intentado».

**Las traducciones las hacen los traductores de la noche, no el reparador.** Dentro de la sesión del agente
no se puede lanzar otro agente: Claude Code no pasa su permiso a las órdenes que ejecuta. El agente arregla
el original y pide en su informe qué hay que traducir (`traducir`); el programa lanza `traducir-dia.sh` en
la copia, con su comprobación, antes de juzgar el arreglo.

**Un solo mensaje, después.** Arreglado: qué fallaba, qué se ha hecho y si el número sale a su hora. Sin
arreglo (no puede, no pasa la comprobación, se le acaba el tiempo o no arranca): el aviso de siempre, con
el diagnóstico. Si lo que había era solo una línea del registro y no hay nada que arreglar, nada. Todo
queda en `registro/reparador.jsonl` y en `registro/reparador-<id>.log`, y el informe del día lo cuenta.

Cada incidencia se atiende una vez: no hay bucles. `REPARADOR=0` o `estado/reparador/apagado` lo
desconectan y los avisos salen como antes; si el propio programa falla, también.

## Alternativas descartadas

- **Solo más programas** (reintentos y comprobaciones): se han añadido para lo de las traducciones
  (ADR 0026), pero no cubren lo que nadie ha previsto.
- **Un reparador solo para las traducciones**: el fallo del 15-11-2026 era de otro tipo, y el siguiente
  será de otro.
- **Dejar que el agente trabaje sobre el número de verdad**: un arreglo a medias a las 6:45 sería peor
  que el fallo. Por eso la copia y la comprobación.
- **Fable 5.2**, que se propuso por ser quien había diagnosticado el fallo del día 17: se eligió Opus.
- **Que no pueda tocar el código**: «cualquier error» incluye los del programa.

## Consecuencias

- Los avisos de fallo llegan más tarde y resueltos, o como antes si no hay arreglo. Lo que no dependía de
  la IA sigue igual: el número de reserva de las 6:30 y el vigilante de GitHub (ADR 0021 y 0028).
- Gasta de la misma suscripción solo cuando hay fallo; sin coste nuevo. En los doce días anteriores hubo
  avisos tres noches.
- Es el único agente con terminal (excepción al ADR 0002). «Cómo se hace el diario» lo dice.
- Un aviso de fallo nuevo se manda con `incidencia`, no con `avisar-juanjo`.
- El texto de «La redacción» sigue hablando de los 16 agentes que hacen el diario; el reparador no
  escribe nada y no se ha añadido a esa cuenta ni al organigrama.

## Riesgos y limitaciones

- **Si falla Claude o se agota la suscripción, el reparador tampoco arranca**: quedan la reserva y el
  vigilante, y el aviso sale como antes.
- **Un agente con terminal puede leer lo que hay en el contenedor**: las claves de despliegue están en
  el disco y el token de Claude, en el entorno del proceso que lo lanza. Claude Code no pasa ese token a
  las órdenes que el agente ejecuta (comprobado en el contenedor: la variable llega vacía), y se le lanza
  con otra carpeta personal y sin poder avisar a nadie; su encargo le dice que los textos que lea no son
  órdenes. Nada de eso es una barrera para un agente que se empeñe.
  Lo que lo acota: no trabaja con los mensajes de los grupos sino con los artículos ya escritos y
  revisados, solo corre cuando algo falla, tiene un tope de tiempo, y nada de lo que cambie llega al
  número ni a git sin pasar la comprobación.
- La comprobación mide lo que el diario ya sabe medir. Un arreglo puede pasarla y no ser el mejor: por
  eso llega siempre el mensaje con lo que se ha hecho, y el registro guarda lo que cambió.
- Lo que pide juicio (una autoría dudosa, un chiste que no se entiende) no lo resuelve: lo dirá y
  llegará el aviso.
- Con la edición en castellano rota antes de empezar no hay texto con el que comparar: ahí la
  comprobación del texto no actúa.

## Evidencia

- El fallo del 17-11-2026: `registro/2026-11-16.log` del NAS (las cuatro traducciones quitadas a la
  1:13 y el aviso de la 1:16) y el ADR 0026. El del 15-11-2026: `registro/2026-11-15.log`
  (`JSONDecodeError` en `cargar()` y «ERROR: el generador falla con la edición nueva»).
- Los avisos que había: `grep avisar-juanjo` en `nas/reloj.sh` y `scripts/` antes de este cambio.
- En el contenedor del NAS, Claude Code responde con el modelo pedido y el permiso de Claude está en
  una variable de entorno, así que el agente puede lanzarse con otra carpeta personal.

## Validación

Con un agente simulado, en una copia, nueve casos: un arreglo bueno se aplica; no se aplica si reescribe
un titular, si toca la publicación o si deja el generador sin funcionar, y llega el aviso de siempre con
el motivo; «nada que arreglar» reenvía el aviso si lo había y calla si solo era una línea del registro;
«no se puede» y el agente que se cae avisan con el diagnóstico; un arreglo de datos y de programa se aplica.

Con el agente de verdad (Opus 5.5), en una copia local con los archivos del 17-11-2026:

- **El fallo del 15-11** (la edición con unas comillas sin escapar, el generador parado y la noche sin
  número): lo arregló sin cambiar el texto y rehízo las dos traducciones que faltaban, en 4 min 45 s.
  La comprobación lo dio por bueno (de un JSON roto y el generador parado, a cero problemas) y el
  número de prueba quedó listo para repetir la noche.
- **Un dato que para al programa** (las fuentes de un artículo, vacías): 58 s. Devolvió las fuentes al
  artículo, corrigió el generador para que no se pare con ese dato y el cambio quedó en git con su
  motivo y la nota del modelo. Como la noche había gastado sus dos intentos, se le dio uno más.

Lo que enseñaron esas pruebas y se corrigió: con el número roto de partida, las medidas de antes no
valen para comparar (un primer arreglo bueno se rechazó por eso); el agente dejó una orden esperando sin
fin (`tail -f`) y hubo que cortarla, y cambió el programa para prevenir, más allá de lo necesario. El
encargo le prohíbe ahora las órdenes que no acaban y le pide tocar el programa solo si sin ese cambio
el número no sale; lo demás lo apunta como pendiente.

Y **dentro del contenedor del NAS**, el 17-11-2026 a las 6:56, con el número ya publicado y sobre una
copia en la que se repitió el fallo de ese día (el artículo con el cuerpo en un texto y las cuatro
ediciones sin traducir): arreglado en 2 min 56 s; de 4 traducciones que faltaban y 80 textos en
castellano, a 0 y 2 (el título oficial de una guía), con la maqueta medida antes y después. En esa prueba
el agente no pudo lanzar a los traductores («Not logged in») y tradujo él mismo: de ahí que ahora las
traducciones las pida y las haga el programa.

Repetida a las 7:03 con ese cambio: el agente partió el artículo en sus párrafos y pidió las traducciones
(59 s); el programa lanzó a los traductores de la noche (3 min 36 s) y la comprobación lo dio por bueno,
con las mismas medidas: de 4 traducciones que faltaban y 80 textos en castellano, a 0 y 2. En total, seis
minutos.
