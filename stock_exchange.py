#!/usr/bin/python

import sys
import traceback
import urllib
import shutil
import os

URL_FOR_STOCK_QUOTES = "http://bossa.pl/pub/ciagle/omega/"
ZIP_FILE_NAME = "omegacgl.zip"
FULL_PATH_TO_SOURCE = os.path.dirname(os.path.realpath(__file__)) + "/source/"


def fetch_last_data_file():

    print "Fetching data ..."
    url_opener = urllib.URLopener()
    url_opener.retrieve(URL_FOR_STOCK_QUOTES + ZIP_FILE_NAME, ZIP_FILE_NAME)
    print "Fetch completed"


def create_directory_and_unzip_file():
    if not os.path.exists(FULL_PATH_TO_SOURCE):
        os.makedirs(FULL_PATH_TO_SOURCE)
    shutil.move(ZIP_FILE_NAME, FULL_PATH_TO_SOURCE + ZIP_FILE_NAME)

if __name__ == '__main__':
    try:
        #fetch_last_data_file()
        create_directory_and_unzip_file()
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)