import streamlit as st
import pandas as pd
from Road_map import *

st.set_page_config(page_icon='💵', page_title="Monitoring" )
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
    "Choose an info type",
    ('Strangle', 'Short', 'Long', 'Diagonal', 'Calendar') # 'Call Monitoring',
)


# =====================================   Strangle
if infoType == 'Strangle':
    st.title('Strangle Position')
    strangle()

# =====================================   Short
if infoType == 'Short':
    st.title('Short Position')
    short()

# # =====================================   Long
# if infoType == 'Long':
#     st.title('Long Position')
#     long()
#
# # =====================================   Diagonal
# if infoType == 'Diagonal':
#     st.title('Diagonal Position')
#     diagonal()
#
# # =====================================   Calendar
# if infoType == 'Calendar':
#     st.title('Calendar Position')
#     calendar()


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








