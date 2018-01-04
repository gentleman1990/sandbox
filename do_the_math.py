#!/usr/bin/python

import sys
import traceback
from file_operations import prepare_data_for_analysis, save_typed_companies
from typing import *

ALL_COMPANY_DATA = []


def oscillators():
    print "Starting calculation for oscillators ..."
    sma30, ema15, avg_vol, ema15_day_before = calculate_oscillators(ALL_COMPANY_DATA)
    typed_by_oscillators = type_company_to_invest_by_oscillators(sma30, ema15, avg_vol, ema15_day_before)
    print "The calculations for oscillators has been completed"
    return typed_by_oscillators


def upper_trending():
    print "Starting calculation for upper trending ..."
    typed_by_upper_trending = type_company_to_invest_by_trending()
    print "The calculations for upper trending has been completed"
    return typed_by_upper_trending


def pick_up_for_invest(tbo, tbut):
    typed = list(set(tbo).intersection(tbut))
    for t in typed:
        print "Typed company: " + str(t)
        save_typed_companies(str(t))
    print "Typing has been completed"


if __name__ == '__main__':
    try:
        ALL_COMPANY_DATA = prepare_data_for_analysis()
        tbo = oscillators()
        for t in tbo:
            print "Typed company: " + str(t)
            save_typed_companies(str(t), "sma30_ema15")
        #tbut = upper_trending()
        #pick_up_for_invest(tbo, tbut)
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)