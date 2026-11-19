<!-- origen: 55be3cd9e913f257 -->
# Style book of Educational AI Daily

How the paper writes. It applies to every agent that writes, reviews, translates or summarises anything the public will
read (articles, briefs, features, “A year ago”, weekly comments, notices, texts for social media and videos) and to the
people who maintain it. It is read in full before starting.

What is common to all of them is here. Each task also has its own guide in `encargos/` with what is specific to it (lengths, format,
tone of the notices, the comic strip…); if a rule here does not apply to a task, its guide says so. The rules that are not about style (what counts as news, what each issue contains and the articles kept
for days without news) are in “How the paper is made”, `docs/como-se-hace.md`.

## Who it is written for

- For teachers and people interested in AI in education who are **not** in the groups. Each
  text must be understood on its own, without having read the messages or other articles: what it is, why it matters to
  a teacher and where to find it.
- **For a very wide public, not for experts**: a teacher of any subject, a family, a
  person starting out with AI. If something is understood only by people who already know the subject, it is rewritten.
- What interests the reader, not how the paper works inside: no agents, files,
  programs or servers in what is published, unless the article is about the paper itself or about
  Anthropic (section “Rigour”).

## Tone

- Formal, informative and impersonal. Never promotional (“incredible”, “essential”, “revolutionises”)
  or alarmist. No exclamation marks or emojis.
- The guides for the notices and the comic strip allow a friendlier tone; never that of an advert.

## Language

- Correct, natural Spanish. The translations have their own section.
- **Inclusive language, but natural**: “el profesorado”, “el alumnado”, “las familias”; without
  doublets or odd symbols.
- **No relative “quien” or “quienes”** in the sense of “the person who”: use “la persona que”, a collective (“el
  profesorado”) or a turn of phrase with the subject first (“separar la creación de la revisión”, not “separar a
  quien crea de quien revisa”). The interrogative, with an accent (“¿quién?”), is fine; a literal quotation is
  left as it is.
- **What the paper publishes are “artículos”**, not “piezas” (the word is only internal, in the
  fields of the files). An article can be a news item, a brief or a feature.
- **What the paper does with a subject: it “publishes” it, it “covers” it**, or the subject “appears in” the paper;
  it does not “tell” it (“cuenta”). “El diario publicó el 3 de noviembre…”, “como recogió el diario…”.
- **AI does not think or want.** No verbs that give a mind or intention to a program (“piensa”,
  “entiende”, “quiere”, “miente”): a model generates, responds or gives a result. What decides is a
  company or a person: “OpenAI ha limitado…”, not “ChatGPT ha decidido…”. What a model makes up is a
  “respuesta inventada” (made-up answer); “alucinación” (hallucination) only when explained.
- **Vocabulary**: “inteligencia artificial” in lower case, and its abbreviation, IA, never AI, except in
  proper names (“Google AI Studio”). “Chatbot” and “alucinar” without quotation marks. “Aplicación” is better than
  “app”, “en línea” than “online”, “enlace” than “link” and “aprendizaje automático” than “machine
  learning”. *Prompt* in italics. A term the reader may not know is explained the first
  time.
- **Acronyms**: a little-known one is spelled out the first time (“la Agencia Española de Protección de
  Datos (AEPD)”); an English technical one (LLM, API, MCP) goes with what it is (“un modelo de lenguaje
  (LLM), el tipo de programa que hay detrás de ChatGPT”). If it is not used again, it is left out.
- **No conditional of rumour**: not “OpenAI habría lanzado…”, but “según [fuente], OpenAI ha
  lanzado…” or “es posible que…”.
- **Clear sentences**: one idea per sentence, the everyday word before the technical one and no
  worn-out metaphors (“cambio de paradigma”, “en la era de la IA”).
- **Clear before brief.** No compressed expressions that force a second reading: chains of nouns
  (“flujo de generación multimodal con verificación cruzada”), jargon from the groups,
  words taken for granted or sentences missing their verb. If a short sentence is understood
  less well than a slightly longer one, the longer one wins: “un sistema que crea imágenes y vídeo y comprueba el
  resultado con otro modelo”.
- The names of products, apps, groups and documents are written as the company or the person who makes them writes them
  (“ChatGPT”, “Vibe Coding Educativo”). A resource in Catalan or another language is described in Spanish
  and keeps its name; the title of a work stays in its language.

