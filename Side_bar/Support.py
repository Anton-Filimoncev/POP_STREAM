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


def get_yahoo_price(ticker):
    yahoo_data = yf.download(ticker, progress=False)
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