import threading
import requests
from bs4 import BeautifulSoup as BS
import concurrent.futures
import mysql.connector

cookies = {
    '__stripe_mid': '0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74',
    'bscscan_cookieconsent': 'True',
    '_gid': 'GA1.2.492679293.1655110389',
    '__cuid': '49772a01dd2442d897ca9efb95c0679e',
    'amp_fef1e8': '9cdef6b7-de00-475b-bdd6-3867bad4f031R...1g5gno1en.1g5gno328.12.4.16',
    'ASP.NET_SessionId': 'vq2l3netspc2ms0fkgqbbi24',
    'cf_clearance': 'xfkOOpWdrtVi.JpRFTm5cMZZLN3k6xZkdP14MgdJWR0-1655279288-0-150',
    '__cflb': '02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njFLXzj8VM8hrGC',
    '_gat_gtag_UA_46998878_23': '1',
    '__cf_bm': 'xUIDqGrtUS_O6ledC7t9r695qh9TOmiU_AFE17jNozY-1655288509-0-AVoCOhA4nxRlx69Fo2leCXIKcAzWL5ziH0O6nR96DWkgv4pyGCLOsm5H+8yiae+26x1HsQGOmHYXj1Z6Hp5GflFio8ApF3eyvqZrHT+Nf0T4TIlerzx2ge22vfoLYW4MVQ==',
    '_ga_PQY6J2Q8EP': 'GS1.1.1655288509.20.1.1655288529.0',
    '_ga': 'GA1.2.608546645.1654740748',
}

headers = {
    'authority': 'bscscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '__stripe_mid=0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74; bscscan_cookieconsent=True; _gid=GA1.2.492679293.1655110389; __cuid=49772a01dd2442d897ca9efb95c0679e; amp_fef1e8=9cdef6b7-de00-475b-bdd6-3867bad4f031R...1g5gno1en.1g5gno328.12.4.16; ASP.NET_SessionId=vq2l3netspc2ms0fkgqbbi24; cf_clearance=xfkOOpWdrtVi.JpRFTm5cMZZLN3k6xZkdP14MgdJWR0-1655279288-0-150; __cflb=02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njFLXzj8VM8hrGC; _gat_gtag_UA_46998878_23=1; __cf_bm=xUIDqGrtUS_O6ledC7t9r695qh9TOmiU_AFE17jNozY-1655288509-0-AVoCOhA4nxRlx69Fo2leCXIKcAzWL5ziH0O6nR96DWkgv4pyGCLOsm5H+8yiae+26x1HsQGOmHYXj1Z6Hp5GflFio8ApF3eyvqZrHT+Nf0T4TIlerzx2ge22vfoLYW4MVQ==; _ga_PQY6J2Q8EP=GS1.1.1655288509.20.1.1655288529.0; _ga=GA1.2.608546645.1654740748',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39',
}


def get_info_from_BSC(token_address: str):
    url = 'https://bscscan.com/token/'
    response = requests.get(url + token_address, cookies=cookies, headers=headers).text

    soup = BS(response, 'html.parser')

    try:
        token_name = soup.find('div', attrs={'class': 'container py-3'}) \
                        .find('h1').text.strip().removeprefix('Token ')
        token_name = str(token_name)
    
        token_info = soup.find('div', attrs={'class': 'card-body'})

        token_value = token_info.find('div', attrs={'id': 'ContentPlaceHolder1_tr_valuepertoken'})
        value = token_value.find('span', attrs={'data-html': 'true'}).text.strip().removeprefix('$')
        value = float(value)
        value_bnb = token_value.find('span', attrs={'class': 'small text-secondary text-nowrap'}).text
        value_bnb = float(value_bnb.strip().removeprefix('@').removesuffix('BNB'))
        total_value = token_value.find('button').text.strip().removeprefix('$')
        total_value = float(total_value)


        total_token = token_info.find('div', attrs={'class': 'row align-items-center'}) \
            .find('div', attrs={'class': 'col-md-8 font-weight-medium'})
        total_token_num = total_token.find('span').text.strip().replace(',', '')
        total_token_num = int(total_token_num)
        token_symbol = str(total_token.find('b').text)

        token_holder = token_info.find('div', attrs={'id': 'ContentPlaceHolder1_tr_tokenHolders'}) \
            .find('div', attrs={'class': 'col-md-8'}).text.strip().replace('addresses', '')
        token_holder = int(token_holder)
    except AttributeError | ValueError:
        return ('', '---', 0, 0, 0, 0, 0, 0, 18)

    token_transaction = token_info.find('div', attrs={'id': 'ContentPlaceHolder1_trNoOfTxns'}).text \
        .replace('Transfers:', '').strip()
    try:
        token_transaction = int(token_transaction)
    except ValueError:
        token_transaction = 0

    decimal = soup.find('div', attrs={'id': 'ContentPlaceHolder1_trDecimals'}).text \
        .replace('Decimals:', '').strip()
    decimal = int(decimal)

    return (token_name, token_symbol, value, value_bnb, total_value, total_token_num,
            token_holder, token_transaction, decimal)
# get_info_from_BSC('0xd7c03d2c7416861488985d8421e4bb8da161bbe8')

list_commit = []

def crawl_info_to_db():
    mydb = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='wewemaylalong2A!'
    )
    
    cur = mydb.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS token_info;")
    cur.execute("USE token_info;")
    mydb.commit()
    
    cur.execute('DROP TABLE IF EXISTS bsc_info;')
    print("Dropped table bsc_info")
    cur.execute('''CREATE TABLE IF NOT EXISTS bsc_info(
        TokenAddress varchar(255) PRIMARY KEY,
        Name varchar(255),
        Symbol varchar(255),
        Value_USD float,
        Value_BNB float,
        TotalValue_USD float,
        TotalTokenSupply int,
        Holder int,
        Transfers int,
        Decimals int
    )''')
    print("Re-created table bsc_info")
    print('----------------------------------------------------------------')
    mydb.commit()

    fh = open('bsc_token_add.txt')
    count = 0
    

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        result = []
        for line in fh:
            # print(count, address, contract_name)
            result.append(executor.submit(a_little_tasks, line=line, count=count,))
            
            count += 1

        for rs in concurrent.futures.as_completed(result):
            print("Done:", rs.done())
    
    for commit in list_commit:
        x = threading.Thread(target=commit_to_db, args=(mydb, cur, commit))
        x.start()
        x.join()
        print("Done-commit: ", commit[2])
    mydb.commit()
    mydb.close()
        
        
tab_char = chr(9)
sql = 'INSERT IGNORE INTO bsc_info ( \
    TokenAddress, Name, Symbol, Value_USD, Value_BNB, \
    TotalValue_USD, TotalTokenSupply, Holder, Transfers, Decimals) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

def a_little_tasks(line: str, count):
    line = line.strip().split(tab_char)
    address = line[0].strip()
    contract_name = line[1].strip()

    try:
        rs = get_info_from_BSC(address)
        list_commit.append((address, rs[0], rs[1], rs[2], rs[3], rs[4], 
                rs[5], rs[6], rs[7], rs[8]))
        print("Success ", count, rs[0], rs[1])
    except Exception as e: 
        list_commit.append((address, contract_name, '---', 0.0, 0.0, 0.0, 0, 0, 0, 18))

        print("Failed ", count, type(e))

def commit_to_db(con, cur, commit_data):
    cur.execute(sql, commit_data)
    con.commit()

crawl_info_to_db()

