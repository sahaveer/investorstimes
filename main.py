# import pprint
import time
import io
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
st.set_page_config(page_title="iTimesAlgo", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="expanded",)

# import glob
# import random
import os
import datetime
import time
import pandas as pd
# import pickle
#import numpy as np66
import nse_bse_search
import create_database
import fundamentals
import plotlyfigures
import processdriver
import screenerpage
import variables
import amibroker
from telegram import Bot
import urllib
import requests
#color_dict = {'Yellow_Lite': "#f8ba43", 'Yellow_Dark': "#D6D41B", 'Blue_Lite': "#0FBAEC", 'Blue_Dark': "#0971C9",'Green_Lite': "#11A694", 'Green_Dark': "#11A64B",} #"Purple_Lite": "#7019BF", 'Purple_Dark': "#9319BF"}
color_dict = {'blue3':{'hash':'#00A3FE','rgb':'rgb(0,163,254)'},
              'yellow1':{'hash':'#FFFF01','rgb':'rgb(255,255,1)'},
              'blue1':{'hash':'#21A1E1', 'rgb':'rgb(33,161,225)'},
              'yellow2':{'hash':'#FFFE57','rgb':'rgb(255,254,87)'},
              'blue2':{'hash':'#5DB7D2','rgb':'rgb(93,183,210)'},
              'green1':{'hash':'#00F954','rgb':'rgb(0,249,84)'},
              'red1':{'hash':'#CC0118','rgb':'rgb(204,1,24)'},
              'black': {'hash': '000000', 'rgb': 'rgb(0,0,0)'},
              'white': {'hash': '#ffffff', 'rgb': 'rgb(255, 255, 255)'},
              }
# color_list = ["#D6D41B","#f8ba43","#0971C9","#1959BF","#11A694","#11A64B","#7019BF","#9319BF"]
color_line = "Red"


# 
# PARAMS
funda_keys = ['PROFIT&LOSS', 'BALANCE SHEET','CASH FLOW']  # dont change the order of this list as it will affect the keys used in Yearly df
# **************************************************************************************************
listed_stocks = []
no_latest_quarterly_stocks = []
stocks_dict = {}
# keep 90 if need the latest results
timedelta_Q_days = pd.Timedelta(days=0)
timedelta_Q_days1 = pd.Timedelta(days=120)
recent_reqd_quarter = datetime.datetime(2024,12,31)
recent_quarter_txt="2025-03-31"
last_quarter_text = "2024-12-31"

# Gets data from the local pkl files
# @st.cache_data
# def get_all_quarterly_list():
#     latest_quarterly_stocks = []
#     available_stocks = []
#     print("Entered get_all_quarterly_list FUNCTION and checks all pickle files")
#     last_announced_quarter1 = ""
    
#     #lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
#     for each_pickl in glob.glob('./pickl/**/*.pkl', recursive=True):
#         each_pickl = each_pickl.replace('\\', '/')
#         # st.info(each_pickl)
#         file_name_only = os.path.basename(each_pickl)
#         #file_name_only = each_pickl.split('/')[-1]
#         tree_folder1 = file_name_only[0].upper()
#         if file_name_only.endswith('Yearly.pkl'):
#             pickle_name = file_name_only.split()[0].strip()  # Since all the pickle files are either Quartetrly or Yearly, we need to get the first company code only
#             if os.path.exists(f'./pickl/{tree_folder1}/{file_name_only} Quarterly.pkl'):        #Check if Quarterly Pkl exists
#                 pass
#             else:                           # if Quarterly Pickle file doesnt exist but Only Yearly Exists
#                 if pickle_name not in available_stocks:
#                     available_stocks.append(pickle_name)
#         elif file_name_only.endswith('Quarterly.pkl'):
#             pickle_name = file_name_only.split()[0].strip()
#             qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder1}/{file_name_only}')
#             qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
#             # st.success(qtr_pnl.columns)
#             if (datetime.datetime.now() - qtr_pnl.columns[-1]) < timedelta_Q_days1 and pickle_name not in latest_quarterly_stocks:
#                 # st.success(f"{pickle_name} has latest q results")
#                 latest_quarterly_stocks.append(pickle_name)
#                 last_announced_quarter1 = datetime.datetime.strftime(qtr_pnl.columns[-1],'%b%Y')
#             if pickle_name not in available_stocks:
#                 available_stocks.append(pickle_name)

#     #return unique_listed_stocks, unique_latest_quarterly_stocks, last_announced_quarter1
#     return latest_quarterly_stocks, last_announced_quarter1, available_stocks
# reads from local pickle file 
# if 'latest_quarterly_stocks' not in st.session_state or 'last_announced_quarter' not in st.session_state or  'available_pickles' not in st.session_state:
#     st.session_state.latest_quarterly_stocks,st.session_state.last_announced_quarter,st.session_state.available_pickles = get_all_quarterly_list()

# WE GET THIS FROM THE TXT FILE
if 'listed_stocks' not in st.session_state:
    send_listed_stocks = []
    with open(f'./watchlist/alllisted.txt','r') as fr:
        #save each line into a list object
        lines = fr.readlines()
        for each in lines:
            send_listed_stocks.append(each.strip())            
    # print(send_listed_stocks)
    st.session_state['listed_stocks'] = send_listed_stocks
    # unique_listed_stocks = nse_bse_search.remove_duplicate_in_watchlist(send_listed_stocks)
    # st.session_state['listed_stocks'] = unique_listed_stocks
    # with open('./watchlist/alllisted.txt', 'w') as file:  # Read each line and append it to the list
    #     for line in unique_listed_stocks:
    #         file.write(line + "\n")
# st.success(st.session_state['listed_stocks'])


