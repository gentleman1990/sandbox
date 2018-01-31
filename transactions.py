#!/usr/bin/python

import sys
import datetime

from file_operations import FULL_PATH_TO_TYPING
from wallet import *
from logger import log_error_to_file
from getters import *
from math import floor


MAX_COMPANIES_IN_WALLET = 5
PERCENTAGE_STOP_LOSS = 5
PERCENTAGE_TAKE_PROFIT = 5


def analyze_for_buying(wallet_name, typed_companies_list, source_data):
    wallet = open_wallet(wallet_name)
    buy(wallet_name, source_data, typed_companies_list, wallet)
    save_wallet(wallet_name, wallet)


def buy(wallet_name, source_data, typed_companies_list, wallet):
    cleared_typed_companies_list = remove_companies_already_in_wallet(wallet, typed_companies_list)
    starting_index = fetch_starting_index(cleared_typed_companies_list, wallet)
    for single_company_index in range(starting_index, -1, -1):
        typed_company_name = cleared_typed_companies_list[single_company_index]
        close_price = float(get_last_close_price(typed_company_name, source_data))
        counts = int(floor(STARTING_FUNDS / MAX_COMPANIES_IN_WALLET / close_price))
        stop_loss = round(float(close_price) * (float(100 - PERCENTAGE_STOP_LOSS) / 100), 2)
        take_profit = round(float(close_price) * (float(100 + PERCENTAGE_TAKE_PROFIT) / 100), 2)
        date = get_last_date(typed_company_name, source_data)

        wallet.append([typed_company_name, counts, close_price, date, stop_loss, take_profit])
        update_free_funds(wallet_name, -(counts*close_price))
        print "Shares for company %s bought in value %s with SL %s and TP %s" % (
        typed_company_name, str(counts), str(stop_loss), str(take_profit))


def analyze_for_selling(wallet_name, source_data):
    wallet = open_wallet(wallet_name)
    wallet_after_selling = sell(wallet_name, wallet, source_data)
    save_wallet(wallet_name, wallet_after_selling)


def sell(wallet_name, wallet, source_data):
    wallet_after_selling = []
    for single_company in wallet:
        company_name = get_company_name(single_company)
        close_price = get_last_close_price(company_name, source_data)
        purchase_price = get_purchase_price_for_company_in_wallet(single_company)
        stop_loss = get_stop_loss_for_company_in_wallet(single_company)
        take_profit = get_take_profit_for_company_in_wallet(single_company)
        number_of_shares = get_number_of_shares_for_company_in_wallet(single_company)

        if close_price > take_profit:
            current_percentage_profit = (take_profit * 100 / purchase_price)
            new_stop_loss = round(float(purchase_price) * (float(current_percentage_profit - 2.5) / 100), 2)
            new_take_profit = round(float(purchase_price) * (float(current_percentage_profit + 5) / 100), 2)

            wallet_after_selling.append([company_name, number_of_shares, purchase_price,
                                         get_purchase_date_for_company_in_wallet(single_company),
                                         new_stop_loss, new_take_profit])
        elif close_price < stop_loss:
            print "Shares for company %s sold in value %s" % (
            company_name, str(get_number_of_shares_for_company_in_wallet(single_company)))

            save_wallet_history(wallet_name, fetch_single_wallet_list_row_for_selling(wallet, single_company, source_data))
            update_free_funds(wallet_name, round(number_of_shares * close_price, 2))
        else:
            wallet_after_selling.append(single_company)
    return wallet_after_selling


def fetch_starting_index(cleared_typed_companies_list, wallet):
    starting_index = MAX_COMPANIES_IN_WALLET - len(wallet) - 1
    if starting_index > len(cleared_typed_companies_list) - 1:
        return len(cleared_typed_companies_list) - 1
    return starting_index


def remove_companies_already_in_wallet(wallet, typed_companies_list):
    for sc in wallet:
        while sc[0] in typed_companies_list:
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


def fetch_single_wallet_list_row_for_selling(wallet, single_company, source_data):
    wallet_history_list_row = []
    company_name = get_company_name(single_company)
    close_price = get_last_close_price(company_name, source_data)
    purchase_price = get_purchase_price_for_company_in_wallet(single_company)
    number_of_shares = get_number_of_shares_for_company_in_wallet(single_company)
    result = round(float(close_price - purchase_price) * number_of_shares, 2)
    purchase_date = get_last_purchase_price(company_name, wallet)
    sold_date = get_last_date(company_name, source_data)

    wallet_history_list_row.append([company_name, number_of_shares, close_price, purchase_date, sold_date, result])

    return wallet_history_list_row
