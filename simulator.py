#!/usr/bin/python

import traceback
from transactions import *
from file_operations import *
from parsing_and_preparing_data import oscillators


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
                #   print "Different data than first one => current: %s and reference %s for company %s" %(current_date, data_in_the_past, single_company[0])
            except Exception:
                #print "Problem with moving past with company ! Removing it from further analysis!"
                excluded_companies += 1
        print "Excluded companies: " + str(excluded_companies)
        tbo = oscillators(companies_to_analysis)
        save_typed_companies_for_simulator(tbo, "sma30_ema15")
        #buy_and_sell(companies_to_analysis)


if __name__ == '__main__':
    try:
        create_new_wallet("simulator", 10000)
        simulate_in_the_past(100)


    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)