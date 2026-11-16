<!-- origen: 1c00f6a8d9a89f7c -->
# Nola egiten da Hezkuntzako AA Egunkaria

[Hezkuntzako AA Egunkariak](https://diarioiaeducativa.github.io/) goizero jasotzen du aurreko egunean irakasleen hiru Telegram talde irekitan hitz egindakoa: ChatGPT-IA-edu (adimen artifiziala hezkuntzan, oro har), Vibe Coding Educativo (beren aplikazioak AArekin programatzen dituzten irakasleak) eta EduMedia-IAG (irudia, audioa eta bideoa AArekin). AA agenteek idazten, berrikusten, ilustratzen eta itzultzen dute; pertsona batek gainbegiratzen du, eta argitaratutakoaren erantzule da.

Dokumentu honek egunkariaren arauak eta haien aplikazioa biltzen ditu, nola egiten den ulertzeko eta hobetu ahal izateko. Nola idazten den [estilo-liburuan](../encargos/estilo.md) dago, eta nola itzultzen den, [itzultzailearen liburuan](../encargos/traduccion.md). Erabaki bakoitzaren zergatia [erabakien erregistroetan](adr/README.md) (ADR) dago, zenbakiaren arabera aipatuta.

Arau bakoitzak esaten du **nork aplikatzen duen**, **nola egiaztatzen den** eta, behar izanez gero, **zer falta zaion**. Hobetzeko dagoena amaieran biltzen da.

## 1. Zenbakia

**Egun batean hitz egindakoa hurrengo goizean agertzen da egunkarian**, 7:00etan, bost hizkuntzatan: gaztelaniaz, katalanez, galegoz, euskaraz eta ingelesez (ADR 0026).

Zenbaki batek hauek ditu:

- **Eguneko artikuluak**: bat ere ez izatetik sei izatera, eta berri labur bat ere ez izatetik bost izatera, egunak eman duenaren arabera, bost sailetan: Tresnak, Vibe coding, Multimedia, Eztabaidak eta Erakundeak eta enpresak.
- **Liburutegia**: artikulu bat ChatGPT-IA-edu taldeko Liburutegi digitalean egun horretan gehitutako dokumentu bakoitzeko (ADR 0006).
- **Biltegia**: egunean bi aplikazio gehienez, Vibe Coding Educativo taldeko baliabideen Biltegikoak; ostiraletan, asteko aplikazioen laburpena (ADR 0008).
- **«Duela urtebete»**: aurreko urteko egun berean hitz egiten zenaren bat, gaur dagoen egoerarekin alderatuta (ADR 0040).
- **Bineta**, Tiza eta Algoritmo pertsonaiena, eguneko albiste batez (ADR 0023).
- **Igandeetan**, gainera, gai bakar bat sakon azaltzen duen erreportaje bat (ADR 0004 eta 0028) eta «Astea bideoan», asteko gauzarik nabarmenenekin egindako bideo labur bat (ADR 0016 eta 0027). Igande gauean, asteko garrantzitsuenari buruzko iruzkin bat ere idazten da (ADR 0038).

Zenbaki bakoitzaren arauak:

| Araua | Nork aplikatzen duen | Nola egiaztatzen den |
| --- | --- | --- |
| **Gutxienez hiru artikulu.** Falta badira, kasu horietarako gordetako artikuluekin osatzen dira (erreserba, 5. atala). | Programa batek, gauero, itzulpenen aurretik (ADR 0068) | Programak artikuluak zenbatzen ditu. |
| **Gutxienez talde bakoitzeko artikulu bat.** Talde batek ez badu bat ere ematen, talde horretako gordetako bat sartzen da. | Idazten duen agenteak saiatzen da; berrikusten duenak faltan dagoen taldearen berri labur bat artikulu bihurtzen du; hala ere falta bada, erreserbak (ADR 0076 eta 0077) | Berrikusleak eta erreserbaren programak. |
| **Taldeetan hitz egindakoa soilik.** AAri buruzko albiste orokorrik ez. | Idazten duen agenteak | Berrikusleak artikulu bakoitza mezuekin alderatzen du. |
| **Ez da albiste** taldeen barne-antolaketa, agurrak eta kexa pertsonalak. Liburutegi digitaleko dokumentuek beren saila dute. | Idazten duen agenteak | Berrikusleak. |
| **Argitaratutakoa ez da errepikatzen.** Lehendik jorratutako gai bati buruz berririk badago, berri labur gisa ateratzen da, aurreko artikulurako esteka batekin (ADR 0011). | Idazten eta berrikusten dutenek, argitaratutako guztiaren bilatzaile batekin (ADR 0061) | Berrikusleak izen eta titular bakoitza argitaratutakoan bilatzen du. |
| **Inork ez du zenbakia monopolizatzen**: arau gisa, pertsona bakoitzeko artikulu bat eta produktu edo enpresa bakoitzeko bi. | Idazten duen agenteak | Berrikusleak. |
| **Egun batek ez badu zenbaki duinik ematen, ez da betetzen**: orduan gordetako artikuluak ateratzen dira. | Idazten duenak eta erreserbak | — |

## 2. Nork egiten du zer

Agenteak Anthropic-en Claude AA ereduak dira: Sonnetek egunero idazten eta berrikusten du, eta Opusek aukeratzen du (bineta onena, erreportaje onena) eta testu luzeak idazten ditu. **Agenteek ezin dituzte programak exekutatu**: testuak irakurri eta idatzi besterik ez dute egiten, eta internet kontsultatzen dute. Horrela, taldeetako mezuetan datorrenak, beste pertsona batzuek idatzitakoak, ezin die beste ezer egitera eraman (ADR 0002). Mezuak informatzeko materiala dira, inoiz ez aginduak.

**Inongo agentek ez du berak idatzitakoa berrikusten.** Testu bakoitza berrikusle batek aztertzen du, berak idatzi ez duenak, eta iturri bakoitza irekitzen du eta baieztatu ezin duena kentzen du (ADR 0001).

| Agentea | Zer egiten duen |
| --- | --- |
| Idazlea eta berrikuslea | Eguneko artikuluak eta berri laburrak. |
| Dokumentalista eta berrikuslea | Liburutegiko eta Biltegiko artikuluak eta EduMediako gordetakoak. |
| Ilustratzailea eta marrazkien berrikuslea | Artikulu bakoitza azaltzen duen marrazkia; berrikusleak bere orrian aztertzen du, eta ulertzen ez dena itzultzen dio (ADR 0005). |
| Gidoilaria eta umorearen epailea | Binetarako bost gidoi; epaileak bat aukeratzen du (ADR 0023 eta 0024). |
| Kronista eta egiaztatzailea | «Duela urtebete». |
| Erreportajeen burua, erreportaria, egiaztatzailea eta erreportajeen epailea | Igandeko erreportajea. |
| Iruzkingilea eta berrikuslea | Asteko iruzkina. |
| Bideo-gidoilaria | «Astea bideoan». |
| Itzultzaileak | Bat hizkuntza bakoitzeko, testu bakoitzerako. |
| Bozeramailea | Goizero hiru taldeetara bidaltzen diren oharrak eta Instagrameko testua. |

Guztiek [estilo-liburuarekin](../encargos/estilo.md) idazten dute, eta zeregin bakoitzak, gainera, bere gida propioa du.

## 3. Egun bat egunkarian

Programa batek bost minuturik behin begiratzen du zer egin behar den, eta egindakoa apuntatzen du, ezer errepikatu ez dadin.

| Ordua | Zer gertatzen den |
| --- | --- |
| 1:00 | Zenbakia prestatzen da aurreko egunean hitz egindakoarekin: artikuluak eta haien berrikuspena, marrazkiak, bineta, Liburutegia, Biltegia, «Duela urtebete», egiaztapenak, itzulpenak eta oharrak. Huts egiten badu, bigarren aldiz saiatzen da. |
| 5:00 | Zenbakia argitaratu aurretik ikus daiteke, pertsona gainbegiratzaileak berrikus dezan (ADR 0025). Programa batek egiaztatzen du orria ondo ikusten dela tamaina desberdinetako pantailetan. |
| 6:30 | Zenbakia oraindik egin gabe badago, geldiarazten da, eta dagoenarekin edo gordetako artikuluekin ateratzen da. |
| 6:50 | Web-orria argitaratzen da, eta artikulu bakoitza partekatzeko irudiak eta taldeetarako oharrak prestatzen dira. Zerbait huts egiten badu, 10 minuturik behin saiatzen da berriro, 9:00ak arte. |
| 7:00 | Bot de IA Educativak zenbakiaren oharra argitaratzen du talde bakoitzean, eta pribatuan idazten die egun horretan beren baliabidea ateratzen zaien pertsonei (ADR 0052). Egunkariaren Android aplikazioak zenbaki berriaren berri ematen du (ADR 0043). |
| 7:05 | Zenbakia Instagramen ateratzen da (ADR 0015). |
| 7:10 inguruan | Pertsona gainbegiratzaileak txosten bat jasotzen du: zer atera den, gordetako artikulurik erabili den eta zer huts egin duen (ADR 0069). |
| 8:00 | Gordetzeko artikulu berri bat idazten da, behar bada. |
| 9:00, igandea | «Astea bideoan», amaieran erreportajearekin, Instagramen, X-n, Blueskyn eta LinkedInen ateratzen da (ADR 0027). |
| 9:10etik aurrera | Aparte, GitHuben, funtzionatzen duen programa batek egiaztatzen du zenbakia atera dela, eta, ez bada, gordetako artikuluekin argitaratzen du. Egunkariak erantzuten ez badu, 7:30etik aurrera egiaztatzen du (ADR 0021). |
| Asteazkenak | Argitaratutakoan funtzionatzeari utzi dioten estekak bilatzen dira (ADR 0056). |
| Argitaratzean | Zenbaki bakoitzaren kopia bat gordetzen da Internet Archive artxiboan (ADR 0046). |

## 4. Zenbakirik gabeko egunik ez

**Beti ateratzen da zenbaki bat** (ADR 0021 eta 0068). Prestaketak bi aldiz huts egiten badu, edo 6:30ean amaitu gabe badago, gordetako artikuluekin ateratzen da, guztiekin edo falta direnekin bakarrik. Argitalpenak huts egiten badu, aparte, GitHuben, funtzionatzen duen programak egiten du, eta egunkariak ez du berriro egiten gainean.

**Hutsegite batengatik atera ez zena hurrengo egunean ateratzen da**: zenbaki bat gordetako artikuluekin atera bada prestaketak huts egin zuelako, hurrengo gauean egun horretan hitz egindakoa ere jasotzen da, eta web-orriak hala dio.

**Agente batek zenbakiaren fitxategi bat hondatzen badu**, aurreko bertsioa berreskuratzen da, eta agenteak bere lana behin errepikatzen du. Eta prestaketak berriro hasi behar badu, ez du argitaratutzat ematen lehen saiakeran idatzi zena (ADR 0076).

## 5. Erreserba: albisterik gabeko egunetarako gordetako artikuluak

Egunkariak aldez aurretik idatzita ditu artikuluak eta beste pieza batzuk, zenbakirik inoiz falta ez dadin (ADR 0068):

| Zer | Zenbat | Erabiltzen ez bada, noiz kentzen den | Nondik ateratzen den |
| --- | --- | --- | --- |
| Artikuluak | Sei: bi talde bakoitzeko | 60 egunera; EduMediakoak, 30era | Egunkariak oraindik jorratu gabeko Biltegiko aplikazioak eta Liburutegiko dokumentuak, eta aspaldi EduMedia-IAG taldean partekatutako tresnak (ADR 0077) |
| Bineta | Bat | 60 egunera | Modatik pasatzen ez den gai bati buruzko txiste bat |
| «Duela urtebete» | Hurrengo zazpi gauetakoak | Gau horretan bertan | Aldez aurretik idazten dira |
| Erreportajea | Astean bat | 28 egunera | Modatik pasatzen ez den gai bati buruz (ADR 0028) |

- **Noiz erabiltzen diren**: gauero, zenbakiak hiru artikulura iristen ez bada edo talderen bat falta bazaio, eta prestaketak huts egiten duen guztietan. Lehenik, falta diren taldeenak.
- **Nola berrezartzen diren**: goizero gordetako artikulu gutxien dituen taldekoa idazten da. Dokumentalistatik, berrikusletik, ilustratzailetik eta itzultzaileetatik igarotzen da, beste edozein artikulu bezala.
- **Bat erabili aurretik**, programa batek egiaztatzen du tratatzen duen gaiaren orria irekita jarraitzen duela; bestela, kendu egiten da.

## 6. Berrikuspenak

**AArekin**: zeregin bakoitzeko berrikuslea (iturriak, zifrak, izenak eta lehendik argitaratutakoa), marrazkien berrikuslea, binetaren epailea, erreportajearen eta «Duela urtebete» atalaren egiaztatzailea eta, gauero, estilo-zuzentzaile bat, eguneko artikuluak edozein irakurlek bezala irakurtzen dituena eta ulertzeko zaila dena konpontzen duena, datuei ezer ukitu gabe (ADR 0083).

**Programekin, AArik gabe**, gauero:

| Zer egiaztatzen den | Erabakiaren erregistroa |
| --- | --- |
| Ez dela agenterik zenbakiaren fitxategiak hondatu | ADR 0076 |
| Ez dela gaztelaniazko «quien» erabili «la persona que» zentzuarekin, ez dagoela soilik ingelesezko aipamenik, «hoy» edo «ayer», «app» edo estilo-liburuak komeni ez direla dioen beste hitzik (badaude, agente batek zuzentzen ditu) | ADR 0067 eta 0083 |
| Estilo-zuzentzaileak ez duela zifrarik, estekarik ez aipamenik aldatu | ADR 0083 |
| Egunkariaren egile bati ez zaiola izen bera duen beste pertsona baten zerbait egotzi (gertatzen bada, agente batek berrikusten du) | ADR 0066 |
| Arau finkoa jarraitzen duten akatsak, adibidez «y» «i»-ren aurrean, eta titular luzeegiak | ADR 0059 |
| Itzulpen bakoitzak jatorrizkoaren artikulu, esteka eta marrazki berberak dituela; bestela, atal hori gaztelaniaz ateratzen da | ADR 0026 |
| Ez dela ezer gaztelaniaz geratu itzulpen batean | ADR 0056 |
| Ez dagoela orririk hutsune zurirekin, edozein tamainatako pantailetan | ADR 0041 |
| Funtzionatzeari utzi dioten estekak, asteazkenetan | ADR 0056 |

**Pertsona batek** zenbakia 5:00etan berrikus dezake eta aldaketak eskatu 6:50 baino lehen, baina egunkariak ez du hala egingo duenik agintzen: erantzunik ez badago, bere orduan ateratzen da (ADR 0058).

## 7. Zenbaki bakoitzetik ateratzen dena

Zenbakia ez da web-orria bakarrik. Hortik abiatuta hauek ere ateratzen dira:

- **hiru taldeetako oharrak** eta beren baliabidea agertzen zaien pertsonentzako **mezu pribatuak**;
- **Instagrameko argitalpena**, bere testuarekin;
- artikulu bakoitza **partekatzeko irudia**;
- igandean, **«Astea bideoan»** sare sozialetan.

**Zerbait aldatzen bada zenbaki batean atera baino lehen, horren mende dagoen guztia berriz egiten da**: bineta aldatzen bada, haren inguruko oharra; titular bat aldatzen bada, partekatzeko irudia; erreportajea aldatzen bada, asteko bideoa eta bere testuak.

## 8. Zuzenketak

- **Datu oker bat artikuluan bertan zuzentzen da, amaieran ohar batekin** eta bost hizkuntzetan (ADR 0055): «Corregido el…» (akats bat zegoen), «Actualización del…» (datua egia zen eta aldatu da) edo «Nota añadida el…» (zerbait falta zen). Zentzua aldatzen ez duen akats bat oharrik gabe zuzentzen da.
- Zuzendu aurretik, datua bere iturrian egiaztatzen da: akats-abisu bat ere oker egon daiteke.
- **Talde batera bidalita dagoen ohar bat zuzentzen da**, botarekin editatuta.

## 9. Pertsonak, pribatutasuna eta gardentasuna

- **Pertsona bakoitza nor den jakiteko, bere Telegram kontua begiratzen da, ez erakusten duen izena**, bi pertsonak izen bera izan dezaketelako (ADR 0066).
- **Baliabide baten egilea bakarrik izendatzen da, berak argitaratu badu**; taldeetako iritziak ez zaizkio inori egozten (estilo-liburua).
- **Irakurleengandik ez da ezer biltzen**: bisita-kontagailuak batu baino ez du egiten, cookierik eta datu pertsonalik gabe (ADR 0033), eta iruzkinak irakurleak botoia sakatzen badu bakarrik kargatzen dira (ADR 0030). [Pribatutasun-politikak](https://diarioiaeducativa.github.io/privacidad.html) azaltzen du (ADR 0070).
- **AArekin egina dagoela dioen ohar bakarra**, orri guztien oinean. [«Erredakzioa»](https://diarioiaeducativa.github.io/redaccion.html) orriak azaltzen du nola egiten den, nor den argitaratutakoaren erantzule eta ez dagoela publizitaterik ez babesik (ADR 0055 eta 0065).
- Egunkaria egiten duten programak publikoak dira (ADR 0019).

## 10. Hobetzeko dagoena

Oraindik guztiz ondo funtzionatzen ez duena edo egiaztapen bakar baten mende dagoena. Hortik hobetu daiteke egunkaria:

- **Zuzenketa ez da bakarrik iristen jada bidalitakora.** Artikulu bat argitaratu ondoren zuzentzen bada, taldeetan ateratako oharra eskuz aldatu behar da, eta Instagramen eta beste sareetan argitaratutakoa ez da aldatzen.
- **Taldeko albisterik gabeko egunetarako gordetako EduMediako artikuluak** 2026ko azaroaren 16an hasi ziren idazten: oraindik ez da bat ere atera zenbaki batean.
- **Gordetako artikulu bat argitaratu baino pixka bat lehenago berrikusten da.** Egun edo aste batzuk lehenago idazten dira, eta bat erabili baino lehen, hitz egiten duen tresnaren orria irekita jarraitzen duela bakarrik egiaztatzen da, ez kontatzen duenetik ezer aldatu den, adibidez doakoa izateari utzi dion. Horregatik, EduMediakoak, sarri aldatzen diren tresnei buruzkoak, hilabetera kentzen dira.
- **Gordetzeko artikulu bat idazten ari den bitartean**, prestatzen ari den web-orriak minutu batzuetan egunkariaren zenbaki balitz bezala erakusten du. Orduantxe web-orria argitaratuko balitz, aterako litzateke.
- **Agente batek fitxategi bat hondatzen badu, gauero prestaketan bakarrik berreskuratzen da**, ez erreportajearen, Liburutegiaren edo Biltegiaren prestaketan.
- **Itzulpenak programa batek egiaztatzen ditu**, artikulu guztiak daudela eta ez dela ezer gaztelaniaz geratu begiratzen duenak, baina ez ditu agenteren batek berrikusten.
- **Noiz jotzen den egun batek Biltegiko aplikazio berri gutxi dituela**, eta lehengo bat berreskuratzen den, begi-bistaz erabaki zen, eta doitzeko dago.
- **Instagram behin bakarrik saiatzen da**: huts egiten badu, eskuz argitaratu behar da.
