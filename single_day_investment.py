#!/usr/bin/python

import sys
import traceback

from parsing_and_preparing_data import calculate_last_day_for
from file_operations import prepare_data_for_analysis, parse_stock_exchange_data
from transactions import analyze_for_buying, analyze_for_selling
from transactions import fetch_all_typed_company
from wallet import create_new_wallet
from statistics import prepare_statistics

if __name__ == '__main__':
    try:
        prepare_data_for_analysis()
        source_data = parse_stock_exchange_data()
        calculate_last_day_for(source_data)

        create_new_wallet("test")
        all_typed_companies = fetch_all_typed_company("sma30_ema15")

        analyze_for_buying("test", all_typed_companies, source_data)
        analyze_for_selling("test", source_data)
        prepare_statistics("test", source_data)

    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)
