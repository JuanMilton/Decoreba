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
last_titulo_id = 0
last_capitulo_id = 0
last_seccion_id = 0
last_subseccion_id = 0
last_segmento_id = 0
last_articulo_id = 0
start_articles = False
end_of_code = ''

last_titulo = ''
last_capitulo = ''
last_seccion = ''
last_subseccion = ''
last_articulo = ''

idnetificador_articulo = ''
articulo_completo = ''
id_parent_articulo = 0

def __separarTituloCompuesto(soup):
	tags_a = soup.find_all(['a'])
	tags_name = []
	for item in tags_a:
		if item.attrs['name'] is not None:
			tags_name.append(item.attrs['name'])
		else:
			print 'ERROR, el tag no tiene un atributo nombre'
			return []
	if (len(tags_name) == 2):
		if tags_name[0] == 'tituloii' and tags_name[1] == 'tituloiicapituloi':
			logger.info('Excepcion procesada : tituloii - tituloiicapituoi')
			tag1 = '<p align=\'center\'><font face=\'Arial\' size=\'2\'><a name=\'tituloii\'></a><span style=\'text-transform: uppercase\'><b>TÍTULO II<br>Dos Direitos e Garantias Fundamentais</b></span></font></p>'
			tag2 = '<p align=\'center\'><font face=\'Arial\' size=\'2\'><br><a name=\'tituloiicapituloi\'></a>CAPÍTULO I<br>DOS DIREITOS E DEVERES INDIVIDUAIS E COLETIVOS</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiii' and tags_name[1] == 'tituloiiicapituloi':
			logger.info('Excepcion procesada : tituloiii - tituloiiicapituloi')
			tag1 = '<p align="center"><font face="Arial" color="#000000" size="3"><a name="tituloiii"></a></font><font face="Arial" color="#000000" size="2"><span style="text-transform: uppercase"><b>TÍTULO III<br>Da Organização do Estado</b></span></font></p>'
			tag2 = '<p align="center"><font face="Arial" color="#000000" size="3"><br></font><font face="Arial" size="2"><a name="tituloiiicapituloi"></a>CAPÍTULO I<br>DA ORGANIZAÇÃO POLÍTICO-ADMINISTRATIVA</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiiicapitulov' and tags_name[1] == 'tituloiiicapitulovsecaoi':
			logger.info('Excepcion procesada : tituloiiicapitulov - tituloiiicapitulovsecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulov"></a>CAPÍTULO V<br>DO DISTRITO FEDERAL E DOS TERRITÓRIOS</font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulovsecaoi"></a><span style="text-transform: uppercase"><b>Seção I<br>DO DISTRITO FEDERAL</b></span></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiiicapitulovii' and tags_name[1] == 'tituloiiicapituloviisecaoi':
			logger.info('Excepcion procesada : tituloiiicapitulovii - tituloiiicapituloviisecaoi')
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulovii"></a>CAPÍTULO VII<br>DA ADMINISTRAÇÃO PÚBLICA</font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapituloviisecaoi"></a><b><span style="text-transform: uppercase">Seção I<br>DISPOSIÇÕES GERAIS</span></b></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]

def __isTitulo(soup):
	attrs = soup.attrs
	if soup.p is not None:
		attrs = soup.p.attrs
	if 'align' in attrs:
		return attrs['align'].lower() == 'center'
	return False

def __isTituloCompuesto(soup):
	tags_a = soup.find_all(['a'])
	total = 0
	for item in tags_a:
		if 'name' in item.attrs:
			total += 1
	return total > 1

