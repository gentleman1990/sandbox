#!/usr/bin/python

import datetime
from getters import *
from wallet import save_statistics, open_wallet, open_wallet_history, fetch_free_funds


def prepare_statistics(wallet_name, source_data):
    wallet = open_wallet(wallet_name)
    wallet_history = open_wallet_history(wallet_name)
    free_funds = fetch_free_funds(wallet_name)
    current_wallet_value = 0
    total_result = 0
    date = ""
    for single_company in wallet:
        company_name = get_company_name(single_company)
        close_price = get_last_close_price(company_name, source_data)
        number_of_shares = get_number_of_shares_for_company_in_wallet(single_company)
        date = get_last_date(company_name, source_data)
        current_wallet_value = current_wallet_value + (close_price * number_of_shares)

    for single_historical_company in wallet_history:
        result = get_total_result(single_historical_company)

        current_wallet_value = current_wallet_value + result
        total_result = total_result + result

    current_wallet_value = current_wallet_value + free_funds
    single_statistics_row = ([str(date), round(current_wallet_value, 2), round(total_result, 2)])
    save_statistics(wallet_name, single_statistics_row)
