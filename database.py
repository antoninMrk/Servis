import connection as connector
import transferObject.Zakazka as Z
import transferObject.Vozidlo as V
import transferObject.Polozka as P


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

    zakazky = []
    for item in e:
        z = Z.Zakazka()
        z.number = item[0]
        z.datum = item[1]
        zakazky.append(z)

        # vozidlo
        vDB = getVozidloByCisloZakazky(z.number)[0]
        v = V.Vozidlo()
        z.vozidlo = v
        v.cisloZakazky = z.number
        v.SPZ = vDB[1]
        v.VIN = vDB[2]
        v.znacka = vDB[3]
        v.typ = vDB[4]
        v.motor = vDB[5]
        v.rokVyroby = vDB[6]
        v.tachometr = vDB[7]

    return zakazky


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
    conn.execute("INSERT INTO vozidlo (cisloZakazky, SPZ, VIN, znacka, typ, motor, rokVyroby, tachometr) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(v.cisloZakazky, v.SPZ.get(), v.VIN.get(), v.znacka.get(), v.typ.get(), v.motor.get(), v.rokVyroby.get(), v.tachometr.get()))
    conn.commit()


def savePolozku(p):
    conn = connector.Connection()
    conn.execute("INSERT INTO polozka VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(p.cisloZakazky, p.cislo, p.oznaceni, p.mnozstvi, p.cenaZaJednotku, p.cenaCelkem))
    conn.commit()
