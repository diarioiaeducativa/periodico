<!-- origen: 3fb0b86e7ca01517 -->
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
- **Tiza eta Algoritmoren bineta**, eguneko albisteetako bati buruzkoa (ADR 0023).
- **Igandeetan**, gainera, gai bakar bat sakon azaltzen duen erreportaje bat (ADR 0004 eta 0028) eta «Astea
  bideoan», asteko gauzarik nabarmenenekin egindako bideo laburra (ADR 0016 eta 0027). Igande gauean, gainera,
  asteko gauzarik garrantzitsuenari buruzko iruzkin bat idazten da (ADR 0038).

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

## 2. Nork egiten duen zer

Agenteak Anthropic-en Claude AA ereduak dira: Sonnet-ek egunero idazten eta berrikusten du, Opus-ek erreportaje
onena aukeratzen du, testu luzeak idazten ditu eta huts egiten duena konpontzen du, eta Fable-k bineta idazten
eta aukeratzen du. **Egunkaria idazten duten agenteek ezin dute programarik exekutatu**: testuak irakurri eta
idatzi eta interneten kontsultatu baino ez dute egiten. Horrela, taldeetako mezuetan datorrenak, beste pertsona
batzuek idatzitakoak, ezin die beste ezer egiterik eragin (ADR 0002). Mezuak informatzeko materiala dira, inoiz
ez aginduak.

Konpontzaileak bakarrik lan egiten du programekin. Ez du egunkariko ezer idazten: zerbaitek huts egiten
duenean jarduten du, arrazoia bilatzen du eta kopia batean konpontzen du. Ezin ditu artikuluen edo binetaren
testuak aldatu, ezta argitaratu ere, eta programa batek egiaztatzen du bere konponketa, aplikatu aurretik (ADR
0087).

**Inork ez du berak idatzitakoa berrikusten.** Testu bakoitza berrikusle batengandik pasatzen da, berak idatzi
ez duen batengandik, eta hark iturri bakoitza irekitzen du eta berretsi ezin duena kentzen du (ADR 0001).

| Agentea | Zer egiten duen |
| --- | --- |
| Idazlea eta berrikuslea | Eguneko artikuluak eta albiste laburrak. |
| Dokumentalista eta berrikuslea | Liburutegiko eta Biltegiko artikuluak, eta EduMediaren gordetakoak. |
| Ilustratzailea eta marrazkien berrikuslea | Artikulu bakoitza azaltzen duen marrazki bat; berrikusleak bere orrian ikusten du eta ulertzen ez dena itzultzen dio (ADR 0005). |
| Gidoilaria eta umorearen epailea | Binetarako bost gidoi; epaileak bat aukeratzen du (ADR 0023 eta 0024). |
| Kronista eta egiaztatzailea | «Duela urtebete». |
| Erreportajeen burua, erreportaria, egiaztatzailea eta erreportajeen epailea | Igandeko erreportajea. |
| Iruzkingilea eta berrikuslea | Asteko iruzkina. |
| Bideoko gidoilaria | «Astea bideoan». |
| Itzultzaileak | Hizkuntza bakoitzeko bat, testu bakoitzerako. |
| Konpontzailea | Zerbaitek huts egiten duenean, zenbakia ateratzeko moduan konpontzen du; ez ditu testuak idazten ez aldatzen. |
| Bozeramailea | Goizero hiru taldeetako abisuak eta Instagrameko testua. |

Guztiek [estilo-liburuaren](../encargos/estilo.md) arabera idazten dute, eta zeregin bakoitzak, gainera, bere
gida du.

## 3. Egun bat egunkarian

Programa batek bost minuturik behin begiratzen du zer dagoen egiteko, eta egindakoa idazten du, ezer ez
errepikatzeko. Orduak Espainiako penintsulakoak dira: UTC+1 neguan eta UTC+2 udan.

