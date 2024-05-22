import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
import datetime



def f_da_bat():

    col1, col2, col3 = st.columns(3)

    with col1:
        ticker = st.text_input('Ticker', 'ES=F')
    with col2:
        days_to_expiration_1 = st.number_input('Days to EXP 1', step=1, min_value=0, max_value=50000, value=30)
    with col3:
        days_to_expiration_2_long = st.number_input('Days to EXP 2 Long', step=1, min_value=0, max_value=50000, value=30)


    col11, col12, col13 = st.columns(3)
    with col11:
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=50000.,  value=4.)

        long_1_sigma = st.number_input('Long 1 Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)
        long_1_prime = st.number_input('Long 1 Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        long_1_strike = st.number_input('Long 1 Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)
    with col12:
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=50000, value=30)
        long_2_sigma = st.number_input('Long 2 Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)
        long_2_prime = st.number_input('Long 2 Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        long_2_strike = st.number_input('Long 2 Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)

    with col13:
        closing_days_array = st.number_input('Closing Days Proba', step=1, min_value=0, max_value=50000,
                                             value=int(days_to_expiration_1))
        short_sigma = st.number_input('Short Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)
        short_prime = st.number_input('Short Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)
        short_strike = st.number_input('Short Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)

    long_1_count = 1
    long_2_count = 1
    short_count = 2


    if st.button("Calculate", type="primary"):
        da_bat_data = get_f_da_but(ticker, rate, days_to_expiration_1, days_to_expiration_2_long, closing_days_array, percentage_array,
                       long_1_sigma, long_2_sigma, short_sigma, long_1_prime, long_2_prime, short_prime, long_1_strike,
                      long_2_strike, short_strike, long_1_count, long_2_count, short_count)
        st.text('Parameters:')
        st.dataframe(da_bat_data[['pop', 'exp_return', 'cvar']], hide_index=True, column_config=None)
        # st.text('Expected Move HV: ' + str(round(exp_move_hv, 3)))
        # st.text('Expected Move IV: ' + str(round(exp_move_iv, 3)))