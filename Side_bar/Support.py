import pandas as pd
import numpy as np
import scipy.stats as stats
import time
import datetime
import yfinance as yf
import math
import requests
import credential
import mibian
from .popoption.ShortPut import shortPut
from .popoption.ShortCall import shortCall
from .popoption.ShortStrangle import shortStrangle
from .popoption.PutCalendar import putCalendar
from .popoption.CallCalendar import callCalendar
from .popoption.PutCalendar_template import putCalendar_template
from .popoption.CallCalendar_template import callCalendar_template
from .popoption.RiskReversal import riskReversal
from .popoption.LongPut import longPut
from .popoption.LongCall import longCall
from sklearn.linear_model import LinearRegression


def nearest_equal_abs(lst, target):
    return min(lst, key=lambda x: abs(abs(x) - target))


def volatility_calc(stock_yahoo):
    # ======= HIST volatility calculated ===========
    try:
        TRADING_DAYS = 252
        returns = np.log(stock_yahoo / stock_yahoo.shift(1))
        returns.fillna(0, inplace=True)
        volatility = returns.rolling(window=TRADING_DAYS).std() * np.sqrt(TRADING_DAYS)
        hist_vol = volatility.iloc[-1]
    except:
        hist_vol = 0

    return hist_vol


def get_exp_move(tick, stock_yahoo):
    print('---------------------------')
    print('------------- Getting HV --------------')
    print('---------------------------')

    stock_yahoo_solo = stock_yahoo['Close']
    hist_vol = volatility_calc(stock_yahoo_solo)

    return hist_vol


def get_yahoo_price(ticker):
    yahoo_data = yf.download(ticker, progress=False)['2018-01-01':]
    return yahoo_data


def get_strangle(tick, rate, percentage_array, days_to_expiration, closing_days_array, quotes):
    current_price = quotes['underlyingPrice'].iloc[0]

    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 2000

    sum_df = pd.DataFrame()
    hv = get_exp_move(tick, yahoo_stock)

    quotes_put = quotes[quotes['side'] == 'put'].reset_index(drop=True)
    quotes_put = quotes_put[quotes_put['strike'] <= underlying * 1].reset_index(drop=True)
    quotes_put = quotes_put[quotes_put['strike'] >= underlying * 0.93].reset_index(drop=True)

    quotes_call = quotes[quotes['side'] == 'call'].reset_index(drop=True)
    quotes_call = quotes_call[quotes_call['strike'] <= underlying * 1.07].reset_index(drop=True)
    quotes_call = quotes_call[quotes_call['strike'] >= underlying * 1].reset_index(drop=True)

    for num, quotes_put_row in quotes_put.iterrows():
        for num, quotes_call_row in quotes_call.iterrows():
            print(quotes_call)
            sigma_call = quotes_call_row['iv'] * 100
            sigma_put = quotes_put_row['iv'] * 100
            call_strike = float(quotes_call_row['strike'])
            call_price = float(quotes_call_row['bid'])
            put_strike = float(quotes_put_row['strike'])
            put_price = float(quotes_put_row['bid'])

            print('sigma_call', sigma_call)
            print('sigma_put', sigma_put)
            print('call_strike', call_strike)
            print('call_price', call_price)
            print('put_strike', put_strike)
            print('put_price', put_price)

            strangle_data = shortStrangle(underlying, (sigma_call + sigma_put) / 2, rate, trials, days_to_expiration,
                                          [closing_days_array], [percentage_array], call_strike,
                                          call_price, put_strike, put_price, yahoo_stock)
            strangle_data = pd.DataFrame(strangle_data)
            strangle_data['Strike Call'] = [call_strike]
            strangle_data['Strike Put'] = [put_strike]
            sum_df = pd.concat([sum_df, strangle_data])

    nearest_atm_strike_call = nearest_equal_abs(quotes_call['strike'].astype('float'), underlying)
    iv_call = quotes_call[quotes_call['strike'] == nearest_atm_strike_call]['iv'].values.tolist()[0]

    nearest_atm_strike_put = nearest_equal_abs(quotes_put['strike'].astype('float'), underlying)
    iv_put = quotes_put[quotes_put['strike'] == nearest_atm_strike_put]['iv'].values.tolist()[0]

    iv = (iv_call + iv_put) / 2

    print('current_iv', iv)

    sum_df['top_score'] = sum_df['pop'] * sum_df['exp_return']
    best_df = sum_df[sum_df['top_score'] == sum_df['top_score'].max()]

    exp_move_hv = hv * underlying * math.sqrt(days_to_expiration / 365)
    exp_move_iv = iv * underlying * math.sqrt(days_to_expiration / 365)

    return sum_df, best_df, exp_move_hv, exp_move_iv


