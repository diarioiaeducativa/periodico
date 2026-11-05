# 19. El código de la redacción, público y con historial nuevo

Fecha: 2026-11-05 · Estado: aceptado

## Contexto

La evaluación VCER del 05-11-2026 dio un 1 en reutilización: el sitio generado era público, pero
el generador, los scripts de la noche y los encargos de los agentes estaban en este repositorio,
que era privado, y el README no explicaba cómo modificarlo. Juanjo aprobó hacerlo público ese
mismo día («hazlo todo»).

En lo que había no salían los mensajes de los grupos (`dias/` nunca se ha subido), los registros
ni las credenciales, pero varios ADR hablaban de la suscripción con la que trabajan los agentes,
y eso no se publica.

## Decisión

- **El repositorio `diarioiaeducativa/periodico` es público**, con licencia AGPL v3 para el
  código y CC BY-SA 4.0 para los textos e ilustraciones.
- **Antes, se limpió lo que no debe salir** (las menciones a la suscripción de los ADR 0001,
  0004, 0005, 0006, 0008 y 0009) y **se empezó un historial nuevo** con un solo commit, porque
  esas menciones seguían en los commits anteriores. El historial anterior, con sus notas
  `refs/notes/ia`, se guarda completo en el repositorio privado
  `diarioiaeducativa/periodico-historial`.
- **El repositorio público es uno nuevo con el mismo nombre.** Al cambiar la visibilidad, GitHub
  respondió con errores 500 y dejó el cambio «en curso» sin terminarlo, también desde la web.
  Se renombró ese repositorio a `diarioiaeducativa/periodico-bloqueado` (privado, con el mismo
  commit), se creó `diarioiaeducativa/periodico` público, se subió el historial nuevo con sus
  notas y la clave de despliegue del NAS pasó al nuevo (una clave solo puede estar en un
  repositorio). Las direcciones no cambian.
- **El clon del NAS se pone en el historial nuevo** con `git fetch` y `git reset --hard
  origin/main`: conserva las carpetas que no se suben (`dias/`, `estado/`, `registro/`…), que
  están en `.gitignore`.
- **«La redacción» enlaza el repositorio** en un apartado nuevo, «El código», y el README dice
  cómo cambiar el aspecto, los encargos y cómo probar una noche sin publicar.

## Alternativas descartadas

- **Una copia pública aparte, sincronizada con la privada**: dos repositorios que mantener para
  quitar unas pocas líneas.
- **Reescribir el historial quitando solo esas líneas** (`git filter-repo`): deja 130 commits
  con identificadores nuevos igualmente, y sus notas de modelo dejarían de corresponder.

## Consecuencias

- Cualquiera puede leer los encargos de los agentes. No les da más margen a quien quiera
  engañarlos con un mensaje en los grupos: los agentes no tienen terminal ni pueden escribir
  fuera de la carpeta de la redacción (ADR 0002), y siguen sin obedecer órdenes de los mensajes.
- Las notas `refs/notes/ia` empiezan de nuevo en el primer commit del historial nuevo; las
  anteriores están en `periodico-historial`.
- Lo que se suba a partir de ahora es público desde el primer momento: los ADR no hablan de
  suscripciones ni de cuentas personales.

## Evidencia

- Búsqueda en todo el historial anterior (`git log --all -p`) de claves de API, tokens de
  GitHub, de Telegram y de Instagram, claves privadas y teléfonos: ninguna. El correo de Juanjo
  solo aparece como autor de los commits.
- `.gitignore`: `dias/`, `registro/`, `estado/`, `revision/`, `instagram/`, `indice/` y los
  borradores.

## Riesgos y limitaciones

- Si algún día se sube por error algo personal, ya es público: los ADR y los encargos se
  escriben pensando en ello.

## Validación

- `git grep` en el árbol publicado de «plan Max», «suscripción», claves y rutas de credenciales:
  sin resultados (salvo las suscripciones de Web Push del ADR 0013, que son otra cosa).
- Desde el contenedor del NAS, `git fetch` y `git push --dry-run` contra el repositorio público
  funcionan con su clave.
- El NAS prepara el número de la noche del 05-11 con el historial nuevo.
