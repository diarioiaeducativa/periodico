# Encargo: el aviso de cada mañana en los tres grupos

A las 7:00, el Bot de IA Educativa publica en cada grupo un mensaje que anuncia el número
del día del «Diario de IA Educativa». Tú escribes esos tres mensajes. El bot los publica
tal cual, sin que nadie los revise.

## Los grupos

- `chatgpt`: ChatGPT-IA-edu, IA en educación en general.
- `vce`: Vibe Coding Educativo, docentes que programan sus propias aplicaciones con IA.
- `edumedia`: EduMedia-IAG, IA generativa para crear audio, vídeo e imagen.

## Cómo es cada aviso

El bot monta el mensaje (ADR 0010): arriba, en negrita, el nombre del diario con el número y,
debajo, la fecha; luego tu **saludo**, tus **puntos**, cada uno con su marca, y el enlace a la
portada, con la imagen del número encima. Tú escribes solo el saludo y los puntos:

- **Saludo**: «Buenos días.» y, si quieres, una frase corta que lleve a los puntos (como mucho
  120 caracteres en total). Que cambie de un día a otro: «Hoy, en el número:» todos los días cansa.
- **Puntos**: de dos a tres, lo más interesante del número **para ese grupo**: primero lo que
  salió de ese mismo grupo, si lo hay, y si no, lo que mejor encaje con su tema. Cada uno, una
  o dos frases que se entiendan solas, de 60 a 200 caracteres, sin punto y aparte. Cada grupo
  recibe una selección o una redacción distinta, no lo mismo con otro orden. No digas lo que
  el número no trae («hoy no hay novedades de vídeo…»): cuenta lo que sí trae.
- Uno de los puntos puede ser la viñeta de Tiza y Algoritmo, con su idea en pocas palabras y
  sin contar el remate, y no todos los días.
- Texto plano: sin Markdown, sin negritas, sin enlaces ni emojis (el enlace y el 👉 los pone el
  bot) y sin la marca de cada punto.
- Tono cercano pero informativo, nunca publicitario: nada de «¡No te lo pierdas!», ni
  exclamaciones, ni adjetivos de anuncio. Lenguaje inclusivo natural («el profesorado»).
- Habla de temas, no de personas: solo se nombra al autor de un recurso que él mismo ha
  publicado, también si es Juanjo de Haro, y sin su cargo (administrar un grupo, ser coautor
  del diario) salvo que tenga que ver con la noticia. Nada que no esté en la edición.
- Que no se parezca a los avisos de los días anteriores (en `avisos/`): cambia el arranque
  tras el saludo, la construcción de las frases y lo que se destaca. Repetir «Hoy en el
  diario…» cada día cansa.

## La descripción de Instagram

El número sale también en Instagram, en la cuenta @comunidad.iaeducativa, como un carrusel de
imágenes (ADR 0015). Escribe además el texto que va debajo, en el campo `instagram`:

- De dos a cuatro frases que cuenten lo que trae el número, para cualquier docente que no
  conoce los grupos: qué se ha visto, compartido o debatido, sin dar por sabido nada.
  Entre 150 y 600 caracteres.
- Impersonal y sin hablar de personas: ni nombres ni «un miembro del grupo». Nada de saludo.
- Texto plano: sin enlaces (en Instagram no se pueden pulsar), sin etiquetas (#), sin emojis
  ni exclamaciones. El programa añade la cabecera con el número, el aviso de que está hecho
  con IA, la remisión al enlace del perfil y las etiquetas.
- Distinto de los avisos de los grupos y de las descripciones de los días anteriores.

## Salida

`avisos/<fecha de publicación>.json`, JSON válido en UTF-8:

```json
{"fecha": "2026-11-03", "avisos": {
  "chatgpt": {"saludo": "Buenos días. …", "puntos": ["…", "…"]},
  "vce": {"saludo": "…", "puntos": ["…", "…"]},
  "edumedia": {"saludo": "…", "puntos": ["…", "…"]}},
 "instagram": "…"}
```
