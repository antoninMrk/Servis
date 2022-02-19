import connection as connector
import transferObject.Zakazka as zakazka


def getAll():
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM zakazka")
    e = c.fetchall()
    print(e)
    return e


def get(number):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM zakazka LIMIT " + number)
    e = c.fetchall()
    print(e)
    return e


def getVozidloByCisloZakazky(cisloZakazky):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM vozidlo where cisloZakazky="+cisloZakazky)
    e = c.fetchall()
    print(e)
    return e


def count():
    conn = connector.Connection()
    c = conn.execute("SELECT count(*) FROM zakazka")
    e = c.fetchall()
    # print(e)
    return e


def save(z):
    conn = connector.Connection()
    conn.execute("INSERT INTO zakazka (cislo, datum) VALUES ({}, '{}')".format(z.number, z.datum))
    conn.commit()


def saveVozidlo(v):
    conn = connector.Connection()
    conn.execute("INSERT INTO vozidlo (cisloZakazky, SPZ, VIN, znacka, typ, motor, rokVyroby, tachometr) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(v.cisloZakazky, v.SPZ, v.VIN, v.znacka, v.typ, v.motor, v.rokVyroby, v.tachometr))
    conn.commit()
