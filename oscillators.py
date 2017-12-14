#!/usr/bin/python

from getters import *


def calculate_SMA(array_company, days):
    reversed_array = get_reverse_array(array_company)
    close_price = 0
    for single_day in range(0, days, 1):
        close_price += get_company_close_price(reversed_array[single_day])
    return close_price/days


def calculate_EMA(array_company, days):
    reversed_array = get_reverse_array(array_company)
    ema_array = prepare_EMA_array(reversed_array, days)
    return ema_array[days-1]


def prepare_EMA_array(reverse_array_company, days):
    ema_array = []
    for single_day in range(0, days, 1):
        close_price = get_company_close_price(reverse_array_company[days-1])
        a_ratio = 2/float((days+1))
        if single_day != 0:
            base = 0
        else:
            base = (1 - a_ratio)*ema_array[single_day-1]
        ema_array[single_day] = close_price*a_ratio + base
    return ema_array


# def calculate_EMA(array_company, days):
#     reversed_array = get_reverse_array(array_company)
#     ema_sum = 0
#     weight_sum = 0
#     for single_day in range(1, days+1, 1):
#         a = 2/float((single_day+1))
#         base = (pow((1 - a), single_day))
#         close_price = get_company_close_price(reversed_array[single_day-1])
#         ema_sum += (base * close_price)
#         weight_sum += base
#     return ema_sum / weight_sum


def calculate_average_volume(array_company):
    volume = 0
    for single_day in range(0, len(array_company), 1):
        volume += get_company_volume(array_company[single_day])
    return volume/len(array_company)


def calculate_average_volume_period(array_company, days):
    reversed_array = get_reverse_array(array_company)
    volume = 0
    for single_day in range(0, days, 1):
        volume += get_company_volume(reversed_array[single_day])
    return volume/days
