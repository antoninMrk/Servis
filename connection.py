import sqlite3


class Connection:

    def __init__(self):
        self.connection = sqlite3.connect("servis.db")
        self.cursor = self.connection.cursor()

    def execute(self, sql):
        return self.cursor.execute(sql)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def commit(self):
        self.connection.commit()
