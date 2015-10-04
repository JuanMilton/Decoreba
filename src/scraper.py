import requests
from bs4 import BeautifulSoup
import logger
import params
import scrapers.constitucion
import scrapers.codigo_civil

logger.info('Iniciando Scraping - planalto')
response = requests.get(params.url)
plain_text = response.text
soup = BeautifulSoup(plain_text)
scrapers.codigo_civil.procesarLegislacion(soup)
logger.info('Finalizado ')