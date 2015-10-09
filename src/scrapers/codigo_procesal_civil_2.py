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
start_articles = False
end_of_code = ''

last_parte = ''
last_libro = ''
last_titulo = ''
last_subtitulo = ''
last_capitulo = ''
last_seccion = ''
last_subseccion = ''

idnetificador_articulo = ''
articulo_completo = ''
id_parent_articulo = 0

next = None
sw_together = False

def __isTitulo(soup):
	attrs = soup.attrs
	if soup.p is not None:
		attrs = soup.p.attrs
	if 'align' in attrs:
		return attrs['align'].lower() == 'center'
	return False

''' Metodo principal para cada parrafo (p) a procesar '''
def __procesarParrafo(soup):
	global sw_together, next, ley_id, last_parte_id, last_libro_id, last_titulo_id, last_subtitulo_id, last_capitulo_id, last_seccion_id, last_subseccion_id, last_segmento_id, start_articles, end_of_code, last_parte, last_libro, last_titulo, last_subtitulo, last_capitulo, last_seccion, last_subseccion, articulo_completo, idnetificador_articulo, id_parent_articulo
	if (__isTitulo(soup)):
		if articulo_completo != '':
			dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent_articulo, idnetificador_articulo)
			idnetificador_articulo = ''
			articulo_completo = ''
		numeracion = hard_code_util.getNumeroTitular2(soup.text)
		if hard_code_util.isParte(soup.text):
			last_libro = last_titulo = last_subtitulo = last_capitulo = last_seccion = last_subseccion = ''
			last_parte = numeracion
			last_segmento_id = last_parte_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_PARTE, ley_id, ley_id, 'parte' + last_parte)
		elif hard_code_util.isLibro(soup.text):
			last_titulo = last_subtitulo = last_capitulo = last_seccion = last_subseccion = ''
			last_libro = numeracion
			if sw_together:
				last_segmento_id = last_libro_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_LIBRO, ley_id, last_parte_id,'parte' + last_parte + '_libro' + last_libro)
			else:
				next = next.find_next('p')
				last_segmento_id = last_libro_id = dao.segmentoDAO.insert(str(soup) + str(next), dao.segmentoDAO.TIPO_LIBRO, ley_id, last_parte_id,'parte' + last_parte + '_libro' + last_libro)
		elif hard_code_util.isSubTitulo(soup.text):
			last_capitulo = last_seccion = last_subseccion = ''
			last_subtitulo = numeracion
			if sw_together:
				last_segmento_id = last_subtitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBTITULO, ley_id, last_titulo_id, 'parte' + last_parte + '_libro' + last_libro + '_titulo' + last_titulo + '_subtitulo' + last_subtitulo)
			else:
				next = next.find_next('p')
				last_segmento_id = last_subtitulo_id = dao.segmentoDAO.insert(str(soup) + str(next), dao.segmentoDAO.TIPO_SUBTITULO, ley_id, last_titulo_id, 'parte' + last_parte + '_libro' + last_libro + '_titulo' + last_titulo + '_subtitulo' + last_subtitulo)
		elif hard_code_util.isTitulo(soup.text):
			if 'TÍTULO VI' in soup.text.encode('utf-8'):
				sw_together = True
			last_subtitulo = last_capitulo = last_seccion = last_subseccion = ''
			last_titulo = numeracion
			if sw_together:
				last_segmento_id = last_titulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_TITULO, ley_id, last_libro_id, 'parte' + last_parte + '_libro' + last_libro + '_titulo' + last_titulo)
			else:
				next = next.find_next('p')
				last_segmento_id = last_titulo_id = dao.segmentoDAO.insert(str(soup) + str(next), dao.segmentoDAO.TIPO_TITULO, ley_id, last_libro_id, 'parte' + last_parte + '_libro' + last_libro + '_titulo' + last_titulo)
		elif hard_code_util.isCapitulo(soup.text):
			last_seccion = last_subseccion = ''
			last_capitulo = numeracion
			cad = 'parte' + last_parte + '_libro' + last_libro + '_titulo' + last_titulo
			id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "_subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			cad += '_capitulo' + last_capitulo
			if sw_together:
				last_segmento_id = last_capitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_CAPITULO, ley_id, id_parent, cad)
			else:
				next = next.find_next('p')
				last_segmento_id = last_capitulo_id = dao.segmentoDAO.insert(str(soup) + str(next), dao.segmentoDAO.TIPO_CAPITULO, ley_id, id_parent, cad)
		elif hard_code_util.isSeccion(soup.text):
			last_subseccion = ''
			last_seccion = numeracion
			cad = 'parte' + last_parte + '_libro' + last_libro + '_titulo' + last_titulo
			id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "_subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			if last_capitulo != '':
				cad += "_capitulo" + last_capitulo
				id_parent = last_capitulo_id
			cad += '_seccion' + last_seccion
			if sw_together:
				last_segmento_id = last_seccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SECCION, ley_id, id_parent, cad)
			else:
				next = next.find_next('p')
				last_segmento_id = last_seccion_id = dao.segmentoDAO.insert(str(soup) + str(next), dao.segmentoDAO.TIPO_SECCION, ley_id, id_parent, cad)
		elif hard_code_util.isSubSeccion(soup.text):
			last_subseccion = numeracion
			cad = 'parte' + last_parte + '_libro' + last_libro + '_titulo' + last_titulo
			id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "_subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			if last_capitulo != '':
				cad += "_capitulo" + last_capitulo
				id_parent = last_capitulo_id
			if last_seccion != '':
				cad += '_seccion' + last_seccion
				id_parent = last_seccion_id
			cad += '_subseccion' + last_subseccion
			if sw_together:
				last_segmento_id = last_subseccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBSECCION, ley_id, id_parent, cad)
			else:
				next = next.find_next('p')
				last_segmento_id = last_subseccion_id = dao.segmentoDAO.insert(str(soup) + str(next), dao.segmentoDAO.TIPO_SUBSECCION, ley_id, id_parent, cad)
	else:
		if hard_code_util.isArticulo(soup.text):
			cad = 'parte' + last_parte + '_libro' + last_libro
			id_parent = last_titulo_id
			if last_titulo != '':
				cad += '_titulo' + last_titulo
				id_parent = last_titulo_id
			if last_subtitulo != '':
				cad += "_subtitulo" + last_subtitulo
				id_parent = last_subtitulo_id
			if last_capitulo != '':
				cad += "_capitulo" + last_capitulo
				id_parent = last_capitulo_id
			if last_seccion != '':
				cad += '_seccion' + last_seccion
				id_parent = last_seccion_id
			if last_subseccion != '':
				cad += '_subseccion' + last_subseccion
				id_parent = last_subseccion_id
			cad = cad + '_articulo' + hard_code_util.getNumeroArticulo(soup.text)
			if soup.find('strike') is not None:
				cad += '-'
			if articulo_completo != '':
				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent, idnetificador_articulo)
				id_parent_articulo = id_parent
			idnetificador_articulo = cad
			articulo_completo = str(soup)
			start_articles = True
		elif start_articles:
			if not __isTitulo(soup):
				articulo_completo += str(soup)

