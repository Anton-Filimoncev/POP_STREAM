import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
import datetime


def strangle():

    col11, col12, col13, col14 = st.columns(4)
    with col11:
        tick = st.text_input('Ticker', '')
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=5000.,  value=4.)
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=5000, value=50)
        # end_date_stat = st.date_input('EXP date')
    with col12:
        # ticker = st.text_input('Ticker', '')
        call_short_strike = st.number_input('Call Strike', step=0.01, format="%.2f", min_value=0., max_value=5000., value=0.01)
        call_short_price = st.number_input('Call Price', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=0.01)

    with col13:
        put_short_strike = st.number_input('Put Strike', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=0.01)
        put_short_price = st.number_input('Put Price', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=0.01)

    with col14:
        sigma = st.number_input('Volatility Mean', step=0.01, format="%.2f", min_value=0., max_value=5000., value=0.01)

        days_to_expiration = st.number_input('Days to EXP', step=1,  min_value=0, max_value=5000, value=10)
        closing_days_array = [st.number_input('Closing Days Proba', step=1,  min_value=0, max_value=5000,
                                              value=int(days_to_expiration/2))]