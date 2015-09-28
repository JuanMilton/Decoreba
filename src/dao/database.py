import MySQLdb
from ... import params

class Database:

    host = params.db_host
    user = params.db_username
    password = params.db_password
    db = params.db_name
    port = params.db_port

    def __init__(self):
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, 
                                db=self.db, port=self.port)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()



    def query(self, query):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()