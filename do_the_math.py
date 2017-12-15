#!/usr/bin/python

import sys
import traceback
from file_operations import prepare_data_for_analysis
from oscillators import *


ALL_COMPANY_DATA = []
SMA15 = {}
EMA30 = {}
AVG_VOLUME = {}

if __name__ == '__main__':
    try:
        ALL_COMPANY_DATA = prepare_data_for_analysis()
        print "Starting analysis ..."
        for single_company in ALL_COMPANY_DATA:
            try:
                SMA15[get_last_company_name(single_company)] = calculate_SMA(single_company, 15)
                EMA30[get_last_company_name(single_company)] = calculate_EMA(single_company, 30)
                AVG_VOLUME[get_last_company_name(single_company)] = calculate_average_volume_period(single_company, 200)
                print get_last_company_name(single_company) + \
                      ": SMA15 - " + str(SMA15[get_last_company_name(single_company)]) + \
                      " | EMA30 - " + str(EMA30[get_last_company_name(single_company)]) + \
                      " | AVG VOLUME 200 - " + str(AVG_VOLUME[get_last_company_name(single_company)])

            except Exception as error:
                print "Problem with calculation for company %s. Reason %s" % (get_last_company_name(single_company), error)
                pass

        print "The analysis has been completed"
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)