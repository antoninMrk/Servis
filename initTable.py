import sqlite3

conn = sqlite3.connect("servis.db")

c = conn.cursor()
c.execute("""CREATE TABLE servis (
client text,
time text,
car text     
)""")

conn.commit()
conn.close()