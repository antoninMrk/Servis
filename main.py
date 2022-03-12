import database as db
import transferObject.Zakazka as Z
import transferObject.Polozka as polozka
import transferObject.Vozidlo as vozidlo
from tkinter import *
from tkinter import messagebox
from datetime import date
import os
import xlsxwriter
from tkinter import ttk


class Boolean(object):
    def __init__(self, val):
        self.val = val


def refresh(opened):
    opened.val = True

    canvas.destroy()
    canvas.__init__()
    canvas.grid()

    searchFrame.destroy()
    searchFrame.__init__()
    searchFrame.grid()

    mainScreenFrame.destroy()
    mainScreenFrame.__init__()
    mainScreenFrame.grid()

    searchScreen()
    zk = db.get()
    mainScreen(zk)


def tisk(zakazka):
    fileName = "zakazky/workbook" + str(zakazka.ID) + ".xlsx"
    wb = xlsxwriter.Workbook(fileName)
    ws = wb.add_worksheet("worksheet1")
    center_format = wb.add_format()
    center_format.set_align('center')

    border_up_format = wb.add_format()
    border_up_format.set_top()
    # A-J
    # 1-48 včetně
    # hlavička
    ws.merge_range("E1:F1","Michal Frohlich", center_format)
    # ws.write("F1", "Michal Frohlich", center_format)
    ws.merge_range("D2:G2", "Adresa: 691 62, Uherčice 159", center_format)
    ws.merge_range("E3:F3", "TEL: 723 891 750", center_format)
    ws.merge_range("E4:F4", "IČO: 1002249473", center_format)

    ws.merge_range("A5:J5", "", border_up_format)

    left_format = wb.add_format()
    left_format.set_align('left')
    ws.set_column('A:XFD', None, left_format)

    ws.write("A6", "Zakázka: " + str(zakazka.ID))
    datumSplit = zakazka.datum.split('-')
    datum = datumSplit[2] + '/' + datumSplit[1] + '/' + datumSplit[0]
    ws.write("D6", "Datum: " + datum)
    ws.write("A7", "Jméno: " + zakazka.jmeno.get())
    ws.write("D7", "Telefon: " + zakazka.telefon.get())

    ws.merge_range("A8:J8", "", border_up_format)

    auto = zakazka.vozidlo
    ws.write("A9", "Vozidlo")
    ws.write("A10", "SPZ: " + auto.SPZ.get())
    ws.write("C10", "VIN: " + auto.VIN.get())
    ws.write("F10", "Značka: " + auto.znacka.get())
    ws.write("I10", "Model: " + auto.typ.get())
    ws.write("A11", "Motor: " + auto.motor.get())
    ws.write("C11", "r.v.: " + auto.rokVyroby.get())
    ws.write("F11", "Tachometr: " + auto.tachometr.get())

    ws.merge_range("A12:J12", "", border_up_format)

    # material
    ws.write("A13", "Material")
    ws.write("A14", "Položka")
    ws.write("F14", "Množství")
    ws.write("G14", "Cena za jednotku")
    ws.write("I14", "Cena celkem")

    polozky = zakazka.polozky
    index = 14
    for pol in polozky:
        index += 1
        ws.write("A" + str(index), pol.oznaceni.get())
        ws.write("F" + str(index), pol.mnozstvi.get())
        ws.write("G" + str(index), pol.cenaZaJednotku.get())
        ws.write("I" + str(index), pol.cenaCelkem.get())

    index += 1
    ws.write("G" + str(index), "Celkem za materiál: ")
    ws.write("I" + str(index), zakazka.celkemZaMaterial.get())

    index += 1
    ws.merge_range("A"+str(index)+":J"+str(index), "", border_up_format)

    # práce
    index += 1
    ws.write("A" + str(index), "Práce")
    index += 1
    ws.write("A" + str(index), "Položka")
    ws.write("F" + str(index), "Počet Nh")
    ws.write("G" + str(index), "Cena za Nh")
    ws.write("I" + str(index), "Cena celkem")

    prace = zakazka.prace
    for p in prace:
        index += 1
        ws.write("A" + str(index), p.oznaceni.get())
        ws.write("F" + str(index), p.mnozstvi.get())
        ws.write("G" + str(index), p.cenaZaJednotku.get())
        ws.write("I" + str(index), p.cenaCelkem.get())

    index += 1
    ws.write("G" + str(index), "Celkem za práci: ")
    ws.write("I" + str(index), zakazka.celkemZaPraci.get())

    index += 1
    ws.merge_range("A"+str(index)+":J"+str(index), "", border_up_format)

    index += 1
    ws.write("G" + str(index), "Celkem: ")
    ws.write("I" + str(index), zakazka.celkemZaZakazku.get())

    wb.close()
    cwd = os.getcwd()
    os.startfile(cwd + "/" + fileName, "print")


