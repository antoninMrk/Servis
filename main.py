import database as db
import transferObject.Zakazka as Z
import transferObject.Polozka as polozka
import transferObject.Vozidlo as vozidlo
from tkinter import *
from tkinter import messagebox
from tkinter import font
import tkinter as tk
from datetime import date
import os
import xlsxwriter
from tkinter import ttk
from PIL import ImageFont


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
    if not os.path.exists('zakazky'):
        os.makedirs('zakazky')
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
    ws.merge_range("E1:F1", "AUTOSERVIS", center_format)
    ws.merge_range("E2:F2", "Michal Frohlich", center_format)
    # ws.write("F1", "Michal Frohlich", center_format)
    ws.merge_range("D3:G3", "Adresa: 691 62, Uherčice 159", center_format)
    ws.merge_range("E4:F4", "TEL: 723 891 750", center_format)
    ws.merge_range("E5:F5", "IČO: 74616862", center_format)

    ws.merge_range("A6:J6", "", border_up_format)

    left_format = wb.add_format()
    left_format.set_align('left')
    ws.set_column('A:XFD', None, left_format)

    ws.write("A7", "Zakázka: " + str(zakazka.cisloZakazky.get()))
    datumSplit = zakazka.datum.split('-')
    datum = datumSplit[2] + '/' + datumSplit[1] + '/' + datumSplit[0]
    ws.write("D7", "Datum: " + datum)
    ws.write("A8", "Jméno: " + zakazka.jmeno.get())
    ws.write("D8", "Telefon: " + zakazka.telefon.get())

    ws.merge_range("A9:J9", "", border_up_format)

    auto = zakazka.vozidlo
    ws.write("A10", "Vozidlo")
    ws.write("A11", "SPZ: " + auto.SPZ.get())
    ws.write("C11", "VIN: " + auto.VIN.get())
    ws.write("F11", "Značka: " + auto.znacka.get())
    ws.write("I11", "Model: " + auto.typ.get())
    ws.write("A12", "Motor: " + auto.motor.get())
    ws.write("C12", "r.v.: " + auto.rokVyroby.get())
    ws.write("F12", "Tachometr: " + auto.tachometr.get())

    ws.merge_range("A13:J13", "", border_up_format)

    # material
    ws.write("A14", "Material")
    ws.write("A15", "Položka")
    ws.write("F15", "Množství")
    ws.write("G15", "Cena za jednotku")
    ws.write("I15", "Cena celkem")

    wrap_format = wb.add_format()
    wrap_format.set_text_wrap()

    polozky = zakazka.polozky
    index = 15
    for pol in polozky:
        index += 1
        text = pol.oznaceni.get()
        font1 = ImageFont.truetype('calibri.ttf', 11)
        size = font1.getsize(text)
        lines = text.splitlines()
        rowSizeMax = 0
        if text == "":
            rowSizeMax = 1
        for line in lines:
            size = font1.getsize(line)
            rowSizeMax += int(size[0] / 224) + 1
            print(size[0])
        numberOfLines = rowSizeMax
        ws.set_row(index - 1, 14.500001 * numberOfLines)
        ws.merge_range("A" + str(index) + ":E" + str(index), text, wrap_format)
        ws.write("F" + str(index), pol.mnozstvi.get())
        ws.write("G" + str(index), pol.cenaZaJednotku.get() + " Kč")
        ws.write("I" + str(index), pol.cenaCelkem.get() + " Kč")

    index += 1
    ws.write("G" + str(index), "Celkem za materiál: ")
    ws.write("I" + str(index), zakazka.celkemZaMaterial.get() + " Kč")

    index += 1
    ws.merge_range("A" + str(index) + ":J" + str(index), "", border_up_format)

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
        text = p.oznaceni.get()
        font1 = ImageFont.truetype('calibri.ttf', 11)
        size = font1.getsize(text)
        lines = text.splitlines()
        rowSizeMax = 0
        if text == "":
            rowSizeMax = 1
        for line in lines:
            size = font1.getsize(line)
            rowSizeMax += int(size[0] / 224) + 1
            print(size[0])
        numberOfLines = rowSizeMax
        ws.set_row(index - 1, 14.500001 * numberOfLines)
        ws.merge_range("A" + str(index) + ":E" + str(index), text, wrap_format)

        ws.write("F" + str(index), p.mnozstvi.get())
        ws.write("G" + str(index), p.cenaZaJednotku.get() + " Kč")
        ws.write("I" + str(index), p.cenaCelkem.get() + " Kč")

    index += 1
    ws.write("G" + str(index), "Celkem za práci: ")
    ws.write("I" + str(index), zakazka.celkemZaPraci.get() + " Kč")

    index += 1
    ws.merge_range("A" + str(index) + ":J" + str(index), "", border_up_format)

    index += 1
    ws.write("G" + str(index), "Celkem: ")
    ws.write("I" + str(index), zakazka.celkemZaZakazku.get() + " Kč")

    wb.close()
    cwd = os.getcwd()
    os.startfile(cwd + "/" + fileName)


