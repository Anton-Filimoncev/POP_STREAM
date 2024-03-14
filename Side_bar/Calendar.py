import numpy as np
import streamlit as st
import pandas as pd
from .Support import *
from .MARKET_DATA import *
import datetime


# Продаем 2 пута DTE 30, покупаем 1 пут DTE 90.
# Страйки одинаковы.
# Подбор в диапазоне от ATM до - 7 процентов.
# POP считаем от маржи. Маржу считаем как страйк пута * 0.2

def tamplate_gen(template_position):
    if template_position == 'BEAR PUT RATIO CALENDAR':
        position_options = {
                            'short': 'put',
                            'long': 'put',
                            'short_count': 2,
                            'long_count': 1,
                            'short_DTE': 30,
                            'long_DTE': 90,
                            'short_strike_limit_from': 0.93,
                            'short_strike_limit_to': 1,
                            'pop_from': 'margin',

                        }
        pass
    if template_position == 'BEAR PUT RATIO DIAGONAL':
        pass
    if template_position == 'BULL PUT DIAGONAL':
        pass
    if template_position == 'BULL CALL RATIO CALENDAR':
        pass
    if template_position == 'BULL CALL RATIO DIAGONAL':
        pass
    if template_position == 'BEAR CALL DIAGONAL':
        pass

    return position_options


