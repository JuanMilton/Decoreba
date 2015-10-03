import os.path, sys
import MySQLdb
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import params
from dao.database import Database

def insert(titulo, descripcion, id_segmento, fecha, id_legislacion):
	try:
		db = Database()
		date = datetime.now()
		query = """
			INSERT INTO ley
			(`titulo`, `descripcion`, `id_segmento`, `fecha`, `id_legislacion`)
			VALUES
			(%s, %s, %s, %s, %s)
			"""
		resp = db.cursor.execute(query, (titulo.decode('utf-8'), descripcion, id_segmento, fecha, id_legislacion))
		db.connection.commit()
	except Exception, e:
		raise

def selectIDSegmento(id_legislacion):
	try:
		db = Database()
		query = """
			SELECT id_segmento FROM ley
			WHERE id_legislacion = %s
			"""
		db.cursor.execute(query, (id_legislacion,))
		resp = db.cursor.fetchone()
		db.connection.commit()
		if resp is None:
			return 0
		for item in resp:
			return item
		return 0
	except Exception, e:
		raise

def deleteLey(id_legislacion):
	try:
		db = Database()
		query = """
			DELETE FROM ley
			WHERE id_legislacion = %s
			"""
		db.cursor.execute(query, (id_legislacion,))
		db.connection.commit()
	except Exception, e:
		raise