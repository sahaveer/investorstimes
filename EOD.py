# this is to only handle csv files and then copy the context to a TXT file
# UPDATE 2NOV2022 : updated avoid_bse_stocks to avoid stocks which are already available in NSE
# IDEA 3NOV2022 : Got to give an option in website to select the coulmns as per users demand and alos option to select if they want BSE CODE o BSE NAME
# IDEA 3NOV2022: Would be better if i could avoid all the gaps in the last of BSE NAMES
import streamlit as st
import glob, os
import os.path
import subprocess
import re
import time
from time import sleep
import datetime
from datetime import timedelta
from datetime import date
import shutil

import urllib.request
from urllib.error import HTTPError
import csv
import pandas as pd
import requests

from zipfile import ZipFile
import zipfile
from zipfile import BadZipFile

from io import BytesIO

from selenium import webdriver
import streamlit as st

from scriptstoavoid import *
import pymongo
from pymongo import MongoClient
# CONNECTION STRING : mongodb+srv://EODBhavcopy:bhavcopy@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority
# client = pymongo.MongoClient("mongodb+srv://EODBhavcopy:<password>@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority")

from telegram import Bot, InputFile
import telegram

import threading
import logging

# Initialize the Telegram Bot with your API token
token_jarvis = "1698319688:AAG5X-bmCzGqWHIyaksIUfBG_rxZRE3tUvI"
token_investrade = '1186829396:AAHCQ0FCVWnTajl1VUwqr04UTdPJh8G3Aow'  # @Sahav_Bot
bot = Bot(token=token_investrade)

#secrets = toml.load("secrets.toml")
#mongodb_username = secrets["mongo"]["username"]
#mongodb_password = secrets["mongo"]["password"]

#@st.cache_resource
def init_connection():
    #Connection_String = "mongodb+srv://EODBhavcopy:bhavcopy@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority"
    #Connection_String = f"mongodb+srv://{mongodb_username}:{mongodb_password}@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority"
    return MongoClient(**st.secrets["mongo"])

# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
def mongo_data(client):
    db = client.get_database('Bhavcopy')
    NSE_col = db["NSEbhav"]
    BSE_col = db["BSEbhav"]
    BSECODE_col = db["BSECODEbhav"]
    INDEX_col = db["INDEXbhav"]
    FUTURE_col = db["FUTURESbhav"]
    OPTIONS_col = db["OPTIONSbhav"]
    userid_col = db["usersdata"]
    topics_col = db["topics"]
    OI_col = db["OI"]
    EOD_col = db["EOD"]
    reco_col = db["RECO"]
    pf_col = db["Portfolio"]
    pfaccess_col = db["PFaccess"]
    return NSE_col,BSECODE_col,BSE_col,INDEX_col,FUTURE_col


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br',
    'accept': '[asterisk]/[asterisk]', 'Connection': 'keep-alive'}
url_oc = "https://www.nseindia.com/"  # option-chain"
sess = requests.Session()
cookies = dict()

# st.title("EOD BHAVCOPY")
# PATHS OF THIS COMPUTER
# path_bhav = 'C:/Users/sahaveer/OneDrive/Documents/bhavcopy/'
# path_csv = "C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/"
# path_download = 'C:/Users/sahaveer/Downloads/'

# WORKIGN ON DATE FORMATS FROM CSV STRING NAMES
mnth_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
             'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}


def empty_folder(folder_path):
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)


