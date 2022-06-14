import sqlite3

con = sqlite3.connect('token.db')

cur = con.cursor()

cur.execute('DROP TABLE TokenData')

con.commit()

con.close()