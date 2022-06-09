import requests

ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/ZOhGCZTUSVSxgQsreqF1y7qweOOjkak8"
BSC_KEY = 'EV41IX58376FTWQM37PW9T3ADJV18HSPZN'
ETHER_KEY = '92KN8VPM8UFJW2CP6PR6G4S9DJBDBM1TA5'

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

# print(get_list_transactions('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))
# print(get_list_transactions('0x0db29475f74e639adb56d225900ae521c285e3ea'))

# get total supply of token by ContractAddress

def get_total_supply(contract_address: str):
    url = 'https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=' +\
         contract_address + '&apikey=' + BSC_KEY
    
    return requests.get(url).text

# print(get_total_supply('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))

# get total circulating supply 
# -> the numbers of cryptocurrencies coins publicly available in the market

def get_total_circulating_supply(contract_address: str):
    url = 'https://api.bscscan.com/api?module=stats&action=tokenCsupply&contractaddress=' +\
        contract_address + '&apikey=' + BSC_KEY
    
    return requests.get(url).text

# print(get_total_circulating_supply('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))


# get token account balance from token address & account address

def get_account_balance(token_address: str, account_address: str):
    url = 'https://api.bscscan.com/api?module=account&action=tokenbalance' +\
        '&contractaddress=' + token_address + '&address=' + account_address +\
        '&tag=latest&apikey=' + BSC_KEY
    
    return requests.get(url).text

# print(get_account_balance('0xeece4436f3bb9d568f0a031c6f109888cd3ce120', '0x0db29475f74e639adb56d225900ae521c285e3ea'))


# verify the contract source code by the token_address

def verify_token_source_code(token_address: str):
    url = 'https://api.etherscan.io/api?module=contract&action=getsourcecode' +\
        '&address=' + token_address + '&apikey=' + ETHER_KEY

    return requests.get(url).text



print(verify_token_source_code('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))