#!/usr/bin/python

import os
import datetime

from file_operations import create_subfolder_for_wallets
from file_operations import get_full_path_to_wallet_directory
from file_operations import get_close_price_from_file
from logger import log_error_to_file, write_to_root_file_wallet, write_to_wallet_history, write_to_wallet


def create_new_wallet(wallet_name, starting_funds):
    if not os.path.exists(get_full_path_to_wallet_directory() + wallet_name):
        path_to_wallet = create_subfolder_for_wallets(wallet_name)
        with open(path_to_wallet + "root.txt", "a") as root:
            root.write("Starting funds, Current funds, Free funds\r\n")
            root.write(str(starting_funds) + ", " + str(starting_funds) + ", " + str(starting_funds))
        with open(path_to_wallet + "wallet.txt", "a") as wallet:
            wallet.write("Company Name, Counts, Purchase price, Datetime, Stop Loss, Take profit")
        with open(path_to_wallet + "wallet_history.txt", "a") as wallet_history:
            wallet_history.write("Company Name, Counts, Sold price, Datetime, Result")
    else:
        log_error_to_file("create_new_wallet", "Wallet has been already created!")


def actualize_wallet(wallet_name, wallet_list):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    actual_state = []

    with open(path_to_wallet + "wallet.txt", "r") as single_file:
        for line in single_file:
            single_row = [x.strip() for x in line.split(',')]
            actual_state.append(single_row)
        truncate_wallet_file(wallet_name)

    for single_company_from_new_wallet in wallet_list:
        new_company_for_purchase = lookup_for_companies_to_sold(actual_state, single_company_from_new_wallet,
                                                                wallet_name)

        if new_company_for_purchase:
            write_to_wallet(wallet_name, single_company_from_new_wallet[0], single_company_from_new_wallet[1],
                            single_company_from_new_wallet[2], str(datetime.date.today()), single_company_from_new_wallet[4], single_company_from_new_wallet[5])


def lookup_for_companies_to_sold(actual_state, single_company_from_new_wallet, wallet_name):
    new_company_for_purchase = True
    for single_company_from_actual_state in actual_state:
        if single_company_from_new_wallet[0] == single_company_from_actual_state[0]:
            new_company_for_purchase = False
            actualize_current_state(single_company_from_actual_state, single_company_from_new_wallet, wallet_name)
    return new_company_for_purchase


def actualize_current_state(single_company_from_actual_state, single_company_from_new_wallet, wallet_name):
    if int(single_company_from_new_wallet[1]) != int(single_company_from_actual_state[1]):
        counts_diff = int(single_company_from_actual_state[1]) - int(single_company_from_new_wallet[1])
        purchase_price = float(single_company_from_actual_state[2])
        sold_price = get_close_price_from_file(single_company_from_new_wallet[0])
        result = round((sold_price - purchase_price) * counts_diff, 2)
        write_to_wallet_history(wallet_name, single_company_from_actual_state[0], str(counts_diff),
                                sold_price, str(datetime.date.today()), str(result))

        if int(single_company_from_new_wallet[1]) != 0:
            write_to_wallet(wallet_name, single_company_from_new_wallet[0], single_company_from_new_wallet[1],
                            single_company_from_new_wallet[2], str(datetime.date.today()), single_company_from_new_wallet[4], single_company_from_new_wallet[5])
    else:
        write_to_wallet(wallet_name, single_company_from_new_wallet[0], single_company_from_new_wallet[1],
                        single_company_from_new_wallet[2], str(datetime.date.today()), single_company_from_new_wallet[4], single_company_from_new_wallet[5])


def actualize_root_file_for_wallet(wallet_name, root_file_list):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    actual_state = []

    with open(path_to_wallet + "root.txt", "r") as single_file:
        for line in single_file:
            single_row = [x.strip() for x in line.split(',')]
            actual_state.append(single_row)
        truncate_root_file(wallet_name)

    write_to_root_file_wallet(wallet_name, root_file_list[0], root_file_list[1], root_file_list[2])


def truncate_wallet_file(wallet_name):
    path_to_wallet = create_subfolder_for_wallets(wallet_name)
    with open(path_to_wallet + "wallet.txt", "a") as wallet:
        wallet.truncate()
        wallet.write("Company Name, Counts, Purchase price, Datetime")


def truncate_root_file(wallet_name):
    path_to_wallet = create_subfolder_for_wallets(wallet_name)
    with open(path_to_wallet + "root.txt", "a") as wallet:
        wallet.truncate()
        wallet.write("Starting funds, Current funds, Free funds")


def open_wallet(wallet_name):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    actual_state = []

    with open(path_to_wallet + "wallet.txt", "r") as single_file:
        for line in single_file:
            single_row = [x.strip() for x in line.split(',')]
            actual_state.append(single_row)

    actual_state.pop(0)
    return actual_state


def open_wallets():
    opened_wallet_list = {}

    for wallet_name in os.listdir(get_full_path_to_wallet_directory()):
        path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
        actual_wallet_state = []

        with open(path_to_wallet + "wallet.txt", "r") as single_file:
            for line in single_file:
                single_row = [x.strip() for x in line.split(',')]
                actual_wallet_state.append(single_row)

        actual_wallet_state.pop(0)
        opened_wallet_list[wallet_name] = actual_wallet_state

    return opened_wallet_list


def fetch_root_file_for_wallet(wallet_name):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    actual_state = []

    with open(path_to_wallet + "root.txt", "r") as single_file:
        for line in single_file:
            single_row = [x.strip() for x in line.split(',')]
            actual_state.append(single_row)

    actual_state.pop(0)
    return actual_state[0]
