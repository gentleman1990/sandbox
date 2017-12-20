#!/usr/bin/python

from getters import *


def calculate_SMA(array_company, days):
    reversed_array = get_reverse_array(array_company)
    close_price = 0
    for single_day in range(0, days, 1):
        close_price += get_company_close_price(reversed_array[single_day])
    return round(close_price / days, 2)


def calculate_EMA(array_company, days):
    ema_array_from_oldest = prepare_EMA_array(array_company, days)
    return ema_array_from_oldest[len(array_company)-1]


def prepare_EMA_array(array_company, days):
    ema_array = {}
    index = days - 1
    for single_day in range(index, len(array_company), 1):
        close_price = get_company_close_price(array_company[single_day])
        multiplier = round(2/float(index), 2)
        if single_day == index:
            ema_array[index] = calculate_SMA(array_company, days)
            continue
        else:
            ema_day_before = ema_array[single_day - 1]
        ema_array[single_day] = round((close_price - ema_day_before)*multiplier + ema_day_before, 2)
    return ema_array


def calculate_average_volume(array_company):
    volume = 0
    for single_day in range(0, len(array_company), 1):
        volume += get_company_volume(array_company[single_day])
    return volume / len(array_company)


def calculate_average_volume_period(array_company, days):
    reversed_array = get_reverse_array(array_company)
    volume = 0
    for single_day in range(0, days, 1):
        volume += get_company_volume(reversed_array[single_day])
    return volume / days


def check_upper_trending_period(array_company, days):
    reversed_array = get_reverse_array(array_company)
    close_price_now = get_company_close_price(reversed_array[0])
    close_price_middle_past = get_company_close_price(reversed_array[days/2])
    close_price_past = get_company_close_price(reversed_array[days])
    if close_price_past < close_price_middle_past < close_price_now:
        return True
    else:
        return False




