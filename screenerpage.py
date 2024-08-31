from selenium.webdriver.common.by import By
import streamlit as st
import glob
import os
#from time import sleep
import time
import random
import urllib.request
import urllib.parse
from urllib.parse import urlparse
import openpyxl
from openpyxl.utils import get_column_letter
import requests
import nse_bse_search
import fundamentals
import processdriver
import pandas as pd


usermail = "sahaveer@gmail.com"
pswrd = "Qwerty@123"
download_excel_xpath = "/html/body/main/div[3]/div[1]/form/button"
login_button_xpath = "/html/body/main/div[2]/div[2]/form/button"

global bsecodenum_codename
global bsecodename_codenum
bsecodenum_codename,bsecodename_codenum,bsecodenum_fullname,bsecodename_fullname,bsefullname_codenum,bsefullname_codename = nse_bse_search.bsecodenum_bsecodename()
# This gets us the BSE NAME from the DAILY BHAVCOPY THAT WE ARE DOWNLOADING
bsesccode_scname,bsescname_sccode = nse_bse_search.bseSCNAME_SCCODE()

global driver

with st.sidebar:
    # PATHS OF THIS COMPUTER
    #st.info("pls mention here your computer paths")
    path_bhav = 'C:/Users/sahaveer/OneDrive/Documents/bhavcopy/'                #st.text_input("path_bhav",value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/')     #'./bhavcopy/')
    path_csv = 'C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/'        #st.text_input("path_csv",value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/')        #'./bhavcopy/csv')
    #path_download = st.text_input("path_download",value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy')
    path_download = "C:/Users/sahaveer/Downloads/"                              #st.text_input("path_download",value="C:/Users/sahaveer/Downloads/")
    path_to_save = path_download+"Results/"
    type_file = "*.xlsx"

def recently_downloaded_file(path_download, type_file):
    sendfile = ''
    #grabs the last created file in a specified folder
    pick_xlsx = glob.glob(path_download+type_file)
    last_created_file = max(pick_xlsx, key=os.path.getctime)
    send_file = last_created_file.replace("\\","/")
    return send_file

def login_screener(driver):
    driver.get('https://www.screener.in/login/')
    #if driver.find_elements_by_id("id_username"):
    if driver.find_elements(by=By.ID, value="id_username"):
        pass
    else:
        return
    #useridform = driver.find_element_by_id('id_username')
    useridform = driver.find_element(by=By.ID,value='id_username')
    pswrdform = driver.find_element(by=By.ID,value='id_password')
    #pswrdform = driver.find_element_by_id('id_password')
    useridform.send_keys(usermail)
    pswrdform.send_keys(pswrd)
    #if driver.find_elements_by_xpath(login_button_xpath):
    if driver.find_elements(by=By.XPATH, value=login_button_xpath):
        #driver.find_element_by_xpath(login_button_xpath).click()
        driver.find_element(by=By.XPATH, value=login_button_xpath).click()
    else:
        st.error("seems like Screener has changed the Xpath")



