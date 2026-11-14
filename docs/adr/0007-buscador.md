# 7. El buscador: Pagefind, en el navegador y sin servidor

Fecha: 2026-11-03 · Estado: aceptado

## Contexto

Con la Biblioteca, los reportajes y los breves, lo publicado ya no se encontraba solo con la
hemeroteca y las secciones, y crecerá a unas cinco o diez piezas por día. El sitio es estático
(GitHub Pages) y no usa servicios de terceros ni cookies; el buscador no podía romper eso.
Juanjo pidió el buscador y aprobó la propuesta («hazlo y publícalo directamente»).

## Decisión

- **Pagefind 1.6.0** (CloudCannon, licencia MIT; https://pagefind.app), instalado con pip
  (`pagefind[bin]`). Al publicar, `python3 -m pagefind --site sitio` indexa la web y deja el
  índice en `sitio/pagefind/`; el navegador del lector solo descarga los trozos del índice que
  necesita cada búsqueda, así que sigue siendo ligero con miles de piezas. Separa los índices por
  el `lang` de cada página y reduce las palabras a su raíz en castellano y en catalán («evaluar»
  encuentra «evaluación»). `generar.py` sigue sin dependencias: el índice es un paso aparte en
  `publicar.sh` y `scripts/publicar-nas.sh`; si falla, el sitio sale igual con el índice anterior.
- **Qué se indexa**: solo el `<article>` de cada pieza, artículo de la Biblioteca, reportaje,
  presentación y breve (`data-pagefind-body`), sin compartir, la lista de fuentes ni los enlaces de origen
  y de las fichas (`data-pagefind-ignore`; los enlaces, desde el ADR 0062). Cada uno lleva su sección como filtro, su fecha como dato y como
  orden, y la clave de su sección para el color. Las viñetas no tienen página propia y no se
  indexan.
- **La página «Buscar»** (`buscar.html`, en las dos ediciones), con interfaz propia sobre la API
  de Pagefind para que siga la maqueta y el tema: campo, filtros por sección con su recuento,
  resultados de diez en diez con sección, fecha, titular y fragmento con las palabras marcadas.
  La búsqueda y la sección quedan en la dirección (`?q=…&seccion=…`), para compartirla.
  La sección elegida se mantiene al escribir otra búsqueda, hasta pulsar «Todas»; cada resultado lleva una
  miniatura bajo el titular, y cada sección, un buscador que abre este con ella elegida (ADR 0062).
- **La lupa** (icono `search` de Lucide) va en la cabecera, junto al enlace a la otra edición y
  el botón del tema, con su misma forma. Para que los tres quepan en un móvil de 360 px, por
  debajo de 26 rem se acerca la separación y el enlace a la otra edición dice solo el nombre de
  la lengua («Castellano», «Català»).
- La imagen del NAS lleva `pagefind[bin]==1.6.0`.

## Alternativas descartadas

- **Un índice JSON propio** cargado entero: con el texto completo pasaría de varios megas en un
  año, demasiado para el móvil.
- **Un buscador externo** (Google, Algolia): servicios de terceros que ven lo que se busca.
- **Buscar por el sentido de una pregunta**: necesita un servidor. Para lo que se dijo en los
  grupos ya está el Bot de IA Educativa.

## Validación

03-11-2026, con Chromium y Firefox, a 1200 y 360 px, en tema claro y oscuro: «evaluar» da 7
resultados (encuentra «evaluación»), «UNESCO» 3, «agentes» 10 y, filtrado por Breves, 2;
«avaluació» en la edición catalana, 5; una palabra inexistente, ningún resultado y su mensaje.
Sin errores de JavaScript ni desbordamiento. 62 páginas indexadas (31 por lengua).
