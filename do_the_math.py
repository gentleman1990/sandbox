#!/usr/bin/python

import sys
import traceback
from file_operations import prepare_data_for_analysis
from oscillators import *


ALL_COMPANY_DATA = []


if __name__ == '__main__':
    try:
        ALL_COMPANY_DATA = prepare_data_for_analysis()
        for single_company in ALL_COMPANY_DATA:
            try:
                print "SMA for " + get_company_name(single_company[0]) + " " + str(calculate_SMA(single_company, 15))
            except Exception as error:
                print "Problem with calculation for company %s. Reason %s" % (get_company_name(single_company[0]), error)
                pass

    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)