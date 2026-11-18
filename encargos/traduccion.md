# Libro del traductor del Diario de IA Educativa

Cómo se traduce el diario del castellano al catalán, al gallego, al euskera y al inglés. Lo leen todos los
agentes que traducen algo que va a leer el público, además del [libro de estilo](estilo.md), que vale
igual en todas las lenguas. Se lee el apartado general y el de la lengua de cada encargo.

## Para todas las lenguas

- **Se traduce el sentido, en el registro natural de cada lengua**, como lo escribiría un periodista
  de esa lengua: sin calcos del castellano en el orden de las palabras, las preposiciones ni las
  expresiones.
- **El mismo contenido**: los mismos artículos, enlaces, cifras, negritas y cursivas que el original.
  No se añade ni se quita información, salvo la explicación de lo propio de España (más abajo).
- **Los nombres no se traducen**: productos, aplicaciones, empresas y los tres grupos («Vibe Coding
  Educativo», «EduMedia-IAG»). Los personajes de la viñeta sí tienen nombre en cada lengua
  (`scripts/idiomas.py`).
- **Lo oficial ajeno queda en su idioma original**: el título de una ley, de un informe, de una guía.
  Un organismo español se traduce si tiene forma habitual en la lengua (el ministerio, una consejería);
  los que tienen nombre propio en su lengua no (Generalitat, Xunta, Ertzaintza). Las siglas oficiales
  se mantienen (LOMLOE, INTEF, AEPD).
- **Lo propio de España se explica** cuando el lector de esa lengua puede no conocerlo, sobre todo en
  inglés: una etapa educativa, las oposiciones, una comunidad autónoma.
- **Un gráfico** (`grafico`) se traduce en su título, sus etiquetas, los nombres de las series y la nota; el
  tipo, la unidad y los valores no se tocan, y el título de la fuente queda en su idioma original.
- **Una fuente en otra lengua lleva su marca** («(en castellà)», «(in Spanish)»), como dice
  `scripts/idiomas.py`.
- **Ante una duda, se consulta la obra de referencia de la lengua** (en su apartado) y no se resuelve de
  memoria. Si una obra no deja leer, se busca la misma respuesta en otra de la lista.
- **El mismo término siempre**: el léxico de la IA de cada lengua está fijado abajo. No se alternan
  formas («xatbot» y «chatbot» en el mismo número).
- **Lo correcto no se corrige**: si una forma parece rara pero la recoge la norma, se deja.

## Catalán

**Norma**: estándar del Institut d'Estudis Catalans (IEC), en registro periodístico.