def search(combobox, searchableEntry):
    searchBy = combobox.get()
    hledanyVyraz = searchableEntry.get()
    if hledanyVyraz != '':
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
            refreshMainScreen(db.get())
    else:
        refreshMainScreen(db.get())


def refreshMainScreen(zak):
    # refresh
    mainScreenFrame.destroy()
    mainScreenFrame.__init__()
    mainScreenFrame.grid()

    mainScreen(zak)


class searchScreen:

    def __init__(self):
        self.searchScreen()

    def searchScreen(self):
        self.n = StringVar()
        self.n.set("SPZ")
        v = self.n.get()
        Label(searchFrame, text="Hledání").grid(columnspan=10)
        clientCombo = ttk.Combobox(searchFrame, textvariable=v, justify='center', state="readonly")
        clientCombo['values'] = ["SPZ", "Jméno", "VIN", ""]
        clientCombo.current(0)
        clientCombo.grid(row=2, column=0)

        m = StringVar()
        searchEntry = Entry(searchFrame, textvariable=m, justify='center', width=30)
        searchEntry.grid(row=3, column=0)
        searchEntry.bind("<Return>", lambda x: search(clientCombo, m))
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

    separator = ttk.Separator(canvasZ, orient="horizontal")
    separator.grid(row=1, sticky=E + W, columnspan=10)
    clients = []
    cisloRadku = 1
    for zakazka in zakazky:
        cisloZakazky = zakazka.cisloZakazky.get()
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
        # Button(canvasZ, command=lambda za=zakazka: tisk(za), text="Vytisknout").grid(row=cisloRadku, column=8)

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

    def findAndSetVehicleByVIN(event):
        zakazkyByVIN = db.getByVIN(z.vozidlo.VIN.get())
        if zakazkyByVIN and z.jmeno.get() == "":
            prvniZakazka = zakazkyByVIN[0]
            z.jmeno.set(prvniZakazka.jmeno.get())
            z.telefon.set(prvniZakazka.telefon.get())
            z.vozidlo.SPZ.set(prvniZakazka.vozidlo.SPZ.get())
            z.vozidlo.VIN.set(prvniZakazka.vozidlo.VIN.get())
            z.vozidlo.znacka.set(prvniZakazka.vozidlo.znacka.get())
            z.vozidlo.typ.set(prvniZakazka.vozidlo.typ.get())
            z.vozidlo.motor.set(prvniZakazka.vozidlo.motor.get())
            z.vozidlo.rokVyroby.set(prvniZakazka.vozidlo.rokVyroby.get())
            z.vozidlo.tachometr.set(prvniZakazka.vozidlo.tachometr.get())

    def odstranitPolozku(polo, can, poly):
        if messagebox.askokcancel("Vymazat", "Opravdu chcete vymazat?", parent=container):
            can.destroy()
            poly.remove(polo)
            ind = 1
            for po in poly:
                po.cislo.set(ind)
                ind += 1

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

    def pridatPolozku(canvasGroup, item):
        p = polozka.Polozka()
        p.cisloZakazky = z.ID

        item.append(p)
        p.cislo.set(len(item))
        showPolozku(p, canvasGroup, item)

    def showPolozku(p, canvasGroup, item):
        def enter(event):
            widget_height = (event.widget.winfo_height() - 4) / 16
            event.widget.config(height=widget_height + 1)

        def update_size(event):
            update_size_widget(event.widget)

        def update_size_widget(widget):
            height = widget.tk.call((widget, "count", "-update", "-displaylines", "1.0", "end"))
            widget.configure(height=height)
            text = widget.get("1.0", END)
            p.oznaceni.set(text[:text.rfind('\n')])

        def calculate(var, index, mode):
            mnozstvi = 0
            if p.mnozstvi.get() != '':
                mnozstvi = p.mnozstvi.get().replace(",", ".")
            cenaZaJednotku = 0
            if p.cenaZaJednotku.get() != '':
                cenaZaJednotku = p.cenaZaJednotku.get().replace(",", ".")
            p.cenaCelkem.set(
                float(mnozstvi) * float(cenaZaJednotku))
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

        Entry(canvasP, textvariable=p.cislo, state='disabled', justify='center', width=8).grid(row=2, column=0,
                                                                                               sticky=N)

        textOznaceni = Text(canvasP, width=58, wrap="word")
        textOznaceni.grid(row=2, column=1, sticky=N)
        textOznaceni.bind("<KeyRelease>", update_size)
        textOznaceni.bind("<Return>", enter)
        textOznaceni.configure(font=("Arial", 13))

        textOznaceni.delete(1.0, END)
        textOznaceni.insert(1.0, p.oznaceni.get())
        textOznaceni.after(100, lambda: update_size_widget(textOznaceni))

        Entry(canvasP, textvariable=p.mnozstvi, justify='center').grid(row=2, column=2, sticky=N)
        Entry(canvasP, textvariable=p.cenaZaJednotku, justify='center').grid(row=2, column=3, sticky=N)
        Entry(canvasP, textvariable=p.cenaCelkem, state='disabled', justify='center').grid(row=2, column=4, sticky=N)
        p.mnozstvi.trace("w", calculate)
        p.cenaZaJednotku.trace("w", calculate)

        button = Button(canvasP, text="X", width=5, command=lambda polo=p, can=canvasP: odstranitPolozku(polo, can, item))
        button.grid(row=2, column=5, sticky=N)
        button.configure(font=("Arial", 8))

    def saveNovaZakazka():
        db.save(z)
        db.saveVozidlo(v)

        db.deletePolozkyForZakazka(z.ID)
        for item in polozky:
            db.savePolozku(item, "material")

        for item in prace:
            db.savePolozku(item, "prace")

        container.destroy()
        refresh(opened)

    def zavrit():
        destroy = True
        if edited.val:
            if messagebox.askokcancel("Zavřít", "Opravdu chceš zavřít zakázku?\nZměny nebudou uloženy!",
                                      parent=container):
                destroy = True
            else:
                destroy = False
        if destroy:
            container.destroy()
            refresh(opened)

    def updated(self):
        edited.val = True

    def windowUpdated(self):
        canvasToScroll.configure(scrollregion=canvasToScroll.bbox("all"))

    def OnMouseWheel(event):
        canvasToScroll.yview_scroll(int(-1 * (event.delta / 120)), "units")

    if opened.val:
        opened.val = False
        v = z.vozidlo
        polozky = z.polozky
        prace = z.prace
        container = Toplevel(root)
        container.state("zoomed")
        container.title("Nová Zakázka")
        container.protocol("WM_DELETE_WINDOW", zavrit)
        container.bind("<Key>", updated)
        container.bind("<MouseWheel>", OnMouseWheel)

        canvasToScroll = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvasToScroll.yview)
        novaZakazkaWindow = ttk.Frame(canvasToScroll)

        novaZakazkaWindow.bind("<Configure>", windowUpdated)
        canvasToScroll.create_window((0, 0), window=novaZakazkaWindow, anchor="nw")
        canvasToScroll.configure(yscrollcommand=scrollbar.set)

        canvasToScroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        zakazkaV = Frame(novaZakazkaWindow)
        zakazkaV.grid(sticky=W, columnspan=10)

        headFrame = Frame(zakazkaV)
        headFrame.grid(row=0, columnspan=10, sticky=W)

        Label(headFrame, text="Zakázka").grid(row=0, column=0)
        separator = ttk.Separator(headFrame, orient="horizontal")
        separator.grid(row=1, sticky=E + W, columnspan=10)
        Label(headFrame, text="Číslo zakázky").grid(row=2, column=0)
        Entry(headFrame, textvariable=z.cisloZakazky, justify="center").grid(row=3, column=0)
        Label(headFrame, text="Datum").grid(row=2, column=1)
        datumSplit = z.datum.split('-')
        datum = datumSplit[2] + '/' + datumSplit[1] + '/' + datumSplit[0]
        Label(headFrame, text=datum).grid(row=3, column=1)

        Label(headFrame, text="Jméno").grid(row=4, column=0)
        Entry(headFrame, textvariable=z.jmeno, justify='center').grid(row=5, column=0)
        Label(headFrame, text="Telefon").grid(row=4, column=1)
        Entry(headFrame, textvariable=z.telefon, justify='center').grid(row=5, column=1)

        tk.Label(zakazkaV, text='     ').grid(column=0, row=1)
        Label(zakazkaV, text="Vozidlo").grid(row=3, column=0)
        ttk.Separator(zakazkaV, orient="horizontal").grid(row=4, sticky=E + W, columnspan=10)

        Label(zakazkaV, text="SPZ").grid(row=5, column=0)
        spzEntry = Entry(zakazkaV, textvariable=v.SPZ, justify='center')
        spzEntry.grid(row=6, column=0)
        spzEntry.bind("<FocusOut>", findAndSetVehicle)
        # novaZakazkaWindow.bind("<Key>", findAndSetVehicle)

        Label(zakazkaV, text="VIN").grid(row=5, column=1)
        vinEntry = Entry(zakazkaV, textvariable=v.VIN, justify='center', width=30)
        vinEntry.grid(row=6, column=1)
        vinEntry.bind("<FocusOut>", findAndSetVehicleByVIN)

        Label(zakazkaV, text="značka").grid(row=5, column=2)
        Entry(zakazkaV, textvariable=v.znacka, justify='center').grid(row=6, column=2)

        Label(zakazkaV, text="model").grid(row=5, column=3)
        Entry(zakazkaV, textvariable=v.typ, justify='center').grid(row=6, column=3)

        Label(zakazkaV, text="motor").grid(row=5, column=4)
        Entry(zakazkaV, textvariable=v.motor, justify='center').grid(row=6, column=4)

        Label(zakazkaV, text="rok výroby").grid(row=5, column=5)
        Entry(zakazkaV, textvariable=v.rokVyroby, justify='center').grid(row=6, column=5)

        Label(zakazkaV, text="tachometr").grid(row=5, column=6)
        Entry(zakazkaV, textvariable=v.tachometr, justify='center').grid(row=6, column=6)

        zakazkaP = Frame(novaZakazkaWindow)
        zakazkaP.grid(sticky=W, columnspan=10)

        tk.Label(zakazkaP, text='     ').grid(row=0, column=0)
        Label(zakazkaP, text="Materiál").grid(row=1, column=0)
        ttk.Separator(zakazkaP, orient="horizontal").grid(row=2, sticky=E + W, columnspan=10)

        Label(zakazkaP, text="č. položky").grid(row=3, column=0)
        Label(zakazkaP, text="Označení položky", width=57).grid(row=3, column=1)
        Label(zakazkaP, text="Množství", width=15).grid(row=3, column=2)
        Label(zakazkaP, text="Cena za jednotku", width=20).grid(row=3, column=3)
        Label(zakazkaP, text="Cena celkem", width=15).grid(row=3, column=4)

        canvasMaterial = Frame(novaZakazkaWindow)
        canvasMaterial.grid(columnspan=10, sticky="e", padx=224)

        Button(zakazkaP, command=lambda: pridatPolozku(zakazkaP, polozky), text="Přidat Material").grid(row=3,
                                                                                                        column=50)

        hasPolozku = False
        for pol in polozky:
            hasPolozku = True
            showPolozku(pol, zakazkaP, polozky)
        if not hasPolozku:
            pridatPolozku(zakazkaP, polozky)

        Label(canvasMaterial, text="Celkem za Material").grid(row=50, column=3)
        Entry(canvasMaterial, textvariable=z.celkemZaMaterial, state='disabled', justify='center').grid(row=50,
                                                                                                        column=4)

        zakazkaPrace = Frame(novaZakazkaWindow)
        zakazkaPrace.grid(sticky=W, columnspan=10)

        Label(zakazkaPrace, text='     ').grid(row=0, column=0)
        Label(zakazkaPrace, text="Práce").grid(row=1, column=0)
        ttk.Separator(zakazkaPrace, orient="horizontal").grid(row=2, sticky=E + W, columnspan=10)
        Label(zakazkaPrace, text="č. položky").grid(row=3, column=0)
        Label(zakazkaPrace, text="Označení práce", width=57).grid(row=3, column=1)
        Label(zakazkaPrace, text="Počet Nh", width=15).grid(row=3, column=2)
        Label(zakazkaPrace, text="Cena za Nh", width=20).grid(row=3, column=3)
        Label(zakazkaPrace, text="Cena celkem", width=15).grid(row=3, column=4)

        canvasPrace = Frame(novaZakazkaWindow)
        canvasPrace.grid(columnspan=10, sticky="e", padx=224)

        Button(zakazkaPrace, command=lambda: pridatPolozku(zakazkaPrace, prace), text="   Přidat Práci    ").grid(row=3,
                                                                                                                  column=50)
        hasPraci = False

        for prac in prace:
            hasPraci = True
            showPolozku(prac, zakazkaPrace, prace)
        if not hasPraci:
            pridatPolozku(zakazkaPrace, prace)

        Label(canvasPrace, text="Celkem za práci").grid(row=50, column=3)
        Entry(canvasPrace, textvariable=z.celkemZaPraci, state='disabled', justify='center').grid(row=50, column=4)

        Label(canvasPrace, text="Celkem").grid(row=51, column=3)
        Entry(canvasPrace, textvariable=z.celkemZaZakazku, state='disabled', justify='center').grid(row=51, column=4)

        zakazkaK = Frame(novaZakazkaWindow)
        zakazkaK.grid(columnspan=10)

        # Button(zakazkaK, command=zavrit, text="Zavřít").grid(row=50, column=0)
        Button(zakazkaK, command=saveNovaZakazka, text="Uložit").grid(row=50, column=50)
        Button(zakazkaK, command=lambda za=z: tisk(za), text="Vytisknout").grid(row=50, column=100)


def zavritMain():
    if messagebox.askokcancel("Zavřít", "Opravdu chceš zavřít Aplikaci Servis?", parent=root):
        root.destroy()


root = Tk()
root.title("Servis")
root.state("zoomed")
root.option_add("*Font", "arial 13")
root.protocol("WM_DELETE_WINDOW", zavritMain)
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# root.attributes("-fullscreen", True)
# default_font = tk.font.nametofont("TkDefaultFont")
# size = default_font.cget("size")
# # default_font.configure(size=max(size+5, 8))

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
