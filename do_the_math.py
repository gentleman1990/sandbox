#!/usr/bin/python

import sys
import traceback
from file_operations import prepare_data_for_analysis

ALL_COMPANY_DATA = []

if __name__ == '__main__':
    try:
        ALL_COMPANY_DATA = prepare_data_for_analysis()
        print ""
    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)