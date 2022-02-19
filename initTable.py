import sqlite3

conn = sqlite3.connect("servis.db")

c = conn.cursor()
c.execute("""CREATE TABLE zakazka (
cislo text,
datum text    
)""")
c.execute("""CREATE TABLE polozka (
cisloZakazky text,
cislo text,
oznaceni text,
mnozstvi text,     
cenaZaJednotku text,     
cenaCelkem text    
)""")
c.execute("""CREATE TABLE vozidlo (
cisloZakazky text,
SPZ text,    
VIN text,    
znacka text,    
typ text,    
motor text,    
rokVyroby text,    
tachometr text  
)""")

conn.commit()
conn.close()
