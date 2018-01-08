#!/usr/bin/python

import traceback
import sys
import math

from file_operations import FULL_PATH_TO_TYPING
from wallet import *
from logger import log_error_to_file


def buy(wallet, company_name, how_many, percentage_stop_loss, percentage_take_profit):
    close_price_from_file = get_close_price_from_file(company_name)
    stop_loss = round(float(close_price_from_file) * (float(100 - percentage_stop_loss) / 100),2)
    take_profit = round(float(close_price_from_file) * (float(100 + percentage_take_profit) / 100), 2)
    if not wallet:
        wallet.append([company_name, how_many, close_price_from_file, str(datetime.date.today()), str(stop_loss), str(take_profit)])
        print "Shares for company %s bought in value %s with SL %s and TP %s" % (company_name, str(how_many), str(stop_loss), str(take_profit))
    elif already_in_wallet(company_name, wallet):
        print "Company already in wallet - you can't buy more"
    else:
        wallet.append([company_name, how_many, close_price_from_file, str(datetime.date.today()), str(stop_loss), str(take_profit)])
        print "Shares for company %s bought in value %s with SL %s and TP %s" % (company_name, str(how_many), str(stop_loss), str(take_profit))


def sell(wallet, company_name, how_many):
    for single_company in wallet:
        if single_company[0] == company_name:
            single_company[1] = int(single_company[1]) - int(how_many)
            print "Shares for company %s sold in value %s" % (company_name, str(how_many))


def check_for_selling():
    # Structure for single company [sc] in wallet you can find in wallet.create_new_wallet()
    # sc[0] - Company name   | sc[1] - Counts
    # sc[2] - Purchase price | sc[3] - Datetime
    # sc[4] - Stop Loss      | sc[5] - Take profit

    wallets_list = open_wallets()

    for wallet_name in wallets_list:
        for sc in wallets_list[wallet_name]:
            wallet_list = wallets_list[wallet_name]
            close_price = get_close_price_from_file(sc[0])
            stop_loss = float(sc[4])
            take_profit = float(sc[5])
            purchase_price = float(sc[2])

            if close_price < stop_loss:
                sell(wallet_list, sc[0], sc[1])
                actualize_wallet(wallet_name, wallet_list)
            elif close_price > take_profit:
                sc[4] = take_profit
                current_percentage_profit = (take_profit * 100 / purchase_price)
                new_take_profit = round(float(sc[2]) * (float(current_percentage_profit + 5) / 100), 2)
                sc[5] = new_take_profit
                actualize_wallet(wallet_name, wallet_list)


def check_for_buying(wallet_name, typed_companies_list):
    # Structure for single company [sc] in wallet you can find in wallet.create_new_wallet()
    # sc[0] - Company name   | sc[1] - Counts
    # sc[2] - Purchase price | sc[3] - Datetime
    # sc[4] - Stop Loss      | sc[5] - Take profit

    opened_wallet = open_wallet(wallet_name)
    wallet_funds = float(fetch_root_file_for_wallet(wallet_name)[1])
    wallet_free_funds = float(fetch_root_file_for_wallet(wallet_name)[2])
    funds_per_company = float(wallet_funds) / 5
    how_many_company_can_we_obtain = math.floor(wallet_free_funds / funds_per_company)

    try:
        for index in range(0, int(how_many_company_can_we_obtain), 1):
            company_name = typed_companies_list[index]
            close_price = float(get_close_price_from_file(company_name))
            how_many = math.floor(funds_per_company / close_price)
            buy(opened_wallet, company_name, how_many, 5, 5)
        actualize_wallet(wallet_name, opened_wallet)
    except Exception as err:
        log_error_to_file("buy", ("Cannot buy stack for wallet %s. Reason: %s") % (wallet_name, err))


    #for sc in opened_wallet:
    #    print sc
    #    get_close_price_from_file(sc[0])
        #odejmowanie od free funds jezeli cos kupimy
        # curent wallet funds - obecna wartosc portfela - suma wszystkich spolek * close price ?
        # przy actualize wallet dodac aktualizowanie root o wartosci dla free funds i current wallet funds


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
        # wallet1 = open_wallet("test")
        all_typed_companies = fetch_all_typed_company("sma30_ema15")

        if all_typed_companies:
            create_new_wallet("test2", 10000)
            check_for_selling()
            check_for_buying("test", all_typed_companies)
        # buy(wallet1, all_typed_companies[0], 10, 5, 5)
        # buy(wallet1, all_typed_companies[1], 10, 5, 5)
        # actualize_wallet("test", wallet1)
        # sell(all_typed_companies[0], 5, wallet1)
        # actualize_wallet("test", wallet1)
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)
