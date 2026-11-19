<!-- origen: 71fd29243d273c19 -->
# Hezkuntzako AA Egunkaria nola egiten den

[Hezkuntzako AA Egunkariak](https://diarioiaeducativa.github.io/) goiz oro biltzen du aurreko egunean irakasleen
Telegrameko hiru talde irekitan hitz egindakoa: ChatGPT-IA-edu (hezkuntzako AA, oro har), Vibe Coding Educativo
(AAren laguntzaz beren aplikazioak programatzen dituzten irakasleak) eta EduMedia-IAG (irudia, audioa eta bideoa
AArekin). AA agenteek idazten, berrikusten, ilustratzen eta itzultzen dute; pertsona batek gainbegiratzen du, eta
argitaratutakoaren erantzule da.

Dokumentu honek egunkariaren arauak eta haiek nola aplikatzen diren biltzen ditu, egunkaria nola egiten den
ulertzeko eta hobetu ahal izateko. Nola idazten den [estilo-liburuan](../encargos/estilo.md) dago, eta nola
itzultzen den, [itzultzailearen liburuan](../encargos/traduccion.md). Erabaki bakoitzaren zergatia
[erabakien erregistroetan](adr/README.md) (ADR) dago, eta zenbakiaren bidez aipatzen dira.

Arau bakoitzak esaten du **nork aplikatzen duen**, **nola egiaztatzen den** eta, behar izanez gero, **zer falta
zaion**. Hobetzeke dagoena amaieran biltzen da.

## 1. Zenbakia

**Egun batean hitz egindakoa hurrengo goizean ateratzen da egunkarian**, 7:00etan (Espainiako penintsulako ordua), bost hizkuntzatan:
gaztelaniaz, katalanez, galegoz, euskaraz eta ingelesez (ADR 0026).

Zenbaki batek hauek ditu:

- **Eguneko artikuluak**: bat ere ez eta sei artean, eta bat ere ez eta bost albiste labur artean, egunak eman
  duenaren arabera, bost ataletan: Tresnak, Vibe coding, Multimedia, Eztabaidak eta Erakundeak eta enpresak.
- **Liburutegia**: artikulu bat, egun horretan ChatGPT-IA-eduko Liburutegi digitalean gehitu den dokumentu
  bakoitzeko (ADR 0006).
- **Biltegia**: egunean bi aplikazio gehienez, Vibe Coding Educativoren baliabideen Biltegikoak; ostiraletan,
  asteko aplikazioen laburpen bat (ADR 0008).
- **«Duela urtebete»**: urte bat lehenago egun berean hitz egiten zenaren zerbait, gaur dagoenarekin
  alderatuta (ADR 0040).
- **Klarion eta Algoritmoren bineta**, eguneko albisteetako bati buruzkoa (ADR 0023).
- **Asteazkenetan**, gainera, taldeetako eztabaida bati buruzko iritzi-zutabe bat: egunkariko pieza bakarra, alderdi
  hartzen duena, eta idazten duen AA ereduak sinatua (ADR 0092).
- **Igandeetan**, gainera, gai bakar bat sakon azaltzen duen erreportaje bat (ADR 0004 eta 0028) eta «Astea
  bideoan», asteko gauzarik nabarmenenekin egindako bideo laburra (ADR 0016 eta 0027). Igande gauean,
  asteko gauzarik garrantzitsuenari buruzko iruzkin bat ere idazten da (ADR 0038).

Zenbaki bakoitzaren arauak:

| Araua | Nork aplikatzen duen | Nola egiaztatzen den |
| --- | --- | --- |
| **Gutxienez hiru artikulu.** Falta badira, horretarako gordetako artikuluekin osatzen dira (erreserba, 5. atala). | Programa batek, gauero, itzulpenen aurretik (ADR 0068) | Programak artikuluak zenbatzen ditu. |
| **Gutxienez talde bakoitzeko artikulu bat.** Talde batek ez badu ezertarako ematen, taldeko gordetako bat sartzen da. | Idazten duen agenteak saiatzen da; berrikusleak falta den taldeko albiste labur bat artikulu bihurtzen du; hala ere falta bada, erreserba (ADR 0076 eta 0077) | Berrikusleak eta erreserbaren programak. |
| **Taldeetan hitz egindakoa bakarrik.** AAri buruzko albiste orokorrik ez. | Idazten duen agenteak | Berrikusleak artikulu bakoitza mezuekin alderatzen du. |
| **Ez da albiste** taldeen barne-antolaketa, agurrak eta kexa pertsonalak. Liburutegi digitaleko dokumentuek beren atala dute. | Idazten duen agenteak | Berrikusleak. |
| **Argitaratutakoa ez da errepikatzen.** Lehen jorratutako gai bati buruz berririk badago, albiste labur gisa ateratzen da, aurreko artikulurako estekarekin (ADR 0011). | Idazten eta berrikusten dutenek, argitaratutako guztiaren bilatzaile batekin (ADR 0061) | Berrikusleak izen eta titular bakoitza argitaratutakoan bilatzen du. |
| **Inork ez du zenbakia monopolizatzen**: arau gisa, pertsona bakoitzeko artikulu bat eta produktu edo enpresa bakoitzeko bi. | Idazten duen agenteak | Berrikusleak. |
| **Egun batek ez badu zenbaki duin baterako ematen, ez da betetzen**: orduan gordetako artikuluak ateratzen dira. | Idazten duenak eta erreserbak | — |
| **Iritzia, bereizita eta sinatuta.** Asteazkeneko zutabeak soilik hartzen du alderdi: «Iritzia» atalean doa, idazten duen ereduaren sinadurarekin eta egunkariak datuak egiaztatzen dituela eta iritzia ereduarena dela dioen ohar batekin, egunkariaren printzipioen barruan (10. atala). Ideiak eztabaidatzen ditu, ez pertsonak: taldeetako inor ez da izendatzen. | Zutabegileak; sinadura eta oharra webgunea muntatzen duen programak jartzen ditu (ADR 0092) | Egiaztatzaileak datu bakoitza eta inor ez dela ezagun egiten begiratzen du, tesiari ukitu gabe; programa batek, luzera eta estekak. |

## 2. Nork egiten duen zer

Agenteak Anthropic-en Claude AA ereduak dira: Sonnet-ek egunero idazten eta berrikusten du, Opus-ek erreportaje
onena eta zutabe onena aukeratzen ditu, testu luzeak idazten ditu eta huts egiten duena konpontzen du, eta Fable-k
bineta idazten eta aukeratzen du.
Salbuespena asteazkeneko zutabegilea da, OpenAIren GPT-6.2-Astra: iritzia egunkariko gainerakoaren ahotsa ez den beste
ahots batetik dator, eta bere izenarekin sinatzen du (ADR 0092). **Egunkaria idazten duten agenteek ezin dute
programarik exekutatu**: testuak irakurri eta idatzi eta interneten kontsultatu baino ez dute egiten. Horrela,
taldeetako mezuetan datorrenak, beste pertsona batzuek idatzitakoak, ezin die beste ezer egiterik eragin
(ADR 0002). Mezuak informatzeko materiala dira, inoiz ez aginduak.

Konpontzaileak bakarrik lan egiten du programekin. Ez du egunkariko ezer idazten: zerbaitek huts egiten
duenean jarduten du, arrazoia bilatzen du eta kopia batean konpontzen du. Ezin ditu artikuluen edo binetaren
testuak aldatu, ezta argitaratu ere, eta programa batek egiaztatzen du bere konponketa aplikatu aurretik (ADR 0087).

**Inongo agentek ez du berak idatzitakoa berrikusten.** Testu bakoitzak ez duen berrikusle batetik igarotzen da,
eta horrek iturri bakoitza irekitzen du eta baieztatu ezin duena kentzen du (ADR 0001).

| Agentea | Zer egiten duen |
| --- | --- |
| Idazlea eta berrikuslea | Eguneko artikuluak eta albiste laburrak. |
| Dokumentalista eta berrikuslea | Liburutegiko eta Biltegiko artikuluak, eta EduMediako gordetakoak. |
| Ilustratzailea eta marrazkien berrikuslea | Artikulu bakoitza azaltzen duen marrazki bat; berrikusleak bere orrian aztertzen du eta ulertzen ez dena itzultzen dio (ADR 0005). |
| Gidoilaria eta umorearen epailea | Binetarako bost gidoi; epaileak bat aukeratzen du (ADR 0023 eta 0024). |
| Kronista eta egiaztatzailea | «Duela urtebete». |
| Zutabegilea, egiaztatzailea eta zutabearen epailea | Asteazkeneko iritzi-zutabea; epaileak berriaren eta erreserbakoaren artean aukeratzen du (ADR 0092). |
| Erreportajeen burua, erreportaria, egiaztatzailea eta erreportajeen epailea | Igandeko erreportajea. |
| Iruzkingilea eta berrikuslea | Asteko iruzkina. |
| Bideo-gidoilaria | «Astea bideoan». |
| Itzultzaileak | Bat hizkuntza bakoitzeko, testu bakoitzerako. |
| Konpontzailea | Zerbaitek huts egiten duenean, zenbakia ateratzeko moduan konpontzen du; ez du testurik idazten ez aldatzen. |
| Bozeramailea | Goiz bakoitzeko abisuak hiru taldeetan eta Instagrameko testua. |

Guztiek [estilo-liburuarekin](../encargos/estilo.md) idazten dute, eta zeregin bakoitzak, gainera, bere gida du.

## 3. Egun bat egunkarian

Programa batek bost minuturik behin begiratzen du zer egin behar den eta egin duena apuntatzen du, ezer ez errepikatzeko.
Orduak Espainiako penintsulakoak dira: UTC+1 neguan eta UTC+2 udan.

| Ordua | Zer gertatzen den |
| --- | --- |
| 1:00 | Zenbakia prestatzen da aurreko egunean hitz egindakoarekin: artikuluak eta haien berrikuspena, marrazkiak, bineta, Liburutegia, Biltegia, «Duela urtebete», egiaztapenak, itzulpenak eta abisuak. Huts eginez gero, bigarren aldiz saiatzen da. |
| 5:00 | Zenbakia argitaratu aurretik ikus daiteke, gainbegiratzen duen pertsonak berrikus dezan (ADR 0025). Programa batek egiaztatzen du orria ondo ikusten dela tamaina desberdinetako pantailetan. |
| 6:30 | Zenbakia oraindik egin gabe badago, geldiarazten da eta dagoenarekin edo gordetako artikuluekin ateratzen da. |
| 6:50 | Webgunea argitaratzen da, eta artikulu bakoitza partekatzeko irudiak eta taldeetako abisuak prestatzen dira. Zerbaitek huts egiten badu, 10 minuturik behin saiatzen da berriro, 9:00ak arte. |
| 7:00 | Bot de IA Educativa-k zenbakiaren abisua argitaratzen du talde bakoitzean eta, egun horretan baliabidea ateratzen zaien pertsonei, pribatuan idazten die (ADR 0052). Egunkariaren Android aplikazioak zenbaki berria dagoela abisatzen du (ADR 0043). |
| 7:05 | Zenbakia Instagramen ateratzen da (ADR 0015). |
| 7:10 inguruan | Gainbegiratzen duen pertsonak txosten bat jasotzen du: zer atera den, gordetako artikulurik erabili den eta zerk huts egin duen (ADR 0069). |
| 8:00 | Gordetzeko artikulu berri bat idazten da, behar bada, eta iritzi-zutabe bat erreserban, bat ere geratzen ez bada. |
| 9:00, igandea | «Astea bideoan», amaieran erreportajearekin, Instagramen, X-n, Bluesky-n eta LinkedIn-en ateratzen da (ADR 0027). |
| 9:10etik aurrera | GitHub-en bereiz dabilen programa batek zenbakia atera dela egiaztatzen du eta, ateratzen ez bada, gordetako artikuluekin argitaratzen du. Egunkariak erantzuten ez badu, 7:30etik aurrera egiaztatzen du (ADR 0021). |
| Asteartea, gauean | Asteazkeneko zenbakiarekin iritzi-zutabea prestatzen da (ADR 0092). |
| Asteazkena | Argitaratutakoan funtzionatzeari utzi dioten estekak bilatzen dira (ADR 0056). |
| Argitaratzean | Zenbaki bakoitzaren kopia bat gordetzen da Internet Archive-ren artxiboan (ADR 0046). |

## 4. Egunik gabe zenbakirik ez

**Beti ateratzen da zenbaki bat** (ADR 0021 eta 0068). Prestaketak bi aldiz huts egiten badu, edo 6:30ean
amaitu gabe badago, gordetako artikuluekin ateratzen da, guztiekin edo falta direnekin soilik. Argitalpenak huts
egiten badu, GitHub-en bereiz dabilen programak egiten du, eta egunkariak ez du berriz egiten gainean.

**Hutsegite batengatik atera ez zena hurrengo egunean ateratzen da**: zenbaki bat gordetako artikuluekin atera bada
prestaketak huts egin zuelako, hurrengo gauean egun horretan hitz egindakoa ere jasotzen da, eta webguneak hala dio.

**Agente batek zenbakiko fitxategi bat hondatzen badu**, aurreko bertsioa berreskuratzen da eta agenteak bere lana
behin errepikatzen du. Eta prestaketak berriz hasi behar badu, ez du argitaratutzat ematen lehen saiakeran idatzi zena
(ADR 0076).

## 5. Erreserba: albisterik gabeko egunetarako gordetako artikuluak

Egunkariak aurrez idatzita ditu artikuluak eta beste pieza batzuk, zenbakirik inoiz ez falta dadin (ADR 0068):

| Zer | Zenbat | Erabiltzen ez bada, noiz kentzen den | Nondik datorren |
| --- | --- | --- | --- |
| Artikuluak | Sei: talde bakoitzeko bi | 60 egun; EduMediakoak, 30 | Egunkariak oraindik jorratu gabe zituen Biltegiko aplikazioak eta Liburutegiko dokumentuak, eta aspaldi EduMedia-IAG-n partekatutako tresnak (ADR 0077) |
| Bineta | Bat | 60 egun | Modatik pasatzen ez den gai bati buruzko txiste bat |
| «Duela urtebete» | Hurrengo zazpi gauetakoak | Gau berean | Aurrez idazten dira |
| Erreportajea | Bat astean | 28 egun | Modatik pasatzen ez den gai bati buruzkoa (ADR 0028) |
| Iritzi-zutabea | Bat | Hurrengo asteazkenean erabili edo baztertu egiten da | Egun batzuen mende ez dagoen eztabaida bati buruzkoa; epaileak berriarekin alderatzen du eta onena ateratzen da (ADR 0092) |

- **Noiz erabiltzen diren**: gauero, zenbakiak hiru artikulutara iristen ez bada edo talderen bat falta bazaio, eta
  prestaketak huts egiten duen guztietan. Lehenik, falta diren taldeetakoak.
- **Nola ordezkatzen diren**: goiz oro, gordetako gutxien dituen taldekoa idazten da. Dokumentalistatik,
  berrikuslearengandik, ilustratzailearengandik eta itzultzaileengandik igarotzen da, edozein artikulu bezala.
- **Bat erabili aurretik**, programa batek egiaztatzen du horrek jorratzen duenaren orria irekita jarraitzen duela;
  bestela, kendu egiten da.

## 6. Berrikuspenak

**AArekin**: zeregin bakoitzeko berrikuslea (iturriak, zifrak, izenak eta lehendik argitaratutakoa), marrazkien
berrikuslea, binetaren epailea, erreportajearen, «Duela urtebete»ren eta iritzi-zutabearen egiaztatzailea eta, gauero,
estilo-zuzentzaile bat, eguneko artikuluak edozein irakurlek bezala irakurtzen dituena eta ulertzeko zailak direnak
konpontzen dituena, daturik ukitu gabe (ADR 0083).

**Programekin, AArik gabe**, gauero:

| Zer egiaztatzen den | Erabakiaren erregistroa |
| --- | --- |
| Ez dela agenterik zenbakiko fitxategiak hondatu | ADR 0076 |
| Ez dela «quien» erabili «la persona que» zentzuarekin, ez dagoela ingelesez bakarrik dauden aipurik, «hoy» edo «ayer», «app» edo estilo-liburuak gomendatzen ez dituen beste hitzik (badaude, agente batek zuzentzen ditu) | ADR 0067 eta 0083 |
| Estilo-zuzentzaileak ez duela zifrarik, estekarik ez aipurik aldatu | ADR 0083 |
| Egunkariko egile bati ez zaiola berdin deitzen den beste pertsona baten zerbait egotzi (gertatzen bada, agente batek berrikusten du) | ADR 0066 |
| Arau finko bati jarraitzen dioten akatsak, hala nola «y» «i»ren aurrean, eta titular luzeegiak | ADR 0059 |
| Itzulpen bakoitzak jatorrizkoaren artikulu, esteka eta marrazki berberak dituela; bestela, zati hori gaztelaniaz ateratzen da | ADR 0026 |
| Itzulpen batean ez dela ezer gaztelaniaz geratu | ADR 0056 |
| Ez dagoela orririk hutsune zuririk, edozein tamainatako pantailetan | ADR 0041 |
| Funtzionatzeari utzi dioten estekak, asteazkenetan | ADR 0056 |

**Pertsona batek** zenbakia berrikus dezake 5:00etan eta aldaketak eskatu 6:50 aurretik, baina egunkariak ez du
hori agintzen: erantzunik ez badago, bere orduan ateratzen da (ADR 0058).

## 7. Zenbaki bakoitzetik ateratzen dena

Zenbakia ez da webgunea bakarrik. Hortik hauek ere ateratzen dira:

- **hiru taldeetako abisuak** eta **mezu pribatuak** baliabidea ageri zaien pertsonei;
- **Instagrameko argitalpena**, bere testuarekin;
- artikulu bakoitza **partekatzeko irudia**;
- igandean, **«Astea bideoan»** sare sozialetan.

**Zenbaki batean zerbait aldatzen bada atera aurretik, horren mende dagoen guztia berriz egiten da**: binetak
aldatzen bada, harekin hitz egiten duen abisua; titular bat aldatzen bada, bere partekatzeko irudia; erreportajea
aldatzen bada, asteko bideoa eta bere testuak.

## 8. Zuzenketak

- **Datu oker bat artikuluan zuzentzen da, amaieran ohar batekin** eta bost hizkuntzatan (ADR 0055): «Corregido el…»
  (akats bat zegoen), «Actualización del…» (datua zuzena zen eta aldatu da) edo «Nota añadida el…» (zerbait falta
  zen). Zentzua aldatzen ez duen akats bat oharrik gabe zuzentzen da.
- Zuzendu aurretik, datua bere iturrian egiaztatzen da: akats-abisu bat ere oker egon daiteke.
- **Talde bati bidalita dagoen abisu bat zuzendu egiten da**, botarekin editatuz.

## 9. Pertsonak, pribatutasuna eta gardentasuna

- **Pertsona bakoitza nor den jakiteko, bere Telegrameko kontua begiratzen da, ez erakusten duen izena**, bi
  pertsonak izen bera izan baitezakete (ADR 0066).
- **Baliabide baten egilea izendatzen da, berak argitaratu badu bakarrik**; taldeetako iritziak ez zaizkio inori
  egozten (estilo-liburua). Egunkariaren iritzi propio bakarra asteazkeneko zutabea da, idazten duen ereduak sinatua
  (ADR 0092).
- **Ez da ezer biltzen irakurleengandik**: bisita-kontagailuak batu baino ez du egiten, cookierik eta datu
  pertsonalik gabe (ADR 0033), eta iruzkinak irakurleak botoia sakatzen badu bakarrik kargatzen dira (ADR 0030).
  [Pribatutasun-politikak](https://diarioiaeducativa.github.io/privacidad.html) azaltzen du (ADR 0070).
- **Egunkaria AArekin egina dagoela dioen abisu bakarra**, orri guztien oinean. [«Erredakzioa»](https://diarioiaeducativa.github.io/redaccion.html)
  orriak azaltzen du nola egiten den, nork erantzuten duen argitaratutakoaz eta ez dagoela publizitaterik ez
  babesik (ADR 0055 eta 0065).
- Egunkaria egiten duten programak publikoak dira (ADR 0019).

## 10. Iritziaren ildoa

Iritzi-zutabeak bere zutabegileak aukeratzen duen jarrera defendatzen du, printzipio hauen barruan. Egunkariaren ildoa
dira: ez dute esaten eztabaida bakoitzaz zer pentsatu, baizik eta nondik iritzia eman.

1. **Lehenik, ikaskuntza.** Teknologia bat ikasten eta irakasten laguntzeko ekartzen duenaren arabera epaitzen da, ez
   berria delako.
2. **Ikasleen datuak babesten dira.** Ezer ez, beharrik gabe ikasleen datu pertsonalak enpresa bati ematera behartzen
   duenik. Kontrola ikastetxeari eta irakasleari uzten dionari eta plataforma bakar bati lotzen ez zaionari
   ematen zaio lehentasuna, benetan balio duenari uko egin gabe.
3. **AA tresna bat da.** Erabilera bakoitzaren atzean erabakitzen eta erantzuten duen pertsona bat dago. Ikasleak
   ebaluatzea, kalifikatzea eta haiei buruz erabakitzea irakasleei dagokie.
4. **Edozein irakasleren eskura.** Proposatzen dena ordaindu gabe eta irakasle arrunt batek dakien baino gehiago jakin
   gabe egin daiteke, eta geletan benetan nola lan egiten den oinarri hartzen du.
5. **Ekitatea.** Ikasle guztiek ez dituzten baliabideekin edo gailuekin bakarrik funtzionatzen duena ez da irtenbide
   orokor gisa aurkezten.
6. **Gardentasuna.** AA erabiltzea ez da lotsatzeko ez susmatzeko arrazoi: noiz eta nola erabili den esaten da.
   Familiek legeak eskatzen duena baino gehiago jakiteko eskubidea dute.
7. **Zorroztasuna, indarra baino lehen.** Datu zehatzak eta egiaztagarriak, kontrako jarrera bere bertsiorik onenean, eta
   ez alarmismorik ez prospektu-gisako gogo biziegirik.

**Nork aplikatzen dituen**: zutabegileak, bere enkarguarekin jasotzen dituena eta haien barruan gaia eta jarrera
aukeratzen dituena.
**Nola egiaztatzen den**: egiaztatzaileak ez du argitaratzen horietako baten aurka doan zutaberik, horregatik tesia
aldatu gabe, eta epaileak haiekin talka egiten duena baztertzen du erreserbakoarekin alderatzean (ADR 0092).

## 11. Hobetzeke dagoena

Oraindik oso ondo funtzionatzen ez duena edo egiaztapen bakar baten mende dagoena. Hortik hobetu daiteke egunkaria:

- **Zuzenketa batek ez du bere kabuz iristen jada bidalitakora.** Artikulu bat argitaratu ondoren zuzentzen bada,
  taldeetan jada atera zen abisua eskuz aldatu behar da, eta Instagramen eta gainerako sareetan argitaratutakoa ez
  da aldatzen.
- **Albisterik gabeko egunetarako gordetako EduMediako artikuluak** 2026ko azaroaren 16an hasi ziren idazten:
  oraindik ez da bat ere atera zenbaki batean.
- **Gordetako artikulu bat argitaratu baino pixka bat lehenago berrikusten da.** Egun edo aste lehenago idazten dira,
  eta bat erabili baino lehen, hitz egiten duen tresnaren orria irekita jarraitzen duela bakarrik egiaztatzen da,
  ez kontatzen duenetik zerbait aldatu den, adibidez doakoa izateari utzi dion. Horregatik, EduMediakoak, sarri
  aldatzen diren tresnei buruzkoak, hilabetera kentzen dira.
- **Gordetzeko artikulu bat idazten ari den bitartean**, prestatzen ari den webguneak minutu batzuetan zenbaki bat
  balitz bezala erakusten du. Une horretan bertan webgunea argitaratuko balitz, ateratzea gertatuko litzateke.
- **Agente batek fitxategi bat hondatzen badu, gauero egiten den prestaketan bakarrik berreskuratzen da**, ez
  erreportajearenean, Liburutegiarenean edo Biltegiarenean.
- **Itzulpenak programa batek egiaztatzen ditu**, artikulu guztiak daudela eta ez dela ezer gaztelaniaz geratu
  begiratzen duena, baina ez ditu agenteren batek berrikusten.
- **Noiz uste den egun batek Biltegiko aplikazio berri gutxi dituela**, eta lehengo bat erreskatatzen den, begi
  hutsez erabaki zen eta doitzeke dago.
- **Instagram behin bakarrik saiatzen da**: huts egiten badu, eskuz argitaratu behar da.
