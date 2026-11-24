<!-- origen: 6ee240bd1246571c -->
# Llibre d'estil del Diari d'IA Educativa

Com escriu el diari. Val per a tot agent que escriu, revisa, tradueix o resumeix alguna cosa que llegirà el
públic (articles, breus, reportatges, «Fa un any», comentaris de la setmana, avisos, textos per a xarxes i
vídeos) i per a les persones que el mantenen. Es llegeix sencer abans de començar.

Aquí hi ha el que és comú. Cada tasca té a més la seva guia a `encargos/` amb el que li és propi (mides, format,
to dels avisos, la vinyeta…); si una norma d'aquí no val per a una tasca, la seva guia ho diu. Les normes que no són d'estil (què és notícia, què porta cada número i els articles guardats
per als dies sense notícies) són a «Com es fa el diari», `docs/como-se-hace.md`.

## Per a qui s'escriu

- Per a docents i persones interessades en la IA en educació que **no són** als grups. Cada
  text s'entén sol, sense haver llegit els missatges ni altres articles: què és, per què importa a
  un docent i on trobar-ho.
- **Per a un públic molt ampli, no per a experts**: un docent de qualsevol matèria, una família, una
  persona que comença amb la IA. Si alguna cosa només l'entenen les persones que ja saben del tema, es reescriu.
- El que interessa al lector, no com funciona el diari per dins: res d'agents, fitxers,
  programes ni servidors en el que es publica, tret que l'article tracti del diari mateix o
  d'Anthropic (apartat «Rigor»).

## To

- Formal, informatiu i impersonal. Mai publicitari («increíble», «imprescindible», «revoluciona»)
  ni alarmista. Sense exclamacions ni emojis.
- Les guies dels avisos i de la vinyeta permeten un to més proper; mai d'anunci.

## Llengua

- Castellà correcte i natural. Les traduccions, al seu apartat.
- **Llenguatge inclusiu, però natural**: «el profesorado», «el alumnado», «las familias»; sense
  desdoblaments ni signes estranys.
- **Sense el relatiu «quien» o «quienes»** amb el sentit de «la persona que»: «la persona que», un col·lectiu («el
  profesorado») o un gir amb l'assumpte al davant («separar la creación de la revisión», no «separar a
  quien crea de quien revisa»). L'interrogatiu, amb accent («¿quién?»), sí; una cita literal es
  deixa tal com és.
- **El que publica el diari són «artículos»**, no «piezas» (la paraula només és interna, als
  camps dels fitxers). Un article pot ser una notícia, un breu, un reportatge.
- **El que fa el diari amb un tema: el «publica», el «recoge»** o el tema «sale en» el diari;
  no el «cuenta». «El diario publicó el 3 de noviembre…», «como recogió el diario…».
- **La IA no pensa ni vol.** Res de verbs que donen ment o intenció a un programa («piensa»,
  «entiende», «quiere», «miente»): un model genera, respon o dona un resultat. El que decideix és una
  empresa o una persona: «OpenAI ha limitado…», no «ChatGPT ha decidido…». El que un model s'inventa
  és una «respuesta inventada»; «alucinación», només explicada.
- **Vocabulari**: «inteligencia artificial», en minúscula, i la seva sigla, IA, mai AI, tret de
  noms propis («Google AI Studio»). «Chatbot» i «alucinar», sense cometes. Millor «aplicación» que
  «app», «en línea» que «online», «enlace» que «link» i «aprendizaje automático» que «machine
  learning». *Prompt*, en cursiva. Un terme que el lector pot no conèixer s'explica la primera
  vegada.
- **Sigles**: una de poc coneguda es desenvolupa la primera vegada («la Agencia Española de Protección de
  Datos (AEPD)»); una de tècnica anglesa (LLM, API, MCP) va amb el que és («un modelo de lenguaje
  (LLM), el tipo de programa que hay detrás de ChatGPT»). Si no es torna a usar, no es posa.
- **Sense condicional de rumor**: no «OpenAI habría lanzado…», sinó «según [fuente], OpenAI ha
  lanzado…» o «es posible que…».
- **Frases clares**: una idea per frase, la paraula corrent abans que la tècnica i fora les
  metàfores gastades («cambio de paradigma», «en la era de la IA»).
