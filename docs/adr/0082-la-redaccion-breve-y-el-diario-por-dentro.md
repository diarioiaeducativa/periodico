# 82. «La redacción» breve y «El diario por dentro»

Fecha: 2026-11-16 · Estado: aceptado

> El [ADR 0093](0093-las-instrucciones-de-los-agentes-como-paginas.md) lleva la lista de las instrucciones también al
> libro de estilo, y cada una a una página del diario en lugar de a GitHub.

## Contexto

«La redacción» había ido sumando apartados (el proceso, el equipo, las secciones, las personas, el código, las
visitas, las comunidades, el contacto, las correcciones, las normas) hasta ser una página muy larga que poca gente
iba a leer. Se pidió una versión ligera para cualquier lector y otra completa para quien quiera conocer el diario a
fondo.

## Decisión

- **«La redacción»** (`redaccion.html`), la versión breve: la entrada; el organigrama con un pie que dice qué es y
  cómo se lee; junto a él, «Cómo se hace cada número», con los tres grupos nombrados, con su tema y su enlace, y
  cuatro ideas en recuadros con icono (de los grupos al diario, cada dato comprobado, nunca un día sin número, una
  persona responde); «Para saber más», con enlaces a la página completa y a los tres documentos de normas; y, al
  pie y centrado, el emblema de las comunidades.
- **«El diario por dentro»** (`dentro.html`), la versión completa: el equipo de agentes, todos los apartados que
  tenía antes «La redacción», en los mismos bloques (`BLOQUES_DENTRO`, antes `BLOQUES_REDACCION`, ADR 0047), y «Las
  instrucciones de cada agente», cada una enlazada a su guía (`GUIAS_AGENTES`).
- Las cinco páginas que explican el diario («La redacción», «El diario por dentro» y las tres normas) llevan al pie
  el mismo «Para saber más», con enlaces a las otras cuatro (`mas_html`).
- Las dos, en los cinco idiomas. Los enlaces de fuera a un apartado que se ha ido (`redaccion.html#privacidad`,
  `#comunidades`, `#contacto`…) llevan solos al mismo apartado de la página completa; el enlace de las comunidades
  del pie va directamente allí.

## Consecuencias

- «La redacción» se lee en un par de minutos; lo demás sigue a un clic.
- Un apartado nuevo sobre el funcionamiento va en «El diario por dentro»; en la breve solo entra lo que cualquier
  lector necesita para hacerse una idea.

## Validación

Las dos páginas, generadas en los cinco idiomas y miradas en Chromium y Firefox, en escritorio, tableta y móvil,
en tema claro y oscuro (16-11-2026), sin huecos ni errores.
