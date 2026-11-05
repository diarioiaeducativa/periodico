# 5. Revisión de los dibujos en su página

Fecha: 2026-11-03 · Estado: aceptado

## Contexto

La infografía del primer reportaje (03-11-2026) salió con los círculos negros en el tema
claro: la sección nueva definía el color de trazo pero no el de relleno, y una variable CSS
sin definir deja el relleno en negro. En oscuro casi no se notaba. Nadie miraba los dibujos
pintados: el ilustrador solo comprobaba que el SVG fuera válido y sin colores escritos a mano.
Juanjo lo vio en pantalla y preguntó si no había un revisor de imágenes; se le propuso una
comprobación con programa y un revisor con IA, y lo aprobó.

## Decisión

- **Un programa sin IA** (`scripts/revisar-dibujos.py`) abre en un Chromium sin pantalla la
  página de cada pieza con dibujo, en tema claro y oscuro, y comprueba: ningún relleno negro
  puro (la tinta del diario nunca es #000), todas las formas con una clase de la hoja de
  estilo, rótulos dentro del dibujo y sin pisarse, contraste de rótulos (4,5:1) y trazos
  (3:1) con el fondo. Deja capturas en `revision/FECHA/` (no se sube).
- **Un revisor visual** (Sonnet 5.5, `encargos/pasos/2b-revision-dibujos.md`) mira esas
  capturas y la pieza, y devuelve lo que no se ve bien o no explica la noticia; solo errores
  de bulto, no de gusto.
- **Una vuelta al ilustrador** (`2c-ilustraciones-rehacer.md`) con todos los motivos. Si tras
  ella el dibujo sigue mal, la pieza sale sin dibujo, el SVG se guarda en
  `revision/FECHA/retirados/` y se avisa a Juanjo. Nunca retrasa ni impide el número.
- Se aplica a los dibujos del día (tras el paso 2 de `noche.sh`) y a la infografía del
  reportaje (en `reportaje.sh`). Los dibujos catalanes pasan solo el programa tras la
  traducción: el que falla se retira y la página catalana usa el castellano, ya revisado.
- La imagen del NAS lleva Playwright 1.61.0 con el Chromium sin pantalla más ligero
  (`--only-shell`), dentro del tope de 2 GB del contenedor; el navegador se cierra siempre.
- «La redacción» presenta al revisor de dibujos (ocho agentes cada día) y el organigrama le
  pone una marca junto al ilustrador.

## Consecuencias

- Uno o dos minutos más por noche, sin coste nuevo.
- Validación (03-11-2026): sobre todo lo publicado, en los dos idiomas y temas, sin falsos
  avisos; con la hoja de estilo de antes de la corrección marca los 9 rellenos negros; con un
  dibujo estropeado a propósito (forma sin clase, rótulos pisados y fuera del dibujo) detecta
  todo, el revisor dice qué quitar, el ilustrador lo arregla y la segunda ronda lo aprueba en un
  minuto; con un ilustrador simulado que no arregla nada, la pieza sale sin dibujo y se avisa.
