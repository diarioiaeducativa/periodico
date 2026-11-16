# 79. Libro del traductor

Fecha: 2026-11-16 · Estado: aceptado

## Contexto

Cada traductor recibía de `scripts/idiomas.py` una línea por lengua (la norma de la academia, cómo se
dice «profesorado», las marcas de las fuentes) y el apartado «Las traducciones» del libro de estilo
(ADR 0078). Nada decía dónde consultar una duda ni cómo se escriben en cada lengua las horas, los
porcentajes, las mayúsculas, los topónimos o los términos de la IA.

Una revisión de lo publicado en las cuatro lenguas (16-11-2026) encontró fallos repetidos de ese tipo:
en inglés, 4.º de ESO traducido como «Year 10» (que además no coincide) y «the diary»; en gallego, «só
equivócase», «Ambos modelos» y etapas en mayúscula; en catalán, etapas en mayúscula, «10:30» y la misma
palabra unas veces «xatbot» y otras «chatbot», «prompt» e «indicació»; en euskera, «diarioak»,
«zentroaren», un «bere» calcado y el porcentaje escrito de dos maneras.

## Decisión

`encargos/traduccion.md`, el libro del traductor: un apartado común (sentido y no calco, nombres que no
se traducen, organismos y siglas, lo propio de España, consultar ante la duda, el mismo término siempre,
no corregir lo correcto) y uno por lengua con su norma, dónde consultar (en línea y con acceso para un
agente), los formatos, el vocabulario de la IA fijado y los calcos frecuentes. Lo leen todos los
encargos de traducción y el guion del vídeo, junto con el libro de estilo, que resume las traducciones y
remite a él. `scripts/idiomas.py` sigue dando a cada encargo los datos de su lengua.

Fuentes: el Optimot, el IEC, ésAdir y el libro de estilo de 3Cat (catalán); la RAG y las guías de la
Xunta (gallego); las normas de Euskaltzaindia, Euskalterm, el libro de estilo de Berria y el Kalkoen
Behatokia de la UPV/EHU (euskera); las guías de The Guardian, de la BBC y de la Comisión Europea, e IATE
(inglés). La web del TERMCAT no deja leer a los programas: su terminología se consulta por el Optimot.

Donde las fuentes no coinciden o no hay término normalizado, el libro fija una forma para que el diario
no alterne: en catalán, el porcentaje con espacio (Optimot), «indicació» para *prompt* (TERMCAT) y
«xatbot»; en inglés, las horas como The Guardian (10.30am); en euskera, «hizkuntza-eredua» y «AA
agentea»; en gallego y en euskera, *prompt* en cursiva.

## Consecuencias

- Las traducciones se escriben con las mismas formas cada noche.
- Lo ya publicado con estos fallos no se cambia solo; se puede corregir aparte.
- Una forma fijada que no convenza se cambia en el libro, en un solo sitio.

## Validación

Las traducciones de la noche siguiente (16 al 17-11-2026) se miran contra el libro: horas, porcentajes,
etapas, «Year», «the diary», y el vocabulario de la IA de cada lengua.
