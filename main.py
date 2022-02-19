import database as db
import transferObject.Zakazka as zakazka
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
    rows = db.get("10")

    canvasZ = Canvas(canvas)
    canvasZ.grid()
    Label(canvasZ, text="Číslo zakázky").grid(row=0, column=0)
    Label(canvasZ, text="Datum").grid(row=0, column=1)
    Label(canvasZ, text="SPZ").grid(row=0, column=2)
    Label(canvasZ, text="VIN").grid(row=0, column=3)

    for row in rows:
        cisloZakazky = row[0]
        v = db.getVozidloByCisloZakazky(cisloZakazky)
        cisloRadku = int(cisloZakazky)+1
        # zakazka
        Label(canvasZ, text=cisloZakazky).grid(row=cisloRadku, column=0)
        Label(canvasZ, text=row[1]).grid(row=cisloRadku, column=1)

        # vozidlo
        Label(canvasZ, text=v[0][1]).grid(row=cisloRadku, column=2)
        Label(canvasZ, text=v[0][2]).grid(row=cisloRadku, column=3)

    Button(canvas, command=novaZakazkaScreen, text="Nova Zakazka").grid(row=50, column=0)


def getNextNumber():
    return str(int(db.count()[0][0]) + 1)


def novaZakazkaScreen():
    def pridatPolozku():
        canvasP = Canvas(zakazkaP)
        canvasP.grid(columnspan=5)

        cisloPolozky = StringVar()
        Entry(canvasP, textvariable=cisloPolozky).grid(row=2, column=0)
        Entry(canvasP, textvariable=cisloPolozky).grid(row=2, column=1)
        Entry(canvasP, textvariable=cisloPolozky).grid(row=2, column=2)
        Entry(canvasP, textvariable=cisloPolozky).grid(row=2, column=3)
        Entry(canvasP, textvariable=cisloPolozky).grid(row=2, column=4)

    def saveNovaZakazka():
        z = zakazka.Zakazka()
        z.number = cisloZakazky
        z.datum = datum
        db.save(z)

        v = vozidlo.Vozidlo()
        v.cisloZakazky = cisloZakazky
        v.SPZ = SPZ.get()
        v.VIN = VIN.get()
        v.znacka = znacka.get()
        v.typ = typ.get()
        v.motor = motor.get()
        v.rokVyroby = rokVyroby.get()
        v.tachometr = tacho.get()
        db.saveVozidlo(v)

        novaZakazkaWindow.destroy()
        refresh()

    def zavrit():
        # todo dialogove okno (ano/ne - data budou deleted)
        novaZakazkaWindow.destroy()

    novaZakazkaWindow = Toplevel(root)
    novaZakazkaWindow.title("Nová Zakázka")

    zakazkaC = Canvas(novaZakazkaWindow)
    zakazkaC.grid()

    Label(zakazkaC, text="Zakázka").grid(row=0, column=0)

    Label(zakazkaC, text="Číslo zakázky").grid(row=1, column=0)
    cisloZakazky = getNextNumber()
    Label(zakazkaC, text=cisloZakazky).grid(row=1, column=1)
    Label(zakazkaC, text="Datum").grid(row=1, column=2)
    datum = str(date.today())
    Label(zakazkaC, text=datum).grid(row=1, column=3)

    zakazkaV = Canvas(novaZakazkaWindow)
    zakazkaV.grid()
    SPZ = StringVar()
    VIN = StringVar()
    znacka = StringVar()
    typ = StringVar()
    motor = StringVar()
    rokVyroby = StringVar()
    tacho = StringVar()

    Label(zakazkaV, text="Vozidlo").grid(row=3, column=0)

    Label(zakazkaV, text="SPZ").grid(row=4, column=0)
    Entry(zakazkaV, textvariable=SPZ).grid(row=5, column=0)

    Label(zakazkaV, text="VIN").grid(row=4, column=1)
    Entry(zakazkaV, textvariable=VIN).grid(row=5, column=1)

    Label(zakazkaV, text="značka").grid(row=4, column=2)
    Entry(zakazkaV, textvariable=znacka).grid(row=5, column=2)

    Label(zakazkaV, text="typ").grid(row=4, column=3)
    Entry(zakazkaV, textvariable=typ).grid(row=5, column=3)

    Label(zakazkaV, text="motor").grid(row=4, column=4)
    Entry(zakazkaV, textvariable=motor).grid(row=5, column=4)

    Label(zakazkaV, text="rok výroby").grid(row=4, column=5)
    Entry(zakazkaV, textvariable=rokVyroby).grid(row=5, column=5)

    Label(zakazkaV, text="tachometr").grid(row=4, column=6)
    Entry(zakazkaV, textvariable=tacho).grid(row=5, column=6)

    zakazkaP = Canvas(novaZakazkaWindow)
    zakazkaP.grid()

    Label(zakazkaP, text="Polozky").grid(row=0, column=0)
    Label(zakazkaP, text="č. položky").grid(row=1, column=0)
    Label(zakazkaP, text="označení položky").grid(row=1, column=1)
    Label(zakazkaP, text="množství").grid(row=1, column=2)
    Label(zakazkaP, text="cena za jednotku").grid(row=1, column=3)
    Label(zakazkaP, text="cena celkem").grid(row=1, column=4)
    Button(zakazkaP, command=pridatPolozku, text="Přidat Položku").grid(row=1, column=50)
    pridatPolozku()

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