def main():
    import random
    stock_quotes = [
        """'I have two basic rules about winning in trading as well as in life:\n1. If you don’t bet, you can’t win.\n2. If you lose all your chips, you can’t bet.' \n\n– Larry Hite""",
        """'When you genuinely accept the risks, you will be at peace with any outcome.'\n – Mark Douglas""",
        """'By living the philosophy that my winners are always in front of me, it is not so painful to take a loss.' \n– Marty Schwartz""",
        """'The trend is your friend until the end when it bends.' \n– Ed Seykota""",
        """'The secret to being successful from a trading perspective is to have an indefatigable and an undying and unquenchable thirst for information and knowledge.'\n-Paul Tudor Jones""",
        """'Wide diversification is only required when investors do not understand what they are doing.'\n– Warren Buffett""",
        """'If you don’t respect risk, eventually they’ll carry you out.'\n– Larry Hite""",
        """'Opportunities come infrequently. When it rains gold put out a bucket not a thimble.'\n– Warren Buffet""",
        """'The trend is your friend – until it stabs you in the back with a chopstick.'\n– @StockCats""",
        """The four most dangerous words in investing are: ‘this time it’s different.'\n– Sir John Templeton""",
        """'It’s not how much money you make, but how much money you keep, how hard it works for you, and how many generations you keep it for.'\n– Robert Kiyosaki""",
        """'Know what you own, and know why you own it.'\n- Peter Lynch""",
        """'All the math you need in the stock market you get in the fourth grade.'\n-Peter Lynch""",
        """'I just wait until there is money lying in the corner, and all I have to do is go over there and pick it up. I do nothing in the meantime.'\n– Jim Rogers""",
        """'A rising tide lifts all boats over the wall of worry and exposes bears swimming naked.'\n– @StockCats""",
        """'In investing, what is comfortable is rarely profitable.”\n– Robert Arnott""",
        """'Sometimes the best trade is no trade.”\n– Anonymous""",
        """The game of speculation is the most uniformly fascinating game in the world. But it is not a game for the stupid, the mentally lazy, the person of inferior emotional balance, or the get-rich-quick adventurer. They will die poor.'\n– Jesse Livermore""",
        """'Bulls make money, bears make money, pigs get slaughtered.""",
        """You get recessions, you have stock market declines. If you don’t understand that’s going to happen, then you’re not ready, you won’t do well in the markets.”\n- Peter Lynch""",
        """'Dangers of watching every tick are twofold: overtrading and increased chances of prematurely liquidating good positions'\n– Jack Schwager""",
        """'Traders need a daily routine that they love. If you don’t love it, you’re not gonna do it.'\n–Scott Redler""",
        """'Financial peace isn’t the acquisition of stuff. It’s learning to live on less than you make, so you can give money back and have money to invest. You can’t win until you do this.'\n– Dave Ramsey""",
        """'Michael Marcus taught me one other thing that is absolutely critical: You have to be willing to make mistakes regularly; there is nothing wrong with it. Michael taught me about making your best judgment, being wrong, making your next best judgment, being wrong, making your third best judgment, and then doubling your money.'\n– Bruce Kovner""",
        """'Amateurs think about how much money they can make. Professionals think about how much money they could lose.'\n– Jack Schwager"""
        """'If you can’t take a small loss, sooner or later you will take the mother of all losses.'\n– Ed Seykota""",
        """'5/1 risk/reward ratio allows you to have a hit rate of 20%. I can actually be a complete imbecile. I can be wrong 80% of time and still not lose.'\n– Paul Tudor Jones""",
        """Bottoms in the investment world don’t end with four-year lows; they end with 10- or 15-year lows.'\n– Jim Rogers""",
        """'If you think in positive terms, you will achieve positive results.'\n— Norman Vincent Peale""",
        """'The market is a device for transferring money from the impatient to the patient.'\n– Warren Buffet""",
        """'Take your profits or someone else will take them for you.'\n– J.J. Evans""",
        """'In trading, everything works sometimes and nothing works always.'""",
        """'The most important quality for an investor is temperament, not intellect. You need a temperament that neither derives great pleasure from being with the crowd or against the crowd.'\n-Warren Buffett"""
        """'All you need is one pattern to make a living.'\n– Linda Raschke""",
        """'The core problem, however, is the need to fit markets into a style of trading rather than finding ways to trade that fit with market behavior.'\n– Brett Steenbarger""",
        """'The obvious rarely happens, the unexpected constantly occurs.'\n– Jesse Livermore""",
        """'Hope is bogus emotion that only costs you money.'\n– Jim Cramer""",
        """'Five fundamental truths:\n1. Anything can happen.\n2. You don’t need to know what is going to happen next in order to make money.\n3. There is a random distribution between wins and losses for any given set of variables that define an edge.\n4. An edge is nothing more than an indication of a higher probability of one thing happening over another.\n5. Every moment in the market is unique.'\n– Mark Douglas""",
        """'Invest in yourself. Your career is the engine of your wealth.'\n– Paul Clitheroe""",
        """'IF YOU WANT TO BE A LEDGE… FIND YOUR EDGE…'\n– Tom Dante @Trader_Dante""",
        """'Once you find the system that works for your style/personality and confidence is gained, wash, rinse, repeat over and over again.'\n– @Sunrisetrader""",
        """'An investment in knowledge pays the best interest.'\n– Benjamin Franklin""",
        """'Investing should be more like watching paint dry or watching grass grow. If you want excitement, take $800 and go to Las Vegas.'\n– Paul Samuelson""",
        """'Stocks are bought not in fear but in hope. They are typically sold out of fear.'\n– Justin Mamis""",
        """'How many millionaires do you know who have become wealthy by investing in savings accounts? I rest my case.'\n– Robert G. Allen""",
        """'Accepting losses is the most important single investment device to insure safety of capital.'\n– Gerald M. Loeb""",
        """'In trading the impossible happens about twice a year.'\n– Henri M Simoes @TraderHMS""",
        """'You don’t need to trade everyday. You trade when your setups are there… The greatest surfers in the world don’t try to catch every wave– Wait for the right setup!'\n-Dale Pinkert""",
        """'The desire for constant action irrespective of underlying conditions is responsible for many losses in Wall Street.'\n– Jesse Livermore""",
    ]

    # st.markdown("### Site is in progress \n Shall be launched asap")
    st.title("Bhavcopy downloader for AmiBroker")

    full_message_temp = """
    <div style="background-color:#6C8594;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
    <p style="text-align:justify;color:black;padding:10px">{}</p>
    </div>
    """
    st.markdown(full_message_temp.format(stock_quotes[random.randint(0, len(stock_quotes) - 1)]),
                unsafe_allow_html=True)

    # with st.sidebar:
    # PATHS OF THIS COMPUTER
    # st.info("pls mention here your computer paths")
    # path_bhav = st.text_input("path_bhav", value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/')  # './bhavcopy/')
    # path_csv = st.text_input("path_csv",value='C:/Users/sahaveer/OneDrive/Documents/bhavcopy/2022 csv/')  # './bhavcopy/csv')
    # path_download = st.text_input("path_download", value='C:/Users/sahaveer/Downloads/')

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
            # st.write("Going to download_bhav Function")
            ddmmmyyyy_list = get_list_of_dates(my1_date, my2_date)
            download_bhav(ddmmmyyyy_list)
            # st.success("Done downloading, lets try extracting now")
            # eod_existing_files(path_bhav, path_csv)
        except BadZipFile:
            st.error("BadZipFile")
            pass
    '''
    The below Button is still under progress! Happy news is I have atleast found a way to get the Bhavfiles here
    '''
    if st.button("Telegram_file_id"):
        ddmmmyyyy_list = get_list_of_dates(my1_date, my2_date)
        st.success(ddmmmyyyy_list)
        client = init_connection()
        NSE_col, BSECODE_col, BSE_col, INDEX_col, FUTURE_col = mongo_data(client)

        for ddmmmyyyy in ddmmmyyyy_list:
            mmm_to_d, mm_to_d, dd_to_d, yyyy_to_d, yy_to_d = get_dateformats(ddmmmyyyy)
            search_date_in_db = yyyy_to_d + mm_to_d + dd_to_d
            get_nse_data = NSE_col.find_one({"date": search_date_in_db})
            nse_file_id = get_nse_data['file_id']
            nse_file_date = get_nse_data['date']
            if nse_file_date == search_date_in_db:
                st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {nse_file_id}")
            get_bse_data = BSE_col.find_one({"date": search_date_in_db})
            bse_file_id = get_bse_data['file_id']
            bse_file_date = get_bse_data['date']
            if bse_file_date == search_date_in_db:
                st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {bse_file_id}")

        # bot.send_message(chat_id="@itimesalgo_d", text="Just a test message")
        file_id = "BQACAgUAAx0Ea_o3YAACJUxlHBK31biRDHN-665spMe370BdYQACvQwAAr604FTgorFAP3tkfTAE"
        start_time = time.time()
        downloaded_file_path = download_telegram_file(file_id, token_investrade)
        # downloaded_file_path = download_fileid(file_id)
        # st.success(downloaded_file_path)

        if downloaded_file_path:
            # st.success(f"File downloaded successfully. \nYou can access it at {downloaded_file_path}")
            with open(downloaded_file_path, "rb") as fp:
                btn = st.download_button(
                    label="Download Text File",
                    data=fp,
                    file_name="your_text_file.txt",
                    mime="text/plain"  # Set the MIME type to 'text/plain' for a text file
                )
            duration = time.time() - start_time
            print(f"Downloaded in {duration} seconds")
        else:
            st.error("File download failed.")


