# 49. Tiza y Algoritmo, en las orejas de la cabecera

Fecha: 2026-11-11 · Estado: aceptado

## Contexto

Los dos personajes de la viñeta salían en los iconos, la imagen de vista previa y la propia viñeta, pero no en
la cabecera de la web. Juanjo (11-11-2026) preguntó dónde podían ir. Se le enseñaron, sobre una copia de la
web real, dos variantes: cada uno a un lado de la cabecera, o los dos juntos y de la mano en el extremo
derecho de la línea del lema. Eligió la primera («vale»), pidió que al pasar el ratón saliera el nombre de
cada uno y aceptó que, al pulsarlos, llevaran a «La viñeta».

## Decisión

- **En las orejas, de pie sobre el filete doble**: Tiza a la izquierda y Algoritmo a la derecha, el mismo lado
  que en la viñeta (ADR 0022). Son los huecos que un periódico tiene a los lados de la mancheta.
- **Dos tamaños**: desde 78rem de ancho, donde la mancheta cabe en una línea y deja sitio a los lados, 6rem de
  alto; por debajo, 3,2rem, en la línea del lema. En el móvil (menos de 40rem) no salen, como el lema, para que
  la cabecera deje ver la primera noticia.
- **El dibujo de la viñeta**, con sus formas (`vineta.py`) y sus mismas clases de color, para que siga el tema
  claro u oscuro: Tiza con los brazos caídos y Algoritmo con los dos en alto. Los trazos engordan con `--k`
  (1,8 en pequeño y 1,3 en grande) para que se lean a ese tamaño. Código en `orejas()` de `generar.py` y estilos
  tras `.lema` en `estaticos/diario.css`.
- **El nombre al pasar por encima** (`title`), en el idioma de la página: Tiza, Guix, Xiz, Klarion o Chalk, y
  Algoritmo, Algorisme o Algorithm, los nombres que ya usan las viñetas traducidas (`nombre_tiza` y
  `nombre_algoritmo` en los textos de cada idioma). **Al pulsarlos, a «La viñeta»**, donde salen cada día.
  En la tableta, donde no hay ratón, el toque lleva a esa página, cuyo título dice cómo se llaman.

## Alternativas descartadas

- **Los dos juntos y de la mano, como en la imagen de vista previa**: juntos ocupan el doble de ancho y a la
  derecha de la mancheta solo quedan unos 60 px, así que se quedaban pequeños en una esquina y rompían la
  simetría.
- **Junto a la mancheta en todas las anchuras**: por debajo de 78rem la mancheta ocupa casi todo el ancho y
  habría que reducirla.

## Consecuencias

- Los personajes salen en todas las páginas con la cabecera completa (las que llevan lema).
- Si cambian las formas de los personajes en `vineta.py`, hay que llevar el cambio a `TIZA_OREJA` y
  `ALGORITMO_OREJA`.

## Validación

Probado el 11-11-2026 en una copia generada con `generar.py`: Chromium, Firefox y WebKit, en tema claro y
oscuro, en los cinco idiomas, a anchuras de 700 a 1440 px y en escritorio, tableta y móvil. Los personajes no
tocan las letras de la mancheta ni el lema. `scripts/revisar-maqueta.js` y `scripts/revisar-anchos.js` salen sin
avisos en la portada, «La redacción» y una noticia de los cinco idiomas. En «La viñeta» avisan de «fecha sola»
en cada tira, igual que en la versión publicada antes del cambio: no lo causa esta decisión.

En el mismo cambio, la mancheta y los enlaces «Volver» de las páginas del primer nivel (secciones, «La viñeta»,
«La redacción»…) apuntaban a `href=""` y recargaban la misma página; ahora llevan a la portada del idioma
(`./`), como el enlace «Portada» de la barra de secciones.
