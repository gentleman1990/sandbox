#!/usr/bin/python

from logger import log_error_to_file
from oscillators import *

FILTERED_COMPANIES = []


def calculate_oscillators(all_company_data):
    sma30 = {}
    ema15 = {}
    avg_vol = {}
    for single_company in all_company_data:
        try:
            sma30[get_last_company_name(single_company)] = calculate_SMA(single_company, 30)
            ema15[get_last_company_name(single_company)] = calculate_EMA(single_company, 15)
            avg_vol[get_last_company_name(single_company)] = calculate_average_volume_period(single_company, 200)
            FILTERED_COMPANIES.append(single_company)
        except Exception as error:
            log_error_to_file("calculate_oscillators", ("Problem with calculation for company %s. Reason %s" % (get_last_company_name(single_company), error)))
            pass
    return sma30, ema15, avg_vol


def type_company_to_invest_by_oscillators(sma30_array, ema15_array, avg_vol_array):
    typed_companies_oscillators = []
    for sc in FILTERED_COMPANIES:
        company_name = get_last_company_name(sc)
        sma30 = sma30_array[company_name]
        ema15 = ema15_array[company_name]
        last_volume = get_last_company_volume(sc)
        if last_volume > 15000 and sma30 > ema15:
            typed_companies_oscillators.append(company_name)
#           print "Potentially company for investment: " + company_name
    return typed_companies_oscillators


def type_company_to_invest_by_trending():
    upper_trending = []
    for sc in FILTERED_COMPANIES:
        if check_upper_trending_period(sc, 100):
            upper_trending.append(get_last_company_name(sc))
#           print "Company with upper trending: " + get_last_company_name(sc)
    return upper_trending
