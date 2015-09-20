from bs4 import BeautifulSoup

def readPreambulo(soup):
	preambulo_head = soup.find('font', {'color': '#800000'})
	preambulo_body = preambulo_head.find_next().find('font', {'size':'2'})
	print preambulo_head.string
	print preambulo_body.string

def readContent(soup):
	titulos = soup.find('span', {'style': 'text-transform: uppercase'})
	next = titulos.find_next()
	while next is not None:
		if next.name == 'p':

			print next

		next = next.find_next()
		#break

def __isTitulo(soup):
	soup.find_next()