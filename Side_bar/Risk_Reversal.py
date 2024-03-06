import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
import datetime

def risk_reversal():

    col11, col12, col13, col14 = st.columns(4)
    with col11:
        tick = st.text_input('Ticker', 'KRE')
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=5000.,  value=4.)
        percentage_array = st.number_input('Multiple of Debit', step=1, min_value=1, max_value=5000, value=1)
        # end_date_stat = st.date_input('EXP date')

    with col12:
        # ticker = st.text_input('Ticker', '')
        long_strike = st.number_input('Call Strike Long', step=0.01, format="%.2f", min_value=0., max_value=5000., value=61.)
        long_price = st.number_input('Call Price Long', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=1.18)

    with col13:
        # ticker = st.text_input('Ticker', '')
        short_strike = st.number_input('Put Strike Short', step=0.01, format="%.2f", min_value=0., max_value=5000., value=38.)
        short_price = st.number_input('Put Price Short', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=2.)
    with col14:
        sigma = st.number_input('Volatility Mean', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                      value=30.)
        days_to_expiration = st.number_input('Days to EXP', step=1,  min_value=0, max_value=5000, value=338)
        closing_days_array = st.number_input('Closing Days Proba', step=1,  min_value=0, max_value=5000,
                                              value=int(days_to_expiration/2))

    if st.button("Calculate", type="primary"):
        strengle_data = get_risk_reversal(tick, sigma, rate, days_to_expiration, closing_days_array,
                                              percentage_array, long_strike, long_price, short_strike, short_price)

        st.dataframe(strengle_data, hide_index=True, column_config=None)

