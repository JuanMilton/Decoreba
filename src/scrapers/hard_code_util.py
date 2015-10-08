# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup

ID_LEGISLACION_CONSTITUCION = 1
ID_LEGISLACION_CODIGO_CIVIL = 2
ID_LEGISLACION_CODIGO_PROCESAL_CIVIL_1 = 3
ID_LEGISLACION_CODIGO_PROCESAL_CIVIL_2 = 4

def isParte(text):
	return text is not None and ('P A R T E' in text.encode('utf-8') or ('PARTE' in text.encode('utf-8') and 'PARTES' not in text.encode('utf-8')))

def isLibro(text):
	return text is not None and 'LIVRO' in text.encode('utf-8')

def isSubTitulo(text):
	return text is not None and 'SUBTÍTULO' in text.encode('utf-8')

def isTitulo(text):
	return text is not None and 'TÍTULO' in text.encode('utf-8')

def isCapitulo(text):
	return text is not None and 'CAPÍTULO' in text.encode('utf-8')

def isSeccion(text):
	return text is not None and 'Seção' in text.encode('utf-8')

def isSubSeccion(text):
	return text is not None and 'Subseção' in text.encode('utf-8')

def isArticulo(text):
	return text is not None and text.strip().startswith('Art.')

def getNumeroTitular(text):
	if text is None:
		return '0'
	if len(text.split()) > 1:
		return text.split()[1]
	return None

def getNumeroArticulo(text):
	if text is None:
		return '0'
	return text.split()[1][:-1]

def startEndConstitucion(text):
	return text is not None and '5 de outubro de 1988.' in text.encode('utf-8')