def calendar_diagonal():
    position_type = st.radio("Choose a position type ", ('Put', 'Call'), horizontal=True)

    col21, col22, col23, col24 = st.columns(4)
    with col21:
        tick = st.text_input('Ticker', 'GOOG')
        rate = st.number_input('Risk Rate ', step=0.01, format="%.2f", min_value=0., max_value=5000., value=4.)
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=5000, value=30)
        # end_date_stat = st.date_input('EXP date')
        short_count_solo = st.number_input('Short Count ', step=1, min_value=1, max_value=5000, value=1)

    with col22:
        # ticker = st.text_input('Ticker', '')
        long_strike = st.number_input('Strike Long', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                      value=150.)
        long_price = st.number_input('Price Long', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                     value=28.45)
        sigma_long = st.number_input('Volatility Long', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                     value=28.99)
        long_count_solo = st.number_input('Long Count ', step=1, min_value=1, max_value=5000, value=1)
    with col23:
        # ticker = st.text_input('Ticker', '')
        short_strike = st.number_input('Strike Short', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                       value=150.)
        short_price = st.number_input('Price Short', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                      value=19.6)
        sigma_short = st.number_input('Volatility Short', step=0.01, format="%.2f", min_value=0., max_value=5000.,
                                      value=28.7)

    with col24:
        days_to_expiration_long = st.number_input('Days to EXP Long', step=1, min_value=0, max_value=5000, value=773)
        days_to_expiration_short = st.number_input('Days to EXP Short', step=1, min_value=0, max_value=5000, value=409)
        closing_days_array = st.number_input('Closing Days Proba', step=1, min_value=0, max_value=5000,
                                             value=int(days_to_expiration_short))

    if st.button("Calculate ", type="primary"):
        strengle_data, profit_for_percent, percentage_type = get_calendar_diagonal_input(tick, sigma_long, sigma_short,
                                                                                         rate, days_to_expiration_long,
                                                                                         days_to_expiration_short,
                                                                                         closing_days_array,
                                                                                         percentage_array,
                                                                                         long_strike, long_price,
                                                                                         short_strike, short_price,
                                                                                         position_type,
                                                                                         short_count_solo,
                                                                                         long_count_solo)

        st.dataframe(strengle_data, hide_index=True, column_config=None)
        st.text(f'Profit Percentage form {percentage_type}: {round(profit_for_percent, 2)}')

    # ----------------------------     BATCH      --------------------------------------
    st.title('________________')

    template_position = st.selectbox(
        'Select Template 👇',
        ('BEAR PUT RATIO CALENDAR', 'BEAR PUT RATIO DIAGONAL', 'BULL PUT DIAGONAL', 'BULL CALL RATIO CALENDAR',
         'BULL CALL RATIO DIAGONAL', 'BEAR CALL DIAGONAL'), index=None)

    st.write('You selected:', template_position)

    position_options = tamplate_gen(template_position)
    print(position_options)

    col1, col2, col3 = st.columns(3)

    with col1:
        ticker = st.text_input('Ticker', 'KRE')
        short_count = st.number_input('Short Count', step=1, min_value=1, max_value=5000, value=position_options['short_count'])
    with col2:
        if position_options['short'] == 'put':
            position_type = st.radio("Choose a position type 👇", ('put', 'call'), horizontal=True)
        else:
            position_type = st.radio("Choose a position type 👇", ('call', 'put'), horizontal=True)
        long_count = st.number_input('Long Count', step=1, min_value=1, max_value=5000, value=position_options['long_count'])
    with col3:
        nearest_dte_short = st.number_input('Nearest DTE Short', step=1, min_value=1, max_value=5000, value=position_options['short_DTE'])
        nearest_dte_long = st.number_input('Nearest DTE Long', step=1, min_value=1, max_value=5000, value=position_options['long_DTE'])

    if 'quotes_short' not in st.session_state:
        st.session_state['quotes_short'] = np.nan

    if 'quotes_long' not in st.session_state:
        st.session_state['quotes_long'] = np.nan

    if 'needed_exp_date_long' not in st.session_state:
        st.session_state['needed_exp_date_long'] = np.nan

    if 'needed_exp_date_short' not in st.session_state:
        st.session_state['needed_exp_date_short'] = np.nan

    if st.button("GET MARKET DATA", type="primary"):
        needed_exp_date_short, dte = hedginglab_get_exp_date(ticker, nearest_dte_short)
        needed_exp_date_long, dte = hedginglab_get_exp_date(ticker, nearest_dte_long)
        quotes_short = hedginglab_get_quotes(ticker, nearest_dte_short)
        quotes_long = hedginglab_get_quotes(ticker, nearest_dte_long)
        st.text('Exp Date Short: ' + str(needed_exp_date_short.date()))
        st.text('Exp Date Long: ' + str(needed_exp_date_long.date()))
        # st.dataframe(quotes)
        st.session_state['quotes_short'] = quotes_short
        st.session_state['quotes_long'] = quotes_long
        st.session_state['needed_exp_date_short'] = needed_exp_date_short
        st.session_state['needed_exp_date_long'] = needed_exp_date_long
        st.success('Market Data Downloaded!')

    quotes_short = st.session_state['quotes_short']
    quotes_long = st.session_state['quotes_long']
    needed_exp_date_short = st.session_state['needed_exp_date_short']
    needed_exp_date_long = st.session_state['needed_exp_date_long']



    col11, col12, col13 = st.columns(3)
    with col11:
        rate = st.number_input('Risk Rate', step=0.01, format="%.2f", min_value=0., max_value=5000., value=4.)
    with col12:
        percentage_array = st.number_input('Percentage', step=1, min_value=1, max_value=5000, value=10)
        try:
            days_to_expiration_long = (needed_exp_date_long - datetime.datetime.now()).days
            days_to_expiration_short = (needed_exp_date_short - datetime.datetime.now()).days
        except:
            days_to_expiration_long = np.nan
            days_to_expiration_short = np.nan  # st.date_input('EXP date')

    with col13:
        try:
            closing_days_array = st.number_input('Closing Days Proba', step=1, min_value=0, max_value=5000,
                                                 value=int(days_to_expiration_short))
        except:
            closing_days_array = st.number_input('Closing Days Proba')

    if st.button("Calculate", type="primary"):
        if type(quotes_short) == type(1.):
            st.error('Pleas Download Market Data', icon="🚨")
        else:
            strengle_data, best_df, exp_move_hv, exp_move_iv = get_calendar_diagonal(ticker, rate,
                                                                                     days_to_expiration_long,
                                                                                     days_to_expiration_short,
                                                                                     closing_days_array,
                                                                                     percentage_array, position_type,
                                                                                     quotes_short, quotes_long,
                                                                                     short_count, long_count, position_options)

            st.text('Best Parameters:')
            st.dataframe(best_df[['pop', 'exp_return', 'cvar', 'Strike_Long', 'Strike_Short']], hide_index=True,
                         column_config=None)
            st.text('Expected Move HV: ' + str(round(exp_move_hv, 3)))
            st.text('Expected Move IV: ' + str(round(exp_move_iv, 3)))
            st.text('Total Parameters:')
            st.dataframe(strengle_data, hide_index=True, column_config=None)
