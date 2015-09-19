import MySQLdb
import params
from database import Database
from datetime import datetime

date = datetime.now()

db = Database()
query = """
        INSERT INTO scraper_log
        (`fecha`, `tipo_log`, `detalle`)
        VALUES
        (%s, %s, %s)
        """
resp = db.cursor.execute(query, (date, 'INFO', 'Hola mundo'))
db.connection.commit()

print resp
print 'OK'