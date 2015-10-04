# -*- coding: latin-1 -*-

import os.path, sys
from bs4 import BeautifulSoup
import hard_code_util
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dao.segmentoDAO
import dao.leyDAO
import logger

ley_id = 0
last_parte_id = 0
last_libro_id = 0
last_titulo_id = 0
last_subtitulo_id = 0
last_capitulo_id = 0
last_seccion_id = 0
last_subseccion_id = 0
last_segmento_id = 0
last_articulo_id = 0
start_articles = False
end_of_code = ''

cont_parte = 0
cont_libro = 0
cont_titulo = 0
cont_subtitulo = 0
cont_capitulo = 0
cont_seccion = 0
cont_subseccion = 0
cont_articulo = 0


def __isTitulo(soup):
	attrs = soup.attrs
	if soup.p is not None:
		attrs = soup.p.attrs
	if 'align' in attrs:
		return attrs['align'].lower() == 'center'
	return False

''' Metodo principal para cada parrafo (p) a procesar '''
def __procesarParrafo(soup):
	global ley_id, last_parte_id, last_libro_id, last_titulo_id, last_subtitulo_id, last_capitulo_id, last_seccion_id, last_subseccion_id, last_segmento_id, last_articulo_id, start_articles, end_of_code, cont_parte, cont_libro, cont_titulo, cont_subtitulo, cont_capitulo, cont_seccion, cont_subseccion, cont_articulo
	if (__isTitulo(soup)):
		if hard_code_util.isParte(soup.text):
			cont_libro = cont_titulo = cont_capitulo = cont_seccion = cont_subseccion = 0
			cont_parte += 1
			last_segmento_id = last_parte_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_PARTE, ley_id, ley_id, 'parte' + str(cont_parte))
		elif hard_code_util.isLibro(soup.text):
			cont_titulo = cont_capitulo = cont_seccion = cont_subseccion = 0
			cont_libro += 1
			last_segmento_id = last_libro_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_LIBRO, ley_id, last_parte_id,'parte' + str(cont_parte) + '|libro' + str(cont_libro))
		elif hard_code_util.isSubTitulo(soup.text):
			cont_capitulo = cont_seccion = cont_subseccion = 0
			cont_subtitulo += 1
			last_segmento_id = last_subtitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBTITULO, ley_id, last_titulo_id, 'parte' + str(cont_parte) + '|libro' + str(cont_libro) + '|titulo' + str(cont_titulo) + '|subtitulo' + str(cont_subtitulo))
		elif hard_code_util.isTitulo(soup.text):
			cont_subtitulo = cont_capitulo = cont_seccion = cont_subseccion = 0
			cont_titulo += 1
			last_segmento_id = last_titulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_TITULO, ley_id, last_libro_id, 'parte' + str(cont_parte) + '|libro' + str(cont_libro) + '|titulo' + str(cont_titulo))
		elif hard_code_util.isCapitulo(soup.text):
			cont_seccion = cont_subseccion = 0
			cont_capitulo += 1
			cad = 'parte' + str(cont_parte) + '|libro' + str(cont_libro) + '|titulo' + str(cont_titulo)
			id_parent = last_titulo_id
			if cont_subtitulo > 0:
				cad += "|subtitulo" + str(cont_subtitulo)
				id_parent = last_subtitulo_id
			cad += '|capitulo' + str(cont_capitulo)
			last_segmento_id = last_capitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_CAPITULO, ley_id, id_parent, cad)
		elif hard_code_util.isSeccion(soup.text):
			cont_subseccion = 0
			cont_seccion += 1
			cad = 'parte' + str(cont_parte) + '|libro' + str(cont_libro) + '|titulo' + str(cont_titulo)
			id_parent = last_titulo_id
			if cont_subtitulo > 0:
				cad += "|subtitulo" + str(cont_subtitulo)
				id_parent = last_subtitulo_id
			if cont_capitulo > 0:
				cad += "|capitulo" + str(cont_capitulo)
				id_parent = last_capitulo_id
			cad += '|seccion' + str(cont_seccion)
			last_segmento_id = last_seccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SECCION, ley_id, id_parent, cad)
		elif hard_code_util.isSubSeccion(soup.text):
			cont_subseccion += 1
			cad = 'parte' + str(cont_parte) + '|libro' + str(cont_libro) + '|titulo' + str(cont_titulo)
			id_parent = last_titulo_id
			if cont_subtitulo > 0:
				cad += "|subtitulo" + str(cont_subtitulo)
				id_parent = last_subtitulo_id
			if cont_capitulo > 0:
				cad += "|capitulo" + str(cont_capitulo)
				id_parent = last_capitulo_id
			if cont_seccion > 0:
				cad += '|seccion' + str(cont_seccion)
				id_parent = last_seccion_id
			cad += '|subseccion' + str(cont_subseccion)
			last_segmento_id = last_subseccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBSECCION, ley_id, id_parent, cad)
	else:
		if hard_code_util.isArticulo(soup.text):
			cad = 'parte' + str(cont_parte) + '|libro' + str(cont_libro) + '|titulo' + str(cont_titulo)
			id_parent = last_titulo_id
			if cont_subtitulo > 0:
				cad += "|subtitulo" + str(cont_subtitulo)
				id_parent = last_subtitulo_id
			if cont_capitulo > 0:
				cad += "|capitulo" + str(cont_capitulo)
				id_parent = last_capitulo_id
			if cont_seccion > 0:
				cad += '|seccion' + str(cont_seccion)
				id_parent = last_seccion_id
			if cont_subseccion > 0:
				cad += '|subseccion' + str(cont_subseccion)
				id_parent = last_subseccion_id
			if soup.find('strike') is None:
				cont_articulo += 1
				last_articulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent, cad + '|articulo' + str(cont_articulo))
			else:
				last_articulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent, cad + '|articulo' + str(cont_articulo + 1) + '-')
			start_articles = True
		elif start_articles:
			if not __isTitulo(soup):
				dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_ITEM_ARTICULO, ley_id, last_articulo_id)

def procesarLegislacion(soup):
	try:
		global ley_id, end_of_code
		id_ley = dao.leyDAO.selectIDSegmento(hard_code_util.ID_LEGISLACION_CODIGO_CIVIL)
		dao.segmentoDAO.deleteSegmentos(id_ley)
		dao.leyDAO.deleteLey(hard_code_util.ID_LEGISLACION_CODIGO_CIVIL)
		ley_id = dao.segmentoDAO.insert('<p align="left"><font face="Arial" color="#800000" size="2">Institui o Código Civil.</font></p>', dao.segmentoDAO.TIPO_LIBRO, None)
		logger.info('Segmento - Ley registrada correctamente, ID = ' + str(ley_id))
		dao.leyDAO.insert('INSTITUI O CÓDIGO CIVIL', '', ley_id, datetime.now(), hard_code_util.ID_LEGISLACION_CODIGO_CIVIL)
		logger.info('Ley registrada correctamente')
		titulo = soup.find('p', {'style': 'text-indent: 30px'})
		next = titulo.find_next('p')
		while next is not None:
			__procesarParrafo(next)
			next = next.find_next('p')
		#id_footer = dao.segmentoDAO.insert(end_of_code, dao.segmentoDAO.TIPO_FOOTER, ley_id, ley_id)
	except Exception, e:
		logger.error('Error general : ' + str(e))
		raise