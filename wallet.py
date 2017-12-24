#!/usr/bin/python

from file_operations import create_subfolder_for_wallets


#WALLET = [COMPANY_NAME, COUNTS, PURCHASE_PRICE]


def create_new_wallet(wallet_name, starting_funds):
    path_to_wallet = create_subfolder_for_wallets(wallet_name)
    with open(path_to_wallet + "root.txt", "a") as root:
        root.write(starting_funds)
    with open(path_to_wallet + "wallet.txt", "a") as wallet:
        wallet.write("Company Name, Counts, Purchase price, Datetime")
    with open(path_to_wallet + "wallet_history.txt", "a") as wallet_history:
        wallet_history.write("Company Name, Counts, Sold price, Datetime, Result")


def load_wallets():
    print ""


