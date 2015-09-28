import MySQLdb
import sys
from database import Database
sys.path.append("..")
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
		return resp.lastrowid
	except Exception, e:
		raise
		return None

resp = insert('HOLA MUNDO', TIPO_LEY)
print resp