import connection as connector
import transferObject.Zakazka as Z
import transferObject.Vozidlo as V
import transferObject.Polozka as P


def get():
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM zakazka ORDER BY zakazka.id desc limit 10")
    e = c.fetchall()
    return convertToZakazky(e)


def getByClient(client):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM zakazka where zakazka.jmeno like '%"+client+"%' ORDER BY zakazka.id desc limit 10")
    e = c.fetchall()
    return convertToZakazky(e)


def getByVIN(VIN):
    conn = connector.Connection()
    c = conn.execute("select z.* from zakazka z JOIN vozidlo v on v.cisloZakazky = z.id where v.VIN = '"+VIN+"' ORDER BY z.id desc limit 10")
    e = c.fetchall()
    return convertToZakazky(e)


def getBySPZ(SPZ):
    conn = connector.Connection()
    c = conn.execute("select z.* from zakazka z JOIN vozidlo v on v.cisloZakazky = z.id where v.SPZ = '"+SPZ+"' ORDER BY z.id desc limit 10")
    e = c.fetchall()
    return convertToZakazky(e)


def convertToZakazky(e):
    zakazky = []
    for item in e:
        z = Z.Zakazka()
        z.ID = item[0]
        z.datum = item[1]
        z.jmeno.set(item[2])
        z.telefon.set(item[3])
        z.celkemZaMaterial.set(item[4])
        z.celkemZaPraci.set(item[5])
        z.celkemZaZakazku.set(item[6])
        z.cisloZakazky.set(item[7])
        zakazky.append(z)

        # vozidlo
        z.vozidlo = getVozidloByCisloZakazky(z.ID)

        # polozky
        z.polozky = getPolozky(z.ID, "material")

        # prace
        z.prace = getPolozky(z.ID, "prace")

    return zakazky


def getVozidloByCisloZakazky(cisloZakazky):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM vozidlo where cisloZakazky=" + str(cisloZakazky))
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


def getPolozky(cisloZakazky, typ):
    conn = connector.Connection()
    c = conn.execute("SELECT * FROM polozka where cisloZakazky=" + str(cisloZakazky))
    items = c.fetchall()
    polozky = []
    for item in items:
        if item[7] == typ:
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
    conn.execute("INSERT OR REPLACE INTO zakazka VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(z.ID, z.datum, z.jmeno.get(), z.telefon.get(), z.celkemZaMaterial.get(), z.celkemZaPraci.get(), z.celkemZaZakazku.get(), z.cisloZakazky.get()))
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


def deletePolozkyForZakazka(idZak):
    conn = connector.Connection()

    sql = "DELETE FROM polozka where cisloZakazky='{}'".format(
            idZak)

    conn.execute(sql)
    conn.commit()

def savePolozku(p, typ):
    conn = connector.Connection()
    if p.ID is None:
        sql = "INSERT INTO polozka (cislo,cisloZakazky,oznaceni,mnozstvi,cenaZaJednotku,cenaCelkem, typ) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            p.cislo.get(),
            p.cisloZakazky,
            p.oznaceni.get(),
            p.mnozstvi.get(),
            p.cenaZaJednotku.get(),
            p.cenaCelkem.get(),
            typ)
    else:
        sql = "INSERT OR REPLACE INTO polozka VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            p.ID,
            p.cislo.get(),
            p.cisloZakazky,
            p.oznaceni.get(),
            p.mnozstvi.get(),
            p.cenaZaJednotku.get(),
            p.cenaCelkem.get(),
            typ)
    conn.execute(sql)
    conn.commit()
