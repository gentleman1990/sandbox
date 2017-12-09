#!/usr/bin/python

import urllib
import shutil
import os
import zipfile
import time

URL_FOR_STOCK_QUOTES = "http://bossa.pl/pub/ciagle/omega/"
ZIP_FILE_NAME = "omegacgl.zip"
FULL_PATH_TO_SOURCE = os.path.dirname(os.path.realpath(__file__)) + "/source/"


def fetch_last_data_file():
    print "Fetching data ..."
    url_opener = urllib.URLopener()
    url_opener.retrieve(URL_FOR_STOCK_QUOTES + ZIP_FILE_NAME, ZIP_FILE_NAME)
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


def parse_stock_exchange_data():
    start_time = time.time()
    all_company_data = []
    print "Parsing and preparing data please wait ..."
    for filename in os.listdir(FULL_PATH_TO_SOURCE):
        with open(FULL_PATH_TO_SOURCE + filename, "r") as single_file:
            SINGLE_COMPANY_ARRAY = []
            for line in single_file:
                single_row = [x.strip() for x in line.split(',')]

                if(single_row[0] != "Name"):
                    SINGLE_COMPANY_ARRAY.append(single_row)

            all_company_data.append(SINGLE_COMPANY_ARRAY)
    print "Parsing and preparing data finished - it takes " + "{0:.2f}".format(float(time.time() - start_time)) + " seconds"
    return all_company_data


def prepare_data_for_analysis():
    #fetch_last_data_file()
    #create_directory_and_unzip_file()
    return parse_stock_exchange_data()
