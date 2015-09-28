import MySQLdb
from ... import params
from database import Database
from datetime import datetime

def insert(titulo, descripcion=None, id_segmento, fecha, version):
	try:
		db = Database()
		date = datetime.now()
		query = """
			INSERT INTO scraper_log
			(`fecha`, `tipo_log`, `detalle`)
			VALUES
			(%s, %s, %s)
			"""
		resp = db.cursor.execute(query, (date, level, detail))
		db.connection.commit()
	except Exception, e:
		raise