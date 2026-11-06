#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Genera la web del «Diario de IA Educativa» a partir de las ediciones, en castellano
(raíz del sitio) y en catalán (carpeta ca/). Sin dependencias: solo la biblioteca estándar.

La portada reúne lo de los últimos días (un día suelto da para pocas piezas); cada
día queda además en su propia página, como archivo."""
import datetime
import hashlib
import html
import json
import pathlib
import re
import os
import shutil
import urllib.parse
from email.utils import format_datetime
from zoneinfo import ZoneInfo

import vineta

RAIZ = pathlib.Path(__file__).resolve().parent
SITIO = RAIZ / "sitio"
NOMBRE = "Diario de IA Educativa"     # en castellano; cada idioma lleva el suyo en IDIOMAS
DIAS_PORTADA = 7        # la portada reúne lo de esta última semana…
MAX_PIEZAS = 10         # …hasta este número de piezas
MAX_BREVES = 3
MAQUETA = "diario"
# Dirección pública del sitio, para los enlaces absolutos del RSS y de la vista previa al compartir
BASE = os.environ.get("PERIODICO_BASE", "https://diarioiaeducativa.github.io/")
ORDEN_SECCIONES = ["herramientas", "vibecoding", "multimedia", "debates", "novedades", "biblioteca"]
BIBLIOTECA_PORTADA = 3   # artículos de la Biblioteca en la portada, aparte de MAX_PIEZAS (ADR 0006)
TEMA_BIBLIOTECA = "https://t.me/ChatGPTedu/21753"
REPOSITORIO = "https://vibe-coding-educativo.github.io/app_edu/"   # el Repositorio de recursos de VCE (ADR 0008)
CODIGO = "https://github.com/diarioiaeducativa/periodico"   # el código de la redacción, público (ADR 0019)
VCER = ("recomendable", 100, "2026-11")   # la última evaluación VCER: resultado, porcentaje y mes (ADR 0020, evaluacion-vcer.md)
# Primer día del número 1: los días anteriores (la prueba) salen en portada y archivo, sin número
LANZAMIENTO = "2026-11-01"

GRUPOS = {
    "chatgpt": ("ChatGPT-IA-edu", "ChatGPTedu"),
    "vce": ("Vibe Coding Educativo", "vceduca"),
    "edumedia": ("EduMedia-IAG", "EduMediaIAG"),
}

# Idiomas: castellano en la raíz y catalán en ca/. El contenido traducido vive en
# ediciones-ca/, ilustraciones-ca/ y vinetas-ca/; si falta algo, se usa el original.
IDIOMAS = {
    "es": {
        "carpeta": "", "sufijo": "", "nombre": "Castellano", "titulo": "Diario de IA Educativa",
        "edicion": "Edición en castellano",
        "lema": "La inteligencia artificial, contada desde tres comunidades docentes",
        "dias": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
        "meses": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                  "septiembre", "octubre", "noviembre", "diciembre"],
        "secciones": {"herramientas": "Herramientas", "vibecoding": "Vibe coding", "multimedia": "Multimedia",
                      "debates": "Debates", "novedades": "Novedades oficiales", "biblioteca": "Biblioteca"},
        "actualizado": "Actualizado el", "num": "Núm.", "numero_largo": "Número",
        "tema": "Cambiar entre tema claro y oscuro", "navegacion": "Navegación",
        "quees": "La redacción", "portada": "Portada", "volver": "Volver a la portada",
        "dia_ant": "Día anterior", "dia_sig": "Día siguiente",
        "leer_conv": "Lee la conversación original en", "tema_en": "Tema tratado en",
        "comprobado": "Comprobado en", "fuente": "Fuente", "conversacion": "Conversación",
        "breves": "Breves", "breves_antes": "Breves anteriores", "vineta": "La viñeta", "vineta_titulo": "La viñeta de Tiza y Algoritmo", "y": "y",
        "a_partir": "A partir de",
        "a_partir_dia": "A partir de las noticias del día.",
        "unete": "Únete a la conversación",
        "grupos_desc": {"chatgpt": "uso general de la inteligencia artificial en educación: experiencias, herramientas y recursos.",
                        "vce": "creación de recursos digitales educativos usando el lenguaje natural.",
                        "edumedia": "creación de audio, vídeo e imagen con IA generativa para el aula."},
        "unete_txt": "El Diario de IA Educativa cuenta lo que se habla en tres grupos abiertos de Telegram donde docentes comparten lo que prueban con la inteligencia artificial. Las conversaciones se pueden leer sin entrar; para participar, basta con unirse.",
        "archivo": "Archivo por días",
        "anyo": "Año", "hemeroteca": "Hemeroteca", "hemeroteca_txt": "Todos los números, por meses.",
        "todos_numeros": "Hemeroteca: todos los números",
        "compartir": "Compartir", "copiado": "Enlace copiado", "compartir_breve": "Compartir este breve", "mas_en": "Más en", "mas_diario": "Más en el diario",
        "no_existe": "Esta página no existe",
        "no_existe_txt": "Puede que el enlace esté mal escrito o que la pieza se haya retirado. La portada de hoy y la hemeroteca siguen ahí.",
        "redactado": "Redactado con IA a partir de las conversaciones de los grupos. Cada dato se comprueba en su fuente original, enlazada al final de cada pieza; las opiniones de los miembros no se atribuyen a nadie.",
        "licencia": "Textos e ilustraciones con licencia", "deed": "deed.es", "reserva_aviso": "Hoy no han podido salir las noticias de los grupos de ayer por un fallo de la redacción del diario. Salen mañana, junto con las de hoy; mientras tanto, un recurso del fondo del repositorio.", "vcer": "Evaluación VCER: Recomendable (100 %), noviembre de 2026", "codigo_enlace": "el repositorio de la redacción",
        "letra": "Letra", "iconos": "Iconos", "traduccion": "",
        "idioma": "Idioma", "secciones_nav": "Secciones", "rss": "RSS",
        "nombre_corto": "Diario IA", "instalar": "Instalar la app",
        "instalar_titulo": "Instala el diario en este dispositivo y ábrelo desde su icono, como una app",
        "instalar_ios": "En el iPhone o el iPad, el diario se puede tener como una app: añádelo a la pantalla de inicio desde el botón de compartir del navegador.",
        "sin_piezas": "Todavía no hay piezas en esta sección.",
        "leer_presentacion": "Leer la presentación", "presentacion": "Cómo se hace este diario: la presentación del número 1",
        "sin_vinetas": "Todavía no hay viñetas.",
        "descripciones": {
            "herramientas": "Asistentes, servicios y modelos de inteligencia artificial de los que se habla en los grupos, explicados desde su uso docente: qué ofrecen, en qué condiciones y para qué puede servir cada uno en clase.",
            "vibecoding": "Aplicaciones que el profesorado crea describiéndolas a una inteligencia artificial, sin necesidad de saber programar, y lo que se aprende en los grupos para hacerlas: instrucciones para generar recursos, agentes de programación y soluciones a problemas habituales. Cada aplicación se presenta con el nombre de su autor o autora, y las que entran en el {repositorio} de Vibe Coding Educativo tienen aquí su artículo.",
            "multimedia": "Audio, vídeo e imagen con inteligencia artificial generativa: las herramientas para crear voces, ilustraciones y vídeos, y los flujos de trabajo que comparten los grupos para producir material educativo.",
            "debates": "Lo que se discute con argumentos en los grupos, como la evaluación, la autoría, la privacidad o la relación con las familias. Las posturas se exponen sin atribuirlas a nadie y, cuando hay argumentos serios en los dos sentidos, se recogen los dos.",
            "novedades": "Lo que publican las administraciones, los organismos y las empresas sobre la inteligencia artificial en educación, como normas, guías, marcos y anuncios, cuando se comenta en los grupos. Cada pieza enlaza al documento original.",
            "biblioteca": "Un artículo por cada documento que entra en la {enlace} de ChatGPT-IA-edu, la colección de guías, informes y estudios sobre inteligencia artificial y educación que reúnen sus miembros. Cada artículo explica quién publica el documento, qué propone y cómo encaja con los demás, y enlaza a su fuente oficial.",
            "reportajes": "Cada domingo, un tema de la semana tratado a fondo: lo que se habló en los grupos, lo que dicen las empresas, las administraciones y los organismos implicados, el marco en España y lo que puede hacer un docente.",
            "breves": "Las noticias que se cuentan en una o dos frases: temas de los grupos que no dan para una pieza entera. Cada breve lleva el enlace a su fuente y a la conversación donde salió, y se puede compartir por separado.",
            "vineta": "Cada día, Tiza y Algoritmo comentan con humor una noticia del número.",
            "videos": "Vídeos cortos del diario y de sus comunidades. Cada domingo, «La semana en vídeo» repasa la semana día a día, con lo más destacado de cada número. Los hace un programa con los textos y los dibujos del diario; son sin voz, con música compuesta también por programa, distinta en cada vídeo.",
        },
        "videos": "Vídeos", "semana_video": "La semana en vídeo", "en_pantalla": "Lo que aparece en pantalla",
        "en_instagram": "Verlo en Instagram", "instagram": "Instagram", "sin_videos": "Todavía no hay vídeos.",
        "video_idioma": "Vídeo en castellano.", "video_enlace": "Enlace a este vídeo",
        "todos_videos": "Todos los vídeos",
        "biblioteca_enlace": "Biblioteca digital", "el_documento": "El documento", "doc_titulo": "Título", "doc_autoria": "Autoría",
        "doc_anyo": "Año", "doc_idioma": "Idioma", "doc_licencia": "Licencia", "doc_leer": "Leer el documento en su fuente oficial",
        "en_biblioteca": "Ver el documento en la Biblioteca digital de ChatGPT-IA-edu",
        "repositorio_enlace": "Repositorio de recursos", "el_recurso": "El recurso", "rec_titulo": "Nombre", "rec_autoria": "Autoría",
        "rec_licencia": "Licencia", "rec_abrir": "Abrir el recurso", "rec_ficha": "Su ficha en el repositorio",
        "en_repositorio": "Ver el Repositorio de recursos de Vibe Coding Educativo", "ampliar": "Ampliar la imagen", "cerrar": "Cerrar",
        "buscar": "Buscar", "buscar_etiqueta": "Buscar en el diario", "buscar_campo": "Escribe lo que buscas",
        "buscar_txt": "Busca en todo lo publicado en el diario: piezas, breves, artículos de la Biblioteca y reportajes, en castellano. Encuentra también las formas de una misma palabra: «evaluar» encuentra «evaluación».",
        "resultados_1": "1 resultado", "resultados_n": "{n} resultados", "sin_resultados": "No hay nada publicado con esas palabras.",
        "todas": "Todas", "mas_resultados": "Más resultados", "buscando": "Buscando…", "sin_buscador": "El buscador no ha podido cargarse.",
        "reportaje": "El reportaje del domingo", "reportajes": "Reportajes", "leer_reportaje": "Leer el reportaje",
        "claves": "Claves", "en_el_diario": "En el diario esta semana", "sin_reportajes": "Todavía no hay reportajes.",
        "reportajes_txt": "Cada domingo, un tema de la semana tratado a fondo.", "palabras": "minutos de lectura",
        "redaccion": {
            "intro": "El Diario de IA Educativa lo escribe una redacción de agentes de inteligencia artificial, cada uno con su oficio, que se revisan entre ellos. Lo idean, lo diseñan y lo supervisan personas, y sale cada mañana a las 7:00, en castellano y en catalán.",
            "proceso_titulo": "Cómo se hace cada número",
            "proceso_intro": "Cada número cuenta lo que se habló el día anterior en los tres grupos. La redacción trabaja de madrugada, con el día ya cerrado, y sigue siempre el mismo orden.",
            "proceso": [
                "A la 1:00, un programa recoge los mensajes del día en los tres grupos y los ordena por grupo y por tema. En este paso no interviene la inteligencia artificial.",
                "El redactor elige los temas que pueden interesar fuera de los grupos y escribe las piezas, comprobando cada dato en su fuente original. Después, el revisor vuelve a abrir cada fuente y quita lo que no puede confirmar.",
                "El ilustrador dibuja cada pieza mientras el guionista escribe cinco guiones para la viñeta. Un programa abre cada dibujo en su página, en tema claro y oscuro, y mide sus colores, su contraste y sus rótulos; después, el revisor de dibujos mira el resultado y devuelve al ilustrador lo que no se ve bien. El juez de humor elige el mejor guion, o ninguno, y un programa dibuja la viñeta.",
                "Si ese día ha entrado algún documento en la {biblioteca} de ChatGPT-IA-edu, el documentalista escribe su artículo y el revisor lo contrasta con el documento. Si el número se queda corto, con menos de cuatro piezas, el documentalista escribe además sobre recursos del {repositorio} de Vibe Coding Educativo, y el sábado repasa los que han entrado en la semana. La noche del sábado se preparan, además, el reportaje y «La semana en vídeo» del domingo.",
                "El traductor prepara la edición en catalán, y el portavoz escribe el mensaje que recibirá cada grupo.",
                "Un programa monta la web con todo lo anterior y la publica a las 6:55. A las 7:00, el bot de los grupos publica el aviso en cada uno de ellos.",
            ],
            "proceso_pie": "Cuando un paso falla o una revisión no da algo por bueno, esa parte se queda fuera y el número sale igual. No hay ningún día sin número: si falla la redacción entera, sale con un artículo de reserva, escrito y revisado otro día, y las noticias de los grupos de ese día salen al siguiente; si el servidor de la redacción no ha publicado a las 9:10, un vigilante que funciona fuera de él saca el número con esa reserva. La persona que supervisa la redacción recibe un aviso en cada caso.",
            "equipo_titulo": "El equipo",
            "organigrama_alt": "Organigrama de la redacción, en el que los agentes de IA van en cajas rellenas y los mensajes y lo publicado, solo con contorno: cada día, los mensajes de los grupos pasan del redactor al revisor, y los documentos de la Biblioteca digital y los recursos del repositorio, del documentalista al revisor. Del revisor salen dos caminos: el guionista y el juez de humor preparan la viñeta, y el ilustrador dibuja lo que explica cada noticia, con el revisor de dibujos, que le devuelve lo que no se ve bien. Todo acaba en el traductor, y el número sale a las 7:00 con un aviso del portavoz para cada grupo. Los domingos, el jefe de reportajes, el reportero y el verificador preparan el reportaje, que pasa también por el ilustrador, el revisor de dibujos y el traductor y sale dentro del número. Además, el guionista de vídeo escribe «La semana en vídeo» con los números de la semana, y el vídeo sale también en el número del domingo.",
            "equipo": [
                ("Redactor", "lee las conversaciones del día de los tres grupos, elige lo que puede interesar a las personas que no están en ellos y escribe las piezas, comprobando cada dato en su fuente original."),
                ("Revisor", "no ha escrito nada: vuelve a abrir cada fuente, compara las piezas con los mensajes y quita lo que no puede confirmar. Hace lo mismo con los artículos de la Biblioteca, contra el propio documento."),
                ("Documentalista", "cuando entra un documento en la Biblioteca digital de ChatGPT-IA-edu, lo lee en su fuente oficial y escribe un artículo sobre él. También escribe sobre los recursos del Repositorio de Vibe Coding Educativo, a partir del propio recurso y de una captura que hace un programa al abrirlo."),
                ("Ilustrador", "dibuja lo que explica cada noticia y, los domingos, la infografía del reportaje."),
                ("Revisor de dibujos", "mira cada dibujo en su página, en tema claro y oscuro, y se lo devuelve al ilustrador si algo no se ve bien o no explica la noticia. Antes, un programa mide lo que se puede medir: colores, contraste y rótulos que se salen o se pisan."),
                ("Guionista", "escribe cinco guiones de la viñeta con Tiza y Algoritmo, sus dos personajes."),
                ("Juez de humor", "elige el mejor, sin haberlos escrito, o ninguno si no tiene gracia."),
                ("Traductor", "prepara la edición en catalán, el Diari d'IA Educativa."),
                ("Portavoz", "escribe cada mañana el aviso con el que el diario se presenta en cada grupo, distinto para cada uno."),
                ("Jefe de reportajes", "los domingos elige el tema de la semana que merece un reportaje, su enfoque y a quién hay que consultar."),
                ("Reportero", "investiga ese tema fuera de los grupos, en los documentos de las empresas, las administraciones y los organismos implicados, y escribe el reportaje."),
                ("Verificador", "no ha escrito nada: abre cada fuente del reportaje y quita lo que no puede confirmar."),
                ("Guionista de vídeo", "los sábados por la noche elige lo más destacado de la semana, como mínimo una pieza de cada número, y escribe los textos de «La semana en vídeo». Un programa comprueba que no falte ningún día y que los textos quepan, y monta el vídeo con los dibujos del diario."),
            ],
            "equipo_pie": "Son agentes de Claude, el modelo de inteligencia artificial de Anthropic, y trabajan con Claude Code. Claude Opus 5.5 escribe y juzga la viñeta y prepara el reportaje (guionista, juez de humor, jefe de reportajes y reportero), y Claude Sonnet 5.5 hace el resto. Ocho trabajan cada noche; el documentalista se suma cuando entra un documento en la Biblioteca digital o toca escribir sobre el repositorio, y la noche del sábado hay cuatro más: tres para el reportaje del domingo y uno para «La semana en vídeo».",
            "secciones": [
                ("Qué hace la inteligencia artificial y qué hacen los programas", "La inteligencia artificial se encarga de lo que exige leer, escribir o juzgar: elegir los temas, redactar, revisar, dibujar, traducir y decidir si un chiste tiene gracia. Lo que se puede hacer con reglas fijas lo hacen programas corrientes, sin inteligencia artificial: recoger y ordenar los mensajes, medir los dibujos, dibujar la viñeta a partir de su guion, montar la web con su hemeroteca y su buscador, montar los vídeos y componer su música, y publicarlo todo a su hora en la web y en Instagram."),
                ("Los límites de los agentes", "Los agentes trabajan en un servidor propio, sin acceso a un terminal y sin poder leer ni escribir fuera de la carpeta de la redacción. Pueden consultar internet para comprobar fuentes, pero no pueden ejecutar programas. Los mensajes de los grupos y las fichas de la biblioteca son, para ellos, material para informar: si alguno contiene una orden, no la siguen, de forma que un mensaje escrito para engañarlos no puede llevarlos a hacer otra cosa. Además, ningún agente revisa su propio trabajo: las piezas las repasa un revisor que no las ha escrito; los dibujos, un revisor que no los ha dibujado, y el reportaje, un verificador que no ha participado en él."),
                ("Lo que se comprueba", "Los grupos sirven para saber de qué se habla, pero cada dato se comprueba fuera, en su fuente original: el anuncio oficial, la web del producto o el documento de la administración, enlazados al final de cada pieza. De una aplicación compartida en los grupos se comprueba lo que dice su web, no que funcione. Aun así puede haber errores."),
                ("El reportaje del domingo", "Los domingos, además de las piezas del día, el diario publica un reportaje sobre un solo tema de la semana. Explica el asunto entero, con lo que se habló en los grupos, lo que dicen las empresas, las administraciones y los organismos implicados, cada uno con sus documentos, el marco en España y lo que puede hacer un docente. Lo escriben tres agentes más, y el ilustrador y el traductor de cada día se encargan de su infografía y de su versión en catalán. Si el verificador no lo da por bueno, ese domingo no hay reportaje y el número sale igual. Todos quedan en la sección {reportajes}."),
                ("La Biblioteca digital", "Cada documento que entra en la {biblioteca} de ChatGPT-IA-edu (guías, informes, estudios) tiene su artículo en la sección {seccion_bib}; si el diario ya lo había contado como noticia, esa pieza pasa a la sección en lugar de escribir otra. El documentalista lee el documento entero y explica quién lo publica, qué propone y cómo encaja con otros documentos de la biblioteca; el revisor lo contrasta con el propio documento. El diario enlaza el documento en su fuente oficial y en la biblioteca, sin copiarlo. Se nombra a sus autores; la persona que lo ha compartido no se nombra, igual que no se atribuyen las opiniones de los grupos."),
                ("El Repositorio de recursos", "El {repositorio} de Vibe Coding Educativo reúne las aplicaciones y recursos que crean y comparten con licencia abierta los docentes de esa comunidad. Los días con menos de cuatro piezas, el documentalista escribe sobre los que han entrado y el diario aún no ha contado, y el número del sábado repasa los de la semana; si no hay ninguno nuevo, rescata uno anterior. Un programa abre cada recurso y guarda una captura de lo que se ve; el documentalista lo describe a partir de la captura y de su página, y el revisor lo vuelve a abrir. Salen en la sección {seccion_vc}, con el nombre de quien lo ha hecho y su licencia."),
                ("Las personas", "La idea del diario es de {raul}, administrador de {edumedia}. La redacción la diseñó y la supervisa {juanjo}."),
                ("El código", "Los programas que preparan y montan el diario y el encargo de cada agente son públicos, en {codigo}, con licencia AGPL v3, y cada decisión está explicada en sus registros de decisiones (ADR). Los mensajes de los grupos no están en él."),
                ("Las comunidades", "{chatgpt}, sobre inteligencia artificial en educación; {vce}, de docentes que programan sus propias aplicaciones con IA, y {edumedia}, sobre IA generativa para crear audio, vídeo e imagen. Las tres son abiertas: cada pieza enlaza a la conversación donde nació, que se puede leer sin entrar."),
                ("Si participas en los grupos", "Las opiniones no se atribuyen a nadie: solo se nombra a la persona que ha publicado un recurso propio. Si aparece algo tuyo y prefieres que no salga, o ves un error, díselo a las personas que administran tu grupo y se retirará o se corregirá."),
            ],
        },
    },
    "ca": {
        "carpeta": "ca/", "sufijo": "-ca", "nombre": "Català", "titulo": "Diari d'IA Educativa",
        "edicion": "Edició en català",
        "lema": "La intel·ligència artificial, explicada des de tres comunitats docents",
        "dias": ["dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte", "diumenge"],
        "meses": ["gener", "febrer", "març", "abril", "maig", "juny", "juliol", "agost",
                  "setembre", "octubre", "novembre", "desembre"],
        "secciones": {"herramientas": "Eines", "vibecoding": "Vibe coding", "multimedia": "Multimèdia",
                      "debates": "Debats", "novedades": "Novetats oficials", "biblioteca": "Biblioteca"},
        "actualizado": "Actualitzat el", "num": "Núm.", "numero_largo": "Número",
        "tema": "Canviar entre tema clar i fosc", "navegacion": "Navegació",
        "quees": "La redacció", "portada": "Portada", "volver": "Torna a la portada",
        "dia_ant": "Dia anterior", "dia_sig": "Dia següent",
        "leer_conv": "Llegeix la conversa original a", "tema_en": "Tema tractat a",
        "comprobado": "Comprovat a", "fuente": "Font", "conversacion": "Conversa",
        "breves": "Breus", "breves_antes": "Breus anteriors", "vineta": "La vinyeta", "vineta_titulo": "La vinyeta de Guix i Algorisme", "y": "i",
        "a_partir": "A partir de",
        "a_partir_dia": "A partir de les notícies del dia.",
        "unete": "Uneix-te a la conversa",
        "grupos_desc": {"chatgpt": "ús general de la intel·ligència artificial a l'educació: experiències, eines i recursos.",
                        "vce": "creació de recursos digitals educatius fent servir el llenguatge natural.",
                        "edumedia": "creació d'àudio, vídeo i imatge amb IA generativa per a l'aula."},
        "unete_txt": "El Diari d'IA Educativa explica el que es parla en tres grups oberts de Telegram on docents comparteixen el que proven amb la intel·ligència artificial. Les converses es poden llegir sense entrar-hi; per participar-hi, n'hi ha prou d'unir-s'hi.",
        "archivo": "Arxiu per dies",
        "anyo": "Any", "hemeroteca": "Hemeroteca", "hemeroteca_txt": "Tots els números, per mesos.",
        "todos_numeros": "Hemeroteca: tots els números",
        "compartir": "Comparteix", "copiado": "Enllaç copiat", "compartir_breve": "Comparteix aquest breu", "mas_en": "Més a", "mas_diario": "Més al diari",
        "no_existe": "Aquesta pàgina no existeix",
        "no_existe_txt": "Pot ser que l'enllaç estigui mal escrit o que la peça s'hagi retirat. La portada d'avui i l'hemeroteca continuen aquí.",
        "redactado": "Redactat amb IA a partir de les converses dels grups. Cada dada es comprova a la seva font original, enllaçada al final de cada peça; les opinions dels membres no s'atribueixen a ningú.",
        "licencia": "Textos i il·lustracions amb llicència", "deed": "deed.ca", "reserva_aviso": "Avui no han pogut sortir les notícies dels grups d'ahir per una fallada de la redacció del diari. Surten demà, juntament amb les d'avui; mentrestant, un recurs del fons del repositori.", "vcer": "Avaluació VCER: Recomanable (100 %), novembre de 2026", "codigo_enlace": "repositori de la redacció",
        "letra": "Lletra", "iconos": "Icones",
        "traduccion": "Traducció automàtica amb IA de l'edició en castellà (Diario de IA Educativa), sense revisió professional.",
        "idioma": "Idioma", "secciones_nav": "Seccions", "rss": "RSS",
        "nombre_corto": "Diari IA", "instalar": "Instal·la l'app",
        "instalar_titulo": "Instal·la el diari en aquest dispositiu i obre'l des de la seva icona, com una app",
        "instalar_ios": "A l'iPhone o l'iPad, el diari es pot tenir com una app: afegeix-lo a la pantalla d'inici des del botó de compartir del navegador.",
        "sin_piezas": "Encara no hi ha peces en aquesta secció.",
        "leer_presentacion": "Llegeix la presentació", "presentacion": "Com es fa aquest diari: la presentació del número 1",
        "sin_vinetas": "Encara no hi ha vinyetes.",
        "descripciones": {
            "herramientas": "Assistents, serveis i models d'intel·ligència artificial dels quals es parla als grups, explicats des del seu ús docent: què ofereixen, en quines condicions i per a què pot servir cadascun a classe.",
            "vibecoding": "Aplicacions que el professorat crea descrivint-les a una intel·ligència artificial, sense necessitat de saber programar, i el que s'aprèn als grups per fer-les: instruccions per generar recursos, agents de programació i solucions a problemes habituals. Cada aplicació es presenta amb el nom del seu autor o autora, i les que entren al {repositorio} de Vibe Coding Educativo hi tenen el seu article.",
            "multimedia": "Àudio, vídeo i imatge amb intel·ligència artificial generativa: les eines per crear veus, il·lustracions i vídeos, i els fluxos de treball que comparteixen els grups per produir material educatiu.",
            "debates": "El que es discuteix amb arguments als grups, com l'avaluació, l'autoria, la privacitat o la relació amb les famílies. Les postures s'exposen sense atribuir-les a ningú i, quan hi ha arguments seriosos en tots dos sentits, es recullen tots dos.",
            "novedades": "El que publiquen les administracions, els organismes i les empreses sobre la intel·ligència artificial en educació, com normes, guies, marcs i anuncis, quan es comenta als grups. Cada peça enllaça al document original.",
            "biblioteca": "Un article per cada document que entra a la {enlace} de ChatGPT-IA-edu, la col·lecció de guies, informes i estudis sobre intel·ligència artificial i educació que reuneixen els seus membres. Cada article explica qui publica el document, què proposa i com encaixa amb els altres, i enllaça a la font oficial.",
            "reportajes": "Cada diumenge, un tema de la setmana tractat a fons: el que es va parlar als grups, el que diuen les empreses, les administracions i els organismes implicats, el marc a Espanya i el que pot fer un docent.",
            "breves": "Les notícies que s'expliquen en una o dues frases: temes dels grups que no donen per a una peça sencera. Cada breu porta l'enllaç a la font i a la conversa on va sortir, i es pot compartir per separat.",
            "vineta": "Cada dia, Guix i Algorisme comenten amb humor una notícia del número.",
            "videos": "Vídeos curts del diari i de les seves comunitats. Cada diumenge, «La setmana en vídeo» repassa la setmana dia a dia, amb el més destacat de cada número. Els fa un programa amb els textos i els dibuixos del diari; són sense veu, amb música composta també per programa, diferent en cada vídeo.",
        },
        "videos": "Vídeos", "semana_video": "La setmana en vídeo", "en_pantalla": "El que apareix a la pantalla",
        "en_instagram": "Mira'l a Instagram", "instagram": "Instagram", "sin_videos": "Encara no hi ha vídeos.",
        "video_idioma": "Vídeo en castellà.", "video_enlace": "Enllaç a aquest vídeo",
        "todos_videos": "Tots els vídeos",
        "biblioteca_enlace": "Biblioteca digital", "el_documento": "El document", "doc_titulo": "Títol", "doc_autoria": "Autoria",
        "doc_anyo": "Any", "doc_idioma": "Idioma", "doc_licencia": "Llicència", "doc_leer": "Llegeix el document a la font oficial",
        "en_biblioteca": "Mira el document a la Biblioteca digital de ChatGPT-IA-edu",
        "repositorio_enlace": "Repositori de recursos", "el_recurso": "El recurs", "rec_titulo": "Nom", "rec_autoria": "Autoria",
        "rec_licencia": "Llicència", "rec_abrir": "Obre el recurs", "rec_ficha": "La seva fitxa al repositori",
        "en_repositorio": "Mira el Repositori de recursos de Vibe Coding Educativo", "ampliar": "Amplia la imatge", "cerrar": "Tanca",
        "buscar": "Cerca", "buscar_etiqueta": "Cerca al diari", "buscar_campo": "Escriu el que cerques",
        "buscar_txt": "Cerca en tot el que s'ha publicat al diari: peces, breus, articles de la Biblioteca i reportatges, en català. Troba també les formes d'una mateixa paraula: «avaluar» troba «avaluació».",
        "resultados_1": "1 resultat", "resultados_n": "{n} resultats", "sin_resultados": "No hi ha res publicat amb aquestes paraules.",
        "todas": "Totes", "mas_resultados": "Més resultats", "buscando": "Cercant…", "sin_buscador": "El cercador no s'ha pogut carregar.",
        "reportaje": "El reportatge del diumenge", "reportajes": "Reportatges", "leer_reportaje": "Llegeix el reportatge",
        "claves": "Claus", "en_el_diario": "Al diari aquesta setmana", "sin_reportajes": "Encara no hi ha reportatges.",
        "reportajes_txt": "Cada diumenge, un tema de la setmana tractat a fons.", "palabras": "minuts de lectura",
        "redaccion": {
            "intro": "El Diari d'IA Educativa l'escriu una redacció d'agents d'intel·ligència artificial, cadascun amb el seu ofici, que es revisen entre ells. L'ideen, el dissenyen i el supervisen persones, i surt cada matí a les 7.00, en castellà i en català.",
            "proceso_titulo": "Com es fa cada número",
            "proceso_intro": "Cada número explica el que es va parlar el dia anterior als tres grups. La redacció treballa de matinada, amb el dia ja tancat, i segueix sempre el mateix ordre.",
            "proceso": [
                "A la 1.00, un programa recull els missatges del dia dels tres grups i els ordena per grup i per tema. En aquest pas no hi intervé la intel·ligència artificial.",
                "El redactor tria els temes que poden interessar fora dels grups i escriu les peces, comprovant cada dada a la seva font original. Després, el revisor torna a obrir cada font i treu el que no pot confirmar.",
                "L'il·lustrador dibuixa cada peça mentre el guionista escriu cinc guions per a la vinyeta. Un programa obre cada dibuix a la seva pàgina, en tema clar i fosc, i en mesura els colors, el contrast i els rètols; després, el revisor de dibuixos mira el resultat i torna a l'il·lustrador el que no es veu bé. El jutge d'humor tria el millor guió, o cap, i un programa dibuixa la vinyeta.",
                "Si aquell dia ha entrat algun document a la {biblioteca} de ChatGPT-IA-edu, el documentalista n'escriu l'article i el revisor el contrasta amb el document. Si el número es queda curt, amb menys de quatre peces, el documentalista escriu a més sobre recursos del {repositorio} de Vibe Coding Educativo, i el dissabte repassa els que hi han entrat durant la setmana. La nit del dissabte es preparen, a més, el reportatge i «La setmana en vídeo» del diumenge.",
                "El traductor prepara l'edició en català, i el portaveu escriu el missatge que rebrà cada grup.",
                "Un programa munta el web amb tot l'anterior i el publica a les 6.55. A les 7.00, el bot dels grups publica l'avís a cadascun.",
            ],
            "proceso_pie": "Quan un pas falla o una revisió no dona alguna cosa per bona, aquella part es queda fora i el número surt igualment. No hi ha cap dia sense número: si falla la redacció sencera, surt amb un article de reserva, escrit i revisat un altre dia, i les notícies dels grups d'aquell dia surten l'endemà; si el servidor de la redacció no ha publicat a les 9.10, un vigilant que funciona fora d'ell treu el número amb aquesta reserva. La persona que supervisa la redacció rep un avís en cada cas.",
            "equipo_titulo": "L'equip",
            "organigrama_alt": "Organigrama de la redacció, en què els agents d'IA van en caixes plenes i els missatges i el que es publica, només amb contorn: cada dia, els missatges dels grups passen del redactor al revisor, i els documents de la Biblioteca digital i els recursos del repositori, del documentalista al revisor. Del revisor surten dos camins: el guionista i el jutge d'humor preparen la vinyeta, i l'il·lustrador dibuixa el que explica cada notícia, amb el revisor de dibuixos, que li torna el que no es veu bé. Tot acaba al traductor, i el número surt a les 7.00 amb un avís del portaveu per a cada grup. Els diumenges, el cap de reportatges, el reporter i el verificador preparen el reportatge, que passa també per l'il·lustrador, el revisor de dibuixos i el traductor i surt dins del número. A més, el guionista de vídeo escriu «La setmana en vídeo» amb els números de la setmana, i el vídeo surt també al número del diumenge.",
            "equipo": [
                ("Redactor", "llegeix les converses del dia dels tres grups, tria el que pot interessar a les persones que no hi són i escriu les peces, comprovant cada dada a la seva font original."),
                ("Revisor", "no ha escrit res: torna a obrir cada font, compara les peces amb els missatges i treu el que no pot confirmar. Fa el mateix amb els articles de la Biblioteca, contra el mateix document."),
                ("Documentalista", "quan entra un document a la Biblioteca digital de ChatGPT-IA-edu, el llegeix a la font oficial i n'escriu un article. També escriu sobre els recursos del Repositori de Vibe Coding Educativo, a partir del mateix recurs i d'una captura que fa un programa en obrir-lo."),
                ("Il·lustrador", "dibuixa el que explica cada notícia i, els diumenges, la infografia del reportatge."),
                ("Revisor de dibuixos", "mira cada dibuix a la seva pàgina, en tema clar i fosc, i el torna a l'il·lustrador si alguna cosa no es veu bé o no explica la notícia. Abans, un programa mesura el que es pot mesurar: colors, contrast i rètols que surten del dibuix o es trepitgen."),
                ("Guionista", "escriu cinc guions de la vinyeta amb Guix i Algorisme, els seus dos personatges."),
                ("Jutge d'humor", "tria el millor, sense haver-los escrit, o cap si no fa gràcia."),
                ("Traductor", "prepara aquesta edició en català a partir de la castellana, el Diario de IA Educativa."),
                ("Portaveu", "escriu cada matí l'avís amb què el diari es presenta a cada grup, diferent per a cadascun."),
                ("Cap de reportatges", "els diumenges tria el tema de la setmana que mereix un reportatge, el seu enfocament i a qui cal consultar."),
                ("Reporter", "investiga aquest tema fora dels grups, als documents de les empreses, les administracions i els organismes implicats, i escriu el reportatge."),
                ("Verificador", "no ha escrit res: obre cada font del reportatge i treu el que no pot confirmar."),
                ("Guionista de vídeo", "els dissabtes a la nit tria el més destacat de la setmana, com a mínim una peça de cada número, i escriu els textos de «La setmana en vídeo». Un programa comprova que no hi falti cap dia i que els textos hi càpiguen, i munta el vídeo amb els dibuixos del diari."),
            ],
            "equipo_pie": "Són agents de Claude, el model d'intel·ligència artificial d'Anthropic, i treballen amb Claude Code. Claude Opus 5.5 escriu i jutja la vinyeta i prepara el reportatge (guionista, jutge d'humor, cap de reportatges i reporter), i Claude Sonnet 5.5 fa la resta. Cada nit en treballen vuit; el documentalista s'hi suma quan entra un document a la Biblioteca digital o toca escriure sobre el repositori, i la nit del dissabte n'hi ha quatre més: tres per al reportatge del diumenge i un per a «La setmana en vídeo».",
            "secciones": [
                ("Què fa la intel·ligència artificial i què fan els programes", "La intel·ligència artificial s'encarrega del que demana llegir, escriure o jutjar: triar els temes, redactar, revisar, dibuixar, traduir i decidir si un acudit té gràcia. El que es pot fer amb regles fixes ho fan programes corrents, sense intel·ligència artificial: recollir i ordenar els missatges, mesurar els dibuixos, dibuixar la vinyeta a partir del guió, muntar el web amb l'hemeroteca i el cercador, muntar els vídeos i compondre'n la música, i publicar-ho tot a l'hora al web i a Instagram."),
                ("Els límits dels agents", "Els agents treballen en un servidor propi, sense accés a un terminal i sense poder llegir ni escriure fora de la carpeta de la redacció. Poden consultar internet per comprovar fonts, però no poden executar programes. Els missatges dels grups i les fitxes de la biblioteca són, per a ells, material per informar: si n'hi ha cap que contingui una ordre, no la segueixen, de manera que un missatge escrit per enganyar-los no els pot portar a fer una altra cosa. A més, cap agent no revisa la seva pròpia feina: les peces les repassa un revisor que no les ha escrites; els dibuixos, un revisor que no els ha dibuixat, i el reportatge, un verificador que no hi ha participat."),
                ("El que es comprova", "Els grups serveixen per saber de què es parla, però cada dada es comprova fora, a la seva font original: l'anunci oficial, el web del producte o el document de l'administració, enllaçats al final de cada peça. D'una aplicació compartida als grups es comprova el que diu el seu web, no que funcioni. Tot i així hi pot haver errors. Aquesta edició és una traducció automàtica de la castellana, sense revisió professional."),
                ("El reportatge del diumenge", "Els diumenges, a més de les peces del dia, el diari publica un reportatge sobre un sol tema de la setmana. Explica l'assumpte sencer, amb el que es va parlar als grups, el que diuen les empreses, les administracions i els organismes implicats, cadascun amb els seus documents, el marc a Espanya i el que pot fer un docent. L'escriuen tres agents més, i l'il·lustrador i el traductor de cada dia se n'encarreguen de la infografia i de la versió en català. Si el verificador no el dona per bo, aquell diumenge no hi ha reportatge i el número surt igualment. Tots queden a la secció {reportajes}."),
                ("La Biblioteca digital", "Cada document que entra a la {biblioteca} de ChatGPT-IA-edu (guies, informes, estudis) té el seu article a la secció {seccion_bib}; si el diari ja l'havia explicat com a notícia, aquella peça passa a la secció en lloc d'escriure'n una altra. El documentalista llegeix el document sencer i explica qui el publica, què proposa i com encaixa amb altres documents de la biblioteca; el revisor el contrasta amb el mateix document. El diari enllaça el document a la font oficial i a la biblioteca, sense copiar-lo. S'anomenen els autors; la persona que l'ha compartit no s'anomena, igual que no s'atribueixen les opinions dels grups."),
                ("El Repositori de recursos", "El {repositorio} de Vibe Coding Educativo reuneix les aplicacions i els recursos que creen i comparteixen amb llicència oberta els docents d'aquesta comunitat. Els dies amb menys de quatre peces, el documentalista escriu sobre els que hi han entrat i que el diari encara no ha explicat, i el número del dissabte repassa els de la setmana; si no n'hi ha cap de nou, en rescata un d'anterior. Un programa obre cada recurs i en guarda una captura del que es veu; el documentalista el descriu a partir de la captura i de la seva pàgina, i el revisor el torna a obrir. Surten a la secció {seccion_vc}, amb el nom de qui l'ha fet i la seva llicència."),
                ("Les persones", "La idea del diari és de {raul}, administrador d'{edumedia}. La redacció la va dissenyar i la supervisa {juanjo}."),
                ("El codi", "Els programes que preparen i munten el diari i l'encàrrec de cada agent són públics, al {codigo}, amb llicència AGPL v3, i cada decisió s'explica als seus registres de decisions (ADR). Els missatges dels grups no hi són."),
                ("Les comunitats", "{chatgpt}, sobre intel·ligència artificial en educació; {vce}, de docents que programen les seves pròpies aplicacions amb IA, i {edumedia}, sobre IA generativa per crear àudio, vídeo i imatge. Totes tres són obertes: cada peça enllaça amb la conversa on va néixer, que es pot llegir sense entrar-hi."),
                ("Si participes als grups", "Les opinions no s'atribueixen a ningú: només s'anomena la persona que ha publicat un recurs propi. Si hi apareix alguna cosa teva i prefereixes que no surti, o hi veus un error, digues-ho a les persones que administren el teu grup i es retirarà o es corregirà."),
            ],
        },
    },
}
L = IDIOMAS["es"]   # idioma de la pasada en curso

# Iconos de Lucide (ISC): wrench, code, clapperboard, messages-square, landmark, library; zap (breves), file-text (reportaje), pen-tool (viñeta), circle-play (vídeo)
ICONOS = {
    "herramientas": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "debates": '<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/>',
    "vibecoding": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "multimedia": '<path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 4"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
    "biblioteca": '<path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/>',
    "novedades": '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "breves": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "reportaje": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "video": '<path d="M9 9.003a1 1 0 0 1 1.517-.859l4.997 2.997a1 1 0 0 1 0 1.718l-4.997 2.997A1 1 0 0 1 9 14.996z"/><circle cx="12" cy="12" r="10"/>',
    "vineta": '<path d="M15.707 21.293a1 1 0 0 1-1.414 0l-1.586-1.586a1 1 0 0 1 0-1.414l5.586-5.586a1 1 0 0 1 1.414 0l1.586 1.586a1 1 0 0 1 0 1.414z"/><path d="m18 13-1.375-6.874a1 1 0 0 0-.746-.776L3.235 2.028a1 1 0 0 0-1.207 1.207L5.35 15.879a1 1 0 0 0 .776.746L13 18"/><path d="m2.3 2.3 7.286 7.286"/><circle cx="11" cy="11" r="2"/>',
}
COMPARTIR = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/></svg>'   # share-2
PLAY = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 9.003a1 1 0 0 1 1.517-.859l4.997 2.997a1 1 0 0 1 0 1.718l-4.997 2.997A1 1 0 0 1 9 14.996z"/><circle cx="12" cy="12" r="10"/></svg>'   # circle-play: la página de vídeos (ADR 0016)
LUPA = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'   # search
LUNA = '<svg class="luna" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>'
SOL = '<svg class="sol" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'


WEB_JUANJO = "https://bilateria.org"
WEB_RAUL = "https://raultorres-ia.github.io/apps/raul-torres-ai-portfolio/"

def de_mes(mes):
    """«de octubre» en castellano; en catalán, «d'octubre» ante vocal."""
    if L is IDIOMAS["ca"] and mes[0] in "aeiou":
        return f"d'{mes}"
    return f"de {mes}"