def download_telegram_file(file_id, bot_token):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getFile"
        save_file = "./bhavfiles/bhav.txt"
        payload = {"file_id": file_id}
        headers = {
            "accept": "application/json",
            "User-Agent": "Telegram Bot SDK - (https://github.com/sahaveer/investorstimes)",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        st.success(response.text)
        # st.success(response.status_code)

        resp_json = response.json()
        file_path = resp_json['result']['file_path']
        file_download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        response = requests.get(file_download_url)

        # st.error(f"So the Second method is giving us filepath : {file_path}")
        if response.status_code == 200:
            # Save the file content to a local file
            with open(save_file, 'wb') as file:
                file.write(response.content)
            return save_file
        else:
            return None

    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return None


def get_list_of_dates(my1_date, my2_date):
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
        else:
            # print(ddmmmyyyy)
            ddmmmyyyy_list.append(ddmmmyyyy)
            my1_date += timedelta(1)
    return ddmmmyyyy_list

def download_bhav(ddmmmyyyy_list):  # nselink,bselink,indexlink,possible_index_name):
    st.markdown(
        "--Sadly NSE site blocked our site from downloading Files. Do try https://t.me/bhavcopy_amibroker to download data--")
    # st.write(ddmmmyyyy_list)
    bhav_date_zip(ddmmmyyyy_list)

    st.markdown("____")
    st.markdown("**Download your copy and PLS spread YOUR LOVE by sharing website to NEAR and DEAR one\'s**")
    st.markdown("____")


def bhav_date_zip(ddmmmyyyy_list):  # ddmmmyyyy and media_group are lists here
    # EXTRACT fro mNSE DB or download data and update in Database
    created_zip = ZipFile("./bhavfiles/EOD.zip", "w")
    created_zip.close()
    EOD_file = f"./bhavfiles/EOD.zip"
    for ddmmmyyyy in ddmmmyyyy_list:
        yyyymmdd, nse_full_link, possible_fullbhav_name, txt2_name, indexlink, possible_index_name, txt1_name, bselink, fnolink = get_links_txtnames(
            ddmmmyyyy)
        # NSE FILE
        try:
            result = ""
            result = nse_file(nse_full_link, possible_fullbhav_name, txt2_name)
            if result == "success":
                # st.success(txt2_name)
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt2_name)
                st.success("DONE NSE BHAVCOPY FOR " + yyyymmdd)
            else:
                # st.error("NSE function didnt return SUCCESS")
                pass
        except Exception as e:
            st.error(f"Failed to download NSE bhavcopy due to : {e}")
            pass
        #  DOWNLOADING INDEX FILE
        try:  # INDEX FILE - DOWNLOADING
            txt1_name = index_file(indexlink, possible_index_name, txt1_name)
            if os.path.exists(txt1_name):
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt1_name)
                st.success("DONE INDEX BHAVCOPIES FOR " + yyyymmdd)
            else:
                # st.error("INDEX function didnt return anything")
                pass
        except Exception as e:
            st.error(f"Failed to download INDEX bhavcopy due to : {e}")
            pass

        try:
            txt3_name, txt3_name1 = bse_file(bselink, yyyymmdd)
            if os.path.exists(txt3_name) and os.path.exists(txt3_name1):
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt3_name)
                    m_zip.write(txt3_name1)
                st.success("DONE BSE BHAVCOPY FOR " + yyyymmdd)
            else:
                # st.error("BSE function didnt return SUCCESS")
                pass
        except Exception as e:
            st.error(f"Failed to download BSE bhavcopy due to : {e}")
            pass

        try:
            txt4_name, txt5_name = fno_file(fnolink, yyyymmdd)
            if os.path.exists(txt4_name) and os.path.exists(txt5_name):
                with ZipFile(EOD_file, "a") as m_zip:
                    m_zip.write(txt4_name)
                    m_zip.write(txt5_name)
                st.success("DONE F&O BHAVCOPY FOR " + yyyymmdd)
            else:
                # st.error("FNO function didnt return SUCCESS")
                pass
        except Exception as e:
            st.error(f"Failed to download F&O bhavcopy due to : {e}")
            pass

    with open(EOD_file, "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="EOD.zip",
            mime="application/octet-stream"
        )


# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=10)
    cookies = dict(request.cookies)

def get_dateformats(ddmmmyyyy):
    mmm_to_d = str(ddmmmyyyy[2:5].upper())
    mm_to_d = str(mnth_dict[mmm_to_d.upper()])
    dd_to_d = str(ddmmmyyyy[0:2])
    yy_to_d = str(ddmmmyyyy[-2:])
    yyyy_to_d = str(ddmmmyyyy[-4:])
    return mmm_to_d, mm_to_d, dd_to_d,yyyy_to_d,yy_to_d

def get_links_txtnames(ddmmmyyyy):
    mmm_to_d, mm_to_d, dd_to_d, yyyy_to_d, yy_to_d = get_dateformats(ddmmmyyyy)
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

    return yyyymmdd, nse_full_link, possible_fullbhav_name, txt2_name, indexlink, possible_index_name, txt1_name, bselink, fnolink


def csv_download(full_link, possible_bhav_name):  # CSV files for NSE and INDEX
    try:
        csvbhav_path = './bhavfiles/' + possible_bhav_name
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')]
        urllib.request.install_opener(opener)
        with urllib.request.urlopen(full_link, timeout=10) as test_file, open(csvbhav_path, 'w', newline="") as f:
            f.write(test_file.read().decode())
            # st.success(f"Downloaded CSV from NSE site in {bhav_csv_path}")
        return csvbhav_path
    except Exception as e:
        set_cookie()
        response = sess.get(nse_full_link, headers=headers, cookies=cookies)
        if response.status_code == 200:
            df = pd.read_csv(pd.compat.StringIO(response.text))
            st.write(df)
        else:
            st.error(f"Error: Unable to fetch CSV. Status code: {response.status_code}")
        st.error(f"{full_link} failed due to {e} ")


