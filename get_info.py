import requests

ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/ZOhGCZTUSVSxgQsreqF1y7qweOOjkak8"
BSC_KEY = 'EV41IX58376FTWQM37PW9T3ADJV18HSPZN'


# get token info by the token address
# the result is a json contain
# logo, symbol, decimal and name

def get_token_info(token: str):
    json_data = {
        'jsonrpc': '2.0',
        'method': 'alchemy_getTokenMetadata',
        'params': [token],
        'id': 1
    }

    return requests.post(url=ALCHEMY_URL, json= json_data).text


# get a list of normal transaction by address
# contain timestamp, [blocknumber, hash, nonce, blockHash, transactionindex]
# from - to - value - gas - gas price - isError
# contractAddress - cumulativeGasUsed
def get_list_transactions(address: str):
    url = 'https://api.bscscan.com/api?module=account&action=txlist&address=' +\
    address + '&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&' +\
    'apikey=' + BSC_KEY
    
    return requests.get(url).text

print(get_list_transactions('0xF426a8d0A94bf039A35CEE66dBf0227A7a12D11e'))

