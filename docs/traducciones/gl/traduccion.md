<!-- origen: 2856bceb652c83cb -->
# Libro do tradutor do Diario de IA Educativa

Como se traduce o diario do castelán ao catalán, ao galego, ao éuscaro e ao inglés. Lérono todos os
axentes que traducen algo que vai ler o público, ademais do [libro de estilo](estilo.md), que vale
igual en todas as linguas. Lese o apartado xeral e o da lingua de cada encargo.

## Para todas as linguas

- **Tradúcese o sentido, no rexistro natural de cada lingua**, como o escribiría un xornalista
  desa lingua: sen calcos do castelán na orde das palabras, nas preposicións nin nas
  expresións.
- **O mesmo contido**: os mesmos artigos, ligazóns, cifras, letras grosas e cursivas que o orixinal.
  Non se engade nin se quita información, salvo a explicación do propio de España (máis abaixo).
- **Os nomes non se traducen**: produtos, aplicacións, empresas e os tres grupos («Vibe Coding
  Educativo», «EduMedia-IAG»). Os personaxes da viñeta si teñen nome en cada lingua
  (`scripts/idiomas.py`).
- **O oficial alleo queda na súa lingua orixinal**: o título dunha lei, dun informe, dunha guía.
  Un organismo español tradúcese se ten forma habitual na lingua (o ministerio, unha consellaría);
  os que teñen nome propio na súa lingua non (Generalitat, Xunta, Ertzaintza). As siglas oficiais
  mantéñense (LOMLOE, INTEF, AEPD).
- **O propio de España explícase** cando o lector desa lingua pode non coñecelo, sobre todo en
  inglés: unha etapa educativa, as oposicións, unha comunidade autónoma.
- **Un gráfico** (`grafico`) tradúcese no seu título, nas súas etiquetas, nos nomes das series e na nota; o
  tipo, a unidade e os valores non se tocan, e o título da fonte queda na súa lingua orixinal.
- **Unha fonte noutra lingua leva a súa marca** («(en castellà)», «(in Spanish)»), como di
  `scripts/idiomas.py`.
- **Ante unha dúbida, consúltase a obra de referencia da lingua** (no seu apartado) e non se resolve de
  memoria. Se unha obra non deixa ler, búscase a mesma resposta noutra da lista.
- **O mesmo termo sempre**: o léxico da IA de cada lingua está fixado abaixo. Non se alternan
  formas («xatbot» e «chatbot» no mesmo número).
- **O correcto non se corrixe**: se unha forma parece rara pero a recolle a norma, déixase.

## Catalán

**Norma**: estándar do Institut d'Estudis Catalans (IEC), en rexistro xornalístico.

