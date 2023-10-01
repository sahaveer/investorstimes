# this is to only handle csv files and then copy the context to a TXT file
# UPDATE 2NOV2022 : updated avoid_bse_stocks to avoid stocks which are already available in NSE
# IDEA 3NOV2022 : Got to give an option in website to select the coulmns as per users demand and alos option to select if they want BSE CODE o BSE NAME
# IDEA 3NOV2022: Would be better if i could avoid all the gaps in the last of BSE NAMES

import re
import time
from time import sleep
import datetime
from datetime import timedelta
from datetime import date
import shutil
import glob,os
import os.path

import urllib.request
from urllib.error import HTTPError
import csv
import pandas as pd
import requests
from zipfile import ZipFile
import zipfile
from zipfile import ZipFile
from zipfile import BadZipFile

from io import BytesIO

from selenium import webdriver
import streamlit as st

from scriptstoavoid import *

#st.title("EOD BHAVCOPY")
# PATHS OF THIS COMPUTER
#path_bhav = 'C:/Users/sahaveer/OneDrive/Documents/bhavcopy/'
#path_csv = "C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/"
#path_download = 'C:/Users/sahaveer/Downloads/'

# WORKIGN ON DATE FORMATS FROM CSV STRING NAMES
mnth_dict = {'JAN':'01' , 'FEB':'02' , 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10', 'NOV':'11', 'DEC':'12'}

def empty_folder(folder_path):
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)


def main():
    #with st.sidebar:
        # PATHS OF THIS COMPUTER
        #st.info("pls mention here your computer paths")
        #path_bhav = st.text_input("path_bhav", value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/')  # './bhavcopy/')
        #path_csv = st.text_input("path_csv",value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/')  # './bhavcopy/csv')
        #path_download = st.text_input("path_download", value='C:/Users/sahaveer/Downloads/')

    col1, col2 = st.columns([1, 1])
    with col1:
        my1_date = st.date_input("FROM", value=date.today(),
                                 min_value=datetime.date(1990, 1, 1))
    with col2:
        if my1_date is not date.today():
            my2_date = st.date_input("TILL", value=min(my1_date + timedelta(60), date.today()),
                                     min_value=datetime.date(1990, 1, 1))
        else:
            my2_date = st.date_input("TILL", value=date.today(),
                                     min_value=datetime.date(1990, 1, 1))
    if st.button("GENERATE BHAVCOPIES"):
        try:
            folder_to_empty = "./bhavfiles"
            empty_folder(folder_to_empty)
            #st.write("Going to download_bhav Function")
            download_bhav(my1_date, my2_date)
            # st.success("Done downloading, lets try extracting now")
            # eod_existing_files(path_bhav, path_csv)
        except BadZipFile:
            st.error("BadZipFile")
            pass



def download_bhav(my1_date,my2_date):              #nselink,bselink,indexlink,possible_index_name):
    ddmmmyyyy1 = my1_date.strftime("%d%b%Y")
    ddmmmyyyy2 = my2_date.strftime("%d%b%Y")
    created_zip = ZipFile("EOD.zip", "w")
    created_zip.close()
    delta = timedelta(days=1)
    files_list = []
    ddmmmyyyy_list = []
    ddmmmyyyy = ddmmmyyyy1
    while my1_date <= my2_date:
        ddmmmyyyy = my1_date.strftime("%d%b%Y")
        weekday_num = datetime.datetime.strptime(ddmmmyyyy, '%d%b%Y').weekday()
        if weekday_num == 5 or weekday_num == 6:
            my1_date += timedelta(1)
            pass
        else :
            #print(ddmmmyyyy)
            ddmmmyyyy_list.append(ddmmmyyyy)
            my1_date += timedelta(1)

    #st.write(ddmmmyyyy_list)
    bhav_date_zip(ddmmmyyyy_list)

    st.markdown("____")
    st.markdown("**Download your copy and PLS spread YOUR LOVE by sharing website to NEAR and DEAR one\'s**")
    st.markdown("____")

