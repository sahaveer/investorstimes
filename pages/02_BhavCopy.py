import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import date
import EOD

#st.set_page_config(page_title="BhavCopy",page_icon=":bar_chart:",layout="wide")
#st.markdown("### Site is in progress \n Shall be launched asap")

with st.sidebar:
    # PATHS OF THIS COMPUTER
    path_bhav = st.text_input("path_bhav",value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/')     #'./bhavcopy/')
    path_csv = st.text_input("path_csv",value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/')        #'./bhavcopy/csv')
    path_download = st.text_input("path_download",value='C:/Users/sahaveer/Downloads/')

my_date = st.date_input("Select date", value=date.today(),
                        min_value=datetime.date(1990, 1, 1))
ddmmmyyyy = my_date.strftime("%d%b%Y")
driver = webdriver.Edge(r"C://Users/sahaveer/PycharmProjects/onlystocks/msedgedriver.exe")
if st.button("Download"):
    # this line is brought from near import lines
    driver = webdriver.Edge(r"C://Users/sahaveer/PycharmProjects/onlystocks/msedgedriver.exe")
    driver.minimize_window()
    EOD.eod_date(driver, ddmmmyyyy,path_bhav,path_csv,path_download)

#Custom CSS to remove header,footer, hamburger icon
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)
