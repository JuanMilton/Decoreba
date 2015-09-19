import requests
from bs4 import BeautifulSoup
import sys
import codecs
import MySQLdb

url = 'http://localhost/legislacion/'


sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

print 'Iniciando Scraping - planalto\n'
print 'URL : ', url

response = requests.get(url)
# print response.content
response.encoding = 'UTF-8'
# text = str(response.content, 'UTF-8', errors='replace')

print response.text