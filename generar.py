#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Genera la web del «Diario de IA Educativa» a partir de las ediciones, en castellano
(raíz del sitio) y traducida al catalán, gallego, euskera e inglés (carpetas ca/, gl/, eu/ y en/, ADR 0026). Sin dependencias: solo la biblioteca estándar.

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
DIAS_PORTADA = 7        # los breves y el reportaje de la portada, de esta última semana
POR_SECCION = 3         # piezas de días anteriores en el bloque de cada sección de la portada: una fila entera
MAX_BREVES = 3
MAQUETA = "diario"
# Dirección pública del sitio, para los enlaces absolutos del RSS y de la vista previa al compartir
BASE = os.environ.get("PERIODICO_BASE", "https://diarioiaeducativa.github.io/")
ORDEN_SECCIONES = ["herramientas", "vibecoding", "multimedia", "debates", "novedades", "biblioteca"]
SECCIONES_FUERA = ["hace-un-ano"]   # con su página, pero sin entrada en el menú: se llega desde el número y el pie (ADR 0040)
# «La redacción» en columnas (ADR 0047): los apartados de `secciones`, por su posición, en bloques por tema:
# cómo trabajan los agentes; las secciones del diario; quién lo lee y quién lo hace. El último empieza por las
# comunidades, con su diagrama arriba de la primera columna: en medio, al no poder partirse, dejaba un hueco
# al pie de la última. Mismo orden en los cinco idiomas.
BLOQUES_REDACCION = ((0, 1, 2), (3, 4, 5, 6, 7), (11, 12, 8, 9, 10, 13))
TODAS_SECCIONES = ORDEN_SECCIONES + SECCIONES_FUERA
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

