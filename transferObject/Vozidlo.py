from tkinter import StringVar


class Vozidlo:

    def __init__(self):
        self.ID = None
        self.cisloZakazky = None
        self.SPZ = StringVar()
        self.VIN = StringVar()
        self.znacka = StringVar()
        self.typ = StringVar()
        self.motor = StringVar()
        self.rokVyroby = StringVar()
        self.tachometr = StringVar()