def search(combobox, searchableEntry):
    searchBy = combobox.get()
    hledanyVyraz = searchableEntry.get()

    if searchBy == "Jméno":
        zak = db.getByClient(hledanyVyraz)
        refreshMainScreen(zak)
    elif searchBy == "VIN":
        zak = db.getByVIN(hledanyVyraz)
        refreshMainScreen(zak)
    elif searchBy == "SPZ":
        zak = db.getBySPZ(hledanyVyraz)
        refreshMainScreen(zak)
    else:
        refreshMainScreen(zakazkyZDB)


def refreshMainScreen(zak):
    # refresh
    mainScreenFrame.destroy()
    mainScreenFrame.__init__()
    mainScreenFrame.grid()

    mainScreen(zak)


def searchScreen():
    Label(searchFrame, text="Hledání").grid(columnspan=10)

    n = StringVar()
    clientCombo = ttk.Combobox(searchFrame, textvariable=n, justify='center', state="readonly")
    clientCombo['values'] = ["", "Jméno", "VIN", "SPZ"]
    clientCombo.grid(row=2, column=0)

    m = StringVar()
    Entry(searchFrame, textvariable=m, justify='center').grid(row=3, column=0)
    Button(searchFrame, command=lambda: search(clientCombo, m), text="Hledat").grid(
        row=4, column=0)


def mainScreen(zakazky):
    opened = Boolean(True)
    edited = Boolean(False)

    Label(mainScreenFrame, text="Zakázky").grid()

    canvasZ = Frame(mainScreenFrame)
    canvasZ.grid()
    Label(canvasZ, text="Číslo zakázky").grid(row=0, column=0)
    Label(canvasZ, text="Klient").grid(row=0, column=1)
    Label(canvasZ, text="SPZ").grid(row=0, column=2)
    Label(canvasZ, text="VIN").grid(row=0, column=3)
    Label(canvasZ, text="Značka").grid(row=0, column=4)
    Label(canvasZ, text="Typ").grid(row=0, column=5)
    Label(canvasZ, text="Datum").grid(row=0, column=6)

    clients = []
    cisloRadku = 0
    for zakazka in zakazky:
        cisloZakazky = zakazka.ID
        cisloRadku += 1

        v = zakazka.vozidlo

        Label(canvasZ, text=cisloZakazky).grid(row=cisloRadku, column=0)
        Label(canvasZ, text=zakazka.jmeno.get()).grid(row=cisloRadku, column=1)
        clients.append(zakazka.jmeno.get())
        # vozidlo
        Label(canvasZ, text=v.SPZ.get()).grid(row=cisloRadku, column=2)
        Label(canvasZ, text=v.VIN.get()).grid(row=cisloRadku, column=3)
        Label(canvasZ, text=v.znacka.get()).grid(row=cisloRadku, column=4)
        Label(canvasZ, text=v.typ.get()).grid(row=cisloRadku, column=5)
        datumSplit = zakazka.datum.split('-')
        datum = datumSplit[2] + '/' + datumSplit[1] + '/' + datumSplit[0]
        Label(canvasZ, text=datum).grid(row=cisloRadku, column=6)

        Button(canvasZ, command=lambda za=zakazka: novaZakazkaScreen(za, opened, edited), text="Upravit").grid(
            row=cisloRadku, column=7)
        Button(canvasZ, command=lambda za=zakazka: tisk(za), text="Vytisknout").grid(row=cisloRadku, column=8)

    Button(mainScreenFrame, command=lambda: novaZakazkaScreenInit(opened, edited), text="Nová Zakázka").grid(row=50,
                                                                                                             column=0)
    return clients


