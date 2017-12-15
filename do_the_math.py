#!/usr/bin/python

import sys
import traceback
from file_operations import prepare_data_for_analysis
from oscillators import *

ALL_COMPANY_DATA = []
FILTERED_COMPANY_DATA = []
SMA30 = {}
EMA15 = {}
AVG_VOLUME = {}
TYPED_COMPANIES = []


def type_company_to_invest():
    for sc in FILTERED_COMPANY_DATA:
        company_name = get_last_company_name(sc)
        sma30 = SMA30[company_name]
        ema15 = EMA15[company_name]
        last_volume = get_last_company_volume(sc)
        if last_volume > 10000 and sma30 > ema15:
            TYPED_COMPANIES.append(company_name)
            print "Potentially company for investment: " + company_name


if __name__ == '__main__':
    try:
        ALL_COMPANY_DATA = prepare_data_for_analysis()
        print "Starting calculation for osillators ..."
        for single_company in ALL_COMPANY_DATA:
            try:
                SMA30[get_last_company_name(single_company)] = calculate_SMA(single_company, 30)
                EMA15[get_last_company_name(single_company)] = calculate_EMA(single_company, 15)
                AVG_VOLUME[get_last_company_name(single_company)] = calculate_average_volume_period(single_company, 200)
                FILTERED_COMPANY_DATA.append(single_company)
            except Exception as error:
                print "Problem with calculation for company %s. Reason %s" % (get_last_company_name(single_company), error)
                pass

        print "The calculations for oscillators has been completed\nStarting typing ..."
        type_company_to_invest()
        print "Typing has been completed"
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)