# Idiomas: castellano en la raíz y los demás en su carpeta (ca/, gl/, eu/, en/; ADR 0026). El contenido
# traducido vive en ediciones-XX/, ilustraciones-XX/, vinetas-XX/…; si falta algo, se usa el original.
# Los textos de la web en gallego, euskera e inglés están en idiomas_web.py.
IDIOMAS = {
    "es": {
        "codigo": "es", "locale": "es_ES",
        "carpeta": "", "sufijo": "", "nombre": "Castellano", "titulo": "Diario de IA Educativa",
        "edicion": "Edición en castellano",
        "lema": "La inteligencia artificial, contada desde tres comunidades docentes",
        "dias": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
        "meses": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                  "septiembre", "octubre", "noviembre", "diciembre"],
        "secciones": {"herramientas": "Herramientas", "vibecoding": "Vibe coding", "multimedia": "Multimedia",
                      "debates": "Debates", "novedades": "Instituciones y empresas", "biblioteca": "Biblioteca", "hace-un-ano": "Hace un año"},
        "actualizado": "Actualizado el", "num": "Núm.", "numero_largo": "Número",
        "tema": "Cambiar entre tema claro y oscuro", "navegacion": "Navegación",
        "contacto": {"titulo": "Contacto", "enlace": "página de contacto", "txt": "Para avisar de un error, pedir que se retire algo o hacer cualquier consulta sobre el diario o su app.", "correo": "Correo", "otras": "También se puede abrir una incidencia en {incidencias} o escribir a las personas que administran cada grupo."},
        "quees": "La redacción", "portada": "Portada", "volver": "Volver a la portada",
        "dia_ant": "Día anterior", "dia_sig": "Día siguiente",
        "leer_conv": "Lee la conversación original en", "tema_en": "Tema tratado en",
        "comprobado": "Comprobado en", "fuente": "Fuente", "conversacion": "Conversación", "comentarios": "Comentarios", "comentarios_aviso": "Para comentar hace falta una {cuenta}. Los comentarios son públicos y se guardan en GitHub.", "comentarios_cuenta": "cuenta gratuita de GitHub",
        "breves": "Breves", "breves_antes": "Breves anteriores", "vineta": "La viñeta", "vineta_titulo": "La viñeta de Tiza y Algoritmo", "nombre_tiza": "Tiza", "nombre_algoritmo": "Algoritmo", "y": "y",
        "a_partir": "A partir de",
        "a_partir_dia": "A partir de las noticias del día.",
        "unete": "Únete a la conversación",
        "grupos_desc": {"chatgpt": "uso general de la inteligencia artificial en educación: experiencias, herramientas y recursos.",
                        "vce": "creación de recursos digitales educativos usando el lenguaje natural.",
                        "edumedia": "creación de audio, vídeo e imagen con IA generativa para el aula."},
        "unete_txt": "El Diario de IA Educativa cuenta lo que se habla en tres grupos abiertos de Telegram donde docentes comparten lo que prueban con la inteligencia artificial. Las conversaciones se pueden leer sin entrar; para participar, basta con unirse.",
        "archivo": "Archivo por días", "pie_archivo": "Archivo", "pie_diario": "El diario", "este_numero": "este número",
        "anyo": "Año", "hemeroteca": "Hemeroteca", "hemeroteca_txt": "Todos los números, por meses y semanas.", "nb_anteriores": "Boletines anteriores", "semana_n": "Semana {n}",
        "dias_cortos": ["L", "M", "X", "J", "V", "S", "D"], "calendario": "Calendario de los números", "cal_anterior": "Mes anterior", "cal_siguiente": "Mes siguiente", "cal_elegir": "Elige el mes", "buscar_numeros": "Busca en todos los números", "cal_portada": "Portada: {fecha}", "cal_resumenes": "Resumen de cada semana", "cal_resumen": "Resumen de la semana {n}",
        # La semana y el mes (ADR 0034)
        "semana": "La semana", "semana_txt": "Todo lo que contó el diario de lo que se habló en los grupos esa semana, por secciones, con el pódcast y el vídeo de cada grupo. Elige un grupo para ver solo lo suyo.", "semana_actual": "Resumen semanal", "grupo_filtro": "Ver lo de un grupo", "grupo_todos": "Todos", "sin_grupo": "Este grupo no tiene piezas esta semana.", "nb_h": "El pódcast y el vídeo de la semana", "nb_txt": "Cada lunes, NotebookLM, de Google, prepara un pódcast y un vídeo de cada grupo con su conversación completa de la semana, también lo que el diario no ha contado. Un agente de IA los contrasta con la conversación antes de publicarlos.", "nb_es": "", "nb_pendiente": "El pódcast y el vídeo de cada grupo se añaden aquí el lunes por la mañana.", "nb_video": "Vídeo", "nb_ver": "Reproducir el vídeo de {g}", "nb_youtube": "Verlo en YouTube", "nb_podcast": "Pódcast", "nb_archive": "Escucharlo en Internet Archive", "cs_h": "Lo más importante de la semana", "cs_h_g": "Lo más importante de la semana en {g}", "cs_nota": "Lo escribe un agente de IA con lo que contó el diario esa semana, y otro lo contrasta con cada pieza antes de publicarlo.", "numeros_semana": "Los números de la semana", "sem_ant": "Semana anterior", "sem_sig": "Semana siguiente", "todo_mes": "Todo el mes", "mes": "El mes", "mes_txt": "Las semanas del mes, con la pieza que abrió cada número.", "mes_ant": "Mes anterior", "mes_sig": "Mes siguiente", "por_meses": "Por meses", "ver_semana": "La semana entera, por secciones", "con_nb": "Con el pódcast y el vídeo de cada grupo", 
        "todos_numeros": "Hemeroteca: todos los números",
        "compartir": "Compartir", "copiado": "Enlace copiado", "una_columna": "Una columna", "columnas": "Columnas", "una_columna_t": "Leer las noticias en una sola columna", "columnas_t": "Leer las noticias en columnas, como en un periódico", "compartir_breve": "Compartir este breve", "mas_en": "Más en", "mas_diario": "Más en el diario",
        "no_existe": "Esta página no existe",
        "sin_conexion": "Sin conexión",
        "sin_conexion_txt": "Esta página no está guardada en este dispositivo. Sin conexión se pueden leer las páginas que ya se han abierto y el último número que se cargó en la portada.",
        "no_existe_txt": "Puede que el enlace esté mal escrito o que la pieza se haya retirado. La portada de hoy y la hemeroteca siguen ahí.",
        "redactado": "Redactado con IA a partir de las conversaciones de los grupos. Cada dato se comprueba en su fuente original, enlazada al final de cada pieza; las opiniones de los miembros no se atribuyen a nadie.",
        "licencia": "Textos e ilustraciones con licencia", "deed": "deed.es", "reserva_aviso": "Hoy no han podido salir las noticias de los grupos de ayer por un fallo de la redacción del diario. Salen mañana, junto con las de hoy; mientras tanto, un recurso del fondo del repositorio.", "vcer": "Evaluación VCER: Recomendable (100 %), noviembre de 2026", "codigo_enlace": "el repositorio de la redacción",
        "letra": "Letra", "iconos": "Iconos", "traduccion": "",
        "idioma": "Idioma", "secciones_nav": "Secciones", "rss": "RSS",
        "nombre_corto": "Diario IA", "instalar": "Instalar la app", "avisos_app": "Avisos del número", "avisos_app_titulo": "Elige si la app te avisa cada mañana cuando sale el número",
        "instalar_titulo": "Instala el diario en este dispositivo y ábrelo desde su icono, como una app",
        "instalar_ios": "En el iPhone o el iPad, el diario se puede tener como una app: añádelo a la pantalla de inicio desde el botón de compartir del navegador.",
        "sin_piezas": "Todavía no hay piezas en esta sección.",
        "leer_presentacion": "Leer la presentación", "presentacion": "Cómo se hace este diario: la presentación del número 1",
        "sin_vinetas": "Todavía no hay viñetas.",
        "descripciones": {
            "hace-un-ano": "Cada día, algo que se hablaba en los grupos el mismo día del año anterior, contado desde hoy: lo que ha cambiado, lo que ya no existe y lo que el tiempo ha resuelto.",
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
        "reportaje": "El reportaje del domingo", "reportajes": "Reportajes", "leer_reportaje": "Leer el reportaje", "leer_hace_un_ano": "Leer cómo ha cambiado",
        "claves": "Claves", "en_el_diario": "En el diario esta semana", "semana_repo": "Cada sábado, el diario repasa los recursos que han entrado durante la semana en el {repositorio} de Vibe Coding Educativo, la colección de aplicaciones y materiales con licencia abierta que crea y comparte el profesorado de esa comunidad.", "ya_contados": "Ya contados en el diario", "otras_semanas": "Otras semanas del repositorio", "sin_reportajes": "Todavía no hay reportajes.",
        "reportajes_txt": "Cada domingo, un tema de la semana tratado a fondo.", "palabras": "minutos de lectura",
        "redaccion": {
            "intro": "El Diario de IA Educativa lo escribe una redacción de agentes de inteligencia artificial, cada uno con su oficio, que se revisan entre ellos. Lo idean, lo diseñan y lo supervisan personas, y sale cada mañana a las 7:00 en castellano, y traducido al catalán, al gallego, al euskera y al inglés.",
            "proceso_titulo": "Cómo se hace cada número", "pagina_semana": "página",
            "proceso_intro": "Cada número cuenta lo que se habló el día anterior en los tres grupos. La redacción trabaja de madrugada, con el día ya cerrado, y sigue siempre el mismo orden.",
            "proceso": [
                "A la 1:00, un programa recoge los mensajes del día en los tres grupos y los ordena por grupo y por tema. En este paso no interviene la inteligencia artificial.",
                "El redactor elige los temas que pueden interesar fuera de los grupos y escribe las piezas, comprobando cada dato en su fuente original. Después, el revisor vuelve a abrir cada fuente y quita lo que no puede confirmar.",
                "El ilustrador dibuja cada pieza mientras el guionista escribe cinco guiones para la viñeta. Un programa abre cada dibujo en su página, en tema claro y oscuro, y mide sus colores, su contraste y sus rótulos; después, el revisor de dibujos mira el resultado y devuelve al ilustrador lo que no se ve bien. El juez de humor elige el mejor guion y un programa dibuja la viñeta.",
                "Si ese día ha entrado algún documento en la {biblioteca} de ChatGPT-IA-edu, el documentalista escribe su artículo y el revisor lo contrasta con el documento. Cada día, el documentalista escribe además sobre hasta dos recursos del {repositorio} de Vibe Coding Educativo que el diario aún no ha contado, y el sábado repasa los que han entrado en la semana. La noche del sábado se preparan, además, el reportaje y «La semana en vídeo» del domingo.",
                "Además, el cronista busca en los mensajes de hace un año justo un tema que muestre cuánto ha cambiado todo y escribe «Hace un año», que un verificador contrasta y el ilustrador dibuja. La noche del domingo, el comentarista escribe lo más importante de la semana.",
                "El traductor prepara las ediciones en catalán, gallego, euskera e inglés, y el portavoz escribe el mensaje que recibirá cada grupo.",
                "Un programa monta la web con todo lo anterior y la publica a las 6:50. A las 7:00, el bot de los grupos publica el aviso en cada uno de ellos.",
            ],
            "proceso_pie": "Cuando un paso falla o una revisión no da algo por bueno, esa parte se queda fuera y el número sale igual. No hay ningún día sin número: si falla la redacción entera, sale con un artículo de reserva, escrito y revisado otro día, que se retira si no se usa en dos meses (el reportaje, en cuatro semanas) y cuyas fuentes se comprueban antes de publicarlo, y las noticias de los grupos de ese día salen al siguiente; si el servidor de la redacción no ha publicado a las 9:10, un vigilante que funciona fuera de él saca el número con esa reserva. La persona que supervisa la redacción recibe un aviso en cada caso.",
            "equipo_titulo": "El equipo",
            "organigrama_alt": "Organigrama de la redacción, en el que los agentes de IA van en cajas rellenas y los mensajes y lo publicado, solo con contorno: cada día, los mensajes de los grupos pasan del redactor al revisor, y los documentos de la Biblioteca digital y los recursos del repositorio, del documentalista al revisor. Del revisor salen dos caminos: el guionista y el juez de humor preparan la viñeta, y el ilustrador dibuja lo que explica cada noticia, con el revisor de dibujos, que le devuelve lo que no se ve bien. Todo acaba en el traductor, y el número sale a las 7:00 con un aviso del portavoz para cada grupo. Cada noche, además, el cronista busca en los mensajes de hace un año un tema que muestre cuánto ha cambiado todo y escribe «Hace un año», que contrasta un verificador y que pasa también por el ilustrador, el revisor de dibujos y el traductor. Los domingos, el jefe de reportajes, el reportero y el verificador preparan el reportaje, que pasa también por el ilustrador, el revisor de dibujos y el traductor; si hay uno de reserva, el juez de reportajes elige el mejor de los dos, y sale dentro del número. Además, el guionista de vídeo escribe «La semana en vídeo» con los números de la semana y el reportaje, y el vídeo sale en el número del domingo y, con el reportaje, a las 9:00 en las redes sociales. La noche del domingo, el comentarista escribe lo más importante de la semana a partir de sus números, un revisor lo contrasta y el traductor lo prepara en los otros idiomas para el resumen semanal.",
            "equipo": [
                ("Redactor", "lee las conversaciones del día de los tres grupos, elige lo que puede interesar a las personas que no están en ellos y escribe las piezas, comprobando cada dato en su fuente original."),
                ("Revisor", "no ha escrito nada: vuelve a abrir cada fuente, compara las piezas con los mensajes y quita lo que no puede confirmar. Hace lo mismo con los artículos de la Biblioteca, contra el propio documento."),
                ("Documentalista", "cuando entra un documento en la Biblioteca digital de ChatGPT-IA-edu, lo lee en su fuente oficial y escribe un artículo sobre él. También escribe sobre los recursos del Repositorio de Vibe Coding Educativo, a partir del propio recurso y de una captura que hace un programa al abrirlo."),
                ("Ilustrador", "dibuja lo que explica cada noticia y, los domingos, la infografía del reportaje."),
                ("Revisor de dibujos", "mira cada dibujo en su página, en tema claro y oscuro, y se lo devuelve al ilustrador si algo no se ve bien o no explica la noticia. Antes, un programa mide lo que se puede medir: colores, contraste y rótulos que se salen o se pisan."),
                ("Guionista", "escribe cinco guiones de la viñeta con Tiza y Algoritmo, sus dos personajes."),
                ("Juez de humor", "elige el mejor y lo afina, sin haberlos escrito."),
                ("Traductor", "prepara las ediciones en catalán, gallego, euskera e inglés."),
                ("Portavoz", "escribe cada mañana el aviso con el que el diario se presenta en cada grupo, distinto para cada uno."),
                ("Jefe de reportajes", "los domingos elige el tema de la semana que merece un reportaje, su enfoque y a quién hay que consultar."),
                ("Reportero", "investiga ese tema fuera de los grupos, en los documentos de las empresas, las administraciones y los organismos implicados, y escribe el reportaje."),
                ("Verificador", "no ha escrito nada: abre cada fuente del reportaje y quita lo que no puede confirmar."),
                ("Juez de reportajes", "cuando hay un reportaje de reserva, compara el nuevo con él sin haber escrito ninguno de los dos y elige el mejor para publicarlo."),
                ("Guionista de vídeo", "los sábados por la noche elige lo más destacado de la semana, como mínimo una pieza de cada número, y escribe los textos de «La semana en vídeo» en los cinco idiomas, con el reportaje del domingo como última escena, y el texto que lo acompaña en las redes. Un programa comprueba que no falte ningún día y que los textos quepan, y monta el vídeo con los dibujos del diario."),
                ("Cronista", "cada noche busca en los mensajes de los grupos de hace un año justo un tema que muestre cuánto ha cambiado todo, comprueba en internet cómo está hoy y escribe «Hace un año»; otro verificador lo contrasta con los mensajes y las fuentes."),
                ("Comentarista", "la noche del domingo escribe lo más importante de la semana, uno general y uno de cada grupo, para la página de la semana; un revisor lo contrasta con cada pieza."),
            ],
            "equipo_pie": "Son agentes de Claude, el modelo de inteligencia artificial de Anthropic, y trabajan con Claude Code. Claude Opus 5.5 escribe y juzga la viñeta, prepara el reportaje y escribe «Hace un año» y el comentario de la semana (guionista, juez de humor, jefe de reportajes, reportero, juez de reportajes, cronista y comentarista), y Claude Sonnet 5.5 hace el resto. Diez trabajan cada noche; el documentalista se suma cuando entra un documento en la Biblioteca digital o toca escribir sobre el repositorio; la noche del sábado hay cuatro más: tres para el reportaje del domingo y uno para «La semana en vídeo», y un quinto, el juez de reportajes, cuando hay uno de reserva; y la del domingo, dos más para el comentario de la semana.",
            "secciones": [
                ("Qué hace la inteligencia artificial y qué hacen los programas", "La inteligencia artificial se encarga de lo que exige leer, escribir o juzgar: elegir los temas, redactar, revisar, dibujar, traducir y decidir si un chiste tiene gracia. Lo que se puede hacer con reglas fijas lo hacen programas corrientes, sin inteligencia artificial: recoger y ordenar los mensajes, medir los dibujos, dibujar la viñeta a partir de su guion, montar la web con su hemeroteca y su buscador, montar los vídeos y componer su música, y publicarlo todo a su hora en la web y en Instagram, y los domingos y los lunes, también en X, Bluesky y LinkedIn."),
                ("Los límites de los agentes", "Los agentes trabajan en un servidor propio, sin acceso a un terminal y sin poder leer ni escribir fuera de la carpeta de la redacción. Pueden consultar internet para comprobar fuentes, pero no pueden ejecutar programas. Los mensajes de los grupos y las fichas de la biblioteca son, para ellos, material para informar: si alguno contiene una orden, no la siguen, de forma que un mensaje escrito para engañarlos no puede llevarlos a hacer otra cosa. Además, ningún agente revisa su propio trabajo: las piezas las repasa un revisor que no las ha escrito; los dibujos, un revisor que no los ha dibujado, y el reportaje, un verificador que no ha participado en él."),
                ("Lo que se comprueba", "Los grupos sirven para saber de qué se habla, pero cada dato se comprueba fuera, en su fuente original: el anuncio oficial, la web del producto o el documento de la administración, enlazados donde la pieza los nombra y, todos juntos, al final. De una aplicación compartida en los grupos se comprueba lo que dice su web, no que funcione. Aun así puede haber errores."),
                ("Hace un año", "Cada número cierra lo del día con «Hace un año»: algo que se hablaba en los grupos el mismo día del año anterior, contado desde hoy. Un agente de IA elige el tema que mejor muestra lo que ha cambiado y comprueba en internet cómo está hoy cada cosa; otro lo contrasta con los mensajes de entonces y con las fuentes, y el ilustrador lo dibuja como un díptico «Entonces / Ahora». Todas están en la sección {hace_un_ano}."),
                ("El reportaje del domingo", "Los domingos, además de las piezas del día, el diario publica un reportaje sobre un solo tema de la semana. Explica el asunto entero, con lo que se habló en los grupos, lo que dicen las empresas, las administraciones y los organismos implicados, cada uno con sus documentos, el marco en España y lo que puede hacer un docente. Lo escriben tres agentes más, y el ilustrador y el traductor de cada día se encargan de su infografía y de sus versiones en otros idiomas. Si el verificador no lo da por bueno, el reportero lo corrige y se verifica otra vez; si aun así no sale, ese domingo se publica un reportaje de reserva, escrito y verificado otro día sobre un tema que no caduca. Cuando hay uno de reserva, un juez de reportajes, que no ha escrito ninguno de los dos, elige el mejor para publicarlo. Todos quedan en la sección {reportajes}."),
                ("La semana", "Cada semana tiene su {pagina_semana}, con todas las piezas por secciones y los números que la forman, y cada mes tiene la suya; la {hemeroteca} se recorre por meses y semanas. Los lunes por la mañana se añaden a la semana un pódcast y un vídeo de cada grupo, que prepara NotebookLM, de Google, con la conversación completa de la semana, también lo que el diario no ha contado. Un agente de IA que no los ha hecho los contrasta con la conversación, y el que tiene errores de bulto se vuelve a generar. Se avisa en cada grupo y el vídeo sale también en X, Bluesky y LinkedIn. Debajo va lo más importante de la semana: un comentario general y uno de cada grupo, que escribe un agente de IA la noche del domingo con lo que contó el diario y que otro contrasta con cada pieza."),
                ("La Biblioteca digital", "Cada documento que entra en la {biblioteca} de ChatGPT-IA-edu (guías, informes, estudios) tiene su artículo en la sección {seccion_bib}; si el diario ya lo había contado como noticia, esa pieza pasa a la sección en lugar de escribir otra. El documentalista lee el documento entero y explica quién lo publica, qué propone y cómo encaja con otros documentos de la biblioteca; el revisor lo contrasta con el propio documento. El diario enlaza el documento en su fuente oficial y en la biblioteca, sin copiarlo. Se nombra a sus autores; la persona que lo ha compartido no se nombra, igual que no se atribuyen las opiniones de los grupos."),
                ("El Repositorio de recursos", "El {repositorio} de Vibe Coding Educativo reúne las aplicaciones y recursos que crean y comparten con licencia abierta los docentes de esa comunidad. Cada día, el documentalista escribe sobre hasta dos de los que han entrado y el diario aún no ha contado, y el número del sábado repasa los de la semana; si no hay ninguno nuevo y el número se queda corto, rescata uno anterior. Un programa abre cada recurso y guarda una captura de lo que se ve; el documentalista lo describe a partir de la captura y de su página, y el revisor lo vuelve a abrir. Salen en la sección {seccion_vc}, con el nombre de quien lo ha hecho y su licencia."),
                ("Las personas", "La idea del diario es de {raul}, administrador de {edumedia}. La redacción la diseñó y la supervisa {juanjo}."),
                ("El código", "Los programas que preparan y montan el diario y el encargo de cada agente son públicos, en {codigo}, con licencia AGPL v3, y cada decisión está explicada en sus registros de decisiones (ADR). Los mensajes de los grupos no están en él."),
                ("Las visitas", "El diario cuenta cuántas visitas recibe y cuántas veces se abre cada página, para saber si llega a quien lo lee. No usa cookies ni guarda nada de quien lo lee: su navegador recuerda qué páginas ya ha contado, para no contarlas dos veces en la misma visita, y al servidor de los autores solo le llega la suma. Lo que el navegador recuerda para el contador se borra a los 13 meses, la duración que pone de ejemplo la {aepd} en su guía sobre medición de audiencia, y las visitas nuevas no lo alargan; el tema, el idioma y la lectura en columnas o en una columna que se eligen se recuerdan sin caducar. Las cifras se guardan por horas durante 25 meses como máximo, el plazo de esa misma guía; después queda solo el total de cada año. Solo las ven las dos personas que hacen el diario. Para poder leerlo sin conexión, el navegador guarda en el propio dispositivo una copia de las páginas abiertas y del último número; esa copia no sale de él. La app de Android es esta misma web y no recoge nada más. Los comentarios se publican con giscus en las Discussions de GitHub: para comentar hace falta una cuenta de GitHub, y GitHub guarda el comentario y el nombre de usuario con su propia política de privacidad. Quien no comenta no envía nada."),
                ("Las comunidades", "{chatgpt}, sobre inteligencia artificial en educación; {vce}, de docentes que programan sus propias aplicaciones con IA, y {edumedia}, sobre IA generativa para crear audio, vídeo e imagen. Las tres son abiertas: cada pieza enlaza a la conversación donde nació, que se puede leer sin entrar."),
                ("Si participas en los grupos", "Las opiniones no se atribuyen a nadie: solo se nombra a la persona que ha publicado un recurso propio. Si aparece algo tuyo y prefieres que no salga, o ves un error, díselo a las personas que administran tu grupo y se retirará o se corregirá."),
                ("Contacto", "El correo y las demás vías para avisar de un error, pedir que se retire algo o hacer cualquier consulta están en la {pagina_contacto}."),
            ],
        },
    },
    "ca": {
        "codigo": "ca", "locale": "ca_ES",
        "carpeta": "ca/", "sufijo": "-ca", "nombre": "Català", "titulo": "Diari d'IA Educativa",
        "edicion": "Edició en català",
        "lema": "La intel·ligència artificial, explicada des de tres comunitats docents",
        "dias": ["dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte", "diumenge"],
        "meses": ["gener", "febrer", "març", "abril", "maig", "juny", "juliol", "agost",
                  "setembre", "octubre", "novembre", "desembre"],
        "secciones": {"herramientas": "Eines", "vibecoding": "Vibe coding", "multimedia": "Multimèdia",
                      "debates": "Debats", "novedades": "Institucions i empreses", "biblioteca": "Biblioteca", "hace-un-ano": "Fa un any"},
        "actualizado": "Actualitzat el", "num": "Núm.", "numero_largo": "Número",
        "tema": "Canviar entre tema clar i fosc", "navegacion": "Navegació",
        "contacto": {"titulo": "Contacte", "enlace": "pàgina de contacte", "txt": "Per avisar d'un error, demanar que es retiri alguna cosa o fer qualsevol consulta sobre el diari o la seva app.", "correo": "Correu", "otras": "També es pot obrir una incidència a {incidencias} o escriure a les persones que administren cada grup."},
        "quees": "La redacció", "portada": "Portada", "volver": "Torna a la portada",
        "dia_ant": "Dia anterior", "dia_sig": "Dia següent",
        "leer_conv": "Llegeix la conversa original a", "tema_en": "Tema tractat a",
        "comprobado": "Comprovat a", "fuente": "Font", "conversacion": "Conversa", "comentarios": "Comentaris", "comentarios_aviso": "Per comentar cal un {cuenta}. Els comentaris són públics i es desen a GitHub.", "comentarios_cuenta": "compte gratuït de GitHub",
        "breves": "Breus", "breves_antes": "Breus anteriors", "vineta": "La vinyeta", "vineta_titulo": "La vinyeta de Guix i Algorisme", "nombre_tiza": "Guix", "nombre_algoritmo": "Algorisme", "y": "i",
        "a_partir": "A partir de",
        "a_partir_dia": "A partir de les notícies del dia.",
        "unete": "Uneix-te a la conversa",
        "grupos_desc": {"chatgpt": "ús general de la intel·ligència artificial a l'educació: experiències, eines i recursos.",
                        "vce": "creació de recursos digitals educatius fent servir el llenguatge natural.",
                        "edumedia": "creació d'àudio, vídeo i imatge amb IA generativa per a l'aula."},
        "unete_txt": "El Diari d'IA Educativa explica el que es parla en tres grups oberts de Telegram on docents comparteixen el que proven amb la intel·ligència artificial. Les converses es poden llegir sense entrar-hi; per participar-hi, n'hi ha prou d'unir-s'hi.",
        "archivo": "Arxiu per dies", "pie_archivo": "Arxiu", "pie_diario": "El diari", "este_numero": "aquest número",
        "anyo": "Any", "hemeroteca": "Hemeroteca", "hemeroteca_txt": "Tots els números, per mesos i setmanes.", "nb_anteriores": "Butlletins anteriors", "semana_n": "Setmana {n}",
        "dias_cortos": ["dl.", "dt.", "dc.", "dj.", "dv.", "ds.", "dg."], "calendario": "Calendari dels números", "cal_anterior": "Mes anterior", "cal_siguiente": "Mes següent", "cal_elegir": "Tria el mes", "buscar_numeros": "Cerca a tots els números", "cal_portada": "Portada: {fecha}", "cal_resumenes": "Resum de cada setmana", "cal_resumen": "Resum de la setmana {n}",
        # La semana y el mes (ADR 0034)
        "semana": "La setmana", "semana_txt": "Tot el que va explicar el diari del que es va parlar als grups aquella setmana, per seccions, amb el pòdcast i el vídeo de cada grup. Tria un grup per veure només el seu.", "semana_actual": "Resum setmanal", "grupo_filtro": "Veure el d'un grup", "grupo_todos": "Tots", "sin_grupo": "Aquest grup no té peces aquesta setmana.", "nb_h": "El pòdcast i el vídeo de la setmana", "nb_txt": "Cada dilluns, NotebookLM, de Google, prepara un pòdcast i un vídeo de cada grup amb tota la seva conversa de la setmana, també el que el diari no ha explicat. Un agent d'IA els contrasta amb la conversa abans de publicar-los.", "nb_es": "Són en castellà.", "nb_pendiente": "El pòdcast i el vídeo de cada grup s'afegeixen aquí dilluns al matí.", "nb_video": "Vídeo", "nb_ver": "Reproduir el vídeo de {g}", "nb_youtube": "Mira'l a YouTube", "nb_podcast": "Pòdcast", "nb_archive": "Escolta'l a Internet Archive", "cs_h": "El més important de la setmana", "cs_h_g": "El més important de la setmana a {g}", "cs_nota": "L'escriu un agent d'IA amb el que va explicar el diari aquella setmana, i un altre el contrasta amb cada peça abans de publicar-lo.", "numeros_semana": "Els números de la setmana", "sem_ant": "Setmana anterior", "sem_sig": "Setmana següent", "todo_mes": "Tot el mes", "mes": "El mes", "mes_txt": "Les setmanes del mes, amb la peça que va obrir cada número.", "mes_ant": "Mes anterior", "mes_sig": "Mes següent", "por_meses": "Per mesos", "ver_semana": "Tota la setmana, per seccions", "con_nb": "Amb el pòdcast i el vídeo de cada grup", 
        "todos_numeros": "Hemeroteca: tots els números",
        "compartir": "Comparteix", "copiado": "Enllaç copiat", "una_columna": "Una columna", "columnas": "Columnes", "una_columna_t": "Llegir les notícies en una sola columna", "columnas_t": "Llegir les notícies en columnes, com en un diari", "compartir_breve": "Comparteix aquest breu", "mas_en": "Més a", "mas_diario": "Més al diari",
        "no_existe": "Aquesta pàgina no existeix",
        "sin_conexion": "Sense connexió",
        "sin_conexion_txt": "Aquesta pàgina no està desada en aquest dispositiu. Sense connexió es poden llegir les pàgines que ja s'han obert i l'últim número que es va carregar a la portada.",
        "no_existe_txt": "Pot ser que l'enllaç estigui mal escrit o que la peça s'hagi retirat. La portada d'avui i l'hemeroteca continuen aquí.",
        "redactado": "Redactat amb IA a partir de les converses dels grups. Cada dada es comprova a la seva font original, enllaçada al final de cada peça; les opinions dels membres no s'atribueixen a ningú.",
        "licencia": "Textos i il·lustracions amb llicència", "deed": "deed.ca", "reserva_aviso": "Avui no han pogut sortir les notícies dels grups d'ahir per una fallada de la redacció del diari. Surten demà, juntament amb les d'avui; mentrestant, un recurs del fons del repositori.", "vcer": "Avaluació VCER: Recomanable (100 %), novembre de 2026", "codigo_enlace": "repositori de la redacció",
        "letra": "Lletra", "iconos": "Icones",
        "traduccion": "Traducció automàtica amb IA de l'edició en castellà (Diario de IA Educativa), sense revisió professional.",
        "idioma": "Idioma", "secciones_nav": "Seccions", "rss": "RSS",
        "nombre_corto": "Diari IA", "instalar": "Instal·la l'app", "avisos_app": "Avisos del número", "avisos_app_titulo": "Tria si l'app t'avisa cada matí quan surt el número",
        "instalar_titulo": "Instal·la el diari en aquest dispositiu i obre'l des de la seva icona, com una app",
        "instalar_ios": "A l'iPhone o l'iPad, el diari es pot tenir com una app: afegeix-lo a la pantalla d'inici des del botó de compartir del navegador.",
        "sin_piezas": "Encara no hi ha peces en aquesta secció.",
        "leer_presentacion": "Llegeix la presentació", "presentacion": "Com es fa aquest diari: la presentació del número 1",
        "sin_vinetas": "Encara no hi ha vinyetes.",
        "descripciones": {
            "hace-un-ano": "Cada dia, alguna cosa que es parlava als grups el mateix dia de l'any anterior, explicada des d'avui: el que ha canviat, el que ja no existeix i el que el temps ha resolt.",
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
        "reportaje": "El reportatge del diumenge", "reportajes": "Reportatges", "leer_reportaje": "Llegeix el reportatge", "leer_hace_un_ano": "Llegeix com ha canviat",
        "claves": "Claus", "en_el_diario": "Al diari aquesta setmana", "semana_repo": "Cada dissabte, el diari repassa els recursos que han entrat durant la setmana al {repositorio} de Vibe Coding Educativo, la col·lecció d'aplicacions i materials amb llicència oberta que crea i comparteix el professorat d'aquesta comunitat.", "ya_contados": "Ja explicats al diari", "otras_semanas": "Altres setmanes del repositori", "sin_reportajes": "Encara no hi ha reportatges.",
        "reportajes_txt": "Cada diumenge, un tema de la setmana tractat a fons.", "palabras": "minuts de lectura",
        "redaccion": {
            "intro": "El Diari d'IA Educativa l'escriu una redacció d'agents d'intel·ligència artificial, cadascun amb el seu ofici, que es revisen entre ells. L'ideen, el dissenyen i el supervisen persones, i surt cada matí a les 7.00 en castellà, i traduït al català, al gallec, al basc i a l'anglès.",
            "proceso_titulo": "Com es fa cada número", "pagina_semana": "pàgina",
            "proceso_intro": "Cada número explica el que es va parlar el dia anterior als tres grups. La redacció treballa de matinada, amb el dia ja tancat, i segueix sempre el mateix ordre.",
            "proceso": [
                "A la 1.00, un programa recull els missatges del dia dels tres grups i els ordena per grup i per tema. En aquest pas no hi intervé la intel·ligència artificial.",
                "El redactor tria els temes que poden interessar fora dels grups i escriu les peces, comprovant cada dada a la seva font original. Després, el revisor torna a obrir cada font i treu el que no pot confirmar.",
                "L'il·lustrador dibuixa cada peça mentre el guionista escriu cinc guions per a la vinyeta. Un programa obre cada dibuix a la seva pàgina, en tema clar i fosc, i en mesura els colors, el contrast i els rètols; després, el revisor de dibuixos mira el resultat i torna a l'il·lustrador el que no es veu bé. El jutge d'humor tria el millor guió i un programa dibuixa la vinyeta.",
                "Si aquell dia ha entrat algun document a la {biblioteca} de ChatGPT-IA-edu, el documentalista n'escriu l'article i el revisor el contrasta amb el document. Cada dia, el documentalista escriu a més sobre fins a dos recursos del {repositorio} de Vibe Coding Educativo que el diari encara no ha explicat, i el dissabte repassa els que hi han entrat durant la setmana. La nit del dissabte es preparen, a més, el reportatge i «La setmana en vídeo» del diumenge.",
                "A més, el cronista busca als missatges de fa just un any un tema que mostri quant ha canviat tot i escriu «Fa un any», que un verificador contrasta i l'il·lustrador dibuixa. La nit del diumenge, el comentarista escriu el més important de la setmana.",
                "El traductor prepara les edicions en català, gallec, basc i anglès, i el portaveu escriu el missatge que rebrà cada grup.",
                "Un programa munta el web amb tot l'anterior i el publica a les 6.50. A les 7.00, el bot dels grups publica l'avís a cadascun.",
            ],
            "proceso_pie": "Quan un pas falla o una revisió no dona alguna cosa per bona, aquella part es queda fora i el número surt igualment. No hi ha cap dia sense número: si falla la redacció sencera, surt amb un article de reserva, escrit i revisat un altre dia, que es retira si no es fa servir en dos mesos (el reportatge, en quatre setmanes) i les fonts del qual es comproven abans de publicar-lo, i les notícies dels grups d'aquell dia surten l'endemà; si el servidor de la redacció no ha publicat a les 9.10, un vigilant que funciona fora d'ell treu el número amb aquesta reserva. La persona que supervisa la redacció rep un avís en cada cas.",
            "equipo_titulo": "L'equip",
            "organigrama_alt": "Organigrama de la redacció, en què els agents d'IA van en caixes plenes i els missatges i el que es publica, només amb contorn: cada dia, els missatges dels grups passen del redactor al revisor, i els documents de la Biblioteca digital i els recursos del repositori, del documentalista al revisor. Del revisor surten dos camins: el guionista i el jutge d'humor preparen la vinyeta, i l'il·lustrador dibuixa el que explica cada notícia, amb el revisor de dibuixos, que li torna el que no es veu bé. Tot acaba al traductor, i el número surt a les 7.00 amb un avís del portaveu per a cada grup. Cada nit, a més, el cronista busca als missatges de fa un any un tema que mostri quant ha canviat tot i escriu «Fa un any», que contrasta un verificador i que passa també per l'il·lustrador, el revisor de dibuixos i el traductor. Els diumenges, el cap de reportatges, el reporter i el verificador preparen el reportatge, que passa també per l'il·lustrador, el revisor de dibuixos i el traductor; si n'hi ha un de reserva, el jutge de reportatges tria el millor dels dos, i surt dins del número. A més, el guionista de vídeo escriu «La setmana en vídeo» amb els números de la setmana i el reportatge, i el vídeo surt al número del diumenge i, amb el reportatge, a les 9.00 a les xarxes socials. La nit del diumenge, el comentarista escriu el més important de la setmana a partir dels seus números, un revisor ho contrasta i el traductor ho prepara en els altres idiomes per al resum setmanal.",
            "equipo": [
                ("Redactor", "llegeix les converses del dia dels tres grups, tria el que pot interessar a les persones que no hi són i escriu les peces, comprovant cada dada a la seva font original."),
                ("Revisor", "no ha escrit res: torna a obrir cada font, compara les peces amb els missatges i treu el que no pot confirmar. Fa el mateix amb els articles de la Biblioteca, contra el mateix document."),
                ("Documentalista", "quan entra un document a la Biblioteca digital de ChatGPT-IA-edu, el llegeix a la font oficial i n'escriu un article. També escriu sobre els recursos del Repositori de Vibe Coding Educativo, a partir del mateix recurs i d'una captura que fa un programa en obrir-lo."),
                ("Il·lustrador", "dibuixa el que explica cada notícia i, els diumenges, la infografia del reportatge."),
                ("Revisor de dibuixos", "mira cada dibuix a la seva pàgina, en tema clar i fosc, i el torna a l'il·lustrador si alguna cosa no es veu bé o no explica la notícia. Abans, un programa mesura el que es pot mesurar: colors, contrast i rètols que surten del dibuix o es trepitgen."),
                ("Guionista", "escriu cinc guions de la vinyeta amb Guix i Algorisme, els seus dos personatges."),
                ("Jutge d'humor", "tria el millor i l'afina, sense haver-los escrit."),
                ("Traductor", "prepara aquesta edició en català a partir de la castellana, el Diario de IA Educativa."),
                ("Portaveu", "escriu cada matí l'avís amb què el diari es presenta a cada grup, diferent per a cadascun."),
                ("Cap de reportatges", "els diumenges tria el tema de la setmana que mereix un reportatge, el seu enfocament i a qui cal consultar."),
                ("Reporter", "investiga aquest tema fora dels grups, als documents de les empreses, les administracions i els organismes implicats, i escriu el reportatge."),
                ("Verificador", "no ha escrit res: obre cada font del reportatge i treu el que no pot confirmar."),
                ("Jutge de reportatges", "quan hi ha un reportatge de reserva, compara el nou amb aquell sense haver escrit cap dels dos i tria el millor per publicar-lo."),
                ("Guionista de vídeo", "els dissabtes a la nit tria el més destacat de la setmana, com a mínim una peça de cada número, i escriu els textos de «La setmana en vídeo» en les cinc llengües, amb el reportatge del diumenge com a darrera escena, i el text que l'acompanya a les xarxes. Un programa comprova que no hi falti cap dia i que els textos hi càpiguen, i munta el vídeo amb els dibuixos del diari."),
                ("Cronista", "cada nit busca als missatges dels grups de fa just un any un tema que mostri quant ha canviat tot, comprova a internet com està avui i escriu «Fa un any»; un altre verificador el contrasta amb els missatges i les fonts."),
                ("Comentarista", "la nit del diumenge escriu el més important de la setmana, un de general i un de cada grup, per a la pàgina de la setmana; un revisor el contrasta amb cada peça."),
            ],
            "equipo_pie": "Són agents de Claude, el model d'intel·ligència artificial d'Anthropic, i treballen amb Claude Code. Claude Opus 5.5 escriu i jutja la vinyeta, prepara el reportatge i escriu «Fa un any» i el comentari de la setmana (guionista, jutge d'humor, cap de reportatges, reporter, jutge de reportatges, cronista i comentarista), i Claude Sonnet 5.5 fa la resta. Cada nit en treballen deu; el documentalista s'hi suma quan entra un document a la Biblioteca digital o toca escriure sobre el repositori; la nit del dissabte n'hi ha quatre més: tres per al reportatge del diumenge i un per a «La setmana en vídeo», i un cinquè, el jutge de reportatges, quan n'hi ha un de reserva; i la del diumenge, dos més per al comentari de la setmana.",
            "secciones": [
                ("Què fa la intel·ligència artificial i què fan els programes", "La intel·ligència artificial s'encarrega del que demana llegir, escriure o jutjar: triar els temes, redactar, revisar, dibuixar, traduir i decidir si un acudit té gràcia. El que es pot fer amb regles fixes ho fan programes corrents, sense intel·ligència artificial: recollir i ordenar els missatges, mesurar els dibuixos, dibuixar la vinyeta a partir del guió, muntar el web amb l'hemeroteca i el cercador, muntar els vídeos i compondre'n la música, i publicar-ho tot a l'hora al web i a Instagram, i els diumenges i els dilluns, també a X, Bluesky i LinkedIn."),
                ("Els límits dels agents", "Els agents treballen en un servidor propi, sense accés a un terminal i sense poder llegir ni escriure fora de la carpeta de la redacció. Poden consultar internet per comprovar fonts, però no poden executar programes. Els missatges dels grups i les fitxes de la biblioteca són, per a ells, material per informar: si n'hi ha cap que contingui una ordre, no la segueixen, de manera que un missatge escrit per enganyar-los no els pot portar a fer una altra cosa. A més, cap agent no revisa la seva pròpia feina: les peces les repassa un revisor que no les ha escrites; els dibuixos, un revisor que no els ha dibuixat, i el reportatge, un verificador que no hi ha participat."),
                ("El que es comprova", "Els grups serveixen per saber de què es parla, però cada dada es comprova fora, a la seva font original: l'anunci oficial, el web del producte o el document de l'administració, enllaçats on la peça els anomena i, tots junts, al final. D'una aplicació compartida als grups es comprova el que diu el seu web, no que funcioni. Tot i així hi pot haver errors. Aquesta edició és una traducció automàtica de la castellana, sense revisió professional."),
                ("Fa un any", "Cada número tanca el del dia amb «Fa un any»: alguna cosa que es parlava als grups el mateix dia de l'any anterior, explicada des d'avui. Un agent d'IA tria el tema que millor mostra el que ha canviat i comprova a internet com està avui cada cosa; un altre el contrasta amb els missatges d'aleshores i amb les fonts, i l'il·lustrador el dibuixa com un díptic «Aleshores / Ara». Totes són a la secció {hace_un_ano}."),
                ("El reportatge del diumenge", "Els diumenges, a més de les peces del dia, el diari publica un reportatge sobre un sol tema de la setmana. Explica l'assumpte sencer, amb el que es va parlar als grups, el que diuen les empreses, les administracions i els organismes implicats, cadascun amb els seus documents, el marc a Espanya i el que pot fer un docent. L'escriuen tres agents més, i l'il·lustrador i el traductor de cada dia se n'encarreguen de la infografia i de les versions en altres llengües. Si el verificador no el dona per bo, el reporter el corregeix i es torna a verificar; si tot i així no surt, aquell diumenge es publica un reportatge de reserva, escrit i verificat un altre dia sobre un tema que no caduca. Quan n'hi ha un de reserva, un jutge de reportatges, que no n'ha escrit cap dels dos, tria el millor per publicar-lo. Tots queden a la secció {reportajes}."),
                ("La setmana", "Cada setmana té la seva {pagina_semana}, amb totes les peces per seccions i els números que la formen, i cada mes té la seva; l'{hemeroteca} es recorre per mesos i setmanes. Els dilluns al matí s'afegeixen a la setmana un pòdcast i un vídeo de cada grup, que prepara NotebookLM, de Google, amb tota la conversa de la setmana, també el que el diari no ha explicat. Un agent d'IA que no els ha fet els contrasta amb la conversa, i el que té errors greus es torna a generar. S'avisa a cada grup i el vídeo surt també a X, Bluesky i LinkedIn. Són en castellà. A sota hi ha el més important de la setmana: un comentari general i un de cada grup, que escriu un agent d'IA la nit del diumenge amb el que va explicar el diari i que un altre contrasta amb cada peça."),
                ("La Biblioteca digital", "Cada document que entra a la {biblioteca} de ChatGPT-IA-edu (guies, informes, estudis) té el seu article a la secció {seccion_bib}; si el diari ja l'havia explicat com a notícia, aquella peça passa a la secció en lloc d'escriure'n una altra. El documentalista llegeix el document sencer i explica qui el publica, què proposa i com encaixa amb altres documents de la biblioteca; el revisor el contrasta amb el mateix document. El diari enllaça el document a la font oficial i a la biblioteca, sense copiar-lo. S'anomenen els autors; la persona que l'ha compartit no s'anomena, igual que no s'atribueixen les opinions dels grups."),
                ("El Repositori de recursos", "El {repositorio} de Vibe Coding Educativo reuneix les aplicacions i els recursos que creen i comparteixen amb llicència oberta els docents d'aquesta comunitat. Cada dia, el documentalista escriu sobre fins a dos dels que hi han entrat i que el diari encara no ha explicat, i el número del dissabte repassa els de la setmana; si no n'hi ha cap de nou i el número es queda curt, en rescata un d'anterior. Un programa obre cada recurs i en guarda una captura del que es veu; el documentalista el descriu a partir de la captura i de la seva pàgina, i el revisor el torna a obrir. Surten a la secció {seccion_vc}, amb el nom de qui l'ha fet i la seva llicència."),
                ("Les persones", "La idea del diari és de {raul}, administrador d'{edumedia}. La redacció la va dissenyar i la supervisa {juanjo}."),
                ("El codi", "Els programes que preparen i munten el diari i l'encàrrec de cada agent són públics, al {codigo}, amb llicència AGPL v3, i cada decisió s'explica als seus registres de decisions (ADR). Els missatges dels grups no hi són."),
                ("Les visites", "El diari compta quantes visites rep i quantes vegades s'obre cada pàgina, per saber si arriba a qui el llegeix. No fa servir galetes ni desa res de qui el llegeix: el seu navegador recorda quines pàgines ja ha comptat, per no comptar-les dues vegades en la mateixa visita, i al servidor dels autors només hi arriba la suma. El que el navegador recorda per al comptador s'esborra al cap de 13 mesos, la durada que posa d'exemple l'{aepd} a la seva guia sobre mesurament d'audiència, i les visites noves no l'allarguen; el tema, l'idioma i la lectura en columnes o en una columna triats es recorden sense caducar. Les xifres es desen per hores durant 25 mesos com a màxim, el termini d'aquesta mateixa guia; després només en queda el total de cada any. Només les veuen les dues persones que fan el diari. Per poder-lo llegir sense connexió, el navegador desa al mateix dispositiu una còpia de les pàgines obertes i de l'últim número; aquesta còpia no en surt. L'app d'Android és aquest mateix web i no recull res més. Els comentaris es publiquen amb giscus a les Discussions de GitHub: per comentar cal un compte de GitHub, i GitHub desa el comentari i el nom d'usuari amb la seva pròpia política de privadesa. Qui no comenta no envia res."),
                ("Les comunitats", "{chatgpt}, sobre intel·ligència artificial en educació; {vce}, de docents que programen les seves pròpies aplicacions amb IA, i {edumedia}, sobre IA generativa per crear àudio, vídeo i imatge. Totes tres són obertes: cada peça enllaça amb la conversa on va néixer, que es pot llegir sense entrar-hi."),
                ("Si participes als grups", "Les opinions no s'atribueixen a ningú: només s'anomena la persona que ha publicat un recurs propi. Si hi apareix alguna cosa teva i prefereixes que no surti, o hi veus un error, digues-ho a les persones que administren el teu grup i es retirarà o es corregirà."),
                ("Contacte", "El correu i les altres vies per avisar d'un error, demanar que es retiri alguna cosa o fer qualsevol consulta són a la {pagina_contacto}."),
            ],
        },
    },
}
from idiomas_web import GL, EU, EN   # noqa: E402
IDIOMAS.update({"gl": GL, "eu": EU, "en": EN})
from textos_para_tu_web import TEXTOS as TEXTOS_PTW   # noqa: E402  (ADR 0032)
for _c, _t in TEXTOS_PTW.items():
    IDIOMAS[_c].update(_t)
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
# Lucide (ISC): text-align-justify (una columna) y columns-3 (columnas), para el botón de lectura (ADR 0044)
UNA_COLUMNA = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18"/><path d="M3 12h18"/><path d="M3 19h18"/></svg>'
COLUMNAS = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/><path d="M15 3v18"/></svg>'
COMPARTIR = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/></svg>'   # share-2
PLAY = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 9.003a1 1 0 0 1 1.517-.859l4.997 2.997a1 1 0 0 1 0 1.718l-4.997 2.997A1 1 0 0 1 9 14.996z"/><circle cx="12" cy="12" r="10"/></svg>'   # circle-play: la página de vídeos (ADR 0016)
LUPA = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'   # search
LUNA = '<svg class="luna" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>'
SOL = '<svg class="sol" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'


WEB_JUANJO = "https://bilateria.org"
WEB_RAUL = "https://raultorres-ia.github.io/apps/raul-torres-ai-portfolio/"

def de_mes(mes):
    """«de octubre» en castellano y gallego; en catalán, «d'octubre» ante vocal."""
    if L["codigo"] == "ca" and mes[0] in "aeiou":
        return f"d'{mes}"
    return f"de {mes}"


def mayus(t):
    """La primera letra en mayúscula, sin tocar las demás (str.capitalize pone «november» en inglés)."""
    return t[:1].upper() + t[1:]


def fecha_larga(iso):
    d = datetime.date.fromisoformat(iso)
    dia, mes = L["dias"][d.weekday()], L["meses"][d.month - 1]
    if L["codigo"] == "en":
        return f"{dia}, {d.day} {mes} {d.year}"
    if L["codigo"] == "eu":   # «2026ko azaroaren 6a, ostirala»
        return f"{d.year}ko {mes}ren {d.day}a, {dia}"
    return f"{dia}, {d.day} {de_mes(mes)} de {d.year}"


def publicacion(iso):
    """Un número sale a la mañana siguiente del día que cuenta: su fecha de cabecera es esa."""
    return (datetime.date.fromisoformat(iso) + datetime.timedelta(days=1)).isoformat()


def hora_de_salida(sale):
    """Las 7:00 de Madrid del día de publicación, pasadas a UTC (el cambio de hora no la mueve)."""
    return datetime.datetime.combine(datetime.date.fromisoformat(sale), datetime.time(7),
                                     ZoneInfo("Europe/Madrid")).astimezone(datetime.timezone.utc)


def romano(n):
    r, resto = "", n
    for v, s in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                 (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while resto >= v:
            r += s
            resto -= v
    return r


def anyo_edicion(iso_publicacion):
    """«Año I» cuenta desde el año del número 1, como en la cabecera clásica de un periódico (en inglés, «Vol. I»)."""
    primero = datetime.date.fromisoformat(publicacion(LANZAMIENTO)).year
    return romano(datetime.date.fromisoformat(iso_publicacion).year - primero + 1)


def mes_largo(iso):
    d = datetime.date.fromisoformat(iso)
    mes = L["meses"][d.month - 1]
    if L["codigo"] == "en":
        return f"{mes} {d.year}"
    if L["codigo"] == "eu":
        return f"{d.year}ko {mes}"
    return f"{mayus(mes)} de {d.year}"


def fecha_corta(iso):
    d = datetime.date.fromisoformat(iso)
    mes = L["meses"][d.month - 1]
    if L["codigo"] == "en":
        return f"{d.day} {mes}"
    if L["codigo"] == "eu":
        return f"{mes}ren {d.day}a"
    return f"{d.day} {de_mes(mes)}"


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
            # La lista de lo ya contado en la semana la pone el programa en el original, no se traduce
            ya = {x["id"]: x["ya_contados"] for x in json.loads((RAIZ / "repositorio" / nombre).read_text()).get("piezas", [])
                  if x.get("ya_contados")}
            for x in rep_:
                if x["id"] in ya:
                    x["ya_contados"] = ya[x["id"]]
            for x in rep_:   # con captura, salen como destacados
                x["importancia"] = 2 if any(r.get("captura") for r in x.get("recursos", [])) else 3
            d["piezas"] = d["piezas"] + rep_
        if d.get("piezas") and (RAIZ / "hace-un-ano" / nombre).exists():   # «Hace un año» (ADR 0040), siempre al final
            hu = json.loads(con_traduccion("hace-un-ano", nombre).read_text())
            if hu.get("hay_pieza"):
                for x in hu.get("piezas", []):
                    x["importancia"] = 9
                d["piezas"] = d["piezas"] + hu.get("piezas", [])
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
    global ULTIMA_SEMANA   # la última «Semana del repositorio»: a ella lleva el antetítulo de las demás
    semanas = [p for d in eds for p in d["piezas"] if p.get("repositorio") == "semana"]
    ULTIMA_SEMANA = semanas[-1] if semanas else None
    n = 0
    for d in eds:   # cada día con piezas desde el lanzamiento es un número del diario
        if d["fecha"] >= LANZAMIENTO:
            n += 1
            d["numero"] = n
        else:
            d["numero"] = None
    return eds


def seleccion_portada(eds):
    """Todo lo del último número, que abre la portada, y, para el bloque de cada sección, sus tres piezas más
    recientes de días anteriores, retrocediendo lo que haga falta: así ningún bloque queda con huecos salvo que
    la sección no tenga más piezas. Antes había un tope de 10 para toda la portada, y con lo de hoy y ayer
    los bloques de las demás secciones se quedaban con una pieza y dos huecos (09-11-2026)."""
    ultima = datetime.date.fromisoformat(eds[-1]["fecha"])
    desde = (ultima - datetime.timedelta(days=DIAS_PORTADA - 1)).isoformat()
    recientes = [d for d in reversed(eds) if d["fecha"] >= desde]
    hoy = eds[-1]["piezas"]
    piezas = [p for p in hoy if p.get("seccion") != "biblioteca"] + [p for p in hoy if p.get("seccion") == "biblioteca"]
    por_seccion = {}
    for d in reversed(eds[:-1]):   # del día más reciente al más antiguo; dentro de cada día, por importancia
        for p in d["piezas"]:
            if p.get("seccion") in ORDEN_SECCIONES and len(por_seccion.setdefault(p["seccion"], [])) < POR_SECCION:
                por_seccion[p["seccion"]].append(p)
    piezas += [p for c in ORDEN_SECCIONES for p in por_seccion.get(c, [])]
    # Los del último número, todos (van arriba); de los días anteriores, como mucho MAX_BREVES
    breves = recientes[0].get("breves", []) + [b for d in recientes[1:] for b in d.get("breves", [])][:MAX_BREVES]
    return piezas, breves


def recursos(prof):
    """Las hojas de estilo y la letra están en la raíz del sitio, compartidas por todos los idiomas."""
    return prof + ("../" if L["carpeta"] else "")


ULTIMA = None   # fecha del último número, para la imagen de vista previa de la portada
ULTIMA_SEMANA = None   # la última pieza «La semana del repositorio» (ADR 0008)


def imagen_og(ruta, codigo):
    """La portada y la página de cada día enseñan la imagen de su número (ADR 0010); lo demás, la genérica."""
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})/", ruta)
    fecha = m.group(1) if m else (ULTIMA if ruta == "" else None)
    if fecha:
        for c in (codigo, "es"):   # sin imagen del número en ese idioma, la del castellano
            if (RAIZ / "og" / "numeros" / f"{fecha}-{c}.png").exists():
                return f"{BASE}og/{fecha}-{c}.png"
    return f"{BASE}og-{codigo if (RAIZ / 'estaticos' / f'og-{codigo}.png').exists() else 'es'}.png"