# def csv_from_other(nse_full_link,possible_fullbhav_name):


def nse_file(nse_full_link, possible_fullbhav_name, txt2_name):
    try:
        bhav_csv_path = csv_download(nse_full_link, possible_fullbhav_name)
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
                                    line[' HIGH_PRICE'] + "," + line[' LOW_PRICE'] + "," + line[' CLOSE_PRICE'] + "," +
                                    line[' TTL_TRD_QNTY'] + "," + line[' DELIV_QTY'] + "\n")

            return "success"
        else:
            # st.error(f"Asked for {yyyymmdd} Date but got {yyyymmdd_cell} in the excel NSE file, thus skipping")
            return "fail"
    except Exception as e:
        # st.error(f"Failed to download NSE file due to {e}")
        return "fail"


def index_file(indexlink, possible_index_name, txt1_name):
    try:
        possible_index_name = possible_index_name + '.csv'
        print("entered INDEX download function")
        bhav_csv_path = csv_download(indexlink, possible_index_name)
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
                        txt.write(replace_index[line['Index Name']] + "," + str(yyyymmdd) + ',' + line[
                            'Open Index Value'] + ","
                                  + line['High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                      'Closing Index Value'] + "," + line['Volume'] + "\n")
                    else:
                        txt.write(
                            line['Index Name'] + "," + str(yyyymmdd) + ',' + line['Open Index Value'] + "," + line[
                                'High Index Value'] + "," + line['Low Index Value'] + "," + line[
                                'Closing Index Value'] + "," + line['Volume'] + "\n")
            return txt1_name
    except Exception as e:
        # st.error(f"Failed to download INDEX file due to {e}")
        return "fail"


def zip_csv_download(link, file_name):
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


def bse_file(bselink, yyyymmdd):
    try:
        print("entered Bse download function")
        bse_file_name = './bhavfiles/bse_temp_file.zip'
        csv_path = zip_csv_download(bselink, bse_file_name)
        print(csv_path)
        csv_path = './bhavfiles/' + csv_path
        print(csv_path)
        print("lets read CSV file now")
        # txt3_name = './bhavfiles/' + file2.split('.CSV')[0] + '.txt'
        txt3_name = './bhavfiles/' + yyyymmdd + "_" + "BSE.txt"
        txt3_name1 = './bhavfiles/' + yyyymmdd + "_" + "BSE_code.txt"
        with open(csv_path, 'r') as reading:
            bse_full_file = csv.DictReader(reading)
            print("Read the CSV file, lets write to txt now")
            with open(txt3_name, 'w') as txt:
                txt.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                for line in bse_full_file:
                    # print(line)
                    if line['SC_GROUP'] not in avoid_bse_series:
                        if line['SC_NAME'] not in avoid_bse_stocks:
                            if line['SC_NAME'] not in avoid_stocks:
                                txt.write(line['SC_NAME'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line[
                                    'HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
        with open(csv_path, 'r') as reading:
            bse_full_file = csv.DictReader(reading)
            print("Read the CSV file, lets write to txt now")
            with open(txt3_name1, 'w') as txt:
                txt.write("TICKERCODE, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME" + "\n")
                for line in bse_full_file:
                    if line['SC_GROUP'] not in avoid_bse_series:
                        if line['SC_NAME'] not in avoid_bse_stocks:
                            if line['SC_NAME'] not in avoid_stocks:
                                txt.write(line['SC_CODE'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line[
                                    'HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['NO_OF_SHRS'] + "\n")
        return txt3_name, txt3_name1
    except Exception as e:
        # st.error(f"Failed to download BSE file due to {e}")
        return "fail"


def fno_file(fnolink, yyyymmdd):
    try:
        print("entered FNO download function")
        fno_file_name = './bhavfiles/fno_temp_file.zip'
        csv_path = zip_csv_download(fnolink, fno_file_name)
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
                        # txt.write(line['SYMBOL'] + " " + line['EXPIRY_DT'] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," +line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS'] + line['OPEN_INT'] + "\n")
                        # as per Bhavcopy Downloader software
                        if line['SYMBOL'] != unique_script:
                            txt.write(line['SYMBOL'] + "-I" + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line[
                                'HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS'] + "," +
                                      line['OPEN_INT'] + "\n")
                            unique_script = line['SYMBOL']
                            count = 1
                        else:
                            count += 1
                            txt.write(line['SYMBOL'] + roman_val[str(count)] + "," + str(yyyymmdd) + "," + line[
                                'OPEN'] + "," + line['HIGH'] + "," + line['LOW'] + "," + line['CLOSE'] + "," + line[
                                          'CONTRACTS'] + "," + line['OPEN_INT'] + "\n")

        with open(csv_path, 'r') as reading:
            fno_full_file = csv.DictReader(reading)
            # name for me shud be "NIFTY 43500CE exp_date"
            with open(txt5_name, 'w') as txt1:
                txt1.write("TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME,OI" + "\n")
                for line in fno_full_file:
                    if line["INSTRUMENT"] == "OPTIDX" and line["OPEN"] != "0" and line["HIGH"] != "0" and line[
                        "LOW"] != "0" and line["CLOSE"] != "0":  # options for INDEX
                        txt1.write(line['SYMBOL'] + " " + line["STRIKE_PR"] + line["OPTION_TYP"] + " " + line[
                            "EXPIRY_DT"] + "," + str(yyyymmdd) + "," + line['OPEN'] + "," + line['HIGH'] + "," + line[
                                       'LOW'] + "," + line['CLOSE'] + "," + line['CONTRACTS'] + line['OPEN_INT'] + "\n")
        return txt4_name, txt5_name
    except Exception as e:
        # st.error(f"Failed to download FNO file due to {e}")
        return "fail"


if __name__ == '__main__':
    main()