if 'latest_quarterly_stocks' not in st.session_state or 'last_announced_quarter' not in st.session_state or  'available_pickles' not in st.session_state or 'no_of_stocks_not_latest' not in st.session_state:
    # how to check time consumed for this below code?
    start = time.perf_counter()
    variables.metadata,st.session_state.latest_quarterly_stocks,st.session_state.last_announced_quarter,st.session_state.available_pickles,st.session_state.no_of_stocks_not_latest = create_database.get_metadata(recent_quarter_txt,last_quarter_text)
    end = time.perf_counter()
    elapsed = end - start
    minutes = int(elapsed // 60)
    seconds = elapsed % 60
    print(f"Time taken: {minutes}min {seconds} sec ")





# @st.cache_data
# def scan_for_old_quarterly(query_list):
#     not_latest_quarterly_stocks=[]
#     for selected in query_list:
#         # print(f"Trying to check if {selected} results are more than {timedelta_Q_days1}days in FUNC scan_for_old_quarterly")
#         if selected != "":
#             query = selected.strip()
#             folder_tree = query[0].upper()
#             if os.path.exists(f'./pickl/{folder_tree}/{query} Quarterly.pkl'):
#                 qtr_pnl = pd.read_pickle(f'./pickl/{folder_tree}/{query} Quarterly.pkl')
#                 if (datetime.datetime.now() - qtr_pnl.columns[-1]) > timedelta_Q_days1 and query not in not_latest_quarterly_stocks:
#                     not_latest_quarterly_stocks.append(query)
#             else:
#                 not_latest_quarterly_stocks.append(query)
#     print(f"not_latest_quarterly_stocks object got updated")
#     return not_latest_quarterly_stocks

col1_header, col2_header = st.columns([2,1])    
with col1_header:
    st.title(f"👇 {len(st.session_state['listed_stocks'])} we got {str(len(st.session_state.available_pickles))} available stocks")
    st.caption(f"{str(len(st.session_state.latest_quarterly_stocks))} stocks announced {st.session_state.last_announced_quarter} Quarterly Results;")

                                                                                                                        # Function to save the dictionary to a file

token_jarvis = "1698319688:AAG5X-bmCzGqWHIyaksIUfBG_rxZRE3tUvI"                     # JarvisPOSTME
chat_ids = ["itimesalgo"]       #,"bhavcopy_amibroker"] # to update quarterly results
bot = Bot(token=token_jarvis)

check_when_last_checked = datetime.timedelta(days=4)
# send_to_telegram = st.checkbox("Send To Telegram", value=False)

def write_tags_to_txt(metadata):
    if len(metadata['metadata']['tags']) >= 1:
        for each in metadata['metadata']['tags']:
            text_file = f'./watchlist/groups/{each}.txt'
            # if each not in variables.user_data.keys():
            #     variables.user_data[each] = []
            # if metadata['code_names'][-1] not in variables.user_data[each]:
            #     with open(text_file, 'a+') as file:
            #         file.write(f"{metadata['code_names'][-1]}\n")
            #         st.success(f"Updated {metadata['code_names'][-1]} in {text_file}")

def save_screener1(codes,force):
    driver = processdriver.getedgedriver()
    if force == False:
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        print("Entered save_screener1 FUNC")
        i=0
        for code in codes:
            i+=1
            print(f"Trying to get details of {code} in saves_screener1 Func")
            #lets search for code in create_database.comp_metadata_col database by countdocuments
            # last_quarter_announced = ""
            st.success(f'We have {create_database.comp_metadata_col.count_documents({"code_names": code})} documents saved in DB')
            
            if create_database.comp_metadata_col.count_documents({"code_names": code}):
                doc_is = create_database.comp_metadata_col.find_one({"code_names":code})
                if doc_is is not None:
                    # st.success(doc_is)
                    if "CONSOLIDATED" in doc_is.keys():
                        # get the last key value saved in the dict of doc_is["CONSOLIDATED"]['QUARTERLY']
                        listed_dict_keys = list(doc_is['CONSOLIDATED']['QUARTERLY'])
                        if len(listed_dict_keys) > 0:
                            last_quarter_announced = listed_dict_keys[-1]
                    elif "STANDALONE" in doc_is.keys():
                        # get the last key value saved in the dict of doc_is["CONSOLIDATED"]['QUARTERLY']
                        listed_dict_keys = list(doc_is['STANDALONE']['QUARTERLY'])
                        if len(listed_dict_keys)>0:
                            last_quarter_announced = listed_dict_keys[-1]
                    else:
                        screenerpage.search_screener1(driver,code)
                    # st.success(last_quarter_announced)
                    # st.success(type(last_quarter_announced))
                    if (last_quarter_announced != recent_quarter_txt ) and (datetime.datetime.now() - doc_is['timestamp']).days>5:
                        screenerpage.search_screener1(driver,code)
                    else:
                        st.success(f"We already got LATEST RESULTS for {code} : {last_quarter_announced}")
                else:
                    screenerpage.search_screener1(driver,code)
            else:
                screenerpage.search_screener1(driver,code)
            # lets sleep for random of 1-10 sec when i is added 10 times
    else:
        for code in codes:
            st.success(code)
            screenerpage.search_screener1(driver,code)

    print("Exiting save_screener1 FUNC")


# Parse the URL parameters to get the selected stock
url = st.experimental_get_query_params()
selected_stock = url.get("selected", [""])[0]


watchlist = create_database.industry_col.find()
industry_dict = {}

if len(st.session_state.latest_quarterly_stocks)>1:
    industry_dict["Latest Quarterly"] = st.session_state.latest_quarterly_stocks #if selected_stock in st.session_state.latest_quarterly_stocks else st.session_state.listed_stocks
else:
    industry_dict["Latest Quarterly"] = st.session_state.listed_stocks

industry_dict['All Listed'] = st.session_state.listed_stocks

for each in watchlist:
    get_this_watchlist_db = each['_id']
    get_this_watchlist_db = get_this_watchlist_db.replace("/"," ")
    industry_dict[get_this_watchlist_db] = []
    for each_stock in each[each['_id']]:
        #each_stock is a stock name in the watchlist get_this_watchlist_db
        industry_dict[get_this_watchlist_db].append(each_stock)

# WATCHLIST OPTIONS
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
# with col3:
with st.sidebar:
    chose_genre = list(industry_dict.keys())
    temp_list_len = [f"{each_key} ({len(industry_dict[each_key])})" for each_key in chose_genre]   #to give name with number in the SelectBox

    # genre = st.radio("Watchlist:",chose_genre,)
    genre = st.selectbox("Watchlist:",chose_genre,)

funda_tech_options = ["Funda_Chart", 'Tech_Chart']#, 'Analyse Watchlist']
show_list_as = industry_dict[genre]
selected = st.sidebar.selectbox("", show_list_as, index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
        

# '''OLD METHOD OF SELCTING SELECTED'''

# chose_genre = ["Latest Quarterly", "All Listed", "Holdings", "Watchlist","Favourite"]
# genre = st.selectbox("Watchlist:",chose_genre,)

#                                                                                                                         # SELECTION OF WATCHLIST
# with col1:
#     if genre == "Latest Quarterly":
#         funda_tech_options = ["Funda_Chart", 'Tech_Chart']#, 'Analyse Watchlist']
#         # checks only Pickle
#         if len(st.session_state.latest_quarterly_stocks)>1:
#             show_list_as = st.session_state.latest_quarterly_stocks #if selected_stock in st.session_state.latest_quarterly_stocks else st.session_state.listed_stocks
#         else:
#             show_list_as = st.session_state.listed_stocks
#         selected = st.sidebar.selectbox("", show_list_as, index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
#         # selected = st.sidebar.selectbox("Pick",show_list_as,
#         #                                 index=st.session_state.latest_quarterly_stocks.index(selected_stock) if selected_stock in st.session_state.latest_quarterly_stocks else st.session_state.listed_stocks.index(selected_stock) if selected_stock in st.session_state.listed_stocks else 0)
        
#             # no_of_stocks_not_latest1 = []
#             # for each in temp_var:
#             #     if each.isdigit():
#             #         no_of_stocks_not_latest1.append(each) #(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
#             #     else:
#             #         no_of_stocks_not_latest1.append(each)
#             # with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
#             #     st.info(no_of_stocks_not_latest1)
#     elif genre =="All Listed" :
#         funda_tech_options = ["Funda_Chart", 'Tech_Chart']#, 'Analyse Watchlist']
#         show_list_as = st.session_state.listed_stocks
#         selected = st.sidebar.selectbox("", show_list_as, index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
        
#     # elif genre == "Holdings":
#     #     funda_tech_options = ["Funda_Chart", 'Tech_Chart']#, 'Analyse Watchlist']
#     #     update_txt_file = './watchlist/holdings.txt'
#     #     show_list_as = st.session_state.user_data['holdings_list']
#     #     # selected = st.sidebar.selectbox("", show_list_as,
#     #     #                 index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
#     #     if 'Holdings' not in st.session_state.no_of_stocks_not_latest:
#     #         st.session_state.no_of_stocks_not_latest['Holdings'] = scan_for_old_quarterly(holdings_list)
#     #     temp_var = st.session_state.no_of_stocks_not_latest['Holdings'] 
#     #     # DISPLAY IN WEBAPP ABT STOCKS WITHOUT LATEST QRESULTS
#     #     if len(temp_var) > 0:
#     #         with col2_header:
#     #             if st.button(f'{len(temp_var)} needs Latest Results'):
#     #                 save_screener1(temp_var)
#     #         no_of_stocks_not_latest1 = []
#     #         for each in temp_var:
#     #             if each.isdigit():
#     #                 no_of_stocks_not_latest1.append(each)    #(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
#     #             else:
#     #                 no_of_stocks_not_latest1.append(each)
#     #         with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
#     #             st.info(no_of_stocks_not_latest1)

#     # elif genre == "Watchlist":
#     #     funda_tech_options = ["Funda_Chart", 'Tech_Chart']#, 'Analyse Watchlist']
#     #     update_txt_file = './watchlist/watchlist.txt'
#     #     show_list_as = st.session_state.user_data['watch_list']
#     #     # selected = st.sidebar.selectbox("", show_list_as,
#     #     #                 index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
#     #     if 'Watchlist' not in st.session_state.no_of_stocks_not_latest:
#     #         st.session_state.no_of_stocks_not_latest['Watchlist'] = scan_for_old_quarterly(watch_list)
#     #     temp_var = st.session_state.no_of_stocks_not_latest['Watchlist']
#     #     # st.info(f"Out of {len(watch_list)} stocks, {len(temp_var)} have NO-LATEST results")

#     #     if len(temp_var) > 0:
#     #         with col2_header:
#     #             if st.button(f'{len(temp_var)} needs Latest Results'):
#     #                 save_screener1(temp_var)
#     #         no_of_stocks_not_latest1 = []
#     #         for each in temp_var:
#     #             if each.isdigit():
#     #                 no_of_stocks_not_latest1.append(each) #(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
#     #             else:
#     #                 no_of_stocks_not_latest1.append(each)
#     #         with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
#     #             st.info(no_of_stocks_not_latest1)
#     # elif genre == "Favourite":
#     #     funda_tech_options = ["Funda_Chart", 'Tech_Chart']#, 'Analyse Watchlist']
#     #     update_txt_file = './watchlist/favourite.txt'
#     #     show_list_as = st.session_state.user_data['favourite_list']
#     #     # selected = st.sidebar.selectbox("", show_list_as,
#     #     #                 index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
#     #     if 'Favourites' not in st.session_state.no_of_stocks_not_latest:
#     #         st.session_state.no_of_stocks_not_latest["Favourites"] = scan_for_old_quarterly(show_list_as)
#     #     temp_var = st.session_state.no_of_stocks_not_latest["Favourites"]
#     #     if len(temp_var) > 0:
#     #         with col2_header:
#     #             if st.button(f'{len(temp_var) } needs Latest Results'):
#     #                 save_screener1(temp_var)
#     #         # ONLY TO SHOW BOTH CODE AND NAME TOGETHER IN EXPANDER
#     #         no_of_stocks_not_latest1 = []
#     #         for each in temp_var:
#     #             if each.isdigit():
#     #                 no_of_stocks_not_latest1.append(each) #(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
#     #             else:
#     #                 no_of_stocks_not_latest1.append(each)
#     #         with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
#     #             st.info(no_of_stocks_not_latest1)



# st.experimental_set_query_params(selected=[selected],)
if selected: 
    funda_tech = option_menu("", funda_tech_options,
                             icons=['house', '📈 '], menu_icon="cast", default_index=0, orientation="horizontal")

    metadata = {}
    # st.success(selected)
    try:
        company_code, comp_Name = nse_bse_search.get_code_name(selected)
    except Exception as TypeError:
        save_screener1([selected],True)
        company_code, comp_Name = nse_bse_search.get_code_name(selected)


                                                                                                                            #SHOWUP SCREENER SITE
    nse_screener_address = "https://www.screener.in/company/" + str(company_code)
    with st.sidebar:
        st.markdown(f"[***NSE SCREENER***]({nse_screener_address})", unsafe_allow_html=True)
        
    if selected.isdigit():
        bse_screener_address = "https://www.screener.in/company/" + str(selected)
        with st.sidebar:
            st.markdown(f"[***BSE SCREENER***]({bse_screener_address})", unsafe_allow_html=True)
        
                                                                                                                         # ADD TO FAVOURITE TXT FILE
                                                                                                                        # GIVE A FAVOURITE BUTTON
    # with col4:
    #     if st.button("+FAVOURITE"):
    #         with open('./watchlist/favourite.txt', 'w') as file:
    #             file.write(selected)

    coltw1, coltw2 = st.columns([2, 2])
                                                                                                                        # TICKER INFORADING VIEW SITE
    ticker_symbol_info = str('''<!-- TradingView Widget BEGIN -->
                                        <div class="tradingview-widget-container">
                                          <div class="tradingview-widget-container__widget"></div>
                                          <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
                                          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
                                          {
                                          "symbol": "xyx",
                                          "width": "100%",
                                          "locale": "en",
                                          "colorTheme": "dark",
                                          "isTransparent": true
                                        }
                                          </script>
                                        </div>
                                        <!-- TradingView Widget END -->''')
    with coltw1:
        components.html(ticker_symbol_info.replace("xyx", company_code), height=200)
                                                                                                                            # FUNDA CHART TAB
    if funda_tech == "Funda_Chart":
        with st.sidebar:
            #color_key = st.selectbox("Bar Color", color_dict.keys())
            color_key = 'blue3'
        # tree_folder = comp_Name[0].upper()
        if company_code.isdigit():
            tree_folder = company_code[0]
        else:
            tree_folder = company_code[0].upper()

        with coltw2:
            subcoltw2_1, subcoltw2_2 = st.columns([1, 1])
            with subcoltw2_1:
                chat_name = st.text_input(label="👉 ChatID", value="itimesAlgo_D")
        
        # # if Quarterly data not available but YEARLY DATA AVAILABLE
        # if not os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):
        #     st.info("ONLY YEARLY DATA AVAILABLE FOR THIS SCRIPT")
        #     df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
        #     # st.info(f"Reading ./pickl/{tree_folder}/{comp_Name} Yearly.pkl")
        #     try:
        #         df_comp.columns = pd.to_datetime(df_comp,'%d-%m-%Y')
        #     except Exception as AttributeError:
        #         pass
        #     # st.dataframe(df_comp)
        #     pnl, balancesht,cashflow = fundamentals.develop_yearly(df_comp)
        #     # st.error("Yearly DATA not in order")
        #     metadata = fundamentals.analyse_Y_df(pnl,balancesht)
        #     metadata['code_names'] = nse_bse_search.process_code(company_code)
        #     metadata['Code'] = metadata['code_names'][-1]
        #     variables.metadata[company_code] = metadata
        
        # # if Quarterly data available and YEARLY DATA AVAILABLE
        # elif os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):
        #     df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
        #     # st.info(f"PKL FILE EXISTS, thus Reading './pickl/{tree_folder}/{comp_Name} Yearly.pkl'   ")
        #     #st.dataframe(df_comp)
        #     try:
        #         df_comp.columns = pd.to_datetime(df_comp,'%d-%m-%Y')
        #         #df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
        #     except Exception as AttributeError:
        #         pass
        #     # st.dataframe(df_comp)
        #     # st.text("**********************")
        #     pnl, balancesht,cashflow = fundamentals.develop_yearly(df_comp)

        #     qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl')
        #     # pnl, balancesht, qtr_pnl = fundamentals.develop_data(qtr_pnl, df_comp)
        #     try:
        #         qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
        #         # qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
        #     except Exception as AttributeError:
        #         pass
        #     qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)
        #     metadata = fundamentals.analyse_df(pnl,balancesht,qtr_pnl)

        #     metadata['code_names'] = nse_bse_search.process_code(company_code)
        #     metadata['Code'] = metadata['code_names'][-1]
        #     variables.metadata[company_code] = metadata

        # if no Pickle available : then lets get the latest results
        # else:
            # save_screener1([company_code])
            # metadata = variables.metadata[company_code]
            # if not os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):  # if Quarterly data not available
            #     df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
            #     st.info(f"ONLY YEARLY DATA AVAILABLE, thus Reading ./pickl/{tree_folder}/{company_code} Yearly.pkl")
            #     try:
            #         df_comp.columns = pd.to_datetime(df_comp, '%d-%m-%Y')
            #     except Exception as AttributeError:
            #         pass
            #     # st.dataframe(df_comp)
            #     pnl, balancesht,cashflow = fundamentals.develop_yearly(df_comp)
            #     metadata = fundamentals.analyse_Y_df(pnl,balancesht)
            #     metadata['code_names'] = nse_bse_search.process_code(company_code)
            #     metadata['Code'] = metadata['code_names'][-1]
            #     variables.metadata[company_code] = metadata

            # elif os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):
            #     st.info(f"PKL FILE EXISTS, thus Reading './pickl/{tree_folder}/{company_code} Yearly.pkl' and './pickl/{tree_folder}/{company_code} Quarterly.pkl'   ")
            #     df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
            #     # st.info(f"PKL FILE EXISTS, thus Reading './pickl/{tree_folder}/{comp_Name} Yearly.pkl'   ")
            #     # st.dataframe(df_comp)
            #     try:
            #         df_comp.columns = pd.to_datetime(df_comp, '%d-%m-%Y')
            #         # df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
            #     except Exception as AttributeError:
            #         pass
            #     pnl, balancesht,cashflow = fundamentals.develop_yearly(df_comp)

            #     qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl')
                
            #     try:
            #         qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
            #         # qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
            #     except Exception as AttributeError:
            #         pass

            #     qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)
            #     metadata = fundamentals.analyse_df(pnl, balancesht, qtr_pnl)
            #     metadata['code_names'] = nse_bse_search.process_code(company_code)
            #     metadata['Code'] = metadata['code_names'][-1]
            #     variables.metadata[company_code] = metadata

        #print random number 
        
        # already_tried = "FALSE"
        # if st.checkbox("FORCE DOWNLOAD FROM SCREENER", value=False):
        #     save_screener1([company_code])            
        #     already_tried = "TRUE"
        if create_database.comp_metadata_col.count_documents({"code_names":company_code}):
            reqd_obj = create_database.comp_metadata_col.find_one({"code_names":company_code})
            variables.metadata[company_code] = reqd_obj
        metadata = variables.metadata[company_code]


        if 'CONSOLIDATED' in metadata.keys() and 'STANDALONE' in metadata.keys():
            cons_std = option_menu("", ["CONSOLIDATED","STANDALONE"],
                        icons=['📈 ', '📈 '], menu_icon="cast", default_index=0, orientation="horizontal")

        if 'CONSOLIDATED' in metadata.keys() or 'STANDALONE' in metadata.keys():
            # IMPROVISE : lets give 2 tabs here to select amongst CONSOL and STANDLONE
            if 'CONSOLIDATED' in metadata.keys():
                df_comp_dict = metadata['CONSOLIDATED']['YEARLY'] #get df from metadata of fdatabase
                # df_comp = pd.DataFrame.from_dict(df_comp_dict, orient='index').transpose()
                df_comp = pd.concat({sec: pd.DataFrame.from_dict(items, orient='index') for sec, items in df_comp_dict.items()})
                # Optional: Name the index
                df_comp.index.set_names(['Section', 'Item'], inplace=True)
                df_comp.columns = pd.to_datetime(df_comp.columns)
                # st.success("Seems like we got a DF from DB")
                # st.dataframe(df_comp)
                pnl, balancesht,cashflow = fundamentals.develop_yearly(df_comp)

                qtr_pnl_dict = metadata['CONSOLIDATED']['QUARTERLY']#get dataframe from DB
                qtr_pnl = pd.DataFrame.from_dict(qtr_pnl_dict, orient='index').transpose()
                # st.dataframe(qtr_pnl)
                qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)        
            else:
                df_comp_dict = metadata['STANDALONE']['YEARLY'] #get df from metadata of fdatabase
                # df_comp = pd.DataFrame.from_dict(df_comp_dict, orient='index').transpose()
                df_comp = pd.concat({sec: pd.DataFrame.from_dict(items, orient='index') for sec, items in df_comp_dict.items()})
                # Optional: Name the index
                df_comp.index.set_names(['Section', 'Item'], inplace=True)
                df_comp.columns = pd.to_datetime(df_comp.columns)
                # st.dataframe(df_comp)
                pnl, balancesht,cashflow = fundamentals.develop_yearly(df_comp)
                qtr_pnl_dict = metadata['STANDALONE']['QUARTERLY']#get dataframe from DB
                qtr_pnl = pd.DataFrame.from_dict(qtr_pnl_dict, orient='index').transpose()
                # st.dataframe(qtr_pnl)
                qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)        

        proscons_col1, proscons_col2 = st.columns([1,1])
        with proscons_col1:
            st.text("SECTOR:")
            st.subheader(f"{metadata['comp_metadata']['sector']}")
            st.title("PROS")
            for each in metadata['metadata']['pros']:
                st.success(each)


        with proscons_col2:
            st.text("INDUSTRY:")
            st.subheader(f"{metadata['comp_metadata']['industry']}")
            st.title("CONS")
            for each in metadata['metadata']['cons']:
                st.error(each)
            
        options = st.multiselect("TAGS",["Favourite"]+metadata['metadata']['tags'],metadata['metadata']['tags'])
        

        with st.sidebar:  # with col2:
            sub_choose = st.selectbox("Fundamentals:", fundamentals.funda_menu)
            # st.title(comp_Name)


        sentence = amibroker.amibroker_notes_insights(metadata=metadata)
        

        with coltw2:
            textarea_is = st.text_area(label="👉 INSIGHTS", value=sentence, height=180, key="InsightsYQ")

            # file_like = io.StringIO(sentence)
            # Provide a download button
            # st.download_button(
            #     label=f"📥 Download {company_code}",
            #     data=file_like,
            #     file_name=f"{company_code}.txt",
            #     mime="text/plain"
            # )
        with subcoltw2_2:            
            if st.button('Send Telegram'):
                # bot.send_message(chat_id=chat_id, text=sentence)
                # URL encode the message
                message_txt_encoded = urllib.parse.quote(textarea_is)
                # Construct the Telegram API URL
                group_address = f'https://api.telegram.org/bot1698319688:AAG5X-bmCzGqWHIyaksIUfBG_rxZRE3tUvI/sendMessage?chat_id=@{chat_name}&text={message_txt_encoded}'

                # Send the message
                resp = requests.get(group_address)

        # with col2_header:
            # pnl, balancesht,cashflow = fundamentals.develop_yearly()
                
            # if st.button("Read Data from Database"):
            #     yr_cons,yr_std,qtr_cons,qtr_std = screenerpage.read_database_to_get_df(id_value=metadata['code_names'][-1])
            #     if not yr_cons.eq(0).all().all() and not yr_cons.empty:
            #         st.dataframe(yr_cons)
            #     if not qtr_cons.eq(0).all().all() and not qtr_cons.empty:
            #         st.dataframe(qtr_cons)
            #     if not yr_std.eq(0).all().all() and not yr_std.empty:
            #         st.dataframe(yr_std)
            #     if not qtr_std.eq(0).all().all() and not qtr_std.empty:
            #         st.dataframe(qtr_std)


        #sub_choose = option_menu("", fundamentals.funda_menu,default_index=3,orientation="horizontal")
        if sub_choose == "PROFIT&LOSS":            # YEARLY PNL
            Ykeydata,YSales, YOtherIncome,YExpenses,YOperatingProfit,YNetProfit,Ytable = st.tabs(['Key Data','SALES','OTHER INCOME','EXPENSES','OPERATING PROFIT','NET PROFIT','Y DATA'])

            with Ytable:
                # THE FOLLOWIGN CODE CALCULATES THE GROWTH OR DEGROWTH
                st.dataframe(pnl.style.format(formatter="{:.1f}"))
            with Ykeydata:
                plotlyfigures.group_2_bars(pnl,"SALES","OTHER INCOME",comp_Name, "Yearly")
                plotlyfigures.group_2_bars(pnl,"PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Yearly")
                #plotlyfigures.group_3_bars(pnl, "SALES", "PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Yearly")
                plotlyfigures.both_lines(pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'], comp_Name, "Yearly")
                plotlyfigures.bar_line(pnl, 'OPERATING PROFIT','OPM %', color_dict[color_key]['hash'], comp_Name, "Yearly")
                plotlyfigures.bar_line(pnl,'NET PROFIT','NPM %',color_dict[color_key]['hash'],comp_Name, "Yearly")

            with YSales:
                plotlyfigures.qoq_growth(pnl, 'SALES', color_dict[color_key]['hash'], comp_Name, "Yearly")
            with YOtherIncome:
                plotlyfigures.go_bar(pnl, 'OTHER INCOME', color_dict[color_key]['hash'], comp_Name,"Yearly")
            with YExpenses:
                plotlyfigures.go_bar(pnl, 'EXPENSES', color_dict[color_key]['hash'], comp_Name,"Yearly")
            with YOperatingProfit:
                plotlyfigures.qoq_growth(pnl, 'OPERATING PROFIT', color_dict[color_key]['hash'], comp_Name, "Yearly")
            with YNetProfit:
                plotlyfigures.qoq_growth(pnl,'NET PROFIT',color_dict[color_key]['hash'],comp_Name, "Yearly")

        if sub_choose == 'QTR PnL':                #QUARTERLY PNL

            Qkeydata, QSales, QOtherIncome, QExpenses, QOperatingProfit, QNetProfit, Qtable = st.tabs(
                ['Key Data', 'SALES', 'OTHER INCOME', 'EXPENSES', 'OPERATING PROFIT', 'NET PROFIT', 'Q DATA'])
            with Qtable:
                st.dataframe(qtr_pnl)
                # Replace the first row with NaN for the QoQ columns
                #df.loc[0, ['SALES_QoQ', 'NET PROFIT_QoQ', 'OPERATING PROFIT_QoQ']] = np.nan
                #df = df.transpose()
                #st.dataframe(qtr_pnl.style.format(formatter="{:.1f}"))

            with Qkeydata:
                plotlyfigures.group_2_bars(qtr_pnl, "SALES", "OTHER INCOME",comp_Name, "Quarterly")
                plotlyfigures.group_2_bars(qtr_pnl,"PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Quarterly")
                #plotlyfigures.group_3_bars(qtr_pnl, "SALES",  "PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Quarterly")
                plotlyfigures.both_lines(qtr_pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'],comp_Name, "Quarterly")
                plotlyfigures.bar_line(qtr_pnl, 'OPERATING PROFIT','OPM %', color_dict[color_key]['hash'], comp_Name, "Quarterly")
                plotlyfigures.bar_line(qtr_pnl,'NET PROFIT','NPM %',color_dict[color_key]['hash'],comp_Name, "Quarterly")

            with QSales:
                plotlyfigures.qoq_growth(qtr_pnl,"SALES", color_dict[color_key]['hash'],comp_Name, "Quarterly")
            with QOtherIncome:
                plotlyfigures.go_bar(qtr_pnl, 'OTHER INCOME', color_dict[color_key]['hash'], comp_Name, "Quarterly")
            with QExpenses:
                plotlyfigures.go_bar(qtr_pnl, 'EXPENSES', color_dict[color_key]['hash'], comp_Name, "Quarterly")
            with QOperatingProfit:
                plotlyfigures.qoq_growth(qtr_pnl, 'OPERATING PROFIT', color_dict[color_key]['hash'], comp_Name, "Quarterly")
            with QNetProfit:
                plotlyfigures.qoq_growth(qtr_pnl,'NET PROFIT',color_dict[color_key]['hash'],comp_Name, "Quarterly")

        if sub_choose == 'BALANCE SHEET':        #YEARLY BALANCE SHEET
            BSKeyData, BSReserves, BSBorrowings, BSOtherAssets, BSOtherLiabilities, BSReceivables, BSInventory, BSCWIP, BStable = st.tabs(['KeyData','Reserves','Borrowings','OtherAssets','OtherLiabilities','Receivables','Inventory','CWIP','BS DATA'])
            with BSKeyData:
                plotlyfigures.bar_line(balancesht,"RESERVES","BORROWINGS",color_dict[color_key]['hash'],comp_Name, "Yearly")
                plotlyfigures.bar_line(balancesht,"RECEIVABLES","INVENTORY",color_dict[color_key]['hash'],comp_Name, "Yearly")
                plotlyfigures.bar_line(balancesht, "DEBTOR DAYS", "INVENTORY TURNOVER",color_dict[color_key]['hash'], comp_Name, "Yearly")
                plotlyfigures.bar_line(balancesht, "NET BLOCK", "CAPITAL WORK IN PROGRESS",color_dict[color_key]['hash'], comp_Name, "Yearly")
                #plotlyfigures.bar_line(balancesht, "NET BLOCK", "INVESTMENTS", color_dict[color_key]['hash'], comp_Name,"Yearly")
                #plotlyfigures.both_lines(balancesht, "ROCE", "ROE", color_dict[color_key]['hash'], color_line,comp_Name, "Yearly")

            with BStable:
                st.dataframe(balancesht.style.format(formatter="{:.1f}"))
            with BSCWIP:
                plotlyfigures.go_bar(balancesht, "CAPITAL WORK IN PROGRESS", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSInventory:
                plotlyfigures.go_bar(balancesht, "INVENTORY", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSReserves:
                plotlyfigures.qoq_growth(balancesht, "RESERVES", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSBorrowings:
                plotlyfigures.qoq_growth(balancesht, "BORROWINGS", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSReceivables:
                plotlyfigures.qoq_growth(balancesht, "RECEIVABLES", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSOtherAssets:
                plotlyfigures.qoq_growth(balancesht, "OTHER ASSETS", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSOtherLiabilities:
                plotlyfigures.qoq_growth(balancesht, "OTHER LIABILITIES", color_dict[color_key]['hash'],comp_Name, "Yearly")

        if sub_choose == 'CASH FLOW':        # YEARLY CASH FLOWS
            CF, CFop, CFinv, CFfin, NetCF, CFTab = st.tabs(["KeyData","Operating Cash","Investing Cash","Financing Cash","Net Cash Flow","Table"])
            with CFTab:
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
            with CF:
                plotlyfigures.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_dict[color_key]['hash'],"Yearly")
            with CFop:
                plotlyfigures.qoq_growth(df_comp.loc[sub_choose], "CASH FROM OPERATING ACTIVITY", color_dict[color_key]['hash'],comp_Name,"Yearly")
            with CFfin:
                plotlyfigures.go_bar(df_comp.loc[sub_choose], "CASH FROM FINANCING ACTIVITY", color_dict[color_key]['hash'], comp_Name,"Yearly")
            with CFinv:
                plotlyfigures.go_bar(df_comp.loc[sub_choose], "CASH FROM INVESTING ACTIVITY", color_dict[color_key]['hash'],comp_Name,"Yearly")
            with NetCF:
                plotlyfigures.go_bar(df_comp.loc[sub_choose], "NET CASH FLOW", color_dict[color_key]['hash'], comp_Name,"Yearly")

        if sub_choose == 'Key_Data':
            key_data = str("""<!-- TradingView Widget BEGIN -->
                                    <div class="tradingview-widget-container">
                                      <div class="tradingview-widget-container__widget"></div>
                                      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/financials-overview/" rel="noopener" target="_blank"><span class="blue-text">Fundamental Data</span></a> by TradingView</div>
                                      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-financials.js" async>
                                      {
                                      "colorTheme": "dark",
                                      "isTransparent": false,
                                      "largeChartUrl": "",
                                      "displayMode": "regular",
                                      "width": "100%",
                                      "height": 880,
                                      "symbol": "xx",
                                      "locale": "en"
                                      }
                                      </script>
                                    </div>
                                    <!-- TradingView Widget END -->
                                """)

            comp_profile = str("""
                                    <!-- TradingView Widget BEGIN -->
                                    <div class="tradingview-widget-container">
                                      <div class="tradingview-widget-container__widget"></div>
                                      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text"> Profile</span></a> by TradingView</div>
                                      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
                                      {
                                      "width": "100%",
                                      "height": 880,
                                      "colorTheme": "dark",
                                      "isTransparent": false,
                                      "symbol": "xxyy",
                                      "locale": "en"
                                    }
                                      </script>
                                    </div>
                                    <!-- TradingView Widget END -->
                                    """)
            with st.expander(label="TRADINGVIEW DATA"):
                colx, coly = st.columns([1.5, 1])
                with colx:
                    components.html(key_data.replace("xx", company_code), height=1080)
                with coly:
                    components.html(comp_profile.replace("xxyy", company_code), height=1080)
            with st.expander(label='BALANCE SHEET'):
                st.dataframe(balancesht)
            with st.expander(label='YEARLY PNL'):
                st.dataframe(pnl)
            with st.expander(label='QUARTERLY PNL'):
                st.dataframe(qtr_pnl)

            keydata_col1, keydata_col2 = st.columns([1,1])
            with keydata_col1:
                plotlyfigures.bar_line(balancesht, "DEBTOR DAYS", "INVENTORY TURNOVER", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with keydata_col2:
                plotlyfigures.bar_line(balancesht, "NET BLOCK", "CAPITAL WORK IN PROGRESS", color_dict[color_key]['hash'], comp_Name,"Yearly")
            with keydata_col1:
                plotlyfigures.bar_line(balancesht, "RESERVES", "BORROWINGS", color_dict[color_key]['hash'], comp_Name,"Yearly")
            with keydata_col2:
                plotlyfigures.bar_line(balancesht, "WORKING CAPITAL", "CASH & BANK", color_dict[color_key]['hash'],comp_Name,"Yearly")

            with keydata_col1:
                st.title("QUARTERLY")
                plotlyfigures.group_2_bars(qtr_pnl, "SALES", "OTHER INCOME", comp_Name, "Quarterly")

            with keydata_col2:
                st.title("YEARLY")
                plotlyfigures.group_2_bars(pnl, "SALES", "OTHER INCOME", comp_Name, "Yearly")

            with keydata_col1:
                plotlyfigures.both_lines(qtr_pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'],
                                        comp_Name, "Quarterly")
                plotlyfigures.bar_line(qtr_pnl, 'NET PROFIT', 'NPM %', color_dict[color_key]['hash'], comp_Name, "Quarterly")

            with keydata_col2:
                plotlyfigures.both_lines(pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'],
                                        comp_Name, "Yearly")
                plotlyfigures.bar_line(pnl, 'NET PROFIT', 'NPM %', color_dict[color_key]['hash'], comp_Name, "Yearly")

            plotlyfigures.go_group_bar(df_comp.loc['CASH FLOW'], "cash_flows", color_dict[color_key]['hash'], "Yearly")

        # for each in variables.metadata.keys():
        #     st.info(each)

    
    # if funda_tech == "Funda_Chart":
    #     with st.sidebar:
    #         #color_key = st.selectbox("Bar Color", color_dict.keys())
    #         color_key = 'blue3'
    #     # tree_folder = comp_Name[0].upper()
    #     # if company_code[0].isdigit():
    #     #     tree_folder = company_code[0]
    #     # else:
    #     #     tree_folder = company_code[0].upper()
    #     # SHOW CONSOLIDATED AND STANDALONE
    #     yr_cons_dict,yr_std_dict,qtr_cons_dict,qtr_std_dict = screenerpage.read_database_to_get_df(id_value=company_code[0])

    #     sub_chose_dict = {}
    #     sub_chose_dict["Consolidated"] = {}
    #     sub_chose_dict["Standalone"] = {}

    #     #check consolidated data
        
    #     if len(yr_cons_dict)!=0:
    #         if len(qtr_cons_dict)!=0:
    #             # both yearly and qtr data available in Consolidated
    #             consolidated_data_availability = True
    #             sub_chose_dict["Consolidated"]["Yearly"] = yr_cons_dict
    #             sub_chose_dict["Consolidated"]["Quarterly"] = qtr_cons_dict
    #         else:
    #             #only yearly data is available in Consolidated data
    #             consolidated_yearly_availablity = True
                
    #             sub_chose_dict["Consolidated"]["Yearly"] = qtr_cons_dict
    #     elif len(qtr_cons)!=0:
    #         consolidated_quarterly_availability = True
    #         sub_chose_dict['Consolidated']['Quarterly'] = yr_cons_dict
        
    #     #check Standalone data
    #     if len(yr_std)!=0:
    #         if len(qtr_std)!=0:
    #             standalone_data_availability = True
    #             sub_chose_dict["Standalone"]["Yearly"] = yr_std_dict
    #             sub_chose_dict["Standalone"]["Quarterly"] = qtr_std_dict
    #         else:
    #             standalone_yearly_availablity = True
    #             sub_chose_dict["Standalone"]["Yearly"] = yr_std_dict

    #     elif len(qtr_std)!=0:
    #         standalone_quarterly_availablity = True
    #         sub_chose_dict["Standalone"]["Quarterly"] = qtr_std_dict

    #     if consolidated_data_availability==False and standalone_data_availability == False:
    #         st.error("No data available for this company")
    #     else:
    #         # make list of sub_chose_dict keys?
    #         main_chose = list(sub_chose_dict.keys())


    #         sub_choose = st.selectbox("Fundamentals:", fundamentals.funda_menu)


    if funda_tech == "Tech_Chart":
        with st.expander(label="IF ERROR / FETCHING APPLE STOCK"):
            st.write("We are having issues in generating Tech Charts for BSE Codes and some of the NSE codes as well.")
            st.write("Appreciate using our site. Will fix this asap")
        tech_widget = str("""<!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
              <div id="analytics-platform-chart-demo"></div>
              <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Chart</span></a> by TradingView</div>
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget(
              {
              "container_id": "analytics-platform-chart-demo",
              "width": "100%","height": "680",
              "symbol": "xxyyzz",
              "interval": "W",
              "timezone": "exchange",
              "theme": "dark",
              "style": "0",
              "toolbar_bg": "#f1f3f6",
              "withdateranges": true,
              "allow_symbol_change": true,
              "save_image": false,
              "details": true,"hotlist": true,"calendar": true,
              "studies": [
                {id:"RSI@tv-basicstudies"},
                {id:"MASimple@tv-basicstudies", inputs: {length:21}},
                {id:"MASimple@tv-basicstudies", inputs: {length:55}}
              ],
              "show_popup_button": true,
              "popup_width": "1000",
              "popup_height": "650",
              "locale": "en"
            }
              );
              </script>
            </div>
            <!-- TradingView Widget END -->""")
        tech1_widget = tech_widget.replace("xxyyzz",company_code)
        components.html(tech1_widget.replace("xxyyzz",company_code), height = 1080)
        tech_chart_widget = """<!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
          <div id="technical-analysis-chart-demo"></div>
          <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Chart</span></a> by TradingView</div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget(
          {
          "container_id": "technical-analysis-chart-demo",
          "width": "100%",
          "height": "680",
          "symbol": "nifty",
          "interval": "D",
          "timezone": "exchange",
          "theme": "dark",
          "style": "1",
          "toolbar_bg": "#f1f3f6",
          "withdateranges": true,
          "hide_side_toolbar": false,
          "allow_symbol_change": true,
          "save_image": false,
          "studies": [
            "RSI@tv-basicstudies",
            "MASimple@tv-basicstudies",
            "MASimple@tv-basicstudies"
          ],
          "show_popup_button": true,
          "popup_width": "1000",
          "popup_height": "650",
          "locale": "en"
        }
          );
          </script>
        </div>
        <!-- TradingView Widget END -->"""
        # components.html(tech_chart_widget, height=1080)



# if st.checkbox("DONOT TICK THIS : UPLOAD", value=False):
    # Function to load the dictionary from a file
    # def load_metadata():
    #     if os.path.exists('./metadata.pkl'):
    #         with open('./metadata.pkl', 'rb') as f:
    #             return pickle.load(f)
    #     else:
    #         return {}

    # def save_metadata():
    #     with open('./metadata.pkl', 'wb') as f:
    #         pickle.dump(variables.metadata, f)
    #         print("Metadata saved successfully")
    #     saved_on = datetime.datetime.now()
    #     # with open('./userdata.pkl','wb') as f:
    #     #     pickle.dump(st.session_state.user_data, f)
    #     #     print("Userdata saved succesfully")

#     with subcoltw2_2:
#         if st.button("Save Insight&Meta"):
#             create_database.insert_stock_metadata(col = create_database.company_metadata_col, dict=metadata, id = dict['Code'])
#             save_metadata()
#             st.success("Saved Metadata in Database as well, and in amibroker notes file") 
#     with coltw1:
#         KeyNotes_source = st.text_input(label="KeyNotes Source: Enter the URL for Future Reference", value="")
#         KeyNotes_input = st.text_area(label="News / Announcement / Notes",value="", height=60, key="KeyNotes")
#         save_KeyNotes_in_db = st.button("Save")
#         if save_KeyNotes_in_db:
#             my_dict = {}
#             my_dict['datetime'] = datetime.datetime.now()
#             my_dict['Source'] = KeyNotes_source
#             my_dict['Notes'] = KeyNotes_input
#             create_database.insert_dict(col=create_database.create_database.company_metadata_col, id_value=company_code, save_within_document="KeyNotes", dict=my_dict, task="REPLACE")
#             st.success("Notes saved in database")

#     with st.expander(label=f"Metadata of {company_code}"):
#         for each in metadata.keys():
#             st.info(f"{each} : {metadata[each]}")


#     with col2_header:
#         if st.button("SAVE METADATA"):
#             save_metadata()
#             st.success("Metadata saved successfully in pickle form")
#         if st.button('Get aminotes from DB'):
#             amibroker.ami_notes_from_database1()
#             st.success(f"Saved in amibroker/dbnotes/")
#         if st.button(f'GET RESULTS : Script'):
#             save_screener1([metadata['code_names'][-1]])
#         if st.button(f"Process all Pickle Files in this watchlist and make TAGS from this WATCHLIST"):
#             for each_code in show_list_as:
#                 code_names = nse_bse_search.process_code(company_code)                    
#                 if os.path.exists(f"./pickl/{company_code[0]}/{company_code} Yearly.pkl") and os.path.exists(f"./pickl/{company_code[0]}/{company_code} Quarterly.pkl"):
#                     with open(f"./pickl/{company_code[0]}/{company_code} Yearly.pkl", 'rb') as file:
#                         yr_df = pickle.load(file)                    
#                     with open(f"./pickl/{company_code[0]}/{company_code} Quarterly.pkl", 'rb') as file:
#                         qtr_df = pickle.load(file)
#                     st.success(f"Processing {company_code}")
#                     pnl, balancesht,cashflow = fundamentals.develop_yearly(yr_df)
#                     qtr_pnl = fundamentals.develop_quarterly(qtr_df)
#                     metadata = fundamentals.analyse_df(pnl, balancesht, qtr_pnl)
#                     metadata['code_names'] = code_names
#                     metadata['Code'] = code_names[-1]
#                     variables.metadata[company_code] = metadata
#                     write_tags_to_txt(metadata=metadata)
#                     save_metadata()
            
    
#         if st.button("Download ALL stocks again:"):
#             save_screener1(st.session_state.listed_stocks)
#         if len(st.session_state.no_of_stocks_not_latest) > 0:
#             # st.error(temp_var)
#             if st.button(f'Get Results of {len(st.session_state.no_of_stocks_not_latest)} scripts with NO_LATEST_RESULTS'):
#                 save_screener1(st.session_state.no_of_stocks_not_latest)

#         if st.button(f'Get Latest Results from this watchlist'):
#             save_screener1(show_list_as)

#         if selected:
#             if st.button(f'Get Latest Results for {selected}'):
#                 save_screener1([selected])




# if 'Not Latest Quarterly' not in st.session_state.no_of_stocks_not_latest:
#     st.session_state.no_of_stocks_not_latest['Not Latest Quarterly'] = scan_for_old_quarterly(st.session_state.listed_stocks)                

# with st.expander(label="METADATA"):
#     st.success(f"We got about {len(metadata.keys())} saved in our Metadata")
#     i=0
#     for each in variables.metadata.keys():
#         st.info(each)
#         i+=1
#         if i==5: break
#
#     st.success(f"We got about {len(variables.metadata.keys())} saved in our Metadata")

st.write("____")
st.write('made with :green_heart: to Indian Stock Investors')

#Custom CSS to remove header,footer, hamburger icon
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)


tick_force = st.checkbox(label="Force Download",value=False)
if st.button("Download ALL stocks again:"):
    try:
        save_screener1(st.session_state.listed_stocks,True)
    except Exception as e:
        st.error("You are running on Server, Only Sahaveer has access")
        st.error(e)

if st.button(f'Get Latest Results from this watchlist'):
    try:
        save_screener1(show_list_as,tick_force)
    except Exception as e:
        st.error("You are running on Server, Only Sahaveer has access")
        st.error(e)

if selected:
    if st.button(f'Get Latest Results for {selected}'):
        try:
            save_screener1(codes=[selected],force=True)
        except Exception as e:
            st.error("You are running on Server, Only Sahaveer has access")
            st.error(e)

if st.button('Save all data in DB as notes:'):
    amibroker.ami_notes_from_database1()
    st.success(f"Saved in amibroker/dbnotes/")


#REFERENCE :
#FLASK : https://www.datasciencelearner.com/how-to-create-a-bar-chart-from-a-dataframe-in-python/#:~:text=There%20is%20also%20another%20method%20to%20create%20a,y-axis%20values%20you%20want%20to%20draw%20the%20bar.

#Streamlit Basics : https://www.datacamp.com/tutorial/streamlit#on-windows-

# https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb#:~:text=When%20building%20data%20apps%20using%20Streamlit%2C%20sometimes%20you,displayed%20in%20the%20app%20looks%20plain%20and%20static.

#https://towardsdatascience.com/create-a-bar-chart-race-animation-app-using-streamlit-and-raceplotly-e44495249f11


#   https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/



# if 'nsecode_list' not in st.session_state or 'nseISIN_list' not in st.session_state:
#     nse_data = pd.read_csv('./cm21JUN2024bhav.csv')
#     nse_data.columns = nse_data.columns.str.replace(' ', '_')
#     st.session_state.nseISIN_list = nse_data["ISIN"].tolist()
#     st.session_state.nsecode_list = nse_data["SYMBOL"].tolist()

#import json
#from streamlit_lottie import st_lottie
#from streamlit_lottie import st_lottie_spinner

# def load_userdata():
#     if os.path.exists('./userdata.pkl'):
#         with open('./userdata.pkl', 'rb') as f:
#             try:
#                 return pickle.load(f)
#             except Exception as EOFError:
#                 return {}
#     else:
#         return {}

# variables.user_data = load_userdata()

# if 'user_data' not in st.session_state:
#     st.session_state.user_data = variables.user_data

# ONLY TO MAKE SURE NOT TO OVERWRITE THE GROUPS FOLDERS
# fromwhere = './watchlist/groups/**/'
# typeoffile = '*.txt'
# files = glob.iglob(r''+fromwhere + typeoffile, recursive=True)  # making recursive True gives sub directories as well
# for file in files:
#     chang = str(file)
#     txt_files_dir = chang.replace("\\","/")
#     txt_file_name_only = os.path.basename(txt_files_dir)
#     variables.user_data[txt_file_name_only.split('.')[0]] = []
#     with open(f"{txt_files_dir}",'r') as file:
#         for each_line in file:
#             # print(each_line)
#             variables.user_data[txt_file_name_only.split('.')[0]].append(each_line.strip())

# st.info(variables.user_data)
# global bsecodenum_codename
# # global bsecodename_codenum
# if 'bsecodenum_codename' not in st.session_state and 'bsecodename_codenum' not in st.session_state:
#     st.session_state.bsecodenum_codename,st.session_state.bsecodename_codenum,bsecodenum_fullname,bsecodename_fullname,bsefullname_codenum,bsefullname_codename = nse_bse_search.bsecodenum_bsecodename()
#     # This gets us the BSE NAME from the DAILY BHAVCOPY THAT WE ARE DOWNLOADING
#     st.session_state.bsesccode_scname,st.session_state.bsescname_sccode = nse_bse_search.bseSCNAME_SCCODE()


# def load_lottiefile(filepath: str):
#     with open(filepath, "r") as f:
#         return json.load(f)
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_bar = load_lottiefile("./lottie/barchart.json")  # replace link to local lottie file
# lottie_data_analysis = load_lottiefile("./lottie/data-analysis.json")
# with st.sidebar:
#     st_lottie(
#         lottie_data_analysis,
#         speed=0.7,
#         reverse=False,
#         loop=True,
#         quality="low",  # medium ; high
#         height=None,
#         width=None,
#         key="barchart",)

#REGARDING USER DATA 

# def liked_stocks(script_code):
#     if "liked" in st.session_state.user_data:
#         st.session_state.user_data['liked'].append(script_code)
#     else:
#         st.session_state.user_data['liked'] = []
#         st.session_state.user_data['liked'].append(script_code)

# def disliked_stocks(script_code):
#     if "disliked" in st.session_state.user_data:
#         st.session_state.user_data['disliked'].append(script_code)
#     else:
#         st.session_state.user_data['disliked'] = []
#         st.session_state.user_data['disliked'].append(script_code)



#NEED TO USE DATABASE FOR THIS holdings_func, watchlist_func
# holdings_list = []
# watch_list = []

# @st.cache_data
# def holdings_func():
#     if os.path.exists('./watchlist/holdings.txt'):
#         holdings_list = []
#         # Open the file in read mode
#         with open('./watchlist/holdings.txt', 'r') as file:                                                                       # Read each line and append it to the list
#             for line in file:
#                 holdings_list.append(line.strip())
#         unique_holdings_list = nse_bse_search.remove_duplicate_in_watchlist(holdings_list)
#         # st.info(f"{len(holdings_list)} is reduced to {len(unique_holdings_list)}")
#         with open('./watchlist/holdings.txt', 'w') as file:  # Read each line and append it to the list
#             for line in unique_holdings_list:
#                 file.write(line + "\n")
#     return unique_holdings_list

# @st.cache_data
# def watchlist_func():
#     if os.path.exists('./watchlist/watchlist.txt'):
#         watch_list = []
#         with open('./watchlist/watchlist.txt', 'r') as file:  # Read each line and append it to the list
#             for line in file:
#                 watch_list.append(line.strip())
#         unique_watchlist = nse_bse_search.remove_duplicate_in_watchlist(watch_list)
#         # st.info(f"{len(watch_list)} is reduced to {len(unique_watchlist)}")
#         with open('./watchlist/watchlist.txt', 'w') as file:  # Read each line and append it to the list
#             for line in unique_watchlist:
#                 file.write(line + "\n")
#     return unique_watchlist

# @st.cache_data
# def favourite_func():
#     if os.path.exists('./watchlist/favourite.txt'):
#         added_watch_list = []
#         with open('./watchlist/favourite.txt', 'r') as file:  # Read each line and append it to the list
#             for line in file:
#                 added_watch_list.append(line.strip())
#         unique_added_watch_list = nse_bse_search.remove_duplicate_in_watchlist(added_watch_list)
#     return unique_added_watch_list

# if 'holdings_list' not in st.session_state.user_data:
#     st.session_state.user_data['holdings_list'] = holdings_func()
# if 'watch_list' not in st.session_state.user_data:
#     st.session_state.user_data['watch_list'] = watchlist_func()
# if 'favourite_list' not in st.session_state.user_data:
#     st.session_state.user_data['favourite_list'] = favourite_func()

# holdings_list = st.session_state.user_data['holdings_list']
# watch_list = st.session_state.user_data['watch_list']
# favourite_list = st.session_state.user_data['favourite_list']



# def get_code(query):
    #need to make sure this is from Database
    # if 'bsenames_list' not in st.session_state or 'bsecodes_list' not in st.session_state:  # if 'bse_ISIN' not in st.session_state or 'bse_ycode' not in st.session_state
    #     bse_data = pd.read_csv('./Select.csv', header=0, index_col=False)
    #     bse_data.columns = bse_data.columns.str.replace(' ', '_')
    #     st.session_state.bse_ISIN = bse_data["ISIN_No"].tolist()
    #     st.session_state.bse_ycode = bse_data["Security_Id"].tolist()
    #     st.session_state.bsenames_list = bse_data["Security_Name"].tolist()
    #     st.session_state.bsecodes_list = bse_data["Security_Code"].tolist()

    # if 'nsecode_list' not in st.session_state or 'nseISIN_list' not in st.session_state:
    #     nse_data = pd.read_csv('./cm21JUN2024bhav.csv')
    #     nse_data.columns = nse_data.columns.str.replace(' ', '_')
    #     st.session_state.nseISIN_list = nse_data["ISIN"].tolist()
    #     st.session_state.nsecode_list = nse_data["SYMBOL"].tolist()

    # query = query.strip()
    # # TEMPORARY CONVERTING THIS TO CODE NUMBER
    # company_code = None
    # code_name = None
    # if query.isdigit():
    #     company_code = (query)
    #     if int(company_code) in st.session_state.bsecodenum_codename.keys():
    #         code_name = st.session_state.bsecodenum_codename[int(company_code)]
    #     else:
    #         code_name = query              

    # else:
    #     if query in st.session_state.nsecode_list:
    #         company_code = query
    #         code_name = query
    #     else:
    #         if query in st.session_state.bsecodename_codenum.keys():
    #             company_code = str(st.session_state.bsecodename_codenum[query])
    #             code_name = query
    #         else:
    #             company_code = str(query)
    #             code_name = query
                
    # #st.info(company_code)
    # return company_code, code_name


# to GET LIST OF STOCKS IN WATCHLIST and MAKE WATCHLISTS AS PER TAGS and show them as DROPDOWN LIST
# company_in = {}
# company_in['ALL'] = show_list_as
# for company_code in show_list_as:
#     try:
#         # st.success(variables.metadata[company_code])
#         if company_code in variables.metadata.keys():
#             if 'tags' not in variables.metadata[company_code]['metadata'].keys():
#                 variables.metadata[company_code]['metadata']['tags'] = []
#             comp_tags = variables.metadata[company_code]['metadata']['tags']
#             # st.info(f"for {company_code} : Comp tags are {comp_tags")
#             if len(comp_tags) >= 1:                            
#                 for each in comp_tags:
#                     if each.endswith('2024') or each.endswith('2025') or each.endswith('DEMAND')  or each.startswith('BestQ') :
#                         if each not in company_in.keys():
#                             company_in[each] = []
#                         company_in[each].append(company_code)
#                 # for each in comp_tags:
#                 #     if each.endswith('2024') or each.endswith('2025') or each.endswith('DEMAND') or each.startswith('BestQ') :
#                 #         company_in[each].append(company_code)            
#     except Exception as KeyError:
#         pass

# company_in_keys = list(company_in.keys())
# company_in_values = list(company_in.values())
# #get a list of company_in.keys() with its len(company_in[each_key]) after it
# temp_list_company_in = list(company_in.keys())  
# temp_list_len = [f"{each_key} ({len(company_in[each_key])})" for each_key in temp_list_company_in]   #to give name with number in the SelectBox

# first_selected = st.sidebar.selectbox("ChoseW", list(temp_list_len), index=0)
# selected_first_as = company_in[first_selected.split(" (")[0]]           # removin the last number_part in the watchlist_name
# selected_first_as = nse_bse_search.remove_duplicate_in_watchlist(selected_first_as)
# selected = st.sidebar.selectbox("", selected_first_as,
#                 index=selected_first_as.index(selected_stock) if selected_stock in selected_first_as else 0)

# if st.button(f"Make Txt file from {first_selected.split(' (')[0]}"):
#     with open(f'./watchlist/watchlist {first_selected.split(" (")[0]}.txt', 'w') as wr:
#         for each in selected_first_as:
#             wr.write(each+"\n")
