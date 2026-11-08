# 31. Las fuentes, enlazadas donde se nombran

Fecha: 2026-11-08 · Estado: aceptado

## Contexto

Los encargos pedían las fuentes en `fuentes`, que el diario pone al pie de cada pieza, y
permitían enlaces en el texto, pero solo los obligaban para lo ya publicado (ADR 0011). Cada
redactor decidía: en el número del 8 de noviembre, la pieza sobre la memoria de los agentes
enlazaba en el texto el artículo de Anthropic, pero no el de Bilateria, y la de Incluxat no
enlazaba nada. En lo publicado hasta entonces, 66 de las 136 fuentes en castellano solo estaban
al pie. Juanjo, 08-11-2026, ante el artículo de Bilateria sin enlace: «está bien que esté abajo
pero también debería estar aquí, lo mismo para el resto de artículos».

## Decisión

- **Cada fuente que el texto nombra se enlaza en su primera mención**, con su nombre como texto
  del enlace; `fuentes` sigue al pie con todas. La norma está en `encargos/enlaces.md`, común a
  redacción, Biblioteca, Repositorio y reportaje, y cada encargo la recuerda junto a `fuentes`.
- **El revisor de cada sección lo comprueba** y enlaza lo que falte (pasos 1, 9, 13 y 17).
- **Lo ya publicado se enlazó también**, en los cinco idiomas y en la reserva, con
  `scripts/enlazar-fuentes.py`: un agente propone dónde va cada enlace y el programa solo lo
  acepta si el texto, quitados los enlaces nuevos, es idéntico carácter a carácter al original,
  y si cada enlace nuevo es de una fuente de la pieza y sale una sola vez.

## Alternativas descartadas

- **Dejar las fuentes solo al pie**: obliga a bajar hasta el final para ir a lo que el texto
  acaba de nombrar.
- **Enlazar lo ya publicado buscando el título de cada fuente en el texto, sin agente**: los
  títulos de `fuentes` no coinciden con cómo los nombra el texto («Bilateria: Agentes de IA…»
  frente a «el artículo «Agentes de IA…»»), y menos en las traducciones.
- **Volver a redactar o traducir lo publicado**: cambiaría textos ya revisados.

## Consecuencias

- Las piezas llevan más enlaces en el cuerpo; `generar.py` ya los convertía (`md()`), también los
  de los mensajes de la Biblioteca, que llevan al artículo del diario.
- Las traducciones conservan los enlaces del castellano (pasos 5, 11, 15 y 18).

## Evidencia

- `encargos/enlaces.md`, `encargos/redaccion.md` y los pasos de repaso, en el commit de este ADR.
- Recuento de partida: `fuentes` cuyo `url` no aparece en el cuerpo, en `ediciones`,
  `biblioteca`, `reportajes` y `repositorio` del NAS el 08-11-2026.

## Riesgos y limitaciones

- Si el texto no nombra una fuente (una noticia que solo la usa para comprobar un dato), no se
  enlaza: queda al pie.
- El agente puede elegir un texto de enlace demasiado corto o largo; el programa garantiza que no
  cambia el texto, no que el enlace esté en el mejor sitio.

## Validación

- Número del 8 de noviembre: las 6 fuentes que faltaban, enlazadas en los cinco idiomas antes de
  publicarse; comprobado en la vista previa (ADR 0025).
- Lo anterior: RESULTADO.
