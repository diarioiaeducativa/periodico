<!-- origen: 56f62be900e21585 -->
# Llibre del traductor del Diari d'IA Educativa

Com es tradueix el diari del castellà al català, al gallec, a l'èuscar i a l'anglès. El llegeixen tots els
agents que tradueixen alguna cosa que ha de llegir el públic, a més del [llibre d'estil](estilo.md), que val
igual en totes les llengües. Es llegeix l'apartat general i el de la llengua de cada encàrrec.

## Per a totes les llengües

- **Es tradueix el sentit, en el registre natural de cada llengua**, com l'escriuria un periodista
  d'aquesta llengua: sense calcs del castellà en l'ordre de les paraules, les preposicions ni les
  expressions.
- **El mateix contingut**: els mateixos articles, enllaços, xifres, negretes i cursives que l'original.
  No s'afegeix ni se suprimeix informació, tret de l'explicació del que és propi d'Espanya (més avall).
- **Els noms no es tradueixen**: productes, aplicacions, empreses i els tres grups («Vibe Coding
  Educativo», «EduMedia-IAG»). Els personatges de la vinyeta sí que tenen nom en cada llengua
  (`scripts/idiomas.py`).
- **Allò oficial aliè es queda en la llengua original**: el títol d'una llei, d'un informe, d'una guia.
  Un organisme espanyol es tradueix si té forma habitual en la llengua (el ministeri, una conselleria);
  els que tenen nom propi en la seva llengua no (Generalitat, Xunta, Ertzaintza). Les sigles oficials
  es mantenen (LOMLOE, INTEF, AEPD).
- **El que és propi d'Espanya s'explica** quan el lector d'aquesta llengua pot no conèixer-ho, sobretot
  en anglès: una etapa educativa, les oposicions, una comunitat autònoma.
- **Un gràfic** (`grafico`) es tradueix en el títol, les etiquetes, els noms de les sèries i la nota; el
  tipus, la unitat i els valors no es toquen, i el títol de la font es queda en la llengua original.
- **Una font en una altra llengua porta la seva marca** («(en castellà)», «(in Spanish)»), com diu
  `scripts/idiomas.py`.
- **Davant d'un dubte, es consulta l'obra de referència de la llengua** (en el seu apartat) i no es resol
  de memòria. Si una obra no deixa llegir, es busca la mateixa resposta en una altra de la llista.
- **El mateix terme sempre**: el lèxic de la IA de cada llengua està fixat a sota. No s'alternen
  formes («bot de conversa» i «chatbot» en el mateix número).
- **Allò correcte no es corregeix**: si una forma sembla estranya però la recull la norma, es deixa.

## Català

**Norma**: estàndard de l'Institut d'Estudis Catalans (IEC), en registre periodístic.

**On consultar**
- [Optimot](https://aplicacions.llengua.gencat.cat/llc/AppJava/index.html): cerca alhora en el
  diccionari de l'IEC, en les fitxes de dubtes i en la terminologia del TERMCAT.
- La terminologia del TERMCAT, també amb l'eina `buscar_termcat`: cerca en els diccionaris que el TERMCAT
  publica en obert ([Terminologia oberta](https://www.termcat.cat/ca/terminologia-oberta): la Neoloteca, la
  d'intel·ligència artificial, la d'educació i la de productes informàtics) i dona el terme català, els seus
  equivalents i la definició. Un terme normalitzat preval sobre qualsevol altra forma.
- [Diccionari de la llengua catalana (DIEC2)](https://dlc.iec.cat/), [Gramàtica (GIEC)](https://giec.iec.cat/)
  i [Ortografia](https://oiec.iec.cat/) de l'IEC.
- [ésAdir](https://www.esadir.cat/) i el [Llibre d'estil de 3Cat](https://www.3cat.cat/llibredestil/):
  l'estil periodístic de la ràdio i la televisió públiques.

**Format**
- Hores amb punt: «a les 10.30»; el fus, «(hora peninsular espanyola, UTC+1)».
- Percentatge amb espai: «10 %», com demana l'Optimot.
- Milers amb punt (115.000); ordinals «4t d'ESO», «1r de batxillerat».
- Càrrecs, etapes educatives i assignatures en minúscula («primària», «batxillerat»); els organismes, en
  majúscula.
- Topònims amb forma catalana tradicional: Saragossa, Osca, la Corunya, Biscaia.

**Vocabulari**
- «el professorat», «l'alumnat»; «soc», sense accent.
- IA: «intel·ligència artificial (IA)», «IA generativa», «model de llenguatge gran (LLM)», «agent d'IA»,
  «aprenentatge automàtic», «al·lucinació», «codi obert», «aplicació».
- *Prompt*: «indicació», el terme normalitzat pel TERMCAT; la primera vegada, amb l'anglès en cursiva
  entre parèntesis: «una indicació (*prompt*)».
- *Chatbot*: «bot de conversa», el terme normalitzat pel TERMCAT.

**Calcs que no**: «en base a», «a nivell de». **Correctes, no es canvien**: «degut a», «sí que», «app».

## Gallec

**Norma**: normativa de la Real Academia Galega (RAG), en registre periodístic.

**On consultar**
- [Dicionario da RAG](https://academia.gal/dicionario) i les [Normas ortográficas e
  morfolóxicas](https://publicacions.academia.gal/index.php/rag/catalog/download/252/248/152?inline=1).
- [Na Universidade en galego sen dúbida](https://www.lingua.gal/documents/204205/217676/engalegosendubida.pdf?version=1.0)
  i el [curs de llenguatge administratiu de la Xunta](https://www.lingua.gal/documents/204205/217796/01-CURSO-MEDIO-LINGUAXE-ADMINISTRATIVA_v2.pdf?version=1.0):
  números, majúscules, topònims i col·locació del pronom.
- [Digalego](https://digalego.xunta.gal/gl) (diccionari amb equivalències), [TERGAL](http://www.cirp.gal/tergal)
  (terminologia) i el [Nomenclátor](https://toponimia.xunta.gal/gl) (topònims de Galícia).

**Format**
- Hores amb punt: «ás 10.30»; el fus, «(hora peninsular española, UTC+1)».
- Percentatge amb espai: «30 %».
- Milers amb espai: «115 000».
- Càrrecs, dies, mesos i etapes en minúscula: «educación primaria», «bacharelato», «educación secundaria».
- Topònims de Catalunya i del País Basc en la seva forma oficial: «Girona», «Donostia».

**Vocabulari**
- «o profesorado», «o alumnado»; cura el gènere («o xiz») i evita els castellanismes («encerado», no
  «pizarra»; «relatorios», no «ponencias»).
- IA: «intelixencia artificial (IA)», «IA xerativa», «modelo de linguaxe (LLM)», «axente de IA»,
  «aprendizaxe automática», «código aberto», «aplicación». Els quatre últims no són en el
  diccionari de la RAG amb aquest sentit: el diari els usa així.
- *Prompt*, en cursiva, i explicat la primera vegada com a «instrución», com fa la Xunta.

**Gramàtica que falla sovint**
- El pronom va davant del verb quan el precedeix un adverbi o una negació sense pausa: «só se
  equivoca», no «só equivócase».
- «Ambos» porta article davant del substantiu: «ambos os modelos».

## Èuscar

**Norma**: èuscar batua d'Euskaltzaindia, en registre periodístic.

**On consultar**
- [Normes d'Euskaltzaindia](https://www.euskaltzaindia.eus/index.php?option=com_euskaltzaindiarenarauak&view=frontpage&Itemid=1723&lang=eu)
  (cadascuna en PDF) i el seu diccionari.
- [Euskalterm](https://www.euskadi.eus/euskalterm/) (terminologia), [Elhuyar](https://hiztegiak.elhuyar.eus/)
  i [Labayru](https://hiztegia.labayru.eus/) (diccionaris).
- [Llibre d'estil de Berria](https://www.berria.eus/estiloliburua/): l'estil periodístic.
- [Kalkoen Behatokia](https://www.ehu.eus/ehg/kalkoak/) de la UPV/EHU: calcs del castellà.

**Format** (norma 203 d'Euskaltzaindia)
- Hores: «10:30ean»; el fus, «(Espainiako penintsulako ordua, UTC+1)». Dates: «2026ko azaroaren 13an».
- Percentatge amb el signe al davant i espai: «% 35».
- Milers amb espai: «115 000».
- Càrrecs en minúscula; organismes i etapes educatives en majúscula («Lehen Hezkuntza», «Batxilergoa»),
  com mana la norma 200.
- Sigles i noms declinats sense guionet: «AAren», «ElevenLabsen».
- Topònims: normes 32 (Espanya), 151 (regions) i 38 (països).

**Vocabulari**
- «irakasleak», «ikasleak»; el diari és «egunkaria», mai «diarioa»; un centre educatiu és
  «ikastetxea», no «zentroa».
- IA: «adimen artifiziala (AA)», «AA sortzailea», «ikaste automatikoa», «kode irekia», «aplikazioa»,
  «txatbota». El model de llenguatge i l'agent d'IA no tenen terme normalitzat: el diari usa
  «hizkuntza-eredua» i «AA agentea».
- *Prompt*, en cursiva, sense traduir: no té terme normalitzat.

**Calcs que no**: el «bere» innecessari (Kalkoen Behatokia).

## Anglès

**Norma**: anglès britànic, en registre periodístic. El diari és «the paper», mai «the diary».

**On consultar**
- [Guia d'estil de The Guardian](https://www.theguardian.com/guardian-observer-style-guide-a) (cada
  lletra en la seva pàgina) i la de la [BBC](https://www.bbc.co.uk/newsstyleguide/all).
- [Guia d'estil per a la traducció a l'anglès de la Comissió Europea](https://knowledge-centre-translation-interpretation.ec.europa.eu/en/resources-translating-eu-documents/guidelines-translating-eu-documents-english),
  amb el *Country Compendium*: organismes i topònims d'Espanya.
- [IATE](https://iate.europa.eu) (terminologia de la UE) i l'[Oxford Learner's Dictionary](https://www.oxfordlearnersdictionaries.com).

**Format**
- Dates: «13 November 2026». Hores: «10.30am», com The Guardian; el fus,
  «10.30am CET (UTC+1)», o CEST (UTC+2) a l'estiu, i la de fora amb la d'origen: «10am PT (6pm CET, UTC+1)».
- Percentatge enganxat a la xifra: «35%». Milers amb coma: «115,000».
- Cometes angleses (“ ”), mai les espanyoles; ortografia en -ise («organise»).
- Càrrecs, etapes i organismes genèrics en minúscula («the education ministry», «secondary education»).
- Topònims: A Coruña, Lleida, Catalonia, the Basque Country.

**Vocabulari**
- «teachers», «students» o «pupils».
- IA: «AI», «generative AI», «large language model (LLM)», «AI agent», «machine learning»,
  «hallucination», «open-source» (amb guionet davant del substantiu), «app».
- Allò que en l'original es va dir en anglès es copia de la font, no es retradueix.

**El que és propi d'Espanya**
- Un organisme, amb el seu nom descriptiu en anglès i la sigla original: «the Spanish education
  ministry», «Spain's education law (LOMLOE)»; mai una sigla anglesa inventada.
- «autonomous community» (comunitat autònoma), «regional education ministry» (conselleria),
  «competitive civil service exam» (oposicions), «vocational training» (FP).
- **Mai «Year 10» ni una altra equivalència del sistema britànic**: els cursos no coincideixen. El nom
  espanyol amb l'edat: «the fourth year of ESO (students aged 15 to 16)», «Bachillerato (the final two
  years of secondary school, ages 16 to 18)».