def search_screener(driver,code):
    # driver.maximize_window()
    code = str(code)
    consolidated_available = False
    standalone_available = False
    Yearly_data_consolidated = ""
    Quarterly_data_consolidated = ""
    Yearly_data_standalone = ""
    Quarterly_data_standalone = ""

    #if driver.find_elements_by_xpath('/html/body/nav/div[1]/div/div[1]/div/div[3]/div[1]'):

    if driver.find_elements(by=By.XPATH, value='/html/body/nav/div[1]/div/div[1]/div/div[3]/div[1]'):
        pass
    else:
        login_screener(driver)
        #link_consolidated = 'https://www.screener.in/company/'+code+'/consolidated/'
        #link_standalone =  'https://www.screener.in/company/'+code+'/'
        #st.info(f"Inside the search_screener function, we are searching for {code_list[i]}")
                    # FIRST SEARCH IS IN CONSOLIDATED
    try:
        driver.get('https://www.screener.in/company/' + code + '/consolidated/')
        time.sleep(random.uniform(1, 3))
        #time.sleep(2)
        if driver.find_elements(by=By.XPATH, value=download_excel_xpath):
            parsed = urlparse(driver.current_url)
            path_parts = parsed.path.split('/')
            # st.info(f"tryingf in consolidated {path_parts}")
            if len(path_parts) >= 2:
                company_code = path_parts[2]  # gets code from within the screener_url
                driver.find_element(by=By.XPATH, value=download_excel_xpath).click()
                time.sleep(2)
                latest_file = recently_downloaded_file(path_download, type_file)
                book = openpyxl.load_workbook(latest_file)
                # st.info(f"Got {company_code} from the screener site")
                qtr_pnl, df_comp = fundamentals.get_tables(book[fundamentals.tabs[-1]],
                                                        latest_file)  # send a sheet(not whole workbook)
                if not df_comp.eq(0).all().all():
                    # Convert column names to datetime
                    dates = pd.to_datetime(df_comp.columns)
                    # Check if the date range is complete and sequential
                    if len(dates) == 1:
                        Yearly_data_consolidated = "valid"
                    else:
                        # st.info(df_comp.columns)
                        get_month = dates[0].strftime('%b')
                        # st.info(get_month)
                        freq_text = 'A-' + get_month.upper()
                        expected_dates = pd.date_range(start=dates.min(), end=dates.max(), freq=freq_text)
                        # Adjust dates to the end of March for the correct comparison
                        # expected_dates = expected_dates + pd.DateOffset(days=-1)
                        st.info(f"Consolidated Yearly: \ndates are {dates}\nexpected_dates are {expected_dates}")
                        if len(dates) == len(expected_dates) and dates.equals(expected_dates):
                            # st.success("Yearly Consolidated dates are equal")
                            Yearly_data_consolidated = "valid"
                        else:
                            Yearly_data_consolidated = "NA"
                else:
                    Yearly_data_consolidated = "NA"

                if not qtr_pnl.eq(0).all().all():            
                    # Convert column names to datetime
                    dates = pd.to_datetime(qtr_pnl.columns)
                    # Check if the date range is complete and sequential
                    if len(dates) ==1:
                        Quarterly_data_consolidated = "valid"
                    else:
                        expected_dates = pd.date_range(start=dates.min(), end=dates.max(), freq='Q')
                        st.info(f"Consolidated Quarterly: dates are {dates}\n expected_dates are {expected_dates}")
                        if len(dates)==len(expected_dates) and dates.equals(expected_dates):
                            # st.success("Quarterly Consolidated dates are equal")
                            Quarterly_data_consolidated = "valid"
                        else:
                            Quarterly_data_consolidated = "NA"
                else:
                    Quarterly_data_consolidated = "NA"
                
                if Quarterly_data_consolidated == "valid" and Yearly_data_consolidated == "valid":
                    consolidated_available = True
        st.success(f"consolidated_available is {consolidated_available}")
    except Exception as HTTPError:
        st.error(f"HTTPError in consolidated {HTTPError}")
    try:
        driver.get('https://www.screener.in/company/' + code)
        time.sleep(random.uniform(1, 3))
        # time.sleep(2)
        if driver.find_elements(by=By.XPATH, value=download_excel_xpath):
            parsed = urlparse(driver.current_url)
            path_parts = parsed.path.split('/')
            # st.info(f"tryingf in consolidated {path_parts}")
            if len(path_parts) >= 2:
                company_code = path_parts[2]  # gets code from within the screener_url
                driver.find_element(by=By.XPATH, value=download_excel_xpath).click()
                time.sleep(2)
                latest_file = recently_downloaded_file(path_download, type_file)
                book = openpyxl.load_workbook(latest_file)
                qtr_pnl1, df_comp1 = fundamentals.get_tables(book[fundamentals.tabs[-1]],
                                                        latest_file)  # send a sheet(not whole workbook)
                if not df_comp1.eq(0).all().all():
                    # Convert column names to datetime
                    dates1 = pd.to_datetime(df_comp1.columns)
                    # Check if the date range is complete and sequential
                    if len(dates1) == 1:
                        Yearly_data_standalone = "valid"
                    else:
                        expected_dates1 = pd.date_range(start=dates1.min(), end=dates1.max(), freq='A-MAR')
                        st.info(f"Yearly Standalone: \ndates1 is {dates1}\nexpected_dates1 is {expected_dates1}")
                        if len(dates1) == len(expected_dates1) and dates1.equals(expected_dates1):
                            # st.success("Yearly Standalone dates are equal")
                            Yearly_data_standalone = "valid"
                        else:
                            Yearly_data_standalone = "NA"
                else:
                    Yearly_data_standalone = "NA"
                if not qtr_pnl1.eq(0).all().all():            
                    # consolidated_available = True
                    # Convert column names to datetime
                    dates1 = pd.to_datetime(qtr_pnl1.columns)
                    # Check if the date range is complete and sequential
                    if len(dates1) == 1:
                        Quarterly_data_standalone = "valid"                    
                    else:
                        expected_dates1 = pd.date_range(start=dates1.min(), end=dates1.max(), freq='Q')
                        st.info(f"Quarterly Standalone : \ndates1 is {dates1}\nexpected_dates1 is {expected_dates1}")    
                        if len(dates1) == len(expected_dates1) and dates1.equals(expected_dates1):
                            # st.success("Quarterly Standalone dates are equal")
                            Quarterly_data_standalone = "valid"
                        else:
                            Quarterly_data_standalone = "NA"
                else:
                    Quarterly_data_standalone = "NA"
                if Quarterly_data_standalone == "valid" and Yearly_data_standalone == "valid":
                    standalone_available = True
        st.success(f"standalone_available is {standalone_available}")
    except Exception as HTTPError:
        st.error(f"HTTPError in standalone {HTTPError}")

    if consolidated_available or standalone_available:
        if company_code.isdigit():
            company_code = int(company_code)
            save_pickl_as = bsecodenum_codename[company_code].strip()  # + " Consolidated"
            # save_pickl_as = book['Data Sheet']['B1'].value
        else:
            save_pickl_as = company_code.strip()  # + " Consolidated"
        st.info(f"GOT THRU GETTING THE SAVE_PICKLE_AS {save_pickl_as}")

    if consolidated_available and standalone_available:                  # if both consol and stdalone last quarter date is same
        st.info("We got both Standalone and Consolidated results")
        if qtr_pnl1.columns[-1] == qtr_pnl.columns[-1]:
            st.info("Both Standalone and Consolidated have same last quarter date")
            #lets check whose len(columns) is greater
            if len(qtr_pnl.columns) >= len(qtr_pnl1.columns) and len(df_comp.columns) >= len(df_comp1.columns):
                st.success("Consolidated has more columns, So considering CONSOLIDATED results")
                return df_comp,qtr_pnl,save_pickl_as.upper() 
            else:
                st.success("Standalone has more columns, So considering STANDALONE results")
                return df_comp1,qtr_pnl1,save_pickl_as.upper()
            # return df_comp,qtr_pnl,save_pickl_as.upper()
        elif qtr_pnl.columns[-1]<qtr_pnl1.columns[-1]:
            st.success("Standalone has more recent data, So considering Standalone results")
            return df_comp1,qtr_pnl1,save_pickl_as.upper()
        elif qtr_pnl.columns[-1]>qtr_pnl1.columns[-1]:
            st.success("Consolidated has more recent data, So considering CONSOLIDATED results")
            return df_comp,qtr_pnl,save_pickl_as.upper()
        else:
            return None,None,None
        
    elif consolidated_available is False and standalone_available is True:
        st.success("We got only Standalone results")
        return df_comp1,qtr_pnl1,save_pickl_as.upper()
    elif consolidated_available is True and standalone_available is False:
        st.success("We got only Consolidated results")
        return df_comp,qtr_pnl,save_pickl_as.upper()
    else:
        return None,None,None

