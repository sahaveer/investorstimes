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

import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from telegram import Bot, InputFile
import telegram
import threading
import logging
import random


from scriptstoavoid import *

# Initialize the Telegram Bot with your API token
token_jarvis = "1698319688:AAG5X-bmCzGqWHIyaksIUfBG_rxZRE3tUvI"
token_investrade = '1186829396:AAHCQ0FCVWnTajl1VUwqr04UTdPJh8G3Aow'  # @Sahav_Bot
bot = Bot(token=token_investrade)

# secrets = toml.load("secrets.toml")
# mongodb_username = secrets["mongo"]["username"]
# mongodb_password = secrets["mongo"]["password"]


def get_external_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        data = response.json()
        return data.get("ip")
    else:
        return "Unknown"
external_ip = get_external_ip()
# st.write("External IP:", external_ip)


# @st.cache_resource
def init_connection():
    # Connection_String = f"mongodb+srv://{mongodb_username}:{mongodb_password}@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority"
    # return MongoClient(**st.secrets["mongo"])
    # Connection_String = f"mongodb+srv://{st.secrets["mongo"]}@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority"
    # return MongoClient(Connection_String, server_api=ServerApi('1'), tls=True)
    Connection_String = "mongodb+srv://EODBhavcopy:bhavcopy@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority"
    return MongoClient(Connection_String)


# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
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
    return NSE_col, BSECODE_col, BSE_col, INDEX_col, FUTURE_col, OPTIONS_col


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br',
    'accept': '[asterisk]/[asterisk]', 'Connection': 'keep-alive'}
url_oc = "https://www.nseindia.com/"  # option-chain"
sess = requests.Session()
cookies = dict()

# st.title("EOD BHAVCOPY")


# WORKIGN ON DATE FORMATS FROM CSV STRING NAMES
mnth_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
             'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}


def empty_folder(folder_path):
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)


