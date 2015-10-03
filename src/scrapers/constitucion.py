# -*- coding: latin-1 -*-

import os.path, sys
from bs4 import BeautifulSoup
import hard_code_util
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dao.segmentoDAO

ley_id = 0
last_titulo_id = 0
last_capitulo_id = 0
last_seccion_id = 0
last_subseccion_id = 0

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
			tag1 = '<p align=\'center\'><font face=\'Arial\' size=\'2\'><a name=\'tituloii\'></a><span style=\'text-transform: uppercase\'><b>TÍTULO II<br>Dos Direitos e Garantias Fundamentais</b></span></font></p>'
			tag2 = '<p align=\'center\'><font face=\'Arial\' size=\'2\'><br><a name=\'tituloiicapituloi\'></a>CAPÍTULO I<br>DOS DIREITOS E DEVERES INDIVIDUAIS E COLETIVOS</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiii' and tags_name[1] == 'tituloiiicapituloi':
			tag1 = '<p align="center"><font face="Arial" color="#000000" size="3"><a name="tituloiii"></a></font><font face="Arial" color="#000000" size="2"><span style="text-transform: uppercase"><b>TÍTULO III<br>Da Organização do Estado</b></span></font></p>'
			tag2 = '<p align="center"><font face="Arial" color="#000000" size="3"><br></font><font face="Arial" size="2"><a name="tituloiiicapituloi"></a>CAPÍTULO I<br>DA ORGANIZAÇÃO POLÍTICO-ADMINISTRATIVA</font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiiicapitulov' and tags_name[1] == 'tituloiiicapitulovsecaoi':
			tag1 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulov"></a>CAPÍTULO V<br>DO DISTRITO FEDERAL E DOS TERRITÓRIOS</font></p>'
			tag2 = '<p align="CENTER"><font face="Arial" size="2"><a name="tituloiiicapitulovsecaoi"></a><span style="text-transform: uppercase"><b>Seção I<br>DO DISTRITO FEDERAL</b></span></font></p>'
			return [(BeautifulSoup(tag1.decode('utf-8'))).p, (BeautifulSoup(tag2.decode("utf-8"))).p]
		elif tags_name[0] == 'tituloiiicapitulovii' and tags_name[1] == 'tituloiiicapituloviisecaoi':
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
	global ley_id
	global last_titulo_id
	global last_capitulo_id
	global last_seccion_id
	global last_subseccion_id
	if (__isTitulo(soup)):
		if (__isTituloCompuesto(soup)):
			resp = __separarTituloCompuesto(soup) # resp es una lista de partes, cada parte es un tag
			for p in resp:
				__procesarParrafo(p)
		else :
			if hard_code_util.isTitulo(soup.text):
				last_titulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_TITULO, ley_id)
			elif hard_code_util.isCapitulo(soup.text):
				last_capitulo_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_CAPITULO, last_titulo_id)
			elif hard_code_util.isSeccion(soup.text):
				last_seccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SECCION, last_capitulo_id)
			elif hard_code_util.isSubSeccion(soup.text):
				last_subseccion_id = dao.segmentoDAO.insert(str(soup), dao.segmentoDAO.TIPO_SUBSECCION, last_seccion_id)


def readPreambulo(soup):
	preambulo_head = soup.find('font', {'color': '#800000'})
	preambulo_body = preambulo_head.find_next().find('font', {'size':'2'})
	print preambulo_head.string
	print preambulo_body.string

def readContent(soup):
	global ley_id
	ley_id = dao.segmentoDAO.insert('<p align="center"><a href="https://legislacao.planalto.gov.br/legisla/legislacao.nsf/viwTodos/509f2321d97cd2d203256b280052245a?OpenDocument&amp;Highlight=1,constitui%C3%A7%C3%A3o&amp;AutoFramed"><font face="Arial" color="#0000FF" size="2"><b>CONSTITUIÇÃO DA REPÚBLICA FEDERATIVA DO BRASIL DE 1988</b></font></a></p>', dao.segmentoDAO.TIPO_LEY)
	titulo = soup.find('p', {'align': 'center'})
	next = titulo
	while next is not None:
		if next.name == 'p':
			__procesarParrafo(next)
		next = next.find_next()