def search_screener1(driver,code):
    #if driver.find_elements_by_xpath('/html/body/nav/div[1]/div/div[1]/div/div[3]/div[1]'):
    try:
        if driver.find_elements(by=By.XPATH, value='/html/body/nav/div[1]/div/div[1]/div/div[3]/div[1]'):
            #st.info("No download link")
            # return None,None,None
            pass
        else:
            login_screener(driver)
            #link_consolidated = 'https://www.screener.in/company/'+code+'/consolidated/'
            #link_standalone =  'https://www.screener.in/company/'+code+'/'
            #st.info(f"Inside the search_screener function, we are searching for {code_list[i]}")
                        # FIRST SEARCH IS IN CONSOLIDATED

            driver.get('https://www.screener.in/company/' + code + '/consolidated/')
            time.sleep(random.uniform(1, 3))
            # time.sleep(2)
            if driver.find_elements(by=By.XPATH, value=download_excel_xpath):
                # got into consolidated
                parsed = urlparse(driver.current_url)
                path_parts = parsed.path.split('/')
                #st.info(f"tryingf in consolidated {path_parts}")
                if len(path_parts) >= 2:
                    company_code = path_parts[2]                #gets code from within the screener_url

                    driver.find_element(by=By.XPATH, value=download_excel_xpath).click()
                    time.sleep(2)
                    latest_file = recently_downloaded_file(path_download, type_file)
                    book = openpyxl.load_workbook(latest_file)
                    #st.info(f"Got {company_code} from the screener site")
                    if company_code.isdigit():
                        company_code = int(company_code)
                        save_pickl_as = bsecodenum_codename[company_code].strip() #+ " Consolidated"
                        #save_pickl_as = book['Data Sheet']['B1'].value
                    else:
                        save_pickl_as = company_code.strip() #+ " Consolidated"
                    qtr_pnl, df_comp = fundamentals.get_tables(book[fundamentals.tabs[-1]],
                                                               latest_file)  # send a sheet(not whole workbook)
                                                                                                                            # if Quarterly data is all 0, then better to get the standalone report as well
                    if qtr_pnl.eq(0).all().all() :
                        driver.get('https://www.screener.in/company/' + code + '/')
                        # time.sleep(2)
                        time.sleep(random.uniform(1, 3))
                        if driver.find_elements(by=By.XPATH, value=download_excel_xpath):
                            parsed = urlparse(driver.current_url)
                            path_parts = parsed.path.split('/')
                            #st.info(f"Failed in consolidated, so in standalone {path_parts}")
                            if len(path_parts) >= 2:
                                company_code = path_parts[2]
                                #st.info(company_code)
                                driver.find_element(by=By.XPATH, value=download_excel_xpath).click()
                                time.sleep(2)
                                latest_file = recently_downloaded_file(path_download, type_file)
                                # df_comp, comp_name = create_df(latest_file)
                                book = openpyxl.load_workbook(latest_file)
                                if company_code.isdigit():
                                    company_code = int(company_code)
                                    save_pickl_as = bsecodenum_codename[company_code].strip()
                                    #save_pickl_as = book['Data Sheet']['B1'].value
                                else:
                                    save_pickl_as = company_code.strip() #+ "Standalone"
                                qtr_pnl, df_comp = fundamentals.get_tables(book[fundamentals.tabs[-1]],
                                                                           latest_file)  # send a sheet(not whole workbook)
                                return df_comp, qtr_pnl, save_pickl_as.upper()
                            else:
                                st.info("Company name not found in the URL.")
                    else:
                        return df_comp, qtr_pnl, save_pickl_as.upper()
                else:
                    st.info("Company name not found in the URL.")

            else:
                driver.get('https://www.screener.in/company/' + code + '/')
                # time.sleep(2)
                time.sleep(random.uniform(1, 3))
                if driver.find_elements(by=By.XPATH, value=download_excel_xpath):
                    parsed = urlparse(driver.current_url)
                    path_parts = parsed.path.split('/')
                    #st.info(f"tryingf in standalone directly {path_parts}")
                    if len(path_parts) >= 2:
                        company_code = path_parts[2]
                        st.info(company_code)
                        driver.find_element(by=By.XPATH, value=download_excel_xpath).click()
                        time.sleep(2)
                        latest_file = recently_downloaded_file(path_download, type_file)
                        # df_comp, comp_name = create_df(latest_file)
                        book = openpyxl.load_workbook(latest_file)
                        if company_code.isdigit():
                            company_code = int(company_code)
                            save_pickl_as = bsecodenum_codename[company_code] #+ " Standalone"
                            #save_pickl_as = book['Data Sheet']['B1'].value
                        else:
                            save_pickl_as = company_code #+ " Standalone"
                        qtr_pnl, df_comp = fundamentals.get_tables(book[fundamentals.tabs[-1]],
                                                                   latest_file)  # send a sheet(not whole workbook)
                        return df_comp, qtr_pnl, save_pickl_as.upper()
                    else:
                        st.info("Company name not found in the URL.")
                else:
                    return None, None, None
    except Exception as e:
        st.info(e)