def get_short(tick, rate, days_to_expiration, closing_days_array, percentage_array,
              position_type, quotes):
    print(quotes)
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 2000

    sum_df = pd.DataFrame()

    hv = get_exp_move(tick, yahoo_stock)

    if position_type == 'Put':
        quotes = quotes[quotes['side'] == 'put'].reset_index(drop=True)
        quotes = quotes[quotes['strike'] <= underlying * 1].reset_index(drop=True)
        quotes = quotes[quotes['strike'] >= underlying * 0.9].reset_index(drop=True)
        for num, quote_row in quotes.iterrows():
            print(quote_row)
            sigma = quote_row['iv'] * 100
            short_strike = quote_row['strike']
            short_price = quote_row['bid']
            short_data = shortPut(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array],
                                  [percentage_array],
                                  short_strike, short_price, yahoo_stock)
            short_data = pd.DataFrame(short_data)
            short_data['Strike'] = [short_strike]
            sum_df = pd.concat([sum_df, short_data])

    if position_type == 'Call':
        quotes = quotes[quotes['side'] == 'call'].reset_index(drop=True)
        quotes = quotes[quotes['strike'] <= underlying * 1.1].reset_index(drop=True)
        quotes = quotes[quotes['strike'] >= underlying * 1].reset_index(drop=True)
        for num, quote_row in quotes.iterrows():
            print(quote_row)
            sigma = quote_row['iv'] * 100
            short_strike = quote_row['strike']
            short_price = quote_row['bid']
            short_data = shortCall(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array],
                                   [percentage_array],
                                   short_strike, short_price, yahoo_stock)
            short_data = pd.DataFrame(short_data)
            short_data['Strike'] = [short_strike]
            sum_df = pd.concat([sum_df, short_data])

    nearest_atm_strike = nearest_equal_abs(quotes['strike'].astype('float'), underlying)
    iv = quotes[quotes['strike'] == nearest_atm_strike]['iv'].values.tolist()[0]
    print('nearest_strike', nearest_atm_strike)
    print('current_iv', iv)

    sum_df['top_score'] = sum_df['pop'] * sum_df['exp_return']
    best_df = sum_df[sum_df['top_score'] == sum_df['top_score'].max()]

    exp_move_hv = hv * underlying * math.sqrt(days_to_expiration / 365)
    exp_move_iv = iv * underlying * math.sqrt(days_to_expiration / 365)

    return sum_df, best_df, exp_move_hv, exp_move_iv


