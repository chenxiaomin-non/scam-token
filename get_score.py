import get_info, crawl_event

def get_score(address: str):
    original_score = 100

    # check the token information by using BSC Scan and Alchemy
    info_reason, to_info_point = get_info.get_token_info(address)
    if to_info_point == 0:
        info_reason = "Token information: OK"
    else:
        original_score+=to_info_point

    contract_source, isverified = get_info.verify_token_source_code(address)
    if isverified == False:
        original_score -= 20
    else:
        contract_source = "Contract Source code: OK"

    total_tok, creator_hold = get_info.get_total_token_of_creator(address)
    if creator_hold > 5:
        original_score -= 30

    total_sup = get_info.get_total_supply(address)

    trans,trans_exceed = crawl_event.get_transaction_of_the_token(address, total_sup)
    if trans_exceed > 5:
        original_score -= 30

    pers_set = crawl_event.get_all_person_hold_the_token(trans)

    holder_list, holder_count = crawl_event.get_balance_of_person_hold_token(pers_set, address)
    original_score -= holder_count * 5

    if original_score >= 70:
        total_explain = info_reason + '\n' + contract_source
        return original_score, "There's no sign of scamming with this token, but please be careful anyway", total_explain
    elif original_score >= 50 and original_score<=70:
        total_explain = info_reason + '\n' + contract_source
        return original_score, "This token is probably scam, please be careful", total_explain
    else:
        total_explain = info_reason + '\n' + contract_source
        return original_score, "This token is a scam, please stay away", total_explain
