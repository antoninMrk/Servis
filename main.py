import time
import tkinter.messagebox

import database as db
import transferObject.Zakazka as Z
import transferObject.Polozka as polozka
import transferObject.Vozidlo as vozidlo
from tkinter import *
from datetime import date


def refresh():
    canvas.destroy()
    canvas.__init__()
    canvas.grid()
    mainScreen()


def mainScreen():
    Label(canvas, text="Zakázky").grid()
    zakazky = db.get("10")

    canvasZ = Canvas(canvas)
    canvasZ.grid()
    Label(canvasZ, text="Číslo zakázky").grid(row=0, column=0)
    Label(canvasZ, text="Klient").grid(row=0, column=1)
    Label(canvasZ, text="SPZ").grid(row=0, column=2)
    Label(canvasZ, text="VIN").grid(row=0, column=3)
    Label(canvasZ, text="Značka").grid(row=0, column=4)
    Label(canvasZ, text="Typ").grid(row=0, column=5)
    Label(canvasZ, text="Datum").grid(row=0, column=6)

    for zakazka in zakazky:
        cisloZakazky = zakazka.ID
        cisloRadku = int(cisloZakazky)+1

        v = zakazka.vozidlo

        Label(canvasZ, text=cisloZakazky).grid(row=cisloRadku, column=0)
        Label(canvasZ, text=zakazka.jmeno.get()).grid(row=cisloRadku, column=1)

        # vozidlo
        Label(canvasZ, text=v.SPZ.get()).grid(row=cisloRadku, column=2)
        Label(canvasZ, text=v.VIN.get()).grid(row=cisloRadku, column=3)
        Label(canvasZ, text=v.znacka.get()).grid(row=cisloRadku, column=4)
        Label(canvasZ, text=v.typ.get()).grid(row=cisloRadku, column=5)

        Label(canvasZ, text=zakazka.datum).grid(row=cisloRadku, column=6)

        Button(canvasZ, command=lambda za=zakazka: novaZakazkaScreen(za), text="Upravit").grid(row=cisloRadku, column=7)

    Button(canvas, command=novaZakazkaScreenInit, text="Nova Zakázka").grid(row=50, column=0)


def getNextNumber():
    return str(int(db.count()[0][0]) + 1)


def novaZakazkaScreenInit():
    cisloZakazky = getNextNumber()

    z = Z.Zakazka()
    z.ID = cisloZakazky
    z.datum = str(date.today())

    v = vozidlo.Vozidlo()
    v.cisloZakazky = cisloZakazky

    z.polozky = []
    z.vozidlo = v

    novaZakazkaScreen(z)


def novaZakazkaScreen(z):
    def pridatPolozku():
        p = polozka.Polozka()
        p.cisloZakazky = z.ID

        polozky.append(p)
        p.cislo.set(len(polozky))
        showPolozku(p)

    def showPolozku(p):
        def calculate(var, index, mode):
            if p.mnozstvi.get() != '' and p.cenaZaJednotku.get() != '':
                p.cenaCelkem.set(int(p.mnozstvi.get())*int(p.cenaZaJednotku.get()))

        canvasP = Canvas(zakazkaP)
        canvasP.grid(columnspan=5)

        Entry(canvasP, textvariable=p.cislo, state='disabled').grid(row=2, column=0)
        Entry(canvasP, textvariable=p.oznaceni).grid(row=2, column=1)
        Entry(canvasP, textvariable=p.mnozstvi).grid(row=2, column=2)
        Entry(canvasP, textvariable=p.cenaZaJednotku).grid(row=2, column=3)
        Entry(canvasP, textvariable=p.cenaCelkem).grid(row=2, column=4)
        p.mnozstvi.trace("w", calculate)
        p.cenaZaJednotku.trace("w", calculate)

    def saveNovaZakazka():
        db.save(z)
        db.saveVozidlo(v)

        for item in polozky:
            db.savePolozku(item)

        novaZakazkaWindow.destroy()
        refresh()

    def zavrit():
        # todo dialogove okno (ano/ne - data budou deleted)
        novaZakazkaWindow.destroy()
        refresh()

    v = z.vozidlo
    polozky = z.polozky
    novaZakazkaWindow = Toplevel(root)
    novaZakazkaWindow.title("Nová Zakázka")

    zakazkaC = Canvas(novaZakazkaWindow)
    zakazkaC.grid()

    Label(zakazkaC, text="Zakázka").grid(row=0, column=0)

    Label(zakazkaC, text="Číslo zakázky").grid(row=1, column=0)
    Label(zakazkaC, text=z.ID).grid(row=1, column=1)
    Label(zakazkaC, text="Datum").grid(row=1, column=2)
    Label(zakazkaC, text=z.datum).grid(row=1, column=3)
    Label(zakazkaC, text="Jméno").grid(row=1, column=4)
    Entry(zakazkaC, textvariable=z.jmeno).grid(row=1, column=5)

    zakazkaV = Canvas(novaZakazkaWindow)
    zakazkaV.grid()

    Label(zakazkaV, text="Vozidlo").grid(row=3, column=0)

    Label(zakazkaV, text="SPZ").grid(row=4, column=0)
    Entry(zakazkaV, textvariable=v.SPZ).grid(row=5, column=0)

    Label(zakazkaV, text="VIN").grid(row=4, column=1)
    Entry(zakazkaV, textvariable=v.VIN).grid(row=5, column=1)

    Label(zakazkaV, text="značka").grid(row=4, column=2)
    Entry(zakazkaV, textvariable=v.znacka).grid(row=5, column=2)

    Label(zakazkaV, text="typ").grid(row=4, column=3)
    Entry(zakazkaV, textvariable=v.typ).grid(row=5, column=3)

    Label(zakazkaV, text="motor").grid(row=4, column=4)
    Entry(zakazkaV, textvariable=v.motor).grid(row=5, column=4)

    Label(zakazkaV, text="rok výroby").grid(row=4, column=5)
    Entry(zakazkaV, textvariable=v.rokVyroby).grid(row=5, column=5)

    Label(zakazkaV, text="tachometr").grid(row=4, column=6)
    Entry(zakazkaV, textvariable=v.tachometr).grid(row=5, column=6)

    zakazkaP = Canvas(novaZakazkaWindow)
    zakazkaP.grid()

    Label(zakazkaP, text="Polozky").grid(row=0, column=0)
    Label(zakazkaP, text="č. položky").grid(row=1, column=0)
    Label(zakazkaP, text="označení položky").grid(row=1, column=1)
    Label(zakazkaP, text="množství").grid(row=1, column=2)
    Label(zakazkaP, text="cena za jednotku").grid(row=1, column=3)
    Label(zakazkaP, text="cena celkem").grid(row=1, column=4)
    Button(zakazkaP, command=pridatPolozku, text="Přidat Položku").grid(row=1, column=50)
    for pol in z.polozky:
        showPolozku(pol)

    zakazkaK = Canvas(novaZakazkaWindow)
    zakazkaK.grid()
    Button(zakazkaK, command=saveNovaZakazka, text="Uložit").grid(row=50, column=50)
    Button(zakazkaK, command=zavrit, text="Zavřít").grid(row=50, column=49)


root = Tk()
root.title("Servis")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# root.attributes("-fullscreen", True)

canvas = Canvas(root)
canvas.grid()

mainScreen()

# b = tk.Button(root, text="X", command=quit, bg="red", fg="white")
# b.grid(row=0, column=10)


root.mainloop()
