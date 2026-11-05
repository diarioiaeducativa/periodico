# 20. La evaluación VCER, en el pie

Fecha: 2026-11-05 · Estado: aceptado

## Contexto

El 05-11-2026 se evaluó el diario con la rúbrica VCER de la guía «Vibe coding responsable». La
primera pasada dio un 90 %; tras corregir lo que señaló (ADR 0019 y cambios en los ADR 0003,
0011 y 0014), la segunda dio un 100 %. Juanjo aprobó guardar el informe y poner la mención en
el pie («hazlo todo»).

## Decisión

- **El informe completo está en `evaluacion-vcer.md`**, en la raíz del repositorio; una
  evaluación nueva lo sustituye.
- **El pie de todas las páginas lleva la mención** «Evaluación VCER: Recomendable (100 %),
  noviembre de 2026» («Avaluació VCER: Recomanable (100 %), novembre de 2026»), con el
  porcentaje, enlazada a la página de la VCER con el título y la dirección del diario en el
  idioma de la página. Sin versión, porque el diario no tiene número de versión.
- El resultado está en la constante `VCER` de `generar.py` y el texto, en los textos de cada
  idioma: al repetir la evaluación se cambian los dos.

## Alternativas descartadas

- **La mención sin porcentaje**: la guía la permite, pero con un 100 % no hay nada que matizar.

## Consecuencias

- La mención dice de cuándo es la evaluación; si el diario cambia mucho, hay que repetirla.

## Evidencia

- `evaluacion-vcer.md`; la página de la mención, comprobada en castellano y en catalán.

## Riesgos y limitaciones

- La evaluación del contenido se hizo sobre un número: es una muestra, no una garantía de los
  siguientes.

## Validación

- La mención sale en el pie de las dos ediciones y su enlace abre la página de la VCER con el
  título, la dirección, el resultado y la fecha correctos.
