#!/usr/bin/python


def get_company_name(single_company_row):
    return single_company_row[0]


def get_company_date(single_company_row):
    return single_company_row[1]


def get_company_open_price(single_company_row):
    return float(single_company_row[2])


def get_company_high_price(single_company_row):
    return float(single_company_row[3])


def get_company_low_price(single_company_row):
    return float(single_company_row[4])


def get_company_close_price(single_company_row):
    return float(single_company_row[5])


def get_company_volume(single_company_row):
    return int(single_company_row[6])


def get_reverse_array(single_array_company):
    reversed_array = []
    iterator = reversed(single_array_company)
    while iterator.__length_hint__() > 0:
        reversed_array.append(iterator.next())

    return reversed_array


def get_last_company_name(single_company_row):
    return single_company_row[len(single_company_row)-1][0]


def get_last_company_date(single_company_row):
    return single_company_row[len(single_company_row)-1][1]


def get_last_company_open_price(single_company_row):
    return float(single_company_row[len(single_company_row)-1][2])


def get_last_company_high_price(single_company_row):
    return float(single_company_row[len(single_company_row)-1][3])


def get_last_company_low_price(single_company_row):
    return float(single_company_row[len(single_company_row)-1][4])


def get_last_company_close_price(single_company_row):
    return float(single_company_row[len(single_company_row)-1][5])


def get_last_company_volume(single_company_row):
    return int(single_company_row[len(single_company_row)][6])
