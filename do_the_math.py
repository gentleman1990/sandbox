#!/usr/bin/python

import sys
import traceback
from file_operations import prepare_data_for_analysis
from oscillators import *
from logger import log_error_to_file

ALL_COMPANY_DATA = []
FILTERED_COMPANY_DATA = []
SMA30 = {}
EMA15 = {}
AVG_VOLUME = {}
UPPER_TRENDING = []
TYPED_COMPANIES_OSCILLATORS = []


def calculate_oscillators():
    for single_company in ALL_COMPANY_DATA:
        try:
            SMA30[get_last_company_name(single_company)] = calculate_SMA(single_company, 30)
            EMA15[get_last_company_name(single_company)] = calculate_EMA(single_company, 15)
            AVG_VOLUME[get_last_company_name(single_company)] = calculate_average_volume_period(single_company, 200)
            FILTERED_COMPANY_DATA.append(single_company)
        except Exception as error:
            log_error_to_file("calculate_oscillators", ("Problem with calculation for company %s. Reason %s" % (get_last_company_name(single_company), error)))
            pass


def type_company_to_invest_by_oscillators():
    for sc in FILTERED_COMPANY_DATA:
        company_name = get_last_company_name(sc)
        sma30 = SMA30[company_name]
        ema15 = EMA15[company_name]
        last_volume = get_last_company_volume(sc)
        if last_volume > 15000 and sma30 > ema15:
            TYPED_COMPANIES_OSCILLATORS.append(company_name)
            #print "Potentially company for investment: " + company_name


def type_company_to_invest_by_trending():
    for sc in FILTERED_COMPANY_DATA:
        if check_upper_trending_period(sc, 200):
            UPPER_TRENDING.append(get_last_company_name(sc))
            #print "Company with upper trending: " + get_last_company_name(sc)

if __name__ == '__main__':
    try:
        ALL_COMPANY_DATA = prepare_data_for_analysis()
        print "Starting calculation for osillators ..."
        calculate_oscillators()
        print "The calculations for oscillators has been completed"
        print "Starting typing ..."
        type_company_to_invest_by_oscillators()
        type_company_to_invest_by_trending()
        typed = list(set(UPPER_TRENDING).intersection(TYPED_COMPANIES_OSCILLATORS))
        for t in typed:
            print "Typed company: " + str(t)
        print "Typing has been completed"
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)