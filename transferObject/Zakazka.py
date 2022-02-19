class Zakazka:

    def __init__(self):
        self.number = None
        self.date = None
        self.polozky = []
        self.vozidlo = None

    def setNumber(self, number):
        self.number = number

    def setDate(self, date):
        self.date = date

    def setPolozky(self, polozky):
        self.polozky = polozky

    def addPolozka(self, polozka):
        self.polozky.append(polozka)
