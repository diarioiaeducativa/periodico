<!-- origen: 330bbfafb8d3d5a4 -->
# Libro de estilo do Diario de IA Educativa

Como escribe o diario. Vale para todo axente que escribe, revisa, traduce ou resume algo que vai
ler o público (artigos, breves, reportaxes, «Hai un ano», comentarios da semana, avisos, textos
para redes e vídeos) e para as persoas que o manteñen. Léese enteiro antes de comezar.

Aquí está o común. Cada tarefa ten ademais a súa guía en `encargos/` co propio (medidas, formato,
ton dos avisos, a viñeta…); se unha norma de aquí non vale para unha tarefa, a súa guía dío. As normas que non son de estilo (que é noticia, que leva cada número e os artigos gardados
para os días sen noticias) están en «Como se fai o diario», `docs/como-se-hace.md`.

## Para quen se escribe

- Para docentes e persoas interesadas na IA na educación que **non están** nos grupos. Cada
  texto enténdese só, sen ter lido as mensaxes nin outros artigos: que é, por que lle importa a
  un docente e onde atopalo.
- **Para un público moi amplo, non para expertos**: un docente de calquera materia, unha familia, unha
  persoa que comeza coa IA. Se algo só o entenden as persoas que xa saben do tema, reescríbese.
- O que lle interesa á persoa lectora, non como funciona o diario por dentro: nada de axentes, ficheiros,
  programas nin servidores no que se publica, salvo que o artigo trate do propio diario ou de
  Anthropic (apartado «Rigor»).

## Ton

- Formal, informativo e impersoal. Nunca publicitario («incrible», «imprescindible», «revoluciona»)
  nin alarmista. Sen exclamacións nin emojis.
- As guías dos avisos e da viñeta permiten un ton máis achegado; nunca de anuncio.

## Lingua

- Castelán correcto e natural. As traducións, no seu apartado.
- **Linguaxe inclusiva, pero natural**: «o profesorado», «o alumnado», «as familias»; sen
  desdobramentos nin signos raros.
- **Sen o relativo «quien» ou «quienes»** co sentido de «la persona que»: «la persona que», un colectivo («el
  profesorado») ou un xiro co asunto diante («separar la creación de la revisión», non «separar a
  quien crea de quien revisa»). O interrogativo, con til («¿quién?»), si; unha cita literal
  déixase como está.
- **O que publica o diario son «artigos»**, non «pezas» (a palabra só é interna, nos
  campos dos arquivos). Un artigo pode ser unha noticia, un breve, unha reportaxe.
- **O que fai o diario cun tema: «publícao», «recólleo»** ou o tema «sae» no diario;
  non o «conta». «El diario publicó el 3 de noviembre…», «como recogió el diario…».
- **A IA non pensa nin quere.** Nada de verbos que lle dan mente ou intención a un programa («pensa»,
  «entende», «quere», «minte»): un modelo xera, responde ou dá un resultado. O que decide é unha
  empresa ou unha persoa: «OpenAI limitou…», non «ChatGPT decidiu…». O que un modelo inventa
  é unha «resposta inventada»; «alucinación», só explicada.
- **Vocabulario**: «intelixencia artificial», en minúscula, e a súa sigla, IA, nunca AI, salvo en
  nomes propios («Google AI Studio»). «Chatbot» e «alucinar», sen comiñas. Mellor «aplicación» que
  «app», «en liña» que «online», «ligazón» que «link» e «aprendizaxe automática» que «machine
  learning». *Prompt*, en cursiva. Un termo que a persoa lectora pode non coñecer explícase a primeira
  vez.
- **Siglas**: unha pouco coñecida desenvólvese a primeira vez («la Agencia Española de Protección de
  Datos (AEPD)»); unha técnica inglesa (LLM, API, MCP) vai co que é («un modelo de linguaxe
  (LLM), o tipo de programa que hai detrás de ChatGPT»). Se non se volve usar, non se pon.
- **Sen condicional de rumor**: non «OpenAI habría lanzado…», senón «segundo [fonte], OpenAI
  lanzou…» ou «é posible que…».
