import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
from .MARKET_DATA import *
import datetime


def f_strangle():
    col1, col2 = st.columns(2)

    with col1:
        ticker = st.text_input('Ticker', 'ES=F')
    with col2:
        days_to_expiration = st.number_input('Days to EXP', step=1, min_value=0, max_value=50000, value=30)


    col11, col12, col13 = st.columns(3)
    with col11:
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=50000.,  value=4.)
        closing_days_array = st.number_input('Closing Days Proba', step=1, min_value=0, max_value=50000,
                                             value=int(days_to_expiration))
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=50000, value=50)

    with col12:
        call_price = st.number_input('Call Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        call_strike = st.number_input('Call Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)
        sigma_call = st.number_input('Call Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)


    with col13:
        put_price = st.number_input('Put Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        put_strike = st.number_input('Put Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)
        sigma_put = st.number_input('Put Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)

    if st.button("Calculate", type="primary"):

        strengle_data, exp_move_hv = get_f_strangle(ticker, rate, percentage_array, days_to_expiration,
                                                    closing_days_array, sigma_call, sigma_put, call_price,
                                                    put_price, call_strike, put_strike)

        st.text('Best Parameters:')
        st.dataframe(strengle_data[['pop', 'exp_return', 'cvar']], hide_index=True, column_config=None)
        st.text('Expected Move HV: ' + str(round(exp_move_hv, 3)))


