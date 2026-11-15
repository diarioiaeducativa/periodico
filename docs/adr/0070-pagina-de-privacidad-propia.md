# 70. Página de privacidad propia

Fecha: 2026-11-15 · Estado: aceptado

## Contexto

Lo que el diario hace con los datos estaba en el apartado «Las visitas» de «La redacción» (ADR 0033 y 0042),
y la ficha de Google Play enlazaba `redaccion.html#privacidad` como política de privacidad. Juanjo, al
revisarlo el 15-11-2026, vio que ese enlace no llevaba «a ningún sitio claro de privacidad» y pidió una página
real, `privacidad.html`, con enlace en el pie de todas las páginas.

## Decisión

- `privacidad.html` en los cinco idiomas (`pagina_privacidad()` en `generar.py`; textos en
  `L["privacidad"]`), con el enlace «Privacidad» en el pie, junto a «Contacto». Cuatro apartados: las visitas,
  lo que queda en el dispositivo del usuario, la app de Android (también que los avisos no envían datos) y los
  servicios de terceros que intervienen (GitHub Pages, IONOS, Internet Archive y giscus).
- En «La redacción», el apartado de las visitas se queda en dos frases que llevan a la página nueva, para no
  repetir el tema en dos sitios. Conserva el ancla `#privacidad`, que enlazaban la ficha de Play y otras webs.
- La ficha de Google Play pasa a enlazar `privacidad.html`.

## Alternativas descartadas

- **Dejarlo en «La redacción» con otro título**: seguía sin ser una página que se encuentre como política de
  privacidad, ni desde el pie ni desde la ficha de Play.

## Consecuencias

- Si cambia el contador (ADR 0033), el alojamiento, lo que guarda el dispositivo o un servicio de terceros,
  hay que cambiar esta página en los cinco idiomas.
- La frase sobre quién ve las cifras («Solo las ven las dos personas que hacen el diario») se quitó a
  petición de Juanjo.

## Evidencia

- GitHub Pages registra la IP de cada visita por seguridad: documentación de GitHub, «What is GitHub Pages?»,
  apartado «Data collection» (consultado el 15-11-2026).
- Los registros de acceso del hosting de IONOS (`~/logs/access.log.*.gz`) guardan la IP con el último byte a
  cero y conservan unas ocho semanas de ficheros (37 el 15-11-2026, de la semana 38 a la 46).
- Las páginas publicadas solo cargan recursos de fuera para los vídeos (`archive.org`, con
  `preload="none"`) y el contador (`bilateria.org`); comprobado en la portada, `redaccion.html`,
  `videos.html` y un número el 15-11-2026.

## Riesgos y limitaciones

- El plazo de los registros de IONOS es el observado, no uno que IONOS publique para este plan.

## Validación

- Generado en una copia (`generar.py`), con `scripts/revisar-maqueta.js` sin avisos en `privacidad.html`,
  `eu/privacidad.html` y `redaccion.html`, en Chromium y Firefox, escritorio y móvil (15-11-2026).
