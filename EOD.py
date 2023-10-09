# this is to only handle csv files and then copy the context to a TXT file
# UPDATE 2NOV2022 : updated avoid_bse_stocks to avoid stocks which are already available in NSE
# IDEA 3NOV2022 : Got to give an option in website to select the coulmns as per users demand and alos option to select if they want BSE CODE o BSE NAME
# IDEA 3NOV2022: Would be better if i could avoid all the gaps in the last of BSE NAMES

import csv
import datetime
from datetime import timedelta
import glob,os
import shutil
import zipfile
from zipfile import ZipFile
from zipfile import BadZipFile
import requests
from io import BytesIO
import urllib.request
from selenium import webdriver
from time import sleep
from datetime import date
import streamlit as st
import pandas as pd

from scriptstoavoid import *
import bhavcopy_url

def main():
    driver = webdriver.Edge(r"C:/Users/sahaveer/PycharmProjects/msedgedriver.exe")
    driver.minimize_window()
    with st.sidebar:
        # PATHS OF THIS COMPUTER
        st.info("pls mention here your computer paths")
        path_bhav = st.text_input("path_bhav", value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/')  # './bhavcopy/')
        path_csv = st.text_input("path_csv",
                                 value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/')  # './bhavcopy/csv')
        path_download = st.text_input("path_download", value='C:/Users/sahaveer/Downloads/')

    my_date = st.date_input("Select date", value=date.today(),
                            min_value=datetime.date(1990, 1, 1))
    ddmmmyyyy = my_date.strftime("%d%b%Y")
    if st.button("Download"):
        eod_date(driver, ddmmmyyyy, path_bhav, path_csv, path_download)
    st.write("___")
    if st.button("Existing"):
        eod_existing_files(path_bhav, path_csv)
        st.write("done EXISTing files")
    st.write("___")
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
            download_bhav(my1_date, my2_date)
            # download_bhav(nselink,bselink, indexlink, possible_index_name)
            # st.success("Done downloading, lets try extracting now")
            # eod_existing_files(path_bhav, path_csv)
        except BadZipFile:
            st.error("BadZipFile")
            pass


def driver_get(url):
    driver.get(url)
def eod_extract(file):
    if (just_filename[:2] == 'EQ'):  # BSE STOCKS
        # st.success("Working on BSE Data : " + just_filename)
        date_bse = str(file[-10:-8])
        mnth_bse = str(file[-8:-6])
        yr_bse = str(file[-6:-4])
        yyyymmdd = str(20) + yr_bse + mnth_bse + date_bse
        with open(file, 'r') as reading:
            file1 = csv.DictReader(reading)
            # file_list = list(file1)
            # st.write(type(file_list[0]['TIMESTAMP']))
            bse_filename = str(file[-10:-4])
            # amibroker_date_format = input()
            with open(path_bhav + 'bse' + bse_filename + '.txt', 'w') as txt:
                for line in file1:
                    if line['SC_GROUP'] not in avoid_bse_series:
                        if line['SC_NAME'] not in avoid_bse_stocks and avoid_stocks:
                            txt.write(
                                line['SC_CODE'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
        #shutil.move(file, path_csv)
        st.success('DONE BSE ' + file)

    elif (just_filename[:2] == 'cm'):  # if(file[-19:-17]=="cm"):                      # NSE STOCKS
        # st.write("Working on NSE Data : " + just_filename)
        date_nse = str(file[-17:-15])
        mnth_format = str(file[-15:-12])
        mnth_nse = mnth_dict[mnth_format]
        yr_nse = str(file[-12:-8])
        yyyymmdd = yr_nse + mnth_nse + date_nse
        with open(file, 'r') as reading:
            file1 = csv.DictReader(reading)
            nse_filename = str(file[-17:-8])
            # amibroker_date_format = input()
            with open(path_bhav + 'nse' + nse_filename + '.txt', 'w') as txt:
                for line in file1:
                    if line['SERIES'] not in avoid_series:
                        if line['SYMBOL'] not in avoid_stocks:
                            txt.write(
                                line['SYMBOL'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                line['LOW'] + "," + line['CLOSE'] + "," + line['TOTTRDQTY'] + "\n")
            # st.write(f'files saved as nse' + nse_filename)
        #shutil.move(file, path_csv)
        st.success('DONE NSE ' + file)

    elif (just_filename[:3] == 'ind'):  # if(file[-19:-17]=="cm"):                      # NSE STOCKS
        only_filename = just_filename.split('.')[0]
        # st.write("Working on INDEX Data : " + only_filename)
        dd = str(only_filename[-8:-6])
        mm = str(only_filename[-6:-4])
        yyyy = str(only_filename[-4:])
        yyyymmdd = yyyy + mm + dd
        with open(file, 'r') as reading:
            index_file = csv.DictReader(reading)
            index_filename = just_filename
            with open(path_bhav + 'nse' + index_filename + '.txt', 'w') as txt:
                for line in index_file:
                    # txt.write('\'' + line['Index Name'] + "\',")       # FOR WRITING INDEX NAMES INTO TXT
                    if line['Index Name'] in replace_index.keys():
                        txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line[
                            'Open Index Value'] + "," + line[
                                      'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                      'Closing Index Value'] + "," + line['Volume'] + "\n")
                    else:
                        txt.write(
                            line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                'Closing Index Value'] + "," + line['Volume'] + "\n")

def nse_list(path_bhav,path_csv):               #NOT BEING USED NOW
    last_cm = max(glob.glob(path_csv + 'sec' + '*.csv'), key=os.path.getctime)
    cm_file = last_cm.replace("\\", "/")
    st.success(f"Reading NSE file {cm_file}")
    with open(cm_file, 'r') as reading:
        file1 = csv.DictReader(reading)
        with open(path_bhav + 'nselist' + '.txt', 'w') as txt:
            for line in file1:
                if line[' SERIES'] not in avoid_series:
                    if line['SYMBOL'] not in avoid_stocks:
                        txt.write(line['SYMBOL'] + "\n")
    st.success('DONE NSE List')

#this writes BSE NAMES AS CODE NUMBERS
def bse_list(path_bhav,path_csv):               # NOT BEING USED NOW
    last_cm = max(glob.glob(path_csv + 'EQ' + '*.csv'), key=os.path.getctime)
    cm_file = last_cm.replace("\\", "/")
    with open(cm_file, 'r') as reading:
        file1 = csv.DictReader(reading)
        with open(path_bhav + 'bselist' + '.txt', 'w') as txt:
            for line in file1:
                if line['SC_GROUP'] not in avoid_bse_series :
                    if line['SC_NAME'] not in avoid_bse_stocks and avoid_stocks:
                        txt.write(line['SC_CODE'] + "\n")
    st.success('DONE BSE List')

def eod_existing_files(path_bhav,path_csv):
    #st.success(" ok boss, let me work on the existing CSV files now")
    #for filepath in glob.glob("./bhavcopy/*.csv",recursive=False):
    for filepath in glob.glob(r"{}*.csv".format(path_bhav), recursive=False):
        file = filepath.replace("\\","/")
        just_filename = file.split('/')[-1]
        if (os.path.isfile(path_csv + just_filename)):
            st.warning(f'file ' + just_filename + ' already exists')
            pass
        else:
            if (just_filename[:2] == 'EQ'):  # BSE STOCKS
                #st.write("Working on BSE Data : " + file)
                date_bse = str(file[-10:-8])
                mnth_bse = str(file[-8:-6])
                yr_bse = str(file[-6:-4])
                yyyymmdd = str(20) + yr_bse + mnth_bse + date_bse
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    # file_list = list(file1)
                    # st.write(type(file_list[0]['TIMESTAMP']))
                    #bse_filename = path_bhav + '/' + just_filename.split('.CSV')[0] + '.txt'    #str(file[-10:-4])
                    bse_filename = path_bhav + '/' + yyyymmdd + "_" + "BSE.txt"
                    #st.write(bse_filename)
                    with open(bse_filename , 'w') as txt:
                        txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in file1:
                            if line['SC_GROUP'] not in avoid_bse_series :
                                if line['SC_NAME'] not in avoid_bse_stocks and avoid_stocks:
                                    txt.write(
                                        line['SC_NAME'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                        line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    #bse_filename1 = path_bhav + '/' + just_filename.split('.CSV')[0] + 'Code.txt'  # str(file[-10:-4])
                    bse_filename1 = path_bhav + '/' + yyyymmdd + "_" + "BSE_code.txt"
                    with open(bse_filename1, 'w') as txt:
                        txt.write("TICKERCODE, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in file1:
                            txt.write(
                                line['SC_CODE'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," +
                                line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")

                shutil.move(file, path_csv)
                st.success('DONE BSE ' + file)

            elif (just_filename[:2] == 'cm'):  #if(file[-19:-17]=="cm"):                      # NSE STOCKS
                #st.write("Working on NSE Data : " + just_filename)
                date_nse = str(file[-17:-15])
                mnth_format = str(file[-15:-12])
                mnth_nse = mnth_dict[mnth_format]
                yr_nse = str(file[-12:-8])
                yyyymmdd = yr_nse+mnth_nse+date_nse
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    nse_filename = str(file[-17:-8])
                    #amibroker_date_format = input()
                    with open(path_bhav+'nse'+nse_filename+'.txt','w') as txt :
                        txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in file1:
                            if line['SERIES'] not in avoid_series:
                                if line['SYMBOL'] not in avoid_stocks:
                                    txt.write(line['SYMBOL'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['TOTTRDQTY'] + "\n")
                    #st.write(f'files saved as nse' + nse_filename)
                shutil.move(file, path_csv)
                st.success('DONE NSE ' + file)

            elif (just_filename[:3] == 'ind'):  #if(file[-19:-17]=="cm"):                      # NSE STOCKS
                only_filename = just_filename.split('.')[0]
                #st.write("Working on INDEX Data : " + only_filename)
                dd = str(only_filename[-8:-6])
                mm = str(only_filename[-6:-4])
                yyyy = str(only_filename[-4:])
                yyyymmdd = yyyy+mm+dd
                with open(file,'r') as reading:
                    index_file = csv.DictReader(reading)
                    index_filename = just_filename
                    st.write(path_bhav + 'nse' + index_filename + '.txt')
                    with open(path_bhav+'nse'+index_filename+'.txt','w') as txt:
                        txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                        for line in index_file:
                            #txt.write('\'' + line['Index Name'] + "\',")       # FOR WRITING INDEX NAMES INTO TXT
                            if line['Index Name'] in replace_index.keys():
                                txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                    'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                    'Closing Index Value'] + "," + line['Volume'] + "\n" )
                            else :
                                txt.write(line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                    'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                              'Closing Index Value'] + "," + line['Volume'] + "\n")
                shutil.move(file, path_csv)
                st.success('DONE INDICES ' + file)
            elif (just_filename[:3] == 'sec'):
                try:
                    st.write(just_filename)
                    date_nse = str(just_filename[18:20])
                    mnth_nse = str(just_filename[20:22])
                    yr_nse = str(just_filename[22:26])
                    yyyymmdd = yr_nse + mnth_nse + date_nse
                    st.write(yyyymmdd)
                    txt1_name = path_bhav + just_filename.split('.csv')[0] + '.txt'
                    st.write(txt1_name)
                    first_lines = pd.read_csv(file, nrows=10)
                    print(first_lines)
                    for i in range(len(first_lines[' DATE1'])):
                        print("Reading the date now")
                        save_cell_temp = str(first_lines[' DATE1'][i]).strip()
                        date_nse_cell = save_cell_temp[0:2]
                        print(date_nse_cell)
                        mnth_format_cell = save_cell_temp[3:6]
                        mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
                        print(mnth_format_cell)
                        print(mnth_nse_cell)
                        yr_nse_cell = str(save_cell_temp[7:])
                        print(yr_nse_cell)
                        yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
                        st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)
                        '''
                        date_nse_cell = first_lines[' DATE1'][i][0:2]
                        print(date_nse_cell)
                        mnth_format_cell = first_lines[' DATE1'][i][3:6]
                        mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
                        print(mnth_format_cell)
                        print(mnth_nse_cell)
                        yr_nse_cell = str(20) + str(first_lines[' DATE1'][i][7:])
                        print(yr_nse_cell)
                        yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
                        st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)'''
                    if yyyymmdd == yyyymmdd_cell:
                        with open(file, 'r') as reading:
                            nse_full_file = csv.DictReader(reading)
                            print("Read csv file")
                            with open(txt1_name, 'a') as txt:
                                txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, TRADED_QTY, DELIVERABLE_QTY" + "\n")
                                print("STARTED WERITING TEXT FILE")
                                for line in nse_full_file:
                                    if line[' SERIES'] not in avoid_series:
                                        if line['SYMBOL'] not in avoid_stocks:
                                            txt.write(
                                                line['SYMBOL'] + "," + str(yyyymmdd) + "," + line[' OPEN_PRICE'] + "," +
                                                line[
                                                    ' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[
                                                    ' CLOSE_PRICE'] + "," + line[
                                                    ' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")
                        st.success("Created file in " + txt1_name)
                    else:
                        st.error("the DATE and THE FILE GENERATED ARE DIFFERENT. THUS SKIPPING")
                    shutil.move(file, path_csv)
                    st.success('DONE FULLBHAV ' + file)

                except:
                    pass

# this will download files locally in the local computer.
def download_all_data(driver,indexlink, bselink, nselink,path_bhav,path_csv,path_download,nse_full_link,possible_fullbhav_name):
    # DOWNLOAD INDEX FILE and MOVE TO BHAVCOPY LOCATION
    try:
        index_d = driver.get(indexlink)
        sleep(2)
        last_created_file = max(glob.glob(path_download + '*.csv'), key=os.path.getctime)
        shutil.move(last_created_file, path_bhav)
    except:
        st.warning('unable to download Index file')
    # DOWNLOAD BSE FILE and MOVE TO BHAVCOPY LOCATION
    try:
        bse_d = driver.get(bselink)
        # bse_zip = ZipFile(BytesIO(bse_d.content))
        # bse_zip.extractall(r'{}'.format(path_bhav))
        sleep(2)
        last_created_file = max(glob.glob(path_download + '*.zip'), key=os.path.getctime)
        shutil.move(last_created_file, path_bhav)
        last_zip = max(glob.glob(path_bhav + '*.zip'), key=os.path.getctime)
        try:
            with ZipFile(last_zip, 'r') as zip:
                # list all the contents of the zip file
                #st.write(f'{zip.infolist()}')
                zip.extractall(path_bhav)
        except:
            st.warning('Couldnt Extract bse file')
    except:
        st.warning('Couldnt Download bse file')

    # DOWNLOAD NSE FILE THROUGH REQUESTS
    try:
        nse_d = requests.get(nselink)
        nse_zip = ZipFile(BytesIO(nse_d.content))
        nse_zip.extractall(r'{}'.format(path_bhav))
    except:
        st.warning("Couldnt download nse file")
    try:
        with urllib.request.urlopen(nse_full_link) as test_nse_file, open(f'' + path_bhav + '/' + possible_fullbhav_name, 'w',
                                                                          newline="") as f:
            f.write(test_nse_file.read().decode())
        date_nse = str(possible_fullbhav_name[18:20])
        # st.write(date_nse)
        mnth_nse = str(possible_fullbhav_name[20:22])
        # st.write(mnth_nse)
        yr_nse = str(possible_fullbhav_name[22:26])
        # st.write(yr_nse)
        yyyymmdd = yr_nse + mnth_nse + date_nse
        txt1_name = possible_fullbhav_name.split('.csv')[0] + '.txt'
        first_lines = pd.read_csv(f'' + path_bhav + '/' +possible_fullbhav_name, nrows=10)
        for i in range(len(first_lines[' DATE1'])):
            date_nse_cell = first_lines[' DATE1'][i][1:3]
            mnth_format_cell = first_lines[' DATE1'][i][4:7]
            mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
            yr_nse_cell = str(first_lines[' DATE1'][i][8:])
            yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
            # st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)
        if yyyymmdd == yyyymmdd_cell:
            with open(f'' + path_bhav + '/' +possible_fullbhav_name, 'r') as reading:
                nse_full_file = csv.DictReader(reading)
                with open(f'' + path_bhav + '/' + txt1_name, 'a') as txt:
                    txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, TRADED_QTY, DELIVERABLE_QTY" + "\n")
                    for line in nse_full_file:
                        if line[' SERIES'] not in avoid_series:
                            if line['SYMBOL'] not in avoid_stocks:
                                txt.write(
                                    line['SYMBOL'] + "," + str(yyyymmdd) + "," + line[' OPEN_PRICE'] + "," +
                                    line[
                                        ' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[
                                        ' CLOSE_PRICE'] + "," + line[
                                        ' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")
            st.write("DONE FULL BHAVCOPY:   " + yyyymmdd)
            shutil.move(path_bhav + '/' + possible_fullbhav_name, path_csv)
        else:
            st.error("the DATE and THE FILE GENERATED ARE DIFFERENT. THUS SKIPPING")
    except:
        pass

# This EODDATE function requires other functions viz., download_all_data, eod_existing_files.
def eod_date(driver,ddmmmyyyy,path_bhav,path_csv,path_download):
    # downloads links from nse and bse
    mmm_to_d = str(ddmmmyyyy[2:5].upper())
    mm_to_d = str(mnth_dict[mmm_to_d])
    dd_to_d = str(ddmmmyyyy[0:2])
    yy_to_d = str(ddmmmyyyy[-2:])
    yyyy_to_d = str(ddmmmyyyy[-4:])
    nselink = 'https://www1.nseindia.com/content/historical/EQUITIES/' + yyyy_to_d + '/' + mmm_to_d + '/cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv.zip'
    bselink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + dd_to_d + mm_to_d + yy_to_d + '_CSV.ZIP'
    indexlink = 'https://www1.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
    nse_full_link = "https://archives.nseindia.com/products/content/sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    possible_fullbhav_name = "sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    st.write(f'NSE link is : ' + nselink)
    st.write(f'BSE link is : ' + bselink)
    st.write(f'Index link is : ' + indexlink)
    try:
        download_all_data(driver,indexlink, bselink, nselink,path_bhav,path_csv,path_download,nse_full_link,possible_fullbhav_name)
        #st.success("Done downloading, lets try extracting now")
        eod_existing_files(path_bhav,path_csv)
    except BadZipFile:
        pass


def index_file(indexlink,possible_index_name,txt1_name):
    # INDEX FILE
    with urllib.request.urlopen(indexlink) as testfile, open(f'./bhavfiles/' + possible_index_name + '.csv','w',newline="") as f:
        f.write(testfile.read().decode())
    dd = str(possible_index_name[-8:-6])
    mm = str(possible_index_name[-6:-4])
    yyyy = str(possible_index_name[-4:])
    yyyymmdd = yyyy + mm + dd
    with open(f'./bhavfiles/' + possible_index_name + '.csv', 'r') as reading:
        index_file = csv.DictReader(reading)
        with open(txt1_name, 'a') as txt:
            txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
            for line in index_file:
                # txt.write('\'' + line['Index Name'] + "\',")       # FOR WRITING INDEX NAMES INTO TXT
                if line['Index Name'] in replace_index.keys():
                    txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line[
                        'Open Index Value'] + "," + line[
                                  'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                  'Closing Index Value'] + "," + line['Volume'] + "\n")
                else:
                    txt.write(
                        line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                            'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                            'Closing Index Value'] + "," + line['Volume'] + "\n")

def bse_file(bselink,yyyymmdd):
    bse_file_name = './bhavfiles/bse_temp_file.zip'
    # Add a User-Agent header to the request
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    # Download the file
    urllib.request.urlretrieve(bselink, bse_file_name)
    # OPENS DOWNLOADED ZIP FILE AND EXTRACTS CSV FILE
    with ZipFile(bse_file_name, 'r') as zip:
        # list all the contents of the zip file
        for zipinfo in zip.infolist():
            with zip.open(zipinfo) as file:
                file2 = str(zipinfo.filename)
                print(file2)
        zip.extractall('./bhavfiles/')
        # print("Extracted succesfully")
    txt3_name = './bhavfiles/' + file2.split('.CSV')[0] + '.txt'

    with open(f'./bhavfiles/' + file2, 'r') as reading:
        bse_full_file = csv.DictReader(reading)
        with open(txt3_name, 'a') as txt:
            txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
            for line in bse_full_file:
                # print(line)
                if line['SC_GROUP'] not in avoid_bse_series:
                    if line['SC_NAME'] not in avoid_bse_stocks and line['SC_NAME'] not in avoid_stocks:
                        txt.write(line['SC_NAME'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line[
                            'HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
    return txt3_name

def nse_file(nse_full_link,possible_fullbhav_name,txt2_name):

    with urllib.request.urlopen(nse_full_link) as test_nse_file, open(f'' + possible_fullbhav_name, 'w',
                                                                      newline="") as f:
        f.write(test_nse_file.read().decode())
    st.info("downloaded nse file")
    #               NSE WHOLE BHAVCOPY
    # st.write("getting yyyymmdd from file name")
    # sec_bhavdata_full_23082022.csv
    # st.write(possible_fullbhav_name)
    date_nse = str(possible_fullbhav_name[18:20])
    #st.write(date_nse)
    mnth_nse = str(possible_fullbhav_name[20:22])
    #st.write(mnth_nse)
    yr_nse = str(possible_fullbhav_name[22:26])
    #st.write(yr_nse)
    yyyymmdd = yr_nse + mnth_nse + date_nse
    txt1_name = possible_fullbhav_name.split('.csv')[0] + '.txt'
    first_lines = pd.read_csv(possible_fullbhav_name, nrows=10)
    for i in range(len(first_lines[' DATE1'])):
        date_nse_cell = first_lines[' DATE1'][i][1:3]
        mnth_format_cell = first_lines[' DATE1'][i][4:7]
        mnth_nse_cell = mnth_dict[mnth_format_cell.upper()]
        yr_nse_cell = str(first_lines[' DATE1'][i][8:])
        yyyymmdd_cell = yr_nse_cell + mnth_nse_cell + date_nse_cell
        # st.write("CHECK THIS from file name :" + yyyymmdd + "from cell value " + yyyymmdd_cell)
    if yyyymmdd == yyyymmdd_cell:
        print("bOTH DATES ARE SAME")
        with open(possible_fullbhav_name, 'r') as reading:
            nse_full_file = csv.DictReader(reading)
            with open(txt2_name, 'a') as txt:
                txt.write("SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, TRADED_QTY, DELIVERABLE_QTY" + "\n")
                for line in nse_full_file:
                    if line[' SERIES'] not in avoid_series:
                        if line['SYMBOL'] not in avoid_stocks:
                            txt.write(
                                line['SYMBOL'] + "," + str(yyyymmdd) + "," + line[' OPEN_PRICE'] + "," +
                                line[
                                    ' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[
                                    ' CLOSE_PRICE'] + "," + line[
                                    ' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")
        return "success"
    else:
        st.info("Both dates are not same")
        return "fail"

def download_bhav(my1_date,my2_date):              #nselink,bselink,indexlink,possible_index_name):
    ddmmmyyyy1 = my1_date.strftime("%d%b%Y")
    ddmmmyyyy2 = my2_date.strftime("%d%b%Y")
    created_zip = ZipFile("EOD.zip", "w")
    created_zip.close()
    mnth_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    delta = timedelta(days=1)
    files_list = []
    ddmmmyyyy = ddmmmyyyy1
    while my1_date <= my2_date:
        #st.write(my1_date)
        #st.success("started loop")
        ddmmmyyyy = my1_date.strftime("%d%b%Y")
        weekday_num = datetime.datetime.strptime(ddmmmyyyy, '%d%b%Y').weekday()
        if weekday_num == 5 or weekday_num == 6:
            my1_date += timedelta(1)
            pass
        else :
            mmm_to_d = str(ddmmmyyyy[2:5].upper())
            mm_to_d = str(mnth_dict[mmm_to_d])
            dd_to_d = str(ddmmmyyyy[0:2])
            yy_to_d = str(ddmmmyyyy[-2:])
            yyyy_to_d = str(ddmmmyyyy[-4:])
            yyyymmdd = yyyy_to_d + mm_to_d + dd_to_d
            #https://archives.nseindia.com/products/content/sec_bhavdata_full_30122022.csv
            #https://www1.nseindia.com/content/indices/ind_close_all_30122022.csv
            #TEMPORARILY, NOT USING NSELINK
            nselink = 'https://www1.nseindia.com/content/historical/EQUITIES/' + yyyy_to_d + '/' + mmm_to_d + '/cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv.zip'
            # possible_nse_name = 'cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'full.csv'
            bselink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + dd_to_d + mm_to_d + yy_to_d + '_CSV.ZIP'
            indexlink = 'https://www1.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
            # NSEFULLLINK GIVES DELIVERY DATA AS WELL
            nse_full_link = "https://archives.nseindia.com/products/content/sec_bhavdata_full_"+ dd_to_d + mm_to_d + yyyy_to_d + ".csv"
            possible_fullbhav_name = "sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
            possible_index_name = 'ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d
            txt1_name = './bhavfiles/' + possible_index_name + '.txt'
            txt2_name = './bhavfiles/' + possible_fullbhav_name.split('.csv')[0] + '.txt'

            # INDEX FILE, FULL BHAVCOPY,
            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading INDEX FILE: " + ddmmmyyyy)
                index_file(indexlink,possible_index_name,txt1_name)
                with col2:
                    st.write("DONE INDEX BHAVCOPY:    " + yyyymmdd)
                # write the text file into a zipped file
                with ZipFile("EOD.zip", "a") as m_zip:
                    m_zip.write(txt1_name)
            except:
                #st.info("Could not download index file. Try downloading using this link :")
                st.write(indexlink)

            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading BSE FILE: " + ddmmmyyyy)
                txt3_name = bse_file(bselink,yyyymmdd)
                with col2:
                    st.write("DONE BSE BHAVCOPY:    " + yyyymmdd)
                # write the text file into a zipped file
                with ZipFile("EOD.zip", "a") as m_zip:
                    m_zip.write(txt3_name)
            except:
                #st.info("Could not download BSE file. Try downloading using this link :")
                st.write(bselink)
            # NSE FILE
            try:
                result = ""
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading NSE FULL BHAV FILE: " + ddmmmyyyy)

                result = nse_file(nse_full_link,possible_fullbhav_name,txt2_name)
                st.info("Returned from nse_file function")
                print(result)
                if result == "success":
                    with col2:
                        st.write("DONE FULL BHAVCOPY:   " + yyyymmdd)
                    with ZipFile("EOD.zip", "a") as m_zip:
                        m_zip.write(txt2_name)
                elif result == "fail":
                    st.info("the DATE and THE FILE GENERATED ARE DIFFERENT. THUS SKIPPING")
            except:
                #st.info("Could not download NSE file. Try downloading using this link :")
                st.write(nse_full_link)
            # LOOP and get into the next date
            my1_date += timedelta(1)

    # PROVIDE THE UPDATED ZIP FILE AS DOWNLOADABLE CONTENT
    with open("EOD.zip", "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="EOD.zip",
            mime="application/octet-stream"
        )

    st.markdown("____")
    st.markdown("**Download your copy and PLS spread YOUR LOVE by sharing BHAVCOPY to NEAR and DEAR one\'s**")

    st.markdown("____")
    #with open(txt_name) as f:
    #    st.download_button('DOWNLOAD BHAVCOPY', f, file_name=txt_name)  # Defaults to 'text/plain'

    '''
    try:
        bse_d = urllib.request.urlopen(bselink.content()
        with ZipFile(BytesIO(bse_d)) as my_zip_file:
            for file in my_zip_file.namelist():
                st.info(file)
                with open(file, 'r') as reading:
                    file1 = csv.DictReader(reading)
                    #       PRINTS WHOLE DATA AS DISCTIONARY
                    for line in file1:
                        print(line)
        #index_zip = ZipFile(BytesIO(bse_d.content))
        # bse_zip.extractall(r'{}'.format(path_bhav))
    except:
        st.warning('unable to download Index file')
    '''





def empty_folder(folder_path):
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def download_bhav1(my1_date, my2_date):
    ddmmmyyyy1 = my1_date.strftime("%d%b%Y")
    ddmmmyyyy2 = my2_date.strftime("%d%b%Y")
    empty_folder("./bhavfiles")
    EOD_file = "./bhavfiles/" + "EOD.zip"
    created_zip = ZipFile(EOD_file, "w")
    created_zip.close()
    mnth_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    delta = timedelta(days=1)
    files_list = []
    ddmmmyyyy = ddmmmyyyy1
    while my1_date <= my2_date:
        # st.write(my1_date)
        # st.success("started loop")
        ddmmmyyyy = my1_date.strftime("%d%b%Y")
        weekday_num = datetime.datetime.strptime(ddmmmyyyy, '%d%b%Y').weekday()
        if weekday_num == 5 or weekday_num == 6 or ddmmmyyyy in holidays_ddmmmyyyy:
            my1_date += timedelta(1)
            pass
        else:
            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading NSE FILE: " + ddmmmyyyy)
                txt2_name = bhavcopy_url.nse_file('./bhavfiles/', ddmmmyyyy)
                if os.path.exists(txt2_name):
                    # TO SEND AS ZIP FILE
                    with ZipFile(EOD_file, "a") as m_zip:
                        m_zip.write(txt2_name)
                else:
                    pass
                with col2:
                    st.write("DONE INDEX BHAVCOPY:    " + yyyymmdd)
            except:
                # st.info("Could not download index file. Try downloading using this link :")
                pass
            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading INDEX FILE: " + ddmmmyyyy)
                txt1_name = bhavcopy_url.index_file('./bhavfiles/',ddmmmyyyy)

                if os.path.exists(txt1_name):
                    with ZipFile(EOD_file, "a") as m_zip:
                        m_zip.write(txt1_name)
                with col2:
                    st.write("DONE INDEX BHAVCOPY:    " + yyyymmdd)
            except:
                # st.info("Could not download BSE file. Try downloading using this link :")
                pass
            # NSE FILE
            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading BSE FULL BHAV FILE: " + ddmmmyyyy)
                txt3_name,txt3_name1 = bhavcopy_url.bse_file('./bhavfiles/',ddmmmyyyy)
                #print(f"Succesfully got data from BSE site {txt3_name}")
                if os.path.exists(txt3_name) and os.path.exists(txt3_name1):
                    with ZipFile(EOD_file, "a") as m_zip:
                        m_zip.write(txt3_name)
                        m_zip.write(txt3_name1)
                with col2:
                    st.write("DONE BSE BHAVCOPY:    " + yyyymmdd)

            except:
                pass
            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading FUTURES FULL BHAV FILE: " + ddmmmyyyy)
                txt4_name = bhavcopy_url.futures_file('./bhavfiles/',ddmmmyyyy)
                if os.path.exists(txt4_name):
                    with ZipFile(EOD_file, "a") as m_zip:
                        m_zip.write(txt4_name)
                with col2:
                    st.write("DONE FUTURES BHAVCOPY:    " + yyyymmdd)
            except:
                pass
            try:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("Downloading OPTIONS FULL BHAV FILE: " + ddmmmyyyy)
                txt5_name = bhavcopy_url.options_file('./bhavfiles/',ddmmmyyyy)
                if os.path.exists(txt5_name):
                    with ZipFile(EOD_file, "a") as m_zip:
                        m_zip.write(txt5_name)
                with col2:
                    st.write("DONE OPTIONS BHAVCOPY:    " + yyyymmdd)
            except:
                pass

            # LOOP and get into the next date
            my1_date += timedelta(1)

    # PROVIDE THE UPDATED ZIP FILE AS DOWNLOADABLE CONTENT
    with open(EOD_file, "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="EOD.zip",
            mime="application/octet-stream"
        )

    st.markdown("____")
    st.markdown("**Download your copy and PLS spread YOUR LOVE by sharing BHAVCOPY to NEAR and DEAR one\'s**")

    st.markdown("____")
    # with open(txt_name) as f:
    #    st.download_button('DOWNLOAD BHAVCOPY', f, file_name=txt_name)  # Defaults to 'text/plain'


if __name__ == '__main__':
    main()
