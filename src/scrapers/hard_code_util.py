# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup

ID_LEGISLACION_CONSTITUCION = 1

def isTitulo(text):
	return text is not None and 'título' in text.lower().encode('utf-8')

def isCapitulo(text):
	return text is not None and 'capítulo' in text.lower().encode('utf-8')

def isSeccion(text):
	return text is not None and 'seção' in text.lower().encode('utf-8')

def isSubSeccion(text):
	return text is not None and 'subseção' in text.lower().encode('utf-8')

def isArticulo(text):
	return text is not None and text.strip().startswith('Art.')

def startEnd(text):
	return text is not None and '5 de outubro de 1988.' in text.encode('utf-8')
