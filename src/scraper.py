import requests
from bs4 import BeautifulSoup
import sys
import codecs
import MySQLdb


sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

print 'Iniciando Scraping - planalto\n'
print 'URL : ', url

response = requests.get(url)
response.encoding = 'UTF-8'

# print response.text

print 'Finalizado con exito'