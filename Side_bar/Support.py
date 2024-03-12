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

            strangle_data = shortStrangle(underlying, (sigma_call+sigma_put)/2, rate, trials, days_to_expiration,
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

    iv = (iv_call + iv_put)/2

    print('current_iv', iv)

    sum_df['top_score'] = sum_df['pop'] * sum_df['exp_return']
    best_df = sum_df[sum_df['top_score'] == sum_df['top_score'].max()]

    exp_move_hv = hv*underlying*math.sqrt(days_to_expiration/365)
    exp_move_iv = iv * underlying * math.sqrt(days_to_expiration / 365)

    return sum_df, best_df, exp_move_hv, exp_move_iv

def get_short(tick, rate, days_to_expiration, closing_days_array, percentage_array,
                                  position_type, quotes):
    print(quotes)
    current_price = quotes['underlyingPrice'].iloc[0]

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
            short_data = shortPut(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array], [percentage_array],
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
            short_data = shortCall(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array], [percentage_array],
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

    exp_move_hv = hv*underlying*math.sqrt(days_to_expiration/365)
    exp_move_iv = iv * underlying * math.sqrt(days_to_expiration / 365)

    return sum_df, best_df, exp_move_hv, exp_move_iv



def get_calendar_diagonal(tick, sigma_long, sigma_short, rate, days_to_expiration_long,
                          days_to_expiration_short, closing_days_array, percentage_array, long_strike, long_price,
                                              short_strike, short_price, position_type):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 2000
    if position_type == 'Put':
        calendar_diagonal_data = putCalendar(underlying, sigma_short, sigma_long, rate, trials,
                                                  days_to_expiration_short,
                                                  days_to_expiration_long, [closing_days_array], [percentage_array],
                                                  long_strike,
                                                  long_price, short_strike, short_price, yahoo_stock)
        print("calendar_diagonal_data Put: ", calendar_diagonal_data)

    if position_type == 'Call':
        calendar_diagonal_data = callCalendar(underlying, sigma_short, sigma_long, rate, trials,
                                                   days_to_expiration_short,
                                                   days_to_expiration_long, [closing_days_array], [percentage_array],
                                                   long_strike,
                                                   long_price, short_strike, short_price, yahoo_stock)
        print("calendar_diagonal_data Call: ", calendar_diagonal_data)


    return pd.DataFrame(calendar_diagonal_data)

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
        long_data = longPut(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array], [percentage_array],
                 long_strike, long_price, yahoo_stock)
        print("Long Put: ", long_data)

    if position_type == 'Call':
        long_data = longCall(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array], [percentage_array],
                 long_strike, long_price, yahoo_stock)
        print("Long Call: ", long_data)

    return pd.DataFrame(long_data)

