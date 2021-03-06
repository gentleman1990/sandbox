#!/usr/bin/python

import time
from file_operations import save_typed_companies
from typing import *


def oscillators(all_company_data_list):
    start_time = time.time()
    print "Starting calculation for oscillators ..."
    filtered_companies, sma30, ema15, avg_vol, ema15_day_before = calculate_oscillators(all_company_data_list)
    typed_by_oscillators = type_company_to_invest_by_oscillators(filtered_companies, sma30, ema15, avg_vol, ema15_day_before)
    print "The calculations for oscillators has been completed - it takes " + "{0:.2f}".format(float(time.time() - start_time)) + " seconds"
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


def calculate_last_day_for(all_company_data):
    tbo = oscillators(all_company_data)
    save_typed_companies(tbo, "sma30_ema15")