- **Abans clar que breu.** Res d'expressions comprimides que obliguen a rellegir: substantius
  encadenats («flujo de generación multimodal con verificación cruzada»), argot dels grups,
  paraules que es donen per sabudes o frases a les quals falta el verb. Si una frase curta s'entén
  pitjor que una de una mica més llarga, va la llarga: «un sistema que crea imágenes y vídeo y comprueba el
  resultado con otro modelo».
- Els noms de productes, aplicacions, grups i documents, tal com els escriu l'empresa o la persona que els fa
  («ChatGPT», «Vibe Coding Educativo»). Un recurs en català o en una altra llengua es descriu en castellà
  i conserva el seu nom; el títol d'una obra queda en el seu idioma.
- **Amb el seu nom d'ara**, encara que el missatge o la font faci servir l'antic: NotebookLM es diu Gemini Notebook
  des del 16 de juliol de 2026. La primera vegada, si ajuda a reconèixer-lo, «Gemini Notebook (antes NotebookLM)»;
  «Fa un any» usa el d'aleshores, perquè parla d'aleshores.

## Titulars, antetítols i entradetes

- **Titular**: clar, amb verb, sense preguntes ni ganxos («no creerás…»). Diu què aporta el que
  recull, no només el nom de l'eina o del document. **Com a molt 90 caràcters**, comptant
  els espais: el que no càpiga va a l'antetítol o a l'entradeta. Sense abusar de l'arrencada «Un…» o
  «Una…» («Un buscador permite…»): de tant en tant val, però millor començar pel que canvia o per qui
  actua («Las orientaciones de privacidad del INTEF pasan del PDF a una web con buscador y filtros»).
- **Antetítol**: de dues a cinc paraules, sense verb: el tipus de cosa o l'àmbit («Guía oficial»,
  «Nuevo en el repositorio», «Del fondo de EduMedia»). Com en els ladillos, ni comença per «Qué», «Lo que», «Cómo»
  o «Por qué» ni porta «lo» amb un participi o un adjectiu: «Estudios sobre IA y aprendizaje», no «Lo que dice la
  investigación».
- **Entradeta**: una o dues frases que resumeixen l'article (dues o tres en el reportatge). No repeteix el
  titular: aporta el següent.
- **El titular i l'entradeta no diuen més que el cos ni que la font.** El que el cos
  matisa («según la empresa», «en los planes de pago», «es una hipótesis del autor») no desapareix
  a dalt. Una prova sense res amb què comparar no «demuestra» ni «sugiere» una causa.
