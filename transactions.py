#!/usr/bin/python

import datetime
import traceback
import sys
from file_operations import get_close_price_from_file
from file_operations import FULL_PATH_TO_TYPING
from logger import log_error_to_file
from wallet import *

TYPED_COMPANIES = []


def buy(company_name, how_many, wallet):
    close_price_from_file = get_close_price_from_file(company_name)
    if not wallet:
        wallet.append([company_name, how_many, close_price_from_file * how_many, str(datetime.date.today())])
        print "Shares for company %s bought in value %s" % (company_name, str(how_many))
    elif already_in_wallet(company_name, wallet):
        print "Company already in wallet - you can't buy more"
    else:
        wallet.append([company_name, how_many, close_price_from_file * how_many, str(datetime.date.today())])
        print "Shares for company %s bought in value %s" % (company_name, str(how_many))


def sell(company_name, how_many, wallet):
    for single_company in wallet:
        if single_company[0] == company_name:
            single_company[1] = single_company[1] - how_many
            print "Shares for company %s sold in value %s" % (company_name, str(how_many))
        if single_company[1] == 0:
            wallet.remove(single_company)
            print "Shares for company %s sold in value %s" % (company_name, str(how_many))


def fetch_all_typed_company():
    filename = str(datetime.date.today())
    try:
        with open(FULL_PATH_TO_TYPING + filename + ".txt") as f:
            for company_name in f:
                TYPED_COMPANIES.append(company_name.rstrip())
    except Exception as err:
        log_error_to_file("fetch_all_typed_company", "There isn't any typed company")


def already_in_wallet(company_name, wallet):
    for single_company in wallet:
        if single_company[0] == company_name:
            return True
    return False

if __name__ == '__main__':
    try:
        wallet1 = []
        fetch_all_typed_company()
        create_new_wallet("test", 10000)
        buy(TYPED_COMPANIES[0], 10, wallet1)
        buy(TYPED_COMPANIES[1], 10, wallet1)
        sell(TYPED_COMPANIES[0], 5, wallet1)
        actualize_wallet("test", wallet1)
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)