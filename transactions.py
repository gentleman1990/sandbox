#!/usr/bin/python

import traceback
import sys
from file_operations import FULL_PATH_TO_TYPING
from wallet import *


def buy(wallet, company_name, how_many, percentage_stop_loss, percentage_take_profit):
    close_price_from_file = get_close_price_from_file(company_name)
    stop_loss = round(float(close_price_from_file) * (float(100 - percentage_stop_loss) / 100),2)
    take_profit = round(float(close_price_from_file) * (float(100 + percentage_take_profit) / 100),2)
    if not wallet:
        wallet.append([company_name, how_many, close_price_from_file, str(datetime.date.today()), str(stop_loss), str(take_profit)])
        print "Shares for company %s bought in value %s with SL %s and TP %s" % (company_name, str(how_many), str(stop_loss), str(take_profit))
    elif already_in_wallet(company_name, wallet):
        print "Company already in wallet - you can't buy more"
    else:
        wallet.append([company_name, how_many, close_price_from_file, str(datetime.date.today()), str(stop_loss), str(take_profit)])
        print "Shares for company %s bought in value %s with SL %s and TP %s" % (company_name, str(how_many), str(stop_loss), str(take_profit))


def sell(company_name, how_many, wallet):
    for single_company in wallet:
        if single_company[0] == company_name:
            single_company[1] = int(single_company[1]) - int(how_many)
            print "Shares for company %s sold in value %s" % (company_name, str(how_many))


def check_for_selling(wallet_name):
    wallet_array = open_wallet(wallet_name)

    for sc in wallet_array:
        close_price = get_close_price_from_file(sc[0])
        stop_loss = sc[4]
        take_profit = sc[5]


def fetch_all_typed_company(algorithm_name):
    filename = str(datetime.date.today())
    typed_companies = []
    try:
        with open(FULL_PATH_TO_TYPING + filename + "_" + algorithm_name + ".txt") as f:
            for company_name in f:
                typed_companies.append(company_name.rstrip())
    except Exception as err:
        log_error_to_file("fetch_all_typed_company", "There isn't any typed company" + str(err))
        sys.exit(1)
    return typed_companies


def already_in_wallet(company_name, wallet):
    for single_company in wallet:
        if single_company[0] == company_name:
            return True
    return False

if __name__ == '__main__':
    try:
        wallet1 = open_wallet("test")
        all_typed_companies = fetch_all_typed_company("sma30_ema15")
        create_new_wallet("test", 10000)
        buy(wallet1, all_typed_companies[0], 10, 5, 5)
        buy(wallet1, all_typed_companies[1], 10, 5, 5)
        actualize_wallet("test", wallet1)
        sell(all_typed_companies[0], 5, wallet1)
        actualize_wallet("test", wallet1)
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)
