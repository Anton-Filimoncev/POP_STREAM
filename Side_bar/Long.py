import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
import datetime



def long():


    position_type = st.radio("Choose a position type", ('Put', 'Call'), horizontal=True)

    col11, col12, col13 = st.columns(3)
    with col11:
        tick = st.text_input('Ticker', 'CRM')
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=5000.,  value=4.)
        percentage_array = st.number_input('Multiple of debit', step=1, min_value=1, max_value=5000, value=1)
        # end_date_stat = st.date_input('EXP date')
    with col12:
        # ticker = st.text_input('Ticker', '')
        long_strike = st.number_input('Strike', step=0.01, format="%.2f", min_value=0., max_value=5000., value=170.)
        long_price = st.number_input('Price', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=9.16)

    with col13:
        sigma = st.number_input('Volatility Mean', step=0.01, format="%.2f", min_value=0., max_value=5000., value=36.)

        days_to_expiration = st.number_input('Days to EXP', step=1,  min_value=0, max_value=5000, value=256)
        closing_days_array = st.number_input('Closing Days Proba', step=1,  min_value=0, max_value=5000,
                                              value=int(days_to_expiration))

    if st.button("Calculate", type="primary"):
        strengle_data = get_long(tick, sigma, rate, days_to_expiration, closing_days_array, percentage_array,
                                  long_strike, long_price, position_type)
        st.dataframe(strengle_data, hide_index=True, column_config=None)