**Dónde consultar**
- [Optimot](https://aplicacions.llengua.gencat.cat/llc/AppJava/index.html): busca a la vez en el
  diccionario del IEC, en las fichas de dudas y en la terminología del TERMCAT. Es la vía para el TERMCAT,
  cuya web no deja leer a los programas.
- [Diccionari de la llengua catalana (DIEC2)](https://dlc.iec.cat/), [Gramàtica (GIEC)](https://giec.iec.cat/)
  y [Ortografia](https://oiec.iec.cat/) del IEC.
- [ésAdir](https://www.esadir.cat/) y el [Llibre d'estil de 3Cat](https://www.3cat.cat/llibredestil/):
  el estilo periodístico de la radio y la televisión públicas.

**Formato**
- Horas con punto: «a les 10.30»; el huso, «(hora peninsular espanyola, UTC+1)».
- Porcentaje con espacio: «10 %», como pide el Optimot.
- Millares con punto (115.000); ordinales «4t d'ESO», «1r de batxillerat».
- Cargos, etapas educativas y asignaturas en minúscula («primària», «batxillerat»); los organismos, en
  mayúscula.
- Topónimos con forma catalana tradicional: Saragossa, Osca, la Corunya, Biscaia.

**Vocabulario**
- «el professorat», «l'alumnat»; «soc», sin tilde.
- IA: «intel·ligència artificial (IA)», «IA generativa», «model de llenguatge gran (LLM)», «agent d'IA»,
  «aprenentatge automàtic», «al·lucinació», «codi obert», «aplicació».
- *Prompt*: «indicació», el término normalizado por el TERMCAT; la primera vez, con el inglés en cursiva
  entre paréntesis: «una indicació (*prompt*)».
- *Chatbot*: «xatbot».

**Calcos que no**: «en base a», «a nivell de». **Correctos, no se cambian**: «degut a», «sí que», «app».

## Gallego

**Norma**: normativa de la Real Academia Galega (RAG), en registro periodístico.

**Dónde consultar**
- [Dicionario da RAG](https://academia.gal/dicionario) y las [Normas ortográficas e
  morfolóxicas](https://publicacions.academia.gal/index.php/rag/catalog/download/252/248/152?inline=1).
- [Na Universidade en galego sen dúbida](https://www.lingua.gal/documents/204205/217676/engalegosendubida.pdf?version=1.0)
  y el [curso de lenguaje administrativo de la Xunta](https://www.lingua.gal/documents/204205/217796/01-CURSO-MEDIO-LINGUAXE-ADMINISTRATIVA_v2.pdf?version=1.0):
  números, mayúsculas, topónimos y colocación del pronombre.
- [Digalego](https://digalego.xunta.gal/gl) (diccionario con equivalencias), [TERGAL](http://www.cirp.gal/tergal)
  (terminología) y el [Nomenclátor](https://toponimia.xunta.gal/gl) (topónimos de Galicia).

**Formato**
- Horas con punto: «ás 10.30»; el huso, «(hora peninsular española, UTC+1)».
- Porcentaje con espacio: «30 %».
- Millares con espacio: «115 000».
- Cargos, días, meses y etapas en minúscula: «educación primaria», «bacharelato», «educación secundaria».
- Topónimos de Cataluña y del País Vasco en su forma oficial: «Girona», «Donostia».

**Vocabulario**
- «o profesorado», «o alumnado»; cuida el género («o xiz») y evita los castellanismos («encerado», no
  «pizarra»; «relatorios», no «ponencias»).
- IA: «intelixencia artificial (IA)», «IA xerativa», «modelo de linguaxe (LLM)», «axente de IA»,
  «aprendizaxe automática», «código aberto», «aplicación». Los cuatro últimos no están en el
  diccionario de la RAG con este sentido: el diario los usa así.
- *Prompt*, en cursiva, y explicado la primera vez como «instrución», como hace la Xunta.

**Gramática que falla a menudo**
- El pronombre va delante del verbo cuando lo precede un adverbio o una negación sin pausa: «só se
  equivoca», no «só equivócase».
- «Ambos» lleva artículo delante del sustantivo: «ambos os modelos».

## Euskera

**Norma**: euskera batua de Euskaltzaindia, en registro periodístico.

**Dónde consultar**
- [Normas de Euskaltzaindia](https://www.euskaltzaindia.eus/index.php?option=com_euskaltzaindiarenarauak&view=frontpage&Itemid=1723&lang=eu)
  (cada una en PDF) y su diccionario.
- [Euskalterm](https://www.euskadi.eus/euskalterm/) (terminología), [Elhuyar](https://hiztegiak.elhuyar.eus/)
  y [Labayru](https://hiztegia.labayru.eus/) (diccionarios).
- [Libro de estilo de Berria](https://www.berria.eus/estiloliburua/): el estilo periodístico.
- [Kalkoen Behatokia](https://www.ehu.eus/ehg/kalkoak/) de la UPV/EHU: calcos del castellano.

**Formato** (norma 203 de Euskaltzaindia)
- Horas: «10:30ean»; el huso, «(Espainiako penintsulako ordua, UTC+1)». Fechas: «2026ko azaroaren 13an».
- Porcentaje con el signo delante y espacio: «% 35».
- Millares con espacio: «115 000».
- Cargos en minúscula; organismos y etapas educativas en mayúscula («Lehen Hezkuntza», «Batxilergoa»),
  como manda la norma 200.
- Siglas y nombres declinados sin guion: «AAren», «ElevenLabsen».
- Topónimos: normas 32 (España), 151 (regiones) y 38 (países).

**Vocabulario**
- «irakasleak», «ikasleak»; el diario es «egunkaria», nunca «diarioa»; un centro educativo es
  «ikastetxea», no «zentroa».
- IA: «adimen artifiziala (AA)», «AA sortzailea», «ikaste automatikoa», «kode irekia», «aplikazioa»,
  «txatbota». El modelo de lenguaje y el agente de IA no tienen término normalizado: el diario usa
  «hizkuntza-eredua» y «AA agentea».
- *Prompt*, en cursiva, sin traducir: no tiene término normalizado.

**Calcos que no**: el «bere» innecesario (Kalkoen Behatokia).

## Inglés

**Norma**: inglés británico, en registro periodístico. El diario es «the paper», nunca «the diary».

**Dónde consultar**
- [Guía de estilo de The Guardian](https://www.theguardian.com/guardian-observer-style-guide-a) (cada
  letra en su página) y la de la [BBC](https://www.bbc.co.uk/newsstyleguide/all).
- [Guía de estilo para la traducción al inglés de la Comisión Europea](https://knowledge-centre-translation-interpretation.ec.europa.eu/en/resources-translating-eu-documents/guidelines-translating-eu-documents-english),
  con el *Country Compendium*: organismos y topónimos de España.
- [IATE](https://iate.europa.eu) (terminología de la UE) y el [Oxford Learner's Dictionary](https://www.oxfordlearnersdictionaries.com).

**Formato**
- Fechas: «13 November 2026». Horas: «10.30am», como The Guardian; el huso,
  «10.30am CET (UTC+1)», o CEST (UTC+2) en verano, y la de fuera con la de origen: «10am PT (6pm CET, UTC+1)».
- Porcentaje pegado a la cifra: «35%». Millares con coma: «115,000».
- Comillas inglesas (“ ”), nunca las españolas; ortografía en -ise («organise»).
- Cargos, etapas y organismos genéricos en minúscula («the education ministry», «secondary education»).
- Topónimos: A Coruña, Lleida, Catalonia, the Basque Country.

**Vocabulario**
- «teachers», «students» o «pupils».
- IA: «AI», «generative AI», «large language model (LLM)», «AI agent», «machine learning»,
  «hallucination», «open-source» (con guion delante del sustantivo), «app».
- Lo que en el original se dijo en inglés se copia de la fuente, no se retraduce.

**Lo propio de España**
- Un organismo, con su nombre descriptivo en inglés y la sigla original: «the Spanish education
  ministry», «Spain's education law (LOMLOE)»; nunca una sigla inglesa inventada.
- «autonomous community» (comunidad autónoma), «regional education ministry» (consejería),
  «competitive civil service exam» (oposiciones), «vocational training» (FP).
- **Nunca «Year 10» ni otra equivalencia del sistema británico**: los cursos no coinciden. El nombre
  español con la edad: «the fourth year of ESO (students aged 15 to 16)», «Bachillerato (the final two
  years of secondary school, ages 16 to 18)».
