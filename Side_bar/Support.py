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

def get_yahoo_price(ticker):
    yahoo_data = yf.download(ticker, progress=False)['2018-01-01':]
    return yahoo_data



def get_strangle(tick, rate, percentage_array, call_short_strike, call_short_price, put_short_strike,
                                 put_short_price, sigma, days_to_expiration, closing_days_array):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 3000
    strangle_data = shortStrangle(underlying, sigma, rate, trials, days_to_expiration,
                        [closing_days_array], [percentage_array], call_short_strike,
                        call_short_price, put_short_strike, put_short_price, yahoo_stock)
    print("Short Strangle: ", strangle_data)

    return pd.DataFrame(strangle_data)

def get_short(tick, sigma, rate,days_to_expiration, closing_days_array, percentage_array,
                                  short_strike, short_price, position_type):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 3000
    if position_type == 'Put':
        short_data = shortPut(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array], [percentage_array],
                 short_strike, short_price, yahoo_stock)
        print("Short Put: ", short_data)

    if position_type == 'Call':
        short_data = shortCall(underlying, sigma, rate, trials, days_to_expiration, [closing_days_array], [percentage_array],
                 short_strike, short_price, yahoo_stock)
        print("Short Call: ", short_data)

    return pd.DataFrame(short_data)



def get_calendar_diagonal(tick, sigma_long, sigma_short, rate, days_to_expiration_long,
                          days_to_expiration_short, closing_days_array, percentage_array, long_strike, long_price,
                                              short_strike, short_price, position_type):
    yahoo_stock = get_yahoo_price(tick)
    underlying = yahoo_stock['Close'].iloc[-1]
    trials = 3000
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
    trials = 3000

    risk_reversal_data = riskReversal(underlying, sigma, rate, trials, days_to_expiration,
                          [closing_days_array], [percentage_array], long_strike, long_price, short_strike,
                          short_price, yahoo_stock)

    print("risk_reversal_data: ", risk_reversal_data)

    return pd.DataFrame(risk_reversal_data)