''' Metodo principal para cada parrafo (p) a procesar '''
def __procesarParrafo(soup):
	global ley_id, last_titulo_id, last_capitulo_id, last_seccion_id, last_subseccion_id, last_segmento_id, last_articulo_id, start_articles, end_of_code, last_titulo, last_capitulo, last_seccion, last_subseccion, last_articulo, articulo_completo, idnetificador_articulo, id_parent_articulo
	if (__isTitulo(soup)):
		if (__isTituloCompuesto(soup)):
			resp = __separarTituloCompuesto(soup) # resp es una lista de partes, cada parte es un tag
			for p in resp:
				__procesarParrafo(p)
		else :
			if articulo_completo != '':
				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent_articulo, idnetificador_articulo)
				idnetificador_articulo = ''
				articulo_completo = ''
			numeracion = hard_code_util.getNumeroTitular(soup.text)
			if hard_code_util.isTitulo(soup.text):
				last_titulo = last_capitulo = last_seccion = last_subseccion = ''
				last_titulo = numeracion
				last_segmento_id = last_titulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_TITULO, ley_id, ley_id, 'titulo' + last_titulo)
			elif hard_code_util.isCapitulo(soup.text):
				last_seccion = last_subseccion = ''
				last_capitulo = numeracion
				last_segmento_id = last_capitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_CAPITULO, ley_id, last_titulo_id, 'titulo' + last_titulo + "_capitulo" + last_capitulo)
			elif hard_code_util.isSeccion(soup.text):
				last_subseccion = ''
				last_seccion = numeracion
				cad = 'titulo' + last_titulo
				id_parent = last_titulo_id
				if last_capitulo != '':
					cad += "_capitulo" + last_capitulo
					id_parent = last_capitulo_id
				cad += '_seccion' + last_seccion
				last_segmento_id = last_seccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SECCION, ley_id, id_parent, cad)
			elif hard_code_util.isSubSeccion(soup.text):
				last_subseccion = numeracion
				cad = 'titulo' + last_titulo
				id_parent = last_titulo_id
				if last_capitulo != '':
					cad += "_capitulo" + last_capitulo
					id_parent = last_capitulo_id
				if last_seccion != '':
					cad += '_seccion' + last_seccion
					id_parent = last_seccion_id
				cad += '_subseccion' + last_subseccion
				last_subseccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBSECCION, ley_id, id_parent, cad)
				last_segmento_id = last_subseccion_id
	else:
		if hard_code_util.isArticulo(soup.text):
			cad = 'titulo' + last_titulo
			id_parent = last_titulo_id
			if last_capitulo != '':
				cad += "_capitulo" + last_capitulo
				id_parent = last_capitulo_id
			if last_seccion != '':
				cad += '_seccion' + last_seccion
				id_parent = last_seccion_id
			if last_subseccion != '':
				cad += '_subseccion' + last_subseccion
				id_parent = last_subseccion_id
			cad += '_articulo' + hard_code_util.getNumeroArticulo(soup.text)
			if soup.find('strike') is not None:
				 cad += '-'
			if articulo_completo != '':
				dao.segmentoDAO.insert(articulo_completo, dao.segmentoDAO.TIPO_ARTICULO, ley_id, id_parent, idnetificador_articulo)
				id_parent_articulo = id_parent
			idnetificador_articulo = cad
			articulo_completo = str(soup)
			start_articles = True
		elif start_articles:
			if hard_code_util.startEndConstitucion(soup.text) or len(end_of_code) > 0:
				end_of_code += str(soup)
			else:
				if not __isTitulo(soup):
					articulo_completo += str(soup)

def readPreambulo(soup):
	global ley_id
	preambulo_head = soup.find('font', {'color': '#800000'})
	preambulo_body = preambulo_head.find_next().find('font', {'size':'2'})
	preambulo = str(preambulo_head) + str(preambulo_body)
	id_header = dao.segmentoDAO.insert(preambulo, dao.segmentoDAO.TIPO_HEADER, ley_id, ley_id)	
	logger.info('Preambulo registrado correctamente, ID = ' + str(id_header))
	return preambulo_body.find_next('p')

def procesarLegislacion(soup):
	try:
		global ley_id, end_of_code
		id_ley = dao.leyDAO.selectIDSegmento(hard_code_util.ID_LEGISLACION_CONSTITUCION)
		dao.segmentoDAO.deleteSegmentos(id_ley)
		dao.leyDAO.deleteLey(hard_code_util.ID_LEGISLACION_CONSTITUCION)
		ley_id = dao.segmentoDAO.insert('<p align="center"><a href="https://legislacao.planalto.gov.br/legisla/legislacao.nsf/viwTodos/509f2321d97cd2d203256b280052245a?OpenDocument&amp;Highlight=1,constitui%C3%A7%C3%A3o&amp;AutoFramed"><font face="Arial" color="#0000FF" size="2"><b>CONSTITUIÇÃO DA REPÚBLICA FEDERATIVA DO BRASIL DE 1988</b></font></a></p>', dao.segmentoDAO.TIPO_LEY, None)
		logger.info('Segmento - Ley registrada correctamente, ID = ' + str(ley_id))
		dao.leyDAO.insert('CONSTITUIÇÃO DA REPÚBLICA FEDERATIVA DO BRASIL DE 1988', '', ley_id, datetime.now(), hard_code_util.ID_LEGISLACION_CONSTITUCION)
		logger.info('Ley registrada correctamente')
		soup_inicial = readPreambulo(soup)
		#titulo = soup.find('p', {'align': 'center'})
		print soup_inicial,'\n'
		next = soup_inicial
		while next is not None:
			__procesarParrafo(next)
			next = next.find_next('p')
		id_footer = dao.segmentoDAO.insert(end_of_code, dao.segmentoDAO.TIPO_FOOTER, ley_id, ley_id)
		logger.info('Se registro el footer, ID = ' + str(id_footer))
	except Exception, e:
		logger.error('Error general : ' + str(e))
		raise