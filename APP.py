import streamlit as st
import pandas as pd
from Road_map import *

st.set_page_config(page_icon='💵', page_title="POP" )
# ---- HIDE STREAMLIT STYLE ----
# # MainMenu {visibility: hidden;}
# header {visibility: hidden;}
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



infoType = st.sidebar.radio(
    "Choose a position type",
    ('Strangle', 'Short', 'Long', 'Calendar/Diagonal', 'Risk Reversal') # 'Call Monitoring',
)


# =====================================   Strangle
if infoType == 'Strangle':
    st.title('Strangle Position')
    strangle()

# =====================================   Short
if infoType == 'Short':
    st.title('Short Position')
    short()

# =====================================   Long
if infoType == 'Long':
    st.title('Long Position')
    long()
#
# =====================================   Calendar/Diagonal
if infoType == 'Calendar/Diagonal':
    st.title('Calendar/Diagonal Position')
    calendar_diagonal()
#
# =====================================   Risk Reversal
if infoType == 'Risk Reversal':
    st.title('Risk Reversal Position')
    risk_reversal()


# =====================================
if infoType == 'git test':
    from git import Repo
    PATH_OF_GIT_REPO = "https://github.com/Anton-Filimoncev/MONITORING_SYSTEM.git"
    COMMIT_MESSAGE = 'comment from python script'

    #
    def git_push():
        # try:
        repo = Repo(search_parent_directories=True)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        # except:
        #     print('Some error occured while pushing the code')


    git_push()