| Ordua | Zer gertatzen den |
| --- | --- |
| 1:00 | Zenbakia prestatzen da aurreko egunean hitz egindakoarekin: artikuluak eta haien berrikusketa, marrazkiak, bineta, Liburutegia, Biltegia, «Duela urtebete», egiaztapenak, itzulpenak eta abisuak. Huts egiten badu, bigarren aldiz saiatzen da. |
| 5:00 | Zenbakia argitaratu aurretik ikus daiteke, gainbegiratzen duen pertsonak berrikus dezan (ADR 0025). Programa batek egiaztatzen du orria ondo ikusten dela tamaina desberdineko pantailetan. |
| 6:30 | Zenbakia oraindik egin gabe badago, geldituko da, eta dagoenarekin edo gordetako artikuluekin ateratzen da. |
| 6:50 | Web-orria argitaratzen da, eta artikulu bakoitza partekatzeko irudiak eta taldeetako abisuak prestatzen dira. Zerbaitek huts egiten badu, 10 minuturik behin saiatzen da berriro, 9:00ak arte. |
| 7:00 | Bot de IA Educativak zenbakiaren abisua argitaratzen du talde bakoitzean, eta egun horretan baliabidea ateratzen zaien pertsonei pribatuan idazten die (ADR 0052). Egunkariaren Android aplikazioak zenbaki berriaren berri ematen du (ADR 0043). |
| 7:05 | Zenbakia Instagramen ateratzen da (ADR 0015). |
| 7:10 inguruan | Gainbegiratzen duen pertsonak txosten bat jasotzen du: zer atera den, gordetako artikulurik erabili den eta zerk huts egin duen (ADR 0069). |
| 8:00 | Artikulu berri bat idazten da gordetzeko, behar bada. |
| 9:00, igandea | «Astea bideoan», amaieran erreportajearekin, Instagramen, X-n, Bluesky-n eta LinkedIn-en ateratzen da (ADR 0027). |
| 9:10etik aurrera | Aparte funtzionatzen duen programa batek, GitHuben, zenbakia atera dela egiaztatzen du, eta, ez bada atera, gordetako artikuluekin argitaratzen du. Egunkariak erantzuten ez badu, 7:30etik bertatik egiaztatzen du (ADR 0021). |
| Asteazkenetan | Argitaratutakoan funtzionatzeari utzi dioten estekak bilatzen dira (ADR 0056). |
| Argitaratzean | Zenbaki bakoitzaren kopia bat gordetzen da Internet Archive-ren artxiboan (ADR 0046). |

## 4. Zenbakirik gabeko egunik ez

**Beti ateratzen da zenbaki bat** (ADR 0021 eta 0068). Prestaketak bi aldiz huts egiten badu, edo 6:30ean
amaitu gabe badago, gordetako artikuluekin ateratzen da, guztiekin edo falta direnekin bakarrik. Argitalpenak
huts egiten badu, aparte funtzionatzen duen programak egiten du, GitHuben, eta egunkariak ez du berriro egiten
gainean.

**Hutsegite bategatik atera ez zena hurrengo egunean ateratzen da**: zenbaki bat gordetako artikuluekin atera
bada prestaketak huts egin zuelako, hurrengo gauean egun horretan hitz egindakoa ere biltzen da, eta web-orriak
hala dio.

**Agente batek zenbakiko fitxategi bat hondatzen badu**, aurreko bertsioa berreskuratzen da, eta agenteak bere
lana behin errepikatzen du. Eta prestaketak berriro hasi behar badu, ez du argitaratutzat ematen lehen saiakeran
idatzi zena (ADR 0076).

## 5. Erreserba: albisterik gabeko egunetarako gordetako artikuluak

Egunkariak aldez aurretik idatzita ditu artikuluak eta beste pieza batzuk, zenbakirik inoiz falta ez dadin (ADR
0068):

| Zer | Zenbat | Erabiltzen ez bada, noiz kentzen den | Nondik datorren |
| --- | --- | --- | --- |
| Artikuluak | Sei: talde bakoitzeko bi | 60 egun; EduMediarenak, 30 | Egunkariak oraindik jorratu gabeko Biltegiko aplikazioak eta Liburutegiko dokumentuak, eta EduMedia-IAG-en aspaldi partekatutako tresnak (ADR 0077) |
| Bineta | Bat | 60 egun | Modatik pasatzen ez den gai bati buruzko txiste bat |
| «Duela urtebete» | Hurrengo zazpi gauetakoak | Gau horretan bertan | Aldez aurretik idazten dira |
| Erreportajea | Astean bat | 28 egun | Modatik pasatzen ez den gai bati buruz (ADR 0028) |

