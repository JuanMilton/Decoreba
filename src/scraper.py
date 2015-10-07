import requests
from bs4 import BeautifulSoup
import logger
import params
import scrapers.constitucion
import scrapers.codigo_civil
import scrapers.codigo_procesal_civil_1

logger.info('Iniciando Scraping - planalto')
response = requests.get(params.url)
plain_text = response.text
soup = BeautifulSoup(plain_text)
#scrapers.codigo_civil.procesarLegislacion(soup)
#scrapers.constitucion.procesarLegislacion(soup)
scrapers.codigo_procesal_civil_1.procesarLegislacion(soup)
logger.info('Finalizado ')