# Contador de visitas (ADR 0033): el navegador recuerda qué páginas ha contado en la visita en curso, que
# acaba tras 30 minutos sin abrir ninguna; al servidor (bilateria.org) solo le llega la suma: la página,
# si empieza una visita y el título. Sin cookies ni datos de quien lee. No cuenta los robots, los
# navegadores automatizados, la portada que salta a otro idioma ni los navegadores marcados con
# ?nocontar=1 (?nocontar=0 lo deshace). El panel marca así, con un salto de ida y vuelta, cada navegador
# desde el que entran los autores (volver=1; la vuelta es fija, al panel). El widget para otras webs
# (insertar.html) no lleva contador. Solo cuenta en la dirección del diario: ni las copias de la Wayback
# Machine (ADR 0046) ni la vista previa de casa.
CONTADOR = """<script>try{(function(){
var q=new URLSearchParams(location.search),k='diario.nocontar';
if(q.get('nocontar')==='1')localStorage.setItem(k,'1');else if(q.get('nocontar')==='0')localStorage.removeItem(k);
if(q.get('volver')==='1'){location.replace('https://bilateria.org/app/diario-ia-educativa/?marcado=1');return;}
if(location.hostname!=='diarioiaeducativa.github.io'||window.SALTO||navigator.webdriver||localStorage.getItem(k)||/bot|crawl|spider|slurp|preview|lighthouse|headless/i.test(navigator.userAgent))return;
var v=JSON.parse(localStorage.getItem('diario.visita')||'null'),ahora=Date.now(),p=location.pathname,nueva=!v||!(ahora-v.t<18e5);
if(nueva)v={t:ahora,p:[]};
var cuenta=v.p.indexOf(p)<0;v.t=ahora;if(cuenta)v.p.push(p);
localStorage.setItem('diario.visita',JSON.stringify(v));if(!localStorage.getItem('diario.desde'))localStorage.setItem('diario.desde',ahora);
if(nueva||cuenta)navigator.sendBeacon('https://bilateria.org/app/diario-ia-educativa/contar.php',new URLSearchParams({p:cuenta?p:'',n:nueva?'1':'0',t:document.title}));
})();}catch(_){}</script>"""


# La cuenta de la visita del contador («diario.visita») caduca a los 13 meses de guardarse por primera
# vez, la duración que pone de ejemplo la AEPD, y lo esencial: las visitas nuevas no la renuevan (ADR 0033).
# AEPD (2024), «Uso de cookies para herramientas de medición de audiencia», ap. III.A, garantía 2, p. 4
# (https://www.aepd.es/guias/guia-cookies-analiticas-externas.pdf). «diario.desde» guarda esa fecha y,
# pasada, se borra la cuenta y se empieza de cero; si en ese momento hay una visita en curso, se conserva,
# para no contarla dos veces. El tema y el idioma son preferencias de quien lee y no caducan: la guía solo
# pide la caducidad para la medición. Tampoco la marca de los autores («diario.nocontar»), que solo está
# en sus navegadores y quitan ellos con ?nocontar=0. Va en el primer script de la cabecera, con el tema y con la
# marca de la app de Android, que tiene que ponerse antes de que la portada salte de idioma (ADR 0043).
AEPD_MEDICION = "https://www.aepd.es/guias/guia-cookies-analiticas-externas.pdf"   # solo en castellano
CADUCIDAD = """<script>try{(function(){
var s=localStorage,c=+s.getItem('diario.desde'),ahora=Date.now();
if(c&&ahora-c>%d){var v=JSON.parse(s.getItem('diario.visita')||'null');s.removeItem('diario.visita');s.removeItem('diario.desde');c=0;
if(v&&ahora-v.t<18e5)s.setItem('diario.visita',JSON.stringify(v));}
if(!c&&s.getItem('diario.visita')!==null)s.setItem('diario.desde',ahora);
var t=s.getItem('sala.tema');if(t)document.documentElement.dataset.theme=t;
if(/^android-app:\\/\\/io\\.github\\.diarioiaeducativa/.test(document.referrer))sessionStorage.setItem('diario.app','1');})();}catch(_){}</script>""" % (395 * 86400000)
def datos_noticia(titular, ruta, fecha, imagen=None):
    """Los datos estructurados de una pieza, para los buscadores (schema.org, ADR 0039): qué es, cuándo
    salió y quién la firma. La firma es la redacción, con su página, donde se cuenta cómo se hace; sin
    fecha de modificación, que no se lleva."""
    redaccion = {"@type": "Organization", "name": L["titulo"], "url": BASE + L["carpeta"] + "redaccion.html"}
    d = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": titular,
         "datePublished": hora_de_salida(publicacion(fecha)).isoformat(), "inLanguage": L["codigo"],
         "mainEntityOfPage": BASE + L["carpeta"] + ruta, "author": redaccion, "publisher": redaccion}
    if imagen:
        d["image"] = [imagen]
    return d


def cabeza(titulo, prof, descripcion, ruta, portada=False, datos=None):
    codigo = L["codigo"]
    r = recursos(prof)
    # En la portada, quien llega sin haber elegido idioma va al de su navegador; lo elegido se recuerda.
    # Los robots de los buscadores no se redirigen: indexan cada edición en su dirección (ADR 0026).
    salto = ""
    if portada:
        destinos = ",".join(f"{c}:'{href_idioma(prof, ruta, c)}'" for c in IDIOMAS if c != codigo)
        if codigo == "es":
            cond = ("var g=localStorage.getItem('sala.idioma'),n=(navigator.language||'').slice(0,2).toLowerCase(),"
                    "bot=/bot|crawl|spider|slurp|inspection|lighthouse|preview|facebookexternalhit/i.test(navigator.userAgent),"
                    "d=g||(bot?null:n);")
        else:   # un enlace a otra edición se respeta: solo cambia si se eligió otro idioma
            cond = "var d=localStorage.getItem('sala.idioma');"
        salto = f"<script>try{{var D={{{destinos}}};{cond}if(d&&D[d]){{window.SALTO=1;location.replace(D[d]);}}}}catch(_){{}}</script>"
    alternas = "".join(f'<link rel="alternate" hreflang="{c}" href="{e(BASE + d["carpeta"] + ruta)}">\n'
                       for c, d in IDIOMAS.items() if ruta != "404.html")
    if ruta != "404.html":
        alternas += f'<link rel="alternate" hreflang="x-default" href="{e(BASE + ruta)}">\n'
    # Cada página dice cuál es su dirección, para que las que llegan con parámetros (?grupo=, ?nocontar=)
    # no cuenten como páginas distintas; cada idioma, la suya (ADR 0039)
    canonica = f'<link rel="canonical" href="{e(BASE + L["carpeta"] + ruta)}">\n' if ruta != "404.html" else ""
    if portada and codigo == "es" and ruta == "":   # el nombre del sitio, que Google toma de la portada de la raíz
        datos = {"@context": "https://schema.org", "@type": "WebSite", "name": L["titulo"], "url": BASE}
    ld = ('<script type="application/ld+json">' + json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
          + "</script>\n") if datos else ""
    return f"""<!doctype html>
<html lang="{codigo}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
{canonica}{alternas}{ld}<link rel="alternate" type="application/rss+xml" title="{e(L["titulo"])}" href="{prof}feed.xml">
<meta property="og:type" content="{"website" if portada else "article"}">
<meta property="og:site_name" content="{e(L["titulo"])}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{e(BASE + L["carpeta"] + ruta)}">
<meta property="og:image" content="{e(imagen_og(ruta, codigo))}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{L["locale"]}">
<meta name="twitter:card" content="summary_large_image">
{CADUCIDAD}
<script>try{{if(localStorage.getItem('diario.columnas')==='una')document.documentElement.classList.add('una-columna');}}catch(_){{}}</script>
{salto}
{CONTADOR if ruta not in ("404.html", "sin-conexion.html") else ""}
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
    """La misma página en otro idioma."""
    if ruta == "404.html":   # solo hay una, en la raíz: las otras ediciones llevan a su portada
        return "/" + IDIOMAS[destino]["carpeta"]
    return f"{recursos(prof)}{IDIOMAS[destino]['carpeta']}{ruta}" or "./"


ICONO_IDIOMAS = ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/>'
                 '<path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/></svg>')   # languages (Lucide)


def selector_idioma(prof, ruta):
    """Un botón con el idioma en uso que despliega los cinco, cada uno en su lengua y con una marca en el
    actual. Cada opción lleva a la misma página en ese idioma: son enlaces, y los buscadores los siguen."""
    yo = L["codigo"]
    actual = ' aria-current="true"'
    items = "".join(
        f'<li><a href="{href_idioma(prof, ruta, c)}" lang="{c}" hreflang="{c}" data-idioma="{c}"'
        f'{actual if c == yo else ""}>{d["nombre"]}</a></li>' for c, d in IDIOMAS.items())
    rotulo = f'{L["idioma"]}: {L["nombre"]}'
    return (f'<span class="idiomas"><button type="button" class="idioma-boton" aria-expanded="false" aria-controls="menu-idiomas" '
            f'title="{rotulo}" aria-label="{rotulo}">{ICONO_IDIOMAS}<span class="idioma-cod" aria-hidden="true">{yo.upper()}</span></button>'
            f'<ul class="idioma-menu" id="menu-idiomas" hidden>{items}</ul></span>')


# Comentarios (ADR 0030): giscus guarda cada hilo en las Discussions del repositorio del sitio, sin
# servidor propio. El hilo es de la pieza, no de la página: el mismo en los cinco idiomas.
GISCUS = {"repo": "diarioiaeducativa/diarioiaeducativa.github.io", "repo-id": "R_kgDOVfWo0w",
          "category": "Comentarios", "category-id": "DIC_kwDOVfWo084DKlp3"}
GISCUS_IDIOMA = {"es": "es", "ca": "ca", "gl": "es", "eu": "eu", "en": "en"}   # giscus no tiene gallego


def comentarios(ruta):
    """El bloque de comentarios de una pieza. `ruta` es la de la pieza sin idioma (AAAA-MM-DD/id.html)."""
    datos = dict(GISCUS, mapping="specific", term=ruta.removesuffix(".html"), strict="1",
                 **{"reactions-enabled": "0", "emit-metadata": "0", "input-position": "top",
                    "lang": GISCUS_IDIOMA.get(L["codigo"], "en"), "loading": "lazy"})
    attrs = "".join(f's.setAttribute("data-{k}",{json.dumps(v)});' for k, v in datos.items())
    aviso = L["comentarios_aviso"].format(cuenta=enlace("https://github.com/signup", L["comentarios_cuenta"]))
    return f"""<section class="comentarios" data-pagefind-ignore aria-labelledby="t-comentarios">
    <h2 id="t-comentarios">{L["comentarios"]}</h2>
    <p class="comentarios-aviso">{aviso}</p>
    <div class="comentarios-caja"></div>
    <script>
    (function(){{
      var raiz=document.documentElement, caja=document.currentScript.previousElementSibling;
      function tema(){{var t=raiz.dataset.theme; return (t? t==='dark' : matchMedia('(prefers-color-scheme: dark)').matches)?'transparent_dark':'light';}}
      var s=document.createElement('script'); s.src='https://giscus.app/client.js'; s.async=true; s.crossOrigin='anonymous';
      {attrs}s.setAttribute('data-theme',tema()); caja.appendChild(s);
      // Al cambiar el tema del diario, también el de los comentarios
      new MutationObserver(function(){{var f=document.querySelector('iframe.giscus-frame');
        if(f) f.contentWindow.postMessage({{giscus:{{setConfig:{{theme:tema()}}}}}},'https://giscus.app');}}).observe(raiz,{{attributes:true,attributeFilter:['data-theme']}});
    }})();
    </script>
  </section>"""


def boton_tema():
    return f'<button type="button" class="tema" id="tema" title="{L["tema"]}" aria-label="{L["tema"]}">{LUNA}{SOL}</button>'


SCRIPT_FILAS = """<script>
/* Que ninguna fila de piezas deje blancos (ADR 0041). En cada fila, cada pieza puede enseñar de su entradilla
   entre dos líneas y la entradilla entera; se busca la altura a la que pueden acabar todas (la de la pieza que
   antes se queda sin texto) y cada una enseña las líneas que caben hasta ahí. La entradilla entera está en el
   artículo. Se rehace al cambiar el ancho. En una sola columna (el móvil) no se toca nada. */
(function(){
  var SEL='.fila-destacadas,.mas-dia,.alt-b,.alt-a,.fila-seccion,.fila-breves-hu,.nb-grupos',ENT='.entradilla,.nb-resumen';
  /* Hasta dónde llega lo visible de una pieza: lo que oculta una entradilla recortada no cuenta (ADR 0045) */
  function fondo(el){var m=el.getBoundingClientRect().top,w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,r,i,rs,a,tope;
    while((n=w.nextNode())){if(!n.textContent.trim())continue;tope=Infinity;for(a=n.parentElement;a&&a!==el.parentElement;a=a.parentElement)if(getComputedStyle(a).overflow!=='visible')tope=Math.min(tope,a.getBoundingClientRect().bottom);
      r=document.createRange();r.selectNodeContents(n);rs=r.getClientRects();for(i=0;i<rs.length;i++)m=Math.max(m,Math.min(rs[i].bottom,tope));}
    el.querySelectorAll('figure').forEach(function(f){m=Math.max(m,f.getBoundingClientRect().bottom);});return m;}
  function suelta(e){e.style.display='block';e.style.webkitLineClamp='unset';e.style.lineClamp='none';e.style.overflow='visible';e.style.webkitBoxOrient='';}
  function recorta(e,l){e.style.display='-webkit-box';e.style.webkitBoxOrient='vertical';e.style.webkitLineClamp=l;e.style.lineClamp=l;e.style.overflow='hidden';}
  function igualar(){
    document.querySelectorAll(SEL).forEach(function(g){
      var hijos=[].slice.call(g.children).filter(function(c){return c.offsetParent;});
      hijos.forEach(function(c){c.querySelectorAll(ENT).forEach(suelta);});
      if(hijos.length<2||getComputedStyle(g).gridTemplateColumns.split(' ').length<2)return;
      var filas={};hijos.forEach(function(c){var k=Math.round(c.getBoundingClientRect().top/8);(filas[k]=filas[k]||[]).push(c);});
      Object.keys(filas).forEach(function(k){var f=filas[k];if(f.length<2)return;
        var d=f.map(function(c){var es=c.querySelectorAll(ENT),e=es[es.length-1],b=fondo(c);
          if(!e||!e.textContent.trim())return {c:c,min:b,max:b};
          var lh=parseFloat(getComputedStyle(e).lineHeight)||24,n=Math.max(1,Math.round(e.getBoundingClientRect().height/lh));
          /* cada línea que se quita sube el final de la pieza una línea, haya lo que haya debajo (los enlaces) */
          return {c:c,e:e,lh:lh,n:n,b:b,min:b-(n-Math.min(2,n))*lh,max:b};});
        var meta=Math.min.apply(null,d.map(function(x){return x.max;})),suelo=Math.max.apply(null,d.map(function(x){return x.min;}));
        if(meta<suelo)meta=suelo;
        d.forEach(function(x){if(!x.e)return;var l=x.n-Math.ceil((x.b-meta-3)/x.lh);l=Math.max(Math.min(2,x.n),Math.min(x.n,l));if(l<x.n)recorta(x.e,l);});
      });
      /* En la disposición A, lo que quede lo absorbe el dibujo de la pieza grande: entre un tercio y algo más de
         la mitad de su ancho de alto */
      if(g.classList.contains('alt-a')){var gr=g.querySelector('.alt-grande'),li=g.querySelector('.alt-lista'),il=gr&&gr.querySelector('.ilu');
        if(il&&li){il.style.height='';il.style.aspectRatio='';var dif=fondo(li)-fondo(gr),h=il.getBoundingClientRect().height,w=il.getBoundingClientRect().width;
          var nh=Math.max(w/3.2,Math.min(w*0.6,h+dif));if(Math.abs(nh-h)>2){il.style.aspectRatio='auto';il.style.height=nh+'px';}
          /* Si el dibujo ya está en su tope y la lista sigue más larga, sus entradillas se recortan línea a línea
             (como mucho hasta dos), de la última pieza a la primera (ADR 0045) */
          var es=[].slice.call(li.querySelectorAll('.entradilla')).reverse(),q;
          for(q=0;q<es.length;q++){var e=es[q],lh=parseFloat(getComputedStyle(e).lineHeight)||24,n=Math.round(e.getBoundingClientRect().height/lh);
            while(n>2&&fondo(li)-fondo(gr)>lh/2){n--;recorta(e,n);}}}}
    });
  }
  var t;function luego(){clearTimeout(t);t=setTimeout(igualar,120);}
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(igualar);else window.addEventListener('load',igualar);
  window.addEventListener('load',igualar);window.addEventListener('resize',luego);
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.filtro-grupo'))luego();});   /* la semana: al elegir un grupo cambian las filas */
})();
/* El dibujo de una pieza, del reportaje o de «Hace un año» lleva a su artículo, como el titular (ADR 0045). Con Ctrl, Mayúsculas o la rueda, en otra
   pestaña. El teclado y el lector de pantalla entran por el titular, sin un enlace repetido. */
(function(){
  function destino(e){var f=e.target.closest&&e.target.closest('main.portada .ilu'),c=f&&f.closest('.pieza, .editorial');
    if(!c||f.querySelector('.ampliar'))return null;var a=c.querySelector('.titular a');return a&&a.href;}
  document.addEventListener('click',function(e){var h=destino(e);if(!h)return;
    if(e.ctrlKey||e.metaKey||e.shiftKey)window.open(h,'_blank');else location.href=h;});
  document.addEventListener('auxclick',function(e){var h=destino(e);if(h&&e.button===1)window.open(h,'_blank');});
})();
</script>"""


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
  // Columnas o una columna (ADR 0044): se recuerda en el dispositivo para todas las noticias
  var bc=document.querySelector('.columnas-boton');
  if(bc) bc.addEventListener('click',function(){
    var una=raiz.classList.toggle('una-columna');
    try{ if(una) localStorage.setItem('diario.columnas','una'); else localStorage.removeItem('diario.columnas');}catch(_){}
  });
  document.querySelectorAll('[data-idioma]').forEach(function(a){
    a.addEventListener('click',function(){try{localStorage.setItem('sala.idioma',a.dataset.idioma);}catch(_){}});
  });
  // El menú de idiomas (ADR 0026): se abre al pulsar el botón y se cierra al pulsar fuera o con Escape
  var bi=document.querySelector('.idioma-boton'), mi=document.getElementById('menu-idiomas');
  if(bi&&mi){
    function idiomas(abre){mi.hidden=!abre; bi.setAttribute('aria-expanded',abre?'true':'false'); if(abre){var a=mi.querySelector('[aria-current]')||mi.querySelector('a'); a&&a.focus();}}
    bi.addEventListener('click',function(ev){ev.stopPropagation(); idiomas(mi.hidden);});
    document.addEventListener('click',function(ev){if(!mi.hidden&&!mi.contains(ev.target))idiomas(false);});
    document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&!mi.hidden){idiomas(false);bi.focus();}});
  }
  // En el móvil las secciones se deslizan: la sección abierta, a la vista
  var lista=document.querySelector('.secciones-lista'), activa=lista&&lista.querySelector('[aria-current]');
  if(activa&&lista.scrollWidth>lista.clientWidth) lista.scrollLeft=activa.offsetLeft-(lista.clientWidth-activa.offsetWidth)/2;
  // Ampliar una captura o un dibujo: sobre la propia página, al mayor tamaño que quepa, con la X arriba a la derecha.
  // Atiende a toda la página, también a las imágenes que se ponen después (la portada del día en la hemeroteca).
  document.addEventListener('click',function(ev){
    var b=ev.target.closest&&ev.target.closest('button.ampliar'); if(!b) return;
    (function(){
      var img=b.querySelector('img'), dib=b.querySelector('svg'), v=document.createElement('div'), x=document.createElement('button'), g;
      v.className='visor'; v.setAttribute('role','dialog'); v.setAttribute('aria-modal','true');
      if(img){ g=img.cloneNode(); v.setAttribute('aria-label',img.alt);
        // Una imagen muy alta (la portada de un número) se abre a lo ancho y se baja dentro del visor
        if(img.getAttribute('height')/img.getAttribute('width')>1.4) v.classList.add('alta'); }
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
    })();
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
  // Lectura sin conexión (ADR 0042): el service worker guarda lo que se abre y el último número. Solo en
  // el propio diario, no dentro del marco de otra web.
  // La primera vez, la página se ha cargado sin él: le pasa lo cargado para que lo guarde con el último número.
  if('serviceWorker' in navigator&&window.top===window){
    var sinControl=!navigator.serviceWorker.controller;
    navigator.serviceWorker.register('/sw.js').then(function(){return navigator.serviceWorker.ready;}).then(function(r){
      if(!sinControl||!r.active)return;
      var u=[location.href].concat(performance.getEntriesByType('resource').map(function(x){return x.name;})
        .filter(function(n){return n.indexOf(location.origin+'/')===0;}));
      r.active.postMessage({guardar:u});
    }).catch(function(){});
  }
  // Los avisos del número (ADR 0043) son de la app de Android: el enlace sale solo dentro de ella, que se
  // reconoce porque la abre con su nombre como referencia. En la sesión, no para siempre: la app comparte
  // la memoria del sitio con Chrome, y en Chrome el enlace no haría nada.
  // La marca la pone CADUCIDAD, el primer script de la cabecera, antes de que la portada salte de idioma.
  var av=document.querySelector('.avisos-app');
  if(av){try{if(sessionStorage.getItem('diario.app'))av.hidden=false;}catch(_){}}
  // «Para tu web» (ADR 0032): el botón despliega sus opciones y se cierra al pulsar fuera o con Escape
  var bl=document.querySelector('.llevar-boton'), ml=document.getElementById('menu-llevar');
  function cerrarLlevar(){ if(ml&&!ml.hidden){ml.hidden=true; bl.setAttribute('aria-expanded','false');} }
  if(bl&&ml){
    bl.addEventListener('click',function(ev){ev.stopPropagation(); var abre=ml.hidden; ml.hidden=!abre; bl.setAttribute('aria-expanded',abre?'true':'false'); if(abre) ml.querySelector('.llevar-op').focus();});
    document.addEventListener('click',function(ev){if(!ml.hidden&&!ml.contains(ev.target)&&!bl.contains(ev.target))cerrarLlevar();});
    document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&!ml.hidden){cerrarLlevar();bl.focus();}});
  }
  // Copiar sin pedir nada a mano: el portapapeles del navegador o, si no lo deja (sin HTTPS), un campo
  // oculto. La pieza entera se copia con formato, para el editor de un blog, y como código, para un bloque HTML.
  function copiar(texto, html){
    if(navigator.clipboard&&window.isSecureContext){
      if(html&&window.ClipboardItem&&navigator.clipboard.write)
        return navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([html],{type:'text/html'}),'text/plain':new Blob([texto],{type:'text/plain'})})])
          .catch(function(){return navigator.clipboard.writeText(texto);});
      return navigator.clipboard.writeText(texto);
    }
    return new Promise(function(ok,mal){
      var t=document.createElement('textarea'); t.value=texto; t.setAttribute('readonly',''); t.style.position='fixed'; t.style.top='0'; t.style.opacity='0';
      document.body.append(t); t.select(); try{document.execCommand('copy')?ok():mal();}catch(x){mal(x);} t.remove();
    });
  }
  document.querySelectorAll('[data-copiar],[data-plantilla],[data-desde]').forEach(function(b){
    b.addEventListener('click',function(){
      var texto=b.dataset.copiar, html=null, r=b.querySelector('span'), antes=r.textContent;
      if(b.dataset.plantilla){html=document.getElementById(b.dataset.plantilla).innerHTML.trim(); texto=html;}
      if(b.dataset.desde) texto=document.getElementById(b.dataset.desde).value;
      copiar(texto,html).then(function(){
        r.textContent=b.dataset.hecho; b.classList.add('hecho');
        setTimeout(function(){r.textContent=antes; b.classList.remove('hecho'); if(b.closest('.llevar-menu')) cerrarLlevar();},1600);
      },function(){});
    });
  });
  // Compartir: el menú del dispositivo; si no lo hay, se copia el enlace
  document.querySelectorAll('.compartir:not(.copiar):not(.llevar-boton)').forEach(function(b){
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
    """El pie, como el de un periódico (09-11-2026): tres columnas iguales, cada una con su título y su lista
    (los grupos, el archivo y el diario, con los créditos en letra pequeña bajo sus enlaces, para que las tres
    columnas tengan una altura parecida). El número que se está viendo se marca con una franja de color y
    «(este número)», no con negrita."""
    archivo = "".join(
        (f'<li class="pie-actual"><a href="{prof}{d["fecha"]}/" aria-current="page">{mayus(fecha_larga(publicacion(d["fecha"])))}</a>'
         f' <span class="pie-este">({L["este_numero"]})</span></li>') if d["fecha"] == actual else
        f'<li><a href="{prof}{d["fecha"]}/">{mayus(fecha_larga(publicacion(d["fecha"])))}</a></li>'
        for d in list(reversed(eds))[:DIAS_PIE])
    mirar = (f'<li><a href="{prof}semana/{semana_de(eds[-1]["fecha"])}/">{L["semana_actual"]}</a></li>'
             f'<li><a href="{prof}archivo.html">{L["todos_numeros"]}</a></li>'
             f'<li><a href="{prof}hace-un-ano.html">{L["secciones"]["hace-un-ano"]}</a></li>')
    grupos = "".join(f'<li>{enlace("https://t.me/" + a, n)}: <span class="pie-grupo-desc">{L["grupos_desc"][k]}</span></li>'
                     for k, (n, a) in GRUPOS.items())
    trad = f'<p>{L["traduccion"]}</p>' if L["traduccion"] else ""
    return f"""<footer class="pie">
  <div class="pie-unete">
    <h2>{L["unete"]}</h2>
    <p>{L["unete_txt"]}</p>
    <ul class="pie-grupos">{grupos}</ul>
    {pie_comunidades(prof)}
  </div>
  <nav class="pie-archivo" aria-label="{L["archivo"]}">
    <h2>{L["pie_archivo"]}</h2>
    <ul class="pie-lista">{archivo}</ul>
    <ul class="pie-lista pie-mirar">{mirar}</ul>
  </nav>
  <nav class="pie-diario" aria-label="{L["pie_diario"]}">
    <h2>{L["pie_diario"]}</h2>
    <ul class="pie-lista">
      <li><a href="{prof}redaccion.html">{L["quees"]}</a></li>
      <li><a href="{prof}contacto.html">{L["contacto"]["titulo"]}</a></li>
      <li><a href="{prof}videos.html">{L["videos"]}</a></li>
      <li>{enlace(INSTAGRAM, L["instagram"])}</li>
      <li><a href="{prof}para-tu-web.html">{L["ptw_titulo"]}</a></li>
      <li><a href="{prof}feed.xml">{L["rss"]}</a></li>
      <li class="instalar-app" hidden><button type="button" class="instalar" title="{e(L["instalar_titulo"])}">{L["instalar"]}</button></li>
      <li class="avisos-app" hidden><a href="intent://avisos?idioma={L["codigo"]}#Intent;scheme=diarioia;package=io.github.diarioiaeducativa;end" title="{e(L["avisos_app_titulo"])}">{L["avisos_app"]}</a></li>
    </ul>
    <p class="instalar-ios" hidden>{L["instalar_ios"]}</p>
    <div class="pie-creditos">
    <p>{L["redactado"]}</p>
    {trad}
    <p>© {datetime.date.fromisoformat(eds[-1]["fecha"]).year} {enlace(WEB_JUANJO, "Juan José de Haro")} {L["y"]} {enlace(WEB_RAUL, "Raül Torres")}. {L["licencia"]} {enlace("https://creativecommons.org/licenses/by-sa/4.0/" + L["deed"], "CC BY-SA 4.0")}.</p>
    <p>{L["letra"]} {enlace("https://github.com/productiontype/Newsreader", "Newsreader")} (Production Type, <a href="{prof}{"../" if L["carpeta"] else ""}fuentes/OFL.txt">OFL</a>). {L["iconos"]} {enlace("https://lucide.dev", "Lucide")} (<a href="{prof}{"../" if L["carpeta"] else ""}LICENSE-LUCIDE.txt">ISC</a>).</p>
    <p>{enlace(url_vcer(), L["vcer"])}.</p>
    </div>
  </nav>
