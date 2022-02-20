class Zakazka:

    def __init__(self):
        self.ID = None
        self.datum = None
        self.polozky = []
        self.vozidlo = None

    def addPolozka(self, polozka):
        self.polozky.append(polozka)
