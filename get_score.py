import get_info, crawl_event

def get_score(address: str):
    original_score = 100

    explain = ""

    # check the token information by using BSC Scan and Alchemy
    INFO_POINT = 5
    info_reason, to_info_point = get_info.get_token_info(address)
    if to_info_point == 0:
        info_reason = " - Token information: OK"
    else:
        original_score += to_info_point*INFO_POINT
    explain += '''Information Check:\n''' + info_reason + '\n\n'


    # check the source code of the token contract is verified or not
    VERIFY_POINT = 20
    contract_source, isverified = get_info.verify_token_source_code(address)
    if isverified == False:
        original_score -= VERIFY_POINT
        this_explain = ''' - Verifying Contract Source Failed\n - Maybe creator authorized for special permission'''
    else:
        this_explain = " - Contract Source Verifying: OK"
    explain += '''Verify Contract Check:\n'''+ this_explain + '\n\n'


    # check the creator of the token contract hold more than 5% of 
    # the number of the token or not
    CREATOR_HOLD_TOKEN_POINT = 30
    total_tok, creator_hold = get_info.get_total_token_of_creator(address)
    explain += '''Token hold by creator Check:\n'''
    if creator_hold > 5:
        original_score -= CREATOR_HOLD_TOKEN_POINT
        explain += ''' - Creator hold more than 5% of the number of total supply\n\n'''
    elif creator_hold > 20:
        original_score -= 2*CREATOR_HOLD_TOKEN_POINT
        explain += ''' - Creator hold more than 20% of the number of total supply\n\n'''
    else:
        explain += ''' - Token hold by creator Check: OK\n\n'''

    total_sup = get_info.get_total_supply(address)

    # check the number of transaction that transaction value exceed 
    # 5% of total circulating supply
    TRANSACTION_VALUES_POINT = 20
    trans,trans_exceed = crawl_event.get_transaction_of_the_token(address, total_sup)
    explain += '''Transaction value Check: \n'''
    if trans_exceed > 5:
        original_score -= TRANSACTION_VALUES_POINT
        explain += ''' - The number of transaction which its value exceed 5% of total supply is more than 5\n\n'''
    else:
        explain += ''' - Transaction value Check: OK\n\n'''

    # number of transactions check
    NUMBER_OF_TRANSACTION_POINT = 20
    number_of_trans = len(trans)
    explain += '''Transaction Count Check:\n'''
    if number_of_trans <= 30:
        original_score -= NUMBER_OF_TRANSACTION_POINT
        explain += ' - The number of transactions is less than 30\n\n'
    elif number_of_trans <= 100:
        original_score -= 10
        explain += ' - The number of transactions is less than 100\n\n'
    else:
        original_score += 10
        explain += ' - Transaction Count Check: OK\n\n'

    pers_set = crawl_event.get_all_person_hold_the_token(trans)

    # get the number of token which is held by people
    # if there're so many people hold more than 5% of total supply
    # may be it's scam token
    holder_list, holder_count = crawl_event.get_balance_of_person_hold_token(pers_set, address)
    explain += "Holder Value Check: \n"
    if holder_count <= 2:
        original_score += 10
        explain += ' - There are less than 3 people hold at least 5% of total supply\n\n'
    elif holder_count <= 5:
        original_score -= 10
        explain += ' - There are 3 - 5 people hold at least 5% of total supply\n\n'
    else:
        original_score -= 20
        explain += ' - There are more than 5 people hold at least 5% of total supply\n\n'


    # get the liquidity of the token
    name, symbol, price, BNBprice = get_info.get_liquidity_of_token(address)
    explain += "Liquidity Check:\n"
    BNBprice = float(BNBprice)
    if BNBprice <= 0.1:
        explain += " - The token almost has no value ( < 0.1 BNB )\n\n"
        original_score -= 30
    elif BNBprice <= 0.4:
        explain += " - The token may not have value as we expected ( < 0.4 BNB )\n\n"
        original_score -= 10
    else:
        explain += " - Liquidity Check: OK"
        original_score += 15


    # check for special conditions
    if creator_hold > 99:
        original_score = 0
    elif creator_hold > 90 and original_score != 0:
        original_score = 0

    if original_score >= 70:
        return original_score, "There's no sign of scamming with this token, but please be careful anyway", explain
    elif original_score >= 40 :
        return original_score, "This token is probably scam, please be careful", explain
    else:
        return original_score, "This token is a scam, please stay away", explain, name, symbol
