import connection as connector
import transferObject.Zakazka as Z
import transferObject.Vozidlo as V
import transferObject.Polozka as P


def get(number):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM zakazka LIMIT " + number)
    e = c.fetchall()

    zakazky = []
    for item in e:
        z = Z.Zakazka()
        z.ID = item[0]
        z.datum = item[1]
        zakazky.append(z)

        # vozidlo
        z.vozidlo = getVozidloByCisloZakazky(z.ID)

        # polozky
        z.polozky = getPolozky(z.ID)

    return zakazky


def getVozidloByCisloZakazky(cisloZakazky):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM vozidlo where cisloZakazky=" + cisloZakazky)
    e = c.fetchall()
    # print(e)

    vDB = e[0]
    v = V.Vozidlo()

    v.ID = vDB[0]
    v.cisloZakazky = vDB[1]
    v.SPZ.set(vDB[2])
    v.VIN.set(vDB[3])
    v.znacka.set(vDB[4])
    v.typ.set(vDB[5])
    v.motor.set(vDB[6])
    v.rokVyroby.set(vDB[7])
    v.tachometr.set(vDB[8])
    return v


def getPolozky(cisloZakazky):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM polozka where cisloZakazky=" + cisloZakazky)
    items = c.fetchall()
    polozky = []
    for item in items:
        polozka = P.Polozka()
        polozka.ID = item[0]
        polozka.cislo.set(item[1])
        polozka.cisloZakazky = item[2]
        polozka.oznaceni.set(item[3])
        polozka.mnozstvi.set(item[4])
        polozka.cenaZaJednotku.set(item[5])
        polozka.cenaCelkem.set(item[6])

        polozky.append(polozka)

    return polozky


def count():
    conn = connector.Connection()
    c = conn.execute("SELECT count(*) FROM zakazka")
    e = c.fetchall()
    # print(e)
    return e


def save(z):
    conn = connector.Connection()
    conn.execute("INSERT OR REPLACE INTO zakazka VALUES ('{}', '{}')".format(z.ID, z.datum))
    conn.commit()


def saveVozidlo(v):
    conn = connector.Connection()
    if v.ID is None:
        sql = "INSERT INTO vozidlo (cisloZakazky, SPZ, VIN, znacka, typ, motor, rokVyroby, tachometr) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            v.cisloZakazky,
            v.SPZ.get(),
            v.VIN.get(),
            v.znacka.get(),
            v.typ.get(),
            v.motor.get(),
            v.rokVyroby.get(),
            v.tachometr.get())
    else:
        sql = "INSERT OR REPLACE INTO vozidlo VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            v.ID,
            v.cisloZakazky,
            v.SPZ.get(),
            v.VIN.get(),
            v.znacka.get(),
            v.typ.get(),
            v.motor.get(),
            v.rokVyroby.get(),
            v.tachometr.get())
    conn.execute(sql)
    conn.commit()


def savePolozku(p):
    conn = connector.Connection()
    if p.ID is None:
        sql = "INSERT INTO polozka (cislo,cisloZakazky,oznaceni,mnozstvi,cenaZaJednotku,cenaCelkem) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            p.cislo.get(),
            p.cisloZakazky,
            p.oznaceni.get(),
            p.mnozstvi.get(),
            p.cenaZaJednotku.get(),
            p.cenaCelkem.get())
    else:
        sql = "INSERT OR REPLACE INTO polozka VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            p.ID,
            p.cislo.get(),
            p.cisloZakazky,
            p.oznaceni.get(),
            p.mnozstvi.get(),
            p.cenaZaJednotku.get(),
            p.cenaCelkem.get())
    conn.execute(sql)
    conn.commit()