- **Frases claras**: unha idea por frase, a palabra corrente antes ca a técnica e fóra as
  metáforas gastadas («cambio de paradigma», «na era da IA»).
- **Antes claro que breve.** Nada de expresións comprimidas que obrigan a reler: substantivos
  encadeados («fluxo de xeración multimodal con verificación cruzada»), xerga dos grupos,
  palabras que se dan por sabidas ou frases ás que lles falta o verbo. Se unha frase curta se entende
  peor ca unha algo máis longa, vai a longa: «un sistema que crea imaxes e vídeo e comproba o
  resultado con outro modelo».
- Os nomes de produtos, aplicacións, grupos e documentos, tal como os escribe a empresa ou a persoa que os fai
  («ChatGPT», «Vibe Coding Educativo»). Un recurso en catalán ou noutra lingua descríbese en castelán
  e conserva o seu nome; o título dunha obra queda no seu idioma.

## Titulares, antetítulos e entradas

- **Titular**: claro, con verbo, sen preguntas nin ganchos («non vas crer…»). Di que achega o que
  recolle, non só o nome da ferramenta ou do documento. **Como moito 90 caracteres**, contando
  os espazos: o que non caiba vai ao antetítulo ou á entrada.
- **Antetítulo**: de dúas a cinco palabras, sen verbo: o tipo de cousa ou o ámbito («Guía oficial»,
  «Novo no repositorio», «Do fondo de EduMedia»).
- **Entrada**: unha ou dúas frases que resumen o artigo (dúas ou tres na reportaxe). Non repite o
  titular: achega o seguinte.
- **O titular e a entrada non din máis ca o corpo nin ca a fonte.** O que o corpo
  matiza («segundo a empresa», «nos plans de pago», «é unha hipótese do autor») non desaparece
  arriba. Unha proba sen nada co que comparar non «demostra» nin «suxire» unha causa.
- **Intertítulos** (os títulos dos apartados dunha reportaxe): un titular pequeno que di o que conta o seu apartado
  (quen fai que, o dato), con verbo se se pode e como moito 60 caracteres: «A revisión de Stanford só admite
  estudos causais», non «Que conta como proba». Nada de etiquetas que valerían para calquera texto: nin comezar
  por «Que», «O que», «Como» ou «Por que», nin parellas abstractas («Entender ou entregar», «O medio e o método»,
  «Do produto ao proceso»), nin «Máis aló de…». Ningún repite o doutra reportaxe.
- **O que non é destes días leva a súa data no titular**: un informe de agosto non «se publica»
  hoxe, é «Un informe de agosto…».

## Persoas

- **Temas, non persoas.** Non se nomea as persoas que opinan ou preguntan nos grupos, tampouco con «un
  membro dixo…»: recóllense as posturas.
- **Nómease o autor dun recurso que el mesmo publicou** (unha aplicación, unha guía, un
  documento), como crédito («creada por…»), co nome que consta no propio recurso ou o
  nome completo da persoa que o publica. Un nome de pía non identifica a ninguén: se o recurso non
  di quen o fai, «o seu autor», e que a web non o indica. Nunca se completa un apelido.
- **Quen é quen di a marca do material, non o nome** (ADR 0066): os autores do diario
  son só as mensaxes marcadas `[autor del diario: …]`; outra persoa co mesmo nome de pía é
  outra persoa. As marcas non se publican.
- **Os autores do diario, coma calquera**: nómeanse como crédito dos seus recursos igual que os
  demais, co nome completo co que asinan o diario, aínda que nos grupos usen outro.
- **Os cargos, só se teñen que ver coa noticia** (administrar un grupo, ser coautor do
  diario): se non, a persoa é un docente máis.
- **Se o artigo trata do propio diario, dío** con esas palabras («este diario»).
- **O alumnado**: non se publica nada que o identifique (nome, imaxe, nin centro e curso xuntos),
  aínda que apareza no material compartido. Dunha ferramenta para a aula dise, segundo as súas
  condicións, se pide datos do alumnado e se os usa para adestrar os seus modelos; se non consta, dise.

## Rigor

