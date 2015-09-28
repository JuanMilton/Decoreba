import os.path, sys
import MySQLdb
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import params
from dao.database import Database

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