# 85. Las normas, traducidas a las otras lenguas

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

Las tres normas públicas (`docs/como-se-hace.md`, `encargos/estilo.md` y `encargos/traduccion.md`, publicadas como
páginas por el ADR 0081) estaban solo en castellano, porque son los documentos con los que trabajan los agentes y no
se quería mantener cuatro copias a mano. Las ediciones en catalán, gallego, euskera e inglés las enlazaban avisando
de que estaban en castellano. Se pidió que también se puedan leer en cada lengua.

## Decisión

- El original sigue siendo el castellano, que es lo que leen los agentes. La traducción de cada documento va en
  `docs/traducciones/<lengua>/<nombre>.md`, con la huella del original en la primera línea.
- **La traducción se hace en el momento de cambiar el original** (Juanjo, 19-11-2026: «la traduccion debe ser al
  momento de cambiar el articulo»): el agente que cambia uno de los tres documentos lanza en el mismo trabajo
  `scripts/normas-traducir.sh` en el contenedor y vuelve a publicar la web con las traducciones, que sube también al
  repositorio. La pasada de cada noche queda como red para lo que se haya escapado.
- `scripts/normas-traducir.sh`, también cada noche en `noche.sh`: si un original ha cambiado o falta su traducción, un agente
  por lengua lo traduce (`encargos/pasos/37-normas-traduccion.md`), con el libro del traductor, las cuatro lenguas a
  la vez. `scripts/normas_traducir.py` comprueba después que la traducción tiene los mismos títulos, puntos, filas de
  tabla, nombres de archivo, enlaces y números de ADR que el original; si no, se quita. Casi todas las noches no hay
  nada que hacer.
- `generar.py` publica la página de una lengua (`/ca/normas.html`…) solo si su traducción es de la versión actual del
  original, con un aviso de traducción automática con IA y el enlace al original. Si no la hay, los enlaces de esa
  lengua llevan al castellano y lo dicen («(en castellà)»), como hasta ahora, y su selector de idioma lleva a «La
  redacción» de esa lengua.
- Los ejemplos que explican una norma del castellano («quien», «pieza») se dejan en castellano en la traducción.
- La publicación sube las traducciones con el número (`publicar-nas.sh`).

## Consecuencias

- Cada lector puede leer las normas en su lengua; un cambio en el original se traduce en el momento. Hasta el
  19-11-2026 se traducía la noche siguiente, y mientras tanto esa lengua enlazaba al castellano: ese día una norma
  nueva del libro de estilo dejó sus cuatro traducciones en castellano al publicar la web por la mañana.
- La primera vez, unas 6.300 palabras por lengua; después, solo los documentos que cambien.

## Validación

Generado sin traducciones (16-11-2026): las ediciones traducidas siguen enlazando al castellano y lo avisan. La
primera traducción de los tres documentos a las cuatro lenguas se hace el mismo día, con la comprobación.
