#!/usr/bin/python

import os

from file_operations import create_subfolder_for_wallets
from file_operations import get_full_path_to_wallet_directory
from logger import log_error_to_file

WALLET_HEADER = "Company Name, Counts, Purchase price, Datetime, Stop Loss, Take profit"
ROOT_HEADER = "Starting funds, Current funds, Free funds\r\n"
WALLET_HISTORY_HEADER = "Company Name, Counts, Sold price, Datetime, Result"


def create_new_wallet(wallet_name, starting_funds):
    if not os.path.exists(get_full_path_to_wallet_directory() + wallet_name):
        path_to_wallet = create_subfolder_for_wallets(wallet_name)
        with open(path_to_wallet + "root.txt", "a") as root:
            root.write(ROOT_HEADER)
            root.write(str(starting_funds) + ", " + str(starting_funds) + ", " + str(starting_funds))
        with open(path_to_wallet + "wallet.txt", "a") as wallet:
            wallet.write(WALLET_HEADER)
        with open(path_to_wallet + "wallet_history.txt", "a") as wallet_history:
            wallet_history.write(WALLET_HISTORY_HEADER)
    else:
        log_error_to_file("create_new_wallet", "Wallet has been already created!")


def truncate_wallet_file(wallet_name):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    with open(path_to_wallet + "wallet.txt", "r+") as wallet:
        wallet.truncate()
        wallet.write(WALLET_HEADER)


def open_wallet(wallet_name):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    actual_state = []

    with open(path_to_wallet + "wallet.txt", "r") as single_file:
        for line in single_file:
            single_row = [x.strip() for x in line.replace("[", "").replace("]", "").replace("'", "").split(',')]
            actual_state.append(single_row)

    actual_state.pop(0)
    return actual_state


def save_wallet(wallet_name, wallet_list):
    truncate_wallet_file(wallet_name)
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    wallet_file = open(path_to_wallet + "wallet.txt", "a")
    for sc in wallet_list:
        wallet_file.write("\r\n%s" % sc)


def fetch_root_file_for_wallet(wallet_name):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    actual_state = []

    with open(path_to_wallet + "root.txt", "r") as single_file:
        for line in single_file:
            single_row = [x.strip() for x in line.split(',')]
            actual_state.append(single_row)

    actual_state.pop(0)
    return actual_state[0]