def bhav_date_zip(ddmmmyyyy_list):             #ddmmmyyyy and media_group are lists here
    # EXTRACT fro mNSE DB or download data and update in Database
    created_zip = ZipFile("./bhavfiles/EOD.zip", "w")
    created_zip.close()
    EOD_file = f"./bhavfiles/EOD.zip"
    for ddmmmyyyy in ddmmmyyyy_list:
        yyyymmdd, nse_full_link, possible_fullbhav_name, txt2_name, indexlink, possible_index_name, txt1_name, bselink, fnolink = get_links_txtnames(ddmmmyyyy)
        # NSE FILE
        try:
            result = ""
            result = nse_file(nse_full_link, possible_fullbhav_name, txt2_name)
            print(f"NSE returned {result}")
            if result == "success":
                #st.success(txt2_name)
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt2_name)
                st.success("DONE NSE BHAVCOPY FOR " + yyyymmdd)
            else:
                pass
        except:
            st.error("Failed to download INDEX bhavcopy")
            pass
        #  DOWNLOADING INDEX FILE
        try:  # INDEX FILE - DOWNLOADING
            txt1_name = index_file(indexlink, possible_index_name, txt1_name)
            print(f'Index file returned : {txt1_name}')
            if os.path.exists(txt1_name):
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt1_name)
                st.success("DONE BSE BHAVCOPIES FOR " + yyyymmdd)

        except:
            st.error("Failed to download INDEX bhavcopy")
            pass

        try:
            txt3_name, txt3_name1 = bse_file(bselink, yyyymmdd)
            print(f"Succesfully got data from BSE site {txt3_name}")
            if os.path.exists(txt3_name) and os.path.exists(txt3_name1):
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt3_name)
                    m_zip.write(txt3_name1)
                st.success("DONE BSE BHAVCOPY FOR " + yyyymmdd)
        except:
            st.error("Failed to download INDEX bhavcopy")
            pass

        try:
            txt4_name, txt5_name = fno_file(fnolink, yyyymmdd)
            print(f"Succesfully got data from BSE site {txt4_name}")
            if os.path.exists(txt4_name) and os.path.exists(txt5_name):
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt4_name)
                    m_zip.write(txt5_name)
                st.success("DONE INDEX BHAVCOPY FOR " + yyyymmdd)
        except:
            st.error("Failed to download F&O bhavcopy")
            pass

    with open(EOD_file, "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="EOD.zip",
            mime="application/octet-stream"
        )


def get_links_txtnames(ddmmmyyyy):
    mmm_to_d = str(ddmmmyyyy[2:5].upper())
    mm_to_d = str(mnth_dict[mmm_to_d.upper()])
    dd_to_d = str(ddmmmyyyy[0:2])
    yy_to_d = str(ddmmmyyyy[-2:])
    yyyy_to_d = str(ddmmmyyyy[-4:])
    yyyymmdd = yyyy_to_d + mm_to_d + dd_to_d

    # https://archives.nseindia.com/products/content/sec_bhavdata_full_30122022.csv
    # https://www1.nseindia.com/content/historical/EQUITIES/2019/SEP/cm30SEP2019bhav.csv.zip
    nselink = 'https://www1.nseindia.com/content/historical/EQUITIES/' + yyyy_to_d + '/' + mmm_to_d + '/cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv.zip'
    possible_nse_name = 'cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'full.csv'
    # NSEFULLLINK GIVES DELIVERY DATA AS WELL
    nse_full_link = "https://archives.nseindia.com/products/content/sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    possible_fullbhav_name = "sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    txt2_name = './bhavfiles/' + yyyy_to_d + mm_to_d + dd_to_d + "_" + "NSE.txt"

    # indexlink = 'https://www1.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
    indexlink = 'https://archives.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
    possible_index_name = 'ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d
    txt1_name = './bhavfiles/' + yyyy_to_d + mm_to_d + dd_to_d + "_" + "INDEX.txt"

    # FOR bselink and fnolink yyyymmdd is required and not txtnames
    bselink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + dd_to_d + mm_to_d + yy_to_d + '_CSV.ZIP'
    fnolink = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + yyyy_to_d + "/" + mmm_to_d + "/fo" + dd_to_d + mmm_to_d + yyyy_to_d + "bhav.csv.zip"

    return yyyymmdd,nse_full_link, possible_fullbhav_name, txt2_name, indexlink, possible_index_name, txt1_name, bselink, fnolink

