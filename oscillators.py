#!/usr/bin/python

from getters import *


def calculate_SMA(company_list, days):
    reversed_comapnies_list = get_reverse_list(company_list)
    close_price = 0
    for single_day in range(0, days, 1):
        close_price += get_company_close_price(reversed_comapnies_list[single_day])
    return round(close_price / days, 2)


def calculate_SMA_past(comapny_list, days, days_past_since_now):
    comapny_list_with_deleted_items = comapny_list[:-days_past_since_now]
    reversed_list = get_reverse_list(comapny_list_with_deleted_items)
    close_price = 0
    for single_day in range(0, days, 1):
        close_price += get_company_close_price(reversed_list[single_day])
    return round(close_price / days, 2)


def calculate_EMA(comapny_list, days):
    reversed_list = get_reverse_list(comapny_list)
    multiplier = 2/float(days+1)
    ema_previous_value = 0.0
    for day in range(days-1, -1, -1):
        if ema_previous_value == 0.0:
            ema_previous_value = calculate_SMA_past(comapny_list, days, days-2)
        close_price = get_company_close_price(reversed_list[day])
        actual_ema = close_price*multiplier + ema_previous_value*(1-multiplier)
        ema_previous_value = actual_ema
    return actual_ema


def calculate_EMA_past(comapny_list, days, days_past_since_now):
    comapny_list_with_deleted_items = comapny_list[:-days_past_since_now]
    reversed_list = get_reverse_list(comapny_list_with_deleted_items)
    multiplier = 2/float(days+1)
    ema_previous_value = 0.0
    for day in range(days-1, -1, -1):
        if ema_previous_value == 0.0:
            ema_previous_value = calculate_SMA_past(comapny_list, days, days-2)
        close_price = get_company_close_price(reversed_list[day])
        actual_ema = close_price*multiplier + ema_previous_value*(1-multiplier)
        ema_previous_value = actual_ema
    return actual_ema



def calculate_average_volume(comapny_list):
    volume = 0
    for single_day in range(0, len(comapny_list), 1):
        volume += get_company_volume(comapny_list[single_day])
    return volume / len(comapny_list)


def calculate_average_volume_period(comapny_list, days):
    reversed_list = get_reverse_list(comapny_list)
    volume = 0
    for single_day in range(0, days, 1):
        volume += get_company_volume(reversed_list[single_day])
    return volume / days


def check_upper_trending_period(comapny_list, days):
    reversed_list = get_reverse_list(comapny_list)
    close_price_now = get_company_close_price(reversed_list[0])
    close_price_middle_past = get_company_close_price(reversed_list[days/2])
    close_price_past = get_company_close_price(reversed_list[days])
    if close_price_past < close_price_middle_past < close_price_now:
        return True
    else:
        return False




