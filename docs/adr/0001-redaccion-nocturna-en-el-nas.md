# 1. Redacción nocturna en el NAS

Fecha: 2026-11-02 · Estado: aceptado

## Contexto

El diario tiene que salir solo cada mañana. El número 1 (01-11-2026) se hizo a mano en una
sesión de Claude Code en el portátil: los agentes se lanzaron uno a uno y el sitio se subió
desde allí. Los mensajes de los grupos ya los guarda el Bot de IA Educativa en el NAS
(`bot-chatgpt-ia-edu/repo/datos/<grupo>/mensajes.jsonl`), y el bot publica a las 7:00 los
avisos que encuentra en `datos/diario/<fecha>.json` (ADR 0025 del bot).

## Decisión

- Un contenedor propio, `diario-ia-educativa`, con la imagen del boletín semanal (que ya
  trae Claude Code, Python y git) y el mismo token de un año de Claude de los demás
  contenedores con agente: no añade ningún pago.
- `nas/reloj.sh` mira cada cinco minutos qué toca: desde la 1:00, `scripts/noche.sh`
  prepara el número con las conversaciones de ayer (dos intentos como mucho); a las 6:30,
  si no está, avisa a Juanjo por Telegram; desde las 6:50, `scripts/publicar-nas.sh` lo
  publica, para que el sitio ya esté en línea cuando el bot avisa a las 7:00. Hasta el
  07-11-2026 era a las 6:55: ese día el NAS subió el número a las 6:56 y a las 6:57 GitHub Pages
  aún estaba desplegando, con las páginas nuevas en 404; Juanjo pidió adelantarlo («10 minutos en
  lugar de 5, por si github va lento»). Lo decidido
  queda en `estado/`, así que un reinicio no repite nada; y si `estado/` se pierde (al
  restaurar en otra máquina), un número cuya edición ya está en GitHub no se rehace.
- Los siete agentes de la redacción, con los encargos de `encargos/` y el modelo fijado por
  su nombre exacto: redactor, revisor, ilustrador, traductor y autor de los avisos con
  Sonnet 5.5 (`claude-sonnet-5-5`); guionista y juez de humor con Opus 5.5
  (`claude-opus-5-5`), que ganó la prueba a ciegas del 01-11-2026. Los que no dependen
  entre sí trabajan a la vez.
- **Redactor y revisor son dos agentes distintos** (`encargos/pasos/1-redaccion.md` y
  `1-repaso.md`): el redactor deja su borrador en `ediciones-borrador/` y el revisor, en una
  sesión aparte que no ha escrito nada, abre cada fuente y deja la versión final en
  `ediciones/`. Hasta el 02-11-2026 los dos pasos iban en la misma sesión, con la instrucción
  de repasar «como un editor distinto», lo que no casaba con lo publicado en «La redacción»
  («no ha escrito nada»); se separaron ese día, antes del número 2. Si el borrador dice que no
  hay número, no hay nada que repasar y pasa tal cual.
- Lo imprescindible es la edición: cada paso (borrador y repaso) se reintenta una vez y, si
  falta, no hay número. Sin repaso no se publica el borrador. Lo demás se
  degrada sin parar nada: sin viñeta válida, sale sin viñeta; sin traducción, la edición
  catalana usa el castellano (`generar.py`); sin avisos, el bot no anuncia.
- Lo que escriben los agentes se guarda en este repositorio (`diarioiaeducativa/periodico`)
  y el sitio en `diarioiaeducativa.github.io`, cada uno con su clave de despliegue. Los
  mensajes de `dias/` no se suben. Cada commit lleva su nota `refs/notes/ia` con los modelos.
- Avisos entregados al bot solo después de subir el sitio, para que nunca anuncien un número
  que no está.

## Alternativas descartadas

- **Dentro del contenedor del boletín**: comparte imagen, pero mezclaría un proceso diario
  con uno semanal que ocupa la madrugada del lunes, y un fallo de uno pararía el otro.
- **En el portátil**: depende de que esté encendido de madrugada.
- **Publicar a las 7:00 en punto, como se pensó al principio**: GitHub Pages tarda un
  minuto en servir lo nuevo y el aviso del bot saldría apuntando al número anterior.

## Consecuencias

- Mientras se trabaje en el código en el portátil, hay que hacer `git pull` antes, porque el
  NAS sube cada mañana lo que escriben los agentes.
- `noche.sh` trae lo último con `git pull` al empezar; si el pull cambia el propio `noche.sh`,
  se relanza una vez con la versión nueva (`NOCHE_RELANZADO`), porque bash ya ha leído el
  viejo y lo ejecutaría con los encargos nuevos. Se vio el 02-11-2026 al separar redactor y
  revisor: sin esto, esa noche no habría habido número.
- Tope de 2 GB de memoria y 1,5 núcleos para el contenedor: tres agentes a la vez caben, y
  no puede llenar el swap del NAS como pasó el 01/02-11-2026.

## Riesgos y limitaciones

- Nadie revisa el número antes de publicarse: el repaso del segundo agente es la única
  revisión. Por eso el revisor no es el redactor y abre cada fuente.
- Si el token de Claude caduca (05-10-2027), no hay número; el vigía del NAS avisa antes.

## Validación

Prueba completa en el NAS el 02-11-2026, con las conversaciones del 01-11 en una copia y sin
publicar: los siete agentes terminaron en 6 minutos (redacción y repaso, 2 min 18 s) con tres
piezas, dos breves, cuatro ilustraciones, viñeta elegida, traducción y avisos. Registro en
`/volume1/docker/diario-ia-educativa/registro-pruebas/2026-11-02-prueba-completa.log`. Sacó a
la luz dos fallos, ya corregidos: `sitio/` no existe en un clon nuevo, y los archivos fijos
del sitio (estilos, fuentes, iconos) solo vivían ahí, así que publicar desde el NAS los habría
borrado; ahora están en `estaticos/`. El acceso a GitHub se comprobó con `git push --dry-run`
en los dos repositorios, y los permisos de los agentes, con un agente que intentó leer el home
y `/proc`, usar Bash y escribir fuera: todo denegado (ADR 0002).

Redactor y revisor separados, probados el 02-11-2026 en una copia aparte con las
conversaciones del 01-11, sin publicar: borrador en 1 min 43 s y repaso en 1 min 19 s. El
revisor, que no había escrito nada, corrigió ocho cosas del borrador (una cifra atribuida a
quien no la dio, una conclusión que nadie formuló en el grupo, «cuatro pasos» donde la fuente
da cinco, un «ya exige» que la documentación pone en futuro) y retiró un enlace que no pudo
abrir.
