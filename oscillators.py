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
    ema_sum = 0
    weight_sum = 0
    for single_day in range(0, days, 1):
        close_price = get_company_close_price(reversed_array[single_day])
        ema_sum += close_price * (days - single_day)
        weight_sum += (days-single_day)
    return ema_sum/weight_sum


def calculate_average_volume(array_company):
    volume = 0
    for single_day in range(0, len(array_company), 1):
        volume += get_company_volume(array_company)
    return volume/len(array_company)


def calculate_average_volume_period(array_company, days):
    reversed_array = get_reverse_array(array_company)
    volume = 0
    for single_day in range(0, days, 1):
        volume += get_company_volume(reversed_array)
    return volume/days
