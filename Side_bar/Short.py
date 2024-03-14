import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
from .MARKET_DATA import *
import datetime



def short():

    col1, col2, col3 = st.columns(3)

    with col1:
        ticker = st.text_input('Ticker', 'KRE')

    with col2:
        position_type = st.radio("Choose a position type", ('Put', 'Call'), horizontal=True)
    with col3:
        nearest_dte = st.number_input('Nearest DTE', step=1, min_value=1, max_value=5000, value=45)


    if 'quotes' not in st.session_state:
        st.session_state['quotes'] = np.nan

    if 'needed_exp_date' not in st.session_state:
        st.session_state['needed_exp_date'] = np.nan

    if st.button("GET MARKET DATA", type="primary"):
        needed_exp_date, dte = hedginglab_get_exp_date(ticker, nearest_dte)
        quotes = hedginglab_get_quotes(ticker, nearest_dte)
        # st.text(dte)
        st.text('Exp Date: ' + str(needed_exp_date.date()))
        # st.dataframe(quotes)
        st.session_state['quotes'] = quotes
        st.session_state['needed_exp_date'] = needed_exp_date
        st.success('Market Data Downloaded!')

    quotes = st.session_state['quotes']
    needed_exp_date = st.session_state['needed_exp_date']

    col11, col12, col13 = st.columns(3)
    with col11:
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=5000.,  value=4.)
    with col12:
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=5000, value=50)
        try:
            days_to_expiration = (needed_exp_date - datetime.datetime.now()).days
        except:
            days_to_expiration = np.nan #st.date_input('EXP date')

    with col13:
        try:
            closing_days_array = st.number_input('Closing Days Proba', step=1, min_value=0, max_value=5000,
                                                 value=int(days_to_expiration))
        except:
            closing_days_array = st.number_input('Closing Days Proba')

    if st.button("Calculate", type="primary"):
        print('quotes')
        print(quotes)
        short_data, best_df, exp_move_hv, exp_move_iv = get_short(ticker, rate, days_to_expiration, closing_days_array, percentage_array,
                                  position_type, quotes)

        st.text('Best Parameters:')
        st.dataframe(best_df[['pop', 'exp_return', 'cvar', 'Strike']], hide_index=True, column_config=None)
        st.text('Expected Move HV: ' + str(round(exp_move_hv, 3)))
        st.text('Expected Move IV: ' + str(round(exp_move_iv, 3)))
        st.text('Total Parameters:')
        st.dataframe(short_data, hide_index=True, column_config=None)