</footer>"""


FLECHA_ANT = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m12 8-4 4 4 4"/><path d="M16 12H8"/></svg>'   # circle-arrow-left
FLECHA_SIG = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m12 16 4-4-4-4"/><path d="M8 12h8"/></svg>'   # circle-arrow-right


def barra_secciones(prof, activa, ant="", sig=""):
    """La barra de secciones bajo la mancheta, como en un periódico; «La redacción» cierra la barra, también en el móvil.
    El número anterior (`ant`) y el siguiente (`sig`), en la portada y en la página de cada número, van como flechas
    delante de «Portada», como los botones de atrás y adelante del navegador, sin una línea propia (ADR 0045)."""
    marca = ' aria-current="page"'
    enlaces = [f'<a class="dia-ant" href="{ant}" title="{L["dia_ant"]}" aria-label="{L["dia_ant"]}">{FLECHA_ANT}</a>'] if ant else []
    if sig:
        enlaces.append(f'<a class="dia-sig" href="{sig}" title="{L["dia_sig"]}" aria-label="{L["dia_sig"]}">{FLECHA_SIG}</a>')
    enlaces += [f'<a href="{prof or "./"}"{marca if activa == "portada" else ""}>{L["portada"]}</a>']
    enlaces += [f'<a class="sec-{c}" href="{prof}{c}.html"{marca if c == activa else ""}>{L["secciones"][c]}</a>' for c in ORDEN_SECCIONES]
    enlaces.append(f'<a class="sec-reportaje" href="{prof}reportajes.html"{marca if activa == "reportajes" else ""}>{L["reportajes"]}</a>')
    enlaces.append(f'<a class="sec-vineta" href="{prof}vineta.html"{marca if activa == "vineta" else ""}>{L["vineta"]}</a>')
    quees = f'<a class="quees" href="{prof}redaccion.html"{marca if activa == "redaccion" else ""}>{L["quees"]}</a>'
    return f'<nav class="secciones" aria-label="{L["secciones_nav"]}"><div class="secciones-lista">{"".join(enlaces)}{quees}</div></nav>'


# Tiza y Algoritmo en las orejas de la cabecera (ADR 0049), con las formas de la viñeta (vineta.py) y sus
# mismas clases de color, para que sigan el tema. Tiza, con los brazos caídos; Algoritmo, con los dos en alto.
TIZA_OREJA = (
    '<path class="t" d="M-9 314 L-11 332 L-19 332 M9 314 L11 332 L19 332"/>'
    '<path class="tz" d="M-21 304 L-21 194 Q-21 184 -13 186 L-6 182 L2 187 L9 183 L17 188 Q21 188 21 196 L21 304 Q21 314 11 314 L-11 314 Q-21 314 -21 304 Z"/>'
    '<path class="cara veta" d="M-15 278 L-15 302 M14 266 L14 280"/>'
    '<circle class="ft polvo" cx="-14" cy="174" r="1.4"/><circle class="ft polvo" cx="4" cy="169" r="1.1"/><circle class="ft polvo" cx="15" cy="176" r="1.3"/>'
    '<g transform="translate(2 216)"><circle class="fcara" cx="-9" cy="0" r="2.6"/><circle class="fcara" cx="9" cy="0" r="2.6"/><path class="cara" d="M-8 12 Q0 21 8 12"/></g>'
    '<path class="t" d="M-21 252 Q-31 272 -29 290 M21 252 Q31 272 29 290"/>')
ALGORITMO_OREJA = (
    '<path class="a discontinuo" d="M-18 314 L18 314 M-10 323 L10 323"/>'
    '<rect class="fz" x="-28" y="216" width="56" height="86" rx="7"/>'
    '<g transform="translate(2 244)"><circle class="ojo" cx="-9" cy="0" r="7"/><circle class="ojo" cx="9" cy="0" r="7"/>'
    '<circle class="fpupila" cx="-9" cy="0" r="3"/><circle class="fpupila" cx="9" cy="0" r="3"/><path class="sp" d="M-8 13 Q0 22 8 13"/></g>'
    '<path class="a" d="M-28 264 L-44 234 M28 264 L44 234"/>')


def orejas(prof):
    """Los dos personajes a los lados de la cabecera, de pie sobre el filete doble: Tiza a la izquierda y
    Algoritmo a la derecha, como en la viñeta (ADR 0022). Cada uno dice su nombre al pasar por encima y lleva
    a «La viñeta», donde salen cada día."""
    def una(lado, nombre, caja, dibujo):
        x, y, w, h = caja
        return (f'<a class="oreja oreja-{lado}" href="{prof}vineta.html" title="{nombre}" aria-label="{nombre}: {L["vineta"]}">'
                f'<svg viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" aria-hidden="true" focusable="false">{dibujo}</svg></a>')
    return (f'<div class="orejas">{una("izq", L["nombre_tiza"], (-36, 162, 72, 172), TIZA_OREJA)}'
            f'{una("der", L["nombre_algoritmo"], (-50, 162, 100, 172), ALGORITMO_OREJA)}</div>')


def cabecera(prof, ruta, fecha, cuenta, es_portada, h1=True, activa=None, ant="", sig=""):
    """`cuenta` es el número de la edición, rodeado a mano con el bolígrafo rojo, como en un periódico.
    Con h1="dia" (la página de un número de la hemeroteca), la mancheta es el h1 de la página, con el
    enlace a la portada y la fecha solo para el lector de pantalla: se ve igual que con un <p>."""
    etiqueta = "h1" if h1 else "p"
    nombre = L["titulo"] if h1 is True else f'<a href="{prof or "./"}">{L["titulo"]}</a>'
    sale = publicacion(fecha)
    if h1 == "dia":
        nombre += f'<span class="solo-lector">, {fecha_larga(sale)}</span>'
    cuando = f'<time datetime="{sale}">{mayus(fecha_larga(sale))}</time>'
    numero = (f'<span class="edicion-num"><span class="anyo">{(anyo_edicion(sale) + ". " + L["anyo"]) if L["codigo"] == "eu" else (L["anyo"] + " " + anyo_edicion(sale))}</span>'
              f'<span class="numero"><span class="solo-lector">{L["numero_largo"]} </span><span aria-hidden="true">{L["num"]}&nbsp;</span><b>{cuenta}</b></span></span>')
    return f"""<header class="cabecera">
  <div class="cabecera-fila">
    <span class="cuando">{cuando}</span>
    {numero if cuenta else '<span></span>'}
    <span class="controles"><a class="ico-video" href="{prof}videos.html" title="{L["videos"]}" aria-label="{L["videos"]}">{PLAY}</a><a class="lupa" href="{prof}buscar.html" title="{L["buscar_etiqueta"]}" aria-label="{L["buscar_etiqueta"]}">{LUPA}<span class="lupa-rotulo">{L["buscar"]}</span></a>{selector_idioma(prof, ruta)}{boton_tema()}</span>
  </div>
  <{etiqueta} class="mancheta">{nombre}</{etiqueta}>
  <p class="lema">{L["lema"]}</p>
  {orejas(prof)}
  {barra_secciones(prof, activa, ant, sig)}
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


def fecha_rotulo(p):
    """La fecha que se ve junto a la sección: la del número; en «Hace un año», la de entonces con su año
    («7 de noviembre de 2025»), para que se vea de un golpe que es antiguo (ADR 0040)."""
    if p.get("seccion") in SECCIONES_FUERA and p.get("fecha_original"):
        return fecha_con_anyo(p["fecha_original"])
    return fecha_corta(publicacion(p["fecha"]))


def boton_columnas():
    """Columnas o una columna (ADR 0044): solo en el ordenador (diario.css lo esconde en lo demás); el rótulo
    que se ve depende de la clase de <html>, que pone la cabeza antes de pintar, y lo recuerda SCRIPT_TEMA."""
    return (f'<button type="button" class="columnas-boton" data-pagefind-ignore>'
            f'<span class="a-una" title="{e(L["una_columna_t"])}">{UNA_COLUMNA}{e(L["una_columna"])}</span>'
            f'<span class="a-columnas" title="{e(L["columnas_t"])}">{COLUMNAS}{e(L["columnas"])}</span></button>')


def rotulos(p, mostrar_fecha, prof="", sin_seccion=False, boton=""):
    sec = p.get("seccion", "")
    fecha = f' <span class="fecha-pieza">{fecha_rotulo(p)}</span>' if mostrar_fecha else ""
    if boton:
        fecha = f' <span class="seccion-dcha">{boton}{fecha}</span>'
    nombre = L["secciones"].get(sec, "")
    rotulo = f'<a href="{prof}{sec}.html">{icono(sec)} {nombre}</a>' if sec in L["secciones"] else nombre
    if sin_seccion:   # en la página de la sección, el nombre ya está en el título
        rotulo = ""
    ante = e(p.get("antetitulo"))
    u = ULTIMA_SEMANA
    if p.get("repositorio") == "semana" and u and (u["fecha"], u["id"]) != (p.get("fecha"), p.get("id")):
        ante = f'<a href="{href(prof, u)}">{ante}</a>'   # es una serie: lleva a la última
    if not rotulo:   # sin el nombre de la sección, la fecha va en la línea del antetítulo: sola dejaba un hueco encima del titular
        return f'<p class="antetitulo con-fecha">{fecha}{ante}</p>'
    return f"""<p class="seccion"><span>{rotulo}</span>{fecha}</p>
  <p class="antetitulo">{ante}</p>"""


def cabeza_pieza(texto, ilu):
    """La cabeza de una noticia (ADR 0044): en el ordenador, titular y entradilla junto al dibujo."""
    return f'<div class="cabeza-pieza"><div class="cabeza-texto">{texto}</div>{ilu}</div>'



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


