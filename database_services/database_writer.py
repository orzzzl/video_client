import pymysql

class DatabaseWriter:
    @staticmethod
    def make_connection():
        connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='deepmagic',
                                 db='pod_client',
                                 cursorclass=pymysql.cursors.DictCursor)
        return connection

    def execute(self, sql_statement):
        c = self.make_connection()
        try:
            with c.cursor() as cursor:
                cursor.execute(sql_statement)

            c.commit()
        finally:
            c.close()