def csv_download(full_link,possible_bhav_name):             # CSV files for NSE and INDEX
    csvbhav_path = './bhavfiles/' + possible_bhav_name
    with urllib.request.urlopen(full_link, timeout=5) as test_file, open(csvbhav_path, 'w',newline="") as f:
        f.write(test_file.read().decode())
    return csvbhav_path
def nse_file(nse_full_link,possible_fullbhav_name,txt2_name):
    try:
        bhav_csv_path = csv_download(nse_full_link,possible_fullbhav_name)
        date_nse = str(possible_fullbhav_name[18:20])
        mnth_nse = str(possible_fullbhav_name[20:22])
        yr_nse = str(possible_fullbhav_name[22:26])
        yyyymmdd = yr_nse + mnth_nse + date_nse
        first_lines = pd.read_csv(bhav_csv_path, nrows=10)
        for i in range(len(first_lines[' DATE1'])):
            date_nse_cell = first_lines[' DATE1'][i][1:3]
            mnth_format_cell = first_lines[' DATE1'][i][4:7]
            mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
            yr_nse_cell = str(first_lines[' DATE1'][i][8:])
            yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
            # st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)
        if yyyymmdd == yyyymmdd_cell:
            with open(bhav_csv_path, 'r') as reading:
                nse_full_file = csv.DictReader(reading)
                with open(txt2_name, 'w') as txt:
                    txt.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME, OI" + "\n")
                    for line in nse_full_file:
                        if line[' SERIES'] not in avoid_series:
                            if line['SYMBOL'] not in avoid_stocks:
                                txt.write(
                                    line['SYMBOL'] + "," + str(yyyymmdd) + "," + line[' OPEN_PRICE'] + "," +
                                    line[' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[' CLOSE_PRICE'] + "," + line[' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")
            return "success"
        else:
            return "fail"
    except Exception as TimedoutError:
        return "fail"
def index_file(indexlink,possible_index_name,txt1_name):
    try:
        possible_index_name = possible_index_name + '.csv'
        print("entered INDEX download function")
        bhav_csv_path = csv_download(indexlink,possible_index_name)
        # INDEX FILE
        dd = str(possible_index_name.split('.')[0][-8:-6])
        mm = str(possible_index_name.split('.')[0][-6:-4])
        yyyy = str(possible_index_name.split('.')[0][-4:])
        yyyymmdd = yyyy + mm + dd
        with open(bhav_csv_path, 'r') as reading:
            index_file = csv.DictReader(reading)
            with open(txt1_name, 'w') as txt:
                txt.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                for line in index_file:
                    # txt.write('\'' + line['Index Name'] + "\',")       # FOR WRITING INDEX NAMES INTO TXT
                    if line['Index Name'] in replace_index.keys():
                        txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + ","
                                  + line['High Index Value'] + "," + line['Low Index Value'] + "," + line['Closing Index Value'] + "," + line['Volume'] + "\n")
                    else:
                        txt.write(
                            line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                'Closing Index Value'] + "," + line['Volume'] + "\n")
            return txt1_name
    except Exception as TimedoutError:
        return "fail"

def zip_csv_download(link,file_name):
    print("Entered zip_csv_dowonlaod function")
    # Add a User-Agent header to the request
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    with urllib.request.urlopen(link, timeout=15) as response:
        with open(file_name, 'wb') as file:
            file.write(response.read())
    # OPENS DOWNLOADED ZIP FILE AND EXTRACTS CSV FILE
    with ZipFile(file_name, 'r') as zip:
        # list all the contents of the zip file
        print("Getting into infolist to get the filename")
        for zipinfo in zip.infolist():
            with zip.open(zipinfo) as file:
                file2 = str(zipinfo.filename)
        # print("Copied textfile name")
        zip.extractall('./bhavfiles/')
        # print("Extracted zipfile succesfully")
    return file2