def getNextNumber():
    return str(int(db.count()[0][0]) + 1)


def novaZakazkaScreenInit(opened, edited):
    cisloZakazky = getNextNumber()

    z = Z.Zakazka()
    z.ID = cisloZakazky
    z.datum = str(date.today())

    v = vozidlo.Vozidlo()
    v.cisloZakazky = cisloZakazky

    z.polozky = []
    z.vozidlo = v

    novaZakazkaScreen(z, opened, edited)


def novaZakazkaScreen(z, opened, edited):
    def findAndSetVehicle(event):
        zakazkyBySPZ = db.getBySPZ(z.vozidlo.SPZ.get())
        if zakazkyBySPZ and z.jmeno.get() == "":
            prvniZakazka = zakazkyBySPZ[0]
            z.jmeno.set(prvniZakazka.jmeno.get())
            z.telefon.set(prvniZakazka.telefon.get())
            z.vozidlo.SPZ.set(prvniZakazka.vozidlo.SPZ.get())
            z.vozidlo.VIN.set(prvniZakazka.vozidlo.VIN.get())
            z.vozidlo.znacka.set(prvniZakazka.vozidlo.znacka.get())
            z.vozidlo.typ.set(prvniZakazka.vozidlo.typ.get())
            z.vozidlo.motor.set(prvniZakazka.vozidlo.motor.get())
            z.vozidlo.rokVyroby.set(prvniZakazka.vozidlo.rokVyroby.get())
            z.vozidlo.tachometr.set(prvniZakazka.vozidlo.tachometr.get())

    def pridatPolozku(canvasGroup, item):
        p = polozka.Polozka()
        p.cisloZakazky = z.ID

        item.append(p)
        p.cislo.set(len(item))
        showPolozku(p, canvasGroup)

    def showPolozku(p, canvasGroup):
        def calculate(var, index, mode):
            if p.mnozstvi.get() != '' and p.cenaZaJednotku.get() != '':
                p.cenaCelkem.set(float(p.mnozstvi.get().replace(",", ".")) * float(p.cenaZaJednotku.get().replace(",", ".")))
                cenaZaMaterial = 0
                for poloz in z.polozky:
                    if poloz.cenaCelkem.get() != '':
                        cenaZaMaterial += float(poloz.cenaCelkem.get())

                z.celkemZaMaterial.set(str(cenaZaMaterial))

                cenaZaPraci = 0
                for pra in z.prace:
                    if pra.cenaCelkem.get() != '':
                        cenaZaPraci += float(pra.cenaCelkem.get())

                z.celkemZaPraci.set(str(cenaZaPraci))
                z.celkemZaZakazku.set(str(float(cenaZaMaterial) + float(cenaZaPraci)))

        canvasP = Frame(canvasGroup)
        canvasP.grid(columnspan=10, sticky=W)

        Entry(canvasP, textvariable=p.cislo, state='disabled', justify='center', width=8).grid(row=2, column=0)
        Entry(canvasP, textvariable=p.oznaceni, justify='center', width=50).grid(row=2, column=1)
        Entry(canvasP, textvariable=p.mnozstvi, justify='center').grid(row=2, column=2)
        Entry(canvasP, textvariable=p.cenaZaJednotku, justify='center').grid(row=2, column=3)
        Entry(canvasP, textvariable=p.cenaCelkem, state='disabled', justify='center').grid(row=2, column=4)
        p.mnozstvi.trace("w", calculate)
        p.cenaZaJednotku.trace("w", calculate)

    def saveNovaZakazka():
        db.save(z)
        db.saveVozidlo(v)

        for item in polozky:
            db.savePolozku(item, "material")

        for item in prace:
            db.savePolozku(item, "prace")

        novaZakazkaWindow.destroy()
        refresh(opened)

    def zavrit():
        destroy = True
        if edited.val:
            if messagebox.askokcancel("Zavřít", "Opravdu chceš zavřít zakázku?\nZměny nebudou uloženy!",
                                      parent=novaZakazkaWindow):
                destroy = True
            else:
                destroy = False
        if destroy:
            novaZakazkaWindow.destroy()
            refresh(opened)

    def updated(self):
        edited.val = True

    if opened.val:
        opened.val = False
        v = z.vozidlo
        polozky = z.polozky
        prace = z.prace
        novaZakazkaWindow = Toplevel(root)
        novaZakazkaWindow.title("Nová Zakázka")
        novaZakazkaWindow.protocol("WM_DELETE_WINDOW", zavrit)
        novaZakazkaWindow.bind("<Key>", updated)

        zakazkaC = Frame(novaZakazkaWindow)
        zakazkaC.grid(sticky=W, columnspan=10)

        Label(zakazkaC, text="Zakázka").grid(row=0, column=0)

        Label(zakazkaC, text="Číslo zakázky").grid(row=1, column=0)
        Label(zakazkaC, text=z.ID).grid(row=1, column=1)
        Label(zakazkaC, text="Datum").grid(row=1, column=2)
        datumSplit = z.datum.split('-')
        datum = datumSplit[2] + '/' + datumSplit[1] + '/' + datumSplit[0]
        Label(zakazkaC, text=datum).grid(row=1, column=3)

        zakazkaV = Frame(novaZakazkaWindow)
        zakazkaV.grid(sticky=W, columnspan=10)

        Label(zakazkaV, text="Jméno").grid(row=0, column=0)
        Entry(zakazkaV, textvariable=z.jmeno, justify='center').grid(row=1, column=0)
        Label(zakazkaV, text="Telefon").grid(row=0, column=1)
        Entry(zakazkaV, textvariable=z.telefon, justify='center').grid(row=1, column=1)

        Label(zakazkaV, text="Vozidlo").grid(row=3, column=0)

        Label(zakazkaV, text="SPZ").grid(row=4, column=0)
        spzEntry = Entry(zakazkaV, textvariable=v.SPZ, justify='center')
        spzEntry.grid(row=5, column=0)
        spzEntry.bind("<FocusOut>", findAndSetVehicle)
        # novaZakazkaWindow.bind("<Key>", findAndSetVehicle)

        Label(zakazkaV, text="VIN").grid(row=4, column=1)
        Entry(zakazkaV, textvariable=v.VIN, justify='center').grid(row=5, column=1)

        Label(zakazkaV, text="značka").grid(row=4, column=2)
        Entry(zakazkaV, textvariable=v.znacka, justify='center').grid(row=5, column=2)

        Label(zakazkaV, text="model").grid(row=4, column=3)
        Entry(zakazkaV, textvariable=v.typ, justify='center').grid(row=5, column=3)

        Label(zakazkaV, text="motor").grid(row=4, column=4)
        Entry(zakazkaV, textvariable=v.motor, justify='center').grid(row=5, column=4)

        Label(zakazkaV, text="rok výroby").grid(row=4, column=5)
        Entry(zakazkaV, textvariable=v.rokVyroby, justify='center').grid(row=5, column=5)

        Label(zakazkaV, text="tachometr").grid(row=4, column=6)
        Entry(zakazkaV, textvariable=v.tachometr, justify='center').grid(row=5, column=6)

        zakazkaP = Frame(novaZakazkaWindow)
        zakazkaP.grid(sticky=W, columnspan=10)

        Label(zakazkaP, text="Materiál").grid(row=0, column=0)
        Label(zakazkaP, text="č. položky").grid(row=1, column=0)
        Label(zakazkaP, text="Označení položky", width=42).grid(row=1, column=1)
        Label(zakazkaP, text="Množství", width=15).grid(row=1, column=2)
        Label(zakazkaP, text="Cena za jednotku", width=20).grid(row=1, column=3)
        Label(zakazkaP, text="Cena celkem", width=15).grid(row=1, column=4)

        canvasMaterial = Frame(novaZakazkaWindow)
        canvasMaterial.grid(columnspan=10, sticky="e", padx=140)

        Button(zakazkaP, command=lambda: pridatPolozku(zakazkaP, polozky), text="Přidat Material").grid(row=1, column=50)

        hasPolozku = False
        for pol in z.polozky:
            hasPolozku = True
            showPolozku(pol, zakazkaP)
        if not hasPolozku:
            pridatPolozku(zakazkaP, polozky)

        Label(canvasMaterial, text="Celkem za Material").grid(row=50, column=3)
        Entry(canvasMaterial, textvariable=z.celkemZaMaterial, state='disabled', justify='center').grid(row=50,
                                                                                                        column=4)

        zakazkaPrace = Frame(novaZakazkaWindow)
        zakazkaPrace.grid(sticky=W, columnspan=10)

        Label(zakazkaPrace, text="Práce").grid(row=0, column=0)
        Label(zakazkaPrace, text="č. položky").grid(row=1, column=0)
        Label(zakazkaPrace, text="Označení práce", width=42).grid(row=1, column=1)
        Label(zakazkaPrace, text="Počet Nh", width=15).grid(row=1, column=2)
        Label(zakazkaPrace, text="Cena za Nh", width=20).grid(row=1, column=3)
        Label(zakazkaPrace, text="Cena celkem", width=15).grid(row=1, column=4)

        canvasPrace = Frame(novaZakazkaWindow)
        canvasPrace.grid(columnspan=10, sticky="e", padx=140)

        Button(zakazkaPrace, command=lambda: pridatPolozku(zakazkaPrace, prace), text="   Přidat Práci    ").grid(row=1,
                                                                                                             column=50)
        hasPraci = False

        for prac in prace:
            hasPraci = True
            showPolozku(prac, zakazkaPrace)
        if not hasPraci:
            pridatPolozku(zakazkaPrace, prace)

        Label(canvasPrace, text="Celkem za práci").grid(row=50, column=3)
        Entry(canvasPrace, textvariable=z.celkemZaPraci, state='disabled', justify='center').grid(row=50, column=4)

        Label(canvasPrace, text="Celkem").grid(row=51, column=3)
        Entry(canvasPrace, textvariable=z.celkemZaZakazku, state='disabled', justify='center').grid(row=51, column=4)

        zakazkaK = Frame(novaZakazkaWindow)
        zakazkaK.grid(columnspan=10)

        Button(zakazkaK, command=zavrit, text="Zavřít").grid(row=50, column=0)
        Button(zakazkaK, command=saveNovaZakazka, text="Uložit").grid(row=50, column=50)
        Button(zakazkaK, command=lambda za=z: tisk(za), text="Vytisknout").grid(row=50, column=100)


root = Tk()
root.title("Servis")
root.state("zoomed")
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# root.attributes("-fullscreen", True)

canvas = Frame(root)
canvas.grid()

searchFrame = Frame(canvas)
searchFrame.grid()

mainScreenFrame = Frame(canvas)
mainScreenFrame.grid()

zakazkyZDB = db.get()

searchScreen()
mainScreen(zakazkyZDB)

# b = tk.Button(root, text="X", command=quit, bg="red", fg="white")
# b.grid(row=0, column=10)


root.mainloop()
