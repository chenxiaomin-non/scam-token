import requests
from bs4 import BeautifulSoup



cookies = {
    'ASP.NET_SessionId': 'dyz5pht1znunf4rajfc1vzgb',
    '__cflb': '02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njGKxWpUm2DtKRv',
    '_gid': 'GA1.2.224020595.1654740748',
    '__stripe_mid': '0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74',
    '__cuid': '49772a01dd2442d897ca9efb95c0679e',
    'bscscan_cookieconsent': 'True',
    '__cf_bm': 'X9eommP6Dnq07c1xXTCvXStVRtq3Ax8QDDCcPkrM0pQ-1654765006-0-AcSzpRfvU4RGhShVEkK5TiT+f5UUbgi5yPeJIbeKNcsLZ+BQq3vClfPEfXGka1pUDQwNdDb2+oUolwGTG3adQzUJzNT+UeqhOXegCLc6rPqf6P6LuOPGK/Sl39CueANNTQ==',
    'amp_fef1e8': 'e28591fc-3928-47d5-80ba-92c06d3887acR...1g53r3t29.1g53r3t29.i.2.k',
    '__stripe_sid': '9e460181-1480-4890-b15f-d05b3817d75d4f5643',
    '_gat_gtag_UA_46998878_23': '1',
    '_ga_PQY6J2Q8EP': 'GS1.1.1654765006.5.1.1654765790.0',
    '_ga': 'GA1.2.608546645.1654740748',
}

headers = {
    'authority': 'bscscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'ASP.NET_SessionId=dyz5pht1znunf4rajfc1vzgb; __cflb=02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njGKxWpUm2DtKRv; _gid=GA1.2.224020595.1654740748; __stripe_mid=0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74; __cuid=49772a01dd2442d897ca9efb95c0679e; bscscan_cookieconsent=True; __cf_bm=X9eommP6Dnq07c1xXTCvXStVRtq3Ax8QDDCcPkrM0pQ-1654765006-0-AcSzpRfvU4RGhShVEkK5TiT+f5UUbgi5yPeJIbeKNcsLZ+BQq3vClfPEfXGka1pUDQwNdDb2+oUolwGTG3adQzUJzNT+UeqhOXegCLc6rPqf6P6LuOPGK/Sl39CueANNTQ==; amp_fef1e8=e28591fc-3928-47d5-80ba-92c06d3887acR...1g53r3t29.1g53r3t29.i.2.k; __stripe_sid=9e460181-1480-4890-b15f-d05b3817d75d4f5643; _gat_gtag_UA_46998878_23=1; _ga_PQY6J2Q8EP=GS1.1.1654765006.5.1.1654765790.0; _ga=GA1.2.608546645.1654740748',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33',
}

params = {
    'm': 'normal',
    'a': '0xeece4436f3bb9d568f0a031c6f109888cd3ce120',
    'v': '0xeece4436f3bb9d568f0a031c6f109888cd3ce120',
}

response = requests.get('https://bscscan.com/address-events', 
                params=params, cookies=cookies, headers=headers).text

soup = BeautifulSoup(response, "html.parser")

list_tr = soup.find_all("tr")

data_tr = []

TOTAL_SUPPLY = 21000000000000000000000000

for tr in list_tr:
    if tr.find("hash-tag text-truncate") != -1:
        data_tr.append(tr)

for tr in data_tr[:-2]:
    tr_soup = BeautifulSoup(str(tr), "html.parser")
    td_list = tr_soup.find_all("td")
    try:
        td_log = td_list[2].find_all("table")[0]

        td_info = td_list[0]
        span_list = td_info.find_all("span")
        print("Transaction Hash: ", span_list[0].text)
        print("Time: ", span_list[1].text)


        value_soup = td_log.find_all("span", style="display:none")
        number = int(value_soup[0].text, 16)
        print("Value: ",number)
        if TOTAL_SUPPLY // number <= 20:
            print("Alert: The transaction > 5% of the total supply!")
        
        print()

    except Exception:
        continue
    

    