def bse_file(bselink,yyyymmdd):
    try:
        print("entered Bse download function")
        bse_file_name = './bhavfiles/bse_temp_file.zip'
        csv_path = zip_csv_download(bselink,bse_file_name)
        print(csv_path)
        csv_path = './bhavfiles/' + csv_path
        print(csv_path)
        print("lets read CSV file now")
        #txt3_name = './bhavfiles/' + file2.split('.CSV')[0] + '.txt'
        txt3_name = './bhavfiles/' + yyyymmdd + "_" + "BSE.txt"
        txt3_name1 = './bhavfiles/' + yyyymmdd + "_" + "BSE_code.txt"
        with open(csv_path, 'r') as reading:
            bse_full_file = csv.DictReader(reading)
            print("Read the CSV file, lets write to txt now")
            with open(txt3_name, 'w') as txt:
                txt.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                for line in bse_full_file:
                    #print(line)
                    if line['SC_GROUP'] not in avoid_bse_series:
                        if line['SC_NAME'] not in avoid_bse_stocks:
                            if line['SC_NAME'] not in avoid_stocks:
                                txt.write(line['SC_NAME'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
        with open(csv_path, 'r') as reading:
            bse_full_file = csv.DictReader(reading)
            print("Read the CSV file, lets write to txt now")
            with open(txt3_name1, 'w') as txt:
                txt.write("TICKERCODE, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                for line in bse_full_file:
                    if line['SC_GROUP'] not in avoid_bse_series:
                        if line['SC_NAME'] not in avoid_bse_stocks:
                            if line['SC_NAME'] not in avoid_stocks:
                                txt.write(line['SC_CODE'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
        return txt3_name,txt3_name1
    except Exception as TimedoutError:
        return "fail"
def fno_file(fnolink,yyyymmdd):
    try:
        print("entered FNO download function")
        fno_file_name = './bhavfiles/fno_temp_file.zip'
        csv_path = zip_csv_download(fnolink,fno_file_name)
        csv_path = './bhavfiles/' + csv_path
        print("lets read CSV file now")
        txt4_name = './bhavfiles/' + yyyymmdd + "_" + "FUTURES.txt"
        txt5_name = './bhavfiles/' + yyyymmdd + "_" + "INDEX OPTIONS.txt"
        with open(csv_path, 'r') as reading:
            fno_full_file = csv.DictReader(reading)
            # first_row = next(fno_full_file)
            unique_script = ""
            roman_val = {'1': '-I', '2': '-II', '3': '-III', '4': '-IV', '5': '-V', '6': '-VI', '7': '-VII',
                         '8': '-VIII', '9': '-IX', '10': '-X'}
            with open(txt4_name, 'w') as txt:
                txt.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME,OI" + "\n")
                for line in fno_full_file:
                    if line["OPTION_TYP"] == "XX":  # FOR FUTURES
                        # FOR ME : to get as "BANKNIFTY EXP_DATE"
                        #txt.write(line['SYMBOL'] + " " + line['EXPIRY_DT'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," +line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS'] + line['OPEN_INT'] + "\n")
                        # as per Bhavcopy Downloader software
                        if line['SYMBOL'] != unique_script:
                            txt.write(line['SYMBOL'] + "-I" + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS']+ "," + line['OPEN_INT'] + "\n")
                            unique_script = line['SYMBOL']
                            count = 1
                        else:
                            count += 1
                            txt.write(line['SYMBOL'] + roman_val[str(count)] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS']+ "," + line['OPEN_INT'] + "\n")

        with open(csv_path, 'r') as reading:
            fno_full_file = csv.DictReader(reading)
            # name for me shud be "NIFTY 43500CE exp_date"
            with open(txt5_name, 'w') as txt1:
                txt1.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME,OI" + "\n")
                for line in fno_full_file:
                    if line["INSTRUMENT"] == "OPTIDX" and line["OPEN"] != "0" and line["HIGH"] != "0" and line["LOW"] != "0" and line["CLOSE"] != "0":  # options for INDEX
                        txt1.write(line['SYMBOL'] + " " + line["STRIKE_PR"] + line["OPTION_TYP"] + " " + line["EXPIRY_DT"] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS'] + line['OPEN_INT'] + "\n")
        return txt4_name,txt5_name
    except Exception as TimedoutError:
        return "fail"




if __name__ == '__main__':
    main()
