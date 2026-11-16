# 80. Las normas del diario, enlazadas desde «La redacción»

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

El diario tiene tres documentos públicos sobre cómo se hace: `docs/como-se-hace.md` (las normas, quién
las aplica, cómo se comprueban y lo que falta), el libro de estilo (`encargos/estilo.md`, ADR 0078) y el
libro del traductor (`encargos/traduccion.md`, ADR 0079). Hacía falta decidir cómo se llega a ellos desde
la web sin llenar el pie de enlaces.

Los medios de referencia no ponen sus normas sueltas en el pie: la BBC las tiene en sus «Editorial
Guidelines», dentro de «About the BBC», y The Guardian, en «About us», con su código editorial: el lector
las encuentra en la página que explica quién hace el medio y cómo trabaja.

## Decisión

Un apartado más en «La redacción», la página que ya explica cómo se hace el diario y que está en el
menú y en el pie: «Las normas del diario», en los cinco idiomas, con los tres documentos enlazados en el
repositorio público, donde GitHub los muestra ya maquetados. En las ediciones traducidas se dice que los
tres están en castellano. Va en el bloque de «quién lo hace», junto a «El código». El pie no cambia.

## Consecuencias

- Ningún enlace nuevo en el pie ni en el menú.
- Los documentos se leen en GitHub, no en la web del diario; si algún día se quieren con la maqueta del
  diario, habría que generarlos como páginas.

## Validación

«La redacción» generada en castellano, catalán e inglés, mirada en Chromium y Firefox, en escritorio y
móvil (16-11-2026): el apartado entra en las columnas sin dejar huecos.
