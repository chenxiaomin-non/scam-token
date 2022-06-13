import sqlite3

def create_table_if_not_exists():
    con = sqlite3.connect('token.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS TokenData (
        TokenAddress text,
        Score int,
        Explain text,
        Result text,
        Color text,
        Name text,
        Symbol text
    )''')

    con.commit()
    con.close()

def insert_token_data(TokenAddress: str, Score: int, Explain: str, Result: str, Color: str, Name: str, Symbol: str):
    con = sqlite3.connect('token.db')
    cur = con.cursor()
    cur.execute('INSERT INTO TokenData VALUES (?, ?, ?, ?, ?, ?, ?)', (TokenAddress, Score, Explain, Result, Color, Name, Symbol))
    con.commit()
    con.close()

def find_token_data(TokenAddress: str):
    con = sqlite3.connect('token.db')
    cur = con.cursor()
    create_table_if_not_exists()

    result = cur.execute('SELECT * FROM TokenData WHERE TokenAddress = ?', (TokenAddress,))
    rs = None
    for temp in result:
        rs = temp
    con.close()
    return rs
