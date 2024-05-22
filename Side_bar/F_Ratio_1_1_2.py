import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
import datetime



def f_ratio_112():

    col1, col2 = st.columns(2)

    with col1:
        ticker = st.text_input('Ticker', 'ES=F')
    with col2:
        days_to_expiration = st.number_input('Days to EXP', step=1, min_value=0, max_value=50000, value=30)
    # with col3:
    #     days_to_expiration_2_long = st.number_input('Days to EXP 2 Long', step=1, min_value=0, max_value=5000, value=50)


    col11, col12, col13 = st.columns(3)
    with col11:
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=50000.,  value=4.)

        short_1_sigma = st.number_input('Short 1 Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)
        short_1_prime = st.number_input('Short 1 Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        short_1_strike = st.number_input('Short 1 Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)
    with col12:
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=50000, value=30)
        short_2_sigma = st.number_input('Short 2 Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)
        short_2_prime = st.number_input('Short 2 Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        short_2_strike = st.number_input('Short 2 Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)

    with col13:
        closing_days_array = st.number_input('Closing Days Proba', step=1, min_value=0, max_value=50000,
                                             value=int(days_to_expiration))
        long_sigma = st.number_input('Long Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)
        long_prime = st.number_input('Long Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        long_strike = st.number_input('Long Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)


    long_count = 1
    short_1_count = 1
    short_2_count = 2


    if st.button("Calculate", type="primary"):

        da_ratio_112_data = get_f_ratio_112(ticker, long_sigma, short_1_sigma, short_2_sigma, rate,  days_to_expiration,
                                      closing_days_array, percentage_array, long_strike, short_1_strike, short_2_strike,
                                      long_prime, short_1_prime, short_2_prime,  long_count, short_1_count,
                                      short_2_count)

        st.text('Parameters:')
        st.dataframe(da_ratio_112_data[['pop', 'exp_return', 'cvar']], hide_index=True, column_config=None)
        # st.text('Expected Move HV: ' + str(round(exp_move_hv, 3)))
        # st.text('Expected Move IV: ' + str(round(exp_move_iv, 3)))