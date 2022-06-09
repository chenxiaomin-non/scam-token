import requests

from bs4 import BeautifulSoup

cookies = {
    'ASP.NET_SessionId': 'dyz5pht1znunf4rajfc1vzgb',
    '__cflb': '02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njGKxWpUm2DtKRv',
    '_gid': 'GA1.2.224020595.1654740748',
    '__stripe_mid': '0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74',
    'bscscan_userid': 'truongtnn404',
    'bscscan_pwd': 'lhhuong80045',
    'bscscan_autologin': 'True',
    '__cuid': '49772a01dd2442d897ca9efb95c0679e',
    'amp_fef1e8': 'e28591fc-3928-47d5-80ba-92c06d3887acR...1g53llp7n.1g53llp7n.h.2.j',
    '__cf_bm': 'ryYMbJhxwugNZT5O1X67DS06NNztYcWOno33q1W1Zrc-1654760702-0-ATx0ZCvONZ1PTZuvYOQPs48MqoYvi9tvkHGzC07s5hFHWT6T8PaR2U5MB7MCwm3VUbgRJnG//vVAvua6rE7aJa2bgjMx60lHHo2XT3TUq0quQNytb/K6SLVOce06qeFoOA==',
    '_ga_PQY6J2Q8EP': 'GS1.1.1654760701.4.1.1654761090.0',
    '_ga': 'GA1.2.608546645.1654740748',
}

headers = {
    'authority': 'bscscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'ASP.NET_SessionId=dyz5pht1znunf4rajfc1vzgb; __cflb=02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njGKxWpUm2DtKRv; _gid=GA1.2.224020595.1654740748; __stripe_mid=0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74; bscscan_userid=truongtnn404; bscscan_pwd=lhhuong80045; bscscan_autologin=True; __cuid=49772a01dd2442d897ca9efb95c0679e; amp_fef1e8=e28591fc-3928-47d5-80ba-92c06d3887acR...1g53llp7n.1g53llp7n.h.2.j; __cf_bm=ryYMbJhxwugNZT5O1X67DS06NNztYcWOno33q1W1Zrc-1654760702-0-ATx0ZCvONZ1PTZuvYOQPs48MqoYvi9tvkHGzC07s5hFHWT6T8PaR2U5MB7MCwm3VUbgRJnG//vVAvua6rE7aJa2bgjMx60lHHo2XT3TUq0quQNytb/K6SLVOce06qeFoOA==; _ga_PQY6J2Q8EP=GS1.1.1654760701.4.1.1654761090.0; _ga=GA1.2.608546645.1654740748',
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

url = 'https://bscscan.com/address/'
token_address = '0xeece4436f3bb9d568f0a031c6f109888cd3ce120'

response = requests.get(url + token_address, cookies=cookies, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

data = soup.find_all("td")

for element in data:
    ele = str(element)
    if ele.find("showAge") != -1 or ele.find("showDate") != -1 or \
         ele.find("0x") != -1:
        
        ele_data = BeautifulSoup(ele, "html.parser")
        text = ele_data.text
        print(type(text))


        

