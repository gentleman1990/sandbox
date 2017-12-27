#!/usr/bin/python

import os

from file_operations import create_subfolder_for_wallets
from file_operations import get_full_path_to_wallet_directory
from logger import log_error_to_file


def create_new_wallet(wallet_name, starting_funds):
    if not os.path.exists(get_full_path_to_wallet_directory() + wallet_name):
        path_to_wallet = create_subfolder_for_wallets(wallet_name)
        with open(path_to_wallet + "root.txt", "a") as root:
            root.write(str(starting_funds))
        with open(path_to_wallet + "wallet.txt", "a") as wallet:
            wallet.write("Company Name, Counts, Purchase price, Datetime")
        with open(path_to_wallet + "wallet_history.txt", "a") as wallet_history:
            wallet_history.write("Company Name, Counts, Sold price, Datetime, Result")
    else:
        log_error_to_file("create_new_wallet", "Wallet has been already created!")


def actualize_wallet(wallet_name, wallet_array):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    actual_state = []

    with open(path_to_wallet + "wallet.txt", "r") as single_file:
        for line in single_file:
            single_row = [x.strip() for x in line.split(',')]
            actual_state.append(single_row)

    print ""


