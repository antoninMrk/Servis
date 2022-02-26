from tkinter import StringVar


class Zakazka:

    def __init__(self):
        self.ID = None
        self.jmeno = StringVar()
        self.datum = None
        self.polozky = []
        self.vozidlo = None
        self.telefon = StringVar()

    def addPolozka(self, polozka):
        self.polozky.append(polozka)