- **Ladillos** (els títols dels apartats d'un reportatge): un titular petit que diu el que explica el seu apartat
  (qui fa què, la dada), amb verb si es pot i com a molt 60 caràcters: «La revisión de Stanford solo admite
  estudios causales», no «Qué cuenta como prueba». Res d'etiquetes que valdrien per a qualsevol text: ni començar
  per «Qué», «Lo que», «Cómo» o «Por qué», ni parelles abstractes («Entender o entregar», «El medio y el método»,
  «Del producto al proceso»), ni «Más allá de…», ni «lo» amb un participi o un adjectiu, sigui on sigui («lo aprendido», «lo importante»).
  Cap no repeteix el d'un altre reportatge.
- **El que no és d'aquests dies porta la seva data al titular**: un informe d'agost no «es publica»
  avui, és «Un informe de agosto…».

## Persones

- **Temes, no persones.** No es nomena les persones que opinen o pregunten als grups, tampoc amb «un
  membre va dir…»: es recullen les postures.
- **Es nomena l'autor d'un recurs que ell mateix ha publicat** (una aplicació, una guia, un
  document), com a crèdit («creada por…»), amb el nom que consta en el mateix recurs o el
  nom complet de la persona que el publica. Un nom de pila no identifica ningú: si el recurs no
  diu qui el fa, «su autor», i que la web no ho indica. Mai no es completa un cognom.
- **Qui és qui ho diu la marca del material, no el nom** (ADR 0066): els autors del diari
  són només els missatges marcats `[autor del diario: …]`; una altra persona amb el mateix nom de pila és
  una altra persona. Les marques no es publiquen.
- **Els autors del diari, com qualsevol**: es nomenen com a crèdit dels seus recursos igual que els
  altres, amb el nom complet amb què signen el diari, encara que als grups en facin servir un altre.
- **Els càrrecs, només si tenen a veure amb la notícia** (administrar un grup, ser responsable del
  diari): si no, la persona és un docent més. Que un recurs sigui d'un autor del diari no fa que hi tingui
  a veure: «responsable de este diario» només hi va si l'article tracta del diari mateix.
- **Si l'article tracta del diari mateix, ho diu** amb aquestes paraules («este diario»).
- **L'alumnat**: no es publica res que l'identifiqui (nom, imatge, ni centre i curs junts),
  encara que aparegui en el material compartit. D'una eina per a l'aula es diu, segons les seves
  condicions, si demana dades de l'alumnat i si les fa servir per entrenar els seus models; si no consta, es diu.

## Rigor

- **Cada afirmació es comprova a la font original**: l'anunci oficial, la pàgina del producte,
  el document de l'administració. Un missatge del grup, un enllaç a X o un vídeo no basten.
- **El que no es pot comprovar, es treu o es diu com a no confirmat.** Res d'inventar
  dates, xifres, autors ni funcions.
- **El que anuncia una empresa, amb les seves condicions**: en quin pla, a quin preu, fins quan, en quins
  països. «Gratis» o «para todos» es contrasta amb les seves condicions.
- **El llenguatge de les empreses, atribuït o fora**: «revolucionario», «potente» o «sin
  precedentes», només dins d'una cita atribuïda; el text diu què fa el producte. Un estudi o una
  enquesta es presenta amb qui el fa i qui el paga, i si és de la mateixa empresa, es diu
  («según un estudio de la propia OpenAI»). Una nota de premsa no es reprodueix: s'identifica i es
  reescriu.
- **Quan un article tracta d'Anthropic o de Claude**, una frase recorda que el diari l'escriuen
  agents de Claude, perquè el lector ho tingui en compte. Anomenar-los de passada, en una llista, no ho demana.
- **Les xifres, amb la precisió de la font** (sense decimals que la font no dona) i una proporció
  amb la seva quantitat absoluta («el doble, de 10 a 20 centros»). Si la font dona xifres diferents segons
  la versió o el pla, es diu a quina correspon cada una. Del 20 % al 30 % són 10 punts més, no
  un 10 % més. Millor «uno de cada ocho docentes» que «el 12,5 %».
- **Una norma, aplicada al cas**: si l'article explica el que exigeix una llei o una autoritat, diu també
  què suposa per al que tracta (si cal permís, un avís o res), i no deixa que el lector tregui la
  conclusió (Juanjo, 19-11-2026, davant les condicions de l'AEPD a la peça d'Umami: «debes hacerlo tú»).
- **Les dades que canvien es daten** («a 1 de noviembre de 2026»); la resta no porta data.
- **Tota hora, amb el seu fus**, perquè el diari es llegeix a tot el món (ADR 0091). La d'Espanya:
  «a les 10.30 (hora peninsular espanyola, UTC+1)», UTC+2 a l'estiu; «peninsular», perquè Canàries va
  una hora per darrere. La de fora, amb la d'origen i l'equivalent a Espanya: «a les 10.00 de
  Califòrnia (19.00 a l'Espanya peninsular, UTC+1)». Si un text dona diverses hores del mateix lloc, el
  fus hi va la primera vegada.
- **Una pàgina oficial pot estar desactualitzada**: si contradiu el que el diari ja va publicar amb el
  document al davant, mana el publicat, i es diu.
- **Abans de jutjar un enllaç, s'obre**: l'adreça no diu el que hi ha a la pàgina ni la seva data.
- **El que el diari ja va publicar, igual**: un article sobre un assumpte ja tractat dona les mateixes
  xifres i dates que l'anterior, l'enllaça i, si alguna cosa ha canviat, ho diu.

## Cites i altres idiomes

- Cites breus i exactes, entre cometes, i poques: l'article explica, no copia.
- **El que va entre cometes es busca tal qual a la font**; si no hi apareix, es treu o es
  parafrasea. Una frase presa d'una font va entre cometes o es reescriu.
- **Cap cita només en anglès**: o traduïda, o amb la traducció al costat entre parèntesis.
- El que és oficial i d'altri (el títol d'una norma, d'un informe) queda en el seu idioma original.

## Fonts i enllaços

El detall és a `encargos/enlaces.md`; l'essencial:

- **El que es nomena s'enllaça on es nomena**, en la seva primera menció i amb el seu nom com a text de
  l'enllaç; al peu, a `fuentes`, totes.
- **A la font original i oficial**, en castellà (o en català) si existeix aquesta versió; una
  eina, a la web que farà servir el lector, no al seu repositori de codi.
- **El que ja s'ha publicat i està clarament relacionat, enllaçat** amb la seva clau (`pieza:AAAA-MM-DD/id`),
  amb un text que digui de què tracta, mai «aquí».
- El text d'un enllaç mai no és «mensaje 123» ni una adreça nua.
- Un enllaç que descarrega un fitxer ho diu: «la guía (PDF)».

## Forma

- **Cometes espanyoles** («»); dins d'elles, les angleses (“”).
- **El percentatge, amb espai** (25 %); els milers, amb punt (1.200); les monedes, amb el seu nom
  («10 dólares», «4 euros»).
- Paràgrafs de tres a sis frases en els textos llargs (cada guia dona la seva mida). Negretes amb mesura:
  dues o tres idees en un text llarg.
- Enllaços en Markdown (`[texto](url)`); en els textos per a avisos i xarxes, text pla (ho diuen les seves
  guies).
- **Mai «hoy», «ayer» ni «esta semana»**: la data o el dia («el jueves 12»). El número surt el dia
  següent de les converses i queda a la hemeroteca; el que es guarda per a un altre dia (la reserva,
  «Fa un any» escrit per avançat) tampoc no diu «acaba de».

## Gràfics

- **Un gràfic, només quan explica alguna cosa que el text no deixa veure d'un cop d'ull**: tres o més xifres comparables
  de la mateixa font (els resultats d'un estudi, una enquesta, una evolució en el temps). No per adornar ni
  per a una o dues xifres, que es diuen al text.
- **El dibuixa el programa del diari a partir de les dades** (el camp `grafico` de l'article o de l'apartat del
  reportatge, ADR 0084), mai un agent a mà: barres horitzontals (`barras`, per comparar), columnes
  (`columnas`, per a poques categories amb etiquetes curtes) o línies (`lineas`, per a una evolució).
- **Les dades, exactes i d'una sola font**: els mateixos valors que dona la font, amb la seva precisió, i la mateixa
  unitat per a tots. Les barres comencen sempre en zero (el programa ho fa sol); res de barrejar en un gràfic
  xifres de fonts diferents.
- **Títol que diu què es mesura**, no la conclusió («Redacciones humanas que los detectores tomaron por IA»), i
  etiquetes curtes.
- **La font, sempre**, enllaçada; i a la nota, el que cal per llegir-ho bé: quantes persones o casos, d'on i
  quan, i si les dades són de la mateixa empresa («según la empresa»).

## Les traduccions

Cada edició es tradueix al català, al gallec, a l'euskera i a l'anglès, amb el mateix criteri que el
castellà i en el registre natural de cada llengua, no calcat. Com es fa en cada llengua (norma,
on consultar, formats, vocabulari de la IA i el que és propi d'Espanya) és al llibre del traductor,
`encargos/traduccion.md`.

## Correccions

- Un error es corregeix sense esperar que ningú ho demani, en el mateix article i en els cinc idiomes, amb
  la seva nota al final (ADR 0055): «Corregido el…» (hi havia un error), «Actualización del…» (la dada era
  certa i ha canviat) o «Nota añadida el…» (faltava alguna cosa). Una errata que no canvia el sentit es
  corregeix sense nota.
- Si l'error era al titular, als avisos o a les xarxes, la correcció arriba també allà.
- No es retira un article sencer si n'hi ha prou amb canviar una part.

## El que es comprova sense IA

Uns programes repassen cada nit algunes d'aquestes normes (ADR 0056, 0059 i 0067), però no substitueixen
el revisor:

- `scripts/revisar-estilo.py`: el «quien» relatiu, les cites només en anglès i les normes de vocabulari i
  forma que es poden cercar («hoy», «pieza», «el diario cuenta», «app», el condicional de rumor, el
  percentatge) i els ladillos dels reportatges amb motlles d'etiqueta o ja usats; el que troba ho corregeix un
  agent.
- `scripts/comprobar-corrector.py`: que el corrector d'estil, un agent que repassa cada nit la
  redacció dels articles del dia, no ha canviat cap dada.
- `scripts/corregir-erratas.py`: «e» davant de «i», «u» davant de «o», les cometes espanyoles en anglès, i avisa
  dels titulars de més de 90 caràcters.
- `scripts/revisar-idiomas.py`: castellà que s'ha colat en una traducció.
- `scripts/revisar-autoria.py`: el que s'atribueix a un autor del diari i és d'un altre compte.
