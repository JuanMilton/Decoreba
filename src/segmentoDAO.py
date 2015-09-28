import MySQLdb
from database import Database
import params

TIPO_LEY = 'LEY'
TIPO_TITULO = 'TITULO'
TIPO_CAPITULO = 'CAPITULO'
TIPO_SECCION = 'SECCION'
TIPO_SUBSECCION = 'SUBSECCION'
TIPO_ARTICULO = 'ARTICULO'
TIPO_ITEM_ARTICULO = 'ITEM_ARTICULO'

def insert(contenido, tipo, id_parent=None):
	try:
		db = Database()
		query = """
			INSERT INTO segmento
			(`contenido`, `tipo`, `id_parent`)
			VALUES
			(%s, %s, %s)
			"""
		resp = db.cursor.execute(query, (contenido, tipo, id_parent))
		db.connection.commit()
		if resp == 1:
			return db.cursor.lastrowid
	except Exception, e:
		raise
	return None