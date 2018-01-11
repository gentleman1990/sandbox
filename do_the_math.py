#!/usr/bin/python

import sys
import traceback
import copy
from file_operations import prepare_data_for_analysis, save_typed_companies, parse_stock_exchange_data
from typing import *


def oscillators(all_company_data_list):
    print "Starting calculation for oscillators ..."
    filtered_companies, sma30, ema15, avg_vol, ema15_day_before = calculate_oscillators(all_company_data_list)
    typed_by_oscillators = type_company_to_invest_by_oscillators(filtered_companies, sma30, ema15, avg_vol, ema15_day_before)
    print "The calculations for oscillators has been completed"
    return typed_by_oscillators


# def upper_trending():
#     print "Starting calculation for upper trending ..."
#     typed_by_upper_trending = type_company_to_invest_by_trending()
#     print "The calculations for upper trending has been completed"
#     return typed_by_upper_trending


def pick_up_for_invest(tbo, tbut):
    typed = list(set(tbo).intersection(tbut))
    for t in typed:
        print "Typed company: " + str(t)
        save_typed_companies(str(t))
    print "Typing has been completed"


def simulate_in_the_past(number_of_days):
    for index in range(number_of_days, 0, -1):
        company_data = parse_stock_exchange_data()
        excluded_companies = 0
        companies_to_analysis = []
        data_in_the_past = company_data[0][-index-1][1]
        print "Analysis for date " + data_in_the_past
        for single_company in company_data:
            try:
                del single_company[-index:-1]
                del single_company[-1]
                current_date = single_company[-1][1]
                if current_date != data_in_the_past:
                    excluded_companies += 1
                else:
                    companies_to_analysis.append(single_company)
#                    print "Different data than first one => current: %s and reference %s for company %s" %(current_date, data_in_the_past, single_company[0])
            except Exception:
                #print "Problem with moving past with company ! Removing it from further analysis!"
                excluded_companies += 1
        print "Excluded companies: " + str(excluded_companies)
        tbo = oscillators(companies_to_analysis)
        for t in tbo:
            print "Typed company: " + str(t)

            #save_typed_companies(str(t), "sma30_ema15")

if __name__ == '__main__':
    try:
        # prepare_data_for_analysis()
        all_company_data = parse_stock_exchange_data()

        #calculate_last_date()
        simulate_in_the_past(100)

    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)