## Headlines, kickers and standfirsts

- **Headline**: clear, with a verb, with no questions or hooks (“you won’t believe…”). It says what the subject
  contributes, not just the name of the tool or the document. **At most 90 characters**, counting
  spaces: whatever does not fit goes in the kicker or the standfirst.
- **Kicker**: two to five words, with no verb: the type of thing or the field (“Guía oficial”,
  “Nuevo en el repositorio”, “Del fondo de EduMedia”).
- **Standfirst**: one or two sentences that sum up the article (two or three in a feature). It does not repeat the
  headline: it adds what comes next.
- **The headline and the standfirst do not say more than the body or the source.** What the body
  qualifies (“according to the company”, “on paid plans”, “it is the author’s hypothesis”) does not disappear
  at the top. A test with nothing to compare against does not “prove” or “suggest” a cause.
- **What is not from these days carries its date in the headline**: a report from August is not “published”
  today; it is “Un informe de agosto…”.

## People

- **Topics, not people.** The people who give opinions or ask questions in the groups are not named, not even with “a
  member said…”: the positions are gathered.
- **The author of a resource they have published themselves is named** (an app, a guide, a
  document), as a credit (“creada por…”), with the name that appears on the resource itself or the full
  name of the person who publishes it. A first name does not identify anyone: if the resource does not
  say who makes it, “su autor” is used, and it is said that the website does not indicate it. A surname is never completed.
- **Who is who is told by the mark on the material, not by the name** (ADR 0066): the authors of the paper
  are only the messages marked `[autor del diario: …]`; another person with the same first name is
  another person. The marks are not published.
- **The authors of the paper, like anyone else**: they are named as credit for their resources just like the
  others, with the full name they sign the paper with, even if they use another in the groups.
- **Roles are mentioned only if they have to do with the news** (administering a group, being co-author of the
  paper): otherwise the person is just another teacher.
- **If the article is about the paper itself, it says so** in those words (“este diario”).
- **Students**: nothing that identifies them is published (name, image, or school and year together),
  even if they appear in the shared material. Of a tool for the classroom it is said, according to its
  terms, whether it asks for student data and whether it uses them to train its models; if that is not stated, that is said.

## Rigour

- **Every claim is checked against the original source**: the official announcement, the product page,
  the government document. A message in the group, a link to X or a video is not enough.
- **What cannot be checked is removed or stated as unconfirmed.** No inventing
  dates, figures, authors or features.
- **What a company announces, with its conditions**: on which plan, at what price, until when, in which
  countries. “Free” or “for everyone” is checked against its conditions.
- **Company language, attributed or left out**: “revolutionary”, “powerful” or “unprecedented”
  only inside an attributed quotation; the text says what the product does. A study or a
  survey is presented with who carries it out and who pays for it, and if it is the company’s own, that is said
  (“según un estudio de la propia OpenAI”). A press release is not reproduced: it is identified and
  rewritten.
- **When an article is about Anthropic or Claude**, one sentence reminds readers that the paper is written by
  Claude agents, so that they can bear it in mind. Naming them in passing, in a list, does not call for it.
- **Figures, with the precision of the source** (no decimals the source does not give) and a proportion
  with its absolute quantity (“el doble, de 10 a 20 centros”). If the source gives different figures depending on
  the version or the plan, it is said which each one corresponds to. From 20% to 30% is 10 points more, not
  10% more. “Uno de cada ocho docentes” is better than “el 12,5 %”.
- **Data that change are dated** (“a 1 de noviembre de 2026”); the rest carries no date.
- **Every time, with its time zone**, because the paper is read all over the world (ADR 0091). The Spanish one:
  “a las 10:30 (hora peninsular española, UTC+1)”, UTC+2 in summer; “peninsular”, because the Canary Islands are
  an hour behind. One from elsewhere, with the local time and the equivalent in Spain: “a las 10:00 de
  California (19:00 en la España peninsular, UTC+1)”. If a text gives several times for the same place, the
  time zone goes the first time.
- **An official page may be out of date**: if it contradicts what the paper has already published with
  the document in front of it, what was published prevails, and that is said.
- **Before judging a link, open it**: the address does not say what is on the page or its date.
- **What the paper has already published, the same**: an article on a subject already covered gives the same
  figures and dates as the earlier one, links to it and, if something has changed, says so.

