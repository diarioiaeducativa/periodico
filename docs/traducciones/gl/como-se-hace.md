<!-- origen: 1c00f6a8d9a89f7c -->
# Como se fai o Diario de IA Educativa

O [Diario de IA Educativa](https://diarioiaeducativa.github.io/) recolle cada mañá o que se falou o día
anterior en tres grupos abertos de Telegram de docentes: ChatGPT-IA-edu (a IA na educación en xeral),
Vibe Coding Educativo (docentes que programan as súas aplicacións con IA) e EduMedia-IAG (imaxe, son e
vídeo con IA). Escribe-o, revisa-o, ilustra-o e traduce-o axentes de IA; unha persoa supervisa-o e
responde do publicado.

Este documento reúne as normas do diario e como se aplican, para entender como se elabora e poder
melloralo. Como se escribe está no [libro de estilo](../encargos/estilo.md) e como se traduce, no
[libro do tradutor](../encargos/traduccion.md). O porqué de cada decisión está nos [rexistros de
decisións](adr/README.md) (ADR), que se citan polo seu número.

Cada norma di **quen a aplica**, **como se comproba** e, se fai falta, **que lle falta**. O que falta
por mellorar reúne-se ao final.

## 1. O número

**O que se fala un día sae no diario á mañá seguinte**, ás 7.00, en cinco idiomas: castelán, catalán,
galego, éuscaro e inglés (ADR 0026).

Un número leva:

- **Os artigos do día**: de ningún a seis, e de ningún a cinco breves, segundo o que dese o día, en
  cinco seccións: Ferramentas, Vibe coding, Multimedia, Debates e Institucións e empresas.
- **Biblioteca**: un artigo por cada documento que se engadiu ese día á Biblioteca dixital de
  ChatGPT-IA-edu (ADR 0006).
- **Repositorio**: ata dúas aplicacións ao día do Repositorio de recursos de Vibe Coding Educativo; os
  venres, un resumo das da semana (ADR 0008).
- **«Hai un ano»**: algo do que se falaba o mesmo día do ano anterior, comparado con como está hoxe
  (ADR 0040).
- **A viñeta** de Xiz e Algoritmo, sobre unha das noticias do día (ADR 0023).
- **O domingo**, ademais, unha reportaxe que explica a fondo un só tema (ADR 0004 e 0028) e «A semana en
  vídeo», un vídeo curto co máis destacado da semana (ADR 0016 e 0027). A noite do domingo escribe-se
  tamén un comentario sobre o máis importante da semana (ADR 0038).

As normas de cada número:

| Norma | Quen a aplica | Como se comproba |
| --- | --- | --- |
| **Como mínimo tres artigos.** Se faltan, complétan-se con artigos gardados para estes casos (a reserva, apartado 5). | Un programa, cada noite, antes das traducións (ADR 0068) | O programa conta os artigos. |
| **Como mínimo un artigo de cada grupo.** Se un grupo non dá para ningún, entra un gardado deste grupo. | O axente que redacta tenta facelo; o que revisa converte en artigo un breve do grupo que falte; se aínda así falta, a reserva (ADR 0076 e 0077) | O revisor e o programa da reserva. |
| **Só o que se falou nos grupos.** Nada de noticias xerais sobre IA. | O axente que redacta | O revisor compara cada artigo coas mensaxes. |
| **Non é noticia** a organización interna dos grupos, os saúdos nin as queixas persoais. Os documentos da Biblioteca dixital teñen a súa propia sección. | O axente que redacta | O revisor. |
| **Non se repite o xa publicado.** Se hai algo novo sobre un tema xa tratado, sae como breve, cunha ligazón ao artigo anterior (ADR 0011). | O que redacta e o que revisa, cun buscador de todo o publicado (ADR 0061) | O revisor busca cada nome e cada titular no xa publicado. |
| **Ninguén acapara o número**: como norma, un artigo por persoa e dous por produto ou empresa. | O axente que redacta | O revisor. |
| **Se un día non dá para un número digno, non se enche**: entón saen artigos gardados. | O que redacta e a reserva | — |

## 2. Quen fai cada cousa

Os axentes son modelos de IA de Claude, de Anthropic: Sonnet escribe e revisa cada día, e Opus escolle
(a mellor viñeta, a mellor reportaxe) e escribe os textos longos. **Os axentes non poden executar
programas**: só len e escriben textos e consultan internet. Así, nada do que chega nas mensaxes dos
grupos, que escriben outras persoas, pode levalos a facer outra cousa (ADR 0002). As mensaxes son
material para informar, nunca ordes.

**Ningún axente revisa o que escribiu el mesmo.** Cada texto pasa por un revisor que non o escribiu, que
abre cada fonte e quita o que non pode confirmar (ADR 0001).

| Axente | Que fai |
| --- | --- |
| Redactor e revisor | Os artigos e breves do día. |
| Documentalista e revisor | Os artigos da Biblioteca, do Repositorio e os gardados de EduMedia. |
| Ilustrador e revisor de debuxos | Un debuxo que explica cada artigo; o revisor mira-o na súa páxina e devolve o que non se entende (ADR 0005). |
| Guionista e xuíz de humor | Cinco guións para a viñeta; o xuíz escolle un (ADR 0023 e 0024). |
| Cronista e verificador | «Hai un ano». |
| Xefe de reportaxes, repórter, verificador e xuíz de reportaxes | A reportaxe do domingo. |
| Comentarista e revisor | O comentario da semana. |
| Guionista de vídeo | «A semana en vídeo». |
| Tradutores | Un por idioma, para cada texto. |
| Voceiro | Os avisos de cada mañá nos tres grupos e o texto para Instagram. |

Todos escriben co [libro de estilo](../encargos/estilo.md), e cada tarefa ten ademais a súa propia guía.

## 3. Un día no diario

Un programa mira cada cinco minutos que toca facer e apunta o que xa fixo, para non repetir nada.

| Hora | Que pasa |
| --- | --- |
| 1.00 | Prepara-se o número co que se falou o día anterior: os artigos e a súa revisión, os debuxos, a viñeta, a Biblioteca, o Repositorio, «Hai un ano», as comprobacións, as traducións e os avisos. Se falla, tenta-se unha segunda vez. |
| 5.00 | O número xa se pode ver antes de publicalo, para que a persoa supervisora o revise (ADR 0025). Un programa comproba que a páxina se vexa ben en pantallas de distintos tamaños. |
| 6.30 | Se o número aínda non está feito, pára-se e sae co que haxa ou con artigos gardados. |
| 6.50 | Publica-se a web e prepáran-se as imaxes para compartir cada artigo e os avisos dos grupos. Se algo falla, volve intentar-se cada 10 minutos ata as 9.00. |
| 7.00 | O Bot de IA Educativa publica o aviso do número en cada grupo e escribe por privado ás persoas cuxo recurso sae ese día (ADR 0052). A aplicación do diario para Android avisa do novo número (ADR 0043). |
| 7.05 | O número sae en Instagram (ADR 0015). |
| Cara ás 7.10 | A persoa supervisora recibe un informe: que saíu, se se usaron artigos gardados e que fallou (ADR 0069). |
| 8.00 | Escribe-se un artigo novo para gardar, se fai falta. |
| 9.00, domingo | «A semana en vídeo», coa reportaxe ao final, sae en Instagram, X, Bluesky e LinkedIn (ADR 0027). |
| Desde as 9.10 | Un programa que funciona á parte, en GitHub, comproba que o número saíu e, se non, publica-o con artigos gardados. Se o diario non responde, comproba-o xa desde as 7.30 (ADR 0021). |
| Mércores | Búscan-se no publicado as ligazóns que deixaron de funcionar (ADR 0056). |
| Ao publicar | Garda-se unha copia de cada número no arquivo de Internet Archive (ADR 0046). |

## 4. Ningún día sen número

**Sempre sae un número** (ADR 0021 e 0068). Se a preparación falla dúas veces, ou ás 6.30 non rematou,
sae con artigos gardados, todos ou só os que falten. Se a publicación falla, fai-a o programa que
funciona á parte, en GitHub, e o diario non a volve facer enriba.

**O que non saíu por un fallo sae ao día seguinte**: se un número saíu con artigos gardados porque
fallou a preparación, a noite seguinte recolle-se tamén o que se falou ese día, e a web di-o.

**Se un axente estraga un ficheiro do número**, recupera-se a versión anterior e o axente repite o seu
traballo unha vez. E se a preparación ten que comezar de novo, non dá por publicado o que se escribiu no
primeiro intento (ADR 0076).

## 5. A reserva: artigos gardados para os días sen noticias

O diario ten escritos de antemán artigos e outras pezas, para que nunca falte un número (ADR 0068):

| Que | Cantos | Retira-se se non se usa en | De onde sae |
| --- | --- | --- | --- |
| Artigos | Seis: dous de cada grupo | 60 días; os de EduMedia, 30 | Aplicacións do Repositorio e documentos da Biblioteca que o diario aínda non tratara, e ferramentas compartidas tempo atrás en EduMedia-IAG (ADR 0077) |
| Viñeta | Unha | 60 días | Unha chanza sobre un tema que non pasa de moda |
| «Hai un ano» | Os das sete noites seguintes | Esa mesma noite | Escriben-se por adiantado |
| Reportaxe | Un por semana | 28 días | Sobre un tema que non pasa de moda (ADR 0028) |

- **Cando se usan**: cada noite, se o número non chega a tres artigos ou lle falta algún grupo, e sempre
  que falla a preparación. Primeiro, os dos grupos que faltan.
- **Como se repoñen**: cada mañá escribe-se un do grupo que teña menos gardados. Pasa por documentalista,
  revisor, ilustrador e tradutores, como calquera artigo.
- **Antes de usar un**, un programa comproba que a páxina do que trata segue aberta; se non, retira-se.

## 6. As revisións

**Con IA**: o revisor de cada tarefa (fontes, cifras, nomes e o xa publicado), o revisor de debuxos, o
xuíz da viñeta, o verificador da reportaxe e de «Hai un ano» e, cada noite, un corrector de estilo que
le os artigos do día como un lector calquera e arranxa o que custa entender, sen tocar os datos
(ADR 0083).

**Con programas, sen IA**, cada noite:

| Que se comproba | Rexistro da decisión |
| --- | --- |
| Que ningún axente estragase os ficheiros do número | ADR 0076 |
| Que non se use «quien» co sentido de «la persona que» nin haxa citas só en inglés, «hoy» ou «ayer», «app» ou outras palabras que o libro de estilo desaconsella (se as hai, un axente corrixe-as) | ADR 0067 e 0083 |
| Que o corrector de estilo non cambiase ningunha cifra, ligazón nin cita | ADR 0083 |
| Que non se lle atribúa a un autor do diario algo doutra persoa que se chama igual (se pasa, un axente revisa-o) | ADR 0066 |
| Erratas que seguen unha regra fixa, como «y» diante de «i», e titulares demasiado longos | ADR 0059 |
| Que cada tradución teña os mesmos artigos, ligazóns e debuxos que o orixinal; se non, esa parte sae en castelán | ADR 0026 |
| Que non quedase nada en castelán nunha tradución | ADR 0056 |
| Que ningunha páxina teña ocos en branco, en pantallas de calquera tamaño | ADR 0041 |
| Ligazóns que deixaron de funcionar, os mércores | ADR 0056 |

**Unha persoa** pode revisar o número ás 5.00 e pedir cambios antes das 6.50, pero o diario non o
promete: se non hai resposta, sae á súa hora (ADR 0058).

## 7. O que sae a partir de cada número

O número non é só a web. A partir del saen tamén:

- os **avisos nos tres grupos** e as **mensaxes privadas** ás persoas cuxo recurso aparece;
- a **publicación en Instagram**, co seu texto;
- a **imaxe para compartir** cada artigo;
- o domingo, **«A semana en vídeo»** nas redes sociais.

**Se algo cambia nun número antes de que saia, refai-se todo o que depende diso**: se cambia a viñeta, o
aviso que fala dela; se cambia un titular, a súa imaxe para compartir; se cambia a reportaxe, o vídeo da
semana e os seus textos.

## 8. Correccións

- **Un dato equivocado corrixe-se no artigo, cunha nota ao final** e nos cinco idiomas (ADR 0055):
  «Corregido el…» (había un erro), «Actualización del…» (o dato era certo e cambiou) ou «Nota añadida
  el…» (faltaba algo). Unha errata que non cambia o sentido corrixe-se sen nota.
- Antes de corrixir, comproba-se o dato na súa fonte: un aviso de erro tamén pode estar equivocado.
- **Un aviso que xa se enviou a un grupo corrixe-se** editándoo co bot.

## 9. Persoas, privacidade e transparencia

- **Para saber quen é cada persoa mira-se a súa conta de Telegram, non o nome que mostra**, porque dúas
  persoas poden chamarse igual (ADR 0066).
- **Só se nomea o autor dun recurso que el mesmo publicou**; as opinións dos grupos non se lle atribúen
  a ninguén (libro de estilo).
- **Non se recolle nada dos lectores**: o contador de visitas só suma, sen cookies nin datos persoais
  (ADR 0033), e os comentarios só se cargan se o lector preme o botón (ADR 0030). Explica-o a [política de
  privacidade](https://diarioiaeducativa.github.io/privacidad.html) (ADR 0070).
- **Un só aviso de que o diario está feito con IA**, no pé de todas as páxinas. A páxina [«A
  redacción»](https://diarioiaeducativa.github.io/redaccion.html) explica como se fai, quen responde do
  publicado e que non hai publicidade nin patrocinio (ADR 0055 e 0065).
- Os programas que fan o diario son públicos (ADR 0019).

## 10. O que falta por mellorar

O que aínda non funciona de todo ben ou depende dunha soa comprobación. É por onde se pode mellorar o
diario:

- **Unha corrección non chega soa ao que xa se enviou.** Se se corrixe un artigo despois de publicalo, o
  aviso que xa saíu nos grupos hai que cambialo a man, e o publicado en Instagram e nas outras redes non
  se cambia.
- **Os artigos de EduMedia gardados para os días sen noticias do grupo** comezaron a escribir-se o 16 de
  novembro de 2026: aínda non saíu ningún nun número.
- **Un artigo gardado revisa-se pouco antes de publicar-se.** Escriben-se con días ou semanas de
  antelación, e xusto antes de usar un só se comproba que a páxina da ferramenta da que fala segue
  aberta, non se cambiou algo do que conta, por exemplo se deixou de ser gratuíta. Por iso os de
  EduMedia, sobre ferramentas que cambian a miúdo, retiran-se ao mes.
- **Mentres se escribe un artigo para gardar**, a web que se está a preparar mostra-o durante uns
  minutos coma se fose un número do diario. Se xusto entón se publicase a web, sairía.
- **Se un axente estraga un ficheiro, recupera-se só na preparación de cada noite**, non na da
  reportaxe, a Biblioteca ou o Repositorio.
- **As traducións comproba-as un programa**, que mira que estean todos os artigos e que non quedase nada
  en castelán, pero ningún axente as revisa.
- **Cando se considera que un día ten poucas aplicacións novas do Repositorio**, e se rescata unha
  anterior, decidiu-se a ollo e está por axustar.
- **Instagram só se intenta unha vez**: se falla, hai que publicalo a man.
