import sqlite3

conn = sqlite3.connect("servis.db")

c = conn.cursor()
c.execute("""INSERT INTO servis VALUES ('Jozo2', '19/2/2022','fiat')    
""")
c.execute("""""")

conn.commit()
conn.close()
