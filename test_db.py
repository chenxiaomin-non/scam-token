import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='wewemaylalong2A!',
    database='token_info'
)

cur = mydb.cursor()

cur.execute('SHOW TABLES;')
print(cur.fetchall())

sql = 'INSERT IGNORE INTO bsc_info ( \
    TokenAddress, Name, Symbol, Value_USD, Value_BNB, \
    TotalValue_USD, TotalTokenSupply, Holder, Transfers, Decimals) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
params = ("a", "b", "c", 1.0, 1.0, 1.0, 1, 1, 1, 1)

cur.execute(sql, params)
mydb.commit()
cur.execute('SELECT * FROM bsc_info')

rs = cur.fetchall()

for row in rs:
    print(row)

