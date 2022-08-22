import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import date,timedelta
import EOD

st.title("BHAVCOPY NSE especially for AMIBROKER USERS")

col1,col2 = st.columns([1,1])
with col1:
    my1_date = st.date_input("FROM", value=date.today(),
                                min_value=datetime.date(1990, 1, 1))
with col2:
    if my1_date is not date.today():
        my2_date = st.date_input("TILL", value=min(my1_date+timedelta(60),date.today()),
                                    min_value=datetime.date(1990, 1, 1))
    else :
        my2_date = st.date_input("TILL", value=date.today(),
                                 min_value=datetime.date(1990, 1, 1))

if st.button("GENERATE BHAVCOPIES"):
    try:
        EOD.download_bhav(my1_date,my2_date)
        #EOD.download_bhav(nselink,bselink, indexlink, possible_index_name)
        # st.success("Done downloading, lets try extracting now")
        #eod_existing_files(path_bhav, path_csv)
    except BadZipFile:
        st.error("BadZipFile")
        pass
