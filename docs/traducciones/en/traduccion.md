<!-- origen: 56f62be900e21585 -->
# Educational AI Daily translator's handbook

How Educational AI Daily is translated from Spanish into Catalan, Galician, Basque and English. It is read by every agent that translates anything the public will read, together with the [style guide](estilo.md), which applies equally in every language. Read the general section and the section for the language of each commission.

## For all languages

- **Translate the meaning, in the natural register of each language**, as a journalist writing in that language would: no calques from Spanish in word order, prepositions or expressions.
- **The same content**: the same articles, links, figures, bold and italics as the original. No information is added or removed, except the explanation of anything specific to Spain (below).
- **Names are not translated**: products, applications, companies and the three groups (“Vibe Coding Educativo”, “EduMedia-IAG”). The characters in the cartoon do have a name in each language (`scripts/idiomas.py`).
- **Official foreign material stays in its original language**: the title of a law, a report, a guide. A Spanish body is translated if it has a customary form in the language (the ministry, a regional education department); those with a proper name in their own language are not (Generalitat, Xunta, Ertzaintza). Official acronyms are kept (LOMLOE, INTEF, AEPD).
- **Anything specific to Spain is explained** when readers of that language may not know it, especially in English: an educational stage, the *oposiciones*, an autonomous community.
- **A chart** (`grafico`) is translated in its title, its labels, the names of its series and its note; the type, the unit and the values are left untouched, and the title of the source stays in its original language.
- **A source in another language carries its tag** (“(en castellà)”, “(in Spanish)”), as `scripts/idiomas.py` says.
- **When in doubt, consult the language's reference work** (in its section) and do not settle it from memory. If a work cannot be read, look for the same answer in another one on the list.
- **The same term every time**: the AI vocabulary of each language is fixed below. Forms are not alternated (“bot de conversa” and “chatbot” in the same issue).
- **What is correct is not corrected**: if a form looks odd but the standard accepts it, leave it.

## Catalan

**Standard**: the standard of the Institut d'Estudis Catalans (IEC), in journalistic register.