- **Noiz erabiltzen diren**: gauero, zenbakiak hiru artikulura iristen ez bada edo talderen bat falta bazaio,
  eta prestaketak huts egiten duen guztietan. Lehenik, falta diren taldeetakoak.
- **Nola berritzen diren**: goiz oro bat idazten da, gordetako gutxien dituen taldekoa. Dokumentalistarengandik,
  berrikuslearengandik, ilustratzailearengandik eta itzultzaileengandik pasatzen da, beste edozein artikulu
  bezala.
- **Bat erabili aurretik**, programa batek egiaztatzen du aipatzen duen orria irekita jarraitzen duela; ez
  bada, kendu egiten da.

## 6. Berrikusketak

**AArekin**: zeregin bakoitzaren berrikuslea (iturriak, zifrak, izenak eta lehen argitaratutakoa), marrazkien
berrikuslea, binetaren epailea, erreportajearen eta «Duela urtebete»ren egiaztatzailea eta, gauero, estilo-zuzentzaile
bat, eguneko artikuluak edozein irakurlek bezala irakurtzen dituena eta ulertzeko zailak direnak konpontzen
dituena, daturik ukitu gabe (ADR 0083).

**Programekin, AArik gabe**, gauero:

| Zer egiaztatzen den | Erabakiaren erregistroa |
| --- | --- |
| Agenteren batek zenbakiko fitxategiak hondatu ez dituela | ADR 0076 |
| Ez dela «quien» erabiltzen «la persona que» zentzuarekin, ezta ingelesez soilik dauden aipuak, «hoy» edo «ayer», «app» edo estilo-liburuak desaholkatzen ez dituen beste hitz batzuk ere (badaude, agente batek zuzentzen ditu) | ADR 0067 eta 0083 |
| Estilo-zuzentzaileak ez duela zifrarik, estekarik ez aipurik aldatu | ADR 0083 |
| Egunkariko egile bati, izen bera duen beste pertsona baten zerbait ez egozten zaiola (gertatzen bada, agente batek berrikusten du) | ADR 0066 |
| Arau finkoa duten akatsak, esate baterako «y» «i»ren aurrean, eta titular luzeegiak | ADR 0059 |
| Itzulpen bakoitzak jatorrizkoaren artikulu, esteka eta marrazki berberak dituela; ez bada, atal hori gaztelaniaz ateratzen da | ADR 0026 |
| Itzulpen batean ezer gaztelaniaz geratu ez dela | ADR 0056 |
| Orriren batek ez duela hutsune zuririk, edozein tamainatako pantailetan | ADR 0041 |
| Funtzionatzeari utzi dioten estekak, asteazkenetan | ADR 0056 |

**Pertsona batek** zenbakia 5:00etan berrikus dezake eta aldaketak eskatu 6:50 baino lehen, baina egunkariak ez
du hori agintzen: erantzunik ez badago, bere orduan ateratzen da (ADR 0058).

## 7. Zenbaki bakoitzetik ateratzen dena

Zenbakia ez da web-orria bakarrik. Hortik abiatuta hauek ere ateratzen dira:

- **hiru taldeetako abisuak** eta baliabidea ageri zaien pertsonei bidalitako **mezu pribatuak**;
- **Instagrameko argitalpena**, bere testuarekin;
- artikulu bakoitza partekatzeko **irudia**;
- igandean, **«Astea bideoan»** sare sozialetan.

**Zenbaki batean zerbait aldatzen bada atera aurretik, horren mende dagoen guztia berregiten da**: bineta
aldatzen bada, hari buruz hitz egiten duen abisua; titular bat aldatzen bada, bere partekatzeko irudia;
erreportajea aldatzen bada, asteko bideoa eta bere testuak.

## 8. Zuzenketak

