import sqlite3

conn = sqlite3.connect("servis.db")

c = conn.cursor()
c.execute("""CREATE TABLE zakazka (
ID text,
datum text, 
jmeno text,
telefon text
)""")
c.execute("""CREATE UNIQUE INDEX zakazka_idx ON zakazka(ID) 
""")
c.execute("""CREATE TABLE polozka (
ID integer primary key autoincrement,
cislo text,
cisloZakazky text,
oznaceni text,
mnozstvi text,     
cenaZaJednotku text,     
cenaCelkem text,
typ text    
)""")
c.execute("""CREATE UNIQUE INDEX polozka_idx ON polozka(ID) 
""")
c.execute("""CREATE TABLE vozidlo (
ID integer primary key autoincrement,
cisloZakazky text,
SPZ text,    
VIN text,    
znacka text,    
typ text,    
motor text,    
rokVyroby text,    
tachometr text  
)""")
c.execute("""CREATE UNIQUE INDEX vozidlo_idx ON vozidlo(ID) 
""")

conn.commit()
conn.close()
