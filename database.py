import connection as connector


def getAll():
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM servis")
    e = c.fetchall()
    print(e)
    return e


def get(number):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM servis LIMIT "+number)
    e = c.fetchall()
    print(e)
    return e


def insert():
    conn = connector.Connection()
    conn.execute("INSERT INTO servis VALUES ('Jozo', '19/2/2022','fiat')")