**Onde consultar**
- [Optimot](https://aplicacions.llengua.gencat.cat/llc/AppJava/index.html): busca á vez no
  dicionario do IEC, nas fichas de dúbidas e na terminoloxía do TERMCAT. É a vía para o TERMCAT,
  cuxa web non deixa ler aos programas.
- [Diccionari de la llengua catalana (DIEC2)](https://dlc.iec.cat/), [Gramàtica (GIEC)](https://giec.iec.cat/)
  e [Ortografia](https://oiec.iec.cat/) do IEC.
- [ésAdir](https://www.esadir.cat/) e o [Llibre d'estil de 3Cat](https://www.3cat.cat/llibredestil/):
  o estilo xornalístico da radio e da televisión públicas.

**Formato**
- Horas con punto: «a les 10.30»; o fuso, «(hora peninsular espanyola, UTC+1)».
- Porcentaxe con espazo: «10 %», como pide o Optimot.
- Millares con punto (115.000); ordinais «4t d'ESO», «1r de batxillerat».
- Cargos, etapas educativas e materias en minúscula («primària», «batxillerat»); os organismos, en
  maiúscula.
- Topónimos con forma catalá tradicional: Saragossa, Osca, la Corunya, Biscaia.

**Vocabulario**
- «el professorat», «l'alumnat»; «soc», sen til.
- IA: «intel·ligència artificial (IA)», «IA generativa», «model de llenguatge gran (LLM)», «agent d'IA»,
  «aprenentatge automàtic», «al·lucinació», «codi obert», «aplicació».
- *Prompt*: «indicació», o termo normalizado polo TERMCAT; a primeira vez, co inglés en cursiva
  entre parénteses: «una indicació (*prompt*)».
- *Chatbot*: «xatbot».

**Calcos que non**: «en base a», «a nivell de». **Correctos, non se cambian**: «degut a», «sí que», «app».

## Galego

**Norma**: normativa da Real Academia Galega (RAG), en rexistro xornalístico.

**Onde consultar**
- [Dicionario da RAG](https://academia.gal/dicionario) e as [Normas ortográficas e
  morfolóxicas](https://publicacions.academia.gal/index.php/rag/catalog/download/252/248/152?inline=1).
- [Na Universidade en galego sen dúbida](https://www.lingua.gal/documents/204205/217676/engalegosendubida.pdf?version=1.0)
  e o [curso de linguaxe administrativa da Xunta](https://www.lingua.gal/documents/204205/217796/01-CURSO-MEDIO-LINGUAXE-ADMINISTRATIVA_v2.pdf?version=1.0):
  números, maiúsculas, topónimos e colocación do pronome.
- [Digalego](https://digalego.xunta.gal/gl) (dicionario con equivalencias), [TERGAL](http://www.cirp.gal/tergal)
  (terminoloxía) e o [Nomenclátor](https://toponimia.xunta.gal/gl) (topónimos de Galicia).

**Formato**
- Horas con punto: «ás 10.30»; o fuso, «(hora peninsular española, UTC+1)».
- Porcentaxe con espazo: «30 %».
- Millares con espazo: «115 000».
- Cargos, días, meses e etapas en minúscula: «educación primaria», «bacharelato», «educación secundaria».
- Topónimos de Cataluña e do País Vasco na súa forma oficial: «Girona», «Donostia».

**Vocabulario**
- «o profesorado», «o alumnado»; coida o xénero («o xiz») e evita os castelanismos («encerado», non
  «pizarra»; «relatorios», non «ponencias»).
- IA: «intelixencia artificial (IA)», «IA xerativa», «modelo de linguaxe (LLM)», «axente de IA»,
  «aprendizaxe automática», «código aberto», «aplicación». Os catro últimos non están no
  dicionario da RAG con este sentido: o diario úsaos así.
- *Prompt*, en cursiva, e explicado a primeira vez como «instrución», como fai a Xunta.

**Gramática que falla a miúdo**
- O pronome vai diante do verbo cando o precede un adverbio ou unha negación sen pausa: «só se
  equivoca», non «só equivócase».
- «Ambos» leva artigo diante do substantivo: «ambos os modelos».

## Éuscaro

**Norma**: éuscaro batua de Euskaltzaindia, en rexistro xornalístico.

**Onde consultar**
- [Normas de Euskaltzaindia](https://www.euskaltzaindia.eus/index.php?option=com_euskaltzaindiarenarauak&view=frontpage&Itemid=1723&lang=eu)
  (cada unha en PDF) e o seu dicionario.
- [Euskalterm](https://www.euskadi.eus/euskalterm/) (terminoloxía), [Elhuyar](https://hiztegiak.elhuyar.eus/)
  e [Labayru](https://hiztegia.labayru.eus/) (dicionarios).
- [Libro de estilo de Berria](https://www.berria.eus/estiloliburua/): o estilo xornalístico.
- [Kalkoen Behatokia](https://www.ehu.eus/ehg/kalkoak/) da UPV/EHU: calcos do castelán.

**Formato** (norma 203 de Euskaltzaindia)
- Horas: «10:30ean»; o fuso, «(Espainiako penintsulako ordua, UTC+1)». Datas: «2026ko azaroaren 13an».
- Porcentaxe co signo diante e espazo: «% 35».
- Millares con espazo: «115 000».
- Cargos en minúscula; organismos e etapas educativas en maiúscula («Lehen Hezkuntza», «Batxilergoa»),
  como manda a norma 200.
- Siglas e nomes declinados sen guión: «AAren», «ElevenLabsen».
- Topónimos: normas 32 (España), 151 (rexións) e 38 (países).

**Vocabulario**
- «irakasleak», «ikasleak»; o diario é «egunkaria», nunca «diarioa»; un centro educativo é
  «ikastetxea», non «zentroa».
- IA: «adimen artifiziala (AA)», «AA sortzailea», «ikaste automatikoa», «kode irekia», «aplikazioa»,
  «txatbota». O modelo de linguaxe e o axente de IA non teñen termo normalizado: o diario usa
  «hizkuntza-eredua» e «AA agentea».
- *Prompt*, en cursiva, sen traducir: non ten termo normalizado.

**Calcos que non**: o «bere» innecesario (Kalkoen Behatokia).

## Inglés

**Norma**: inglés británico, en rexistro xornalístico. O diario é «the paper», nunca «the diary».

**Onde consultar**
- [Guía de estilo de The Guardian](https://www.theguardian.com/guardian-observer-style-guide-a) (cada
  letra na súa páxina) e a da [BBC](https://www.bbc.co.uk/newsstyleguide/all).
- [Guía de estilo para a tradución ao inglés da Comisión Europea](https://knowledge-centre-translation-interpretation.ec.europa.eu/en/resources-translating-eu-documents/guidelines-translating-eu-documents-english),
  co *Country Compendium*: organismos e topónimos de España.
- [IATE](https://iate.europa.eu) (terminoloxía da UE) e o [Oxford Learner's Dictionary](https://www.oxfordlearnersdictionaries.com).

**Formato**
- Datas: «13 November 2026». Horas: «10.30am», como The Guardian; o fuso,
  «10.30am CET (UTC+1)», ou CEST (UTC+2) en verán, e a de fóra coa de orixe: «10am PT (6pm CET, UTC+1)».
- Porcentaxe pegada á cifra: «35%». Millares con coma: «115,000».
- Comiñas inglesas (“ ”), nunca as españolas; ortografía en -ise («organise»).
- Cargos, etapas e organismos xenéricos en minúscula («the education ministry», «secondary education»).
- Topónimos: A Coruña, Lleida, Catalonia, the Basque Country.

**Vocabulario**
- «teachers», «students» ou «pupils».
- IA: «AI», «generative AI», «large language model (LLM)», «AI agent», «machine learning»,
  «hallucination», «open-source» (con guión diante do substantivo), «app».
- O que no orixinal se dixo en inglés cópiase da fonte, non se retraduce.

**O propio de España**
- Un organismo, co seu nome descritivo en inglés e a sigla orixinal: «the Spanish education
  ministry», «Spain's education law (LOMLOE)»; nunca unha sigla inglesa inventada.
- «autonomous community» (comunidade autónoma), «regional education ministry» (consellaría),
  «competitive civil service exam» (oposicións), «vocational training» (FP).
- **Nunca «Year 10» nin outra equivalencia do sistema británico**: os cursos non coinciden. O nome
  español coa idade: «the fourth year of ESO (students aged 15 to 16)», «Bachillerato (the final two
  years of secondary school, ages 16 to 18)».
