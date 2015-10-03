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

def insert(contenido, tipo, id_ley, id_parent=None, identificador=None):
	try:
		db = Database()
		query = """
			INSERT INTO segmento
			(`contenido`, `tipo`, `id_parent`, `id_ley`, `identificador`)
			VALUES
			(%s, %s, %s, %s, %s)
			"""
		resp = db.cursor.execute(query, (contenido.decode('utf-8'), tipo, id_parent, id_ley, identificador))
		db.connection.commit()
		if resp == 1:
			return db.cursor.lastrowid
	except Exception, e:
		raise
	return None

def deleteSegmentos(id_ley):
	try:
		db = Database()
		query = """
			DELETE FROM segmento
			WHERE id = %s OR id_ley = %s
			"""
		db.cursor.execute(query, (id_ley, id_ley))
		db.connection.commit()
	except Exception, e:
		raise