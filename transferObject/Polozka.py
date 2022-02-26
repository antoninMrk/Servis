from tkinter import StringVar


class Polozka:

    def __init__(self):
        self.ID = None
        self.cislo = StringVar()
        self.cisloZakazky = None
        self.oznaceni = StringVar()
        self.mnozstvi = StringVar()
        self.cenaZaJednotku = StringVar()
        self.cenaCelkem = StringVar()
        self.typ = None
