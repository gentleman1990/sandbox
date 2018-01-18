#!/usr/bin/python

from transactions import *
from file_operations import *
from do_the_math import oscillators


def simulate_in_the_past(number_of_days):
    for index in range(number_of_days, 0, -1):
        company_data = parse_stock_exchange_data()
        excluded_companies = 0
        companies_to_analysis = []
        data_in_the_past = company_data[0][-index-1][1]
        print "Analysis for date " + data_in_the_past
        for single_company in company_data:
            try:
                del single_company[-index:-1]
                del single_company[-1]
                current_date = single_company[-1][1]
                if current_date != data_in_the_past:
                    excluded_companies += 1
                else:
                    companies_to_analysis.append(single_company)
                #   print "Different data than first one => current: %s and reference %s for company %s" %(current_date, data_in_the_past, single_company[0])
            except Exception:
                #print "Problem with moving past with company ! Removing it from further analysis!"
                excluded_companies += 1
        print "Excluded companies: " + str(excluded_companies)
        tbo = oscillators(companies_to_analysis)
        save_typed_companies_for_simulator(tbo, "sma30_ema15")
        #buy_and_sell(companies_to_analysis)


def buy_and_sell(source_companies_data):
    atc = fetch_all_typed_company_for_simulator("sma30_ema15")
    if atc:
        check_for_selling_for_simulator("simulator", source_companies_data)
        check_for_buying_for_simulator("simulator", atc, source_companies_data)

        #poprawic get_close_price_from file dla buying i selling


def get_close_price_from_companies_list(companies_list, company_name):
    for sc in companies_list:
        if sc[-1][0] == company_name:
            return sc[-1][5]


def check_for_selling_for_simulator(wallet_name, source_companies_data):
    # Structure for single company [sc] in wallet you can find in wallet.create_new_wallet()
    # sc[0] - Company name   | sc[1] - Counts
    # sc[2] - Purchase price | sc[3] - Datetime
    # sc[4] - Stop Loss      | sc[5] - Take profit

    opened_wallet = open_wallet(wallet_name)

    root_wallet = fetch_root_file_for_wallet(wallet_name)
    starting_funds = float(root_wallet[0])
    wallet_funds = float(root_wallet[1])
    wallet_free_funds = float(root_wallet[2])

    for sc in opened_wallet:
        close_price = float(get_close_price_from_companies_list(source_companies_data, sc[0]))
        count = int(sc[1])
        stop_loss = float(sc[4])
        take_profit = float(sc[5])
        purchase_price = float(sc[2])

        if close_price < stop_loss:
            sell(sc, sc[0], sc[1])
            actualize_wallet(wallet_name, opened_wallet)

            wallet_funds += ((close_price - purchase_price) * count)
            wallet_free_funds += (close_price * count)
            actualize_root_file_for_wallet(wallet_name, [starting_funds, wallet_funds, wallet_free_funds])
        elif close_price > take_profit:
            current_percentage_profit = (take_profit * 100 / purchase_price)
            sc[4] = round(float(sc[2]) * (float(current_percentage_profit - 2.5) / 100), 2)
            new_take_profit = round(float(sc[2]) * (float(current_percentage_profit + 5) / 100), 2)
            sc[5] = new_take_profit
            actualize_wallet(wallet_name, opened_wallet)


def check_for_buying_for_simulator(wallet_name, typed_companies_list, source_data):
    # Structure for single company [sc] in wallet you can find in wallet.create_new_wallet()
    # sc[0] - Company name   | sc[1] - Counts
    # sc[2] - Purchase price | sc[3] - Datetime
    # sc[4] - Stop Loss      | sc[5] - Take profit

    opened_wallet = open_wallet(wallet_name)
    cleared_typed_companies_list = remove_companies_already_in_wallet(opened_wallet, typed_companies_list)
    root_file_for_wallet = fetch_root_file_for_wallet(wallet_name)
    starting_funds = float(root_file_for_wallet[0])
    wallet_funds = float(root_file_for_wallet[1])
    wallet_free_funds = float(root_file_for_wallet[2])
    funds_per_company = float(wallet_funds) / 5
    how_many_company_can_we_obtain = 5 - len(opened_wallet)

    try:
        for index in range(0, int(how_many_company_can_we_obtain), 1):
            company_name = cleared_typed_companies_list[index]
            close_price = float(get_close_price_from_companies_list(source_data, company_name))
            how_many = int(math.floor(funds_per_company / close_price))
            total_cost = (float(how_many) * close_price)
            if wallet_free_funds > total_cost:
                buy(opened_wallet, company_name, how_many, 5, 5)
                wallet_free_funds -= total_cost
            elif total_cost > wallet_free_funds > 1000:
                how_many = int(math.floor(wallet_free_funds / close_price))
                total_cost = (float(how_many) * close_price)
                buy(opened_wallet, company_name, how_many, 5, 5)
                wallet_free_funds -= total_cost
        actualize_wallet(wallet_name, opened_wallet)
        actualize_root_file_for_wallet(wallet_name, [starting_funds, wallet_funds, wallet_free_funds])
    except Exception as err:
        log_error_to_file("buy", ("Cannot buy stack for wallet %s. Reason: %s") % (wallet_name, err))

if __name__ == '__main__':
    try:
        create_new_wallet("simulator", 10000)
        simulate_in_the_past(100)


    except Exception as err:
        print("Failed to execute plugin. Reason: %s" % err)
        traceback.print_exc()
        sys.exit(1)