**Where to look**
- [Optimot](https://aplicacions.llengua.gencat.cat/llc/AppJava/index.html): searches at once the IEC dictionary, the query sheets and the TERMCAT terminology.
- TERMCAT terminology, also with the `buscar_termcat` tool: it searches the dictionaries that TERMCAT publishes openly ([Terminologia oberta](https://www.termcat.cat/ca/terminologia-oberta): the Neoloteca, and those for artificial intelligence, education and computer products) and gives the Catalan term, its equivalents and the definition. A standardised term takes precedence over any other form.
- [Diccionari de la llengua catalana (DIEC2)](https://dlc.iec.cat/), [Gramàtica (GIEC)](https://giec.iec.cat/) and [Ortografia](https://oiec.iec.cat/) of the IEC.
- [ésAdir](https://www.esadir.cat/) and the [Llibre d'estil de 3Cat](https://www.3cat.cat/llibredestil/): the journalistic style of public radio and television.

**Format**
- Times with a full stop: “a les 10.30”; the time zone, “(hora peninsular espanyola, UTC+1)”.
- Percentage with a space: “10 %”, as Optimot requires.
- Thousands with a full stop (115.000); ordinals “4t d'ESO”, “1r de batxillerat”.
- Job titles, educational stages and subjects in lower case (“primària”, “batxillerat”); bodies in upper case.
- Place names in their traditional Catalan form: Saragossa, Osca, la Corunya, Biscaia.

**Vocabulary**
- “el professorat”, “l'alumnat”; “soc”, without an accent.
- AI: “intel·ligència artificial (IA)”, “IA generativa”, “model de llenguatge gran (LLM)”, “agent d'IA”, “aprenentatge automàtic”, “al·lucinació”, “codi obert”, “aplicació”.
- *Prompt*: “indicació”, the term standardised by TERMCAT; the first time, with the English in italics in brackets: “una indicació (*prompt*)”.
- *Chatbot*: “bot de conversa”, the term standardised by TERMCAT.

**Calques to avoid**: “en base a”, “a nivell de”. **Correct, not to be changed**: “degut a”, “sí que”, “app”.

## Galician

**Standard**: the rules of the Real Academia Galega (RAG), in journalistic register.

**Where to look**
- [Dicionario da RAG](https://academia.gal/dicionario) and the [Normas ortográficas e morfolóxicas](https://publicacions.academia.gal/index.php/rag/catalog/download/252/248/152?inline=1).
- [Na Universidade en galego sen dúbida](https://www.lingua.gal/documents/204205/217676/engalegosendubida.pdf?version=1.0) and the [Xunta's course on administrative language](https://www.lingua.gal/documents/204205/217796/01-CURSO-MEDIO-LINGUAXE-ADMINISTRATIVA_v2.pdf?version=1.0): numbers, capital letters, place names and pronoun placement.
- [Digalego](https://digalego.xunta.gal/gl) (a dictionary with equivalents), [TERGAL](http://www.cirp.gal/tergal) (terminology) and the [Nomenclátor](https://toponimia.xunta.gal/gl) (place names in Galicia).

**Format**
- Times with a full stop: “ás 10.30”; the time zone, “(hora peninsular española, UTC+1)”.
- Percentage with a space: “30 %”.
- Thousands with a space: “115 000”.
- Job titles, days, months and stages in lower case: “educación primaria”, “bacharelato”, “educación secundaria”.
- Place names in Catalonia and the Basque Country in their official form: “Girona”, “Donostia”.

**Vocabulary**
- “o profesorado”, “o alumnado”; watch the gender (“o xiz”) and avoid Castilianisms (“encerado”, not “pizarra”; “relatorios”, not “ponencias”).
- AI: “intelixencia artificial (IA)”, “IA xerativa”, “modelo de linguaxe (LLM)”, “axente de IA”, “aprendizaxe automática”, “código aberto”, “aplicación”. The last four are not in the RAG dictionary with this meaning: the paper uses them that way.
- *Prompt*, in italics, and explained the first time as “instrución”, as the Xunta does.

**Grammar that often goes wrong**
- The pronoun goes before the verb when it is preceded by an adverb or a negation with no pause: “só se equivoca”, not “só equivócase”.
- “Ambos” takes an article before the noun: “ambos os modelos”.

## Basque

**Standard**: standard Basque (euskara batua) of Euskaltzaindia, in journalistic register.

**Where to look**
- [Euskaltzaindia's rules](https://www.euskaltzaindia.eus/index.php?option=com_euskaltzaindiarenarauak&view=frontpage&Itemid=1723&lang=eu) (each as a PDF) and its dictionary.
- [Euskalterm](https://www.euskadi.eus/euskalterm/) (terminology), [Elhuyar](https://hiztegiak.elhuyar.eus/) and [Labayru](https://hiztegia.labayru.eus/) (dictionaries).
- [Berria's style guide](https://www.berria.eus/estiloliburua/): journalistic style.
- [Kalkoen Behatokia](https://www.ehu.eus/ehg/kalkoak/) of the UPV/EHU: calques from Spanish.

**Format** (Euskaltzaindia's rule 203)
- Times: “10:30ean”; the time zone, “(Espainiako penintsulako ordua, UTC+1)”. Dates: “2026ko azaroaren 13an”.
- Percentage with the sign first and a space: “% 35”.
- Thousands with a space: “115 000”.
- Job titles in lower case; bodies and educational stages in upper case (“Lehen Hezkuntza”, “Batxilergoa”), as rule 200 requires.
- Acronyms and names declined without a hyphen: “AAren”, “ElevenLabsen”.
- Place names: rules 32 (Spain), 151 (regions) and 38 (countries).

**Vocabulary**
- “irakasleak”, “ikasleak”; the paper is “egunkaria”, never “diarioa”; an educational centre is “ikastetxea”, not “zentroa”.
- AI: “adimen artifiziala (AA)”, “AA sortzailea”, “ikaste automatikoa”, “kode irekia”, “aplikazioa”, “txatbota”. The language model and the AI agent have no standardised term: the paper uses “hizkuntza-eredua” and “AA agentea”.
- *Prompt*, in italics, untranslated: it has no standardised term.

**Calques to avoid**: the unnecessary “bere” (Kalkoen Behatokia).

## English

**Standard**: British English, in journalistic register. The paper is “the paper”, never “the diary”.

**Where to look**
- [The Guardian style guide](https://www.theguardian.com/guardian-observer-style-guide-a) (each letter on its own page) and the [BBC's](https://www.bbc.co.uk/newsstyleguide/all).
- [The European Commission's style guide for translating into English](https://knowledge-centre-translation-interpretation.ec.europa.eu/en/resources-translating-eu-documents/guidelines-translating-eu-documents-english), with the *Country Compendium*: Spanish bodies and place names.
- [IATE](https://iate.europa.eu) (EU terminology) and the [Oxford Learner's Dictionary](https://www.oxfordlearnersdictionaries.com).

**Format**
- Dates: “13 November 2026”. Times: “10.30am”, as The Guardian has it; the time zone, “10.30am CET (UTC+1)”, or CEST (UTC+2) in summer, and a time from elsewhere together with the original: “10am PT (6pm CET, UTC+1)”.
- Percentage attached to the figure: “35%”. Thousands with a comma: “115,000”.
- English quotation marks (“ ”), never the Spanish ones; -ise spelling (“organise”).
- Job titles, stages and generic bodies in lower case (“the education ministry”, “secondary education”).
- Place names: A Coruña, Lleida, Catalonia, the Basque Country.

**Vocabulary**
- “teachers”, “students” or “pupils”.
- AI: “AI”, “generative AI”, “large language model (LLM)”, “AI agent”, “machine learning”, “hallucination”, “open-source” (hyphenated before a noun), “app”.
- Whatever was said in English in the original is copied from the source, not retranslated.

**Anything specific to Spain**
- A body, with its descriptive name in English and the original acronym: “the Spanish education ministry”, “Spain's education law (LOMLOE)”; never an invented English acronym.
- “autonomous community” (comunidad autónoma), “regional education ministry” (consejería), “competitive civil service exam” (oposiciones), “vocational training” (FP).
- **Never “Year 10” or any other equivalence from the British system**: the years do not match. The Spanish name with the age: “the fourth year of ESO (students aged 15 to 16)”, “Bachillerato (the final two years of secondary school, ages 16 to 18)”.