- **Datu oker bat artikuluan zuzentzen da, amaieran ohar batekin**, eta bost hizkuntzatan (ADR 0055):
  «Corregido el…» (akats bat zegoen), «Actualización del…» (datua egiazkoa zen eta aldatu da) edo «Nota
  añadida el…» (zerbait falta zen). Esanahia aldatzen ez duen akats bat oharrik gabe zuzentzen da.
- Zuzendu aurretik, datua bere iturrian egiaztatzen da: akats baten abisua ere oker egon daiteke.
- **Talde batera bidali den abisu bat zuzentzen da**, botarekin editatuz.

## 9. Pertsonak, pribatutasuna eta gardentasuna

- **Pertsona bakoitza nor den jakiteko, bere Telegram kontua begiratzen da, ez erakusten duen izena**, bi
  pertsonak izen bera izan dezaketelako (ADR 0066).
- **Baliabide baten egilea bakarrik aipatzen da, berak argitaratu badu**; taldeetako iritziak ez zaizkio
  inori egozten (estilo-liburua).
- **Ez da irakurleei buruzko ezer biltzen**: bisita-kontagailuak batu baino ez du egiten, cookierik eta datu
  pertsonalik gabe (ADR 0033), eta iruzkinak irakurleak botoia sakatzen badu bakarrik kargatzen dira (ADR
  0030). [Pribatutasun-politikak](https://diarioiaeducativa.github.io/privacidad.html) azaltzen du (ADR 0070).
- **Egunkaria AArekin egina dagoela dioen abisu bakarra**, orri guztien oinean. [«Erredakzioa»](https://diarioiaeducativa.github.io/redaccion.html)
  orriak azaltzen du nola egiten den, nork erantzuten duen argitaratutakoaz eta ez dagoela publizitaterik ez
  babesik (ADR 0055 eta 0065).
- Egunkaria egiten duten programak publikoak dira (ADR 0019).

## 10. Hobetzeke dagoena

Oraindik oso ondo ez dabilena edo egiaztapen bakar baten mende dagoena. Hortik hobe daiteke egunkaria:

- **Zuzenketa batek ez du bere kabuz iristen ordurako bidalitakora.** Artikulu bat argitaratu ondoren zuzentzen
  bada, taldeetan ordurako atera zen abisua eskuz aldatu behar da, eta Instagramen eta beste sareetan
  argitaratutakoa ez da aldatzen.
- **Taldeko albisterik gabeko egunetarako gordetako EduMediaren artikuluak** 2026ko azaroaren 16an hasi ziren
  idazten: oraindik ez da bat ere atera zenbaki batean.
- **Gordetako artikulu bat argitaratu baino pixka bat lehenago berrikusten da.** Egun edo aste batzuk
  lehenago idazten dira, eta bat erabili baino lehen, hitz egiten duen tresnaren orria irekita jarraitzen
  duela egiaztatzen da soilik, ez kontatzen duenetik zerbait aldatu den, adibidez doakoa izateari utzi dion.
  Horregatik, EduMediarenak, maiz aldatzen diren tresnei buruzkoak, hilabetera kentzen dira.
- **Gordetzeko artikulu bat idazten ari den bitartean**, prestatzen ari den web-orriak minutu batzuetan
  egunkariaren zenbaki balitz bezala erakusten du. Orduantxe web-orria argitaratuko balitz, aterako litzateke.
- **Agente batek fitxategi bat hondatzen badu, gauero egiten den prestaketan bakarrik berreskuratzen da bere
  kabuz**, ez erreportajearenean, Liburutegiarenean edo Biltegiarenean.
- **Itzulpenak programa batek egiaztatzen ditu**, artikulu guztiak daudela eta ezer ez dela gaztelaniaz
  geratu begiratzen duena, baina inongo agentek ez ditu berrikusten.
- **Noiz uste den egun batek Biltegiko aplikazio berri gutxi dituela**, eta lehenagoko bat erreskatatzen den,
  begi-neurriz erabaki zen eta doitzeke dago.
- **Instagram behin bakarrik saiatzen da**: huts egiten badu, eskuz argitaratu behar da.
