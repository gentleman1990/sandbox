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
        print "Company already" + company_name + "in wallet - you can't buy more"
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
        root_wallet = fetch_root_file_for_wallet(wallet_name)
        starting_funds = float(root_wallet[0])
        wallet_funds = float(root_wallet[1])
        wallet_free_funds = float(root_wallet[2])

        for sc in wallets_list[wallet_name]:
            wallet_list = wallets_list[wallet_name]
            close_price = get_close_price_from_file(sc[0])
            count = int(sc[1])
            stop_loss = float(sc[4])
            take_profit = float(sc[5])
            purchase_price = float(sc[2])

            if close_price < stop_loss:
                sell(wallet_list, sc[0], sc[1])
                actualize_wallet(wallet_name, wallet_list)

                wallet_funds += ((close_price - purchase_price) * count)
                wallet_free_funds += (close_price * count)
                actualize_root_file_for_wallet(wallet_name, [starting_funds, wallet_funds, wallet_free_funds])
            elif close_price > take_profit:
                current_percentage_profit = (take_profit * 100 / purchase_price)
                sc[4] = round(float(sc[2]) * (float(current_percentage_profit - 2.5) / 100), 2)
                new_take_profit = round(float(sc[2]) * (float(current_percentage_profit + 5) / 100), 2)
                sc[5] = new_take_profit
                actualize_wallet(wallet_name, wallet_list)


def check_for_buying(wallet_name, typed_companies_list):
    # Structure for single company [sc] in wallet you can find in wallet.create_new_wallet()
    # sc[0] - Company name   | sc[1] - Counts
    # sc[2] - Purchase price | sc[3] - Datetime
    # sc[4] - Stop Loss      | sc[5] - Take profit

    opened_wallet = open_wallet(wallet_name)
    cleared_typed_companies_list = remove_companies_already_in_wallet(opened_wallet, typed_companies_list)
    root_file_for_wallet = fetch_root_file_for_wallet(wallet_name)
    starting_funds = float(root_file_for_wallet[0])
    wallet_funds = float(root_file_for_wallet[1])
    wallet_free_funds = float(root_file_for_wallet[2])
    funds_per_company = float(wallet_funds) / 5
    how_many_company_can_we_obtain = 5 - len(opened_wallet)

    try:
        for index in range(0, int(how_many_company_can_we_obtain), 1):
            company_name = cleared_typed_companies_list[index]
            close_price = float(get_close_price_from_file(company_name))
            how_many = int(math.floor(funds_per_company / close_price))
            total_cost = (float(how_many) * close_price)
            if wallet_free_funds > total_cost:
                buy(opened_wallet, company_name, how_many, 5, 5)
                wallet_free_funds -= total_cost
            elif total_cost > wallet_free_funds > 1000:
                how_many = int(math.floor(wallet_free_funds / close_price))
                total_cost = (float(how_many) * close_price)
                buy(opened_wallet, company_name, how_many, 5, 5)
                wallet_free_funds -= total_cost
        actualize_wallet(wallet_name, opened_wallet)
        actualize_root_file_for_wallet(wallet_name, [starting_funds, wallet_funds, wallet_free_funds])
    except Exception as err:
        log_error_to_file("buy", ("Cannot buy stack for wallet %s. Reason: %s") % (wallet_name, err))


def remove_companies_already_in_wallet(opened_wallet, typed_companies_list):
    for sc in opened_wallet:
        if sc[0] in typed_companies_list:
            typed_companies_list.remove(sc[0])
    return typed_companies_list


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


def fetch_all_typed_company_for_simulator(algorithm_name):
    typed_companies = []
    try:
        with open(FULL_PATH_TO_TYPING + "simulator_" + algorithm_name + ".txt") as f:
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
        # create_new_wallet("test3", 15000)
        all_typed_companies = fetch_all_typed_company("sma30_ema15")

        if all_typed_companies:
            create_new_wallet("sma_ema", 10000)
            check_for_selling()
            check_for_buying("sma_ema", all_typed_companies)
        # buy(wallet1, all_typed_companies[0], 10, 5, 5)
        # buy(wallet1, all_typed_companies[1], 10, 5, 5)
        # actualize_wallet("test", wallet1)
        # sell(all_typed_companies[0], 5, wallet1)
        # actualize_wallet("test", wallet1)
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)