def get_calendar_diagonal(tick, rate, days_to_expiration_long, days_to_expiration_short, closing_days_array,
                          percentage_array, position_type, quotes_short, quotes_long, short_count, long_count, position_options):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 2000

    sum_df = pd.DataFrame()

    hv = get_exp_move(tick, yahoo_stock)

    if position_type == 'put':
        quotes_short = quotes_short[quotes_short['side'] == 'put'].reset_index(drop=True)
        quotes_short = quotes_short[quotes_short['strike'] <= underlying * position_options['short_strike_limit_to']].reset_index(drop=True)
        quotes_short = quotes_short[quotes_short['strike'] >= underlying * position_options['short_strike_limit_from']].reset_index(drop=True)

        quotes_long = quotes_long[quotes_long['side'] == 'put'].reset_index(drop=True)
        quotes_long = quotes_long[quotes_long['strike'] <= underlying * position_options['long_strike_limit_to']].reset_index(drop=True)
        quotes_long = quotes_long[quotes_long['strike'] >= underlying * position_options['long_strike_limit_from']].reset_index(drop=True)
        for num, quotes_short_row in quotes_short.iterrows():
            for num_long, quotes_long_row in quotes_long.iterrows():
                sigma_short = quotes_short_row['iv'] * 100
                short_strike = quotes_short_row['strike']
                short_price = quotes_short_row['bid'] * short_count
                sigma_long = quotes_long_row['iv'] * 100
                long_strike = quotes_long_row['strike']
                long_price = quotes_long_row['ask'] * long_count

                if position_options['structure'] == 'calendar':
                    if quotes_short_row['strike'] == quotes_long_row['strike']:
                        calendar_diagonal_data, max_profit, percentage_type = putCalendar_template(underlying, sigma_short, sigma_long, rate, trials,
                                                             days_to_expiration_short, days_to_expiration_long,
                                                             [closing_days_array],
                                                             [percentage_array], long_strike, long_price, short_strike,
                                                             short_price, yahoo_stock, short_count, long_count, position_options)
                        print('calendar_diagonal_data', calendar_diagonal_data)
                        calendar_diagonal_data = pd.DataFrame(calendar_diagonal_data)
                        calendar_diagonal_data['Strike_Short'] = [short_strike]
                        calendar_diagonal_data['Strike_Long'] = [long_strike]
                        sum_df = pd.concat([sum_df, calendar_diagonal_data])
                else:
                    calendar_diagonal_data, max_profit, percentage_type = putCalendar_template(underlying, sigma_short,
                                                                                               sigma_long, rate, trials,
                                                                                               days_to_expiration_short,
                                                                                               days_to_expiration_long,
                                                                                               [closing_days_array],
                                                                                               [percentage_array],
                                                                                               long_strike, long_price,
                                                                                               short_strike,
                                                                                               short_price, yahoo_stock,
                                                                                               short_count, long_count,
                                                                                               position_options)
                    print('calendar_diagonal_data', calendar_diagonal_data)
                    calendar_diagonal_data = pd.DataFrame(calendar_diagonal_data)
                    calendar_diagonal_data['Strike_Short'] = [short_strike]
                    calendar_diagonal_data['Strike_Long'] = [long_strike]
                    sum_df = pd.concat([sum_df, calendar_diagonal_data])

    if position_type == 'call':
        quotes_short = quotes_short[quotes_short['side'] == 'call'].reset_index(drop=True)
        quotes_short = quotes_short[quotes_short['strike'] <= underlying * position_options['short_strike_limit_to']].reset_index(drop=True)
        quotes_short = quotes_short[quotes_short['strike'] >= underlying * position_options['short_strike_limit_from']].reset_index(drop=True)

        quotes_long = quotes_long[quotes_long['side'] == 'call'].reset_index(drop=True)
        quotes_long = quotes_long[quotes_long['strike'] <= underlying * position_options['long_strike_limit_to']].reset_index(drop=True)
        quotes_long = quotes_long[quotes_long['strike'] >= underlying * position_options['long_strike_limit_from']].reset_index(drop=True)

        # if position_options['structure'] == 'calendar':
        #     quotes_long =

        for num, quotes_short_row in quotes_short.iterrows():
            for num_long, quotes_long_row in quotes_long.iterrows():
                sigma_short = quotes_short_row['iv'] * 100
                short_strike = quotes_short_row['strike']
                short_price = quotes_short_row['bid'] * short_count

                sigma_long = quotes_long_row['iv'] * 100
                long_strike = quotes_long_row['strike']
                long_price = quotes_long_row['ask'] * long_count

                print('short bid', quotes_short_row['bid'])
                print('short_price', short_price)
                print('long ask', quotes_long_row['ask'])
                print('long_price', long_price)
                print('long_strike', long_strike)
                print('short_strike', short_strike)
                print('long_strike', sigma_long)
                print('short_strike', sigma_short)
                print('days_to_expiration_short', days_to_expiration_short)
                print('days_to_expiration_long', days_to_expiration_long)

                if position_options['structure'] == 'calendar':
                    if quotes_short_row['strike'] == quotes_long_row['strike']:
                        calendar_diagonal_data, max_profit, percentage_type = callCalendar_template(underlying, sigma_short, sigma_long, rate, trials,
                                                             days_to_expiration_short, days_to_expiration_long,
                                                             [closing_days_array],
                                                             [percentage_array], long_strike, long_price, short_strike,
                                                             short_price, yahoo_stock,
                                                             short_count, long_count, position_options)

                        calendar_diagonal_data = pd.DataFrame(calendar_diagonal_data)
                        calendar_diagonal_data['Strike_Short'] = [short_strike]
                        calendar_diagonal_data['Strike_Long'] = [long_strike]
                        sum_df = pd.concat([sum_df, calendar_diagonal_data])
                else:
                    calendar_diagonal_data, max_profit, percentage_type = callCalendar_template(underlying, sigma_short,
                                                                                                sigma_long, rate,
                                                                                                trials,
                                                                                                days_to_expiration_short,
                                                                                                days_to_expiration_long,
                                                                                                [closing_days_array],
                                                                                                [percentage_array],
                                                                                                long_strike, long_price,
                                                                                                short_strike,
                                                                                                short_price,
                                                                                                yahoo_stock,
                                                                                                short_count, long_count,
                                                                                                position_options)

                    calendar_diagonal_data = pd.DataFrame(calendar_diagonal_data)
                    calendar_diagonal_data['Strike_Short'] = [short_strike]
                    calendar_diagonal_data['Strike_Long'] = [long_strike]
                    sum_df = pd.concat([sum_df, calendar_diagonal_data])

    nearest_atm_strike = nearest_equal_abs(quotes_short['strike'].astype('float'), underlying)
    iv = quotes_short[quotes_short['strike'] == nearest_atm_strike]['iv'].values.tolist()[0]
    print('nearest_strike', nearest_atm_strike)
    print('current_iv', iv)
    sum_df['top_score'] = sum_df['pop'] * sum_df['exp_return']
    best_df = sum_df[sum_df['top_score'] == sum_df['top_score'].max()]
    exp_move_hv = hv * underlying * math.sqrt(days_to_expiration_short / 365)
    exp_move_iv = iv * underlying * math.sqrt(days_to_expiration_short / 365)

    return sum_df, best_df, exp_move_hv, exp_move_iv, max_profit, percentage_type


