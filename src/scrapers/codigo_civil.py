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

last_parte = ''
last_libro = ''
last_titulo = ''
last_subtitulo = ''
last_capitulo = ''
last_seccion = ''
last_subseccion = ''
last_articulo = ''


def __isTitulo(soup):
	attrs = soup.attrs
	if soup.p is not None:
		attrs = soup.p.attrs
	if 'align' in attrs:
		return attrs['align'].lower() == 'center'
	return False

''' Metodo principal para cada parrafo (p) a procesar '''
def __procesarParrafo(soup):
	global ley_id, last_parte_id, last_libro_id, last_titulo_id, last_subtitulo_id, last_capitulo_id, last_seccion_id, last_subseccion_id, last_segmento_id, last_articulo_id, start_articles, end_of_code, last_parte, last_libro, last_titulo, last_subtitulo, last_capitulo, last_seccion, last_subseccion, last_articulo
	if (__isTitulo(soup)):
		numeracion = hard_code_util.getNumeroTitular(soup.text)
		if hard_code_util.isParte(soup.text):
			last_libro = last_titulo = last_capitulo = last_seccion = last_subseccion = ''
			last_parte = numeracion
			last_segmento_id = last_parte_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_PARTE, ley_id, ley_id, 'parte' + last_parte)
		elif hard_code_util.isLibro(soup.text):
			last_titulo = last_capitulo = last_seccion = last_subseccion = ''
			last_libro = numeracion
			last_segmento_id = last_libro_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_LIBRO, ley_id, last_parte_id,'parte' + last_parte + '|libro' + last_libro)
		elif hard_code_util.isSubTitulo(soup.text):
			last_capitulo = last_seccion = last_subseccion = ''
			last_subtitulo = numeracion
			last_segmento_id = last_subtitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBTITULO, ley_id, last_titulo_id, 'parte' + last_parte + '|libro' + last_libro + '|titulo' + last_titulo + '|subtitulo' + last_subtitulo)
		elif hard_code_util.isTitulo(soup.text):
			last_subtitulo = last_capitulo = last_seccion = last_subseccion = ''
			last_titulo = numeracion
			last_segmento_id = last_titulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_TITULO, ley_id, last_libro_id, 'parte' + last_parte + '|libro' + last_libro + '|titulo' + last_titulo)
		elif hard_code_util.isCapitulo(soup.text):
			last_seccion = last_subseccion = ''
			last_capitulo = numeracion
			cad = 'parte' + last_parte + '|libro' + last_libro + '|titulo' + last_titulo
			id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "|subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			cad += '|capitulo' + last_capitulo
			last_segmento_id = last_capitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_CAPITULO, ley_id, id_parent, cad)
		elif hard_code_util.isSeccion(soup.text):
			last_subseccion = ''
			last_seccion = numeracion
			cad = 'parte' + last_parte + '|libro' + last_libro + '|titulo' + last_titulo
			id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "|subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			if last_capitulo != '':
				cad += "|capitulo" + last_capitulo
				id_parent = last_capitulo_id
			cad += '|seccion' + last_seccion
			last_segmento_id = last_seccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SECCION, ley_id, id_parent, cad)
		elif hard_code_util.isSubSeccion(soup.text):
			last_subseccion = numeracion
			cad = 'parte' + last_parte + '|libro' + last_libro + '|titulo' + last_titulo
			id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "|subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			if last_capitulo != '':
				cad += "|capitulo" + last_capitulo
				id_parent = last_capitulo_id
			if last_seccion != '':
				cad += '|seccion' + last_seccion
				id_parent = last_seccion_id
			cad += '|subseccion' + last_subseccion
			last_segmento_id = last_subseccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBSECCION, ley_id, id_parent, cad)
	else:
		if hard_code_util.isArticulo(soup.text):
			cad = 'parte' + last_parte + '|libro' + last_libro + '|titulo' + last_titulo
			id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "|subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			if last_capitulo != '':
				cad += "|capitulo" + last_capitulo
				id_parent = last_capitulo_id
			if last_seccion != '':
				cad += '|seccion' + last_seccion
				id_parent = last_seccion_id
			if last_subseccion != '':
				cad += '|subseccion' + last_subseccion
				id_parent = last_subseccion_id
			cad = cad + '|articulo' + hard_code_util.getNumeroArticulo(soup.text)
			if soup.find('strike') is not None:
				cad += '-'
			last_articulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent, cad)
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