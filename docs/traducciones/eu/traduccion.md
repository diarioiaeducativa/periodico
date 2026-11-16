<!-- origen: 9cc2281a405c9371 -->
# Adimen Artifizial Hezitzailearen Egunkariaren itzultzailearen liburua

Egunkaria gaztelaniatik katalanera, galegora, euskarara eta ingelesera nola itzultzen den azaltzen du. Publikoak
irakurriko duen zerbait itzultzen duten agente guztiek irakurtzen dute, [estilo-liburuarekin](estilo.md) batera, hori
hizkuntza guztietan berdin baliatzen baita. Atal orokorra eta eskaera bakoitzeko hizkuntzaren atala irakurtzen dira.

## Hizkuntza guztientzat

- **Zentzua itzultzen da, hizkuntza bakoitzaren erregistro naturalean**, hizkuntza horretako kazetari batek
  idatziko lukeen bezala: gaztelaniaren kalkorik gabe, hitzen ordenan, preposizioetan eta esamoldeetan.
- **Eduki bera**: jatorrizkoaren artikulu, esteka, zifra, letra lodi eta etzan berberak. Ez da informaziorik
  gehitzen edo kentzen, Espainiari dagozkionen azalpena izan ezik (jarraian).
- **Izenak ez dira itzultzen**: produktuak, aplikazioak, enpresak eta hiru taldeak («Vibe Coding
  Educativo», «EduMedia-IAG»). Bineta-ko pertsonaiek, ordea, izena dute hizkuntza bakoitzean
  (`scripts/idiomas.py`).
- **Besteren ofiziala jatorrizko hizkuntzan uzten da**: lege, txosten edo gida baten izenburua.
  Espainiako erakunde bat itzultzen da hizkuntzan ohiko forma badu (ministerioa, kontseilaritza);
  hizkuntza horretan izen propioa dutenak ez (Generalitat, Xunta, Ertzaintza). Siglak
  mantentzen dira (LOMLOE, INTEF, AEPD).
- **Espainiari dagokiona azaltzen da** hizkuntza horretako irakurleak ezagutzen ez badu, batez ere
  ingelesez: hezkuntza-etapa bat, oposizioak, autonomia-erkidego bat.
- **Grafiko bat** (`grafico`) itzultzen da izenburuan, etiketetan, serieen izenetan eta oharrean; mota,
  unitatea eta balioak ez dira ukitzen, eta iturriaren izenburua jatorrizko hizkuntzan geratzen da.
- **Beste hizkuntza bateko iturriak bere marka darama** («(en castellà)», «(in Spanish)»), `scripts/idiomas.py`-k
  dioen bezala.
- **Zalantzarik izanez gero, hizkuntzaren erreferentziazko lana kontsultatzen da** (bere atalean) eta ez da
  buruz ebazten. Lan batek irakurtzen uzten ez badu, erantzun bera zerrendako beste batean bilatzen da.
- **Termino bera beti**: hizkuntza bakoitzeko AAren lexikoa behean finkatuta dago. Formak ez dira txandakatzen
  («xatbot» eta «chatbot» zenbaki berean).
- **Zuzena dena ez da zuzentzen**: forma bat arraroa iruditu arren arauak jasotzen badu, utzi egiten da.

## Katalana

**Araua**: Institut d'Estudis Catalans-en (IEC) estandarra, kazetaritza-erregistroan.

