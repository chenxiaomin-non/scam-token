import requests
from datetime import datetime

ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/ZOhGCZTUSVSxgQsreqF1y7qweOOjkak8"
BSC_KEY = 'EV41IX58376FTWQM37PW9T3ADJV18HSPZN'
ETHER_KEY = '92KN8VPM8UFJW2CP6PR6G4S9DJBDBM1TA5'


# get token info by the token address
# the result is a json contain
# logo, symbol, decimal and name

def get_token_info(token: str):
    explain = ''
    check_point = 0

    ### check with crptoquant api
    headers = {'Authorization': 'Bearer ' + token}
    url = 'https://api.cryptoquant.com/v1/erc20/status/entity-list?token=link&type=exchange'
    response = requests.get(url, headers=headers).json()
    
    if response['status']['code'] == 401:
        explain += ' - Not found information about the token in CryptoQuant - ERC20'
        check_point -= 1
    
    ### chekc with alchemy api
    json_data = { 
        'jsonrpc': '2.0',
        'method': 'alchemy_getTokenMetadata',
        'params': [token],
        'id': 1, }
    response = requests.post(ALCHEMY_URL, json=json_data).json()
    try:
        if response['error']['code'] == -32602:
            explain += '\n - Not found information about the token in Alchemy - ERC20'
            check_point -= 1
    except KeyError:
        explain = response['result']
        check_point = 0

    return (explain, check_point)

# print(get_token_info('0x1985365e9f78359a9B6AD760e32412f4a445E862'))

# get total supply of token by ContractAddress
def get_total_supply(contract_address: str):
    url = 'https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=' +\
         contract_address + '&apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    try:
        rs = int(data)
    except ValueError:
        rs = 0
    return rs


# get total circulating supply 
# -> the numbers of cryptocurrencies coins publicly available in the market

def get_total_circulating_supply(contract_address: str):
    url = 'https://api.bscscan.com/api?module=stats&action=tokenCsupply&contractaddress=' +\
        contract_address + '&apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    return int(data)

# print(get_total_circulating_supply('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))


# get token account balance from token address & account address

def get_account_balance(token_address: str, account_address: str):
    url = 'https://api.bscscan.com/api?module=account&action=tokenbalance' +\
        '&contractaddress=' + token_address + '&address=' + account_address +\
        '&tag=latest&apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    return int(data)

# print(get_account_balance('0xeece4436f3bb9d568f0a031c6f109888cd3ce120', '0x0db29475f74e639adb56d225900ae521c285e3ea'))


# verify the contract source code by the token_address
def verify_token_source_code(token_address: str):
    url = 'https://api.etherscan.io/api?module=contract&action=getsourcecode' +\
        '&address=' + token_address + '&apikey=' + ETHER_KEY

    data = requests.get(url).json()['result'][0]['ABI']
    if data == "Contract source code not verified":
        return ("Contract source code not verified", False)
    else:
        return ("Contract source code verified", True)


# get a list of normal transaction by address
# contain timestamp, [blocknumber, hash, nonce, blockHash, transactionindex]
# from - to - value - gas - gas price - isError
# contractAddress - cumulativeGasUsed

def get_list_transactions(address: str):
    url = 'https://api.bscscan.com/api?module=account&action=txlist&address=' +\
    address + '&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&' +\
    'apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    result = []
    for transaction in data:
        time = datetime.utcfromtimestamp(int(transaction['timeStamp'])) \
                    .strftime('%Y-%m-%d %H:%M:%S')
        sender = transaction['from']
        receiver = transaction['to']
        value = int(transaction['value']) / 10**18
        result.append((time, sender, receiver, value))
    
    return result

# print(get_list_transactions('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))
# print(get_list_transactions('0x0db29475f74e639adb56d225900ae521c285e3ea'))

# get infor about the creator of the token
def get_creator_of_token(address: str):
    transaction = get_list_transactions(address)[-1]
    (time, creator, _, _) = transaction
    explain = "Token Address: " + address + "\nCreator: " + creator + "\n" +\
        "Time create: "+ time 
    
    return (explain, creator)

# print(get_creator_of_token('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))


# get the total token which is held by the creator 
def get_total_token_of_creator(address: str):
    (_, creator) = get_creator_of_token(address)
    number_of_token = int(get_account_balance(address, creator))
    total_cir = int(get_total_circulating_supply(address))

    return (number_of_token, number_of_token/total_cir * 100)

# print(get_total_token_of_creator('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))

# print(verify_token_source_code('0xeece4436f3bb9d568f0a031c6f109888cd3ce120'))

def check_validate_input(token: str):
    result = get_total_supply(token)
    if result == 0:
        return False
    return True

# get the liquidity of the token by USD or BNB
def get_liquidity_of_token(token: str):
    url = 'https://api.pancakeswap.info/api/v2/tokens/' + token
    response = requests.get(url).json()
    try:
        data = response['data']
        name = data['name']
        symbol = data['symbol']
        price_USD = data['price']
        price_BNB = data['price_BNB']
    except:
        return('Not Found', 'Not Found', '0', '0.0')
    return (name, symbol, price_USD, price_BNB)