def main():
    st.set_page_config(
        page_title="Bhavcopy downloader for AmiBroker",
        #page_icon=":hammer_and_wrench:",
        layout="wide"
    )
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
    #st.title("Bhavcopy downloader for AmiBroker")

    full_message_temp = """
    <div style="background-color:#6C8594;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
    <p style="text-align:justify;color:black;padding:10px">{}</p>
    </div>
    """
    st.markdown(full_message_temp.format(stock_quotes[random.randint(0, len(stock_quotes) - 1)]),
                unsafe_allow_html=True)

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


    if st.button("Telegram_file_id"):
        try:
            EOD_file = f"./bhavfiles/getzip.zip"
            created_zip = ZipFile(EOD_file, "w")
            start_time = time.time()
            file_not_in_db = []
            created_zip.close()
            ddmmmyyyy_list = get_list_of_dates(my1_date, my2_date)
            #st.success(ddmmmyyyy_list)
            client = init_connection()
            NSE_col, BSECODE_col, BSE_col, INDEX_col, FUTURE_col, OPTIONS_col = mongo_data(client)
            for ddmmmyyyy in ddmmmyyyy_list:
                #EOD_file = add_zip(ddmmmyyyy,NSE_col, BSECODE_col, BSE_col, INDEX_col, FUTURE_col, OPTIONS_col, EOD_file, file_not_in_db)
                mmm_to_d, mm_to_d, dd_to_d, yyyy_to_d, yy_to_d = get_dateformats(ddmmmyyyy)
                search_date_in_db = yyyy_to_d + mm_to_d + dd_to_d
                nse_textfile_name = search_date_in_db + "_" + "NSE.txt"
                index_textfile_name = search_date_in_db + "_" + "INDEX.txt"
                BSE_textfile_name = search_date_in_db + "_" + "BSE.txt"
                BSECode_textfile_name = search_date_in_db + "_" + "BSE_code.txt"
                Futures_textfile_name = search_date_in_db + "_" + "FUTURES.txt"
                Options_textfile_name = search_date_in_db + "_" + "INDEX OPTIONS.txt"
                # st.info(f"Searching for {search_date_in_db}")
                get_nse_data = NSE_col.find_one({"date": search_date_in_db})
                if get_nse_data is not None:
                    nse_file_id = get_nse_data['file_id']
                    nse_file_date = get_nse_data['date']
                    if nse_file_date == search_date_in_db:
                        # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {nse_file_id}")
                        downloaded_file_path = download_telegram_file(nse_file_id, token_investrade, nse_textfile_name)
                        #st.success(f"NSE FILE : {downloaded_file_path}")
                        with ZipFile(EOD_file, "a") as m_zip:
                            m_zip.write(downloaded_file_path)
                else:
                    if ddmmmyyyy not in file_not_in_db:
                        file_not_in_db.append(ddmmmyyyy)
                get_bse_data = BSE_col.find_one({"date": search_date_in_db})
                print(get_bse_data)
                if get_bse_data  is not None:
                    bse_file_id = get_bse_data['file_id']
                    bse_file_date = get_bse_data['date']
                    if bse_file_date == search_date_in_db:
                        downloaded_file_path = download_telegram_file(bse_file_id, token_investrade, BSE_textfile_name)
                        #st.success(f"BSE FILE : {downloaded_file_path}")
                        with ZipFile(EOD_file, "a") as m_zip:
                            m_zip.write(downloaded_file_path)
                        # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {bse_file_id}")
                else:
                    if ddmmmyyyy not in file_not_in_db:
                        file_not_in_db.append(ddmmmyyyy)
                get_bsecode_data = BSECODE_col.find_one({"date": search_date_in_db})
                if get_bsecode_data  is not None:
                    bsecode_file_id = get_bsecode_data['file_id']
                    bsecode_file_date = get_bsecode_data['date']
                    if bsecode_file_date == search_date_in_db:
                        downloaded_file_path = download_telegram_file(bsecode_file_id, token_investrade,
                                                                      BSECode_textfile_name)
                        #st.success(f"BSECODe FILE : {downloaded_file_path}")
                        with ZipFile(EOD_file, "a") as m_zip:
                            m_zip.write(downloaded_file_path)
                        # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {bsecode_file_id}")
                else:
                    if ddmmmyyyy not in file_not_in_db:
                        file_not_in_db.append(ddmmmyyyy)
                get_index_data = INDEX_col.find_one({"date": search_date_in_db})
                if get_index_data  is not None:
                    index_file_id = get_index_data['file_id']
                    index_file_date = get_index_data['date']
                    if index_file_date == search_date_in_db:
                        downloaded_file_path = download_telegram_file(index_file_id, token_investrade,
                                                                      index_textfile_name)
                        #st.success(f"INDEX FILE : {downloaded_file_path}")
                        with ZipFile(EOD_file, "a") as m_zip:
                            m_zip.write(downloaded_file_path)
                        # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {index_file_id}")
                else:
                    if ddmmmyyyy not in file_not_in_db:
                        file_not_in_db.append(ddmmmyyyy)
                get_futures_data = FUTURE_col.find_one({"date": search_date_in_db})
                if get_futures_data is not None:
                    futures_file_id = get_futures_data['file_id']
                    futures_file_date = get_futures_data['date']
                    if futures_file_date == search_date_in_db:
                        downloaded_file_path = download_telegram_file(futures_file_id, token_investrade,
                                                                      Futures_textfile_name)
                        #st.success(f"Futures FILE : {downloaded_file_path}")
                        with ZipFile(EOD_file, "a") as m_zip:
                            m_zip.write(downloaded_file_path)
                else:
                    if ddmmmyyyy not in file_not_in_db:
                        file_not_in_db.append(ddmmmyyyy)
                get_options_data = OPTIONS_col.find_one({"date": search_date_in_db})
                if get_options_data is not None:
                    options_file_id = get_options_data['file_id']
                    options_file_date = get_options_data['date']
                    if options_file_date == search_date_in_db:
                        downloaded_file_path = download_telegram_file(options_file_id, token_investrade,
                                                                      Options_textfile_name)
                        #st.success(f"OPTIONS FILE : {downloaded_file_path}")
                        with ZipFile(EOD_file, "a") as m_zip:
                            m_zip.write(downloaded_file_path)
                else:
                    if ddmmmyyyy not in file_not_in_db:
                        file_not_in_db.append(ddmmmyyyy)

            with open(EOD_file, "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP",
                    data=fp,
                    file_name="EOD.zip",
                    mime="application/octet-stream")

            #if len(file_not_in_db) >= 0:
                #for each in file_not_in_db:
                    #bot.send_message(chat_id="304381618", text=f"/bhav {each}")
                    #file_not_in_db.pop(each)
                #yyyymmdd = each[5:] + mnth_dict(each[2:5]) + each[:2]
                #if NSE_col.find_one({"date": yyyymmdd}) is True:
            # bot.send_message(chat_id="@itimesalgo_d", text="Just a test message")
            duration = time.time() - start_time
            st.info(f"Downloaded in {duration} seconds")
            #file_id = "BQACAgUAAx0Ea_o3YAACJUxlHBK31biRDHN-665spMe370BdYQACvQwAAr604FTgorFAP3tkfTAE"
            #save_file = "./bhavfiles/bhav.txt"
            #downloaded_file_path = download_telegram_file(file_id, token_investrade, save_file)
            #if downloaded_file_path:
                # st.success(f"File downloaded successfully. \nYou can access it at {downloaded_file_path}")
                #with open(downloaded_file_path, "rb") as fp:
                    #btn = st.download_button(
                        #label="Download Text File",
                        #data=fp,
                        #file_name="your_text_file.txt",
                        #mime="text/plain"  # Set the MIME type to 'text/plain' for a text file)
            #else:
                #st.error("File download failed.")
        except Exception as e:
            st.error(f"Got error {e}")
            external_ip = get_external_ip()
            #bot.send_message(chat_id="304381618",text=f"Not able to reach MONGODB \nAdd IP Address {external_ip} to your MongoDB Account")