- **Cada afirmación comprécase na fonte orixinal**: o anuncio oficial, a páxina do produto,
  o documento da administración. Unha mensaxe do grupo, unha ligazón a X ou un vídeo non abondan.
- **O que non se pode comprobar, quítase ou dise como non confirmado.** Nada de inventar
  datas, cifras, autores nin funcións.
- **O que anuncia unha empresa, coas súas condicións**: en que plan, a que prezo, ata cando, en que
  países. «Gratis» ou «para todos» contrástase coas súas condicións.
- **A linguaxe das empresas, atribuída ou fóra**: «revolucionario», «potente» ou «sen
  precedentes», só dentro dunha cita atribuída; o texto di que fai o produto. Un estudo ou unha
  enquisa preséntase con quen o fai e quen o paga, e se é da propia empresa, dise
  («segundo un estudo da propia OpenAI»). Unha nota de prensa non se reproduce: identifícase e
  reescríbese.
- **Cando un artigo trata de Anthropic ou de Claude**, unha frase lembra que o diario o escriben
  axentes de Claude, para que a persoa lectora o teña en conta. Nomealos de pasada, nunha lista, non o pide.
- **As cifras, coa precisión da fonte** (sen decimais que a fonte non dá) e unha proporción
  coa súa cantidade absoluta («o dobre, de 10 a 20 centros»). Se a fonte dá cifras distintas segundo
  a versión ou o plan, dise a cal corresponde cada unha. Do 20 % ao 30 % son 10 puntos máis, non
  un 10 % máis. Mellor «un de cada oito docentes» que «o 12,5 %».
- **Unha norma, aplicada ao caso**: se o artigo conta o que esixe unha lei ou unha autoridade, di tamén
  que supón para o que trata (se fai falta permiso, un aviso ou nada), e non deixa que a persoa lectora saque a
  conclusión (Juanjo, 19-11-2026, ante as condicións da AEPD no artigo de Umami: «debes hacerlo tú»).
- **Os datos que cambian fíganse con data** («a 1 de novembro de 2026»); o demais non leva data.
- **Toda hora, co seu fuso**, porque o diario se le en todo o mundo (ADR 0091). A de España:
  «ás 10.30 (hora peninsular española, UTC+1)», UTC+2 en verán; «peninsular», porque Canarias vai
  unha hora por detrás. A de fóra, coa de orixe e a equivalente en España: «ás 10.00 de
  California (as 19.00 na España peninsular, UTC+1)». Se un texto dá varias horas do mesmo sitio, o
  fuso vai a primeira vez.
- **Unha páxina oficial pode estar desactualizada**: se contradi o que o diario xa publicou co
  documento diante, manda o publicado, e dise.
- **Antes de xulgar unha ligazón, ábrese**: o enderezo non di o que hai na páxina nin a súa data.
- **O que o diario xa publicou, igual**: un artigo sobre un asunto xa tratado dá as mesmas
  cifras e datas ca o anterior, enlázao e, se algo cambiou, dío.

## Citas e outros idiomas

- Citas breves e exactas, entre comiñas, e poucas: o artigo explica, non copia.
- **O que vai entre comiñas búscase tal cal na fonte**; se non aparece, quítase ou
  parafraséase. Unha frase tomada dunha fonte vai entre comiñas ou reescríbese.
- **Ningunha cita só en inglés**: ou traducida, ou coa tradución ao lado entre parénteses.
- O oficial alleo (o título dunha norma, dun informe) queda no seu idioma orixinal.

## Fontes e ligazóns

O detallado está en `encargos/enlaces.md`; o esencial:

- **O que se nomea enlázase onde se nomea**, na súa primeira mención e co seu nome como texto da
  ligazón; ao pé, en `fuentes`, todas.
- **Á fonte orixinal e oficial**, en castelán (ou en catalán) se existe esa versión; unha
  ferramenta, á web que usará a persoa lectora, non ao seu repositorio de código.
- **O xa publicado que está claramente relacionado, enlazado** coa súa clave (`pieza:AAAA-MM-DD/id`),
  cun texto que diga de que trata, nunca «aquí».
