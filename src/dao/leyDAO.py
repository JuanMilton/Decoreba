import os.path, sys
import MySQLdb
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import params
from dao.database import Database

def insert(titulo, descripcion, id_segmento, fecha, version, id_legislacion):
	try:
		db = Database()
		date = datetime.now()
		query = """
			INSERT INTO ley
			(`titulo`, `descripcion`, `id_segmento`, `fecha`, `version`, `id_legislacion`)
			VALUES
			(%s, %s, %s, %s, %s, %s)
			"""
		resp = db.cursor.execute(query, (titulo.decode('utf-8'), descripcion, id_segmento, fecha, version, id_legislacion))
		db.connection.commit()
	except Exception, e:
		raise

def getVersion(legislacion):
	try:
		db = Database()
		query = """
			SELECT version FROM ley ORDER BY version DESC LIMIT 1
			"""
		db.cursor.execute(query)
		resp = db.cursor.fetchone()
		db.connection.commit()
		if resp is None:
			return 0
		for item in resp:
			return item
		return 0
	except Exception, e:
		raise