def add_zip(ddmmmyyyy,NSE_col, BSECODE_col, BSE_col, INDEX_col, FUTURE_col, OPTIONS_col, EOD_file, file_not_in_db):
    mmm_to_d, mm_to_d, dd_to_d, yyyy_to_d, yy_to_d = get_dateformats(ddmmmyyyy)
    search_date_in_db = yyyy_to_d + mm_to_d + dd_to_d
    nse_textfile_name = search_date_in_db + "_" + "NSE.txt"
    index_textfile_name = search_date_in_db + "_" + "INDEX.txt"
    BSE_textfile_name = search_date_in_db + "_" + "BSE.txt"
    BSECode_textfile_name = search_date_in_db + "_" + "BSE_code.txt"
    Futures_textfile_name = search_date_in_db + "_" + "FUTURES.txt"
    Options_textfile_name = search_date_in_db + "_" + "INDEX OPTIONS.txt"
    # st.info(f"Searching for {search_date_in_db}")
    get_nse_data = NSE_col.find_one({"date": search_date_in_db})
    if get_nse_data is True:
        nse_file_id = get_nse_data['file_id']
        nse_file_date = get_nse_data['date']
        if nse_file_date == search_date_in_db:
            # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {nse_file_id}")
            downloaded_file_path = download_telegram_file(nse_file_id, token_investrade, nse_textfile_name)
            st.success(f"NSE FILE : {downloaded_file_path}")
            with ZipFile(EOD_file, "a") as m_zip:
                m_zip.write(downloaded_file_path)
    else:
        if ddmmmyyyy not in file_not_in_db:
            file_not_in_db.append(ddmmmyyyy)
    get_bse_data = BSE_col.find_one({"date": search_date_in_db})
    if get_bse_data is True:
        bse_file_id = get_bse_data['file_id']
        bse_file_date = get_bse_data['date']
        if bse_file_date == search_date_in_db:
            downloaded_file_path = download_telegram_file(bse_file_id, token_investrade, BSE_textfile_name)
            st.success(f"BSE FILE : {downloaded_file_path}")
            with ZipFile(EOD_file, "a") as m_zip:
                m_zip.write(downloaded_file_path)
            # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {bse_file_id}")
    else:
        if ddmmmyyyy not in file_not_in_db:
            file_not_in_db.append(ddmmmyyyy)
    get_bsecode_data = BSECODE_col.find_one({"date": search_date_in_db})
    if get_bsecode_data is True:
        bsecode_file_id = get_bsecode_data['file_id']
        bsecode_file_date = get_bsecode_data['date']
        if bsecode_file_date == search_date_in_db:
            downloaded_file_path = download_telegram_file(bsecode_file_id, token_investrade, BSECode_textfile_name)
            st.success(f"BSECODe FILE : {downloaded_file_path}")
            with ZipFile(EOD_file, "a") as m_zip:
                m_zip.write(downloaded_file_path)
            # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {bsecode_file_id}")
    else:
        if ddmmmyyyy not in file_not_in_db:
            file_not_in_db.append(ddmmmyyyy)
    get_index_data = INDEX_col.find_one({"date": search_date_in_db})
    if get_index_data is True:
        index_file_id = get_index_data['file_id']
        index_file_date = get_index_data['date']
        if index_file_date == search_date_in_db:
            downloaded_file_path = download_telegram_file(index_file_id, token_investrade, index_textfile_name)
            st.success(f"INDEX FILE : {downloaded_file_path}")
            with ZipFile(EOD_file, "a") as m_zip:
                m_zip.write(downloaded_file_path)
            # st.success(f"Got File_id for {search_date_in_db} from MONGODB : \n {index_file_id}")
    else:
        if ddmmmyyyy not in file_not_in_db:
            file_not_in_db.append(ddmmmyyyy)
    get_futures_data = FUTURE_col.find_one({"date": search_date_in_db})
    if get_futures_data is True:
        futures_file_id = get_futures_data['file_id']
        futures_file_date = get_futures_data['date']
        if futures_file_date == search_date_in_db:
            downloaded_file_path = download_telegram_file(futures_file_id, token_investrade, Futures_textfile_name)
            st.success(f"Futures FILE : {downloaded_file_path}")
            with ZipFile(EOD_file, "a") as m_zip:
                m_zip.write(downloaded_file_path)
    else:
        if ddmmmyyyy not in file_not_in_db:
            file_not_in_db.append(ddmmmyyyy)
    get_options_data = OPTIONS_col.find_one({"date": search_date_in_db})
    if get_options_data is True:
        options_file_id = get_options_data['file_id']
        options_file_date = get_options_data['date']
        if options_file_date == search_date_in_db:
            downloaded_file_path = download_telegram_file(options_file_id, token_investrade, Options_textfile_name)
            st.success(f"OPTIONS FILE : {downloaded_file_path}")
            with ZipFile(EOD_file, "a") as m_zip:
                m_zip.write(downloaded_file_path)
    else:
        if ddmmmyyyy not in file_not_in_db:
            file_not_in_db.append(ddmmmyyyy)

    bot.send_message(chat_id="304381618", text=f"/bhav {ddmmmyyyy}")
    file_not_in_db.pop(ddmmmyyyy)
    st.success(EOD_file)
    return EOD_file

def download_telegram_file(file_id, bot_token, save_file):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getFile"
        payload = {"file_id": file_id}
        headers = {
            "accept": "application/json",
            "User-Agent": "Telegram Bot SDK - (https://github.com/sahaveer/investorstimes)",
            "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        # st.success(response.text)
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
        if weekday_num == 5 or weekday_num == 6 or ddmmmyyyy in holidays_ddmmmyyyy:
            my1_date += timedelta(1)
            pass
        else:
            # print(ddmmmyyyy)
            ddmmmyyyy_list.append(ddmmmyyyy)
            my1_date += timedelta(1)
    return ddmmmyyyy_list

def get_dateformats(ddmmmyyyy):
    mmm_to_d = str(ddmmmyyyy[2:5].upper())
    mm_to_d = str(mnth_dict[mmm_to_d.upper()])
    dd_to_d = str(ddmmmyyyy[0:2])
    yy_to_d = str(ddmmmyyyy[-2:])
    yyyy_to_d = str(ddmmmyyyy[-4:])
    return mmm_to_d, mm_to_d, dd_to_d, yyyy_to_d, yy_to_d

if __name__ == '__main__':
    main()

