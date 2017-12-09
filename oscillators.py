#!/usr/bin/python

from getters import *


def calculate_SMA(array_company, days):
    reversed_array = reversed[array_company]
    close_price = 0
    for single_day in range(0, days, 1):
        close_price+= get_company_close_price(reversed_array[single_day-1])
    return close_price/days


def calculate_EMA(array_company, days):
    reversed_array = reversed[array_company]
    ema_sum = 0
    weight_sum = 0
    for single_day in range(0, days, 1):
        close_price = get_company_close_price(reversed_array[single_day-1])
        ema_sum += close_price * (days - single_day)
        weight_sum += (days-single_day)
    return ema_sum/weight_sum
