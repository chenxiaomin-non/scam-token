import requests
from bs4 import BeautifulSoup as BS

cookies = {
    '__stripe_mid': '0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74',
    '__cuid': '49772a01dd2442d897ca9efb95c0679e',
    'bscscan_cookieconsent': 'True',
    'amp_fef1e8': 'e28591fc-3928-47d5-80ba-92c06d3887acR...1g543kalk.1g543m86p.u.2.10',
    'ASP.NET_SessionId': 'xaddwg0bozgkhvuisyn4lnjr',
    '__cflb': '0H28vyb6xVveKGjdV3CYUMgiti5JgVsZrvLVC2sjuja',
    '_gid': 'GA1.2.492679293.1655110389',
    '_ga_PQY6J2Q8EP': 'GS1.1.1655110388.10.1.1655111310.0',
    '_ga': 'GA1.2.608546645.1654740748',
    '_gat_gtag_UA_46998878_23': '1',
    '__cf_bm': 'uV4OZwmhMSV8j2uTS0sj7gbrjb7OnKywZoPK01D4boE-1655111310-0-AShsP3NEnilz1f3DyBoOQXr2EbJDMbJwXgo7xMZZ1CpjexpxW2qG9XTtj95XDQ+fo0OtFPYI9n9g5q7qmmmizItQbPFtAywGvF7Vi7tu/0tgAJCXF3eNBFa//UVlcHXIyA==',
}

headers = {
    'authority': 'bscscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '__stripe_mid=0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74; __cuid=49772a01dd2442d897ca9efb95c0679e; bscscan_cookieconsent=True; amp_fef1e8=e28591fc-3928-47d5-80ba-92c06d3887acR...1g543kalk.1g543m86p.u.2.10; ASP.NET_SessionId=xaddwg0bozgkhvuisyn4lnjr; __cflb=0H28vyb6xVveKGjdV3CYUMgiti5JgVsZrvLVC2sjuja; _gid=GA1.2.492679293.1655110389; _ga_PQY6J2Q8EP=GS1.1.1655110388.10.1.1655111310.0; _ga=GA1.2.608546645.1654740748; _gat_gtag_UA_46998878_23=1; __cf_bm=uV4OZwmhMSV8j2uTS0sj7gbrjb7OnKywZoPK01D4boE-1655111310-0-AShsP3NEnilz1f3DyBoOQXr2EbJDMbJwXgo7xMZZ1CpjexpxW2qG9XTtj95XDQ+fo0OtFPYI9n9g5q7qmmmizItQbPFtAywGvF7Vi7tu/0tgAJCXF3eNBFa//UVlcHXIyA==',
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
    url = 'https://bscscan.com/address/'
    response = requests.get(url + token_address, cookies=cookies, headers=headers).text

    soup = BS(response, 'html.parser')
    rs = soup.find(id='ContentPlaceHolder1_tr_tokeninfo').text
    text = str(rs).replace('Token', '').replace('Tracker:', '').replace('\n', '').strip()
    rs = text.split(' ')
    for dt in rs[1:-1]:
        rs[0] += (' ' + dt)
    return (rs[0], rs[-1].replace('(', '').replace(')', ''))
# get_info_from_BSC('0xd7c03d2c7416861488985d8421e4bb8da161bbe8')