- O texto dunha ligazón nunca é «mensaxe 123» nin un enderezo espido.
- Unha ligazón que descarga un arquivo dío: «a guía (PDF)».

## Forma

- **Comiñas españolas** («»); dentro delas, as inglesas (“”).
- **A porcentaxe, con espazo** (25 %); os millares, con espazo (1 200); as moedas, co seu nome
  («10 dólares», «4 euros»).
- Parágrafos de tres a seis frases nos textos longos (cada guía dá a súa medida). Letra grosa con mesura:
  dúas ou tres ideas nun texto longo.
- Ligazóns en Markdown (`[texto](url)`); nos textos para avisos e redes, texto plano (dínoo as súas
  guías).
- **Nunca «hoy», «ayer» nin «esta semana»**: a data ou o día («o xoves 12»). O número sae o día
  seguinte ás conversas e queda na hemeroteca; o que se garda para outro día (a reserva,
  «Hai un ano» escrito por adiantado) tampouco di «acaba de».

## Gráficos

- **Un gráfico, só cando explica algo que o texto non deixa ver dunha ollada**: tres ou máis cifras comparables
  da mesma fonte (os resultados dun estudo, unha enquisa, unha evolución no tempo). Non para amañar nin
  para unha ou dúas cifras, que se din no texto.
- **Debúxao o programa do diario a partir dos datos** (o campo `grafico` do artigo ou do apartado da
  reportaxe, ADR 0084), nunca un axente a man: barras horizontais (`barras`, para comparar), columnas
  (`columnas`, para poucas categorías con etiquetas curtas) ou liñas (`lineas`, para unha evolución).
- **Os datos, exactos e dunha soa fonte**: os mesmos valores que dá a fonte, coa súa precisión, e a mesma
  unidade para todos. As barras empezan sempre en cero (o programa faino só); nada de mesturar nun gráfico
  cifras de fontes distintas.
- **Título que di que se mide**, non a conclusión («Redaccións humanas que os detectores tomaron por IA»), e
  etiquetas curtas.
- **A fonte, sempre**, enlazada; e na nota, o que fai falta para lelo ben: cantas persoas ou casos, de
  onde e cando, e se os datos son da propia empresa («segundo a empresa»).

## As traducións

Cada edición tradúcese ao catalán, ao galego, ao euskera e ao inglés, co mesmo criterio que o
castelán e no rexistro natural de cada lingua, non calcado. Como se fai en cada lingua (norma,
onde consultar, formatos, vocabulario da IA e o propio de España) está no libro do tradutor,
`encargos/traduccion.md`.

## Correccións

- Un erro córrixese sen esperar a que ninguén o pida, no mesmo artigo e nos cinco idiomas, coa
  súa nota ao final (ADR 0055): «Corregido el…» (había un erro), «Actualización del…» (o dato era
  certo e cambiou) ou «Nota añadida el…» (faltaba algo). Unha errata que non cambia o sentido
  córrixese sen nota.
- Se o erro estaba no titular, nos avisos ou nas redes, a corrección chega tamén alí.
- Non se retira un artigo enteiro se abonda con cambiar unha parte.

## O que se comproba sen IA

Uns programas repasan cada noite algunhas destas normas (ADR 0056, 0059 e 0067), pero non substitúen
o revisor:

- `scripts/revisar-estilo.py`: o «quien» relativo, as citas só en inglés e as normas de vocabulario e
  forma que se poden buscar («hoy», «pieza», «el diario cuenta», «app», o condicional de rumor, a
  porcentaxe) e os intertítulos das reportaxes con moldes de etiqueta ou xa usados; o que atopa corríxeo un
  axente.
- `scripts/comprobar-corrector.py`: que o corrector de estilo, un axente que repasa cada noite a
  redacción dos artigos do día, non cambiou ningún dato.
- `scripts/corregir-erratas.py`: «e» ante «i», «u» ante «o», as comiñas españolas en inglés, e avisa
  dos titulares de máis de 90 caracteres.
- `scripts/revisar-idiomas.py`: castelán que se coou nunha tradución.
- `scripts/revisar-autoria.py`: o que se lle atribúe a un autor do diario e é doutra conta.