def fecha_larga(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{L['dias'][d.weekday()]}, {d.day} {de_mes(L['meses'][d.month - 1])} de {d.year}"


def publicacion(iso):
    """Un número sale a la mañana siguiente del día que cuenta: su fecha de cabecera es esa."""
    return (datetime.date.fromisoformat(iso) + datetime.timedelta(days=1)).isoformat()


def romano(n):
    r, resto = "", n
    for v, s in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                 (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while resto >= v:
            r += s
            resto -= v
    return r


def anyo_edicion(iso_publicacion):
    """«Año I» cuenta desde el año del número 1, como en la cabecera clásica de un periódico."""
    primero = datetime.date.fromisoformat(publicacion(LANZAMIENTO)).year
    return romano(datetime.date.fromisoformat(iso_publicacion).year - primero + 1)


def mes_largo(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{L['meses'][d.month - 1].capitalize()} de {d.year}"


def fecha_corta(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {de_mes(L['meses'][d.month - 1])}"


def e(t):
    return html.escape(t or "", quote=True)


def enlace(url, texto):
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{texto}</a>'


PIEZAS = set()   # (fecha, id) de todo lo publicado, para los enlaces entre piezas (encargos/enlaces.md)


def enlace_pieza(m):
    """[texto](pieza:AAAA-MM-DD/id) → enlace a esa pieza en el idioma de la página, desde la raíz del
    sitio para que valga en cualquier página. Si la pieza no existe, queda el texto sin enlace."""
    texto, fecha, pid = m.group(1), m.group(2), m.group(3)
    if (fecha, pid) not in PIEZAS:
        return texto
    return f'<a href="/{L["carpeta"]}{fecha}/{pid}.html">{texto}</a>'


def md(t):
    """Escapa y convierte los enlaces [texto](url) del Markdown en enlaces."""
    t = e(t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)   # cursiva: títulos de obras
    t = re.sub(r"\[([^\]]+)\]\(pieza:(\d{4}-\d{2}-\d{2})/([\w-]+)\)", enlace_pieza, t)   # otra pieza del diario
    t = re.sub(r"\[([^\]]+)\]\(((?:\.\./)?\d{4}-\d{2}-\d{2}/[\w-]+\.html)\)", r'<a href="\2">\1</a>', t)   # forma antigua
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", lambda m: enlace(html.unescape(m.group(2)), m.group(1)), t)


def icono(seccion):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONOS.get(seccion, "")}</svg>'


def url_mensaje(m):
    """Enlace público al mensaje: los tres grupos son públicos y se leen sin ser miembro."""
    if not m or m.get("grupo") not in GRUPOS or not m.get("id"):
        return None
    return f"https://t.me/{GRUPOS[m['grupo']][1]}/{int(m['id'])}"


def con_traduccion(carpeta, nombre):
    """El archivo traducido si existe; si no, el original."""
    f = RAIZ / f"{carpeta}{L['sufijo']}" / nombre
    return f if f.exists() else RAIZ / carpeta / nombre


CAPTURA_ANCHO, CAPTURA_ALTO = 1280, 800   # las capturas de los recursos del repositorio (scripts/repositorio.py)


def captura(prof, r, ampliable=False):
    """La captura de un recurso del repositorio (ADR 0008). En el artículo se amplía al pulsarla."""
    src = f'{recursos(prof)}capturas/{e(pathlib.Path(r["captura"]).name)}'
    img = (f'<img src="{src}" alt="{e(r.get("captura_alt") or r.get("titulo"))}" width="{CAPTURA_ANCHO}" '
           f'height="{CAPTURA_ALTO}" loading="lazy" decoding="async">')
    if ampliable:
        img = boton_ampliar(img, e(r.get("captura_alt") or r.get("titulo")))
    return f'<figure class="ilu captura">{img}</figure>'


def ilustracion(fecha, pieza, prof="", ampliable=False):
    f = con_traduccion("ilustraciones", f"{fecha}-{pieza['id']}.svg")
    if not f.exists():
        # Un artículo del repositorio no lleva dibujo, sino la captura de su recurso (la del primero en la semana)
        r = next((x for x in pieza.get("recursos", []) if x.get("captura")), None)
        return captura(prof, r, ampliable) if r else ""
    svg = re.sub(r"<\?xml.*?\?>", "", f.read_text()).strip()
    desc = e(pieza.get("ilustracion_alt") or pieza["titular"])
    svg = svg.replace("<svg", f'<svg role="img" aria-label="{desc}"', 1)
    return f'<figure class="ilu">{boton_ampliar(svg, desc) if ampliable else svg}</figure>'


def boton_ampliar(contenido, desc):
    """Un dibujo o una captura que se amplía al pulsarlo, sobre la propia página. El botón tapa la
    descripción de lo que lleva dentro para el lector de pantalla: la repite en su nombre."""
    return (f'<button type="button" class="ampliar" aria-label="{e(L["ampliar"])}: {desc}" title="{e(L["ampliar"])}" '
            f'data-cerrar="{e(L["cerrar"])}">{contenido}</button>')


def cargar():
    eds = []
    nombres = sorted({f.name for c in ("ediciones", "biblioteca", "repositorio") for f in (RAIZ / c).glob("*.json")})
    for nombre in nombres:
        f = RAIZ / "ediciones" / nombre
        d = json.loads(con_traduccion("ediciones", nombre).read_text()) if f.exists() else {}
        if not (d.get("hay_edicion") and d.get("piezas")):
            d = {"fecha": nombre[:-5], "hay_edicion": True, "piezas": [], "breves": [], "reserva": d.get("reserva")}
        if (RAIZ / "biblioteca" / nombre).exists():   # los artículos de la Biblioteca digital (ADR 0006)
            bib = json.loads(con_traduccion("biblioteca", nombre).read_text()).get("piezas", [])
            for x in bib:   # todos llevan dibujo: salen como destacados, marque lo que marque el agente
                x["importancia"] = 2
            d["piezas"] = d["piezas"] + bib
        if (RAIZ / "repositorio" / nombre).exists():   # los recursos del Repositorio de VCE (ADR 0008)
            rep_ = json.loads(con_traduccion("repositorio", nombre).read_text()).get("piezas", [])
            for x in rep_:   # con captura, salen como destacados
                x["importancia"] = 2 if any(r.get("captura") for r in x.get("recursos", [])) else 3
            d["piezas"] = d["piezas"] + rep_
        if d.get("piezas"):
            d["piezas"].sort(key=lambda p: p.get("importancia", 3))
            for p in d["piezas"]:
                p["fecha"] = d["fecha"]
            for i, b in enumerate(d.get("breves", []), 1):
                b["fecha"], b["n"] = d["fecha"], i   # cada breve tiene su página: AAAA-MM-DD/breve-N.html
            r = RAIZ / "reportajes" / f.name   # el reportaje del domingo, con el número que sale ese día (ADR 0004)
            if r.exists():
                rep = json.loads(con_traduccion("reportajes", f.name).read_text())
                if rep.get("hay_reportaje") and rep.get("apartados"):
                    d["reportaje"] = dict(rep, fecha=d["fecha"], seccion=None, reportaje=True)
            eds.append(d)
    # Un documento de la Biblioteca que el diario ya había contado no tiene artículo propio: la pieza
    # que lo contó pasa también a la sección Biblioteca, con el enlace al documento (ADR 0006)
    por_id = {(p["fecha"], p["id"]): p for d in eds for p in d["piezas"]}
    for f in sorted((RAIZ / "biblioteca").glob("*.json")):
        for y in json.loads(f.read_text()).get("ya_contado", []):
            p = por_id.get((y.get("fecha"), y.get("id")))
            if p and y.get("mensaje"):
                p["biblioteca"] = y["mensaje"]
    n = 0
    for d in eds:   # cada día con piezas desde el lanzamiento es un número del diario
        if d["fecha"] >= LANZAMIENTO:
            n += 1
            d["numero"] = n
        else:
            d["numero"] = None
    return eds


def seleccion_portada(eds):
    """Lo de los últimos días: lo más reciente delante y, dentro de cada día, por importancia.
    Abre la pieza principal del último día."""
    ultima = datetime.date.fromisoformat(eds[-1]["fecha"])
    desde = (ultima - datetime.timedelta(days=DIAS_PORTADA - 1)).isoformat()
    recientes = [d for d in reversed(eds) if d["fecha"] >= desde]
    todas = [p for d in recientes for p in d["piezas"]]
    piezas = [p for p in todas if p.get("seccion") != "biblioteca"][:MAX_PIEZAS]
    piezas += [p for p in todas if p.get("seccion") == "biblioteca"][:BIBLIOTECA_PORTADA]
    # Los del último número, todos (van arriba); de los días anteriores, como mucho MAX_BREVES
    breves = recientes[0].get("breves", []) + [b for d in recientes[1:] for b in d.get("breves", [])][:MAX_BREVES]
    return piezas, breves


def recursos(prof):
    """Las hojas de estilo y la letra están en la raíz del sitio, compartidas por los dos idiomas."""
    return prof + ("../" if L["carpeta"] else "")


ULTIMA = None   # fecha del último número, para la imagen de vista previa de la portada


def imagen_og(ruta, codigo):
    """La portada y la página de cada día enseñan la imagen de su número (ADR 0010); lo demás, la genérica."""
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})/", ruta)
    fecha = m.group(1) if m else (ULTIMA if ruta == "" else None)
    if fecha and (RAIZ / "og" / "numeros" / f"{fecha}-{codigo}.png").exists():
        return f"{BASE}og/{fecha}-{codigo}.png"
    return f"{BASE}og-{codigo}.png"


def cabeza(titulo, prof, descripcion, ruta, portada=False):
    codigo = "ca" if L["carpeta"] else "es"
    r = recursos(prof)
    otro = "es" if codigo == "ca" else "ca"
    # En la portada, quien llega sin haber elegido idioma va al del sistema; lo elegido se recuerda
    salto = ""
    if portada:
        if codigo == "es":   # al catalán, si se eligió o si el sistema está en catalán y no se eligió nada
            cond = "var g=localStorage.getItem('sala.idioma');if(g==='ca'||(!g&&(navigator.language||'').slice(0,2)==='ca'))"
        else:                # al castellano, solo si se eligió: un enlace a la edición catalana se respeta
            cond = "if(localStorage.getItem('sala.idioma')==='es')"
        salto = f"<script>try{{{cond}location.replace('{href_idioma(prof, ruta, otro)}');}}catch(_){{}}</script>"
    return f"""<!doctype html>
<html lang="{codigo}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="alternate" hreflang="{otro}" href="{href_idioma(prof, ruta, otro)}">
<link rel="alternate" type="application/rss+xml" title="{e(L["titulo"])}" href="{prof}feed.xml">
<meta property="og:type" content="{"website" if portada else "article"}">
<meta property="og:site_name" content="{e(L["titulo"])}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{e(BASE + L["carpeta"] + ruta)}">
<meta property="og:image" content="{e(imagen_og(ruta, codigo))}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{"ca_ES" if codigo == "ca" else "es_ES"}">
<meta name="twitter:card" content="summary_large_image">
<script>try{{var t=localStorage.getItem('sala.tema');if(t)document.documentElement.dataset.theme=t;}}catch(_){{}}</script>
{salto}
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{r}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
<link rel="manifest" href="{prof}manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="{e(L["nombre_corto"])}">
<meta name="theme-color" content="#16181d">
<link rel="stylesheet" href="{r}fuentes.css?v={version_estatico("fuentes.css")}">
<link rel="stylesheet" href="{r}comun.css?v={version_estatico("comun.css")}">
<link rel="stylesheet" href="{r}{MAQUETA}.css?v={version_estatico(MAQUETA + ".css")}">
</head>
"""


def version_estatico(nombre):
    """Huella del contenido de una hoja de estilos: cambia la dirección cuando cambia la hoja, y el
    navegador no mezcla una página nueva con la hoja antigua que guardaba (GitHub Pages: 10 min)."""
    return hashlib.sha256((RAIZ / "estaticos" / nombre).read_bytes()).hexdigest()[:8]


def href_idioma(prof, ruta, destino):
    """La misma página en el otro idioma."""
    if ruta == "404.html":   # solo hay una, en la raíz: la otra edición lleva a su portada
        return "/ca/" if destino == "ca" else "/"
    if destino == "ca":
        return f"{prof}ca/{ruta}"
    return f"{prof}../{ruta}"


def selector_idioma(prof, ruta):
    """Como en un periódico: un enlace a la otra edición, con su nombre en su idioma."""
    codigo = "ca" if L["carpeta"] else "es"
    otro = "es" if codigo == "ca" else "ca"
    d = IDIOMAS[otro]
    return (f'<a class="edicion" href="{href_idioma(prof, ruta, otro)}" lang="{otro}" hreflang="{otro}" '
            f'data-idioma="{otro}"><span class="largo">{d["edicion"]}</span><span class="corto">{d["nombre"]}</span></a>')


def boton_tema():
    return f'<button type="button" class="tema" id="tema" title="{L["tema"]}" aria-label="{L["tema"]}">{LUNA}{SOL}</button>'


SCRIPT_TEMA = """<script>
(function(){
  var raiz=document.documentElement, sistema=matchMedia('(prefers-color-scheme: dark)');
  function oscuro(){return raiz.dataset.theme? raiz.dataset.theme==='dark' : sistema.matches;}
  function pinta(){raiz.dataset.theme = oscuro()?'dark':'light';}
  pinta();
  sistema.addEventListener('change',function(){try{if(!localStorage.getItem('sala.tema')){delete raiz.dataset.theme;pinta();}}catch(_){pinta();}});
  document.getElementById('tema').addEventListener('click',function(){
    var nuevo = oscuro()?'light':'dark'; raiz.dataset.theme=nuevo;
    try{ if((nuevo==='dark')===sistema.matches) localStorage.removeItem('sala.tema'); else localStorage.setItem('sala.tema',nuevo);}catch(_){}
  });
  document.querySelectorAll('[data-idioma]').forEach(function(a){
    a.addEventListener('click',function(){try{localStorage.setItem('sala.idioma',a.dataset.idioma);}catch(_){}});
  });
  // En el móvil las secciones se deslizan: la sección abierta, a la vista
  var lista=document.querySelector('.secciones-lista'), activa=lista&&lista.querySelector('[aria-current]');
  if(activa&&lista.scrollWidth>lista.clientWidth) lista.scrollLeft=activa.offsetLeft-(lista.clientWidth-activa.offsetWidth)/2;
  // Ampliar una captura o un dibujo: sobre la propia página, al mayor tamaño que quepa, con la X arriba a la derecha
  document.querySelectorAll('button.ampliar').forEach(function(b){
    b.addEventListener('click',function(){
      var img=b.querySelector('img'), dib=b.querySelector('svg'), v=document.createElement('div'), x=document.createElement('button'), g;
      v.className='visor'; v.setAttribute('role','dialog'); v.setAttribute('aria-modal','true');
      if(img){ g=img.cloneNode(); v.setAttribute('aria-label',img.alt); }
      else {   // un dibujo: en su marco, con los colores de su sección y tan grande como quepa
        var sec=b.closest('[class*="sec-"]'), c=sec&&[].find.call(sec.classList,function(k){return k.indexOf('sec-')===0;}), vb=dib.viewBox.baseVal;
        if(c) v.classList.add(c);
        g=document.createElement('div'); g.className='ilu'; g.append(dib.cloneNode(true)); v.setAttribute('aria-label',dib.getAttribute('aria-label')||'');
        g.style.width='min(100%, calc((100dvh - 6.2rem) * '+(vb&&vb.height?vb.width/vb.height:16/9)+' + 2rem))';
      }
      x.type='button'; x.className='cerrar'; x.setAttribute('aria-label',b.dataset.cerrar||'Cerrar'); x.title=x.getAttribute('aria-label');
      x.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
      g.removeAttribute('loading'); v.append(g,x); document.body.append(v); document.body.classList.add('con-visor'); x.focus();
      // La imagen crece desde donde está en la página y vuelve a su sitio al cerrar; sin movimiento
      // si el sistema pide reducirlo
      var origen=img||b.closest('.ilu')||b, cerrando=false;
      var suave=g.animate&&!matchMedia('(prefers-reduced-motion: reduce)').matches;
      function zoom(abre){
        var a=origen.getBoundingClientRect(), z=g.getBoundingClientRect(), op={duration:300,easing:'cubic-bezier(.2,.8,.2,1)',fill:'both'};
        var pag='translate('+(a.left-z.left)+'px,'+(a.top-z.top)+'px) scale('+(a.width/z.width)+','+(a.height/z.height)+')';
        var k=[{transform:pag},{transform:'none'}], f=[{backgroundColor:'rgba(10,12,16,0)'},{backgroundColor:'rgba(10,12,16,0.88)'}], o=[{opacity:0},{opacity:1}];
        if(!abre){k.reverse();f.reverse();o.reverse();}
        g.style.transformOrigin='0 0'; v.animate(f,op); x.animate(o,op); return g.animate(k,op);
      }
      if(suave) zoom(true);
      function quitar(){v.remove();document.body.classList.remove('con-visor');document.removeEventListener('keydown',tecla);b.focus();}
      function fuera(){if(cerrando)return; cerrando=true; if(suave) zoom(false).onfinish=quitar; else quitar();}
      // El visor es modal: con el tabulador, el foco se queda en su único control, la X
      function tecla(ev){if(ev.key==='Escape')fuera(); else if(ev.key==='Tab'){ev.preventDefault();x.focus();}}
      v.addEventListener('click',function(ev){if(!g.contains(ev.target))fuera();});
      document.addEventListener('keydown',tecla);
    });
  });
  // Instalar como app (ADR 0013): el enlace del pie sale solo donde el navegador deja instalar con un
  // toque (Chrome, Edge); en iPhone y iPad, cómo añadirlo a la pantalla de inicio. Instalada, nada.
  var inst=document.querySelector('.instalar-app'), ios=document.querySelector('.instalar-ios'), pide=null;
  var instalada=matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  if(inst&&!instalada){
    addEventListener('beforeinstallprompt',function(ev){ev.preventDefault();pide=ev;inst.hidden=false;});
    inst.querySelector('button').addEventListener('click',function(){
      if(!pide)return; pide.prompt(); pide.userChoice.then(function(){pide=null;inst.hidden=true;},function(){});
    });
    addEventListener('appinstalled',function(){inst.hidden=true;});
    if(ios&&(/iP(hone|ad|od)/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1))) ios.hidden=false;
  }
  // Compartir: el menú del dispositivo; si no lo hay, se copia el enlace
  document.querySelectorAll('.compartir').forEach(function(b){
    b.addEventListener('click',function(){
      var url=b.dataset.url||location.href, datos={title:b.dataset.titulo||document.title,url:url}, r=b.querySelector('span');
      if(navigator.share){navigator.share(datos).catch(function(){});return;}
      if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){
        var antes=r.textContent; r.textContent=b.dataset.copiado; b.classList.add('hecho'); b.disabled=true;
        setTimeout(function(){r.textContent=antes;b.classList.remove('hecho');b.disabled=false;},1800);
      });}
    });
  });
})();
</script>"""


DIAS_PIE = 7            # el pie lista los últimos días; el resto, en la hemeroteca


def url_vcer():
    """La página de la mención VCER, con el título y la dirección del diario en el idioma de la página."""
    r, p, f = VCER
    q = urllib.parse.urlencode({"r": r, "p": p, "f": f, "t": L["titulo"], "u": BASE + L["carpeta"]}, quote_via=urllib.parse.quote)
    return "https://vibe-coding-educativo.github.io/vibe-responsable/vcer/?" + q


def pie(prof, eds, actual):
    marca = ' aria-current="page"'
    archivo = "".join(
        f'<li><a href="{prof}{d["fecha"]}/"{marca if d["fecha"] == actual else ""}>{fecha_larga(publicacion(d["fecha"])).capitalize()}</a></li>'
        for d in list(reversed(eds))[:DIAS_PIE])
    grupos = "".join(f'<li>{enlace("https://t.me/" + a, n)}: <span class="pie-grupo-desc">{L["grupos_desc"][k]}</span></li>'
                     for k, (n, a) in GRUPOS.items())
    trad = f'<p>{L["traduccion"]}</p>' if L["traduccion"] else ""
    return f"""<footer class="pie">
  <div class="pie-unete">
    <h2>{L["unete"]}</h2>
    <p>{L["unete_txt"]}</p>
    <ul class="pie-grupos">{grupos}</ul>
    <p class="pie-rss"><a href="{prof}redaccion.html">{L["quees"]}</a> · <a href="{prof}videos.html">{L["videos"]}</a> · {enlace(INSTAGRAM, L["instagram"])} · <a href="{prof}feed.xml">{L["rss"]}</a><span class="instalar-app" hidden> · <button type="button" class="instalar" title="{e(L["instalar_titulo"])}">{L["instalar"]}</button></span></p>
    <p class="instalar-ios" hidden>{L["instalar_ios"]}</p>
  </div>
  <nav class="pie-archivo" aria-label="{L["archivo"]}">
    <h2>{L["archivo"]}</h2>
    <ul>{archivo}</ul>
    <p class="pie-hemeroteca"><a href="{prof}archivo.html">{L["todos_numeros"]}</a></p>
  </nav>
  <div class="pie-creditos">
    <p>{L["redactado"]}</p>
    {trad}
    <p>© {datetime.date.fromisoformat(eds[-1]["fecha"]).year} {enlace(WEB_JUANJO, "Juan José de Haro")} {L["y"]} {enlace(WEB_RAUL, "Raül Torres")}. {L["licencia"]} {enlace("https://creativecommons.org/licenses/by-sa/4.0/" + L["deed"], "CC BY-SA 4.0")}.</p>
    <p>{L["letra"]} {enlace("https://github.com/productiontype/Newsreader", "Newsreader")} (Production Type, <a href="{prof}fuentes/OFL.txt">OFL</a>). {L["iconos"]} {enlace("https://lucide.dev", "Lucide")} (<a href="{prof}LICENSE-LUCIDE.txt">ISC</a>).</p>
    <p>{enlace(url_vcer(), L["vcer"])}.</p>
  </div>
</footer>"""


def barra_secciones(prof, activa):
    """La barra de secciones bajo la mancheta, como en un periódico; «La redacción» cierra la barra, también en el móvil."""
    marca = ' aria-current="page"'
    enlaces = [f'<a href="{prof or "./"}"{marca if activa == "portada" else ""}>{L["portada"]}</a>']
    enlaces += [f'<a class="sec-{c}" href="{prof}{c}.html"{marca if c == activa else ""}>{L["secciones"][c]}</a>' for c in ORDEN_SECCIONES]
    enlaces.append(f'<a class="sec-reportaje" href="{prof}reportajes.html"{marca if activa == "reportajes" else ""}>{L["reportajes"]}</a>')
    enlaces.append(f'<a class="sec-vineta" href="{prof}vineta.html"{marca if activa == "vineta" else ""}>{L["vineta"]}</a>')
    quees = f'<a class="quees" href="{prof}redaccion.html"{marca if activa == "redaccion" else ""}>{L["quees"]}</a>'
    return f'<nav class="secciones" aria-label="{L["secciones_nav"]}"><div class="secciones-lista">{"".join(enlaces)}{quees}</div></nav>'


def cabecera(prof, ruta, fecha, cuenta, es_portada, nav="", h1=True, activa=None):
    """`cuenta` es el número de la edición, rodeado a mano con el bolígrafo rojo, como en un periódico.
    Con h1="dia" (la página de un número de la hemeroteca), la mancheta es el h1 de la página, con el
    enlace a la portada y la fecha solo para el lector de pantalla: se ve igual que con un <p>."""
    etiqueta = "h1" if h1 else "p"
    nombre = L["titulo"] if h1 is True else f'<a href="{prof}">{L["titulo"]}</a>'
    sale = publicacion(fecha)
    if h1 == "dia":
        nombre += f'<span class="solo-lector">, {fecha_larga(sale)}</span>'
    cuando = f'<time datetime="{sale}">{fecha_larga(sale).capitalize()}</time>'
    numero = (f'<span class="edicion-num"><span class="anyo">{L["anyo"]} {anyo_edicion(sale)}</span>'
              f'<span class="numero"><span class="solo-lector">{L["numero_largo"]} </span><span aria-hidden="true">{L["num"]}&nbsp;</span><b>{cuenta}</b></span></span>')
    return f"""<header class="cabecera">
  <div class="cabecera-fila">
    <span class="cuando">{cuando}</span>
    {numero if cuenta else '<span></span>'}
    <span class="controles"><a class="ico-video" href="{prof}videos.html" title="{L["videos"]}" aria-label="{L["videos"]}">{PLAY}</a><a class="lupa" href="{prof}buscar.html" title="{L["buscar_etiqueta"]}" aria-label="{L["buscar_etiqueta"]}">{LUPA}<span class="lupa-rotulo">{L["buscar"]}</span></a>{selector_idioma(prof, ruta)}{boton_tema()}</span>
  </div>
  <{etiqueta} class="mancheta">{nombre}</{etiqueta}>
  <p class="lema">{L["lema"]}</p>
  {barra_secciones(prof, activa)}
  {f'<nav class="navegacion" aria-label="{L["navegacion"]}">{nav}</nav>' if nav else ""}
</header>"""


def href(prof, p):
    return f'{prof}{p["fecha"]}/{e(p["id"])}.html'


def origen(p):
    n, a = GRUPOS.get(p.get("grupo"), ("", ""))
    u = url_mensaje(p.get("mensaje"))
    if p.get("seccion") == "biblioteca" and u:
        return f'<p class="origen">{enlace(u, L["en_biblioteca"])}</p>'
    if p.get("recursos"):   # un artículo del repositorio: no nace de una conversación
        return f'<p class="origen">{enlace(REPOSITORIO, L["en_repositorio"])}</p>'
    bib = url_mensaje(p.get("biblioteca"))   # una noticia sobre un documento que luego entró en la Biblioteca
    if u and bib:
        return f'<p class="origen">{enlace(u, L["leer_conv"] + " " + n)} · {enlace(bib, L["en_biblioteca"])}</p>'
    if u:
        return f'<p class="origen">{enlace(u, L["leer_conv"] + " " + n)}</p>'
    return f'<p class="origen">{L["tema_en"]} {enlace("https://t.me/" + a, n)}</p>' if n else ""


def rotulos(p, mostrar_fecha, prof="", sin_seccion=False):
    sec = p.get("seccion", "")
    fecha = f' <span class="fecha-pieza">{fecha_corta(publicacion(p["fecha"]))}</span>' if mostrar_fecha else ""
    nombre = L["secciones"].get(sec, "")
    rotulo = f'<a href="{prof}{sec}.html">{icono(sec)} {nombre}</a>' if sec in L["secciones"] else nombre
    if sin_seccion:   # en la página de la sección, el nombre ya está en el título
        rotulo = ""
    return f"""<p class="seccion"><span>{rotulo}</span>{fecha}</p>
  <p class="antetitulo">{e(p.get("antetitulo"))}</p>"""


def pieza(prof, p, clase, nivel, con_ilu, mostrar_fecha, sin_seccion=False, relleno=False):
    ilu = ilustracion(p["fecha"], p, prof) if con_ilu else ""
    if not ilu and relleno:   # en la página de la sección, sin dibujo: el icono de la sección, para que la fila no deje huecos
        ilu = f'<figure class="ilu relleno" aria-hidden="true">{icono(p.get("seccion", ""))}</figure>'
    return f"""<article class="pieza {clase} sec-{e(p.get("seccion", ""))}">
  {ilu}
  <div class="texto">
  {rotulos(p, mostrar_fecha, prof, sin_seccion)}
  <h{nivel} class="titular"><a href="{href(prof, p)}">{e(p["titular"])}</a></h{nivel}>
  <p class="entradilla">{e(p.get("entradilla"))}</p>
  </div>
</article>"""


def ruta_breve(b):
    return f'{b["fecha"]}/breve-{b["n"]}.html'


def texto_plano(t):
    """El texto de un breve sin el Markdown de sus enlaces ni sus negritas."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t or "")
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    return re.sub(r"(?<![*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![*\w])", r"\1", t)


def titulo_breve(b):
    """La primera frase del breve, para el título y la vista previa al compartirlo."""
    t = texto_plano(b["texto"]).strip()
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    frase = m.group(1) if m else t
    return frase if len(frase) <= 110 else frase[:107].rsplit(" ", 1)[0] + "…"


def boton_compartir(b):
    """Solo el icono, discreto: comparte la página del breve, no la de donde se lee."""
    url = BASE + L["carpeta"] + ruta_breve(b)
    return (f'<button type="button" class="compartir solo-icono" data-url="{e(url)}" data-titulo="{e(titulo_breve(b))}" '
            f'data-copiado="{e(L["copiado"])}" title="{e(L["compartir_breve"])}" aria-label="{e(L["compartir_breve"])}">'
            f'{COMPARTIR}<span></span></button>')


def bloque_breves(breves, mostrar_fecha, en_bloque=False):
    if not breves:
        return ""
    items = []
    for b in breves:
        t = md(b["texto"])
        enl = []
        if b.get("url"):
            enl.append(enlace(b["url"], L["fuente"]))
        u = url_mensaje(b.get("mensaje"))
        if u:
            enl.append(enlace(u, L["conversacion"]))
        fecha = f'<span class="fecha-pieza">{fecha_corta(publicacion(b["fecha"]))}</span> ' if mostrar_fecha else ""
        items.append(f'<li>{fecha}{t} {" ".join(enl)} {boton_compartir(b)}</li>')
    if en_bloque:
        return "".join(f'<div class="breve">{i[4:-5]}</div>' for i in items)
    return f'<aside class="breves" aria-labelledby="t-breves"><h2 id="t-breves">{L["breves"]}</h2><ul>{"".join(items)}</ul></aside>'


def cuerpo_portada(prof, piezas, breves, mostrar_fecha, tira=""):
    """Como en un periódico: la apertura a todo el ancho, una fila de destacadas con dibujo,
    la viñeta y, debajo, un bloque por sección con su título a la izquierda (al estilo de
    The Guardian). Las secciones sin piezas no salen. En la portada, los breves del último número
    van arriba, tras las destacadas, como lo demás de hoy; los de días anteriores cierran abajo."""
    p0, resto = piezas[0], piezas[1:]
    hoy = [b for b in breves if b["fecha"] == p0["fecha"]] if mostrar_fecha else []
    breves = [b for b in breves if b not in hoy]
    # Como mucho tres destacadas con dibujo (las más recientes): la portada tiene que caber sin un scroll interminable.
    # En la portada, solo del último número: lo de días anteriores no se cuela entre lo de hoy, va a su sección
    destacadas = [p for p in resto if p.get("importancia", 3) <= 2 and p.get("seccion") != "biblioteca"
                  and (not mostrar_fecha or p["fecha"] == p0["fecha"])][:3]
    # Si quedan huecos, los ocupan las demás piezas de hoy aunque sean menores: así no queda una suelta debajo
    if mostrar_fecha:
        destacadas += [p for p in resto if p not in destacadas and p["fecha"] == p0["fecha"]
                       and p.get("seccion") != "biblioteca"][:3 - len(destacadas)]
    demas = [p for p in resto if p not in destacadas]
    # En la portada, todo lo de hoy va arriba: lo que no cabe entre las destacadas, también los
    # artículos de la Biblioteca, justo debajo en «Más del día»; los bloques, para los días anteriores
    mas_hoy = [p for p in demas if p["fecha"] == p0["fecha"]] if mostrar_fecha else []
    demas = [p for p in demas if p not in mas_hoy]
    html_ = pieza(prof, p0, "principal", 2, True, mostrar_fecha)
    if destacadas:
        filas = "".join(pieza(prof, p, "destacada", 2, True, mostrar_fecha) for p in destacadas)
        sola = " sola" if len(destacadas) == 1 else ""
        html_ += f'<div class="fila fila-destacadas{sola}" style="--n:{min(len(destacadas), 3)}">{filas}</div>'
    if mas_hoy:
        # Sin título: cada pieza lleva su sección, y van en las columnas de las destacadas
        lista = "".join(pieza(prof, p, "menor", 3, False, mostrar_fecha) for p in mas_hoy)
        html_ += f'<div class="fila fila-menores mas-dia" style="--n:3">{lista}</div>'
    if hoy:
        html_ += f"""<section class="bloque sec-breves breves-dia" aria-labelledby="b-breves-dia">
  <h2 id="b-breves-dia" class="bloque-titulo"><a href="{prof}breves.html">{icono("breves")} {L["breves"]}</a></h2>
  <div class="bloque-piezas" style="--n:{min(len(hoy), 3)}">{bloque_breves(hoy, mostrar_fecha, en_bloque=True)}</div>
</section>"""
    html_ += tira
    for clave in ORDEN_SECCIONES:
        de_seccion = [p for p in demas if p.get("seccion") == clave]
        if not de_seccion:
            continue
        lista = "".join(pieza(prof, p, "menor", 3, False, mostrar_fecha, sin_seccion=True) for p in de_seccion)
        html_ += f"""<section class="bloque sec-{clave}" aria-labelledby="b-{clave}">
  <h2 id="b-{clave}" class="bloque-titulo"><a href="{prof}{clave}.html">{icono(clave)} {L["secciones"][clave]}</a></h2>
  <div class="bloque-piezas" style="--n:{min(len(de_seccion), 3)}">{lista}</div>
</section>"""
    sueltas = [p for p in demas if p.get("seccion") not in ORDEN_SECCIONES]
    if sueltas or breves:
        lista = "".join(pieza(prof, p, "menor", 3, False, mostrar_fecha) for p in sueltas) + bloque_breves(breves, mostrar_fecha, en_bloque=True)
        html_ += f"""<section class="bloque sec-breves" aria-labelledby="b-breves">
  <h2 id="b-breves" class="bloque-titulo"><a href="{prof}breves.html">{icono("breves")} {L["breves_antes"] if mostrar_fecha and hoy else L["breves"]}</a></h2>
  <div class="bloque-piezas" style="--n:{min(len(sueltas) + (len(breves) if breves else 0), 3)}">{lista}</div>
</section>"""
    return html_


def bloque_vineta(prof, eds, fecha, en_archivo=False):
    """La tira del día, si la hay: el juez puede dejar un día sin viñeta si ninguna tiene gracia."""
    f = con_traduccion("vinetas", f"{fecha}.json")
    if not f.exists():
        return ""
    elegida = json.loads(f.read_text()).get("elegida")
    if not elegida:
        return ""
    d = next((x for x in eds if x["fecha"] == fecha), None)
    p = next((x for x in (d or {}).get("piezas", []) if x["id"] == elegida.get("pieza")), None)
    origen_txt = f'{L["a_partir"]} <a href="{href(prof, p)}">{e(p["titular"])}</a>.' if p else L["a_partir_dia"]
    return f"""<section class="vineta sec-vineta" aria-labelledby="t-vineta-{fecha}">
  <h2 id="t-vineta-{fecha}" class="vineta-titulo"><span>{"" if en_archivo else f'<a href="{prof}vineta.html">{icono("vineta")} {L["vineta_titulo"]}</a>'}</span> <span class="fecha-pieza">{fecha_corta(publicacion(fecha))}</span></h2>
  <div class="tira">{vineta.tira(elegida["guion"])}</div>
  <p class="vineta-origen">{origen_txt}</p>
</section>"""


def franja_reserva(d):
    """El día que la redacción falló y el número salió con una pieza de reserva (ADR 0021): qué ha
    pasado y que lo de ayer sale mañana. Solo si fue un fallo; un día sin nada que contar, nada."""
    if d.get("reserva") not in ("fallo", True):
        return ""
    return f'<p class="aviso-reserva" role="note">{L["reserva_aviso"]}</p>'


def franja_editorial(prof, d):
    """«Desde la redacción»: a todo el ancho bajo la barra de secciones, el día que la hay (el número 1)."""
    ed = d.get("editorial")
    if not ed:
        return ""
    ed = dict(ed, fecha=d["fecha"])
    return f"""<section class="editorial" aria-labelledby="ed-{e(ed["id"])}">
  <div class="texto">
    <p class="antetitulo">{e(ed["antetitulo"])}</p>
    <h2 id="ed-{e(ed["id"])}" class="titular"><a href="{href(prof, ed)}">{e(ed["titular"])}</a></h2>
    <p class="entradilla">{e(ed["entradilla"])}</p>
    <p class="leer"><a href="{href(prof, ed)}">{L["leer_presentacion"]}</a></p>
  </div>
  {ilustracion(d["fecha"], ed)}
</section>"""


def minutos_lectura(r):
    palabras = sum(len(texto_plano(x).split()) for a in r["apartados"] for x in a.get("parrafos", []))
    return max(1, round(palabras / 220))


def franja_reportaje(prof, r):
    """El reportaje del domingo: a todo el ancho, como la franja editorial, con su infografía."""
    if not r:
        return ""
    return f"""<section class="editorial reportaje-franja" aria-labelledby="rep-{e(r["id"])}">
  <div class="texto">
    <p class="seccion"><span><a href="{prof}reportajes.html">{icono("reportaje")} {L["reportaje"]}</a></span> <span class="fecha-pieza">{fecha_corta(publicacion(r["fecha"]))} · {minutos_lectura(r)} {L["palabras"]}</span></p>
    <p class="antetitulo">{e(r["antetitulo"])}</p>
    <h2 id="rep-{e(r["id"])}" class="titular"><a href="{href(prof, r)}">{e(r["titular"])}</a></h2>
    <p class="entradilla">{e(r["entradilla"])}</p>
    <p class="leer"><a href="{href(prof, r)}">{L["leer_reportaje"]}</a></p>
  </div>
  {ilustracion(r["fecha"], r)}
</section>"""


def reportaje_reciente(eds, fecha):
    """El último reportaje de la semana que acaba en `fecha`: el domingo abre la portada y, los
    días siguientes, sigue en ella tras las destacadas hasta que sale el siguiente."""
    desde = (datetime.date.fromisoformat(fecha) - datetime.timedelta(days=DIAS_PORTADA - 1)).isoformat()
    return next((d["reportaje"] for d in reversed(eds) if desde <= d["fecha"] <= fecha and d.get("reportaje")), None)


def pagina_portada(prof, ruta, eds, piezas, breves, fecha, cuenta, es_portada, nav=""):
    titulo = L["titulo"] if es_portada else f'{L["titulo"]}, {fecha_larga(publicacion(fecha))}'
    dia = next((x for x in eds if x["fecha"] == fecha), {})
    # En la portada, el de la semana; en la página de un día, solo el suyo. Arriba el día que sale;
    # los demás días, después de la viñeta, que es del número de hoy (ADR 0004)
    rep = reportaje_reciente(eds, fecha) if es_portada else dia.get("reportaje")
    arriba = bool(rep) and rep["fecha"] == fecha
    return cabeza(titulo, prof, L["lema"], ruta, portada=es_portada) + f"""<body class="pag-portada">
{cabecera(prof, ruta, fecha, cuenta, es_portada, nav, h1=True if es_portada else "dia", activa="portada" if es_portada else None)}
<main class="portada">
{franja_reserva(dia)}
{franja_editorial(prof, dia)}
{franja_reportaje(prof, rep) if arriba else ""}
{cuerpo_portada(prof, piezas, breves, es_portada, bloque_vineta(prof, eds, fecha) + bloque_semana_video(prof, eds, fecha) + ("" if arriba else franja_reportaje(prof, rep)))}
</main>
{pie(prof, eds, None if es_portada else fecha)}
{SCRIPT_TEMA}
</body>
</html>"""


def enlaces_biblioteca(prof, texto, eds):
    """Un enlace a un documento de la Biblioteca digital lleva a su artículo del diario, si lo tiene."""
    articulos = {int((x.get("mensaje") or {}).get("id") or 0): x for dd in eds for x in dd["piezas"] if x.get("seccion") == "biblioteca"}
    articulos.update({int(x["biblioteca"].get("id") or 0): x for dd in eds for x in dd["piezas"]
                      if x.get("biblioteca") and int(x["biblioteca"].get("id") or 0) not in articulos})
    def cambia(m):
        x = articulos.get(int(m.group(2)))
        return f"]({href(prof, x)})" if x else m.group(0)
    return re.sub(r"\]\((https://t\.me/ChatGPTedu/21753/(\d+))\)", cambia, texto)


def indexado(clave, nombre, fecha):
    """Atributos de Pagefind: solo se indexa esto; con su sección como filtro, su fecha y su color."""
    return (f' data-pagefind-body data-pagefind-filter="seccion:{e(nombre)}" data-pagefind-sort="fecha:{e(fecha)}"'
            f' data-pagefind-meta="fecha:{e(fecha_corta(publicacion(fecha)))}"><span hidden data-pagefind-meta="clave:{e(clave)}"></span')


def enlaces_recurso(r):
    partes = [enlace(r["url"], L["rec_abrir"])] if r.get("url") else []
    if r.get("ficha"):
        partes.append(enlace(r["ficha"], L["rec_ficha"]))
    return " · ".join(partes)


def ficha_recurso(pid, r):
    filas = "".join(f"<dt>{L[k]}</dt><dd>{e(r.get(c))}</dd>" for k, c in
                    (("rec_titulo", "titulo"), ("rec_autoria", "autoria"), ("rec_licencia", "licencia")) if r.get(c))
    return (f'<aside class="ficha-doc" aria-labelledby="rec-{e(pid)}"><h2 id="rec-{e(pid)}">{L["el_recurso"]}</h2>'
            f'<dl>{filas}</dl><p class="doc-leer">{enlaces_recurso(r)}</p></aside>')


def bloque_recurso(prof, pid, r):
    datos = " · ".join(e(x) for x in (r.get("autoria"), r.get("licencia")) if x)
    titulo = enlace(r["url"], e(r["titulo"])) if r.get("url") else e(r["titulo"])
    texto = "".join(f"<p>{md(x)}</p>" for x in r.get("texto", []))
    return (f'<section class="recurso" aria-labelledby="r-{e(pid)}-{e(r.get("id", ""))}">'
            f'<h2 id="r-{e(pid)}-{e(r.get("id", ""))}" class="ladillo">{titulo}</h2>'
            f'{f"<p class=recurso-datos>{datos}</p>" if datos else ""}'
            f'<div class="recurso-cuerpo">{captura(prof, r, ampliable=True) if r.get("captura") else ""}'
            f'<div class="recurso-texto">{texto}<p class="recurso-enlaces">{enlaces_recurso(r)}</p></div></div></section>')


def articulo(prof, ruta, d, p, eds):
    parrafos = [enlaces_biblioteca(prof, x, eds) for x in p.get("cuerpo", [])]
    # La capitular solo cuando el primer párrafo empieza por letra: con comillas o cifras queda rara
    cap = ' class="capitular"' if parrafos and parrafos[0][:1].isalpha() else ""
    cuerpo = "".join(f"<p{cap if i == 0 else ''}>{md(x)}</p>" for i, x in enumerate(parrafos))
    fuentes = "".join(f'<li>{enlace(f["url"], e(f["titulo"]))}</li>' for f in p.get("fuentes", []))
    comprobado = (f'<section class="comprobado" data-pagefind-ignore aria-labelledby="comp-{e(p["id"])}"><h2 id="comp-{e(p["id"])}">'
                  f'{L["comprobado"]}</h2><ul>{fuentes}</ul></section>') if fuentes else ""
    compartir = (f'<p class="acciones" data-pagefind-ignore><button type="button" class="compartir" data-copiado="{e(L["copiado"])}">'
                 f'{COMPARTIR}<span>{L["compartir"]}</span></button></p>')
    doc = p.get("documento") or {}
    ficha_doc = ""
    if doc:
        filas = "".join(f"<dt>{L[k]}</dt><dd>{e(doc.get(c))}</dd>" for k, c in
                        (("doc_titulo", "titulo"), ("doc_autoria", "autoria"), ("doc_anyo", "anyo"), ("doc_idioma", "idioma"), ("doc_licencia", "licencia")) if doc.get(c))
        leer = f'<p class="doc-leer">{enlace(doc["url"], L["doc_leer"])}</p>' if doc.get("url") else ""
        ficha_doc = f'<aside class="ficha-doc" aria-labelledby="doc-{e(p["id"])}"><h2 id="doc-{e(p["id"])}">{L["el_documento"]}</h2><dl>{filas}</dl>{leer}</aside>'
    recs = p.get("recursos") or []
    bloques = ""
    if len(recs) == 1:   # el artículo de un recurso: su ficha, como la del documento de la Biblioteca
        ficha_doc = ficha_recurso(p["id"], recs[0])
    elif recs:           # la semana del repositorio: un apartado por recurso, con su captura
        bloques = "".join(bloque_recurso(prof, p["id"], r) for r in recs)
    return cabeza(f'{p["titular"]} | {L["titulo"]}', prof, p.get("entradilla", ""), ruta) + f"""<body class="pag-articulo">
{cabecera(prof, ruta, d["fecha"], d["numero"], False, h1=False)}
<main class="articulo">
  <article{f' class="sec-{e(p["seccion"])}"' if p.get("seccion") else ""}{indexado(p.get("seccion") or "editorial", L["secciones"].get(p.get("seccion"), L["quees"]), d["fecha"])}>
    {rotulos(p, True, prof)}
    <h1 class="titular">{e(p["titular"])}</h1>
    <p class="entradilla">{e(p.get("entradilla"))}</p>
    {"" if len(p.get("recursos") or []) > 1 else ilustracion(d["fecha"], p, prof, ampliable=True)}
    {ficha_doc}
    <div class="cuerpo">{cuerpo}{bloques}</div>
    {f'<p class="correccion">{md(p["correccion"])}</p>' if p.get("correccion") else ""}
    {origen(p)}
    {compartir}
    {comprobado}
  </article>
  {mas_piezas(prof, eds, p)}
  <p class="volver"><a href="{prof}">{L["volver"]}</a></p>
</main>
{pie(prof, eds, d["fecha"])}
{SCRIPT_TEMA}
</body>
</html>"""


def articulo_reportaje(prof, ruta, d, r, eds):
    """El reportaje: apartados con ladillo, las claves al lado y, al final, las piezas de la semana."""
    apartados = []
    for i, a in enumerate(r["apartados"]):
        pars = a.get("parrafos", [])
        cap = ' class="capitular"' if i == 0 and pars and pars[0][:1].isalpha() else ""
        texto = "".join(f"<p{cap if j == 0 else ''}>{md(x)}</p>" for j, x in enumerate(pars))
        apartados.append((f'<h2 class="ladillo">{e(a["ladillo"])}</h2>' if a.get("ladillo") else "") + texto)
        if i == 0 and r.get("claves"):
            claves = "".join(f"<li>{md(c)}</li>" for c in r["claves"])
            apartados.append(f'<aside class="claves" aria-labelledby="claves-{e(r["id"])}"><h2 id="claves-{e(r["id"])}">{L["claves"]}</h2><ul>{claves}</ul></aside>')
    fuentes = "".join(f'<li>{enlace(f["url"], e(f["titulo"]))}</li>' for f in r.get("fuentes", []))
    comprobado = (f'<section class="comprobado" data-pagefind-ignore aria-labelledby="comp-{e(r["id"])}"><h2 id="comp-{e(r["id"])}">'
                  f'{L["comprobado"]}</h2><ul>{fuentes}</ul></section>') if fuentes else ""
    piezas = {(x["fecha"], x["id"]): x for x in (p for dd in eds for p in dd["piezas"])}
    rel = [piezas[(x.get("fecha"), x.get("id"))] for x in r.get("relacionadas", []) if (x.get("fecha"), x.get("id")) in piezas]
    relacionadas = ""
    if rel:
        items = "".join(f'<li><span class="fecha-pieza">{fecha_corta(publicacion(x["fecha"]))}</span>'
                        f'<a href="{href(prof, x)}">{e(x["titular"])}</a></li>' for x in rel)
        relacionadas = f'<aside class="mas sec-reportaje" aria-labelledby="t-rel"><h2 id="t-rel">{L["en_el_diario"]}</h2><ul>{items}</ul></aside>'
    compartir = (f'<p class="acciones" data-pagefind-ignore><button type="button" class="compartir" data-copiado="{e(L["copiado"])}">'
                 f'{COMPARTIR}<span>{L["compartir"]}</span></button></p>')
    return cabeza(f'{r["titular"]} | {L["titulo"]}', prof, r.get("entradilla", ""), ruta) + f"""<body class="pag-articulo">
{cabecera(prof, ruta, d["fecha"], d["numero"], False, h1=False)}
<main class="articulo reportaje">
  <article class="sec-reportaje"{indexado("reportaje", L["reportajes"], d["fecha"])}>
    <p class="seccion"><span><a href="{prof}reportajes.html">{icono("reportaje")} {L["reportaje"]}</a></span> <span class="fecha-pieza">{fecha_corta(publicacion(r["fecha"]))} · {minutos_lectura(r)} {L["palabras"]}</span></p>
    <p class="antetitulo">{e(r.get("antetitulo"))}</p>
    <h1 class="titular">{e(r["titular"])}</h1>
    <p class="entradilla">{e(r.get("entradilla"))}</p>
    {ilustracion(d["fecha"], r, prof, ampliable=True)}
    <div class="cuerpo">{"".join(apartados)}</div>
    {origen(dict(r, grupo=(r.get("mensaje") or {}).get("grupo")))}
    {compartir}
    {comprobado}
  </article>
  {relacionadas}
  <p class="volver"><a href="{prof}">{L["volver"]}</a></p>
</main>
{pie(prof, eds, d["fecha"])}
{SCRIPT_TEMA}
</body>
</html>"""


def pagina_reportajes(eds):
    reps = [d["reportaje"] for d in reversed(eds) if d.get("reportaje")]
    cuerpo = "".join(franja_reportaje("", r) for r in reps) or f'<p class="vacio">{L["sin_reportajes"]}</p>'
    return cabeza(f'{L["reportajes"]} | {L["titulo"]}', "", L["descripciones"]["reportajes"], "reportajes.html") + f"""<body class="pag-seccion">
{cabecera("", "reportajes.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False, activa="reportajes")}
<main class="portada">
<h1 class="titulo-seccion sec-reportaje">{icono("reportaje")} {L["reportajes"]}</h1>
<p class="descripcion-seccion">{descripcion("reportajes")}</p>
{cuerpo}
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


MAS_PIEZAS = 3


def mas_piezas(prof, eds, p):
    """«Más en esta sección» al pie del artículo: las piezas más recientes de la misma sección;
    si no hay, las del diario. Quien llega desde un aviso tiene adónde seguir."""
    sec = p.get("seccion")
    recientes = [x for d in reversed(eds) for x in d["piezas"] if not (x["id"] == p["id"] and x["fecha"] == p["fecha"])]
    misma = [x for x in recientes if x.get("seccion") == sec][:MAS_PIEZAS]
    if misma and sec in L["secciones"]:
        titulo, lista, clase = f'{L["mas_en"]} {L["secciones"][sec]}', misma, f"sec-{sec}"
    elif recientes:
        titulo, lista, clase = L["mas_diario"], recientes[:MAS_PIEZAS], ""
    else:
        return ""
    items = "".join(f'<li><span class="fecha-pieza">{fecha_corta(publicacion(x["fecha"]))}</span>'
                    f'<a href="{href(prof, x)}">{e(x["titular"])}</a></li>' for x in lista)
    return f'<aside class="mas {clase}" aria-labelledby="t-mas"><h2 id="t-mas">{titulo}</h2><ul>{items}</ul></aside>'


def pagina_breve(prof, d, b, eds):
    """La página de un breve: lo que se abre al compartirlo. El texto, sus enlaces y el botón de compartir."""
    enl = []
    if b.get("url"):
        enl.append(enlace(b["url"], L["fuente"]))
    u = url_mensaje(b.get("mensaje"))
    if u:
        enl.append(enlace(u, L["conversacion"]))
    compartir = (f'<p class="acciones" data-pagefind-ignore><button type="button" class="compartir" data-copiado="{e(L["copiado"])}">'
                 f'{COMPARTIR}<span>{L["compartir"]}</span></button></p>')
    titulo = titulo_breve(b)
    return cabeza(f'{titulo} | {L["titulo"]}', prof, texto_plano(b["texto"]), ruta_breve(b)) + f"""<body class="pag-articulo">
{cabecera(prof, ruta_breve(b), d["fecha"], d["numero"], False, h1=False)}
<main class="articulo breve-pagina">
  <article{indexado("breves", L["breves"], d["fecha"])}>
    <p class="seccion"><span><a href="{prof}breves.html">{icono("breves")} {L["breves"]}</a></span> <span class="fecha-pieza">{fecha_corta(publicacion(b["fecha"]))}</span></p>
    <h1 class="solo-lector">{e(titulo)}</h1>
    <p class="breve-texto">{md(b["texto"])}</p>
    <p class="breve-enlaces">{" · ".join(enl)}</p>
    {compartir}
  </article>
  {mas_piezas(prof, eds, {"id": "", "fecha": "", "seccion": None})}
  <p class="volver"><a href="{prof}">{L["volver"]}</a></p>
</main>
{pie(prof, eds, d["fecha"])}
{SCRIPT_TEMA}
</body>
</html>"""


def nav_dia(prof, eds, i):
    partes = []
    if i > 0:
        partes.append(f'<a class="ant" href="{prof}{eds[i - 1]["fecha"]}/">{L["dia_ant"]}</a>')
    if i + 1 < len(eds):
        partes.append(f'<a class="sig" href="{prof}{eds[i + 1]["fecha"]}/">{L["dia_sig"]}</a>')
    return "".join(partes)


def d_href(d):
    return f'{d["fecha"]}/{e(d["editorial"]["id"])}.html'


INSTAGRAM = "https://www.instagram.com/comunidad.iaeducativa/"


def cargar_videos():
    """Los vídeos del diario (videos/*.json, ADR 0016), del más reciente al más antiguo. Cada uno
    tiene su vídeo y su portada por idioma; si falta el del idioma, va el castellano y se dice."""
    vs = []
    for f in sorted((RAIZ / "videos").glob("*.json")):
        v = json.loads(f.read_text())
        if all((RAIZ / "videos" / x).exists() for x in v["archivos"]["es"].values()):
            vs.append(v)
    return sorted(vs, key=lambda v: v["publicado"], reverse=True)


def texto_video(v, campo):
    x = v.get(campo, {})
    return x.get("ca" if L["carpeta"] else "es") or x.get("es")


def bloque_video(prof, v, titulo_h="h2", enlace_propio=True, titulo=None):
    """Un vídeo vertical, sin reproducción automática, con su portada y lo que dice en pantalla."""
    codigo = "ca" if L["carpeta"] else "es"
    arch = v["archivos"].get(codigo) or v["archivos"]["es"]
    otro_idioma = codigo not in v["archivos"]
    ruta = f'{recursos(prof)}videos/'
    pantalla = "".join(f"<li>{e(x)}</li>" for x in texto_video(v, "pantalla") or [])
    ig = f' · {enlace(v["instagram"], L["en_instagram"])}' if v.get("instagram") else ""
    propio = f' · <a href="{prof}videos.html#{e(v["id"])}">{L["video_enlace"]}</a>' if enlace_propio else ""
    idioma = f' {L["video_idioma"]}' if otro_idioma else ""
    return f"""<figure class="video" id="{e(v["id"])}">
  <{titulo_h} class="video-titulo">{e(titulo or texto_video(v, "titulo"))}</{titulo_h}>
  <video controls preload="none" playsinline poster="{ruta}{e(arch["poster"])}" width="720" height="1280">
    <source src="{ruta}{e(arch["video"])}" type="video/mp4">
  </video>
  <figcaption><p>{e(texto_video(v, "descripcion"))}{idioma}</p>
  <p class="video-meta">{fecha_corta(v["publicado"])}{ig}{propio}</p>
  {f'<details class="video-pantalla"><summary>{L["en_pantalla"]}</summary><ol>{pantalla}</ol></details>' if pantalla else ""}
  </figcaption>
</figure>"""


def fechas_semana(publicado):
    """«Del 2 al 8 de noviembre»: los números de lunes a domingo que repasa el vídeo."""
    fin = datetime.date.fromisoformat(publicado)
    ini = fin - datetime.timedelta(days=6)
    mes = lambda d: de_mes(L["meses"][d.month - 1])  # noqa: E731
    vocal = lambda n: bool(L["carpeta"]) and n in (1, 11)  # noqa: E731   en catalán, «de l'1», «a l'11»
    del_ = "De l'" if vocal(ini.day) else "Del "
    al_ = "a l'" if vocal(fin.day) else "al "
    if ini.month == fin.month:
        return f"{del_}{ini.day} {al_}{fin.day} {mes(fin)}"
    return f"{del_}{ini.day} {mes(ini)} {al_}{fin.day} {mes(fin)}"


def bloque_semana_video(prof, eds, fecha):
    """«La semana en vídeo», en el número del domingo, como franja a todo el ancho (como el
    reportaje): el vídeo y, al lado, las piezas que salen en él, enlazadas a su artículo."""
    v = next((x for x in cargar_videos() if x.get("tipo") == "semana" and x.get("dia") == fecha), None)
    if not v:
        return ""
    codigo = "ca" if L["carpeta"] else "es"
    arch = v["archivos"].get(codigo) or v["archivos"]["es"]
    ruta = f'{recursos(prof)}videos/'
    por_id = {(d["fecha"], p["id"]): p for d in eds for p in d["piezas"]}
    items = ""
    for x in v.get("piezas", []):
        p = por_id.get((x["fecha"], x["id"]))
        if p:
            items += (f'<li class="sec-{e(p.get("seccion") or "")}"><span class="s">{e(L["secciones"].get(p.get("seccion"), ""))}</span>'
                      f'<a href="{href(prof, p)}">{e(p["titular"])}</a></li>')
    pantalla = "".join(f"<li>{e(x)}</li>" for x in texto_video(v, "pantalla") or [])
    ig = f' · {enlace(v["instagram"], L["en_instagram"])}' if v.get("instagram") else ""
    return f"""<section class="editorial semana-franja" id="{e(v["id"])}" aria-labelledby="t-semana-{fecha}">
  <video controls preload="none" playsinline poster="{ruta}{e(arch["poster"])}" width="720" height="1280" aria-describedby="d-semana-{fecha}">
    <source src="{ruta}{e(arch["video"])}" type="video/mp4">
  </video>
  <div class="texto">
    <p class="seccion"><span><a href="{prof}videos.html">{icono("video")} {L["semana_video"]}</a></span> <span class="fecha-pieza">{v.get("duracion", "")} s</span></p>
    <h2 id="t-semana-{fecha}" class="titular">{fechas_semana(v["publicado"])}</h2>
    <p class="entradilla" id="d-semana-{fecha}">{e(texto_video(v, "descripcion"))}</p>
    {f'<ol class="semana-piezas">{items}</ol>' if items else ""}
    <p class="leer"><a href="{prof}videos.html">{L["todos_videos"]}</a>{ig}</p>
    {f'<details class="video-pantalla"><summary>{L["en_pantalla"]}</summary><ol>{pantalla}</ol></details>' if pantalla else ""}
  </div>
</section>"""


def pagina_videos(eds):
    vs = cargar_videos()
    lista = "".join(bloque_video("", v, enlace_propio=False) for v in vs)
    return cabeza(f'{L["videos"]} | {L["titulo"]}', "", L["descripciones"]["videos"], "videos.html") + f"""<body class="pag-seccion">
{cabecera("", "videos.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada videos">
<h1 class="titulo-seccion">{L["videos"]}</h1>
<p class="descripcion-seccion">{descripcion("videos")} {enlace(INSTAGRAM, "@comunidad.iaeducativa")}.</p>
{f'<div class="lista-videos">{lista}</div>' if lista else f'<p class="vacio">{L["sin_videos"]}</p>'}
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def pagina_redaccion(eds):
    """«La redacción»: quién hace el diario, empezando por el equipo de agentes y su organigrama."""
    R = L["redaccion"]
    grupos = {k: enlace("https://t.me/" + a, n) for k, (n, a) in GRUPOS.items()}
    grupos.update(juanjo=enlace(WEB_JUANJO, "Juan José de Haro"), raul=enlace(WEB_RAUL, "Raül Torres"),
                  reportajes=f'<a href="reportajes.html">{L["reportajes"]}</a>',
                  biblioteca=enlace(TEMA_BIBLIOTECA, L["biblioteca_enlace"]), seccion_bib=f'<a href="biblioteca.html">{L["secciones"]["biblioteca"]}</a>',
                  repositorio=enlace(REPOSITORIO, L["repositorio_enlace"]), seccion_vc=f'<a href="vibecoding.html">{L["secciones"]["vibecoding"]}</a>',
                  codigo=enlace(CODIGO, L["codigo_enlace"]))
    pres = next((d for d in eds if d.get("editorial")), None)
    # El organigrama de hoy, con los agentes del domingo; el de la presentación del número 1 queda como se publicó
    f = con_traduccion("ilustraciones", "redaccion-organigrama.svg")
    organigrama = ""
    if f.exists():
        svg = re.sub(r"<\?xml.*?\?>", "", f.read_text()).strip().replace("<svg", f'<svg role="img" aria-label="{e(R["organigrama_alt"])}"', 1)
        organigrama = f'<figure class="ilu">{boton_ampliar(svg, e(R["organigrama_alt"]))}</figure>'
    elif pres:
        organigrama = ilustracion(pres["fecha"], pres["editorial"], ampliable=True)
    equipo = "".join(f"<li><strong>{rol}</strong>: {texto}</li>" for rol, texto in R["equipo"])
    pasos = "".join(f"<li>{x.format(**grupos)}</li>" for x in R["proceso"])
    resto = "".join(f"<h2>{t}</h2><p>{x.format(**grupos)}</p>" for t, x in R["secciones"])
    enlace_pres = f'<p class="presentacion"><a href="{d_href(pres)}">{L["presentacion"]}</a></p>' if pres else ""
    cab = cabecera("", "redaccion.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False, activa="redaccion")
    return cabeza(f'{L["quees"]} | {L["titulo"]}', "", R["intro"], "redaccion.html") + f"""<body class="pag-que-es">
{cab}
<main class="articulo que-es redaccion">
<h1 class="titular">{L["quees"]}</h1>
<p class="entradilla">{R["intro"]}</p>
{organigrama}
<h2>{R["proceso_titulo"]}</h2>
<p>{R["proceso_intro"]}</p>
<ol class="proceso">{pasos}</ol>
<p>{R["proceso_pie"]}</p>
<h2>{R["equipo_titulo"]}</h2>
<ul class="equipo">{equipo}</ul>
<p>{R["equipo_pie"]}</p>
{resto}
{enlace_pres}
<p class="volver"><a href="./">{L["volver"]}</a></p>
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def redireccion(destino):
    """La dirección antigua sigue funcionando: lo publicado no se rompe."""
    return (f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={destino}">'
            f'<link rel="canonical" href="{destino}"><title>{L["quees"]}</title><a href="{destino}">{L["quees"]}</a>')


def descripcion(clave):
    """Qué es cada sección, bajo su título: con tantas secciones, el nombre solo no basta."""
    return L["descripciones"][clave].format(enlace=enlace(TEMA_BIBLIOTECA, L["biblioteca_enlace"]), repositorio=enlace(REPOSITORIO, L["repositorio_enlace"]))


def pagina_seccion(eds, clave):
    todas = [p for d in reversed(eds) for p in d["piezas"]
             if p.get("seccion") == clave or (clave == "biblioteca" and p.get("biblioteca"))]
    if todas:
        cuerpo = "".join(pieza("", p, "destacada", 2, True, True, sin_seccion=True, relleno=True) for p in todas)
        cuerpo = f'<div class="fila fila-seccion" style="--n:3">{cuerpo}</div>'
    else:
        cuerpo = f'<p class="vacio">{L["sin_piezas"]}</p>'
    nombre = L["secciones"][clave]
    return cabeza(f'{nombre} | {L["titulo"]}', "", L["descripciones"][clave].format(enlace=L["biblioteca_enlace"], repositorio=L["repositorio_enlace"]), f"{clave}.html") + f"""<body class="pag-seccion">
{cabecera("", f"{clave}.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False, activa=clave)}
<main class="portada">
<h1 class="titulo-seccion sec-{clave}">{icono(clave)} {nombre}</h1>
<p class="descripcion-seccion">{descripcion(clave)}</p>
{cuerpo}
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def pagina_hemeroteca(eds):
    """Todos los números por meses, del más reciente al más antiguo, cada uno con su apertura."""
    meses = {}
    for d in reversed(eds):
        sale = publicacion(d["fecha"])
        meses.setdefault(sale[:7], []).append((d, sale))
    bloques = []
    for clave, dias in meses.items():
        items = []
        for d, sale in dias:
            num = f' <span class="num">· {L["num"]}&nbsp;{d["numero"]}</span>' if d["numero"] else ""
            abre = d["reportaje"]["titular"] if d.get("reportaje") else d["piezas"][0]["titular"]
            marca = f'<span class="rep">{L["reportaje"]}</span>' if d.get("reportaje") else ""
            items.append(f'<li><a href="{d["fecha"]}/">{fecha_larga(sale).capitalize()}</a>{num}'
                         f'<span class="abre">{marca}{e(abre)}</span></li>')
        bloques.append(f'<h2>{mes_largo(dias[0][1])}</h2><ul>{"".join(items)}</ul>')
    return cabeza(f'{L["hemeroteca"]} | {L["titulo"]}', "", L["hemeroteca_txt"], "archivo.html") + f"""<body class="pag-seccion">
{cabecera("", "archivo.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada hemeroteca">
<h1 class="titulo-seccion">{L["hemeroteca"]}</h1>
<p class="vineta-sub-pagina">{L["hemeroteca_txt"]}</p>
{"".join(bloques)}
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def pagina_404(eds):
    """La página de GitHub Pages para lo que no existe, con rutas absolutas porque se sirve en cualquier nivel.
    En castellano, con la línea en catalán debajo: GitHub solo admite una."""
    ca = IDIOMAS["ca"]
    html_ = cabeza(f'{L["no_existe"]} | {L["titulo"]}', "/", L["no_existe_txt"], "404.html")
    return html_ + f"""<body class="pag-que-es">
{cabecera("/", "404.html", eds[-1]["fecha"], eds[-1]["numero"], False, h1=False)}
<main class="articulo no-existe">
<h1 class="titular">{L["no_existe"]}</h1>
<p>{L["no_existe_txt"]}</p>
<p><a href="/">{L["portada"]}</a> · <a href="/archivo.html">{L["hemeroteca"]}</a></p>
<p class="ca" lang="ca">{ca["no_existe"]}. <a href="/ca/">{ca["portada"]}</a> · <a href="/ca/archivo.html">{ca["hemeroteca"]}</a></p>
</main>
{pie("/", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def sitemap(eds):
    """Todas las páginas de los dos idiomas, con la fecha de su último cambio."""
    urls = []
    ultima = publicacion(eds[-1]["fecha"])
    for codigo, idioma in IDIOMAS.items():
        base = BASE + idioma["carpeta"]
        for ruta in ["", "redaccion.html", "vineta.html", "reportajes.html", "breves.html", "archivo.html", "videos.html"] + [f"{c}.html" for c in ORDEN_SECCIONES]:
            urls.append((base + ruta, ultima))
        for d in eds:
            sale = publicacion(d["fecha"])
            urls.append((f'{base}{d["fecha"]}/', sale))
            for p in d["piezas"] + [d[k] for k in ("editorial", "reportaje") if d.get(k)]:
                urls.append((f'{base}{d["fecha"]}/{p["id"]}.html', sale))
            for b in d.get("breves", []):
                urls.append((base + ruta_breve(b), sale))
    cuerpo = "".join(f"  <url><loc>{e(u)}</loc><lastmod>{f}</lastmod></url>\n" for u, f in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{cuerpo}</urlset>\n'


SCRIPT_BUSCAR = """<script type="module">
const T = __TEXTOS__, POR_PAGINA = 10;
const campo = document.getElementById('q'), estado = document.getElementById('estado'), lista = document.getElementById('resultados'),
      filtros = document.getElementById('filtros'), mas = document.getElementById('mas');
let pf = null, seccion = null, actuales = [], mostrados = 0, vuelta = 0;
const params = new URLSearchParams(location.search);
campo.value = params.get('q') || ''; seccion = params.get('seccion');
try { pf = await import('__RUTA__pagefind/pagefind.js'); await pf.options({ excerptLength: 28 }); await pf.filters(); }
catch (_) { estado.textContent = T.sin_buscador; }
function direccion(q) {   // la búsqueda queda en la dirección, para compartirla tal cual
  const u = new URL(location.href);
  q ? u.searchParams.set('q', q) : u.searchParams.delete('q');
  seccion ? u.searchParams.set('seccion', seccion) : u.searchParams.delete('seccion');
  history.replaceState(null, '', u);
}
function boton(nombre, valor, n) {
  const b = document.createElement('button'); b.type = 'button'; b.className = 'filtro';
  b.textContent = n == null ? nombre : `${nombre} (${n})`;
  b.setAttribute('aria-pressed', String(seccion === valor));
  b.addEventListener('click', () => { seccion = valor; buscar(); });
  return b;
}
function pintaFiltros(r) {
  const cuenta = ((seccion ? r.totalFilters : r.filters) || {}).seccion || {};   // sin sección elegida, el recuento de esta búsqueda
  const nombres = Object.keys(cuenta).filter(k => cuenta[k] > 0).sort((a, b) => cuenta[b] - cuenta[a]);
  filtros.replaceChildren(boton(T.todas, null), ...nombres.map(k => boton(k, k, cuenta[k])));
  filtros.hidden = nombres.length < 2 && !seccion;
}
async function siguientes() {
  const tanda = await Promise.all(actuales.slice(mostrados, mostrados + POR_PAGINA).map(r => r.data()));
  for (const d of tanda) {
    const li = document.createElement('li'); li.className = 'resultado sec-' + ((d.meta && d.meta.clave) || '');
    const rot = document.createElement('p'); rot.className = 'seccion';
    const s = document.createElement('span'); s.textContent = (d.filters && d.filters.seccion && d.filters.seccion[0]) || '';
    const f = document.createElement('span'); f.className = 'fecha-pieza'; f.textContent = (d.meta && d.meta.fecha) || '';
    rot.append(s, f);
    const h = document.createElement('h2'); h.className = 'titular';
    const a = document.createElement('a'); a.href = d.url; a.textContent = (d.meta && d.meta.title) || d.url; h.append(a);
    const x = document.createElement('p'); x.className = 'extracto'; x.innerHTML = d.excerpt;   // Pagefind lo da escapado, con <mark>
    li.append(rot, h, x); lista.append(li);
  }
  mostrados += tanda.length; mas.hidden = mostrados >= actuales.length;
}
async function buscar() {
  const q = campo.value.trim(), esta = ++vuelta;
  direccion(q);
  if (!q || !pf) { lista.replaceChildren(); filtros.hidden = true; mas.hidden = true; if (pf) estado.textContent = ''; return; }
  estado.textContent = T.buscando;
  const r = await pf.debouncedSearch(q, seccion ? { filters: { seccion } } : {}, 250);
  if (r === null || esta !== vuelta) return;
  actuales = r.results; mostrados = 0; lista.replaceChildren();
  const n = actuales.length;
  estado.textContent = n === 0 ? T.sin_resultados : n === 1 ? T.resultados_1 : T.resultados_n.replace('{n}', n);
  pintaFiltros(r); await siguientes();
}
campo.addEventListener('input', () => { seccion = null; buscar(); });
document.getElementById('buscador').addEventListener('submit', ev => { ev.preventDefault(); buscar(); });
mas.addEventListener('click', siguientes);
if (campo.value) buscar(); else campo.focus();
</script>"""


def pagina_buscar(eds):
    """El buscador (ADR 0007): Pagefind en el navegador, sin servidor; busca en la lengua de la página."""
    textos = {k: L[k] for k in ("resultados_1", "resultados_n", "sin_resultados", "todas", "mas_resultados", "buscando", "sin_buscador")}
    script = SCRIPT_BUSCAR.replace("__TEXTOS__", json.dumps(textos, ensure_ascii=False)).replace("__RUTA__", recursos("") or "./")
    return cabeza(f'{L["buscar"]} | {L["titulo"]}', "", L["buscar_txt"], "buscar.html") + f"""<body class="pag-seccion">
{cabecera("", "buscar.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada pagina-buscar">
<h1 class="titulo-seccion">{L["buscar"]}</h1>
<p class="descripcion-seccion">{L["buscar_txt"]}</p>
<form id="buscador" role="search" class="buscador">
  <label class="solo-lector" for="q">{L["buscar_etiqueta"]}</label>
  <span class="campo">{LUPA}<input id="q" name="q" type="search" autocomplete="off" placeholder="{e(L["buscar_campo"])}"></span>
</form>
<div id="filtros" class="filtros" hidden></div>
<p id="estado" class="estado" role="status" aria-live="polite"></p>
<ol id="resultados" class="resultados"></ol>
<p><button type="button" id="mas" class="mas-resultados" hidden>{L["mas_resultados"]}</button></p>
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
{script}
</body>
</html>"""


def pagina_breves(eds):
    """Todos los breves, del más reciente al más antiguo, agrupados por el día en que salieron."""
    bloques = []
    for d in reversed(eds):
        if d.get("breves"):
            sale = publicacion(d["fecha"])
            bloques.append(f'<h2><a href="{d["fecha"]}/">{fecha_larga(sale).capitalize()}</a></h2>'
                           f'<div class="lista-breves">{bloque_breves(d["breves"], False, en_bloque=True)}</div>')
    return cabeza(f'{L["breves"]} | {L["titulo"]}', "", L["descripciones"]["breves"], "breves.html") + f"""<body class="pag-seccion">
{cabecera("", "breves.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada pagina-breves">
<h1 class="titulo-seccion sec-breves">{icono("breves")} {L["breves"]}</h1>
<p class="descripcion-seccion">{descripcion("breves")}</p>
{"".join(bloques)}
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def pagina_vinetas(eds):
    tiras = "".join(bloque_vineta("", eds, d["fecha"], en_archivo=True) for d in reversed(eds))
    return cabeza(f'{L["vineta_titulo"]} | {L["titulo"]}', "", L["lema"], "vineta.html") + f"""<body class="pag-seccion">
{cabecera("", "vineta.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False, activa="vineta")}
<main class="portada">
<h1 class="titulo-seccion sec-vineta">{icono("vineta")} {L["vineta_titulo"]}</h1>
<p class="descripcion-seccion">{descripcion("vineta")}</p>
{tiras or f'<p class="vacio">{L["sin_vinetas"]}</p>'}
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def rss(eds):
    """RSS 2.0 con las piezas, de la más reciente a la más antigua. Fechas en UTC."""
    base = BASE + L["carpeta"]
    items = []
    for d in reversed(eds):
        # Las 7:00 de Madrid del día de publicación, pasadas a UTC (el cambio de hora no la mueve)
        cuando = datetime.datetime.combine(datetime.date.fromisoformat(publicacion(d["fecha"])), datetime.time(7),
                                           ZoneInfo("Europe/Madrid")).astimezone(datetime.timezone.utc)
        for p in ([d["reportaje"]] if d.get("reportaje") else []) + d["piezas"]:
            url = f'{base}{p["fecha"]}/{p["id"]}.html'
            items.append(f"""  <item>
    <title>{e(p["titular"])}</title>
    <link>{e(url)}</link>
    <guid isPermaLink="true">{e(url)}</guid>
    <pubDate>{format_datetime(cuando)}</pubDate>
    <category>{e(L["reportaje"] if p.get("reportaje") else L["secciones"].get(p.get("seccion"), ""))}</category>
    <description>{e(p.get("entradilla"))}</description>
  </item>""")
        for b in d.get("breves", []):   # los breves, con su propia página
            url = base + ruta_breve(b)
            items.append(f"""  <item>
    <title>{e(titulo_breve(b))}</title>
    <link>{e(url)}</link>
    <guid isPermaLink="true">{e(url)}</guid>
    <pubDate>{format_datetime(cuando)}</pubDate>
    <category>{e(L["breves"])}</category>
    <description>{e(texto_plano(b["texto"]))}</description>
  </item>""")
    codigo = "ca" if L["carpeta"] else "es"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{e(L["titulo"])}</title>
  <link>{e(base)}</link>
  <atom:link href="{e(base)}feed.xml" rel="self" type="application/rss+xml"/>
  <description>{e(L["lema"])}</description>
  <language>{codigo}</language>
{chr(10).join(items)}
</channel>
</rss>
"""


def manifiesto():
    """La ficha que permite instalar el diario como app desde el navegador (ADR 0013), una por idioma:
    la instalada desde /ca/ se abre en catalán. Sin service worker ni avisos: siempre se lee lo publicado."""
    raiz = "/" + L["carpeta"]
    return json.dumps({
        "id": raiz, "start_url": raiz, "scope": raiz,
        "name": L["titulo"], "short_name": L["nombre_corto"], "description": L["lema"],
        "lang": "ca" if L["carpeta"] else "es", "dir": "ltr",
        "display": "standalone", "background_color": "#16181d", "theme_color": "#16181d",
        "icons": [
            {"src": "/icono-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/icono-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/icono-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }, ensure_ascii=False, indent=2) + "\n"


def indice_bot(eds):
    """Lo publicado, para que el Bot de IA Educativa busque en el diario (ADR 0017). Una entrada por pieza,
    breve, reportaje o editorial, con su número, su enlace en las dos ediciones y el mensaje original, que
    es lo que el bot cita primero. Sin las notas internas de la redacción («comprobado», «repaso»)."""
    entradas = []

    def poner(d, tipo, ruta, x, texto, seccion=None):
        entradas.append({
            "tipo": tipo, "numero": d["numero"], "fecha": d["fecha"], "sale": publicacion(d["fecha"]),
            "seccion": L["secciones"].get(seccion, "") if seccion else "",
            "antetitulo": x.get("antetitulo", ""), "titular": texto_plano(x.get("titular", "")),
            "entradilla": texto_plano(x.get("entradilla", "")),
            "texto": " ".join(texto_plano(t) for t in texto if t).strip(),
            "grupo": GRUPOS.get((x.get("mensaje") or {}).get("grupo") or x.get("grupo"), ("",))[0],
            "mensaje": url_mensaje(x.get("mensaje")),
            "mensaje_id": f'{x["mensaje"]["grupo"]}:{int(x["mensaje"]["id"])}' if url_mensaje(x.get("mensaje")) else None,
            "fuentes": [{"titulo": f.get("titulo", ""), "url": f["url"]} for f in x.get("fuentes") or [] if f.get("url")],
            "url": BASE + ruta, "url_ca": BASE + IDIOMAS["ca"]["carpeta"] + ruta})

    for d in eds:
        for p in d["piezas"]:
            poner(d, "pieza", f'{d["fecha"]}/{p["id"]}.html', p, p.get("cuerpo") or [], p.get("seccion"))
        for b in d.get("breves", []):
            poner(d, "breve", ruta_breve(b), dict(b, titular=titulo_breve(b),
                  fuentes=[{"titulo": "", "url": b["url"]}] if b.get("url") else []), [b.get("texto", "")])
        if d.get("reportaje"):
            r = d["reportaje"]
            parrafos = [t for a in r.get("apartados", []) for t in [a.get("ladillo", "")] + a.get("parrafos", [])]
            poner(d, "reportaje", f'{d["fecha"]}/{r["id"]}.html', r, parrafos + r.get("claves", []))
        if d.get("editorial"):
            ed = d["editorial"]
            poner(d, "editorial", f'{d["fecha"]}/{ed["id"]}.html', ed, ed.get("cuerpo") or [])
    return json.dumps({"generado": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                       "ultimo_numero": eds[-1]["numero"], "hemeroteca": BASE + "archivo.html",
                       "entradas": entradas}, ensure_ascii=False, indent=1) + "\n"


def escribir(ruta, texto):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto)


def generar_idioma(codigo):
    global L, ULTIMA
    L = IDIOMAS[codigo]
    base = SITIO / L["carpeta"]
    eds = cargar()
    ULTIMA = eds[-1]["fecha"]
    PIEZAS.clear()
    for d in eds:
        PIEZAS.update((d["fecha"], x["id"]) for x in d["piezas"] + [d[k] for k in ("reportaje", "editorial") if d.get(k)])
    piezas, breves = seleccion_portada(eds)
    escribir(base / "index.html",
             pagina_portada("", "", eds, piezas, breves, eds[-1]["fecha"], eds[-1]["numero"], True))
    escribir(base / "redaccion.html", pagina_redaccion(eds))
    escribir(base / "que-es.html", redireccion("redaccion.html"))
    escribir(base / "comunidad.html", redireccion("vibecoding.html"))   # la sección retirada el 01-11-2026
    for clave in ORDEN_SECCIONES:
        escribir(base / f"{clave}.html", pagina_seccion(eds, clave))
    escribir(base / "vineta.html", pagina_vinetas(eds))
    escribir(base / "videos.html", pagina_videos(eds))
    escribir(base / "reportajes.html", pagina_reportajes(eds))
    escribir(base / "breves.html", pagina_breves(eds))
    escribir(base / "buscar.html", pagina_buscar(eds))
    escribir(base / "archivo.html", pagina_hemeroteca(eds))
    escribir(base / "feed.xml", rss(eds))
    escribir(base / "manifest.webmanifest", manifiesto())
    if codigo == "es":
        escribir(RAIZ / "indice" / "diario.json", indice_bot(eds))   # para el bot, no se publica (ADR 0017)
        escribir(SITIO / "404.html", pagina_404(eds))
        escribir(SITIO / "sitemap.xml", sitemap(eds))
    for i, d in enumerate(eds):
        dia = base / d["fecha"]
        escribir(dia / "index.html",
                 pagina_portada("../", f'{d["fecha"]}/', eds, d["piezas"], d.get("breves", []), d["fecha"],
                                d["numero"], False, nav_dia("../", eds, i)))
        for p in d["piezas"]:
            escribir(dia / f'{p["id"]}.html', articulo("../", f'{d["fecha"]}/{p["id"]}.html', d, p, eds))
        for b in d.get("breves", []):
            escribir(base / ruta_breve(b), pagina_breve("../", d, b, eds))
        if d.get("reportaje"):
            r = d["reportaje"]
            escribir(dia / f'{r["id"]}.html', articulo_reportaje("../", f'{d["fecha"]}/{r["id"]}.html', d, r, eds))
        if d.get("editorial"):
            ed = dict(d["editorial"], fecha=d["fecha"])
            escribir(dia / f'{ed["id"]}.html', articulo("../", f'{d["fecha"]}/{ed["id"]}.html', d, ed, eds))
    print(f"{codigo}: {len(eds)} días, {sum(len(d['piezas']) for d in eds)} piezas; portada con {len(piezas)} piezas y {len(breves)} breves")


def main():
    # Los archivos fijos (estilos, fuentes, iconos, imágenes para redes) viven en estaticos/;
    # sitio/ no está en el repositorio y se rehace entero cada vez.
    SITIO.mkdir(exist_ok=True)
    shutil.copytree(RAIZ / "estaticos", SITIO, dirs_exist_ok=True)
    shutil.rmtree(SITIO / "capturas", ignore_errors=True)
    if (RAIZ / "repositorio" / "capturas").exists():   # las capturas de los recursos, para los dos idiomas (ADR 0008)
        shutil.copytree(RAIZ / "repositorio" / "capturas", SITIO / "capturas", dirs_exist_ok=True)
    # Sin restos de piezas retiradas ni de la maqueta descartada
    for viejo in [SITIO / "diario", SITIO / "revista", SITIO / "revista.css", SITIO / "ca"] + \
            [p for p in SITIO.iterdir() if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)]:
        if viejo.is_dir():
            shutil.rmtree(viejo)
        elif viejo.exists():
            viejo.unlink()
    shutil.rmtree(SITIO / "videos", ignore_errors=True)
    if (RAIZ / "videos").exists():   # los vídeos y sus portadas, para los dos idiomas (ADR 0016)
        (SITIO / "videos").mkdir()
        for f in (RAIZ / "videos").iterdir():
            if f.suffix in (".mp4", ".jpg"):
                shutil.copy(f, SITIO / "videos" / f.name)
    if (RAIZ / "og" / "numeros").exists():   # la imagen de vista previa de cada número (ADR 0010)
        shutil.copytree(RAIZ / "og" / "numeros", SITIO / "og", dirs_exist_ok=True)
    for codigo in IDIOMAS:
        generar_idioma(codigo)


if __name__ == "__main__":
    main()
