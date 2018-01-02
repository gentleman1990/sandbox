#!/usr/bin/python

from getters import *


def calculate_SMA(array_company, days):
    reversed_array = get_reverse_array(array_company)
    close_price = 0
    for single_day in range(0, days, 1):
        close_price += get_company_close_price(reversed_array[single_day])
    return round(close_price / days, 2)


def calculate_SMA_past(array_company, days, days_past_since_now):
    array_company_with_deleted_items = array_company[:-days_past_since_now]
    reversed_array = get_reverse_array(array_company_with_deleted_items)
    close_price = 0
    for single_day in range(0, days, 1):
        close_price += get_company_close_price(reversed_array[single_day])
    return round(close_price / days, 2)


def calculate_EMA(array_company, days):
    reversed_array = get_reverse_array(array_company)
    multiplier = 2/float(days+1)
    ema_previous_value = 0.0
    for day in range(days-1, -1, -1):
        if ema_previous_value == 0.0:
            ema_previous_value = calculate_SMA_past(array_company, days, days-2)
        close_price = get_company_close_price(reversed_array[day])
        actual_ema = close_price*multiplier + ema_previous_value*(1-multiplier)
        ema_previous_value = actual_ema
    return actual_ema


def calculate_EMA_past(array_company, days, days_past_since_now):
    array_company_with_deleted_items = array_company[:-days_past_since_now]
    reversed_array = get_reverse_array(array_company_with_deleted_items)
    multiplier = 2/float(days+1)
    ema_previous_value = 0.0
    for day in range(days-1, -1, -1):
        if ema_previous_value == 0.0:
            ema_previous_value = calculate_SMA_past(array_company, days, days-2)
        close_price = get_company_close_price(reversed_array[day])
        actual_ema = close_price*multiplier + ema_previous_value*(1-multiplier)
        ema_previous_value = actual_ema
    return actual_ema



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




