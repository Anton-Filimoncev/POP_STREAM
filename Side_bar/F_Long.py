import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
import datetime



def f_long():

    col1, col2, col3 = st.columns(3)

    with col1:
        ticker = st.text_input('Ticker', 'ES=F')
    with col2:
        position_type = st.radio("Choose a position type 👇", ('Put', 'Call'), horizontal=True)
    with col3:
        days_to_expiration = st.number_input('Days to EXP', step=1, min_value=0, max_value=50000, value=30)


    col11, col12, col13 = st.columns(3)
    with col11:
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=50000.,  value=4.)
        closing_days_array = st.number_input('Closing Days Proba', step=1, min_value=0, max_value=50000,
                                             value=int(days_to_expiration))
    with col12:
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=50000, value=50)
        prime = st.number_input('Prime', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                      value=19.6)

    with col13:
        sigma = st.number_input('Volatility', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                     value=12.)
        strike = st.number_input('Strike', step=0.01, format="%.2f", min_value=0., max_value=50000.,
                                       value=150.)

    if st.button("Calculate", type="primary"):
        short_data = get_f_long(ticker, rate, days_to_expiration, closing_days_array, percentage_array,
                                  position_type, sigma, strike, prime)
        st.text('Parameters:')
        st.dataframe(short_data[['pop', 'exp_return', 'cvar']], hide_index=True, column_config=None)
        # st.text('Expected Move HV: ' + str(round(exp_move_hv, 3)))
        # st.text('Expected Move IV: ' + str(round(exp_move_iv, 3)))