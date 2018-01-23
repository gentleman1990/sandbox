#!/usr/bin/python


def insert_into_sorted_list(company_name, current_volume, co_list):
    added = False
    if len(co_list) == 0:
        co_list.append([company_name, current_volume])
        added = True

    for index in range(0, len(co_list), 1):
        if added: break;
        volume = co_list[index][1]
        if volume < current_volume and index != 0 :
            co_list.insert(index, [company_name, current_volume])
            added = True
        elif volume < current_volume and index == 0:
            co_list.insert(0, [company_name, current_volume])
            added = True
        elif volume > current_volume and index+1 == len(co_list):
            co_list.insert(index + 1, [company_name, current_volume])
            added = True
