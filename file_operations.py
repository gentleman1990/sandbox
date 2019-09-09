#!/usr/bin/python

import shutil
import os
import zipfile
import time
import datetime
import requests
from getters import get_last_company_name

URL_FOR_STOCK_QUOTES = "http://bossa.pl/pub/ciagle/omega/"
ZIP_FILE_NAME = "omegacgl.zip"
FULL_PATH_TO_SOURCE = os.path.dirname(os.path.realpath(__file__)) + "/source/"
FULL_PATH_TO_LOG = os.path.dirname(os.path.realpath(__file__)) + "/logs/"
FULL_PATH_TO_TYPING = os.path.dirname(os.path.realpath(__file__)) + "/typing/"
FULL_PATH_TO_WALLETS = os.path.dirname(os.path.realpath(__file__)) + "/wallets/"


def fetch_last_data_file():
    print "Fetching data ..."
    r = requests.get(URL_FOR_STOCK_QUOTES + ZIP_FILE_NAME, allow_redirects=True)
    open(ZIP_FILE_NAME, 'wb').write(r.content)
    print "Fetch completed"

def unzip():
    print "Unzipping files ..."
    zip_ref = zipfile.ZipFile(FULL_PATH_TO_SOURCE + ZIP_FILE_NAME, 'r')
    zip_ref.extractall(FULL_PATH_TO_SOURCE)
    zip_ref.close()
    print "Unzipping completed"


def create_directory_and_unzip_file():
    if not os.path.exists(FULL_PATH_TO_SOURCE):
        os.makedirs(FULL_PATH_TO_SOURCE)
    shutil.move(ZIP_FILE_NAME, FULL_PATH_TO_SOURCE + ZIP_FILE_NAME)
    unzip()
    os.remove(FULL_PATH_TO_SOURCE + ZIP_FILE_NAME)

    if not os.path.exists(FULL_PATH_TO_LOG):
        os.makedirs(FULL_PATH_TO_LOG)

    if not os.path.exists(FULL_PATH_TO_TYPING):
        os.makedirs(FULL_PATH_TO_TYPING)

    if not os.path.exists(FULL_PATH_TO_WALLETS):
        os.makedirs(FULL_PATH_TO_WALLETS)


def parse_stock_exchange_data():
    start_time = time.time()
    all_company_data = []
    print "Parsing and preparing data please wait ..."
    for filename in os.listdir(FULL_PATH_TO_SOURCE):
        with open(FULL_PATH_TO_SOURCE + filename, "r") as single_file:
            single_company_list = []
            for line in single_file:
                single_row = [x.strip() for x in line.split(',')]

                if single_row[0] != "Name":
                    single_company_list.append(single_row)

            all_company_data.append(single_company_list)
    print "Parsing and preparing data finished - it takes " + "{0:.2f}".format(float(time.time() - start_time)) + " seconds"
    filtered = remove_uncorrected_companies(all_company_data)
    return filtered


def remove_uncorrected_companies(all_company_data):
    filtered_all_company_data = []
    for single_company in all_company_data:
        company_name = get_last_company_name(single_company)
        if not(company_name.startswith("INT") \
                or company_name.startswith("RC") or company_name.startswith("UCEX") \
                or company_name.startswith("BPH") or company_name.startswith("DB")
               or company_name.startswith("WIG") or company_name.startswith("KBC")
               or company_name.startswith("TRIG") or company_name.startswith("ETF")):
            filtered_all_company_data.append(single_company)
    return filtered_all_company_data


def save_typed_companies(companies_list, algorithm_name):
    filename = str(datetime.date.today())
    with open(FULL_PATH_TO_TYPING + filename + "_" + algorithm_name + ".txt", "w") as typing_file:
        typing_file.truncate()
        typing_file.close()
    for sc in companies_list:
        print "Typed company: " + str(sc)
        with open(FULL_PATH_TO_TYPING + filename + "_" + algorithm_name + ".txt", "a") as typing_file:
            typing_file.write(sc + "\r\n")


def save_typed_companies_for_simulator(companies_list, algorithm_name):
    with open(FULL_PATH_TO_TYPING + "simulator_" + algorithm_name + ".txt", "w") as typing_file:
        typing_file.truncate()
        typing_file.close()
    for sc in companies_list:
        print "Typed company: " + str(sc)
        with open(FULL_PATH_TO_TYPING + "simulator_" + algorithm_name + ".txt", "a") as typing_file:
            typing_file.write(sc + "\r\n")


def prepare_data_for_analysis():
    fetch_last_data_file()
    create_directory_and_unzip_file()


def create_subfolder_for_wallets(wallet_name):
    path_to_specific_wallet = FULL_PATH_TO_WALLETS + wallet_name + "/"
    if not os.path.exists(path_to_specific_wallet):
        os.makedirs(path_to_specific_wallet)
    return path_to_specific_wallet


def get_full_path_to_wallet_directory():
    return FULL_PATH_TO_WALLETS


def get_full_path_to_log_directory():
    return FULL_PATH_TO_LOG