**Non kontsultatu**
- [Optimot](https://aplicacions.llengua.gencat.cat/llc/AppJava/index.html): aldi berean bilatzen du IECren
  hiztegian, zalantza-fitxetan eta TERMCATen terminologian. TERMCATera iristeko bidea da,
  haren webak ez baitie programei irakurtzen uzten.
- IECren [Diccionari de la llengua catalana (DIEC2)](https://dlc.iec.cat/), [Gramàtica (GIEC)](https://giec.iec.cat/)
  eta [Ortografia](https://oiec.iec.cat/).
- [ésAdir](https://www.esadir.cat/) eta [3Cat-en estilo-liburua](https://www.3cat.cat/llibredestil/):
  irrati eta telebista publikoen kazetaritza-estiloa.

**Formatua**
- Orduak puntuarekin: «a les 10.30».
- Ehunekoa tarteduna: «10 %», Optimotek eskatzen duen bezala.
- Milakoak puntuarekin (115.000); ordinalak «4t d'ESO», «1r de batxillerat».
- Karguak, hezkuntza-etapak eta ikasgaiak minuskulaz («primària», «batxillerat»); erakundeak,
  maiuskulaz.
- Toponimoak katalanezko forma tradizionalarekin: Saragossa, Osca, la Corunya, Biscaia.

**Hiztegia**
- «el professorat», «l'alumnat»; «soc», azentu gabe.
- AA: «intel·ligència artificial (IA)», «IA generativa», «model de llenguatge gran (LLM)», «agent d'IA»,
  «aprenentatge automàtic», «al·lucinació», «codi obert», «aplicació».
- *Prompt*: «indicació», TERMCATek normalizatutako terminoa; lehen aldian, ingelesezkoa etzanean eta
  parentesi artean: «una indicació (*prompt*)».
- *Chatbot*: «xatbot».

**Kalkorik ez**: «en base a», «a nivell de». **Zuzenak dira, ez dira aldatzen**: «degut a», «sí que», «app».

## Galegoa

**Araua**: Real Academia Galegaren (RAG) araudia, kazetaritza-erregistroan.

**Non kontsultatu**
- [Dicionario da RAG](https://academia.gal/dicionario) eta [Normas ortográficas e
  morfolóxicas](https://publicacions.academia.gal/index.php/rag/catalog/download/252/248/152?inline=1).
- [Na Universidade en galego sen dúbida](https://www.lingua.gal/documents/204205/217676/engalegosendubida.pdf?version=1.0)
  eta [Xuntaren administrazio-hizkuntzaren ikastaroa](https://www.lingua.gal/documents/204205/217796/01-CURSO-MEDIO-LINGUAXE-ADMINISTRATIVA_v2.pdf?version=1.0):
  zenbakiak, maiuskulak, toponimoak eta pronomenaren kokapena.
- [Digalego](https://digalego.xunta.gal/gl) (baliokideak dituen hiztegia), [TERGAL](http://www.cirp.gal/tergal)
  (terminologia) eta [Nomenclátor](https://toponimia.xunta.gal/gl) (Galiziako toponimoak).

**Formatua**
- Orduak puntuarekin: «ás 10.30».
- Ehunekoa tarteduna: «30 %».
- Milakoak tarteduna: «115 000».
- Karguak, egunak, hilabeteak eta etapak minuskulaz: «educación primaria», «bacharelato», «educación secundaria».
- Kataluniako eta Euskal Herriko toponimoak forma ofizialean: «Girona», «Donostia».

**Hiztegia**
- «o profesorado», «o alumnado»; zaindu generoa («o xiz») eta saihestu gaztelaniakeriak («encerado», ez
  «pizarra»; «relatorios», ez «ponencias»).
- AA: «intelixencia artificial (IA)», «IA xerativa», «modelo de linguaxe (LLM)», «axente de IA»,
  «aprendizaxe automática», «código aberto», «aplicación». Azken laurak ez daude RAGen hiztegian
  zentzu horrekin: egunkariak horrela erabiltzen ditu.
- *Prompt*, etzanean, eta lehen aldian «instrución» gisa azalduta, Xuntak egiten duen bezala.

**Maiz huts egiten den gramatika**
- Pronomena aditzaren aurretik doa adberbio batek edo ezeztapen batek etenik gabe aurretik dutenean: «só se
  equivoca», ez «só equivócase».
- «Ambos»-ek artikulua eramaten du izenaren aurretik: «ambos os modelos».

## Euskara

**Araua**: Euskaltzaindiaren euskara batua, kazetaritza-erregistroan.

**Non kontsultatu**
- [Euskaltzaindiaren arauak](https://www.euskaltzaindia.eus/index.php?option=com_euskaltzaindiarenarauak&view=frontpage&Itemid=1723&lang=eu)
  (bakoitza PDF formatuan) eta haren hiztegia.
- [Euskalterm](https://www.euskadi.eus/euskalterm/) (terminologia), [Elhuyar](https://hiztegiak.elhuyar.eus/)
  eta [Labayru](https://hiztegia.labayru.eus/) (hiztegiak).
- [Berriaren estilo-liburua](https://www.berria.eus/estiloliburua/): kazetaritza-estiloa.
- UPV/EHUren [Kalkoen Behatokia](https://www.ehu.eus/ehg/kalkoak/): gaztelaniaren kalkoak.

**Formatua** (Euskaltzaindiaren 203. araua)
- Orduak: «10:30ean». Datak: «2026ko azaroaren 13an».
- Ehunekoa, zeinua aurretik eta tartearekin: «% 35».
- Milakoak tarteduna: «115 000».
- Karguak minuskulaz; erakundeak eta hezkuntza-etapak maiuskulaz («Lehen Hezkuntza», «Batxilergoa»),
  200. arauak agintzen duen bezala.
- Siglak eta izenak gidoirik gabe deklinatzen dira: «AAren», «ElevenLabsen».
- Toponimoak: 32. araua (Espainia), 151. araua (eskualdeak) eta 38. araua (herrialdeak).

**Hiztegia**
- «irakasleak», «ikasleak»; egunkaria «egunkaria» da, inoiz ez «diarioa»; hezkuntza-zentro bat
  «ikastetxea» da, ez «zentroa».
- AA: «adimen artifiziala (AA)», «AA sortzailea», «ikaste automatikoa», «kode irekia», «aplikazioa»,
  «txatbota». Hizkuntza-ereduak eta AA agenteak ez dute termino normalizaturik: egunkariak
  «hizkuntza-eredua» eta «AA agentea» erabiltzen ditu.
- *Prompt*, etzanean, itzuli gabe: ez du termino normalizaturik.

**Kalkorik ez**: beharrezkoa ez den «bere» (Kalkoen Behatokia).

## Ingelesa

**Araua**: Britainia Handiko ingelesa, kazetaritza-erregistroan. Egunkaria «the paper» da, inoiz ez «the diary».

**Non kontsultatu**
- [The Guardianen estilo-gida](https://www.theguardian.com/guardian-observer-style-guide-a) (letra
  bakoitza bere orrian) eta [BBCrena](https://www.bbc.co.uk/newsstyleguide/all).
- [Europako Batzordearen ingelesezko itzulpenerako estilo-gida](https://knowledge-centre-translation-interpretation.ec.europa.eu/en/resources-translating-eu-documents/guidelines-translating-eu-documents-english),
  *Country Compendium*-ekin: Espainiako erakundeak eta toponimoak.
- [IATE](https://iate.europa.eu) (EBren terminologia) eta [Oxford Learner's Dictionary](https://www.oxfordlearnersdictionaries.com).

**Formatua**
- Datak: «13 November 2026». Orduak: «10.30am», The Guardianek bezala.
- Ehunekoa zifrari itsatsita: «35%». Milakoak komarekin: «115,000».
- Ingeles komatxoak (“ ”), inoiz ez gaztelaniazkoak; -ise ortografia («organise»).
- Kargu, etapa eta erakunde generikoak minuskulaz («the education ministry», «secondary education»).
- Toponimoak: A Coruña, Lleida, Catalonia, the Basque Country.

**Hiztegia**
- «teachers», «students» edo «pupils».
- AA: «AI», «generative AI», «large language model (LLM)», «AI agent», «machine learning»,
  «hallucination», «open-source» (izenaren aurrean gidoiarekin), «app».
- Jatorrizkoan ingelesez esan zena iturritik kopiatzen da, ez da berriz itzultzen.

**Espainiari dagokiona**
- Erakunde bat, ingelesezko izen deskribatzailearekin eta jatorrizko siglarekin: «the Spanish education
  ministry», «Spain's education law (LOMLOE)»; inoiz ez asmatutako ingeles sigla bat.
- «autonomous community» (autonomia-erkidegoa), «regional education ministry» (kontseilaritza),
  «competitive civil service exam» (oposizioak), «vocational training» (LH).
- **Inoiz ez «Year 10» ezta britainiar sistemako beste baliokiderik**: ikasturteak ez datoz bat. Espainiako
  izena eta adina: «the fourth year of ESO (students aged 15 to 16)», «Bachillerato (the final two
  years of secondary school, ages 16 to 18)».