def titulares_parejos(ps, por_linea=34):
    """Si los titulares de tres piezas ocupan en una columna de la fila de tres un número de líneas parecido
    (como mucho una de diferencia): con más, la fila de tres deja un blanco y va mejor la otra disposición."""
    lineas = [-(-len(p.get("titular", "")) // por_linea) for p in ps]
    return max(lineas) - min(lineas) <= 1


def sin_viuda(t):
    """Las dos últimas palabras del titular de un artículo, unidas por un espacio que no se parte: así la última
    no se queda sola en su línea en los navegadores sin `text-wrap: pretty` (Firefox) (ADR 0045)."""
    a, sep, b = t.rpartition(" ")
    return f"{a}\u00a0{b}" if sep and len(b) < 12 else t


def reparto(n):
    """Las filas en que se reparten n piezas de una rejilla de tres columnas sin dejar huecos (ADR 0045): filas de
    tres y, al final, de dos; nunca una pieza sola salvo que solo haya una. 4 → 2+2, 5 → 3+2, 7 → 3+2+2."""
    if n <= 3:
        return [n] if n else []
    if n % 3 == 0:
        return [3] * (n // 3)
    if n % 3 == 2:
        return [3] * (n // 3) + [2]
    return [3] * (n // 3 - 1) + [2, 2]


def en_filas(htmls, clase):
    """Las piezas ya compuestas, en filas seguidas según `reparto`, cada una con sus columnas."""
    html_, i = "", 0
    for k, t in enumerate(reparto(len(htmls))):
        sola = " sola" if t == 1 else ""
        sigue = " fila-sigue" if k else ""
        html_ += f'<div class="fila {clase}{sola}{sigue}" style="--n:{t}">{"".join(htmls[i:i + t])}</div>'
        i += t
    return html_


def bloque_alterno(prof, ps, apertura, mostrar_fecha):
    """Las tres piezas del bloque de una sección en la portada, alternando dos disposiciones de una sección a la
    siguiente, como en los diarios de papel y en The Guardian (ADR 0041): con `apertura`, la más reciente con más
    cuerpo y su entradilla entera, y las otras dos al lado, solo con miniatura y titular; si no, las tres en fila
    con una miniatura del mismo tamaño y la entradilla recortada a la misma altura. Así las filas no dejan blancos
    debajo de las piezas cortas. Un filete vertical separa las columnas."""
    if apertura:
        grande = pieza(prof, ps[0], "menor alt-grande", 3, True, mostrar_fecha, sin_seccion=True, relleno=True)
        pequenas = "".join(pieza(prof, p, "menor alt-compacta", 3, True, mostrar_fecha, sin_seccion=True, relleno=True)
                           for p in ps[1:])
        return f'<div class="bloque-piezas alt-a">{grande}<div class="alt-lista">{pequenas}</div></div>'
    fila = "".join(pieza(prof, p, "menor alt-fila", 3, True, mostrar_fecha, sin_seccion=True, relleno=True) for p in ps)
    return f'<div class="bloque-piezas alt-b" style="--n:3">{fila}</div>'


def cuerpo_portada(prof, piezas, breves, mostrar_fecha, tira=""):
    """Como en un periódico: la apertura a todo el ancho, una fila de destacadas con dibujo,
    la viñeta y, debajo, un bloque por sección con su título a la izquierda (al estilo de
    The Guardian). Las secciones sin piezas no salen. En la portada, los breves del último número
    van arriba, tras las destacadas, como lo demás de hoy; los de días anteriores cierran abajo, con el
    rótulo «Breves anteriores» aunque el último número no traiga ninguno."""
    p0, resto = piezas[0], piezas[1:]
    hoy = [b for b in breves if b["fecha"] == p0["fecha"]] if mostrar_fecha else []
    breves = [b for b in breves if b not in hoy]
    # Como mucho tres destacadas con dibujo (las más recientes): la portada tiene que caber sin un scroll interminable.
    # En la portada, solo del último número: lo de días anteriores no se cuela entre lo de hoy, va a su sección
    resto = [p for p in resto if p.get("seccion") not in SECCIONES_FUERA] + [p for p in resto if p.get("seccion") in SECCIONES_FUERA]
    destacadas = [p for p in resto if p.get("importancia", 3) <= 2 and p.get("seccion") != "biblioteca"
                  and (not mostrar_fecha or p["fecha"] == p0["fecha"])][:3]
    # Si quedan huecos, los ocupan las demás piezas de hoy aunque sean menores: así no queda una suelta debajo.
    # La página de un número se compone igual que la parte de arriba de la portada (ADR 0045)
    destacadas += [p for p in resto if p not in destacadas and p["fecha"] == p0["fecha"]
                   and p.get("seccion") not in ["biblioteca"] + SECCIONES_FUERA][:3 - len(destacadas)]
    demas = [p for p in resto if p not in destacadas]
    # En la portada, todo lo de hoy va arriba: lo que no cabe entre las destacadas, también los
    # artículos de la Biblioteca, justo debajo en «Más del día»; los bloques, para los días anteriores
    # «Hace un año» (ADR 0040), con lo de hoy pero fuera de las filas: en su franja a todo el ancho, para que no
    # deje una fila de tres columnas con una sola pieza. Los de días anteriores no salen en la portada.
    hace_un_ano = next((p for p in demas if p.get("seccion") in SECCIONES_FUERA and p["fecha"] == p0["fecha"]), None)
    demas = [p for p in demas if p.get("seccion") not in SECCIONES_FUERA]
    mas_hoy = [p for p in demas if p["fecha"] == p0["fecha"]]
    demas = [p for p in demas if p not in mas_hoy]
    # Una sola pieza de más no se queda sola en una fila de tres (ADR 0045): sube a las destacadas, con su dibujo,
    # y las destacadas se reparten en filas (cuatro, en dos filas de dos)
    if len(mas_hoy) == 1:
        destacadas.append(mas_hoy.pop())
    html_ = pieza(prof, p0, "principal", 2, True, mostrar_fecha)
    if destacadas:
        html_ += en_filas([pieza(prof, p, "destacada", 2, True, mostrar_fecha, relleno=True) for p in destacadas], "fila-destacadas")
    if mas_hoy:
        # Sin título: cada pieza lleva su sección, y van en las columnas de las destacadas
        html_ += en_filas([pieza(prof, p, "menor", 3, False, mostrar_fecha) for p in mas_hoy], "fila-menores mas-dia")
    # En la portada, los breves del día y «Hace un año» van juntos tras las piezas de hoy; en la página de un
    # número, al final, con los breves del número (ADR 0040)
    breves_dia = ""
    if hoy:
        n = min(len(hoy), 2 if hace_un_ano else 3)
        breves_dia = f"""<section class="bloque sec-breves breves-dia" aria-labelledby="b-breves-dia">
  <h2 id="b-breves-dia" class="bloque-titulo"><a href="{prof}breves.html">{icono("breves")} {L["breves"]}</a></h2>
  <div class="bloque-piezas" style="--n:{n}">{bloque_breves(hoy, mostrar_fecha, en_bloque=True)}</div>
</section>"""
    if mostrar_fecha:
        html_ += breves_y_hace_un_ano(prof, breves_dia, hace_un_ano)
    html_ += tira
    visibles, ultima = 0, None
    for clave in ORDEN_SECCIONES:
        de_seccion = [p for p in demas if p.get("seccion") == clave]
        if not de_seccion:
            continue
        visibles += 1
        lista = "".join(pieza(prof, p, "menor", 3, False, mostrar_fecha, sin_seccion=True) for p in de_seccion)
        if mostrar_fecha and len(de_seccion) == POR_SECCION:
            # Alternando: tras una de tres en fila, una con apertura; tras una con apertura, tres en fila si sus
            # titulares son parejos
            apertura = ultima != "a" or not titulares_parejos(de_seccion)
            ultima = "a" if apertura else "b"
            lista = bloque_alterno(prof, de_seccion, apertura, mostrar_fecha)
        html_ += f"""<section class="bloque sec-{clave}" aria-labelledby="b-{clave}">
  <h2 id="b-{clave}" class="bloque-titulo"><a href="{prof}{clave}.html">{icono(clave)} {L["secciones"][clave]}</a></h2>
  {lista if lista.startswith('<div class="bloque-piezas') else f'<div class="bloque-piezas" style="--n:{min(len(de_seccion), 3)}">{lista}</div>'}
</section>"""
    sueltas = [p for p in demas if p.get("seccion") not in TODAS_SECCIONES]
    final = ""
    if sueltas or breves:
        hu_aqui = hace_un_ano if not mostrar_fecha else None
        lista = "".join(pieza(prof, p, "menor", 3, False, mostrar_fecha) for p in sueltas) + bloque_breves(breves, mostrar_fecha, en_bloque=True)
        final = f"""<section class="bloque sec-breves" aria-labelledby="b-breves">
  <h2 id="b-breves" class="bloque-titulo"><a href="{prof}breves.html">{icono("breves")} {L["breves_antes"] if mostrar_fecha else L["breves"]}</a></h2>
  <div class="bloque-piezas" style="--n:{min(len(sueltas) + (len(breves) if breves else 0), 2 if hu_aqui else 3)}">{lista}</div>
</section>"""
    html_ += final if mostrar_fecha else breves_y_hace_un_ano(prof, final, hace_un_ano)
    return html_


def bloque_vineta(prof, eds, fecha, en_archivo=False, pieza=None):
    """La tira del día, si la hay: solo falta si fallan los guiones o el juez, o si los cinco incumplen las prohibiciones.
    Con `pieza`, la de esa noticia, debajo de su artículo: solo si trata de ella, y sin «A partir de…»."""
    f = con_traduccion("vinetas", f"{fecha}.json")
    if not f.exists():
        return ""
    elegida = json.loads(f.read_text()).get("elegida")
    if not elegida or (pieza and elegida.get("pieza") != pieza):
        return ""
    d = next((x for x in eds if x["fecha"] == fecha), None)
    p = next((x for x in (d or {}).get("piezas", []) if x["id"] == elegida.get("pieza")), None)
    # La de un breve lo dice con su número («breve-3», ADR 0035); las antiguas, solo «breve»
    b = next((x for x in (d or {}).get("breves", []) if f'breve-{x.get("n")}' == elegida.get("pieza")), None)
    if p:
        origen_txt = f'{L["a_partir"]} <a href="{href(prof, p)}">{e(p["titular"])}</a>.'
    elif b:
        origen_txt = f'{L["a_partir"]} <a href="{prof}{ruta_breve(b)}">{e(titulo_breve(b))}</a>.'
    else:
        origen_txt = L["a_partir_dia"]
    return f"""<section class="vineta sec-vineta" aria-labelledby="t-vineta-{fecha}">
  <h2 id="t-vineta-{fecha}" class="vineta-titulo"><span>{"" if en_archivo else f'<a href="{prof}vineta.html">{icono("vineta")} {L["vineta_titulo"]}</a>'}</span> <span class="fecha-pieza">{fecha_corta(publicacion(fecha))}</span></h2>
  <div class="tira">{vineta.tira(elegida["guion"])}</div>
  {"" if pieza else f'<p class="vineta-origen">{origen_txt}</p>'}
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
    """El reportaje del domingo: a todo el ancho, como la franja editorial, con su infografía. El tiempo de lectura,
    junto al enlace: en el rótulo no cabía en el móvil y dejaba la fecha sola en una línea."""
    if not r:
        return ""
    return f"""<section class="editorial reportaje-franja" aria-labelledby="rep-{e(r["id"])}">
  <div class="texto">
    <p class="seccion"><span><a href="{prof}reportajes.html">{icono("reportaje")} {L["reportaje"]}</a></span> <span class="fecha-pieza">{fecha_corta(publicacion(r["fecha"]))}</span></p>
    <p class="antetitulo">{e(r["antetitulo"])}</p>
    <h2 id="rep-{e(r["id"])}" class="titular"><a href="{href(prof, r)}">{e(r["titular"])}</a></h2>
    <p class="entradilla">{e(r["entradilla"])}</p>
    <p class="leer"><a href="{href(prof, r)}">{L["leer_reportaje"]}</a> <span class="fecha-pieza">· {minutos_lectura(r)} {L["palabras"]}</span></p>
  </div>
  {ilustracion(r["fecha"], r)}
</section>"""


def franja_hace_un_ano(prof, p):
    """«Hace un año» (ADR 0040): un recuadro a todo el ancho con lo de hoy, como el de una columna fija en un
    periódico de papel: el díptico «Entonces / Ahora» a un lado y el texto al otro. Siempre llena el ancho, tenga
    el número una pieza o tres; sin dibujo, el texto ocupa todo el recuadro."""
    if not p:
        return ""
    ilu = ilustracion(p["fecha"], p)
    return f"""<section class="editorial hace-un-ano-franja sec-hace-un-ano{"" if ilu else " sin-ilu"}" aria-labelledby="hu-{e(p["id"])}">
  {ilu}
  <div class="texto">
    <p class="seccion"><span><a href="{prof}hace-un-ano.html">{icono("hace-un-ano")} {L["secciones"]["hace-un-ano"]}</a></span> <span class="fecha-pieza">{fecha_rotulo(p)}</span></p>
    <p class="antetitulo">{e(p.get("antetitulo", ""))}</p>
    <h2 id="hu-{e(p["id"])}" class="titular"><a href="{href(prof, p)}">{e(p["titular"])}</a></h2>
    <p class="entradilla">{e(p["entradilla"])}</p>
    <p class="leer"><a href="{href(prof, p)}">{L["leer_hace_un_ano"]}</a></p>
  </div>
</section>"""


def recuadro_hace_un_ano(prof, p):
    """«Hace un año» en pequeño, en un recuadro sepia junto a los breves (ADR 0040): el rótulo arriba y el díptico
    en miniatura, a un lado del titular y la entradilla, para que el recuadro no doble en altura a los breves. Sola, a todo el ancho, se veía demasiado grande para una pieza de memoria."""
    return f"""<section class="hace-un-ano-recuadro sec-hace-un-ano" aria-labelledby="hu-{e(p["id"])}">
  <p class="seccion"><span><a href="{prof}hace-un-ano.html">{icono("hace-un-ano")} {L["secciones"]["hace-un-ano"]}</a></span> <span class="fecha-pieza">{fecha_rotulo(p)}</span></p>
  {ilustracion(p["fecha"], p)}
  <p class="antetitulo">{e(p.get("antetitulo", ""))}</p>
  <h2 id="hu-{e(p["id"])}" class="titular"><a href="{href(prof, p)}">{e(p["titular"])}</a></h2>
  <p class="entradilla">{e(p["entradilla"])}</p>
  <p class="leer"><a href="{href(prof, p)}">{L["leer_hace_un_ano"]}</a></p>
</section>"""


def breves_y_hace_un_ano(prof, breves_html, hu):
    """Los breves y «Hace un año», en una fila de dos recuadros del mismo alto: los breves en dos tercios y la
    memoria en el otro. Sin breves, «Hace un año» en su franja ancha; sin «Hace un año», los breves solos."""
    if not hu:
        return breves_html
    if not breves_html:
        return franja_hace_un_ano(prof, hu)
    return f'<div class="fila-breves-hu">{breves_html}{recuadro_hace_un_ano(prof, hu)}</div>'


def reportaje_reciente(eds, fecha):
    """El último reportaje de la semana que acaba en `fecha`: el domingo abre la portada y, los
    días siguientes, sigue en ella tras las destacadas hasta que sale el siguiente."""
    desde = (datetime.date.fromisoformat(fecha) - datetime.timedelta(days=DIAS_PORTADA - 1)).isoformat()
    return next((d["reportaje"] for d in reversed(eds) if desde <= d["fecha"] <= fecha and d.get("reportaje")), None)


def descripcion_dia(dia, piezas):
    """Lo que trae un número, para los buscadores y para la vista previa al compartirlo: los titulares
    de sus piezas principales, con el reportaje delante si lo tiene. Hasta tres, enteros, sin pasar de
    300 caracteres (ADR 0039)."""
    elegidos = []
    for x in (([dia["reportaje"]] if dia.get("reportaje") else []) + list(piezas))[:3]:
        if elegidos and len(" · ".join(elegidos + [x["titular"]])) > 300:
            break
        elegidos.append(x["titular"])
    return " · ".join(elegidos) or L["lema"]


def pagina_portada(prof, ruta, eds, piezas, breves, fecha, cuenta, es_portada, ant="", sig=""):
    titulo = L["titulo"] if es_portada else f'{L["titulo"]}, {fecha_larga(publicacion(fecha))}'
    dia = next((x for x in eds if x["fecha"] == fecha), {})
    # En la portada, el de la semana; en la página de un día, solo el suyo. Arriba el día que sale;
    # los demás días, después de la viñeta, que es del número de hoy (ADR 0004)
    rep = reportaje_reciente(eds, fecha) if es_portada else dia.get("reportaje")
    arriba = bool(rep) and rep["fecha"] == fecha
    # La portada se describe con el lema del diario; la página de cada día, con lo que trae ese número
    descripcion = L["lema"] if es_portada else descripcion_dia(dia, piezas)
    return cabeza(titulo, prof, descripcion, ruta, portada=es_portada) + f"""<body class="pag-portada">
{cabecera(prof, ruta, fecha, cuenta, es_portada, h1=True if es_portada else "dia", activa="portada" if es_portada else None, ant=ant, sig=sig)}
<main class="portada">
{franja_reserva(dia)}
{franja_editorial(prof, dia)}
{franja_reportaje(prof, rep) if arriba else ""}
{cuerpo_portada(prof, piezas, breves, es_portada, bloque_vineta(prof, eds, fecha) + bloque_semana_video(prof, eds, fecha) + ("" if arriba else franja_reportaje(prof, rep)))}
</main>
{pie(prof, eds, None if es_portada else fecha)}
{SCRIPT_TEMA}
{SCRIPT_FILAS}
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
    compartir, plantilla = acciones(d["fecha"], p, ruta, d, eds, llevar=bool(p.get("seccion")))
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
    serie, ya_contados, otras = semana_repositorio(prof, p, eds)
    rot = rotulos(p, True, prof, boton=boton_columnas())
    linea, _, ante = rot.partition("\n  ")   # la línea de la sección, fuera de la cabeza; el antetítulo, dentro
    if not ante:   # sin sección: la línea del antetítulo lleva la fecha y el botón
        linea, ante = "", rot
    cab = cabeza_pieza(f"""{ante}
    <h1 class="titular">{sin_viuda(e(p["titular"]))}</h1>
    <p class="entradilla">{e(p.get("entradilla"))}</p>
    {serie}""", "" if len(p.get("recursos") or []) > 1 else ilustracion(d["fecha"], p, prof, ampliable=True))
    return cabeza(f'{p["titular"]} | {L["titulo"]}', prof, p.get("entradilla", ""), ruta,
                  datos=datos_noticia(p["titular"], ruta, d["fecha"], imagen_pieza(d["fecha"], p)[0])) + f"""<body class="pag-articulo">
{cabecera(prof, ruta, d["fecha"], d["numero"], False, h1=False)}
<main class="articulo en-columnas">
  <article{f' class="sec-{e(p["seccion"])}"' if p.get("seccion") else ""}{indexado(p.get("seccion") or "editorial", L["secciones"].get(p.get("seccion"), L["quees"]), d["fecha"])}>
    {linea}
    {cab}
    {ficha_doc}
    <div class="cuerpo">{cuerpo}{bloques}</div>
    {ya_contados}
    {f'<p class="correccion">{md(p["correccion"])}</p>' if p.get("correccion") else ""}
    {origen(p)}
    {compartir}
    {comprobado}
  </article>
  {plantilla}
  {bloque_vineta(prof, eds, d["fecha"], pieza=p["id"])}
  {otras}
  {mas_piezas(prof, eds, p)}
  {comentarios(ruta)}
  <p class="volver"><a href="{prof or "./"}">{L["volver"]}</a></p>
</main>
{pie(prof, eds, d["fecha"])}
{SCRIPT_TEMA}
</body>
</html>"""


def semana_repositorio(prof, p, eds):
    """Lo propio de «La semana del repositorio» (ADR 0008): la línea fija que dice qué es, la lista de
    lo que entró en la semana y ya tuvo su artículo, y las demás semanas. Vacío en las demás piezas."""
    if p.get("repositorio") != "semana":
        return "", "", ""
    serie = f'<p class="serie">{L["semana_repo"].format(repositorio=enlace(REPOSITORIO, L["repositorio_enlace"]))}</p>'
    por_id = {(x["fecha"], x["id"]): x for dd in eds for x in dd["piezas"]}
    items = []
    for y in sorted(p.get("ya_contados") or [], key=lambda y: (y.get("fecha", ""), y.get("breve", 0))):
        if y.get("breve"):
            destino = f'{prof}{e(y["fecha"])}/breve-{int(y["breve"])}.html'
        elif (y.get("fecha"), y.get("id")) in por_id:
            destino = href(prof, por_id[(y["fecha"], y["id"])])
        else:
            continue
        autoria = f' · {e(y["autoria"])}' if y.get("autoria") else ""
        items.append(f'<li><span class="fecha-pieza">{fecha_corta(publicacion(y["fecha"]))}</span>'
                     f'<a href="{destino}">{e(y["titulo"])}</a>{autoria}</li>')
    ya = (f'<section class="mas sec-vibecoding" data-pagefind-ignore aria-labelledby="ya-{e(p["id"])}"><h2 id="ya-{e(p["id"])}">{L["ya_contados"]}</h2>'
          f'<ul>{"".join(items)}</ul></section>') if items else ""
    demas = [x for dd in reversed(eds) for x in dd["piezas"]
             if x.get("repositorio") == "semana" and (x["fecha"], x["id"]) != (p["fecha"], p["id"])]
    otras = ""
    if demas:
        lis = "".join(f'<li><span class="fecha-pieza">{fecha_corta(publicacion(x["fecha"]))}</span>'
                      f'<a href="{href(prof, x)}">{e(x["titular"])}</a></li>' for x in demas)
        otras = f'<aside class="mas sec-vibecoding" aria-labelledby="t-semanas"><h2 id="t-semanas">{L["otras_semanas"]}</h2><ul>{lis}</ul></aside>'
    return serie, ya, otras


VACIO = ' class="vacio"'


def tabla(tb):
    """Una tabla de consulta dentro de un apartado del reportaje: {"titulo", "columnas", "filas", "nota"}.
    En el móvil cada fila se ve como una ficha, con el nombre de la columna delante (diario.css)."""
    if not tb or not tb.get("filas"):
        return ""
    cols = tb.get("columnas", [])
    cab = "".join(f'<th scope="col">{e(c)}</th>' for c in cols)
    filas = "".join("<tr>" + "".join(
        (f'<th scope="row">{md(x)}</th>' if j == 0 else f'<td data-col="{e(cols[j]) if j < len(cols) else ""}"{VACIO if x.strip() in ("—", "-", "") else ""}>{md(x)}</td>')
        for j, x in enumerate(f)) + "</tr>" for f in tb["filas"])
    titulo = f'<caption>{md(tb["titulo"])}</caption>' if tb.get("titulo") else ""
    nota = f'<p class="tabla-nota">{md(tb["nota"])}</p>' if tb.get("nota") else ""
    return f'<figure class="tabla"><table>{titulo}<thead><tr>{cab}</tr></thead><tbody>{filas}</tbody></table>{nota}</figure>'


def texto_tabla(tb):
    """Lo que la tabla aporta al buscador."""
    if not tb:
        return []
    return [tb.get("titulo", ""), tb.get("nota", "")] + [x for f in tb.get("filas", []) for x in f]


def articulo_reportaje(prof, ruta, d, r, eds):
    """El reportaje: apartados con ladillo, las claves al lado y, al final, las piezas de la semana."""
    apartados = []
    for i, a in enumerate(r["apartados"]):
        pars = a.get("parrafos", [])
        cap = ' class="capitular"' if i == 0 and pars and pars[0][:1].isalpha() else ""
        texto = "".join(f"<p{cap if j == 0 else ''}>{md(x)}</p>" for j, x in enumerate(pars))
        apartados.append((f'<h2 class="ladillo">{e(a["ladillo"])}</h2>' if a.get("ladillo") else "") + texto + tabla(a.get("tabla")))
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
    compartir, plantilla = acciones(d["fecha"], r, ruta, d, eds, reportaje=True)
    cab = cabeza_pieza(f"""<p class="antetitulo">{e(r.get("antetitulo"))}</p>
    <h1 class="titular">{sin_viuda(e(r["titular"]))}</h1>
    <p class="entradilla">{e(r.get("entradilla"))}</p>
    <p class="lectura fecha-pieza">{minutos_lectura(r)} {L["palabras"]}</p>""", ilustracion(d["fecha"], r, prof, ampliable=True))
    return cabeza(f'{r["titular"]} | {L["titulo"]}', prof, r.get("entradilla", ""), ruta,
                  datos=datos_noticia(r["titular"], ruta, d["fecha"], imagen_pieza(d["fecha"], r)[0])) + f"""<body class="pag-articulo">
{cabecera(prof, ruta, d["fecha"], d["numero"], False, h1=False)}
<main class="articulo reportaje en-columnas">
  <article class="sec-reportaje"{indexado("reportaje", L["reportajes"], d["fecha"])}>
    <p class="seccion"><span><a href="{prof}reportajes.html">{icono("reportaje")} {L["reportaje"]}</a></span> <span class="seccion-dcha">{boton_columnas()} <span class="fecha-pieza">{fecha_corta(publicacion(r["fecha"]))}</span></span></p>
    {cab}
    <div class="cuerpo">{"".join(apartados)}</div>
    {origen(dict(r, grupo=(r.get("mensaje") or {}).get("grupo")))}
    {compartir}
    {comprobado}
  </article>
  {plantilla}
  {relacionadas}
  {comentarios(ruta)}
  <p class="volver"><a href="{prof or "./"}">{L["volver"]}</a></p>
</main>
{pie(prof, eds, d["fecha"])}
{SCRIPT_TEMA}
</body>
</html>"""


def pagina_reportajes(eds, mes=None):
    return pagina_lista(eds, lista_reportajes(eds), mes)


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
    return cabeza(f'{titulo} | {L["titulo"]}', prof, texto_plano(b["texto"]), ruta_breve(b),
                  datos=datos_noticia(titulo, ruta_breve(b), d["fecha"])) + f"""<body class="pag-articulo">
{cabecera(prof, ruta_breve(b), d["fecha"], d["numero"], False, h1=False)}
<main class="articulo breve-pagina">
  <article{indexado("breves", L["breves"], d["fecha"])}>
    <p class="seccion"><span><a href="{prof}breves.html">{icono("breves")} {L["breves"]}</a></span> <span class="fecha-pieza">{fecha_corta(publicacion(b["fecha"]))}</span></p>
    <h1 class="solo-lector">{e(titulo)}</h1>
    <p class="breve-texto">{md(b["texto"])}</p>
    <p class="breve-enlaces">{" · ".join(enl)}</p>
    {compartir}
  </article>
  {bloque_vineta(prof, eds, d["fecha"], pieza=f'breve-{b["n"]}')}
  {mas_piezas(prof, eds, {"id": "", "fecha": "", "seccion": None})}
  {comentarios(ruta_breve(b))}
  <p class="volver"><a href="{prof or "./"}">{L["volver"]}</a></p>
</main>
{pie(prof, eds, d["fecha"])}
{SCRIPT_TEMA}
</body>
</html>"""


def d_href(d):
    return f'{d["fecha"]}/{e(d["editorial"]["id"])}.html'


INSTAGRAM = "https://www.instagram.com/comunidad.iaeducativa/"


def cargar_videos():
    """Los vídeos del diario (videos/*.json, ADR 0016), del más reciente al más antiguo. Cada uno
    tiene su vídeo y su portada por idioma; si falta el del idioma, va el castellano y se dice.
    El vídeo de los que ya están en Internet Archive («archive» en el JSON, ADR 0037) no hace falta
    en local; la portada, sí."""
    vs = []
    for f in sorted((RAIZ / "videos").glob("*.json")):
        v = json.loads(f.read_text())
        es = v["archivos"]["es"]
        if (RAIZ / "videos" / es["poster"]).exists() and (v.get("archive") or (RAIZ / "videos" / es["video"]).exists()):
            vs.append(v)
    return sorted(vs, key=lambda v: v["publicado"], reverse=True)


def url_video(prof, v, arch):
    """De Internet Archive si ya está allí (ADR 0037); si no, la copia del sitio."""
    if v.get("archive"):
        return f'https://archive.org/download/{e(v["archive"])}/{e(arch["video"])}'
    return f'{recursos(prof)}videos/{e(arch["video"])}'


def texto_video(v, campo):
    x = v.get(campo, {})
    return x.get(L["codigo"]) or x.get("es")


def bloque_video(prof, v, titulo_h="h2", enlace_propio=True, titulo=None):
    """Un vídeo vertical, sin reproducción automática, con su portada y lo que dice en pantalla."""
    codigo = L["codigo"]
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
    <source src="{url_video(prof, v, arch)}" type="video/mp4">
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
    c = L["codigo"]
    nombre = lambda d: L["meses"][d.month - 1]  # noqa: E731
    mes = lambda d: de_mes(nombre(d))  # noqa: E731
    mismo = ini.month == fin.month
    if c == "en":
        return f"{ini.day}–{fin.day} {nombre(fin)}" if mismo else f"{ini.day} {nombre(ini)} – {fin.day} {nombre(fin)}"
    if c == "eu":
        return (f"{mayus(nombre(fin))}ren {ini.day}–{fin.day}" if mismo
                else f"{mayus(nombre(ini))}ren {ini.day} – {nombre(fin)}ren {fin.day}")
    if c == "gl":
        return f"Do {ini.day} ao {fin.day} {mes(fin)}" if mismo else f"Do {ini.day} {mes(ini)} ao {fin.day} {mes(fin)}"
    vocal = lambda n: c == "ca" and n in (1, 11)  # noqa: E731   en catalán, «de l'1», «a l'11»
    del_ = "De l'" if vocal(ini.day) else "Del "
    al_ = "a l'" if vocal(fin.day) else "al "
    if mismo:
        return f"{del_}{ini.day} {al_}{fin.day} {mes(fin)}"
    return f"{del_}{ini.day} {mes(ini)} {al_}{fin.day} {mes(fin)}"


def bloque_semana_video(prof, eds, fecha):
    """«La semana en vídeo», en el número del domingo, como franja a todo el ancho (como el
    reportaje): el vídeo y, al lado, las piezas que salen en él, enlazadas a su artículo."""
    v = next((x for x in cargar_videos() if x.get("tipo") == "semana" and x.get("dia") == fecha), None)
    if not v:
        return ""
    codigo = L["codigo"]
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
    <source src="{url_video(prof, v, arch)}" type="video/mp4">
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


# «Las comunidades» en «La redacción»: quién está en cada grupo y en varios a la vez, con las cifras que
# deja el Bot de IA Educativa en comunidades/AAAA-MM-DD.json (la última). Tres círculos iguales: con
# tres no se pueden ajustar a la vez todas las áreas a sus cifras, y las zonas pequeñas no se leerían.
# Cada cifra, en el centro de su zona (calculado: la media de sus puntos, con la cifra centrada en altura).
TXT_COMUNIDADES = {
    "es": {"pie": "{n} personas en tres comunidades", "personas": "miembros", "total": "personas distintas", "fecha": "a {f}",
           "nota": "{fecha}.",
           "alt": "Diagrama de los tres grupos de Telegram del diario, con tres círculos que se cruzan. ChatGPT-IA-edu tiene {chatgpt} miembros; Vibe Coding Educativo, {vce}, y EduMedia-IAG, {edumedia}. Solo en ChatGPT-IA-edu están {s_chatgpt}; solo en Vibe Coding Educativo, {s_vce}, y solo en EduMedia-IAG, {s_edumedia}. En ChatGPT-IA-edu y Vibe Coding Educativo, sin EduMedia-IAG, {chatgpt_vce}; en ChatGPT-IA-edu y EduMedia-IAG, sin Vibe Coding Educativo, {chatgpt_edumedia}; en Vibe Coding Educativo y EduMedia-IAG, sin ChatGPT-IA-edu, {vce_edumedia}, y en los tres, {tres}. En total, {total} personas distintas, a {f}."},
    "ca": {"pie": "{n} persones en tres comunitats", "personas": "membres", "total": "persones diferents", "fecha": "a {f}",
           "nota": "{fecha}.",
           "alt": "Diagrama dels tres grups de Telegram del diari, amb tres cercles que s'encreuen. ChatGPT-IA-edu té {chatgpt} membres; Vibe Coding Educativo, {vce}, i EduMedia-IAG, {edumedia}. Només a ChatGPT-IA-edu n'hi ha {s_chatgpt}; només a Vibe Coding Educativo, {s_vce}, i només a EduMedia-IAG, {s_edumedia}. A ChatGPT-IA-edu i Vibe Coding Educativo, sense EduMedia-IAG, {chatgpt_vce}; a ChatGPT-IA-edu i EduMedia-IAG, sense Vibe Coding Educativo, {chatgpt_edumedia}; a Vibe Coding Educativo i EduMedia-IAG, sense ChatGPT-IA-edu, {vce_edumedia}, i als tres, {tres}. En total, {total} persones diferents, a {f}."},
    "gl": {"pie": "{n} persoas en tres comunidades", "personas": "membros", "total": "persoas distintas", "fecha": "a {f}",
           "nota": "{fecha}.",
           "alt": "Diagrama dos tres grupos de Telegram do diario, con tres círculos que se cruzan. ChatGPT-IA-edu ten {chatgpt} membros; Vibe Coding Educativo, {vce}, e EduMedia-IAG, {edumedia}. Só en ChatGPT-IA-edu están {s_chatgpt}; só en Vibe Coding Educativo, {s_vce}, e só en EduMedia-IAG, {s_edumedia}. En ChatGPT-IA-edu e Vibe Coding Educativo, sen EduMedia-IAG, {chatgpt_vce}; en ChatGPT-IA-edu e EduMedia-IAG, sen Vibe Coding Educativo, {chatgpt_edumedia}; en Vibe Coding Educativo e EduMedia-IAG, sen ChatGPT-IA-edu, {vce_edumedia}, e nos tres, {tres}. En total, {total} persoas distintas, a {f}."},
    "eu": {"pie": "{n} pertsona hiru komunitatetan", "personas": "kide", "total": "pertsona desberdin", "fecha": "{f}n",
           "nota": "{fecha}.",
           "alt": "Egunkariaren Telegrameko hiru taldeen diagrama, elkar gurutzatzen diren hiru zirkulurekin. ChatGPT-IA-edu taldeak {chatgpt} kide ditu; Vibe Coding Educativo taldeak, {vce}, eta EduMedia-IAG taldeak, {edumedia}. ChatGPT-IA-edu taldean soilik {s_chatgpt} daude; Vibe Coding Educativo taldean soilik, {s_vce}, eta EduMedia-IAG taldean soilik, {s_edumedia}. ChatGPT-IA-edu eta Vibe Coding Educativo taldeetan, EduMedia-IAG gabe, {chatgpt_vce}; ChatGPT-IA-edu eta EduMedia-IAG taldeetan, Vibe Coding Educativo gabe, {chatgpt_edumedia}; Vibe Coding Educativo eta EduMedia-IAG taldeetan, ChatGPT-IA-edu gabe, {vce_edumedia}, eta hiruretan, {tres}. Guztira, {total} pertsona desberdin, {f}."},
    "en": {"pie": "{n} people in three communities", "personas": "members", "total": "different people", "fecha": "as of {f}",
           "nota": "{fecha}.",
           "alt": "Diagram of the paper's three Telegram groups, with three overlapping circles. ChatGPT-IA-edu has {chatgpt} members; Vibe Coding Educativo, {vce}; and EduMedia-IAG, {edumedia}. Only in ChatGPT-IA-edu: {s_chatgpt}; only in Vibe Coding Educativo: {s_vce}; only in EduMedia-IAG: {s_edumedia}. In ChatGPT-IA-edu and Vibe Coding Educativo but not EduMedia-IAG: {chatgpt_vce}; in ChatGPT-IA-edu and EduMedia-IAG but not Vibe Coding Educativo: {chatgpt_edumedia}; in Vibe Coding Educativo and EduMedia-IAG but not ChatGPT-IA-edu: {vce_edumedia}; in all three: {tres}. In total, {total} different people, as of {f}."},
}


def cifra(n):
    """4061 sin punto (RAE e IEC: hasta cuatro cifras, sin separador); de cinco en adelante, espacio fino. En inglés, coma."""
    if L["codigo"] == "en":
        return f"{n:,}"
    return str(n) if n < 10000 else f"{n:,}".replace(",", " ")


def fecha_dia(iso):
    """«6 de noviembre de 2026», sin el día de la semana."""
    d = datetime.date.fromisoformat(iso)
    if L["codigo"] == "en":
        return f"{d.day} {L['meses'][d.month - 1]} {d.year}"
    if L["codigo"] == "eu":
        return f"{d.year}ko {L['meses'][d.month - 1]}ren {d.day}a"
    return f"{fecha_corta(iso)} de {d.year}"


MESES_ABREV = {"es": "ene feb mar abr may jun jul ago sept oct nov dic", "ca": "gen. febr. març abr. maig juny jul. ag. set. oct. nov. des.",
               "gl": "xan feb mar abr maio xuño xul ago set out nov dec", "eu": "urt. ots. mar. api. mai. eka. uzt. abu. ira. urr. aza. abe.",
               "en": "Jan Feb Mar Apr May Jun Jul Aug Sept Oct Nov Dec"}


def fecha_abrev(iso):
    """«6 nov. 2026» (en euskera, «2026 aza. 6»; en inglés, «6 Nov 2026»)."""
    d = datetime.date.fromisoformat(iso)
    mes = MESES_ABREV[L["codigo"]].split()[d.month - 1]
    if L["codigo"] in ("es", "gl"):
        mes += "."
    if L["codigo"] == "eu":
        return f"{d.year} {mes} {d.day}"
    return f"{d.day} {mes} {d.year}"


def comunidades_datos():
    """Las últimas cifras de los grupos (comunidades/AAAA-MM-DD.json), o None si aún no hay."""
    archivos = sorted((RAIZ / "comunidades").glob("????-??-??.json"))
    return json.loads(archivos[-1].read_text()) if archivos else None


def emblema():
    """Los tres círculos sin cifras: el emblema de las comunidades del diario, para el pie."""
    return ('<svg class="emblema" viewBox="0 0 64 60" aria-hidden="true">'
            '<circle class="venn venn-chatgpt" cx="24" cy="22" r="17"/><circle class="venn venn-vce" cx="40" cy="22" r="17"/>'
            '<circle class="venn venn-edumedia" cx="32" cy="36" r="17"/></svg>')


def pie_comunidades(prof):
    """En el pie, bajo los grupos: el emblema y el total de personas, que lleva al diagrama de «La redacción»."""
    c = comunidades_datos()
    if not c:
        return ""
    texto = TXT_COMUNIDADES[L["codigo"]]["pie"].format(n=cifra(c["total"]))
    return f'<p class="pie-comunidades"><a href="{prof}redaccion.html#comunidades">{emblema()}<span>{texto}</span></a></p>'


GIRO_COMUNIDADES = 30   # grados: así el nombre de EduMedia-IAG no cae encima del total


def comunidades_figura(giro=None):
    """El diagrama de los tres grupos con sus cifras, o nada si aún no hay cifras. Se dibuja derecho
    (ChatGPT-IA-edu y Vibe Coding Educativo arriba, EduMedia-IAG abajo) y se gira entero alrededor de su
    centro; los textos siguen horizontales y cada nombre va por fuera de su círculo, en su dirección."""
    import math
    c = comunidades_datos()
    if not c:
        return ""
    T, g, z = TXT_COMUNIDADES[L["codigo"]], c["grupos"], c["zonas"]
    f = T["fecha"].format(f=fecha_dia(c["fecha"]))
    n = lambda k: cifra(z[k])
    alt = T["alt"].format(chatgpt=cifra(g["chatgpt"]), vce=cifra(g["vce"]), edumedia=cifra(g["edumedia"]),
                          s_chatgpt=n("chatgpt"), s_vce=n("vce"), s_edumedia=n("edumedia"), chatgpt_vce=n("chatgpt+vce"),
                          chatgpt_edumedia=n("chatgpt+edumedia"), vce_edumedia=n("vce+edumedia"), tres=n("tres"),
                          total=cifra(c["total"]), f=f)
    a = math.radians(GIRO_COMUNIDADES if giro is None else giro)
    cx0, cy0, R = 300, 820 / 3, 150          # centro del conjunto (el de los tres centros) y radio
    def gira(x, y):
        dx, dy = x - cx0, y - cy0
        return cx0 + dx * math.cos(a) - dy * math.sin(a), cy0 + dx * math.sin(a) + dy * math.cos(a)
    # Vibe Coding Educativo, el nombre más largo, arriba (centrado, no sobresale); ChatGPT-IA-edu, a la derecha
    centros = {k: gira(x, y) for k, (x, y) in {"vce": (225, 230), "chatgpt": (375, 230), "edumedia": (300, 360)}.items()}
    # El centro de cada zona (la media de sus puntos, calculada con el dibujo derecho)
    zonas = {"vce": (164, 195), "chatgpt": (436, 195), "edumedia": (300, 431), "chatgpt+vce": (300, 168),
             "vce+edumedia": (208, 327), "chatgpt+edumedia": (392, 327), "tres": (300, 274)}
    partes, xs, ys = [], [], []
    for k, (x, y) in centros.items():
        partes.append(f'<circle class="venn venn-{k}" cx="{x:.0f}" cy="{y:.0f}" r="{R}"/>')
        xs += [x - R, x + R]; ys += [y - R, y + R]
    for k, (x, y) in zonas.items():
        x, y = gira(x, y)
        cl = "num num-tres" if k == "tres" else "num"
        partes.append(f'<text class="{cl}" x="{x:.0f}" y="{y + (13 if k == "tres" else 12):.0f}" text-anchor="middle">{n(k)}</text>')
    for k, (x, y) in centros.items():
        d = math.hypot(x - cx0, y - cy0); ux, uy = (x - cx0) / d, (y - cy0) / d
        px, py = cx0 + ux * (d + R + 16), cy0 + uy * (d + R + 16)
        lineas = [(GRUPOS[k][0], f"lbl nom-{k}"), (f"{cifra(g[k])} {T['personas']}", "lbl")]
        ancho = max(len(t) for t, _ in lineas) * 14   # ancho de una letra a 28 px, medido (11,9 a 14,8): por lo alto
        anc = "start" if ux > 0.55 else "end" if ux < -0.55 else "middle"   # arriba y abajo, centrado
        y1 = py + 28 if uy > 0.5 else py - 48 if uy < -0.5 else py - 4
        for i, (t, cl) in enumerate(lineas):
            partes.append(f'<text class="{cl}" x="{px:.0f}" y="{y1 + 32 * i:.0f}" text-anchor="{anc}">{t}</text>')
        x0 = px if anc == "start" else px - ancho if anc == "end" else px - ancho / 2
        xs += [x0, x0 + ancho]; ys += [y1 - 24, y1 + 40]
    total = f"{T['total']} ({fecha_abrev(c['fecha'])})"
    mx, ancho_t = (min(xs) + max(xs)) / 2, len(total) * 11.8
    yt = max(ys) + 66
    partes.append(f'<text class="total" x="{mx:.0f}" y="{yt:.0f}" text-anchor="middle">{cifra(c["total"])}</text>')
    partes.append(f'<text class="lbl" x="{mx:.0f}" y="{yt + 38:.0f}" text-anchor="middle">{total}</text>')
    x0, x1 = min(min(xs), mx - ancho_t / 2) - 10, max(max(xs), mx + ancho_t / 2) + 10
    y0, y1 = min(ys) - 10, yt + 52
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}" role="img" aria-label="{e(alt)}">\n  '
           + "\n  ".join(partes) + "\n</svg>")
    return f'<figure class="ilu comunidades">{boton_ampliar(svg, e(alt))}</figure>'


CORREO_CONTACTO = "jjdeharo@gmail.com"   # el de contacto de la ficha de Google Play (ADR 0042)


def pagina_redaccion(eds):
    """«La redacción»: quién hace el diario, empezando por el equipo de agentes y su organigrama."""
    R = L["redaccion"]
    grupos = {k: enlace("https://t.me/" + a, n) for k, (n, a) in GRUPOS.items()}
    grupos.update(juanjo=enlace(WEB_JUANJO, "Juan José de Haro"), raul=enlace(WEB_RAUL, "Raül Torres"),
                  aepd=enlace(AEPD_MEDICION, "Agencia Española de Protección de Datos"),
                  reportajes=f'<a href="reportajes.html">{L["reportajes"]}</a>',
                  biblioteca=enlace(TEMA_BIBLIOTECA, L["biblioteca_enlace"]), seccion_bib=f'<a href="biblioteca.html">{L["secciones"]["biblioteca"]}</a>',
                  repositorio=enlace(REPOSITORIO, L["repositorio_enlace"]), seccion_vc=f'<a href="vibecoding.html">{L["secciones"]["vibecoding"]}</a>',
                  codigo=enlace(CODIGO, L["codigo_enlace"]),
                  # El contacto tiene página propia (ADR 0051); aquí queda un apartado breve que lleva a ella
                  pagina_contacto=f'<a href="contacto.html">{L["contacto"]["enlace"]}</a>',
                  pagina_semana=f'<a href="semana/">{R["pagina_semana"]}</a>',
                  hemeroteca=f'<a href="archivo.html">{L["hemeroteca"]}</a>',
                  hace_un_ano=f'<a href="hace-un-ano.html">{L["secciones"]["hace-un-ano"]}</a>')
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
    # El diagrama de los grupos, tras la sección que los presenta (la que nombra a {chatgpt})
    venn = comunidades_figura()
    # La de las visitas es también la política de privacidad que enlaza la ficha de Google Play (ADR 0042)
    apartados = [(f'<h2 id="comunidades">{t}</h2>{venn}' if "{chatgpt}" in x else
                  f'<h2 id="privacidad">{t}</h2>' if "{aepd}" in x else
                  f'<h2 id="contacto">{t}</h2>' if "{pagina_contacto}" in x else f"<h2>{t}</h2>") + f"<p>{x.format(**grupos)}</p>"
                 for t, x in R["secciones"]]
    # En el ordenador, en columnas como las noticias (ADR 0047): los apartados van en bloques por tema (cómo
    # trabajan los agentes, las secciones del diario, quién lo lee y quién lo hace), cada uno a lo ancho y con
    # el texto en columnas, para que ningún bloque pase de una pantalla ni un apartado corto quede repartido
    # en tres columnas de una línea. En una columna y en el móvil, todo sigue una detrás de otro.
    usados = {i for bloque in BLOQUES_REDACCION for i in bloque}
    bloques = [list(b) for b in BLOQUES_REDACCION] + [[i for i in range(len(apartados)) if i not in usados]]
    resto = "".join(f'<section class="red-bloque">{"".join(apartados[i] for i in b if i < len(apartados))}</section>'
                    for b in bloques if any(i < len(apartados) for i in b))
    enlace_pres = f'<p class="presentacion"><a href="{d_href(pres)}">{L["presentacion"]}</a></p>' if pres else ""
    cab = cabecera("", "redaccion.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False, activa="redaccion")
    cabeza_red = cabeza_pieza(f"""<p class="antetitulo con-fecha"><span class="seccion-dcha">{boton_columnas()}</span></p>
<h1 class="titular">{L["quees"]}</h1>
<p class="entradilla">{R["intro"]}</p>""", "")
    return cabeza(f'{L["quees"]} | {L["titulo"]}', "", R["intro"], "redaccion.html") + f"""<body class="pag-que-es">
{cab}
<main class="articulo que-es redaccion en-columnas">
{cabeza_red}
<section class="red-proceso">
{organigrama}
<div class="red-texto">
<h2>{R["proceso_titulo"]}</h2>
<p>{R["proceso_intro"]}</p>
<ol class="proceso">{pasos}</ol>
<p>{R["proceso_pie"]}</p>
</div>
</section>
<section class="red-bloque">
<h2>{R["equipo_titulo"]}</h2>
<ul class="equipo">{equipo}</ul>
<p>{R["equipo_pie"]}</p>
</section>
{resto}
{enlace_pres}
<p class="volver"><a href="./">{L["volver"]}</a></p>
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


ICONO_CORREO = ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/>'
                '<rect x="2" y="4" width="20" height="16" rx="2"/></svg>')   # mail


def pagina_contacto(eds):
    """La página de contacto (ADR 0051): el correo a la vista y las otras vías. Página propia y con enlace en
    el pie de todas las demás, como pide Google Play a una app de noticias: como apartado de «La redacción»,
    el revisor no la encontró. Su dirección es la de la declaración de noticias de la ficha: no se renombra."""
    C = L["contacto"]
    # El correo del contacto del desarrollador en Google Play, que la ficha ya publica; en entidades HTML,
    # que se leen igual y lo esconden de los recolectores más simples (ADR 0042)
    correo = "".join(f"&#{ord(ch)};" for ch in CORREO_CONTACTO)
    otras = C["otras"].format(incidencias=enlace("https://github.com/diarioiaeducativa/periodico/issues", "GitHub"))
    return cabeza(f'{C["titulo"]} | {L["titulo"]}', "", C["txt"], "contacto.html") + f"""<body class="pag-que-es">
{cabecera("", "contacto.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="articulo que-es contacto">
<h1 class="titular">{C["titulo"]}</h1>
<p class="entradilla">{C["txt"]}</p>
<p class="contacto-correo">{ICONO_CORREO}<span class="contacto-rotulo">{C["correo"]}</span> <a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;{correo}">{correo}</a></p>
<p>{otras}</p>
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


def pagina_seccion(eds, clave, mes=None):
    return pagina_lista(eds, lista_seccion(eds, clave), mes)


# --- La semana y el mes (ADR 0034) -------------------------------------------------------------------
# La hemeroteca se agrupa por semanas ISO, de lunes a domingo, según el día de los mensajes (d["fecha"]):
# es la misma semana que cubren el pódcast y el vídeo de NotebookLM de cada grupo, que deja el proceso del
# boletín en multimedia/AAAA-WW.json. Una semana es del mes en que cae su jueves, como manda la ISO 8601,
# así ninguna sale en dos meses.
BOLETINES = {   # los boletines semanales que el diario sustituye, en su web de siempre (ADR 0034)
    "chatgpt": "https://chatgpt-ia-edu.github.io/boletin/",
    "vce": "https://vibe-coding-educativo.github.io/boletin/",
    "edumedia": "https://edumedia-iag.github.io/boletin_semanal/",   # el que hacía Raül Torres
}
ICONOS["semana"] = ('<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>'
                    '<path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/>')   # calendar-days


def semana_de(fecha):
    y, w, _ = datetime.date.fromisoformat(fecha).isocalendar()
    return f"{y}-{w:02d}"


def lunes_de(sem):
    y, w = map(int, sem.split("-"))
    return datetime.date.fromisocalendar(y, w, 1)


def mes_de(sem):
    return (lunes_de(sem) + datetime.timedelta(days=3)).isoformat()[:7]


def por_semanas(eds):
    """{semana: [días]}, de la más antigua a la más reciente."""
    sems = {}
    for d in eds:
        sems.setdefault(semana_de(d["fecha"]), []).append(d)
    return sems


def titulo_semana(sem):
    """«Semana 45: del 2 al 8 de noviembre»: el número ISO de la semana, el mismo que llevan los vídeos y
    los pódcast de NotebookLM y los boletines de antes, y sus días."""
    r = rango_semana(sem)
    if L["codigo"] in ("es", "ca", "gl", "eu"):
        r = r[0].lower() + r[1:]
    return f'{L["semana_n"].format(n=int(sem.split("-")[1]))}: {r}'


def rango_semana(sem):
    """«Del 2 al 8 de noviembre»: los días de los mensajes."""
    return fechas_semana((lunes_de(sem) + datetime.timedelta(days=6)).isoformat())


def numeros(ds):
    ns = [d["numero"] for d in ds if d.get("numero")]
    if not ns:
        return ""
    return f'{L["num"]}&nbsp;{ns[0]}' + (f"–{ns[-1]}" if len(ns) > 1 else "")


def cargar_multimedia(sem):
    """El pódcast y el vídeo de NotebookLM de cada grupo, si el boletín ya los ha dejado."""
    f = RAIZ / "multimedia" / f"{sem}.json"
    try:
        return json.loads(f.read_text()).get("grupos") or {}
    except (OSError, ValueError):
        return {}


def id_youtube(url):
    m = re.search(r"(?:youtu\.be/|[?&]v=|/embed/|/shorts/)([\w-]{11})", url or "")
    return m.group(1) if m else None


def grupo_pieza(x):
    return x.get("grupo") or (x.get("mensaje") or {}).get("grupo") or ""


def bloque_notebook(sem, m):
    """Pódcast y vídeo de NotebookLM de cada grupo. El vídeo no se carga hasta que se pulsa (youtube-nocookie):
    abrir la página no avisa a YouTube. El audio, sin precarga."""
    # Los boletines semanales de antes (ADR 0034): cada grupo, el suyo; el filtro deja solo el elegido
    anteriores = (f'<p class="nb-anteriores">{L["nb_anteriores"]}: '
                  + "".join(f'<span data-grupo="{g}">{enlace(u, GRUPOS[g][0])}</span>' for g, u in BOLETINES.items())
                  + "</p>")
    if not m:
        domingo = lunes_de(sem) + datetime.timedelta(days=6)
        if datetime.date.today() <= domingo + datetime.timedelta(days=2):
            return f'<p class="nb-pendiente">{icono("video")} {L["nb_pendiente"]}</p>{anteriores.replace("nb-anteriores", "nb-anteriores suelta", 1)}'
        return anteriores.replace("nb-anteriores", "nb-anteriores suelta", 1)
    fichas = []
    for g, (nombre, _) in GRUPOS.items():
        x = m.get(g) or {}
        if not (x.get("video") or x.get("podcast") or x.get("podcast_mp3")):
            continue
        vid = id_youtube(x.get("video"))
        video = ""
        if vid:
            video = (f'<div class="nb-video"><button type="button" class="nb-play" data-yt="{e(vid)}" '
                     f'aria-label="{e(L["nb_ver"].format(g=nombre))}">{PLAY}<span>{L["nb_video"]}</span></button></div>')
        resumen = f'<p class="nb-resumen">{e(x["resumen"])}</p>' if x.get("resumen") else ""
        audio = ""
        if x.get("podcast_mp3"):
            audio = (f'<p class="nb-rotulo">{L["nb_podcast"]}</p>'
                     f'<audio controls preload="none" src="{e(x["podcast_mp3"])}"></audio>')
        enlaces = []
        if x.get("video"):
            enlaces.append(enlace(x["video"], L["nb_youtube"]))
        if x.get("podcast"):
            enlaces.append(enlace(x["podcast"], L["nb_archive"]))
        fichas.append(f"""<article class="nb-grupo" data-grupo="{g}">
  <h3>{e(nombre)}</h3>
  {video}{resumen}{audio}
  <p class="nb-enlaces">{" · ".join(enlaces)}</p>
</article>""")
    if not fichas:
        return anteriores.replace("nb-anteriores", "nb-anteriores suelta", 1)
    es = f' {L["nb_es"]}' if L["nb_es"] else ""
    return f"""<section class="notebook" aria-labelledby="t-nb">
  <h2 id="t-nb">{icono("video")} {L["nb_h"]}</h2>
  <p class="nb-txt">{L["nb_txt"]}{es}</p>
  <div class="nb-grupos">{"".join(fichas)}</div>
  {anteriores}
</section>"""


ICONOS["hace-un-ano"] = ('<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>')   # rotate-ccw-clock (ADR 0040)
ICONOS["comentario"] = ('<path d="M14 14a2 2 0 0 0 2-2V8h-2"/><path d="M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z"/>'
                        '<path d="M8 14a2 2 0 0 0 2-2V8H8"/>')   # message-square-quote


def bloque_comentario(sem):
    """Los comentarios de la semana (ADR 0038): lo más importante de lo que contó el diario, debajo del pódcast
    y el vídeo. El general se ve con «Todos»; el de cada grupo, al elegir ese grupo (SCRIPT_SEMANA). Sin
    comentario, no sale nada."""
    f = con_traduccion("comentario-semana", f"{sem}.json")
    try:
        c = json.loads(f.read_text())
    except (OSError, ValueError):
        return ""
    if not c.get("hay_comentario"):
        return ""

    def uno(b, rotulo, atributos):
        if not (b and b.get("parrafos")):
            return ""
        pars = "".join(f"<p>{md(x)}</p>" for x in b["parrafos"])
        return (f'<article{atributos}><h2>{icono("comentario")} {e(rotulo)}</h2>'
                f'<h3>{e(b.get("titulo", ""))}</h3>{pars}</article>')

    # El rótulo dice de quién es: «Lo más importante de la semana» con todos, «… en ChatGPT-IA-edu» con un grupo
    articulos = uno(c.get("general"), L["cs_h"], ' class="cs-general"') + "".join(
        uno((c.get("grupos") or {}).get(g), L["cs_h_g"].format(g=nombre), f' class="cs-grupo" data-cs="{g}" hidden')
        for g, (nombre, _) in GRUPOS.items())
    if not articulos:
        return ""
    return f"""<section class="comentario-semana">
  {articulos}
  <p class="cs-nota">{L["cs_nota"]}</p>
</section>"""


SCRIPT_SEMANA = """<script>
(function(){
  var bs=document.querySelectorAll('.filtro-grupo button'),vacio=document.querySelector('.sin-grupo'),G=['chatgpt','vce','edumedia'];
  function poner(v,guardar){
    if(G.indexOf(v)<0)v='';
    bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.g===v?'true':'false');});
    document.querySelectorAll('[data-grupo]').forEach(function(x){x.hidden=!!v&&x.dataset.grupo!==v;});
    document.querySelectorAll('.semana-seccion,.notebook').forEach(function(s){s.hidden=!s.querySelector('[data-grupo]:not([hidden])');});
    if(vacio)vacio.hidden=!v||!!document.querySelector('.semana-seccion:not([hidden])');
    document.querySelectorAll('.cs-general').forEach(function(x){x.hidden=!!v;});
    document.querySelectorAll('.cs-grupo').forEach(function(x){x.hidden=x.dataset.cs!==v;});
    document.querySelectorAll('.comentario-semana').forEach(function(s){s.hidden=!s.querySelector('article:not([hidden])');});
    if(guardar){try{var u=new URL(location.href);if(v)u.searchParams.set('grupo',v);else u.searchParams.delete('grupo');history.replaceState(null,'',u);}catch(_){}}
  }
  bs.forEach(function(b){b.addEventListener('click',function(){poner(b.dataset.g,true);});});
  var g='';try{g=new URLSearchParams(location.search).get('grupo')||'';}catch(_){}
  poner(g,false);
  document.querySelectorAll('.nb-play').forEach(function(b){b.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.yt+'?autoplay=1&rel=0';
    f.title=b.getAttribute('aria-label');f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;
    b.parentNode.replaceChild(f,b);
  });});
})();
</script>"""


def item_semana(prof, x, sale):
    return (f'<li data-grupo="{grupo_pieza(x)}"><span class="fecha-pieza">{fecha_corta(sale)}</span> '
            f'<a href="{prof}{x["fecha"]}/{e(x["id"])}.html">{e(x["titular"])}</a></li>')


def dias_lista(prof, ds):
    items = []
    for d in reversed(ds):
        sale = publicacion(d["fecha"])
        num = f' <span class="num">· {L["num"]}&nbsp;{d["numero"]}</span>' if d["numero"] else ""
        abre = d["reportaje"] if d.get("reportaje") else d["piezas"][0]
        marca = f'<span class="rep">{L["reportaje"]}</span>' if d.get("reportaje") else ""
        items.append(f'<li><a href="{prof}{d["fecha"]}/">{mayus(fecha_larga(sale))}</a>{num}'
                     f'<span class="abre">{marca}<a href="{prof}{d["fecha"]}/{e(abre["id"])}.html">{e(abre["titular"])}</a></span></li>')
    return f'<ul class="dias">{"".join(items)}</ul>'


def pagina_semana(eds, sem, anterior, siguiente):
    prof = "../../"
    ruta = f"semana/{sem}/"
    ds = por_semanas(eds)[sem]
    rango = titulo_semana(sem)
    m = cargar_multimedia(sem)
    secciones = []
    for c in ORDEN_SECCIONES:
        xs = [x for d in ds for x in d["piezas"] if x.get("seccion") == c]
        if xs:
            items = "".join(item_semana(prof, x, publicacion(x["fecha"])) for x in xs)
            secciones.append(f'<section class="semana-seccion sec-{c}"><h2><a href="{prof}{c}.html">{icono(c)} {L["secciones"][c]}</a></h2>'
                             f'<ul class="semana-lista">{items}</ul></section>')
    breves = [b for d in ds for b in d.get("breves", [])]
    if breves:
        items = "".join(f'<li data-grupo="{grupo_pieza(b)}"><span class="fecha-pieza">{fecha_corta(publicacion(b["fecha"]))}</span> '
                        f'<a href="{prof}{ruta_breve(b)}">{e(titulo_breve(b))}</a></li>' for b in breves)
        secciones.append(f'<section class="semana-seccion sec-breves"><h2><a href="{prof}breves.html">{icono("breves")} {L["breves"]}</a></h2>'
                         f'<ul class="semana-lista">{items}</ul></section>')
    # El reportaje, como una línea más, delante de las secciones. «La semana en vídeo» no va aquí: repasa los
    # números de lunes a domingo, no los mensajes, y está en el número del domingo y en Vídeos.
    reps = [d["reportaje"] for d in ds if d.get("reportaje")]
    if reps:
        items = "".join(item_semana(prof, r, publicacion(r["fecha"])) for r in reps)
        secciones.insert(0, f'<section class="semana-seccion sec-reportaje"><h2><a href="{prof}reportajes.html">{icono("reportaje")} {L["reportajes"]}</a></h2>'
                            f'<ul class="semana-lista">{items}</ul></section>')
    botones = [("", L["grupo_todos"])] + [(g, n) for g, (n, _) in GRUPOS.items()]
    filtro = "".join(f'<button type="button" data-g="{g}" aria-pressed="{"true" if not g else "false"}">{e(n)}</button>' for g, n in botones)
    nav = []
    if anterior:
        nav.append(f'<a href="{prof}semana/{anterior}/">← {L["sem_ant"]}</a>')
    nav.append(f'<a href="{prof}mes/{mes_de(sem)}/">{L["todo_mes"]}</a>')
    if siguiente:
        nav.append(f'<a href="{prof}semana/{siguiente}/">{L["sem_sig"]} →</a>')
    nums = numeros(ds)
    titulo = f'{rango} | {L["titulo"]}'
    return cabeza(titulo, prof, L["semana_txt"], ruta) + f"""<body class="pag-seccion">
{cabecera(prof, ruta, eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada semana-pag">
<p class="seccion semana-rotulo"><span>{icono("semana")} {L["semana"]}</span> <span class="fecha-pieza">{lunes_de(sem).year}{" · " + nums if nums else ""}</span></p>
<h1 class="titulo-seccion">{rango}</h1>
<p class="descripcion-seccion">{L["semana_txt"]}</p>
<nav class="semana-nav" aria-label="{L["navegacion"]}">{" · ".join(nav)}</nav>
<div class="filtro-grupo" role="group" aria-label="{e(L["grupo_filtro"])}">{filtro}</div>
{bloque_notebook(sem, m)}
{bloque_comentario(sem)}
{"".join(secciones)}
<p class="sin-grupo vacio" hidden>{L["sin_grupo"]}</p>
<section class="semana-dias"><h2>{L["numeros_semana"]}</h2>{dias_lista(prof, ds)}</section>
</main>
{pie(prof, eds, None)}
{SCRIPT_TEMA}
{SCRIPT_SEMANA}
{SCRIPT_FILAS}
</body>
</html>"""


def pagina_mes(eds, mes, sems, anterior, siguiente):
    prof = "../../"
    ruta = f"mes/{mes}/"
    porsem = por_semanas(eds)
    bloques = []
    for sem in reversed(sems):
        ds = porsem[sem]
        nb = f'<p class="con-nb">{icono("video")} {L["con_nb"]}</p>' if cargar_multimedia(sem) else ""
        nums = numeros(ds)
        bloques.append(f'<section class="mes-semana"><h2><a href="{prof}semana/{sem}/">{titulo_semana(sem)}</a>'
                       f'{f" <span class=num>· {nums}</span>" if nums else ""}</h2>{nb}{dias_lista(prof, ds)}'
                       f'<p class="leer"><a href="{prof}semana/{sem}/">{L["ver_semana"]}</a></p></section>')
    nav = []
    if anterior:
        nav.append(f'<a href="{prof}mes/{anterior}/">← {L["mes_ant"]}</a>')
    nav.append(f'<a href="{prof}archivo.html">{L["hemeroteca"]}</a>')
    if siguiente:
        nav.append(f'<a href="{prof}mes/{siguiente}/">{L["mes_sig"]} →</a>')
    nombre = mes_largo(mes + "-01")
    return cabeza(f'{nombre} | {L["titulo"]}', prof, L["mes_txt"], ruta) + f"""<body class="pag-seccion">
{cabecera(prof, ruta, eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada hemeroteca mes-pag">
<p class="seccion semana-rotulo"><span>{icono("semana")} {L["mes"]}</span></p>
<h1 class="titulo-seccion">{nombre}</h1>
<p class="descripcion-seccion">{L["mes_txt"]}</p>
<nav class="semana-nav" aria-label="{L["navegacion"]}">{" · ".join(nav)}</nav>
{"".join(bloques)}
</main>
{pie(prof, eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def meses_y_semanas(eds):
    """{mes: [semanas]}, en orden."""
    meses = {}
    for sem in por_semanas(eds):
        meses.setdefault(mes_de(sem), []).append(sem)
    return meses


CHEVRON_IZQ = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>'   # chevron-left
CHEVRON_DER = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>'    # chevron-right


def medidas_portadas():
    """Ancho y alto de cada miniatura de portada (scripts/portadas.py), para reservarle el sitio."""
    try:
        return json.loads((RAIZ / "portadas" / "medidas.json").read_text())
    except (OSError, ValueError):
        return {}


def datos_dia(d, medidas):
    """Lo que el calendario cuenta de un número: su fecha de cabecera, el número y su portada en miniatura."""
    foto = f'{d["fecha"]}-{L["codigo"]}.jpg'
    ancho, alto = medidas.get(foto, [0, 0])
    return {"fecha": mayus(fecha_larga(publicacion(d["fecha"]))), "num": f'{L["num"]} {d["numero"]}' if d.get("numero") else "",
            "numero": f'{d["fecha"]}/', "portada": f'{recursos("")}portadas/{foto}' if alto else "", "ancho": str(ancho), "alto": str(alto)}


def piezas_dia(d):
    """Las piezas del número por secciones, en el orden en que salen, sin los breves ni «Hace un año», que no
    están en la parte de arriba del número. Es lo mismo que el script saca de datos/AAAA-MM.json."""
    grupos = {}
    for p in ([d["reportaje"]] if d.get("reportaje") else []) + d["piezas"]:
        c = p.get("seccion") or "reportajes"
        if c not in SECCIONES_FUERA:
            grupos.setdefault(c, []).append((p["titular"], f'{d["fecha"]}/{p["id"]}.html'))
    return grupos


def detalle_dia(x, grupos):
    """El recuadro bajo el calendario con el día elegido: la portada a la izquierda y sus titulares por secciones
    a la derecha. El script lo rehace con los mismos elementos."""
    num = f' <span class="num">· {e(x["num"])}</span>' if x["num"] else ""
    alt = e(L["cal_portada"].format(fecha=x["fecha"]))
    foto = (f'<div class="cal-portada">' + boton_ampliar(f'<img src="{e(x["portada"])}" width="{x["ancho"]}" height="{x["alto"]}" alt="{alt}">', alt)
            + '</div>') if x["portada"] else ""
    secs = "".join(f'<p class="cal-sec sec-{c}">{e(L["secciones"].get(c, c))}</p><ul>'
                   + "".join(f'<li><a href="{e(u)}">{e(tit)}</a></li>' for tit, u in xs) + "</ul>" for c, xs in grupos.items())
    # La fecha y el número, enlazados al número: es su título (Juanjo, 13-11-2026, en lugar de «Leer el número»)
    return f'{foto}<div class="cal-texto"><p class="cal-fecha"><a href="{e(x["numero"])}">{e(x["fecha"])}{num}</a></p>{secs}</div>'


def calendario(eds):
    """Un calendario por mes, por la fecha de cabecera de cada número, que es la que recuerda quien lo leyó
    (ADR 0053): cada día con número enlaza a él. Sale visible el último mes; el script cambia de mes."""
    por_dia = {publicacion(d["fecha"]): d for d in eds}
    medidas = medidas_portadas()
    meses = sorted({k[:7] for k in por_dia})
    ultimo = max(por_dia)
    cabeza_tabla = "".join(f'<th scope="col"><abbr title="{L["dias"][i]}">{L["dias_cortos"][i]}</abbr></th>' for i in range(7)) \
        + f'<th scope="col" class="cal-sem-h" title="{L["cal_resumenes"]}"><span class="solo-lector">{L["cal_resumenes"]}</span>{icono("semana")}</th>'
    porsem = por_semanas(eds)
    tablas = []
    for m in meses:
        y, mo = map(int, m.split("-"))
        dia = datetime.date(y, mo, 1)
        celdas = ['<td class="vacio"></td>'] * dia.weekday()
        while dia.month == mo:
            iso = dia.isoformat()
            d = por_dia.get(iso)
            if d:
                x = datos_dia(d, medidas)
                etiqueta = f'{x["fecha"]}' + (f', {x["num"]}' if x["num"] else "")
                datos = " ".join(f'data-{k}="{e(v)}"' for k, v in x.items())
                celdas.append(f'<td><a href="{x["numero"]}" data-dia="{iso}" {datos} aria-label="{e(etiqueta)}"'
                              f'{" class=elegido" if iso == ultimo else ""}>{dia.day}</a></td>')
            else:
                celdas.append(f'<td><span data-dia="{iso}">{dia.day}</span></td>')
            dia += datetime.timedelta(days=1)
        celdas += ['<td class="vacio"></td>'] * (-len(celdas) % 7)
        # Cada fila, con el resumen de la semana que cuentan sus números: los de martes a domingo cuentan los días
        # de lunes a sábado de la semana de esa fila (el del lunes es el último de la anterior)
        lunes = datetime.date(y, mo, 1) - datetime.timedelta(days=datetime.date(y, mo, 1).weekday())
        filas = ""
        for i in range(0, len(celdas), 7):
            sem = semana_de((lunes + datetime.timedelta(days=i)).isoformat())
            if sem in porsem:
                n = int(sem.split("-")[1])
                titulo = L["cal_resumen"].format(n=n)
                resumen = f'<td class="cal-sem"><a href="semana/{sem}/" title="{e(titulo)}" aria-label="{e(titulo)}">{n}</a></td>'
            else:
                resumen = '<td class="cal-sem"></td>'
            filas += f'<tr>{"".join(celdas[i:i + 7])}{resumen}</tr>'
        tablas.append(f'<table class="cal-mes" data-mes="{m}"{"" if m == meses[-1] else " hidden"}>'
                      f'<caption class="solo-lector">{L["calendario"]}: {mes_largo(m + "-01")}</caption>'
                      f'<thead><tr>{cabeza_tabla}</tr></thead><tbody>{filas}</tbody></table>')
    opciones = "".join(f'<option value="{m}"{" selected" if m == meses[-1] else ""}>{mes_largo(m + "-01")}</option>' for m in reversed(meses))
    textos = json.dumps({"portada": L["cal_portada"], "ampliar": L["ampliar"], "cerrar": L["cerrar"]}, ensure_ascii=False)
    return (f'<section class="calendario" aria-label="{L["calendario"]}" data-textos="{e(textos)}">'
            f'<div class="cal-izq"><div class="cal-nav"><button type="button" class="cal-ant" title="{L["cal_anterior"]}" aria-label="{L["cal_anterior"]}">{CHEVRON_IZQ}</button>'
            f'<select class="cal-elegir" aria-label="{L["cal_elegir"]}">{opciones}</select>'
            f'<button type="button" class="cal-sig" title="{L["cal_siguiente"]}" aria-label="{L["cal_siguiente"]}">{CHEVRON_DER}</button></div>'
            f'{"".join(tablas)}</div><div class="cal-detalle" aria-live="polite">{detalle_dia(datos_dia(por_dia[ultimo], medidas), piezas_dia(por_dia[ultimo]))}</div></section>')


SCRIPT_CALENDARIO = """<script>
(() => {
  const cal = document.querySelector('.calendario'); if (!cal) return;
  const tablas = [...cal.querySelectorAll('.cal-mes')], meses = tablas.map(t => t.dataset.mes);
  const elegir = cal.querySelector('.cal-elegir'), ant = cal.querySelector('.cal-ant'), sig = cal.querySelector('.cal-sig');
  const detalle = cal.querySelector('.cal-detalle');
  const T = JSON.parse(cal.dataset.textos);
  function p(clase, ...hijos) { const x = document.createElement('p'); x.className = clase; x.append(...hijos); return x; }
  function enlace(href, texto) { const a = document.createElement('a'); a.href = href; a.textContent = texto; return a; }
  const meses_datos = {};   // datos/AAAA-MM.json, el mes de las conversaciones, que es la carpeta de cada número
  let vuelta = 0;
  function piezas(numero) {
    const mes = numero.slice(0, 7);
    if (!(mes in meses_datos)) meses_datos[mes] = fetch(`datos/${mes}.json`).then(r => r.ok ? r.json() : null).catch(() => null);
    return meses_datos[mes].then(d => d ? d.noticias.filter(n => n.tipo !== 'breve' && n.seccion !== 'hace-un-ano' && n.id.startsWith(numero)) : null);
  }
  async function marca(a) {   // el día elegido: su portada, su fecha y número y sus titulares por secciones
    cal.querySelectorAll('.cal-mes a.elegido').forEach(x => { x.classList.remove('elegido'); x.setAttribute('aria-pressed', 'false'); });
    a.classList.add('elegido'); a.setAttribute('aria-pressed', 'true');
    const d = a.dataset, esta = ++vuelta;
    const ns = await piezas(d.numero);
    if (esta !== vuelta) return;   // ya se ha elegido otro día
    const hijos = [];
    if (d.portada) {
      const img = document.createElement('img'); img.src = d.portada; img.width = +d.ancho; img.height = +d.alto;
      img.alt = T.portada.replace('{fecha}', d.fecha);
      const b = document.createElement('button'); b.type = 'button'; b.className = 'ampliar';
      b.title = T.ampliar; b.setAttribute('aria-label', T.ampliar + ': ' + img.alt); b.dataset.cerrar = T.cerrar; b.append(img);
      const f = document.createElement('div'); f.className = 'cal-portada'; f.append(b); hijos.push(f);
    }
    const texto = document.createElement('div'); texto.className = 'cal-texto';
    const titulo = enlace(d.numero, d.fecha);
    if (d.num) { const n = document.createElement('span'); n.className = 'num'; n.textContent = ' · ' + d.num; titulo.append(n); }
    texto.append(p('cal-fecha', titulo));
    const secs = new Map();
    for (const n of ns || []) {
      if (!secs.has(n.seccion)) secs.set(n.seccion, { nombre: n.seccion_nombre, xs: [] });
      secs.get(n.seccion).xs.push(n);
    }
    for (const [c, s] of secs) {
      const ul = document.createElement('ul');
      for (const n of s.xs) { const li = document.createElement('li'); li.append(enlace(n.id + '.html', n.titular)); ul.append(li); }
      texto.append(p('cal-sec sec-' + c, s.nombre), ul);
    }
    hijos.push(texto);
    detalle.replaceChildren(...hijos);
    ajusta();
  }
  // Sin huecos (ADR 0041): si los titulares no caben al lado de la portada, siguen por debajo de ella; si son
  // pocos, la portada se recorta por abajo (CSS) para acabar a la vez que ellos.
  const estrecho = matchMedia('(max-width: 36rem)');
  function ajusta() {
    detalle.classList.remove('envuelve');
    const img = detalle.querySelector('.cal-portada img'), tx = detalle.querySelector('.cal-texto');
    if (!img || !tx || estrecho.matches) return;
    const natural = img.getBoundingClientRect().width * img.getAttribute('height') / img.getAttribute('width');
    if (tx.offsetHeight > natural + 24) detalle.classList.add('envuelve');
  }
  let espera; addEventListener('resize', () => { clearTimeout(espera); espera = setTimeout(ajusta, 150); });
  function ver(m, guardar) {
    if (!meses.includes(m)) m = meses[meses.length - 1];
    tablas.forEach(t => { t.hidden = t.dataset.mes !== m; });
    elegir.value = m;
    const i = meses.indexOf(m); ant.disabled = i === 0; sig.disabled = i === meses.length - 1;
    const dias = cal.querySelectorAll(`.cal-mes[data-mes="${m}"] a[data-dia]`);
    if (dias.length) marca(dias[dias.length - 1]);
    if (guardar) {   // el mes queda en la dirección, para compartirlo tal cual
      const u = new URL(location.href);
      i === meses.length - 1 ? u.searchParams.delete('mes') : u.searchParams.set('mes', m);
      history.replaceState(null, '', u);
    }
  }
  elegir.addEventListener('change', () => ver(elegir.value, true));
  ant.addEventListener('click', () => ver(meses[meses.indexOf(elegir.value) - 1], true));
  sig.addEventListener('click', () => ver(meses[meses.indexOf(elegir.value) + 1], true));
  // Un clic (o un toque) elige el día y lo enseña debajo, sin abrirlo: el número se abre desde su portada o desde
  // «Leer el número» (Juanjo, 13-11-2026: pasar el ratón no puede cambiarlo). Sin script, el enlace abre el número.
  cal.querySelectorAll('.cal-mes a[data-dia]').forEach(a => {
    a.setAttribute('role', 'button'); a.setAttribute('aria-pressed', String(a.classList.contains('elegido')));
    a.addEventListener('click', ev => { ev.preventDefault(); marca(a); });
    a.addEventListener('keydown', ev => { if (ev.key === ' ') { ev.preventDefault(); marca(a); } });
  });
  const h = new Date(), hoy = `${h.getFullYear()}-${String(h.getMonth() + 1).padStart(2, '0')}-${String(h.getDate()).padStart(2, '0')}`;
  const celda = cal.querySelector(`[data-dia="${hoy}"]`);
  if (celda) { celda.closest('td').classList.add('hoy'); celda.setAttribute('aria-current', 'date'); }
  ver(new URLSearchParams(location.search).get('mes'), false);
})();
</script>"""


def pagina_hemeroteca(eds):
    """Todos los números (ADR 0034 y 0053): el buscador y el calendario, con el número del día elegido y el resumen
    de cada semana. La lista de semanas y los boletines anteriores que había debajo se quitaron (Juanjo, 13-11-2026):
    lo da el calendario, y las páginas de cada semana enlazan su mes y los boletines."""
    buscador = (f'<form class="buscador hem-buscar" role="search" action="buscar.html">'
                f'<label class="solo-lector" for="q">{L["buscar_etiqueta"]}</label>'
                f'<span class="campo">{LUPA}<input id="q" name="q" type="search" autocomplete="off" placeholder="{e(L["buscar_numeros"])}"></span></form>')
    bloques = [buscador + calendario(eds)]
    return cabeza(f'{L["hemeroteca"]} | {L["titulo"]}', "", L["hemeroteca_txt"], "archivo.html") + f"""<body class="pag-seccion">
{cabecera("", "archivo.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada hemeroteca hem-ancha">
<h1 class="titulo-seccion">{L["hemeroteca"]}</h1>
{"".join(bloques)}
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
{SCRIPT_CALENDARIO}
</body>
</html>"""


def pagina_404(eds):
    """La página de GitHub Pages para lo que no existe, con rutas absolutas porque se sirve en cualquier nivel.
    En castellano, con una línea en cada otro idioma debajo: GitHub solo admite una."""
    otros = "".join(f'<p class="{c}" lang="{c}">{d["no_existe"]}. <a href="/{d["carpeta"]}">{d["portada"]}</a> · '
                    f'<a href="/{d["carpeta"]}archivo.html">{d["hemeroteca"]}</a></p>\n' for c, d in IDIOMAS.items() if c != "es")
    html_ = cabeza(f'{L["no_existe"]} | {L["titulo"]}', "/", L["no_existe_txt"], "404.html")
    return html_ + f"""<body class="pag-que-es">
{cabecera("/", "404.html", eds[-1]["fecha"], eds[-1]["numero"], False, h1=False)}
<main class="articulo no-existe">
<h1 class="titular">{L["no_existe"]}</h1>
<p>{L["no_existe_txt"]}</p>
<p><a href="/">{L["portada"]}</a> · <a href="/archivo.html">{L["hemeroteca"]}</a></p>
{otros}</main>
{pie("/", eds, None)}
{SCRIPT_TEMA}
</body>
</html>"""


def pagina_sin_conexion():
    """Lo que enseña el service worker sin conexión cuando la página pedida no está guardada (ADR 0042), una
    por idioma. Rutas absolutas, porque sale en lugar de cualquier página; sin fecha ni número, porque se
    guarda al instalar y puede tener semanas. No cuenta visitas ni se indexa."""
    portada = "/" + L["carpeta"]
    html_ = cabeza(f'{L["sin_conexion"]} | {L["titulo"]}', portada, L["sin_conexion_txt"], "sin-conexion.html")
    html_ = html_.replace("<head>\n", '<head>\n<meta name="robots" content="noindex">\n', 1)
    return html_ + f"""<body class="pag-que-es">
<header class="cabecera">
  <div class="cabecera-fila"><span></span><span></span><span class="controles">{boton_tema()}</span></div>
  <p class="mancheta"><a href="{portada}">{L["titulo"]}</a></p>
  <p class="lema">{L["lema"]}</p>
</header>
<main class="articulo no-existe">
<h1 class="titular">{L["sin_conexion"]}</h1>
<p>{L["sin_conexion_txt"]}</p>
<p><a href="{portada}">{L["portada"]}</a></p>
</main>
{SCRIPT_TEMA}
</body>
</html>"""


def sitemap(eds):
    """Todas las páginas de todos los idiomas, con la fecha de su último cambio y, en cada una, sus
    versiones en los otros idiomas (xhtml:link), como pide Google para un sitio multilingüe (ADR 0026)."""
    rutas = []
    ultima = publicacion(eds[-1]["fecha"])
    for ruta in ["", "redaccion.html", "contacto.html", "vineta.html", "reportajes.html", "breves.html", "archivo.html", "videos.html", "para-tu-web.html"] + [f"{c}.html" for c in TODAS_SECCIONES]:
        rutas.append((ruta, ultima))
    for sem, ds in por_semanas(eds).items():   # la semana y el mes (ADR 0034)
        rutas.append((f"semana/{sem}/", publicacion(ds[-1]["fecha"])))
    for mes, sems in meses_y_semanas(eds).items():
        rutas.append((f"mes/{mes}/", publicacion(por_semanas(eds)[sems[-1]][-1]["fecha"])))
    for cfg in listas(eds):   # los meses de las páginas que acumulan (ADR 0050)
        if len(cfg["items"]) > cfg["n"]:
            for m in meses_lista(cfg):
                ult = max(publicacion(cfg["fecha"](x)) for x in cfg["items"] if mes_pub(cfg["fecha"](x)) == m)
                rutas.append((f'{cfg["carpeta"]}/{m}.html', ult))
    for d in eds:
        sale = publicacion(d["fecha"])
        rutas.append((f'{d["fecha"]}/', sale))
        for p in d["piezas"] + [d[k] for k in ("editorial", "reportaje") if d.get(k)]:
            rutas.append((f'{d["fecha"]}/{p["id"]}.html', sale))
        for b in d.get("breves", []):
            rutas.append((ruta_breve(b), sale))
    cuerpo = []
    for ruta, f in rutas:
        alternas = "".join(f'<xhtml:link rel="alternate" hreflang="{c}" href="{e(BASE + x["carpeta"] + ruta)}"/>'
                           for c, x in IDIOMAS.items()) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{e(BASE + ruta)}"/>'
        for x in IDIOMAS.values():
            cuerpo.append(f"  <url><loc>{e(BASE + x['carpeta'] + ruta)}</loc><lastmod>{f}</lastmod>{alternas}</url>\n")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{"".join(cuerpo)}</urlset>\n')


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


# --- Las páginas que acumulan (ADR 0050) ---------------------------------------------------------------
# Las secciones, «Breves», «Reportajes» y «La viñeta» enseñan lo más reciente y, al pie, los meses anteriores;
# cada mes, en su página (`<carpeta>/AAAA-MM.html`), con todo lo que salió ese mes. El mes es el de la fecha
# de publicación, la que ve el lector junto a cada pieza. Así ninguna página crece sin fin.
RECIENTES = {"seccion": 12, "reportajes": 4, "breves": 7, "vineta": 7}


def mes_pub(fecha):
    return publicacion(fecha)[:7]


def lista_seccion(eds, clave):
    todas = [p for d in reversed(eds) for p in d["piezas"]
             if p.get("seccion") == clave or (clave == "biblioteca" and p.get("biblioteca"))]
    nombre = L["secciones"][clave]
    return {"carpeta": clave, "pagina": f"{clave}.html", "nombre": nombre, "icono": icono(clave), "clase": f"sec-{clave}",
            "activa": clave, "meta": L["descripciones"][clave].format(enlace=L["biblioteca_enlace"], repositorio=L["repositorio_enlace"]),
            "descripcion": descripcion(clave), "items": todas, "fecha": lambda p: p["fecha"], "n": RECIENTES["seccion"],
            "pintar": lambda prof, ps: en_filas([pieza(prof, p, "destacada", 2, True, True, sin_seccion=True, relleno=True) for p in ps], "fila-seccion"),
            "vacio": L["sin_piezas"], "main": "portada", "scripts": SCRIPT_FILAS}


def lista_reportajes(eds):
    reps = [d["reportaje"] for d in reversed(eds) if d.get("reportaje")]
    return {"carpeta": "reportajes", "pagina": "reportajes.html", "nombre": L["reportajes"], "icono": icono("reportaje"),
            "clase": "sec-reportaje", "activa": "reportajes", "meta": L["descripciones"]["reportajes"],
            "descripcion": descripcion("reportajes"), "items": reps, "fecha": lambda r: r["fecha"], "n": RECIENTES["reportajes"],
            "pintar": lambda prof, rs: "".join(franja_reportaje(prof, r) for r in rs),
            "vacio": L["sin_reportajes"], "main": "portada", "scripts": ""}


def lista_breves(eds):
    """Todos los breves, del más reciente al más antiguo, agrupados por el día en que salieron."""
    def pintar(prof, ds):
        return "".join(f'<h2><a href="{prof}{d["fecha"]}/">{mayus(fecha_larga(publicacion(d["fecha"])))}</a></h2>'
                       f'<div class="lista-breves">{bloque_breves(d["breves"], False, en_bloque=True)}</div>' for d in ds)
    return {"carpeta": "breves", "pagina": "breves.html", "nombre": L["breves"], "icono": icono("breves"), "clase": "sec-breves",
            "activa": None, "meta": L["descripciones"]["breves"], "descripcion": descripcion("breves"),
            "items": [d for d in reversed(eds) if d.get("breves")], "fecha": lambda d: d["fecha"], "n": RECIENTES["breves"],
            "pintar": pintar, "vacio": "", "main": "portada pagina-breves", "scripts": ""}


def lista_vinetas(eds):
    """Las viñetas, de la más reciente a la más antigua; solo los días que la tienen."""
    dias = [d["fecha"] for d in reversed(eds) if bloque_vineta("", eds, d["fecha"], en_archivo=True)]
    return {"carpeta": "vineta", "pagina": "vineta.html", "nombre": L["vineta_titulo"], "icono": icono("vineta"), "clase": "sec-vineta",
            "activa": "vineta", "meta": L["lema"], "descripcion": descripcion("vineta"), "items": dias, "fecha": lambda f: f,
            "n": RECIENTES["vineta"], "pintar": lambda prof, fs: "".join(bloque_vineta(prof, eds, f, en_archivo=True) for f in fs),
            "vacio": L["sin_vinetas"], "main": "portada", "scripts": ""}


def listas(eds):
    """Todas las páginas que acumulan, para escribirlas con sus meses y ponerlas en el mapa del sitio."""
    return [lista_seccion(eds, c) for c in TODAS_SECCIONES] + [lista_reportajes(eds), lista_breves(eds), lista_vinetas(eds)]


def meses_lista(cfg):
    """Los meses con algo, del más reciente al más antiguo."""
    return sorted({mes_pub(cfg["fecha"](x)) for x in cfg["items"]}, reverse=True)


def pagina_lista(eds, cfg, mes=None):
    """La página de una sección (o de los breves, los reportajes o las viñetas) o, con `mes`, la de uno de sus meses."""
    meses = meses_lista(cfg)
    if mes is None:
        prof, ruta = "", cfg["pagina"]
        items = cfg["items"][:cfg["n"]]
        cuerpo = cfg["pintar"](prof, items) if items else (f'<p class="vacio">{cfg["vacio"]}</p>' if cfg["vacio"] else "")
        if len(cfg["items"]) > cfg["n"]:
            enlaces = " · ".join(f'<a href="{cfg["carpeta"]}/{m}.html">{mes_largo(m + "-01")}</a>' for m in meses)
            cuerpo += (f'<nav class="archivo-meses" aria-labelledby="t-meses"><h2 id="t-meses">{L["por_meses"]}</h2>'
                       f'<p>{enlaces}</p></nav>')
        titulo, encabezado = f'{cfg["nombre"]} | {L["titulo"]}', (
            f'<h1 class="titulo-seccion {cfg["clase"]}">{cfg["icono"]} {cfg["nombre"]}</h1>\n'
            f'<p class="descripcion-seccion">{cfg["descripcion"]}</p>')
    else:
        prof, ruta = "../", f'{cfg["carpeta"]}/{mes}.html'
        cuerpo = cfg["pintar"](prof, [x for x in cfg["items"] if mes_pub(cfg["fecha"](x)) == mes])
        i = meses.index(mes)
        nav = []
        if i + 1 < len(meses):
            nav.append(f'<a href="{meses[i + 1]}.html">← {L["mes_ant"]}</a>')
        nav.append(f'<a href="../{cfg["pagina"]}">{cfg["nombre"]}</a>')
        if i > 0:
            nav.append(f'<a href="{meses[i - 1]}.html">{L["mes_sig"]} →</a>')
        nombre_mes = mes_largo(mes + "-01")
        titulo, encabezado = f'{cfg["nombre"]} · {nombre_mes} | {L["titulo"]}', (
            f'<p class="seccion semana-rotulo {cfg["clase"]}"><a href="../{cfg["pagina"]}">{cfg["icono"]} {cfg["nombre"]}</a></p>\n'
            f'<h1 class="titulo-seccion">{nombre_mes}</h1>\n'
            f'<nav class="semana-nav" aria-label="{L["navegacion"]}">{" · ".join(nav)}</nav>')
    return cabeza(titulo, prof, cfg["meta"], ruta) + f"""<body class="pag-seccion">
{cabecera(prof, ruta, eds[-1]["fecha"], eds[-1]["numero"], True, h1=False, activa=cfg["activa"])}
<main class="{cfg["main"]}">
{encabezado}
{cuerpo}
</main>
{pie(prof, eds, None)}
{SCRIPT_TEMA}
{cfg["scripts"]}
</body>
</html>"""


def pagina_breves(eds, mes=None):
    return pagina_lista(eds, lista_breves(eds), mes)


def pagina_vinetas(eds, mes=None):
    return pagina_lista(eds, lista_vinetas(eds), mes)


# ---------------------------------------------------------------------------------------------------
# Para tu web (ADR 0032): canales RSS, datos abiertos, el widget que se incrusta en otra web, su
# configurador y el botón de cada pieza, que copia su tarjeta o la pieza entera para republicarla.
# ---------------------------------------------------------------------------------------------------

LICENCIA_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
ICONO_LLEVAR = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/></svg>'   # code-xml
ICONO_LISTA = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h.01"/><path d="M3 12h.01"/><path d="M3 19h.01"/><path d="M8 5h13"/><path d="M8 12h13"/><path d="M8 19h13"/></svg>'   # list
ICONO_TARJETAS = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>'   # layout-grid
ICONO_RSS = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></svg>'   # rss
ICONO_COPIAR = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'   # copy
TOPE_FEED = 100        # piezas del canal general; los de sección y grupo, TOPE_FILTRO
TOPE_FILTRO = 50
TOPE_NOTICIAS = 50     # piezas de cada noticias*.json que lee el widget (enseña 20 como mucho)
ALTO_TARJETA = 500     # alto del iframe de la tarjeta de una pieza; el dibujo se encoge si falta sitio
# Filtros del widget y de los canales: las secciones, el reportaje y los breves; y los tres grupos
CLAVES_FILTRO = TODAS_SECCIONES + ["reportaje", "breves"]

# Los colores del tema claro de cada sección (comun.css), para el dibujo suelto que se ve fuera del
# diario: con <img> no le llegan las variables de la página. Dentro del widget, mandan las variables.
COLOR_SUELTO = {
    "herramientas": ("#1c3faa", "#e6ebf8", "#c9d4f2"), "debates": ("#b04f0c", "#fbeadb", "#f3cdaa"),
    "vibecoding": ("#1d7547", "#e2f1e8", "#bfe0cc"), "novedades": ("#6a3d9e", "#eee6f7", "#d8c6ee"),
    "multimedia": ("#a8206f", "#fae4f0", "#f2bedb"), "reportaje": ("#1c3faa", "#eef1fa", "#dfe5f7"),
    "biblioteca": ("#0b6e79", "#e0f2f3", "#b7e1e5"), "hace-un-ano": ("#7a4f2a", "#f6ede3", "#e8d3bd"),
}
SUELTO_BASE = {"--ilu-tinta": "#16181d", "--ilu-rojo": "#c8202c", "--c-herramientas": "#1c3faa",
               "--c-comunidad": "#1d7547", "--c-multimedia": "#a8206f"}


def estilo_suelto(seccion):
    """Las reglas de los dibujos de comun.css (.ilu .t, .ilu .fa…), para el <style> del dibujo suelto:
    con la clase propia del dibujo y cada variable con el color claro de su sección como reserva."""
    c, tinte, medio = COLOR_SUELTO.get(seccion, ("#1c3faa", "#f1f2f4", "#dfe5f7"))
    reserva = dict(SUELTO_BASE, **{"--ilu-azul": c, "--ilu-relleno": medio})
    reglas = re.findall(r"^\.ilu ((?:g)?\.[\w-]+) \{([^}]*)\}", (RAIZ / "estaticos" / "comun.css").read_text(), re.M)
    css = "".join(f".ilu-d {sel}{{{cuerpo.strip()}}}" for sel, cuerpo in reglas)
    css = re.sub(r"var\((--[\w-]+)\)", lambda m: f"var({m.group(1)},{reserva[m.group(1)]})" if m.group(1) in reserva else m.group(0), css)
    return f"svg.ilu-d{{background:var(--sec-tinte,{tinte})}}" + css


def dibujo_suelto(fecha, x, seccion):
    """El dibujo de una pieza como archivo propio (ilustraciones/AAAA-MM-DD-id.svg en cada idioma), con
    sus colores dentro: lo usan el RSS, la pieza republicada y el widget."""
    f = con_traduccion("ilustraciones", f"{fecha}-{x['id']}.svg")
    if not f.exists():
        return
    svg = re.sub(r"<\?xml.*?\?>", "", f.read_text()).strip()
    svg = re.sub(r"<svg\b", '<svg class="ilu-d"', svg, count=1)
    svg = re.sub(r"(<svg\b[^>]*>)", lambda m: m.group(1) + f"<style>{estilo_suelto(seccion)}</style>", svg, count=1)
    escribir(SITIO / L["carpeta"] / "ilustraciones" / f.name, svg + "\n")


def imagen_pieza(fecha, x):
    """La dirección pública del dibujo de una pieza (o de la captura de su recurso) y su descripción."""
    if con_traduccion("ilustraciones", f"{fecha}-{x['id']}.svg").exists():
        return f'{BASE}{L["carpeta"]}ilustraciones/{fecha}-{x["id"]}.svg', x.get("ilustracion_alt") or x["titular"]
    r = next((r for r in x.get("recursos", []) if r.get("captura")), None)
    if r:
        return f'{BASE}capturas/{pathlib.Path(r["captura"]).name}', r.get("captura_alt") or r.get("titulo", "")
    return None, None


def fecha_con_anyo(iso):
    """«8 de noviembre de 2026», sin el día de la semana, en el idioma de la página."""
    d = datetime.date.fromisoformat(iso)
    mes = L["meses"][d.month - 1]
    if L["codigo"] == "en":
        return f"{d.day} {mes} {d.year}"
    if L["codigo"] == "eu":
        return f"{d.year}ko {mes}ren {d.day}a"
    return f"{d.day} {de_mes(mes)} de {d.year}"


def grupo_de(x):
    g = (x.get("mensaje") or {}).get("grupo") or x.get("grupo")
    return g if g in GRUPOS else None


def ficha_datos(d, x, tipo):
    """Una pieza, un reportaje o un breve, tal como lo leen los canales RSS y el widget."""
    sale = publicacion(d["fecha"])
    if tipo == "breve":
        ruta, pid, sec = ruta_breve(x), f'{d["fecha"]}/breve-{x["n"]}', "breves"
        titular, entradilla, img, alt = titulo_breve(x), texto_plano(x.get("texto", "")), None, None
        nombre = L["breves"]
    else:
        ruta, pid = f'{d["fecha"]}/{x["id"]}.html', f'{d["fecha"]}/{x["id"]}'
        sec = "reportaje" if tipo == "reportaje" else x.get("seccion", "")
        titular, entradilla = texto_plano(x["titular"]), texto_plano(x.get("entradilla", ""))
        img, alt = imagen_pieza(d["fecha"], x)
        nombre = L["reportaje"] if tipo == "reportaje" else L["secciones"].get(sec, "")
    return {"id": pid, "tipo": tipo, "seccion": sec, "seccion_nombre": nombre,
            "biblioteca": sec == "biblioteca" or bool(x.get("biblioteca")), "grupo": grupo_de(x),
            "antetitulo": texto_plano(x.get("antetitulo", "")), "titular": titular, "entradilla": entradilla,
            "sale": sale, "sale_texto": fecha_corta(sale), "url": BASE + L["carpeta"] + ruta,
            "imagen": img, "imagen_alt": alt}


def todas_las_fichas(eds):
    """De la más reciente a la más antigua; dentro de cada número, el reportaje, las piezas y los breves."""
    fichas = []
    for d in reversed(eds):
        if d.get("reportaje"):
            fichas.append(ficha_datos(d, d["reportaje"], "reportaje"))
        fichas += [ficha_datos(d, p, "pieza") for p in d["piezas"]]
        fichas += [ficha_datos(d, b, "breve") for b in d.get("breves", [])]
    return fichas


def filtrar(fichas, clave):
    """Las de una sección (la Biblioteca incluye las noticias sobre sus documentos), del reportaje, de
    los breves o de un grupo."""
    if clave in GRUPOS:
        return [f for f in fichas if f["grupo"] == clave]
    if clave == "biblioteca":
        return [f for f in fichas if f["biblioteca"]]
    return [f for f in fichas if f["seccion"] == clave]


def nombre_filtro(clave):
    if clave in GRUPOS:
        return GRUPOS[clave][0]
    return {"reportaje": L["reportajes"], "breves": L["breves"]}.get(clave) or L["secciones"][clave]


def archivo_feed(clave=None):
    """feed.xml para todo el diario; feed-<sección>.xml, feed-reportajes.xml, feed-breves.xml y
    feed-<grupo>.xml para cada parte."""
    return "feed.xml" if not clave else f'feed-{"reportajes" if clave == "reportaje" else clave}.xml'


def rss(fichas, clave=None):
    """RSS 2.0, de lo más reciente a lo más antiguo, con el dibujo de cada pieza. Fechas en UTC."""
    base = BASE + L["carpeta"]
    items = []
    for f in fichas:
        cuando = hora_de_salida(f["sale"])
        media = ""
        if f["imagen"]:
            tipo = "image/svg+xml" if f["imagen"].endswith(".svg") else "image/png"
            media = (f'\n    <media:content url="{e(f["imagen"])}" medium="image" type="{tipo}">'
                     f'<media:description>{e(f["imagen_alt"])}</media:description></media:content>')
        items.append(f"""  <item>
    <title>{e(f["titular"])}</title>
    <link>{e(f["url"])}</link>
    <guid isPermaLink="true">{e(f["url"])}</guid>
    <pubDate>{format_datetime(cuando)}</pubDate>
    <category>{e(f["seccion_nombre"])}</category>
    <description>{e(f["entradilla"])}</description>{media}
  </item>""")
    titulo = L["titulo"] + (f" · {nombre_filtro(clave)}" if clave else "")
    anyo = datetime.date.today().year
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
  <title>{e(titulo)}</title>
  <link>{e(base)}</link>
  <atom:link href="{e(base + archivo_feed(clave))}" rel="self" type="application/rss+xml"/>
  <description>{e(L["lema"])}</description>
  <language>{L["codigo"]}</language>
  <copyright>© {anyo} Juan José de Haro, Raül Torres. CC BY-SA 4.0 ({LICENCIA_URL})</copyright>
  <image><url>{BASE}icono-192.png</url><title>{e(titulo)}</title><link>{e(base)}</link></image>
{chr(10).join(items)}
</channel>
</rss>
"""


def datos_json(fichas, que):
    return json.dumps({"diario": L["titulo"], "url": BASE + L["carpeta"], "idioma": L["codigo"],
                       "licencia": "CC BY-SA 4.0", "licencia_url": LICENCIA_URL, "que": que,
                       "noticias": fichas}, ensure_ascii=False, separators=(",", ":")) + "\n"


def publicar_canales(base, eds):
    """Los canales RSS y los datos que lee el widget: noticias.json (todo), noticias-<filtro>.json y
    datos/AAAA-MM.json con todo lo de un mes, para la tarjeta de una pieza concreta."""
    fichas = todas_las_fichas(eds)
    escribir(base / "feed.xml", rss(fichas[:TOPE_FEED]))
    escribir(base / "noticias.json", datos_json(fichas[:TOPE_NOTICIAS], "todo"))
    for clave in CLAVES_FILTRO + list(GRUPOS):
        parte = filtrar(fichas, clave)
        escribir(base / archivo_feed(clave), rss(parte[:TOPE_FILTRO], clave))
        escribir(base / f"noticias-{clave}.json", datos_json(parte[:TOPE_NOTICIAS], clave))
    shutil.rmtree(base / "datos", ignore_errors=True)
    meses = {}
    for f in fichas:
        meses.setdefault(f["id"][:7], []).append(f)
    for mes, lista in meses.items():
        escribir(base / "datos" / f"{mes}.json", datos_json(lista, mes))


def url_widget(**params):
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v}, safe="/")
    return f'{BASE}{L["carpeta"]}insertar.html' + (f"?{q}" if q else "")


def codigo_tarjeta(fecha, x):
    """El código que pega quien quiere la tarjeta de una pieza en su web."""
    src = url_widget(pieza=fecha + "/" + x["id"])
    return (f'<iframe src="{e(src)}" title="{e(L["titulo"])}: {e(texto_plano(x["titular"]))}" '
            f'width="100%" height="{ALTO_TARJETA}" style="border:0;max-width:640px" loading="lazy"></iframe>')


def absoluto(html_, url):
    """Los enlaces y las imágenes, con la dirección completa: el texto se pega en otra web."""
    return re.sub(r'\b(href|src)="([^"]*)"', lambda m: f'{m.group(1)}="{e(urllib.parse.urljoin(url, html.unescape(m.group(2))))}"', html_)


def republicable(d, x, ruta, eds, reportaje=False):
    """La pieza entera, lista para pegar en otra web, con los créditos y la licencia al final (CC BY-SA)."""
    url = BASE + L["carpeta"] + ruta
    partes = [f'<p><em>{e(x["antetitulo"])}</em></p>'] if x.get("antetitulo") else []
    partes.append(f'<h2>{e(x["titular"])}</h2>')
    if x.get("entradilla"):
        partes.append(f'<p><strong>{e(x["entradilla"])}</strong></p>')
    img, alt = imagen_pieza(d["fecha"], x)
    if img:
        partes.append(f'<figure><img src="{e(img)}" alt="{e(alt)}" width="600" style="max-width:100%;height:auto"></figure>')
    if reportaje:
        for a in x.get("apartados", []):
            if a.get("ladillo"):
                partes.append(f'<h3>{e(a["ladillo"])}</h3>')
            partes += [f"<p>{md(t)}</p>" for t in a.get("parrafos", [])]
            # La tabla se desplaza dentro de su marco: en un móvil no ensancha la página ajena
            partes.append(tabla(a.get("tabla")).replace('<figure class="tabla">', '<figure style="overflow-x:auto;margin:1em 0">'))
        if x.get("claves"):
            partes.append(f'<h3>{L["claves"]}</h3><ul>{"".join(f"<li>{md(c)}</li>" for c in x["claves"])}</ul>')
    else:
        partes += [f"<p>{md(enlaces_biblioteca('../', t, eds))}</p>" for t in x.get("cuerpo", [])]
        for r in x.get("recursos") or []:   # los recursos del repositorio, sin su captura ampliable
            titulo = enlace(r["url"], e(r["titulo"])) if r.get("url") else e(r["titulo"])
            datos = " · ".join(e(v) for v in (r.get("autoria"), r.get("licencia")) if v)
            partes.append(f'<h3>{titulo}</h3>' + (f"<p><em>{datos}</em></p>" if datos else "")
                          + "".join(f"<p>{md(t)}</p>" for t in r.get("texto", [])))
    if x.get("correccion"):
        partes.append(f'<p><em>{md(x["correccion"])}</em></p>')
    fuentes = [f for f in x.get("fuentes", []) if f.get("url")]
    if fuentes:
        partes.append(f'<p>{L["rep_fuentes"]}: ' + ", ".join(enlace(f["url"], e(f["titulo"] or f["url"])) for f in fuentes) + ".</p>")
    partes.append(origen(dict(x, grupo=grupo_de(x))))
    diario = enlace(url, L["titulo"])
    creditos = [L["rep_original"].format(diario=diario, fecha=fecha_con_anyo(publicacion(d["fecha"]))),
                L["rep_derechos"].format(anyo=publicacion(d["fecha"])[:4], licencia=enlace(LICENCIA_URL + L["deed"], "CC BY-SA 4.0")),
                L["rep_redactado"]] + ([L["traduccion"]] if L["traduccion"] else [])
    partes.append(f'<p><small>{" ".join(creditos)}</small></p>')
    return absoluto("\n".join(p for p in partes if p), url)


def acciones(fecha, x, ruta, d, eds, reportaje=False, llevar=True):
    """Compartir y «Para tu web»: un botón que despliega la tarjeta para incrustar, la pieza entera para
    republicarla y la página con el resto de opciones. El texto republicable va en un <template>, fuera
    del <article>, para que el buscador no lo cuente dos veces."""
    prof = "../"
    llevar = llevar and (f'<span class="llevar"><button type="button" class="compartir llevar-boton" aria-expanded="false" aria-controls="menu-llevar" '
              f'title="{e(L["llevar"])}">{ICONO_LLEVAR}<span>{L["llevar"]}</span></button>'
              f'<span class="llevar-menu" id="menu-llevar" hidden>'
              f'<button type="button" class="llevar-op" data-copiar="{e(codigo_tarjeta(fecha, x))}" data-hecho="{e(L["llevar_copiado"])}">'
              f'<b>{L["llevar_tarjeta"]}</b><span>{L["llevar_tarjeta_desc"]}</span></button>'
              f'<button type="button" class="llevar-op" data-plantilla="republicar" data-hecho="{e(L["llevar_copiado"])}">'
              f'<b>{L["llevar_completa"]}</b><span>{L["llevar_completa_desc"]}</span></button>'
              f'<a class="llevar-op llevar-mas" href="{prof}para-tu-web.html">{L["llevar_mas"]}</a></span></span>')
    if not llevar:   # el editorial no entra en el widget ni en los canales: solo se comparte
        llevar = ""
    botones = (f'<div class="acciones" data-pagefind-ignore><button type="button" class="compartir" data-copiado="{e(L["copiado"])}">'
               f'{COMPARTIR}<span>{L["compartir"]}</span></button>{llevar}</div>')
    if not llevar:
        return botones, ""
    plantilla = f'<template id="republicar">{republicable(d, x, ruta, eds, reportaje)}</template>'
    return botones, plantilla


SCRIPT_WIDGET = """<script>
(function(){
  var T=__TEXTOS__, CLAVES=__CLAVES__, GR=__GRUPOS__;
  var q=new URLSearchParams(location.search), sec=q.get('seccion')||'', gr=q.get('grupo')||'', pieza=q.get('pieza')||'';
  if(CLAVES.indexOf(sec)<0) sec=''; if(!GR[gr]) gr='';
  if(!/^\\d{4}-\\d{2}-\\d{2}\\/[\\w-]+$/.test(pieza)) pieza='';
  var n=Math.min(20,Math.max(1,parseInt(q.get('n'),10)||5)), estilo=q.get('estilo')==='lista'?'lista':'tarjetas';   // por defecto, tarjetas con dibujo
  var caja=document.getElementById('contenido'), mas=document.getElementById('mas'), filtro=document.getElementById('filtro');
  function el(t,c,x){var e=document.createElement(t); if(c)e.className=c; if(x!=null)e.textContent=x; return e;}
  function enlace(it,c){var a=el('a',c,it.titular); a.href=it.url; a.target='_blank'; a.rel='noopener'; return a;}
  function rotulo(it){var p=el('p','seccion'); p.append(el('span','',it.seccion_nombre),' ',el('span','fecha-pieza',it.sale_texto)); return p;}
  function dibujo(it){
    var f=el('figure','ilu'); if(!it.imagen){f.hidden=true; return f;}
    if(!/\\.svg$/.test(it.imagen)){var i=el('img'); i.src=it.imagen; i.alt=it.imagen_alt||''; f.append(i); return f;}
    // El dibujo, dentro de la página: así toma los colores del tema, también en oscuro
    fetch(it.imagen).then(function(r){if(!r.ok)throw 0; return r.text();}).then(function(t){
      var s=new DOMParser().parseFromString(t,'image/svg+xml').documentElement;
      if(s.nodeName!=='svg')throw 0;
      s.querySelectorAll('script,foreignObject').forEach(function(x){x.remove();});
      s.setAttribute('role','img'); s.setAttribute('aria-label',it.imagen_alt||it.titular);
      f.append(document.importNode(s,true));
    }).catch(function(){f.hidden=true;});
    return f;
  }
  function pinta(lista){
    caja.replaceChildren();
    if(pieza){
      var it=lista.find(function(x){return x.id===pieza;});
      if(!it){caja.append(el('p','w-aviso',T.w_sin)); return;}
      document.title=T.titulo+': '+it.titular;
      var a=el('article','w-pieza sec-'+it.seccion); a.append(dibujo(it),rotulo(it));
      if(it.antetitulo) a.append(el('p','antetitulo',it.antetitulo));
      var h=el('h2','w-titular'); h.append(enlace(it)); a.append(h);
      if(it.entradilla) a.append(el('p','w-entradilla',it.entradilla));
      caja.append(a); mas.href=it.url; mas.textContent=T.w_leer+' →'; return;
    }
    if(sec) lista=lista.filter(function(x){return sec==='biblioteca'?x.biblioteca:x.seccion===sec;});
    if(gr) lista=lista.filter(function(x){return x.grupo===gr;});
    lista=lista.slice(0,n);
    if(!lista.length){caja.append(el('p','w-aviso',T.w_sin)); return;}
    var ol=el('ol',estilo==='tarjetas'?'w-tarjetas':'w-lista');
    lista.forEach(function(it){
      var li=el('li','sec-'+it.seccion);
      if(estilo==='tarjetas') li.append(dibujo(it));
      var tx=el('div','w-texto'); tx.append(rotulo(it)); var h=el('h2','w-titular'); h.append(enlace(it)); tx.append(h);
      if(estilo==='tarjetas'&&it.entradilla) tx.append(el('p','w-entradilla',it.entradilla));
      li.append(tx); ol.append(li);
    });
    caja.append(ol);
  }
  var nombres=[]; if(sec) nombres.push(T.filtros[sec]); if(gr) nombres.push(GR[gr]);
  filtro.textContent=pieza?'':nombres.join(' · ');
  var origen=pieza?'datos/'+pieza.slice(0,7)+'.json':sec?'noticias-'+sec+'.json':gr?'noticias-'+gr+'.json':'noticias.json';
  fetch(origen).then(function(r){if(!r.ok)throw 0; return r.json();}).then(function(d){pinta(d.noticias||[]);})
    .catch(function(){caja.replaceChildren(el('p','w-aviso',T.w_error));});
})();
</script>"""

CSS_WIDGET = """
html, body { height: 100%; }
body.w { margin: 0; background: transparent; font-size: 1rem; line-height: 1.4; }
.w-caja { box-sizing: border-box; height: 100%; display: flex; flex-direction: column; background: var(--papel);
  border: 1px solid var(--filete); border-radius: 8px; overflow: hidden; }
.w-cab { display: flex; align-items: baseline; justify-content: space-between; gap: .6rem; flex-wrap: wrap;
  padding: .55rem .9rem .45rem; border-bottom: 3px double var(--tinta); }
.w-h1 { margin: 0; font-size: 1rem; line-height: 1.3; }
.w-marca { font-weight: 700; font-size: 1.15rem; color: var(--tinta); text-decoration: none; font-variation-settings: "opsz" 48; }
.w-filtro { font-style: italic; color: var(--tinta-2); font-size: .9rem; }
.w-contenido { flex: 1; min-height: 0; overflow: auto; padding: 0 .9rem; display: flex; flex-direction: column; }
.w-pie { padding: .45rem .9rem .55rem; border-top: 1px solid var(--filete); font-size: .92rem; }
.w-pie a, .w-titular a { color: var(--tinta); }
.w-titular { font-size: 1.05rem; line-height: 1.3; margin: .1rem 0 0; font-weight: 600; }
.w-titular a { text-decoration: none; }
.w-titular a:hover, .w-titular a:focus-visible { text-decoration: underline; }
.seccion { margin: 0; font-size: .82rem; font-weight: 600; display: flex; gap: .4rem; flex-wrap: wrap; }
.fecha-pieza { color: var(--tinta-2); font-weight: 400; font-style: italic; }
.w-lista, .w-tarjetas { list-style: none; margin: 0; padding: 0; }
.w-lista li { padding: .6rem 0 .6rem .7rem; border-left: 3px solid var(--sec, var(--tinta)); margin: .55rem 0; }
.w-tarjetas li { display: grid; grid-template-columns: minmax(6rem, 34%) 1fr; gap: .8rem; align-items: start;
  padding: .7rem 0; border-bottom: 1px solid var(--filete); }
.w-tarjetas li:last-child { border-bottom: 0; }
.w-tarjetas .ilu { margin: 0; padding: .3rem; border-radius: 4px; }
.w-tarjetas .ilu[hidden] + .w-texto { grid-column: 1 / -1; }
.w-entradilla { margin: .3rem 0 0; color: var(--tinta-2); font-size: .92rem;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.w-pieza { flex: 1; min-height: 0; display: flex; flex-direction: column; padding: .8rem 0; }
.w-pieza .ilu { position: relative; flex: 1 1 0; min-height: 7rem; margin: 0 0 .7rem; border-radius: 4px; }
/* El dibujo llena el sitio que deja el texto, sin deformarse: con poco alto, se encoge */
.w-pieza .ilu svg, .w-pieza .ilu img { position: absolute; inset: .5rem; width: calc(100% - 1rem); height: calc(100% - 1rem); object-fit: contain; }
.w-pieza .antetitulo { margin: .3rem 0 0; font-style: italic; color: var(--tinta-2); font-size: .95rem; }
.w-pieza .w-titular { font-size: 1.3rem; }
.w-pieza .w-entradilla { -webkit-line-clamp: 4; font-size: 1rem; }
.w-aviso { color: var(--tinta-2); font-style: italic; }
.ilu img { display: block; width: 100%; height: auto; }
@media (max-width: 22rem) { .w-tarjetas li { grid-template-columns: 1fr; } }
"""


def pagina_insertar():
    """El widget (ADR 0032): una página sin cabecera ni pie del diario, para un iframe en otra web. Lee
    noticias*.json o datos/AAAA-MM.json del mismo idioma; sin cookies ni contadores."""
    textos = {k: L[k] for k in ("w_sin", "w_error", "w_leer", "w_mas", "titulo")}
    textos["filtros"] = {c: nombre_filtro(c) for c in CLAVES_FILTRO}
    script = (SCRIPT_WIDGET.replace("__TEXTOS__", json.dumps(textos, ensure_ascii=False))
              .replace("__CLAVES__", json.dumps(CLAVES_FILTRO)).replace("__GRUPOS__", json.dumps({k: v[0] for k, v in GRUPOS.items()}, ensure_ascii=False)))
    r = recursos("")
    return f"""<!doctype html>
<html lang="{L["codigo"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L["titulo"])}</title>
<meta name="robots" content="noindex">
<script>try{{var t=new URLSearchParams(location.search).get('tema');if(t==='claro')document.documentElement.dataset.theme='light';else if(t==='oscuro')document.documentElement.dataset.theme='dark';}}catch(_){{}}</script>
<link rel="stylesheet" href="{r}fuentes.css?v={version_estatico("fuentes.css")}">
<link rel="stylesheet" href="{r}comun.css?v={version_estatico("comun.css")}">
<style>{CSS_WIDGET}</style>
</head>
<body class="w">
<div class="w-caja">
<header class="w-cab"><h1 class="w-h1"><a class="w-marca" href="{BASE}{L["carpeta"]}" target="_blank" rel="noopener">{L["titulo"]}</a></h1><span class="w-filtro" id="filtro"></span></header>
<main class="w-contenido" id="contenido" aria-live="polite"></main>
<footer class="w-pie"><a id="mas" href="{BASE}{L["carpeta"]}" target="_blank" rel="noopener">{L["w_mas"]} →</a></footer>
</div>
{script}
</body>
</html>"""


SCRIPT_PTW = """<script>
(function(){
  var B=__BASES__, f=document.getElementById('ptw-form'), vista=document.getElementById('ptw-iframe'), cod=document.getElementById('ptw-codigo'),
      alto=document.getElementById('ptw-alto'), tocado=false, espera=null, TITULO=__TITULO__;
  function v(n){var x=f.elements[n]; return x?x.value:'';}
  function altoSolo(){var n=Math.min(20,Math.max(1,parseInt(v('n'),10)||5)); return v('estilo')==='tarjetas'? 100+n*175 : 100+n*105;}
  function url(){
    var p=new URLSearchParams();
    ['seccion','grupo'].forEach(function(k){if(v(k))p.set(k,v(k));});
    if(v('n')&&v('n')!=='5')p.set('n',v('n')); if(v('estilo')==='lista')p.set('estilo','lista');
    if(v('tema')!=='auto')p.set('tema',v('tema'));
    var s=p.toString(); return B[v('idioma')]+'insertar.html'+(s?'?'+s:'');
  }
  function pinta(){
    if(!tocado) alto.value=altoSolo();
    var u=url(), h=Math.max(150,parseInt(alto.value,10)||400);
    cod.value='<iframe src="'+u.replace(/&/g,'&amp;')+'" title="'+TITULO[v('idioma')]+'" width="100%" height="'+h+'" style="border:0;max-width:640px" loading="lazy"></iframe>';
    clearTimeout(espera); espera=setTimeout(function(){ if(vista.getAttribute('src')!==u) vista.src=u; vista.height=h; },250);
  }
  alto.addEventListener('input',function(){tocado=true;});
  f.addEventListener('input',pinta); f.addEventListener('change',pinta);
  f.addEventListener('submit',function(ev){ev.preventDefault();});
  pinta();
})();
</script>"""


def pagina_para_tu_web(eds):
    """Cómo llevarse el diario a otra web (ADR 0032): el configurador del widget, con su vista previa y el
    código; y, plegados, la tarjeta de una pieza, los canales RSS y las condiciones para republicar."""
    opciones = f'<option value="">{L["ptw_todas"]}</option>' + "".join(f'<option value="{c}">{e(nombre_filtro(c))}</option>' for c in CLAVES_FILTRO)
    grupos = f'<option value="">{L["ptw_todos"]}</option>' + "".join(f'<option value="{k}">{e(n)}</option>' for k, (n, _) in GRUPOS.items())
    idiomas = "".join(f'<option value="{c}"{" selected" if c == L["codigo"] else ""} lang="{c}">{d["nombre"]}</option>' for c, d in IDIOMAS.items())

    def radios(nombre, valores):
        return "".join(f'<label><input type="radio" name="{nombre}" value="{val}"{" checked" if i == 0 else ""}> {rot}</label>'
                       for i, (val, rot) in enumerate(valores))
    copiar = lambda texto, rot, hecho: (f'<button type="button" class="compartir copiar" data-copiar="{e(texto)}" data-hecho="{e(hecho)}">'
                                        f'{ICONO_COPIAR}<span>{rot}</span></button>')
    canal = lambda clave: (f'<li><span class="nombre">{ICONO_RSS} {e(nombre_filtro(clave) if clave else L["ptw_rss_todo"])}</span>'
                           f'<code>{BASE}{L["carpeta"]}{archivo_feed(clave)}</code>'
                           f'{copiar(BASE + L["carpeta"] + archivo_feed(clave), L["ptw_copiar_dir"], L["ptw_dir_copiada"])}</li>')
    canales = (f'<ul class="ptw-canales">{canal(None)}</ul><h3>{L["ptw_secciones"]}</h3><ul class="ptw-canales">{"".join(canal(c) for c in CLAVES_FILTRO)}</ul>'
               f'<h3>{L["ptw_grupos"]}</h3><ul class="ptw-canales">{"".join(canal(g) for g in GRUPOS)}</ul>')
    condiciones = "".join(f"<li>{t}</li>" for t in L["ptw_repub_lista"])
    licencia = enlace(LICENCIA_URL + L["deed"], "CC BY-SA 4.0")
    bases = json.dumps({c: BASE + d["carpeta"] for c, d in IDIOMAS.items()})
    titulos = json.dumps({c: d["titulo"] for c, d in IDIOMAS.items()}, ensure_ascii=False)
    script = SCRIPT_PTW.replace("__BASES__", bases).replace("__TITULO__", titulos)
    return cabeza(L["ptw_titulo"], "", L["ptw_txt"], "para-tu-web.html") + f"""<body class="pag-seccion">
{cabecera("", "para-tu-web.html", eds[-1]["fecha"], eds[-1]["numero"], True, h1=False)}
<main class="portada pagina-ptw">
<h1 class="titulo-seccion">{ICONO_LLEVAR} {L["ptw_titulo"]}</h1>
<p class="descripcion-seccion">{L["ptw_txt"]}</p>
<section class="ptw-widget" aria-labelledby="ptw-w">
<h2 id="ptw-w">{L["ptw_widget_h"]}</h2>
<p>{L["ptw_widget_txt"]}</p>
<div class="ptw-rejilla">
<form id="ptw-form" class="ptw-form">
  <div class="ptw-campo"><label for="ptw-seccion">{L["ptw_noticias"]}</label><select id="ptw-seccion" name="seccion">{opciones}</select></div>
  <div class="ptw-campo"><label for="ptw-grupo">{L["ptw_grupo"]}</label><select id="ptw-grupo" name="grupo">{grupos}</select></div>
  <div class="ptw-campo"><label for="ptw-n">{L["ptw_cuantas"]}</label><input id="ptw-n" name="n" type="number" min="1" max="20" value="5" inputmode="numeric"></div>
  <div class="ptw-campo"><label for="ptw-idioma">{L["idioma"]}</label><select id="ptw-idioma" name="idioma">{idiomas}</select></div>
  <fieldset class="ptw-campo"><legend>{L["ptw_aspecto"]}</legend><div class="ptw-opciones">{radios("estilo", [("tarjetas", ICONO_TARJETAS + " " + L["ptw_tarjetas"]), ("lista", ICONO_LISTA + " " + L["ptw_lista"])])}</div></fieldset>
  <fieldset class="ptw-campo"><legend>{L["ptw_tema"]}</legend><div class="ptw-opciones">{radios("tema", [("auto", L["ptw_tema_auto"]), ("claro", L["ptw_claro"]), ("oscuro", L["ptw_oscuro"])])}</div></fieldset>
  <div class="ptw-campo"><label for="ptw-alto">{L["ptw_alto"]}</label><input id="ptw-alto" name="alto" type="number" min="150" max="3000" step="10" value="975" inputmode="numeric"></div>
</form>
<div class="ptw-resultado">
  <h3>{L["ptw_vista"]}</h3>
  <div class="ptw-vista"><iframe id="ptw-iframe" title="{e(L["ptw_vista"])}" width="100%" height="975"></iframe></div>
</div>
</div>
<div class="ptw-codigo">
  <label for="ptw-codigo"><b>{L["ptw_codigo"]}</b></label>
  <textarea id="ptw-codigo" rows="3" readonly spellcheck="false"></textarea>
  <p><button type="button" class="compartir copiar" data-desde="ptw-codigo" data-hecho="{e(L["ptw_copiado"])}">{ICONO_COPIAR}<span>{L["ptw_copiar"]}</span></button></p>
  <p class="ptw-nota">{L["ptw_donde"]}</p>
</div>
</section>
<details class="ptw-mas" id="noticia"><summary>{L["ptw_pieza_h"]}</summary><p>{L["ptw_pieza_txt"]}</p></details>
<details class="ptw-mas" id="rss"><summary>{L["ptw_rss_h"]}</summary><p>{L["ptw_rss_txt"]}</p>{canales}</details>
<details class="ptw-mas" id="republicar"><summary>{L["ptw_repub_h"]}</summary><p>{L["ptw_repub_txt"].format(licencia=licencia)}</p><ul>{condiciones}</ul><p>{L["ptw_repub_retirar"]}</p></details>
</main>
{pie("", eds, None)}
{SCRIPT_TEMA}
{script}
</body>
</html>"""


def manifiesto():
    """La ficha que permite instalar el diario como app desde el navegador (ADR 0013), una por idioma:
    la instalada desde /ca/ se abre en catalán. Sin avisos; el service worker (estaticos/sw.js, ADR 0042) solo
    sirve lo guardado cuando no hay conexión, así que con conexión siempre se lee lo publicado."""
    raiz = "/" + L["carpeta"]
    return json.dumps({
        "id": raiz, "start_url": raiz, "scope": raiz,
        "name": L["titulo"], "short_name": L["nombre_corto"], "description": L["lema"],
        "lang": L["codigo"], "dir": "ltr",
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
            parrafos = [t for a in r.get("apartados", []) for t in [a.get("ladillo", "")] + a.get("parrafos", []) + texto_tabla(a.get("tabla"))]
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


# Lo que mira cada mañana la app de Android para avisar del número (ADR 0043): el último, el día en que
# sale (hora de Madrid) y, en cada idioma, su portada y el titular de la primera pieza
ULTIMO = {}


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
             pagina_portada("", "", eds, piezas, breves, eds[-1]["fecha"], eds[-1]["numero"], True,
                            ant=f'{eds[-2]["fecha"]}/' if len(eds) > 1 else ""))   # «Día anterior», flecha ante «Portada»
    escribir(base / "redaccion.html", pagina_redaccion(eds))
    escribir(base / "contacto.html", pagina_contacto(eds))
    escribir(base / "que-es.html", redireccion("redaccion.html"))
    escribir(base / "comunidad.html", redireccion("vibecoding.html"))   # la sección retirada el 01-11-2026
    for clave in TODAS_SECCIONES:
        escribir(base / f"{clave}.html", pagina_seccion(eds, clave))
    escribir(base / "vineta.html", pagina_vinetas(eds))
    escribir(base / "videos.html", pagina_videos(eds))
    escribir(base / "reportajes.html", pagina_reportajes(eds))
    escribir(base / "breves.html", pagina_breves(eds))
    for cfg in listas(eds):   # cada mes de las páginas que acumulan (ADR 0050)
        if len(cfg["items"]) > cfg["n"]:
            for m in meses_lista(cfg):
                escribir(base / cfg["carpeta"] / f"{m}.html", pagina_lista(eds, cfg, m))
    escribir(base / "buscar.html", pagina_buscar(eds))
    escribir(base / "archivo.html", pagina_hemeroteca(eds))
    shutil.rmtree(base / "semana", ignore_errors=True)
    shutil.rmtree(base / "mes", ignore_errors=True)
    sems = list(por_semanas(eds))
    for i, sem in enumerate(sems):   # la semana y el mes (ADR 0034)
        escribir(base / "semana" / sem / "index.html",
                 pagina_semana(eds, sem, sems[i - 1] if i else None, sems[i + 1] if i + 1 < len(sems) else None))
    # /semana/ a secas lleva a la última semana con el pódcast y el vídeo de los grupos (o a la más
    # reciente, si aún no hay ninguna), con el grupo que se pida: es el enlace fijo que dan las webs de
    # los boletines antiguos (ADR 0034).
    if sems:
        destino = next((s for s in reversed(sems) if cargar_multimedia(s)), sems[-1])
        escribir(base / "semana" / "index.html", f"""<!doctype html>
<html lang="{L["codigo"]}"><head><meta charset="utf-8"><title>{L["hemeroteca"]} | {L["titulo"]}</title>
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={destino}/">
<link rel="canonical" href="{BASE}{L["carpeta"]}semana/{destino}/">
<script>location.replace("{destino}/" + location.search + location.hash);</script></head>
<body><p><a href="{destino}/">{titulo_semana(destino)}</a></p></body></html>
""")
    meses = meses_y_semanas(eds)
    claves = list(meses)
    for i, mes in enumerate(claves):
        escribir(base / "mes" / mes / "index.html",
                 pagina_mes(eds, mes, meses[mes], claves[i - 1] if i else None, claves[i + 1] if i + 1 < len(claves) else None))
    publicar_canales(base, eds)   # RSS y datos para el widget (ADR 0032)
    escribir(base / "insertar.html", pagina_insertar())
    escribir(base / "para-tu-web.html", pagina_para_tu_web(eds))
    shutil.rmtree(base / "ilustraciones", ignore_errors=True)   # los dibujos sueltos, sin restos de piezas retiradas
    for d in eds:
        for x in d["piezas"]:
            dibujo_suelto(d["fecha"], x, x.get("seccion", ""))
        if d.get("reportaje"):
            dibujo_suelto(d["fecha"], d["reportaje"], "reportaje")
    escribir(base / "manifest.webmanifest", manifiesto())
    escribir(base / "sin-conexion.html", pagina_sin_conexion())
    ultimo = eds[-1]
    ULTIMO[codigo] = {"url": BASE + L["carpeta"], "titulo": L["titulo"],
                      "titular": texto_plano(ultimo["piezas"][0].get("titular", "")) if ultimo["piezas"] else ""}
    if codigo == "es":
        ULTIMO.update(numero=ultimo["numero"], sale=publicacion(ultimo["fecha"]))
    if codigo == "es":
        escribir(RAIZ / "indice" / "diario.json", indice_bot(eds))   # para el bot, no se publica (ADR 0017)
        escribir(SITIO / "404.html", pagina_404(eds))
        escribir(SITIO / "sitemap.xml", sitemap(eds))
        # Sin vetos: solo dice a los buscadores dónde está el mapa del sitio (ADR 0039)
        escribir(SITIO / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    for i, d in enumerate(eds):
        dia = base / d["fecha"]
        escribir(dia / "index.html",
                 pagina_portada("../", f'{d["fecha"]}/', eds, d["piezas"], d.get("breves", []), d["fecha"],
                                d["numero"], False, ant=f'../{eds[i - 1]["fecha"]}/' if i else "",
                                sig=f'../{eds[i + 1]["fecha"]}/' if i + 1 < len(eds) else ""))
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
    for viejo in [SITIO / "diario", SITIO / "revista", SITIO / "revista.css"] + \
            [SITIO / d["carpeta"] for d in IDIOMAS.values() if d["carpeta"]] + \
            [p for p in SITIO.iterdir() if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)]:
        if viejo.is_dir():
            shutil.rmtree(viejo)
        elif viejo.exists():
            viejo.unlink()
    shutil.rmtree(SITIO / "videos", ignore_errors=True)
    if (RAIZ / "videos").exists():   # las portadas y los vídeos que aún no están en Internet Archive (ADR 0016 y 0037)
        (SITIO / "videos").mkdir()
        en_archive = {a["video"] for v in cargar_videos() if v.get("archive") for a in v["archivos"].values()}
        for f in (RAIZ / "videos").iterdir():
            if f.suffix == ".jpg" or (f.suffix == ".mp4" and f.name not in en_archive):
                shutil.copy(f, SITIO / "videos" / f.name)
    if (RAIZ / "og" / "numeros").exists():   # la imagen de vista previa de cada número (ADR 0010)
        shutil.copytree(RAIZ / "og" / "numeros", SITIO / "og", dirs_exist_ok=True)
    if (RAIZ / "portadas").exists():   # la portada de cada número para la hemeroteca (ADR 0053)
        shutil.copytree(RAIZ / "portadas", SITIO / "portadas", dirs_exist_ok=True, ignore=shutil.ignore_patterns("*.json"))
    entradas_grupos()
    for codigo in IDIOMAS:
        generar_idioma(codigo)
    escribir(SITIO / "ultimo.json", json.dumps({"numero": ULTIMO.pop("numero"), "sale": ULTIMO.pop("sale"),
                                                "idiomas": ULTIMO}, ensure_ascii=False, indent=1) + "\n")


def pieza_de_grupo(d, grupo):
    """La pieza que da imagen al aviso de un grupo: la primera de sus conversaciones que no es de la
    Biblioteca (ADR 0010). Si ese día el grupo no tiene ninguna, None: el aviso lleva la del número."""
    return next((p for p in d["piezas"] if p.get("grupo") == grupo and p.get("seccion") not in ["biblioteca"] + SECCIONES_FUERA), None)


def entradas_grupos():
    """Una página de entrada por número y grupo (n/<número>-<grupo>.html): solo lleva la imagen de
    vista previa de ese grupo y lleva al lector a la portada del número. Así Telegram enseña en cada
    grupo una imagen distinta, aunque los tres avisos abran la misma portada (ADR 0010)."""
    global L
    L = IDIOMAS["es"]   # los avisos van en castellano en los tres grupos
    shutil.rmtree(SITIO / "n", ignore_errors=True)
    for d in cargar():
        if not d.get("numero"):
            continue
        for g in GRUPOS:
            p = pieza_de_grupo(d, g)
            if not p or not (RAIZ / "og" / "numeros" / f'{d["fecha"]}-es-{g}.png').exists():
                continue
            (SITIO / "n").mkdir(exist_ok=True)
            destino = f'../?n={d["numero"]}'
            titulo = f'{L["titulo"]} · {L["num"]} {d["numero"]}'
            (SITIO / "n" / f'{d["numero"]}-{g}.html').write_text(f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>{e(titulo)}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}?n={d["numero"]}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(L["titulo"])}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(p["titular"])}">
<meta property="og:url" content="{BASE}n/{d["numero"]}-{g}.html">
<meta property="og:image" content="{BASE}og/{d["fecha"]}-es-{g}.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta http-equiv="refresh" content="0; url={destino}">
<script>location.replace("{destino}")</script>
</head><body><p><a href="{destino}">{e(titulo)}</a></p></body></html>
""")


if __name__ == "__main__":
    main()
