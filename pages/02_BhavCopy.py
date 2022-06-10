import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import date

st.set_page_config(page_title="BhavCopy",page_icon=":bar_chart:",layout="wide")

st.markdown("### Site is in progress \n Shall be launched asap")
my_date = st.date_input("Select date", value=date.today(),
                        min_value=datetime.date(1990, 1, 1))
ddmmmyyyy = my_date.strftime("%d%b%Y")
driver = webdriver.Edge(r"C://Users/sahaveer/PycharmProjects/onlystocks/msedgedriver.exe")
if st.button("Download"):
    EOD.eod_date(driver, ddmmmyyy)

#Custom CSS to remove header,footer, hamburger icon
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)