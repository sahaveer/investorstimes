import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import date
import EOD

st.title("BHAVCOPY NSE especially for AMIBROKER USERS")
mnth_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}

my1_date = st.date_input("DATE PLS", value=date.today(),
                            min_value=datetime.date(1990, 1, 1))
ddmmmyyyy1 = my1_date.strftime("%d%b%Y")
if st.button("CREATE BHAV"):
    # downloads links from nse and bse
    mmm_to_d = str(ddmmmyyyy1[2:5].upper())
    mm_to_d = str(mnth_dict[mmm_to_d])
    dd_to_d = str(ddmmmyyyy1[0:2])
    yy_to_d = str(ddmmmyyyy1[-2:])
    yyyy_to_d = str(ddmmmyyyy1[-4:])
    nselink = 'https://www1.nseindia.com/content/historical/EQUITIES/' + yyyy_to_d + '/' + mmm_to_d + '/cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv.zip'
    bselink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + dd_to_d + mm_to_d + yy_to_d + '_CSV.ZIP'
    indexlink = 'https://www1.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
    #possible_csvfilename = 'cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv'
    #possible_txtname = 'cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.txt'
    possible_index_name = "ind_close_all_" + dd_to_d + mm_to_d + yyyy_to_d
    #st.write(possible_txtname)
    #st.write(possible_csvfilename)
    #st.write(f'NSE link is : ' + nselink)
    st.write(f'BSE File is still in Progress, instead try downloading the link : ' + bselink)
    #st.write(f'Index link is : ' + indexlink)
    try:
        EOD.download_bhav(nselink,bselink, indexlink, possible_index_name)
        # st.success("Done downloading, lets try extracting now")
        #eod_existing_files(path_bhav, path_csv)
    except BadZipFile:
        st.error("BadZipFile")
        pass