## Quotations and other languages

- Short, exact quotations, in quotation marks, and few: the article explains, it does not copy.
- **What is in quotation marks is looked up word for word in the source**; if it does not appear, it is removed or
  paraphrased. A sentence taken from a source goes in quotation marks or is rewritten.
- **No quotation only in English**: either translated, or with the translation alongside in brackets.
- Official material from others keeps its original language (the title of a regulation or a report).

## Sources and links

The detail is in `encargos/enlaces.md`; the essentials:

- **What is named is linked where it is named**, at its first mention and with its name as the text of the
  link; at the foot, in `fuentes`, all of them.
- **To the original, official source**, in Spanish (or Catalan) if that version exists; a
  tool, to the website the reader will use, not to its code repository.
- **What has already been published and is clearly related is linked**, with its key (`pieza:AAAA-MM-DD/id`),
  with text that says what it is about, never “here”.
- The text of a link is never “mensaje 123” or a bare address.
- A link that downloads a file says so: “la guía (PDF)”.

## Form

- **Spanish quotation marks** (the angle-bracket kind); inside them, English ones (“ ”).
- **The percentage, with a space between figure and sign** (as Spanish writes “25 %”); thousands with a full stop (1.200); currencies by
  name (“10 dólares”, “4 euros”).
- Paragraphs of three to six sentences in long texts (each guide gives its length). Bold used sparingly:
  two or three ideas in a long text.
- Links in Markdown (`[texto](url)`); in the texts for notices and social media, plain text (their
  guides say so).
- **Never “hoy”, “ayer” or “esta semana”**: the date or the day (“el jueves 12”). The issue comes out the day
  after the conversations and stays in the archive; what is kept for another day (the reserve,
  “A year ago” written in advance) does not say “acaba de” either.

## Charts

- **A chart only when it explains something the text does not let you see at a glance**: three or more comparable figures
  from the same source (the results of a study, a survey, a change over time). Not for decoration or
  for one or two figures, which are given in the text.
- **The paper’s program draws it from the data** (the `grafico` field of the article or of the section of the
  feature, ADR 0084), never an agent by hand: horizontal bars (`barras`, for comparing), columns
  (`columnas`, for a few categories with short labels) or lines (`lineas`, for a change over time).
- **The data, exact and from a single source**: the same values the source gives, with their precision, and the same
  unit for all. Bars always start at zero (the program does this itself); no mixing in a chart
  figures from different sources.
- **A title that says what is measured**, not the conclusion (“Redacciones humanas que los detectores tomaron por IA”), and
  short labels.
- **The source, always**, linked; and in the note, what is needed to read it properly: how many people or cases, from
  where and when, and whether the data come from the company itself (“según la empresa”).

## The translations

Each edition is translated into Catalan, Galician, Basque and English, with the same criteria as
Spanish and in the natural register of each language, not calqued. How it is done in each language (standard,
where to look things up, formats, AI vocabulary and what is specific to Spain) is in the translator’s book,
`encargos/traduccion.md`.

## Corrections

- An error is corrected without waiting for anyone to ask, in the same article and in all five languages, with
  its note at the end (ADR 0055): “Corregido el…” (there was an error), “Actualización del…” (the figure was
  correct and has changed) or “Nota añadida el…” (something was missing). A typo that does not change the meaning is
  corrected without a note.
- If the error was in the headline, in the notices or on social media, the correction goes there too.
- An article is not withdrawn entirely if changing one part is enough.

## What is checked without AI

Some programs go over a number of these rules every night (ADR 0056, 0059 and 0067), but they do not replace
the reviewer:

- `scripts/revisar-estilo.py`: the relative “quien”, quotations only in English and the rules of vocabulary and
  form that can be searched for (“hoy”, “pieza”, “el diario cuenta”, “app”, the conditional of rumour, the
  percentage); what it finds is corrected by an agent.
- `scripts/comprobar-corrector.py`: that the style corrector, an agent that goes over the wording of the day’s articles
  every night, has not changed any data.
- `scripts/corregir-erratas.py`: “e” before “i”, “u” before “o”, Spanish quotation marks in English, and it warns
  of headlines of more than 90 characters.
- `scripts/revisar-idiomas.py`: Spanish that has slipped into a translation.
- `scripts/revisar-autoria.py`: what is attributed to an author of the paper that belongs to another account.
