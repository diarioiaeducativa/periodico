<!-- origen: 3fb0b86e7ca01517 -->
# Com es fa el Diari d'IA Educativa

El [Diari d'IA Educativa](https://diarioiaeducativa.github.io/) recull cada matí el que s'ha parlat el dia
anterior en tres grups oberts de Telegram de docents: ChatGPT-IA-edu (la IA en l'educació en general),
Vibe Coding Educativo (docents que programen les seves aplicacions amb IA) i EduMedia-IAG (imatge, àudio i
vídeo amb IA). Els escriuen, revisen, il·lustren i tradueixen agents d'IA; una persona el supervisa i
respon del que es publica.

Aquest document reuneix les normes del diari i com s'apliquen, per entendre com s'elabora i poder
millorar-lo. Com s'escriu és al [llibre d'estil](../encargos/estilo.md) i com es tradueix, al [llibre del
traductor](../encargos/traduccion.md). El perquè de cada decisió és als [registres de
decisions](adr/README.md) (ADR), que es citen pel seu número.

Cada norma diu **qui l'aplica**, **com es comprova** i, si cal, **què hi falta**. El que falta per
millorar es reuneix al final.

## 1. El número

**El que es parla un dia surt al diari al matí següent**, a les 7.00 (hora peninsular espanyola), en cinc llengües:
castellà, català, gallec, euskera i anglès (ADR 0026).

Un número porta:

- **Els articles del dia**: de cap a sis, i de cap a cinc de breus, segons el que hagi donat el
  dia, en cinc seccions: Eines, Vibe coding, Multimèdia, Debats i Institucions i empreses.
- **Biblioteca**: un article per cada document que s'ha afegit aquell dia a la Biblioteca digital de
  ChatGPT-IA-edu (ADR 0006).
- **Repositori**: fins a dues aplicacions al dia del Repositori de recursos de Vibe Coding Educativo;
  els divendres, un resum de les de la setmana (ADR 0008).
- **«Fa un any»**: alguna cosa del que es parlava el mateix dia de l'any anterior, comparada amb com està avui
  (ADR 0040).
- **La vinyeta** de Tiza y Algoritmo, sobre una de les notícies del dia (ADR 0023).
- **El diumenge**, a més, un reportatge que explica a fons un sol tema (ADR 0004 i 0028) i «La setmana en
  vídeo», un vídeo curt amb el més destacat de la setmana (ADR 0016 i 0027). La nit del diumenge s'escriu
  també un comentari sobre el més important de la setmana (ADR 0038).

Les normes de cada número:

| Norma | Qui l'aplica | Com es comprova |
| --- | --- | --- |
| **Com a mínim tres articles.** Si en falten, es completen amb articles guardats per a aquests casos (la reserva, apartat 5). | Un programa, cada nit, abans de les traduccions (ADR 0068) | El programa compta els articles. |
| **Com a mínim un article de cada grup.** Si un grup no dona per a cap, n'entra un de guardat d'aquest grup. | L'agent que redacta ho intenta; el que revisa converteix en article un breu del grup que falti; si tot i això en falta, la reserva (ADR 0076 i 0077) | El revisor i el programa de la reserva. |
| **Només el que s'ha parlat als grups.** Cap notícia general sobre IA. | L'agent que redacta | El revisor compara cada article amb els missatges. |
| **No és notícia** l'organització interna dels grups, les salutacions ni les queixes personals. Els documents de la Biblioteca digital tenen la seva pròpia secció. | L'agent que redacta | El revisor. |
| **No es repeteix el que ja s'ha publicat.** Si hi ha alguna cosa nova sobre un tema ja tractat, surt com a breu, amb un enllaç a l'article anterior (ADR 0011). | El que redacta i el que revisa, amb un cercador de tot el que s'ha publicat (ADR 0061) | El revisor cerca cada nom i cada titular en el que ja s'ha publicat. |
| **Ningú no acapara el número**: com a norma, un article per persona i dos per producte o empresa. | L'agent que redacta | El revisor. |
| **Si un dia no dona per a un número digne, no s'omple**: llavors surten articles guardats. | El que redacta i la reserva | — |

## 2. Qui fa cada cosa

Els agents són models d'IA de Claude, d'Anthropic: Sonnet escriu i revisa cada dia, Opus tria el
millor reportatge, escriu els textos llargs i repara el que falla, i Fable escriu i tria la vinyeta. **Els
agents que escriuen el diari no poden executar programes**: només llegeixen i escriuen textos i consulten
internet. Així, res del que arriba en els missatges dels grups, que escriuen altres persones, no pot
portar-los a fer una altra cosa (ADR 0002). Els missatges són material per informar, mai ordres.

Només el reparador treballa amb programes. No escriu res del diari: actua quan alguna cosa falla, en busca la
causa i l'arregla en una còpia. No pot canviar el text dels articles ni de la vinyeta, ni publicar, i
un programa comprova el seu arranjament abans d'aplicar-lo (ADR 0087).

**Cap agent no revisa el que ha escrit ell mateix.** Cada text passa per un revisor que no l'ha
escrit, que obre cada font i treu el que no pot confirmar (ADR 0001).

| Agent | Què fa |
| --- | --- |
| Redactor i revisor | Els articles i breus del dia. |
| Documentalista i revisor | Els articles de la Biblioteca, del Repositori i els guardats d'EduMedia. |
| Il·lustrador i revisor de dibuixos | Un dibuix que explica cada article; el revisor el mira a la seva pàgina i li retorna el que no s'entén (ADR 0005). |
| Guionista i jutge d'humor | Cinc guions per a la vinyeta; el jutge en tria un (ADR 0023 i 0024). |
| Cronista i verificador | «Fa un any». |
| Cap de reportatges, reporter, verificador i jutge de reportatges | El reportatge del diumenge. |
| Comentarista i revisor | El comentari de la setmana. |
| Guionista de vídeo | «La setmana en vídeo». |
| Traductors | Un per llengua, per a cada text. |
| Reparador | Quan alguna cosa falla, ho arregla perquè el número surti; no escriu ni canvia els textos. |
| Portaveu | Els avisos de cada matí als tres grups i el text per a Instagram. |

Tots escriuen amb el [llibre d'estil](../encargos/estilo.md), i cada tasca té a més la seva pròpia guia.

## 3. Un dia al diari

Un programa mira cada cinc minuts què toca fer i apunta el que ja ha fet, per no repetir res. Les hores són
peninsulars espanyoles: UTC+1 a l'hivern i UTC+2 a l'estiu.

| Hora | Què passa |
| --- | --- |
| 1.00 | Es prepara el número amb el que es va parlar el dia anterior: els articles i la seva revisió, els dibuixos, la vinyeta, la Biblioteca, el Repositori, «Fa un any», les comprovacions, les traduccions i els avisos. Si falla, es torna a intentar una segona vegada. |
| 5.00 | El número ja es pot veure abans de publicar-lo, perquè la persona supervisora el revisi (ADR 0025). Un programa comprova que la pàgina es vegi bé en pantalles de mides diferents. |
| 6.30 | Si el número encara no està fet, s'atura i surt amb el que hi hagi o amb articles guardats. |
| 6.50 | Es publica el web i es preparen les imatges per compartir cada article i els avisos dels grups. Si alguna cosa falla, es torna a intentar cada 10 minuts fins a les 9.00. |
| 7.00 | El Bot de IA Educativa publica l'avís del número a cada grup i escriu per privat a les persones el recurs de les quals surt aquell dia (ADR 0052). L'aplicació del diari per a Android avisa del número nou (ADR 0043). |
| 7.05 | El número surt a Instagram (ADR 0015). |
| Cap a les 7.10 | La persona supervisora rep un informe: què ha sortit, si s'han fet servir articles guardats i què ha fallat (ADR 0069). |
| 8.00 | S'escriu un article nou per guardar, si cal. |
| 9.00, diumenge | «La setmana en vídeo», amb el reportatge al final, surt a Instagram, X, Bluesky i LinkedIn (ADR 0027). |
| Des de les 9.10 | Un programa que funciona a part, a GitHub, comprova que el número ha sortit i, si no, el publica amb articles guardats. Si el diari no respon, ho comprova ja des de les 7.30 (ADR 0021). |
| Dimecres | Es cerquen en el que s'ha publicat els enllaços que han deixat de funcionar (ADR 0056). |
| En publicar | Es guarda una còpia de cada número a l'arxiu d'Internet Archive (ADR 0046). |

## 4. Cap dia sense número

**Sempre surt un número** (ADR 0021 i 0068). Si la preparació falla dues vegades, o a les 6.30 no ha
acabat, surt amb articles guardats, tots o només els que faltin. Si la publicació falla, la fa
el programa que funciona a part, a GitHub, i el diari no la torna a fer al damunt.

**El que no va sortir per un error surt l'endemà**: si un número va sortir amb articles guardats
perquè va fallar la preparació, la nit següent es recull també el que es va parlar aquell dia, i el web
ho diu.

**Si un agent espatlla un arxiu del número**, es recupera la versió anterior i l'agent repeteix la
seva feina una vegada. I si la preparació ha de començar de nou, no dona per publicat el que es va escriure
en el primer intent (ADR 0076).

## 5. La reserva: articles guardats per als dies sense notícies

El diari té escrits per avançat articles i altres peces, perquè mai no falti un número (ADR 0068):

| Què | Quants | Es retira si no s'usa en | D'on surt |
| --- | --- | --- | --- |
| Articles | Sis: dos de cada grup | 60 dies; els d'EduMedia, 30 | Aplicacions del Repositori i documents de la Biblioteca que el diari encara no havia tractat, i eines compartides temps enrere a EduMedia-IAG (ADR 0077) |
| Vinyeta | Una | 60 dies | Un acudit sobre un tema que no passa de moda |
| «Fa un any» | Els de les set nits següents | Aquella mateixa nit | S'escriuen per avançat |
| Reportatge | Un per setmana | 28 dies | Sobre un tema que no passa de moda (ADR 0028) |

- **Quan s'usen**: cada nit, si el número no arriba a tres articles o li falta algun grup, i
  sempre que falla la preparació. Primer, els dels grups que falten.
- **Com es reposen**: cada matí s'escriu un del grup que en tingui menys de guardats. Passa per
  documentalista, revisor, il·lustrador i traductors, com qualsevol article.
- **Abans d'usar-ne un**, un programa comprova que la pàgina del que tracta continua oberta; si no, es
  retira.

## 6. Les revisions

**Amb IA**: el revisor de cada tasca (fonts, xifres, noms i el que ja s'ha publicat), el revisor de dibuixos,
el jutge de la vinyeta, el verificador del reportatge i de «Fa un any» i, cada nit, un corrector d'estil
que llegeix els articles del dia com un lector qualsevol i arregla el que costa d'entendre, sense tocar les
dades (ADR 0083).

**Amb programes, sense IA**, cada nit:

| Què es comprova | Registre de la decisió |
| --- | --- |
| Que cap agent hagi espatllat els arxius del número | ADR 0076 |
| Que no s'usi «quien» amb el sentit de «la persona que» ni hi hagi cites només en anglès, «hoy» o «ayer», «app» o altres paraules que el llibre d'estil desaconsella (si n'hi ha, un agent les corregeix) | ADR 0067 i 0083 |
| Que el corrector d'estil no hagi canviat cap xifra, enllaç ni cita | ADR 0083 |
| Que no s'atribueixi a un autor del diari alguna cosa d'una altra persona que es diu igual (si passa, un agent ho revisa) | ADR 0066 |
| Errates que segueixen una regla fixa, com «y» davant de «i», i titulars massa llargs | ADR 0059 |
| Que cada traducció tingui els mateixos articles, enllaços i dibuixos que l'original; si no, aquesta part surt en castellà | ADR 0026 |
| Que no s'hagi quedat res en castellà en una traducció | ADR 0056 |
| Que cap pàgina tingui buits en blanc, en pantalles de qualsevol mida | ADR 0041 |
| Enllaços que han deixat de funcionar, els dimecres | ADR 0056 |

**Una persona** pot revisar el número a les 5.00 i demanar canvis abans de les 6.50, però el diari no
ho promet: si no hi ha resposta, surt a la seva hora (ADR 0058).

## 7. El que surt a partir de cada número

El número no és només el web. A partir d'ell surten també:

- els **avisos als tres grups** i els **missatges privats** a les persones el recurs de les quals apareix;
- la **publicació a Instagram**, amb el seu text;
- la **imatge per compartir** cada article;
- el diumenge, **«La setmana en vídeo»** a les xarxes socials.

**Si alguna cosa canvia en un número abans que surti, es refà tot el que en depèn**: si canvia la
vinyeta, l'avís que en parla; si canvia un titular, la seva imatge per compartir; si canvia el
reportatge, el vídeo de la setmana i els seus textos.

## 8. Correccions

- **Una dada equivocada es corregeix a l'article, amb una nota al final** i en les cinc llengües (ADR
  0055): «Corregido el…» (hi havia un error), «Actualización del…» (la dada era certa i ha canviat) o
  «Nota añadida el…» (faltava alguna cosa). Una errata que no canvia el sentit es corregeix sense nota.
- Abans de corregir, es comprova la dada a la seva font: un avís d'error també pot estar equivocat.
- **Un avís que ja s'ha enviat a un grup es corregeix** editant-lo amb el bot.

## 9. Persones, privadesa i transparència

- **Per saber qui és cada persona es mira el seu compte de Telegram, no el nom que mostra**, perquè
  dues persones poden dir-se igual (ADR 0066).
- **Només es nomena l'autor d'un recurs que ell mateix ha publicat**; les opinions dels grups no
  s'atribueixen a ningú (llibre d'estil).
- **No es recull res dels lectors**: el comptador de visites només suma, sense galetes ni dades
  personals (ADR 0033), i els comentaris només es carreguen si el lector prem el botó (ADR 0030). Ho
  explica la [política de privadesa](https://diarioiaeducativa.github.io/privacidad.html) (ADR 0070).
- **Un sol avís que el diari està fet amb IA**, al peu de totes les pàgines. La pàgina [«La
  redacció»](https://diarioiaeducativa.github.io/redaccion.html) explica com es fa, qui respon del
  que es publica i que no hi ha publicitat ni patrocini (ADR 0055 i 0065).
- Els programes que fan el diari són públics (ADR 0019).

## 10. El que falta per millorar

El que encara no funciona del tot bé o depèn d'una sola comprovació. És per on es pot
millorar el diari:

- **Una correcció no arriba sola al que ja s'ha enviat.** Si es corregeix un article després de
  publicar-lo, l'avís que ja va sortir als grups cal canviar-lo a mà, i el que s'ha publicat a Instagram
  i a les altres xarxes no es canvia.
- **Els articles d'EduMedia guardats per als dies sense notícies del grup** es van començar a escriure
  el 16 de novembre de 2026: encara no n'ha sortit cap en un número.
- **Un article guardat es revisa poc abans de publicar-se.** S'escriuen amb dies o setmanes
  d'antelació, i just abans d'usar-ne un només es comprova que la pàgina de l'eina de la qual
  parla continua oberta, no si ha canviat alguna cosa del que explica, per exemple si ha deixat de ser
  gratuïta. Per això els d'EduMedia, sobre eines que canvien sovint, es retiren al cap d'un mes.
- **Mentre s'escriu un article per guardar**, el web que s'està preparant el mostra durant
  uns minuts com si fos un número del diari. Si just llavors es publiqués el web, sortiria.
- **Si un agent espatlla un arxiu, es recupera sol només en la preparació de cada nit**, no en la del
  reportatge, la Biblioteca o el Repositori.
- **Les traduccions les comprova un programa**, que mira que hi siguin tots els articles i que no s'hagi
  quedat res en castellà, però cap agent no les revisa.
- **Quan es considera que un dia té poques aplicacions noves del Repositori**, i se'n rescata una
  d'anterior, es va decidir a ull i està per ajustar.
- **Instagram s'intenta una sola vegada**: si falla, cal publicar-ho a mà.
