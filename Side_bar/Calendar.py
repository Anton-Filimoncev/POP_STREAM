import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
import datetime



def calendar_diagonal():

    position_type = st.radio("Choose a position type", ('Put', 'Call'), horizontal=True)

    col11, col12, col13, col14 = st.columns(4)
    with col11:
        tick = st.text_input('Ticker', 'GOOG')
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=5000.,  value=4.)
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=5000, value=30)
        # end_date_stat = st.date_input('EXP date')

    with col12:
        # ticker = st.text_input('Ticker', '')
        long_strike = st.number_input('Strike Long', step=0.01, format="%.2f", min_value=0., max_value=5000., value=150.)
        long_price = st.number_input('Price Long', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=28.45)
        sigma_long = st.number_input('Volatility Long', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                      value=28.99)
    with col13:
        # ticker = st.text_input('Ticker', '')
        short_strike = st.number_input('Strike Short', step=0.01, format="%.2f", min_value=0., max_value=5000., value=150.)
        short_price = st.number_input('Price Short', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                            value=19.6)
        sigma_short = st.number_input('Volatility Short', step=0.01, format="%.2f", min_value=0., max_value=5000., value=28.7)

    with col14:
        days_to_expiration_long = st.number_input('Days to EXP Long', step=1,  min_value=0, max_value=5000, value=773)
        days_to_expiration_short = st.number_input('Days to EXP Short', step=1, min_value=0, max_value=5000, value=409)
        closing_days_array = st.number_input('Closing Days Proba', step=1,  min_value=0, max_value=5000,
                                              value=int(days_to_expiration_short))

    if st.button("Calculate", type="primary"):
        strengle_data = get_calendar_diagonal(tick, sigma_long, sigma_short, rate, days_to_expiration_long,
                          days_to_expiration_short, closing_days_array, percentage_array, long_strike, long_price,
                                              short_strike, short_price, position_type)

        st.dataframe(strengle_data, hide_index=True, column_config=None)