#!/usr/bin/python

from file_operations import get_full_path_to_log_directory
from file_operations import get_full_path_to_wallet_directory


def log_error_to_file(function, message):
    with open(get_full_path_to_log_directory() + "log.txt", "a") as log_file:
        log_file.write("Function: %s - log message: %s \r\n" % (function, message))


def write_to_wallet_history(wallet_name, company_name, counts, sold_price, datetime, result):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    with open(path_to_wallet + "wallet_history.txt", "a") as wallet_history:
        wallet_history.write(("\r\n%s,%s,%s,%s,%s")%(company_name, counts, sold_price, datetime, result))


def write_to_wallet(wallet_name, company_name, counts, purchase_price, datetime, stop_loss, take_profit):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    with open(path_to_wallet + "wallet.txt", "a") as wallet:
        wallet.write(("\r\n%s,%s,%s,%s,%s,%s") % (company_name, counts, purchase_price, datetime, stop_loss, take_profit))


def write_to_root_file_wallet(wallet_name, starting_funds, current_funds, free_funds):
    path_to_wallet = get_full_path_to_wallet_directory() + wallet_name + "/"
    with open(path_to_wallet + "root.txt", "a") as wallet_history:
        wallet_history.write(("\r\n%s,%s,%s")%(starting_funds, current_funds, free_funds))