def procesarLegislacion(soup):
	try:
		global ley_id, end_of_code, next
		id_ley = dao.leyDAO.selectIDSegmento(hard_code_util.ID_LEGISLACION_CODIGO_PROCESAL_CIVIL_2)
		dao.segmentoDAO.deleteSegmentos(id_ley)
		dao.leyDAO.deleteLey(hard_code_util.ID_LEGISLACION_CODIGO_PROCESAL_CIVIL_2)
		ley_id = dao.segmentoDAO.insert('<p align="left"><font face="Arial" color="#800000" size="2">Institui o Código de Processo Civil.</font></p>', dao.segmentoDAO.TIPO_LEY, None, None, 'L13105')
		logger.info('Segmento - Ley registrada correctamente, ID = ' + str(ley_id))
		dao.leyDAO.insert('INSTITUI O CÓDIGO DE PROCESSO CIVIL', '', ley_id, datetime.now(), hard_code_util.ID_LEGISLACION_CODIGO_PROCESAL_CIVIL_2)
		logger.info('Ley registrada correctamente')
		titulo = soup.find('p', {'class' : 'MsoNormal'})
		next = titulo.find_next('p')
		while next is not None:
			__procesarParrafo(next)
			next = next.find_next('p')
	except Exception, e:
		logger.error('Error general : ' + str(e))
		raise