def get_calendar_diagonal_input(tick, sigma_long, sigma_short, rate, days_to_expiration_long,
                                days_to_expiration_short, closing_days_array, percentage_array, long_strike, long_price,
                                short_strike, short_price, position_type, short_count_solo, long_count_solo):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 2000
    if position_type == 'Put':
        calendar_diagonal_data, profit_for_percent, percentage_type = putCalendar(underlying, sigma_short, sigma_long, rate, trials,
                                             days_to_expiration_short,
                                             days_to_expiration_long, [closing_days_array], [percentage_array],
                                             long_strike,
                                             long_price, short_strike, short_price, yahoo_stock, short_count_solo,
                                             long_count_solo)
        print("calendar_diagonal_data Put: ", calendar_diagonal_data)

    if position_type == 'Call':
        calendar_diagonal_data, profit_for_percent, percentage_type = callCalendar(underlying, sigma_short, sigma_long, rate, trials,
                                              days_to_expiration_short, days_to_expiration_long, [closing_days_array],
                                              [percentage_array], long_strike, long_price, short_strike, short_price,
                                              yahoo_stock,
                                              short_count_solo, long_count_solo)
        print("calendar_diagonal_data Call: ", calendar_diagonal_data)

    return pd.DataFrame(calendar_diagonal_data), profit_for_percent, percentage_type


def get_risk_reversal(tick, sigma, rate, days_to_expiration, closing_days_array,
                      percentage_array, long_strike, long_price, short_strike, short_price):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 2000

    risk_reversal_data = riskReversal(underlying, sigma, rate, trials, days_to_expiration,
                                      [closing_days_array], [percentage_array], long_strike, long_price, short_strike,
                                      short_price, yahoo_stock)

    print("risk_reversal_data: ", risk_reversal_data)

    return pd.DataFrame(risk_reversal_data)


def get_long(tick, sigma, rate, days_to_expiration, closing_days_array, percentage_array,
             long_strike, long_price, position_type):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 2000

    if position_type == 'Put':
        long_data = longPut(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array],
                            [percentage_array],
                            long_strike, long_price, yahoo_stock)
        print("Long Put: ", long_data)

    if position_type == 'Call':
        long_data = longCall(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array],
                             [percentage_array],
                             long_strike, long_price, yahoo_stock)
        print("Long Call: ", long_data)

    return pd.DataFrame(long_data)
