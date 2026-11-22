# 98. Ladillos que dicen lo que cuenta su apartado

Fecha: 2026-11-22 · Estado: aceptado

## Contexto

El reportaje del 22-11-2026 abría su primer apartado con el ladillo «Qué cuenta como prueba». Juanjo lo vio en la
vista previa: «este tipo de titulos o expresiones breves no me gustan, se ve enseguida que son de ia». El encargo del
reportaje pedía para los ladillos «un sustantivo o una frase corta», lo que invita a la etiqueta abstracta, y en los
cuatro reportajes publicados hasta entonces los mismos moldes se repetían: «Qué…» o «Lo que…» en nueve ladillos,
parejas abstractas («Entender o entregar», «El medio y el método», «Del producto al proceso») en cinco, y «Qué puede
hacer un docente» dos veces, el 31-10 y el 7-11.

## Decisión

- **La norma, en el libro de estilo** (`encargos/estilo.md`, «Ladillos»): cada ladillo es un titular pequeño que dice
  lo que cuenta su apartado (quién hace qué, el dato), con verbo si se puede y como mucho 60 caracteres. Ni empieza
  por «Qué», «Lo que», «Cómo» o «Por qué», ni es una pareja abstracta, ni «Más allá de…», ni repite el de otro
  reportaje. El encargo del reportaje remite a ella.
- **El reportero recibe los ladillos ya publicados**: `reportaje.sh` deja en `reportajes-borrador/ladillos-usados.txt`
  los de `reportajes/` y los de los reportajes de reserva antes de que escriba.
- **Una comprobación sin IA** en `scripts/revisar-estilo.py` (norma 4), que ya pasa cada noche con su corrector
  `29-estilo`: en los reportajes en castellano, los moldes (`MOLDES`) y los ladillos ya usados en un reportaje
  anterior o de reserva (comparados sin mayúsculas, tildes ni signos; uno de reserva puesto en `reportajes/` no se
  compara consigo mismo, porque tiene el mismo titular). El corrector reescribe el ladillo con lo que dice el
  apartado, en las cinco lenguas, también en inglés.
- **Lo publicado no se rehace**: la norma vale desde el reportaje del 22-11-2026, cuyo primer ladillo pasó a «La
  revisión de Stanford solo admite estudios causales» antes de salir. Los otros tres ladillos de ese reportaje que la
  comprobación señala se dejaron como estaban, porque Juanjo solo pidió cambiar el primero.

## Evidencia y validación

- Con el reportaje del 22-11 tal como salió del verificador, `revisar-estilo.py --dia 2026-11-21` señala
  «Qué cuenta como prueba», «Entender o entregar», «El medio y el método» y «Lo que piden las instituciones».
- `revisar-estilo.py --todo`, sobre los tres reportajes anteriores: 12 avisos de ladillo, entre ellos la repetición
  de «Qué puede hacer un docente». No señala ladillos que dicen algo concreto («La ley: catorce años y función
  educativa», «Datos del alumnado y proveedores»).

## Riesgos

- Los moldes son una lista: un ladillo abstracto con otra forma («Tres reglas que se confunden», «El marco en
  España») pasa. Si aparecen otros que suenan igual, se añaden a `MOLDES`.
- La norma sola no basta, porque el modelo vuelve a los moldes; lo que la sostiene es la comprobación con su
  corrector.
