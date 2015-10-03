import os.path, sys
import MySQLdb
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from dao.database import Database
import params

TIPO_LEY = 'LEY'
TIPO_TITULO = 'TITULO'
TIPO_CAPITULO = 'CAPITULO'
TIPO_SECCION = 'SECCION'
TIPO_SUBSECCION = 'SUBSECCION'
TIPO_ARTICULO = 'ARTICULO'
TIPO_ITEM_ARTICULO = 'ITEM_ARTICULO'
TIPO_FOOTER = 'FOOTER'
TIPO_HEADER = 'HEADER'

def insert(contenido, tipo, id_parent=None):
	try:
		db = Database()
		query = """
			INSERT INTO segmento
			(`contenido`, `tipo`, `id_parent`)
			VALUES
			(%s, %s, %s)
			"""
		resp = db.cursor.execute(query, (contenido.decode('utf-8'), tipo, id_parent))
		db.connection.commit()
		if resp == 1:
			return db.cursor.lastrowid
	except Exception, e:
		raise
	return None