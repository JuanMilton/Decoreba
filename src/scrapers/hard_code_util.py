# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup

def isTitulo(text):
	return text is not None and 'título' in text.lower().encode('utf-8')

def isCapitulo(text):
	return text is not None and 'capítulo' in text.lower().encode('utf-8')

def isSeccion(text):
	return text is not None and 'seção' in text.lower().encode('utf-8')

def isSubSeccion(text):
	return text is not None and 'subseção' in text.lower().encode('utf-8')
