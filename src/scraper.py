import requests
from bs4 import BeautifulSoup
import logger
import params
import scrapers.constitucion

print 'Iniciando Scraping - planalto\n'

response = requests.get(params.url)
plain_text = response.text
soup = BeautifulSoup(plain_text)
#print '\n\n'
#scrapers.constitucion.readPreambulo(soup)
#print '\n\n'
constitucion.readContent(soup)
print '\n\nFinalizado con exito'
