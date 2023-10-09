import os.path

from scriptstoavoid import *
import urllib.request
from urllib.error import HTTPError
import requests
import csv
import pandas as pd
from zipfile import ZipFile

mnth_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
             'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}


def get_date_formats(ddmmmyyyy):
    mmm_to_d = str(ddmmmyyyy[2:5].upper())
    mm_to_d = str(mnth_dict[mmm_to_d.upper()])
    dd_to_d = str(ddmmmyyyy[0:2])
    yy_to_d = str(ddmmmyyyy[-2:])
    yyyy_to_d = str(ddmmmyyyy[-4:])
    yyyymmdd = yyyy_to_d + mm_to_d + dd_to_d
    return mmm_to_d,mm_to_d,dd_to_d,yy_to_d,yyyy_to_d,yyyymmdd
def csv_download(full_link,possible_bhav_name,folder_location):             # CSV files for NSE and INDEX
    csvbhav_path = folder_location + possible_bhav_name
    with urllib.request.urlopen(full_link, timeout=5) as test_file, open(csvbhav_path, 'w',newline="") as f:
        f.write(test_file.read().decode())
    return csvbhav_path

def nse_file(folder_location,ddmmmyyyy):             #(nse_full_link,possible_fullbhav_name,txt2_name):
    mmm_to_d, mm_to_d, dd_to_d, yy_to_d, yyyy_to_d, yyyymmdd = get_date_formats(ddmmmyyyy)
    # https://archives.nseindia.com/products/content/sec_bhavdata_full_30122022.csv
    # https://www1.nseindia.com/content/historical/EQUITIES/2019/SEP/cm30SEP2019bhav.csv.zip
    nselink = 'https://www1.nseindia.com/content/historical/EQUITIES/' + yyyy_to_d + '/' + mmm_to_d + '/cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'bhav.csv.zip'
    possible_nse_name = 'cm' + dd_to_d + mmm_to_d + yyyy_to_d + 'full.csv'
    # NSEFULLLINK GIVES DELIVERY DATA AS WELL
    nse_full_link = "https://archives.nseindia.com/products/content/sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    possible_fullbhav_name = "sec_bhavdata_full_" + dd_to_d + mm_to_d + yyyy_to_d + ".csv"
    txt2_name = folder_location + yyyy_to_d + mm_to_d + dd_to_d + "_" + "NSE.txt"
    try:
        print("entered nse download")
        bhav_csv_path = csv_download(nse_full_link,possible_fullbhav_name,folder_location)
        '''
        with urllib.request.urlopen(nse_full_link, timeout=5) as test_nse_file, open(
                ffolder_location + possible_fullbhav_name, 'w',
                newline="") as f:
            f.write(test_nse_file.read().decode())
        '''
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
            return txt2_name
        else:
            return "fail"
    except Exception as TimedoutError:
        return "fail"
def index_file(folder_location,ddmmmyyyy):
    mmm_to_d, mm_to_d, dd_to_d, yy_to_d, yyyy_to_d, yyyymmdd = get_date_formats(ddmmmyyyy)
    # indexlink = 'https://www1.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
    indexlink = 'https://archives.nseindia.com/content/indices/ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d + '.csv'
    possible_index_name = 'ind_close_all_' + dd_to_d + mm_to_d + yyyy_to_d
    txt1_name = folder_location + yyyy_to_d + mm_to_d + dd_to_d + "_" + "INDEX.txt"
    try:
        possible_index_name = possible_index_name + '.csv'
        print("entered INDEX download function")
        bhav_csv_path = csv_download(indexlink,possible_index_name,folder_location)
        # INDEX FILE
        '''
        with urllib.request.urlopen(indexlink, timeout=5) as testfile, open(ffolder_location + possible_index_name,
                                                                 'w',
                                                                 newline="") as f:
            f.write(testfile.read().decode())
        '''
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

