# El pódcast y el vídeo de cada semana

Aquí deja el proceso del boletín semanal (contenedor `boletin-semanal` del NAS) un archivo por semana ISO,
`AAAA-WW.json`, con el pódcast y el vídeo de NotebookLM de cada grupo (ADR 0034). Cuando aparece o cambia,
`nas/reloj.sh` vuelve a publicar la web con `scripts/publicar-web.sh`, con el número del día ya publicado.

```json
{
  "semana": "2026-45", "desde": "2026-11-02", "hasta": "2026-11-08",
  "grupos": {
    "chatgpt":  {"video": "https://www.youtube.com/watch?v=…",
                 "podcast": "https://archive.org/details/…",
                 "podcast_mp3": "https://archive.org/download/…/….mp3",
                 "resumen": "unas 72 palabras sobre lo que cuenta el vídeo"},
    "vce":      {"…": "…"},
    "edumedia": {"…": "…"}
  }
}
```

Las claves de los grupos son las de `GRUPOS` en `generar.py`. Cualquier grupo o campo puede faltar: sale
lo que haya. La semana va de lunes a domingo según el día de los mensajes, como las páginas `semana/AAAA-WW/`.
El `resumen` se traduce a las otras lenguas en `multimedia-XX/AAAA-WW.json` (ADR 0057) cada vez que este
archivo llega o cambia; si el resumen cambia, la traducción anterior deja de usarse hasta que se rehace.

Conviene escribir el archivo de una vez (a uno temporal y luego `mv`), para que nunca se lea a medias.