def zip_csv_download(link,zipfile_name,extract_to):
    print("Entered zip_csv_dowonlaod function")
    # Add a User-Agent header to the request
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    with urllib.request.urlopen(link, timeout=15) as response:
        with open(zipfile_name, 'wb') as file:
            file.write(response.read())
    # OPENS DOWNLOADED ZIP FILE AND EXTRACTS CSV FILE
    with ZipFile(zipfile_name, 'r') as zip:
        # list all the contents of the zip file
        print("Getting into infolist to get the filename")
        for zipinfo in zip.infolist():
            with zip.open(zipinfo) as file:
                file2 = str(zipinfo.filename)
        print(f"Copied textfile name {file2}")
        zip.extractall(extract_to)
        # print("Extracted zipfile succesfully")
    return file2
def bse_file(folder_location,ddmmmyyyy):
    mmm_to_d, mm_to_d, dd_to_d, yy_to_d, yyyy_to_d, yyyymmdd = get_date_formats(ddmmmyyyy)
    # FOR bselink and fnolink yyyymmdd is required and not txtnames
    bselink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + dd_to_d + mm_to_d + yy_to_d + '_CSV.ZIP'
    txt3_name = folder_location + yyyymmdd + "_" + "BSE.txt"
    txt3_name1 = folder_location + yyyymmdd + "_" + "BSE_code.txt"
    try:
        print("entered Bse download function")
        zip_file_name = folder_location + 'bse_temp_file.zip'
        csv_path = zip_csv_download(bselink,zip_file_name,folder_location)
        print(csv_path)
        csv_path = folder_location + csv_path
        print("lets read BSE CSV file now")
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

def futures_file(folder_location,ddmmmyyyy):
    mmm_to_d, mm_to_d, dd_to_d, yy_to_d, yyyy_to_d, yyyymmdd = get_date_formats(ddmmmyyyy)
    fnolink = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + yyyy_to_d + "/" + mmm_to_d + "/fo" + dd_to_d + mmm_to_d + yyyy_to_d + "bhav.csv.zip"
    txt4_name = folder_location + yyyymmdd + "_" + "FUTURES.txt"
    try:
        print("entered FNO download function")
        zip_file_name = folder_location +'fno_temp_file.zip'
        fno_csv_path = zip_csv_download(fnolink,zip_file_name,folder_location)
        fno_csv_path = folder_location + fno_csv_path
        print("lets read FUTURES CSV file now")
        with open(fno_csv_path, 'r') as reading:
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

        return txt4_name
    except Exception as TimedoutError:
        return "fail"

def options_file(folder_location,ddmmmyyyy):
    mmm_to_d, mm_to_d, dd_to_d, yy_to_d, yyyy_to_d, yyyymmdd = get_date_formats(ddmmmyyyy)
    fnolink = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + yyyy_to_d + "/" + mmm_to_d + "/fo" + dd_to_d + mmm_to_d + yyyy_to_d + "bhav.csv.zip"
    txt5_name = folder_location + yyyymmdd + "_" + "OPTIONS.txt"
    try:
        print("entered FNO download function")
        zip_file_name = folder_location +'fno_temp_file.zip'
        fno_csv_path = zip_csv_download(fnolink,zip_file_name,folder_location)
        fno_csv_path = folder_location + fno_csv_path
        print("lets read OPTIONS CSV file now")
        with open(fno_csv_path, 'r') as reading:
            fno_full_file = csv.DictReader(reading)
            # name for me shud be "NIFTY 43500CE exp_date"
            with open(txt5_name, 'w') as txt1:
                txt1.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME,OI" + "\n")
                for line in fno_full_file:
                    if line["INSTRUMENT"] == "OPTIDX" and line["OPEN"] != "0" and line["HIGH"] != "0" and line["LOW"] != "0" and line["CLOSE"] != "0":  # options for INDEX
                        txt1.write(line['SYMBOL'] + " " + line["STRIKE_PR"] + line["OPTION_TYP"] + " " + line["EXPIRY_DT"] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS'] + line['OPEN_INT'] + "\n")
        return txt5_name
    except Exception as TimedoutError:
        return "fail"
