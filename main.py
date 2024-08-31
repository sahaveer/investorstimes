import time
import glob
import random
import os
import datetime
import time
import pandas as pd
import pickle

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
st.set_page_config(page_title="iTimesAlgo", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="expanded",)

import nse_bse_search
import create_database
import fundamentals
# import processdriver
# import screenerpage
import variables

if 'nsecode_list' not in st.session_state or 'nseISIN_list' not in st.session_state:
        nse_data = pd.read_csv('./cm21JUN2024bhav.csv')
        nse_data.columns = nse_data.columns.str.replace(' ', '_')
        st.session_state.nseISIN_list = nse_data["ISIN"].tolist()
        st.session_state.nsecode_list = nse_data["SYMBOL"].tolist()

# import amibroker

# Function to load the dictionary from a file
def load_metadata():
    if os.path.exists('./metadata.pkl'):
        with open('./metadata.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return {}
variables.metadata = load_metadata()

def save_metadata():
    with open('./metadata.pkl', 'wb') as f:
        pickle.dump(variables.metadata, f)
    with open('./userdata.pkl','wb') as f:
        pickle.dump(st.session_state.user_data, f)
    st.success("Metadata saved successfully")

# for each in variables.metadata.keys():
#     try:
#         variables.metadata[each]['Code'] = each             # to make sure the Company code is available within the dict
#         # variables.metadata[each]['updated_results_on'] = datetime.datetime.now()-datetime.timedelta(days=3)
#         create_database.insert_stock_metadata(variables.metadata[each])
#         st.success(f"Saved {each} in Database")
#         # st.info('LETS try reading from the database')
#         # comp_metadata = "DIDNT FIND ANYTHING FROM DATABASE"
#         # comp_metadata = create_database.company_metadata_col.find_one({"Code": each})
#         # st.info(comp_metadata)
#     except Exception as DuplicateKeyError:
#         st.error(f"Duplicate key error occurred for {each}.")
#save_metadata()

total_keys = len(variables.metadata.keys())
st.sidebar.info(f"Total {total_keys} stocks in metadata")

if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
    # st.session_state.user_data['favourite_list'] = []
    # st.session_state.user_data['holdings_list'] = []
    # st.session_state.user_data['watch_list'] = []

# ONLY TO MAKE SURE NOT TO OVERWRITE THE GROUPS FOLDERS
fromwhere = './watchlist/groups/**/'
typeoffile = '*.txt'
files = glob.iglob(r''+fromwhere + typeoffile, recursive=True)  # making recursive True gives sub directories as well
for file in files:
    chang = str(file)
    txt_files_dir = chang.replace("\\","/")
    txt_file_name_only = os.path.basename(txt_files_dir)
    variables.user_data[txt_file_name_only.split('.')[0]] = []
    with open(f"{txt_files_dir}",'r') as file:
        for each_line in file:
            # print(each_line)
            variables.user_data[txt_file_name_only.split('.')[0]].append(each_line.strip())

# st.info(variables.user_data)

# global bsecodenum_codename
# global bsecodename_codenum
if 'bsecodenum_codename' not in st.session_state and 'bsecodename_codenum' not in st.session_state:
    st.session_state.bsecodenum_codename,st.session_state.bsecodename_codenum,bsecodenum_fullname,bsecodename_fullname,bsefullname_codenum,bsefullname_codename = nse_bse_search.bsecodenum_bsecodename()
    # This gets us the BSE NAME from the DAILY BHAVCOPY THAT WE ARE DOWNLOADING
    st.session_state.bsesccode_scname,st.session_state.bsescname_sccode = nse_bse_search.bseSCNAME_SCCODE()




# if 'nsecode_list' not in st.session_state:
#     st.session_state.nsecode_list = nse_bse_search.nse_code
if 'no_of_stocks_not_latest' not in st.session_state:
    st.session_state.no_of_stocks_not_latest = {}

# PARAMS
funda_keys = ['PROFIT&LOSS', 'BALANCE SHEET',
              'CASH FLOW']  # dont change the order of this list as it will affect the keys used in Yearly df
# **************************************************************************************************
listed_stocks = []
latest_quarterly_stocks = []
no_latest_quarterly_stocks = []

stocks_dict = {}
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

@st.cache_data
def unique_from_watchlist(path):
    if os.path.exists(path):
        get_list = []
        # Open the file in read mode
        with open(path, 'r') as file:                                                                       # Read each line and append it to the list
            for line in file:
                get_list.append(line.strip())
        unique_list = nse_bse_search.remove_duplicate_in_watchlist(get_list)
    return unique_list


timedelta_Q_days = pd.Timedelta(days=120)
#@st.cache_data
def get_all_quarterly_list():
    last_announced_quarter1 = ""
    #lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
    for each_pickl in glob.glob('./pickl/**/*.pkl', recursive=True):
        each_pickl = each_pickl.replace('\\', '/')
        #st.info(each_pickl)
        file_name_only = os.path.basename(each_pickl)
        #file_name_only = each_pickl.split('/')[-1]
        tree_folder1 = file_name_only[0].upper()
        if file_name_only.endswith('Yearly.pkl'):
            pickle_name = file_name_only.split()[0].strip()  # Since all the pickle files are either Quartetrly or Yearly, we need to get the first company code only
        elif file_name_only.endswith('Quarterly.pkl'):
            pickle_name = file_name_only.split()[0].strip()
            qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder1}/{file_name_only}')
            qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
            if (datetime.datetime.now() - qtr_pnl.columns[-1]) < timedelta_Q_days and pickle_name not in latest_quarterly_stocks:
                latest_quarterly_stocks.append(pickle_name.split()[0])
                last_announced_quarter1 = datetime.datetime.strftime(qtr_pnl.columns[-1],'%b%Y')

                                                                                                                        # BEEN TAKING SCRIPTS FROM LISTED SCRIPTS
        # if pickle_name.split()[0] not in send_listed_stocks:
        #     send_listed_stocks.append(pickle_name)

        # unique_latest_quarterly_stocks = nse_bse_search.remove_duplicate_in_watchlist(latest_quarterly_stocks)


    #return unique_listed_stocks, unique_latest_quarterly_stocks, last_announced_quarter1
    return latest_quarterly_stocks, last_announced_quarter1


if 'latest_quarterly_stocks' not in st.session_state or 'last_announced_quarter' not in st.session_state:
    st.session_state.latest_quarterly_stocks,st.session_state.last_announced_quarter = get_all_quarterly_list()


if 'listed_stocks' not in st.session_state:
    send_listed_stocks = []
    with open(f'./watchlist/alllisted.txt','r') as f:
        for each in f:
            send_listed_stocks.append(each)
    unique_listed_stocks = nse_bse_search.remove_duplicate_in_watchlist(send_listed_stocks)
    st.session_state['listed_stocks'] = unique_listed_stocks
    with open('./watchlist/alllisted.txt', 'w') as file:  # Read each line and append it to the list
        for line in unique_listed_stocks:
            file.write(line + "\n")

col1_header, col2_header = st.columns([2,1])
with col1_header:
    st.title(f"👇 Chose among {str(len(st.session_state.listed_stocks))} listed stocks")
    st.subheader(f"{str(len(st.session_state.latest_quarterly_stocks))} stocks announced {st.session_state.last_announced_quarter} Quarterly Results;")
    #selected = st.selectbox("Chose Company", st.session_state.listed_stocks)

#REGARDING USER DATA 

def liked_stocks(script_code):
    if "liked" in st.session_state.user_data:
        st.session_state.user_data['liked'].append(script_code)
    else:
        st.session_state.user_data['liked'] = []
        st.session_state.user_data['liked'].append(script_code)

def disliked_stocks(script_code):
    if "disliked" in st.session_state.user_data:
        st.session_state.user_data['disliked'].append(script_code)
    else:
        st.session_state.user_data['disliked'] = []
        st.session_state.user_data['disliked'].append(script_code)

holdings_list = []
watch_list = []


@st.cache_data
def holdings_func():
    if os.path.exists('./watchlist/holdings.txt'):
        holdings_list = []
        # Open the file in read mode
        with open('./watchlist/holdings.txt', 'r') as file:                                                                       # Read each line and append it to the list
            for line in file:
                holdings_list.append(line.strip())
        unique_holdings_list = nse_bse_search.remove_duplicate_in_watchlist(holdings_list)
        # st.info(f"{len(holdings_list)} is reduced to {len(unique_holdings_list)}")
        with open('./watchlist/holdings.txt', 'w') as file:  # Read each line and append it to the list
            for line in unique_holdings_list:
                file.write(line + "\n")
    return unique_holdings_list

@st.cache_data
def watchlist_func():
    if os.path.exists('./watchlist/watchlist.txt'):
        watch_list = []
        with open('./watchlist/watchlist.txt', 'r') as file:  # Read each line and append it to the list
            for line in file:
                watch_list.append(line.strip())
        unique_watchlist = nse_bse_search.remove_duplicate_in_watchlist(watch_list)
        # st.info(f"{len(watch_list)} is reduced to {len(unique_watchlist)}")
        with open('./watchlist/watchlist.txt', 'w') as file:  # Read each line and append it to the list
            for line in unique_watchlist:
                file.write(line + "\n")
    return unique_watchlist

@st.cache_data
def favourite_func():
    if os.path.exists('./watchlist/favourite.txt'):
        added_watch_list = []
        with open('./watchlist/favourite.txt', 'r') as file:  # Read each line and append it to the list
            for line in file:
                added_watch_list.append(line.strip())
        unique_added_watch_list = nse_bse_search.remove_duplicate_in_watchlist(added_watch_list)
    return unique_added_watch_list

@st.cache_data
def lets_scan_list(query_list):
    no_latest_quarterly_stocks=[]
    for selected in query_list:
        if selected != "":
            query = selected.strip()
            if query.isdigit():
                company_code = int(query)
                if company_code in st.session_state.bsecodenum_codename.keys():
                    comp_Name = st.session_state.bsecodenum_codename[company_code]
                else:
                    comp_Name = None
            else:
                company_code = str(query)
                comp_Name = query

            if comp_Name is not None:
                timedelta_Q1_days = pd.Timedelta(days=180)
                folder_tree = comp_Name[0].upper()
                if os.path.exists(f'./pickl/{folder_tree}/{comp_Name} Quarterly.pkl'):
                    qtr_pnl = pd.read_pickle(f'./pickl/{folder_tree}/{comp_Name} Quarterly.pkl')
                    timedelta_Q1_days = pd.Timedelta(days=180)
                    if (datetime.datetime.now() - qtr_pnl.columns[-1]) > timedelta_Q1_days and selected not in no_latest_quarterly_stocks:
                        no_latest_quarterly_stocks.append(selected)
                else:
                    no_latest_quarterly_stocks.append(selected)
    return no_latest_quarterly_stocks

def get_code(query):
    if 'bsenames_list' not in st.session_state or 'bsecodes_list' not in st.session_state:  # if 'bse_ISIN' not in st.session_state or 'bse_ycode' not in st.session_state
        bse_data = pd.read_csv('./Select.csv', header=0, index_col=False)
        bse_data.columns = bse_data.columns.str.replace(' ', '_')
        st.session_state.bse_ISIN = bse_data["ISIN_No"].tolist()
        st.session_state.bse_ycode = bse_data["Security_Id"].tolist()
        st.session_state.bsenames_list = bse_data["Security_Name"].tolist()
        st.session_state.bsecodes_list = bse_data["Security_Code"].tolist()

    if 'nsecode_list' not in st.session_state or 'nseISIN_list' not in st.session_state:
        nse_data = pd.read_csv('./cm21JUN2024bhav.csv')
        nse_data.columns = nse_data.columns.str.replace(' ', '_')
        st.session_state.nseISIN_list = nse_data["ISIN"].tolist()
        st.session_state.nsecode_list = nse_data["SYMBOL"].tolist()

    query = query.strip()
    # TEMPORARY CONVERTING THIS TO CODE NUMBER
    company_code = None
    code_name = None
    if query.isdigit():
        company_code = (query)
        if int(company_code) in st.session_state.bsecodenum_codename.keys():
            code_name = st.session_state.bsecodenum_codename[int(company_code)]
        else:
            code_name = None
    else:
        if query in st.session_state.nsecode_list:
            company_code = query
            code_name = query
        else:
            if query in st.session_state.bsecodename_codenum.keys():
                company_code = str(st.session_state.bsecodename_codenum[query])
                code_name = query
    #st.info(company_code)
    return company_code, code_name

                                                                                                                        # Function to save the dictionary to a file

with col2_header:
    if st.button("SAVE METADATA"):
        save_metadata()

# IF RECENT_QUARTER IS NOT NEW IN METADATA
# DWONLOADS FROM SCREENER, ANALYSES TO GET THE METADATA
# IF ANY TAGS, THEN WRITES IN RESPECTIVE TEXT FILES
# WRITES A SENTENCE AND SAVES IN AMIBROKER NOTES FORMAT
# PICKLES DATA ALSO


# def get_latest_results(selected_list:list):
#     driver = processdriver.getedgedriver()
#     i=0
#     for selected in selected_list:
#         # st.info(selected)
#         company_code, code_name = get_code(selected)
#         #st.info(company_code)
#         #st.info(code_name)
#         if company_code is not None and code_name is not None:
#             code_names = nse_bse_search.process_code(company_code, code_name)
#             # st.info(company_code)
#             # st.info(code_names[0])
#             # try:
#             # if company_code in variables.metadata.keys():
#             #     if 'recent_quarter' in variables.metadata[company_code].keys():
#             #         the_quarter_is = variables.metadata[company_code]['recent_quarter']
#             #         if (datetime.datetime.now() - the_quarter_is) < timedelta_Q_days:
#             #             metadata = variables.metadata[company_code]

#             # else:
#             if code_names[0] in variables.metadata.keys() and 'recent_quarter' in variables.metadata[code_names[0]].keys() and 'updated_results_on' in variables.metadata[code_names[0]].keys() and (datetime.datetime.now() - variables.metadata[code_names[0]]['recent_quarter']) < timedelta_Q_days and (datetime.datetime.now() - variables.metadata[code_names[0]]['updated_results_on']) < datetime.timedelta(days=3):
#                 #check the recent quarter is not very old
#                 #check if reported date is very recent like just 3 days back
#                 reported_date_is = variables.metadata[code_names[0]]['updated_results_on']
#                 # check the difference is not less than 3 days
#                 st.info(f"The company {code_names[0]} has recent quarter {variables.metadata[code_names[0]]['recent_quarter']} reported recently, thus skipping SCREENER")
#                 metadata = variables.metadata[code_names[0]]
#                 metadata['Code'] = code_names[0]
#                 create_database.insert_stock_metadata(metadata)
#                 st.success(f"Saved Metadata in Database as well")                
#                 # metadata = variables.metadata[code_names[0]]                    
#                 # st.info(f"Metadata is {metadata}")
#             else:
#                 yr_df, qtr_df, code_name_pickle = screenerpage.search_screener(driver,company_code)                     # lets get code_name from site itself to make it convenient and updated
#                 metadata = {}
#                 if yr_df is not None and qtr_df is not None and code_name_pickle is not None:
#                     pnl, balancesht = fundamentals.develop_yearly(yr_df)
#                     qtr_pnl = fundamentals.develop_quarterly(qtr_df)
#                     metadata = fundamentals.analyse_df(pnl, balancesht, qtr_pnl)
#                     metadata['code_names'] = code_names
#                     metadata['Code'] = code_names[0]
#                     variables.metadata[company_code] = metadata
#                     # st.success(variables.metadata[company_code]['recent_quarter'])
#                                                                                                                         #writing tags to its respective text files
#                     if len(metadata['tags'])>=1:
#                         for each in metadata['tags']:
#                             text_file = f'./watchlist/groups/{each}.txt'
#                             if each not in variables.user_data.keys():
#                                 variables.user_data[each] = []
#                             if metadata['code_names'][0] not in variables.user_data[each]:
#                                 with open(text_file,'a+') as file:
#                                     file.write(f"{metadata['code_names'][0]}\n")
#                                     st.success(f"Updated {metadata['code_names'][0]} in {text_file}")
#                             # this_text_list = []
#                             # with open(text_file,'a+') as file:
#                             #     for each in file:
#                             #         this_text_list.append(each)
#                             #     if metadata['code_names'][0] not in this_text_list:
#                             #        file.write(f"{metadata['code_names'][0]}\n")
#                             #        st.success(f"Updated {metadata['code_names'][0]} in {text_file}")

#                     # st.info(metadata)
#                     # st.info(company_code)
#                     # st.info(variables.metadata[company_code])

#                                                                                                                             # LETS CREATE SENTENCE (INSIGHT) from METADATA
#                     sentence = ""
#                     if len(metadata['code_names']) == 1 and metadata['code_names'][0].isdigit():
#                         sentence += f"CODE\tNAME"
#                         sentence += f"{metadata['code_names'][0]} {st.session_state.bsecodenum_codename[int(metadata['code_names'][0])]}"
#                     else:
#                         sentence += f"CODES\n"
#                         for each in metadata['code_names']: sentence += f"{each}\t"

#                     # for each in metadata['code_names']: sentence += f"{each}\t"
#                     sentence += "\n***CONS***\n"
#                     for each in metadata['cons']: sentence += f"{each}\n"
#                     sentence += "\n***YEARLY***" + metadata['YPNL_Statement']
#                     sentence += "\n***QUARTERLY***" + metadata['QPNL_Statement']
#                     sentence += "\n***PROS***\n"
#                     for each in metadata['pros']: sentence += f"{each}\n"
#                     if 'QPNL_tweet' in metadata.keys() and 'YPNL_tweet' in metadata.keys():
#                         sentence += f"\n{metadata['QPNL_tweet']}\n{metadata['YPNL_tweet']}"
#                     # st.info(sentence)
#                     # amibroker.amibroker_notes_insights(code_names, sentence)
#                     create_database.insert_stock_metadata(metadata)
#                     st.success("Saved Metadata in Database as well")
#                     save_metadata()
#                     # if i==50:
#                     #     save_metadata()
#                     #     i=0
#                     time.sleep(random.uniform(1, 3))
#                     #time.sleep(2)
#                                                                                                                             # SAVING TO PICKLE FILE
#                     if code_name_pickle is not None:
#                         # st.info(f"For pickling Yearly we received {code_names}")
#                         # lets process first yearly dataframe
#                         if not yr_df.empty and yr_df is not None and isinstance(yr_df, pd.DataFrame):
#                             yr_df.columns = pd.to_datetime(yr_df.columns, format='%d-%m-%Y')
#                             # st.dataframe(yr_df)
#                             for code_name1 in code_names:
#                                 # st.info(f"{i+1}    {code_name1}")
#                                 if code_name1.isnumeric():
#                                     folder_treeY1 = str(code_name1[0])
#                                     folder_locationY1 = "./pickl/" + folder_treeY1 + "/"
#                                     if not os.path.exists(folder_locationY1):
#                                         os.makedirs(folder_locationY1)

#                                     save_pickl_asY1 = folder_locationY1 + str(code_name1) + " Yearly.pkl"
#                                     yr_df.to_pickle(save_pickl_asY1)
#                                     st.success(f"LATEST : Yearly DataFrame saved in {save_pickl_asY1}")
#                                     pass
#                                 else:
#                                     folder_treeY2 = code_name1[0].upper()
#                                     folder_locationY2 = "./pickl/" + folder_treeY2 + "/"
#                                     if not os.path.exists(folder_locationY2):
#                                         os.makedirs(folder_locationY2)
#                                     save_pickl_asY2 = folder_locationY2 + code_name1 + " Yearly.pkl"
#                                     yr_df.to_pickle(save_pickl_asY2)
#                                     st.success(f"LATEST : Yearly DataFrame saved in {save_pickl_asY2}")

#                             # amibroker.amibroker_notes_csv_yearly(code_names, yr_df)

#                         # st.info(f"For pickling Quarterly we received {code_names}")

#                         # lets process Quarterly Dataframe
#                         # lets process first Quarterly dataframe
#                         if not qtr_df.empty and isinstance(qtr_df, pd.DataFrame) and qtr_df is not None:
#                             qtr_df.columns = pd.to_datetime(qtr_df.columns, format='%d-%m-%Y')
#                             for code_name2 in code_names:
#                                 # st.info(code_name2)
#                                 if code_name2.isnumeric():
#                                     folder_treeQ2 = str(code_name2[0])
#                                     folder_locationQ2 = "./pickl/" + folder_treeQ2 + "/"
#                                     save_pickl_asQ2 = folder_locationQ2 + str(code_name2) + " Quarterly.pkl"
#                                     qtr_df.to_pickle(save_pickl_asQ2)
#                                     st.success(f"LATEST : Quarterly DataFrame saved in {save_pickl_asQ2}")

#                                 else:
#                                     folder_treeQ1 = code_name2[0].upper()
#                                     folder_locationQ1 = "./pickl/" + folder_treeQ1 + "/"
#                                     if not os.path.exists(folder_locationQ1):
#                                         os.makedirs(folder_locationQ1)
#                                     save_pickl_asQ1 = folder_locationQ1 + code_name2 + " Quarterly.pkl"
#                                     qtr_df.to_pickle(save_pickl_asQ1)
#                                     st.success(f"LATEST : Quarterly DataFrame saved in {save_pickl_asQ1}")

#                                     # amibroker.amibroker_notes_csv_quarterly(code_names, qtr_df)

#                                     # st.info(f"saved pickl file {code_name} in working directory pickle folder ")

#                                     # always need a CODE but in STRING format
#                                     # SCANS THE WATCLIST TO GET US THOSE SCRIPTS IN THE WATCHLIST WITHOUT LATEST QRESULTS
#         i+=1
#     save_metadata()


if 'holdings_list' not in st.session_state.user_data:
    st.session_state.user_data['holdings_list'] = holdings_func()
if 'watch_list' not in st.session_state.user_data:
    st.session_state.user_data['watch_list'] = watchlist_func()
if 'favourite_list' not in st.session_state.user_data:
    st.session_state.user_data['favourite_list'] = favourite_func()

holdings_list = st.session_state.user_data['holdings_list']
watch_list = st.session_state.user_data['watch_list']
favourite_list = st.session_state.user_data['favourite_list']

# Parse the URL parameters to get the selected stock
url = st.experimental_get_query_params()
selected_stock = url.get("selected", [""])[0]

# WATCHLIST OPTIONS
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
# with col3:
#     #genre = st.checkbox(label='Only latest Quarter',value=True)
#     genre = st.radio("Chose Genre :",["Holdings",":rainbow[Latest Quarterly]", "Watchlist","All Listed","Favourite"],)
genre = "All Listed"

                                                                                                                        # SELECTION OF WATCHLIST
with col1:
    if genre == ":rainbow[Latest Quarterly]":
        funda_tech_options = ["Funda_Chart", 'Tech_Chart', 'Analyse Watchlist']
        show_list_as = st.session_state.latest_quarterly_stocks if selected_stock in st.session_state.latest_quarterly_stocks else st.session_state.listed_stocks
        # selected = st.sidebar.selectbox("Pick",show_list_as,
        #                                 index=st.session_state.latest_quarterly_stocks.index(selected_stock) if selected_stock in st.session_state.latest_quarterly_stocks else st.session_state.listed_stocks.index(selected_stock) if selected_stock in st.session_state.listed_stocks else 0)
        if 'Latest Quarterly' not in st.session_state.no_of_stocks_not_latest:
            st.session_state.no_of_stocks_not_latest['Latest Quarterly'] = lets_scan_list(show_list_as)

        # with col2_header:
        #     if st.button(f'LATEST RESULTS from entire Watchlist'):
        #         get_latest_results(show_list_as)

        temp_var = st.session_state.no_of_stocks_not_latest['Latest Quarterly']
        if len(temp_var) > 0:
            # with col2_header:
            #     if st.button(f'Get Results of {len(temp_var)} scripts with NO_LATEST_RESULTS'):
            #         get_latest_results(temp_var)
            no_of_stocks_not_latest1 = []
            for each in temp_var:
                if each.isdigit():
                    no_of_stocks_not_latest1.append(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
                else:
                    no_of_stocks_not_latest1.append(each)
            with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
                st.info(no_of_stocks_not_latest1)
    elif genre =="All Listed" :
        funda_tech_options = ["Funda_Chart", 'Tech_Chart', 'Analyse Watchlist']
        show_list_as = st.session_state.listed_stocks
        # selected = st.sidebar.selectbox("", st.session_state.listed_stocks,
        #                                 index=st.session_state.listed_stocks.index(selected_stock) if selected_stock in st.session_state.listed_stocks else 0)
        if 'All Listed' not in st.session_state.no_of_stocks_not_latest:
                st.session_state.no_of_stocks_not_latest["All Listed"] = lets_scan_list(st.session_state.listed_stocks)
        temp_var = st.session_state.no_of_stocks_not_latest["All Listed"]
        # with col2_header:
        #     if st.button(f'Get Latest Results for ALL'):
        #         get_latest_results(show_list_as)

        if len(temp_var) > 0:
            # with col2_header:
            #     if st.button(f'{len(temp_var)} needs Latest Results'):
            #         get_latest_results(temp_var)
            no_of_stocks_not_latest1 = []
            for each in temp_var:
                if each.isdigit():
                    no_of_stocks_not_latest1.append(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
                else:
                    no_of_stocks_not_latest1.append(each)
            with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
                st.info(no_of_stocks_not_latest1)
        # else:
        #     st.button("LOVELY! Watchlist is Updated")
    elif genre == "Holdings":
        funda_tech_options = ["Funda_Chart", 'Tech_Chart', 'Analyse Watchlist']
        update_txt_file = './watchlist/holdings.txt'
        # show_list_as = unique_from_watchlist(update_txt_file)
        show_list_as = st.session_state.user_data['holdings_list']
        # selected = st.sidebar.selectbox("", show_list_as,
        #                 index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
        if 'Holdings' not in st.session_state.no_of_stocks_not_latest:
            st.session_state.no_of_stocks_not_latest['Holdings'] = lets_scan_list(holdings_list)
        temp_var = st.session_state.no_of_stocks_not_latest['Holdings']
        # with col2_header:
        #     if st.button(f'Get Latest Results'):
        #         get_latest_results(show_list_as)
                # DISPLAY IN WEBAPP ABT STOCKS WITHOUT LATEST QRESULTS
        if len(temp_var) > 0:
            # with col2_header:
            #     if st.button(f'{len(temp_var)} needs Latest Results'):
            #         get_latest_results(temp_var)
            no_of_stocks_not_latest1 = []
            for each in temp_var:
                if each.isdigit():
                    no_of_stocks_not_latest1.append(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
                else:
                    no_of_stocks_not_latest1.append(each)
            with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
                st.info(no_of_stocks_not_latest1)
    elif genre == "Watchlist":
        funda_tech_options = ["Funda_Chart", 'Tech_Chart', 'Analyse Watchlist']
        update_txt_file = './watchlist/watchlist.txt'
        # show_list_as = unique_from_watchlist(update_txt_file)
        show_list_as = st.session_state.user_data['watch_list']
        # selected = st.sidebar.selectbox("", show_list_as,
        #                 index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
        if 'Watchlist' not in st.session_state.no_of_stocks_not_latest:
            st.session_state.no_of_stocks_not_latest['Watchlist'] = lets_scan_list(watch_list)
        temp_var = st.session_state.no_of_stocks_not_latest['Watchlist']
        # st.info(f"Out of {len(watch_list)} stocks, {len(temp_var)} have NO-LATEST results")

        with col2_header:
            if st.button(f'Get Latest Results'):
                get_latest_results(show_list_as)
        if len(temp_var) > 0:
            # with col2_header:
            #     if st.button(f'{len(temp_var)} needs Latest Results'):
            #         get_latest_results(temp_var)
            no_of_stocks_not_latest1 = []
            for each in temp_var:
                if each.isdigit():
                    no_of_stocks_not_latest1.append(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
                else:
                    no_of_stocks_not_latest1.append(each)
            with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
                st.info(no_of_stocks_not_latest1)
    elif genre == "Favourite":
        funda_tech_options = ["Funda_Chart", 'Tech_Chart', 'Analyse Watchlist']
        update_txt_file = './watchlist/favourite.txt'
        show_list_as = st.session_state.user_data['favourite_list']
        # selected = st.sidebar.selectbox("", show_list_as,
        #                 index=show_list_as.index(selected_stock) if selected_stock in show_list_as else 0)
        if 'Favourites' not in st.session_state.no_of_stocks_not_latest:
            st.session_state.no_of_stocks_not_latest["Favourites"] = lets_scan_list(show_list_as)
        temp_var = st.session_state.no_of_stocks_not_latest["Favourites"]
        # with col2_header:
        #     if st.button(f'Get Latest Results'):
        #         get_latest_results(show_list_as)

        if len(temp_var) > 0:
            # with col2_header:
            #     if st.button(f'{len(temp_var)} needs Latest Results'):
            #         get_latest_results(temp_var)
            # ONLY TO SHOW BOTH CODE AND NAME TOGETHER IN EXPANDER
            no_of_stocks_not_latest1 = []
            for each in temp_var:
                if each.isdigit():
                    no_of_stocks_not_latest1.append(f"{each} : {st.session_state.bsecodenum_codename[int(each)]}")
                else:
                    no_of_stocks_not_latest1.append(each)
            with st.expander(label=f"{str(len(temp_var))} Stocks in this watchlist have NO latest Quarterly Results"):
                st.info(no_of_stocks_not_latest1)
                                                                                                                        # GET LIST OF STOCKS IN WATCHLIST and MAKE WATCHLISTS AS PER TAGS
company_in = {}
company_in['ALL'] = show_list_as
for company_code in show_list_as:
    if company_code in variables.metadata.keys():
        comp_tags = variables.metadata[company_code]['tags']
        # st.info(f"for {company_code} : Comp tags are {comp_tags")
        if len(comp_tags) >= 1:                
            for each in comp_tags:
                if each.endswith('2024') or each.endswith('DEMAND'):
                    if each not in company_in.keys():
                        company_in[each] = []
            for each in comp_tags:
                if each.endswith('2024') or each.endswith('DEMAND'):
                    company_in[each].append(company_code)
company_in_keys = list(company_in.keys())
company_in_values = list(company_in.values())

#get a list of company_in.keys() with its len(company_in[each_key]) after it
temp_list_company_in = list(company_in.keys())  
temp_list_len = [f"{each_key} ({len(company_in[each_key])})" for each_key in temp_list_company_in]

multi_option_list = []
# first_selected = st.sidebar.selectbox("ChoseW", list(company_in.keys()), index=0)
# selected_first_as = company_in[first_selected]
first_selected = st.sidebar.selectbox("ChoseW", list(temp_list_len), index=0)
selected_first_as = company_in[first_selected.split(" (")[0]]



selected = st.sidebar.selectbox("", selected_first_as,
                index=selected_first_as.index(selected_stock) if selected_stock in selected_first_as else 0)
if st.button(f"Create Text file from {first_selected.split(' (')[0]}"):
    save_txt_file_as = f"watchlist {first_selected.split(" (")[0]}.txt"
    with open(f'./watchlist/tempwatchlist.txt', 'w') as wr:
        for each in selected_first_as:
            wr.write(each+"\n")
    with open(f'./watchlist/tempwatchlist.txt', 'w') as file:
        content = file.read()
        btn = st.download_button(
            label="Download Now",
            data=content,
            file_name=save_txt_file_as,
            mime="application/text")

st.experimental_set_query_params(selected=[selected],)
if selected:
    funda_tech = option_menu("", funda_tech_options,
                             icons=['house', '📈 '], menu_icon="cast", default_index=0, orientation="horizontal")
    metadata = {}
                                                                                                                        # lets get CODE, CODENAMES from LOCAL FILE
    company_code, comp_Name = get_code(selected)
    # st.info(f"COMP CODE from get_code FUCNTION")
                                                                                                                        #SHOWUP SCREENER SITE
    if selected in st.session_state.nsecode_list:
        #company_code = selected
        #comp_Name = selected
        nse_screener_address = "https://www.screener.in/company/" + str(company_code)
        with st.sidebar:
            st.markdown(f"[***NSE SCREENER***]({nse_screener_address})", unsafe_allow_html=True)
    if selected in st.session_state.bsecodename_codenum.keys():
        #company_code = str(st.session_state.bsecodename_codenum[selected])
        #comp_Name = selected
        bse_screener_address = "https://www.screener.in/company/" + str(company_code)
        with st.sidebar:
            st.markdown(f"[***BSE SCREENER***]({bse_screener_address})", unsafe_allow_html=True)
    if selected.isdigit():
        if int(selected) in st.session_state.bsecodenum_codename.keys():
            #company_code = selected
            #comp_Name = st.session_state.bsecodenum_codename[int(selected)]
            bse_screener_address = "https://www.screener.in/company/" + str(selected)
            with st.sidebar:
                st.markdown(f"[***BSE SCREENER***]({bse_screener_address})", unsafe_allow_html=True)
                                                                                                                        # TRADING VIEW DATA
                                                                                                                        # ADD TO FAVOURITE TXT FILE
                                                                                                                        # GIVE A FAVOURITE BUTTON
    # with col4:
    #     if st.button("+FAVOURITE"):
    #         with open('./watchlist/favourite.txt', 'w') as file:
    #             file.write(selected)

    coltw1, coltw2 = st.columns([2, 2])
                                                                                                                        # TICKER INFO FROM TRADING VIEW SITE
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
        components.html(ticker_symbol_info.replace("xyx", comp_Name), height=200)
                                                                                                                            # FUNDA CHART TAB
    if funda_tech == "Funda_Chart":
        with st.sidebar:
            #color_key = st.selectbox("Bar Color", color_dict.keys())
            color_key = 'blue3'
        # tree_folder = comp_Name[0].upper()
        if company_code[0].isdigit():
            tree_folder = company_code[0]
        else:
            tree_folder = company_code[0].upper()

        # st.info(f"In FUNDACHART comp_Name : {comp_Name}")
                                                                                                                        # if Quarterly data not available but YEARLY DATA AVAILABLE
        if not os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and \
                os.path.exists(f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):
            st.info("ONLY YEARLY DATA AVAILABLE FOR THIS SCRIPT")
            df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
            # st.info(f"Reading ./pickl/{tree_folder}/{comp_Name} Yearly.pkl")
            try:
                df_comp.columns = pd.to_datetime(df_comp,'%d-%m-%Y')
            except Exception as AttributeError:
                pass
            # st.dataframe(df_comp)
            pnl, balancesht = fundamentals.develop_yearly(df_comp)
            with st.sidebar:  # with col2:
                sub_choose = st.selectbox("Fundamentals:", fundamentals.funda_keys)
                st.title(comp_Name)
            
            # st.error("Yearly DATA not in order")

        elif os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):
            df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
            # st.info(f"PKL FILE EXISTS, thus Reading './pickl/{tree_folder}/{comp_Name} Yearly.pkl'   ")
            #st.dataframe(df_comp)
            try:
                df_comp.columns = pd.to_datetime(df_comp,'%d-%m-%Y')
                #df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
            except Exception as AttributeError:
                pass
            pnl, balancesht = fundamentals.develop_yearly(df_comp)

            qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl')
            # pnl, balancesht, qtr_pnl = fundamentals.develop_data(qtr_pnl, df_comp)
            try:
                qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
                # qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
            except Exception as AttributeError:
                pass

            qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)
            if company_code in variables.metadata.keys():
                # st.info(f"METADATA already Avaialble ")
                metadata = variables.metadata[company_code]
            else:
                st.info(f"METADATA NOT Avaialble ")
                metadata = fundamentals.analyse_df(pnl,balancesht,qtr_pnl)
                metadata['code_names'] = nse_bse_search.process_code(company_code, comp_Name)
                variables.metadata[company_code] = metadata

            if len(metadata['tags']) >= 1:
                for each in metadata['tags']:
                    text_file = f'./watchlist/groups/{each}.txt'
                    if each not in variables.user_data.keys():
                        variables.user_data[each] = []
                    if metadata['code_names'][0] not in variables.user_data[each]:
                        with open(text_file, 'a+') as file:
                            file.write(f"{metadata['code_names'][0]}\n")
                            st.success(f"Updated {metadata['code_names'][0]} in {text_file}")
                    # this_text_list = []
                    # with open(text_file, 'a+') as file:
                    #     for each in file:
                    #         this_text_list.append(each)
                    #     st.info(this_text_list)
                    #     if metadata['code_names'][0] not in this_text_list:
                    #         file.write(f"{metadata['code_names'][0]}\n")
                    #         st.success(f"Updated {metadata['code_names'][0]} in {text_file}")
            with st.expander(label=f"Metadata of {company_code}"):
                for each in metadata.keys():
                    st.info(f"{each} : {metadata[each]}")
            proscons_col1, proscons_col2 = st.columns([1,1])
            with proscons_col1:
                st.title("PROS")
                for each in metadata['pros']:
                    st.success(each)
            with proscons_col2:
                st.title("CONS")
                for each in metadata['cons']:
                    st.error(each)
            options = st.multiselect(
                "TAGS",
                ["Favourite"]+metadata['tags'],
                metadata['tags'])
            with st.sidebar:  # with col2:
                sub_choose = st.selectbox("Fundamentals:", fundamentals.funda_menu)
                st.title(comp_Name)

            # sentence = f"{comp_Name}: "
            # sentence += fundamentals.stmt_for_qoq(pnl)
            # st.info(metadata)
            sentence = ""
            if len(metadata['code_names']) == 1 and metadata['code_names'][0].isdigit():
                sentence += f"CODE\tNAME\n"
                sentence += f"BSECODE {metadata['code_names'][0]}\t{st.session_state.bsecodenum_codename[int(metadata['code_names'][0])]}"
            else:
                sentence += f"CODES:"
                for each in metadata['code_names']: sentence += f"{each}\t"
            sentence += "\n***CONS***\n"
            for each in metadata['cons']: sentence += f"{each}\n"
            sentence += "\n***YEARLY***" + metadata['YPNL_Statement']
            sentence += "\n***QUARTERLY***" + metadata['QPNL_Statement']

            # sentence += fundamentals.stmt_for_qoq(qtr_pnl)
            sentence += "\n***PROS***\n"
            for each in metadata['pros']: sentence += f"{each}\n"
            if 'QPNL_tweet' in metadata.keys() and 'YPNL_tweet' in metadata.keys():
                sentence += f"\n{metadata['QPNL_tweet']}\n{metadata['YPNL_tweet']}"

            with coltw2:
                subcoltw2_1, subcoltw2_2 = st.columns([1, 1])
                textarea_is = st.text_area(label="👉 INSIGHTS", value=sentence, height=180, key="Insights")
                # with subcoltw2_1:
                #     if st.button("Overwrite Amibroker Notes"):
                #         amibroker.amibroker_notes_insights(metadata['code_names'], textarea_is)
                with subcoltw2_2:
                    if st.button('Send Telegram'):
                        bot.send_message(chat_id=chat_id, text=sentence)

        else:
            # get_latest_results([company_code])
            metadata = variables.metadata[company_code]
            if not os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and \
                    os.path.exists(
                        f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):  # if Quarterly data not available
                df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
                st.info(f"ONLY YEARLY DATA AVAILABLE, thus Reading ./pickl/{tree_folder}/{company_code} Yearly.pkl")
                try:
                    df_comp.columns = pd.to_datetime(df_comp, '%d-%m-%Y')
                except Exception as AttributeError:
                    pass
                # st.dataframe(df_comp)
                pnl, balancesht = fundamentals.develop_yearly(df_comp)

                with col2:
                    sub_choose = st.selectbox("Fundamentals:", fundamentals.funda_keys)

            elif os.path.exists(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl') and os.path.exists(
                    f'./pickl/{tree_folder}/{company_code} Yearly.pkl'):
                st.info(f"PKL FILE EXISTS, thus Reading './pickl/{tree_folder}/{company_code} Yearly.pkl' and './pickl/{tree_folder}/{company_code} Quarterly.pkl'   ")
                df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Yearly.pkl')
                # st.info(f"PKL FILE EXISTS, thus Reading './pickl/{tree_folder}/{comp_Name} Yearly.pkl'   ")
                # st.dataframe(df_comp)
                try:
                    df_comp.columns = pd.to_datetime(df_comp, '%d-%m-%Y')
                    # df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
                except Exception as AttributeError:
                    pass
                pnl, balancesht = fundamentals.develop_yearly(df_comp)

                qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{company_code} Quarterly.pkl')
                # pnl, balancesht, qtr_pnl = fundamentals.develop_data(qtr_pnl, df_comp)
                try:
                    qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
                    # qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
                except Exception as AttributeError:
                    pass

                qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)
                if company_code in variables.metadata.keys():
                    # st.info(f"METADATA already Avaialble ")
                    metadata = variables.metadata[company_code]
                else:
                    # st.info(f"METADATA NOT Avaialble ")
                    metadata = fundamentals.analyse_df(pnl, balancesht, qtr_pnl)
                    metadata['code_names'] = nse_bse_search.process_code(company_code, comp_Name)
                    variables.metadata[company_code] = metadata

                if len(metadata['tags'])>=1:
                    for each in metadata['tags']:
                        text_file = f'./watchlist/groups/{each}.txt'
                        if each not in variables.user_data.keys():
                            variables.user_data[each] = []
                        if metadata['code_names'][0] not in variables.user_data[each]:
                            with open(text_file, 'a+') as file:
                                file.write(f"{metadata['code_names'][0]}\n")
                                st.success(f"Updated {metadata['code_names'][0]} in {text_file}")
                        # this_text_list = []
                        # with open(text_file,'a+') as file:
                        #     for each in file:
                        #         this_text_list.append(each)
                        #     st.info(this_text_list)
                        #     if metadata['code_names'][0] not in this_text_list:
                        #         file.write(f"{metadata['code_names'][0]}\n")
                        #         st.success(f"Updated {metadata['code_names'][0]} in {text_file}")

                # st.info(metadata)
                proscons_col1, proscons_col2 = st.columns([1, 1])
                with proscons_col1:
                    st.title("PROS")
                    for each in metadata['pros']:
                        st.success(each)
                with proscons_col2:
                    st.title("CONS")
                    for each in metadata['cons']:
                        st.error(each)
                options = st.multiselect("TAGS" + metadata['tags'],["Favourite"],metadata['tags'])

                with st.sidebar:  # with col2:
                    sub_choose = st.selectbox("Fundamentals:", fundamentals.funda_menu)
                    st.title(comp_Name)

                # sentence = f"{comp_Name}: "
                # sentence += fundamentals.stmt_for_qoq(pnl)
                # st.info(metadata)
                sentence = ""
                if len(metadata['code_names']) == 1 and metadata['code_names'][0].isdigit():
                    sentence += f"CODE\tNAME"
                    sentence += f"BSECODE {metadata['code_names'][0]}\t{st.session_state.bsecodenum_codename[int(metadata['code_names'][0])]}"
                else:
                    sentence += f"CODES:"
                    for each in metadata['code_names']: sentence += f"{each}\t"
                sentence += "\n***CONS***\n"
                for each in metadata['cons']: sentence += f"{each}\n"
                sentence += "\n***YEARLY***" + metadata['YPNL_Statement']
                sentence += "\n***QUARTERLY***" + metadata['QPNL_Statement']

                # sentence += fundamentals.stmt_for_qoq(qtr_pnl)
                sentence += "\n***PROS***\n"
                for each in metadata['pros']: sentence += f"{each}\n"
                if 'QPNL_tweet' in metadata.keys() and 'YPNL_tweet' in metadata.keys():
                    sentence += f"\n{metadata['QPNL_tweet']}\n{metadata['YPNL_tweet']}"

                with coltw2:
                    subcoltw2_1, subcoltw2_2 = st.columns([1, 1])
                    textarea_is = st.text_area(label="👉 INSIGHTS", value=sentence, height=180, key="Insights")
                    # with subcoltw2_1:
                    #     if st.button("Overwrite Amibroker Notes"):
                    #         amibroker.amibroker_notes_insights(metadata['code_names'], textarea_is)
                    with subcoltw2_2:
                        if st.button('Send Telegram'):
                            bot.send_message(chat_id=chat_id, text=sentence)
                    # subcol4_1, subcol4_2 = st.columns([1,1])
                    # with subcol4_1:
                    #     consolidated = st.checkbox("Consolidated",value=False)
                    # with subcol4_2:
                    #     standalone = st.checkbox("Standalone",value=True)

        # with col2_header:
        #     # if st.button(f'GET RESULTS : Script'):
        #     #     get_latest_results([metadata['code_names'][0]])
        #     if st.button(f"Process all Pickle Files again and make TAGS from this WATCHLIST"):
        #         for each_code in show_list_as:
        #             company_code, code_name = get_code(each_code)
        #             if company_code is not None and code_name is not None:
        #                 code_names = nse_bse_search.process_code(company_code, code_name)                    
        #             #st.info(each_pickl)
        #             if os.path.exists(f"./pickl/{company_code[0]}/{company_code} Yearly.pkl") and os.path.exists(f"./pickl/{company_code[0]}/{company_code} Quarterly.pkl"):
        #                 with open(f"./pickl/{company_code[0]}/{company_code} Yearly.pkl", 'rb') as file:
        #                     yr_df = pickle.load(file)                    
        #                 with open(f"./pickl/{company_code[0]}/{company_code} Quarterly.pkl", 'rb') as file:
        #                     qtr_df = pickle.load(file)
        #                 st.success(f"Processing {company_code}")
        #                 pnl, balancesht = fundamentals.develop_yearly(yr_df)
        #                 qtr_pnl = fundamentals.develop_quarterly(qtr_df)
        #                 # st.dataframe(pnl)
        #                 # st.dataframe(qtr_pnl)                                        
        #                 metadata = fundamentals.analyse_df(pnl, balancesht, qtr_pnl)
        #                 metadata['code_names'] = code_names
        #                 metadata['Code'] = code_names[0]
        #                 variables.metadata[company_code] = metadata
        #                 # st.success(variables.metadata[company_code]['recent_quarter'])
        #                                                                                                                                             #writing tags to its respective text files
        #                 if len(metadata['tags'])>=1:
        #                     for each in metadata['tags']:
        #                         text_file = f'./watchlist/groups/{each}.txt'
        #                         if each not in variables.user_data.keys():
        #                             variables.user_data[each] = []    
        #                         if metadata['code_names'][0] not in variables.user_data[each]:
        #                             with open(text_file,'a+') as file:
        #                                 file.write(f"{metadata['code_names'][0]}\n")
        #                                 st.success(f"Updated {metadata['code_names'][0]} in {text_file}")
        #                     variables.metadata[company_code] = metadata
        #                 save_metadata()



                
                
        #sub_choose = option_menu("", fundamentals.funda_menu,default_index=3,orientation="horizontal")
        if sub_choose == "PROFIT&LOSS":            # YEARLY PNL
            Ykeydata,YSales, YOtherIncome,YExpenses,YOperatingProfit,YNetProfit,Ytable = st.tabs(['Key Data','SALES','OTHER INCOME','EXPENSES','OPERATING PROFIT','NET PROFIT','Y DATA'])

            with Ytable:
                # THE FOLLOWIGN CODE CALCULATES THE GROWTH OR DEGROWTH
                st.dataframe(pnl.style.format(formatter="{:.1f}"))
            with Ykeydata:
                fundamentals.group_2_bars(pnl,"SALES","OTHER INCOME",comp_Name, "Yearly")
                fundamentals.group_2_bars(pnl,"PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Yearly")
                #fundamentals.group_3_bars(pnl, "SALES", "PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Yearly")
                fundamentals.both_lines(pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'], comp_Name, "Yearly")
                fundamentals.bar_line(pnl, 'OPERATING PROFIT','OPM %', color_dict[color_key]['hash'], comp_Name, "Yearly")
                fundamentals.bar_line(pnl,'NET PROFIT','NPM %',color_dict[color_key]['hash'],comp_Name, "Yearly")

            with YSales:
                fundamentals.qoq_growth(pnl, 'SALES', color_dict[color_key]['hash'], comp_Name, "Yearly")
            with YOtherIncome:
                fundamentals.go_bar(pnl, 'OTHER INCOME', color_dict[color_key]['hash'], comp_Name,"Yearly")
            with YExpenses:
                fundamentals.go_bar(pnl, 'EXPENSES', color_dict[color_key]['hash'], comp_Name,"Yearly")
            with YOperatingProfit:
                fundamentals.qoq_growth(pnl, 'OPERATING PROFIT', color_dict[color_key]['hash'], comp_Name, "Yearly")
            with YNetProfit:
                fundamentals.qoq_growth(pnl,'NET PROFIT',color_dict[color_key]['hash'],comp_Name, "Yearly")

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
                fundamentals.group_2_bars(qtr_pnl, "SALES", "OTHER INCOME",comp_Name, "Quarterly")
                fundamentals.group_2_bars(qtr_pnl,"PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Quarterly")
                #fundamentals.group_3_bars(qtr_pnl, "SALES",  "PROFIT BEFORE TAX","NET PROFIT",comp_Name, "Quarterly")
                fundamentals.both_lines(qtr_pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'],comp_Name, "Quarterly")
                fundamentals.bar_line(qtr_pnl, 'OPERATING PROFIT','OPM %', color_dict[color_key]['hash'], comp_Name, "Quarterly")
                fundamentals.bar_line(qtr_pnl,'NET PROFIT','NPM %',color_dict[color_key]['hash'],comp_Name, "Quarterly")

            with QSales:
                fundamentals.qoq_growth(qtr_pnl,"SALES", color_dict[color_key]['hash'],comp_Name, "Quarterly")
            with QOtherIncome:
                fundamentals.go_bar(qtr_pnl, 'OTHER INCOME', color_dict[color_key]['hash'], comp_Name, "Quarterly")
            with QExpenses:
                fundamentals.go_bar(qtr_pnl, 'EXPENSES', color_dict[color_key]['hash'], comp_Name, "Quarterly")
            with QOperatingProfit:
                fundamentals.qoq_growth(qtr_pnl, 'OPERATING PROFIT', color_dict[color_key]['hash'], comp_Name, "Quarterly")
            with QNetProfit:
                fundamentals.qoq_growth(qtr_pnl,'NET PROFIT',color_dict[color_key]['hash'],comp_Name, "Quarterly")

        if sub_choose == 'BALANCE SHEET':        #YEARLY BALANCE SHEET
            BSKeyData, BSReserves, BSBorrowings, BSOtherAssets, BSOtherLiabilities, BSReceivables, BSInventory, BSCWIP, BStable = st.tabs(['KeyData','Reserves','Borrowings','OtherAssets','OtherLiabilities','Receivables','Inventory','CWIP','BS DATA'])
            with BSKeyData:
                fundamentals.bar_line(balancesht,"RESERVES","BORROWINGS",color_dict[color_key]['hash'],comp_Name, "Yearly")
                fundamentals.bar_line(balancesht,"RECEIVABLES","INVENTORY",color_dict[color_key]['hash'],comp_Name, "Yearly")
                fundamentals.bar_line(balancesht, "DEBTOR DAYS", "INVENTORY TURNOVER",color_dict[color_key]['hash'], comp_Name, "Yearly")
                fundamentals.bar_line(balancesht, "NET BLOCK", "CAPITAL WORK IN PROGRESS",color_dict[color_key]['hash'], comp_Name, "Yearly")
                #fundamentals.bar_line(balancesht, "NET BLOCK", "INVESTMENTS", color_dict[color_key]['hash'], comp_Name,"Yearly")
                #fundamentals.both_lines(balancesht, "ROCE", "ROE", color_dict[color_key]['hash'], color_line,comp_Name, "Yearly")

            with BStable:
                st.dataframe(balancesht.style.format(formatter="{:.1f}"))
            with BSCWIP:
                fundamentals.go_bar(balancesht, "CAPITAL WORK IN PROGRESS", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSInventory:
                fundamentals.go_bar(balancesht, "INVENTORY", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSReserves:
                fundamentals.qoq_growth(balancesht, "RESERVES", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSBorrowings:
                fundamentals.qoq_growth(balancesht, "BORROWINGS", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSReceivables:
                fundamentals.qoq_growth(balancesht, "RECEIVABLES", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSOtherAssets:
                fundamentals.qoq_growth(balancesht, "OTHER ASSETS", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with BSOtherLiabilities:
                fundamentals.qoq_growth(balancesht, "OTHER LIABILITIES", color_dict[color_key]['hash'],comp_Name, "Yearly")

        if sub_choose == 'CASH FLOW':        # YEARLY CASH FLOWS
            CF, CFop, CFinv, CFfin, NetCF, CFTab = st.tabs(["KeyData","Operating Cash","Investing Cash","Financing Cash","Net Cash Flow","Table"])
            with CFTab:
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
            with CF:
                fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_dict[color_key]['hash'],"Yearly")
            with CFop:
                fundamentals.qoq_growth(df_comp.loc[sub_choose], "CASH FROM OPERATING ACTIVITY", color_dict[color_key]['hash'],comp_Name,"Yearly")
            with CFfin:
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH FROM FINANCING ACTIVITY", color_dict[color_key]['hash'], comp_Name,"Yearly")
            with CFinv:
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH FROM INVESTING ACTIVITY", color_dict[color_key]['hash'],comp_Name,"Yearly")
            with NetCF:
                fundamentals.go_bar(df_comp.loc[sub_choose], "NET CASH FLOW", color_dict[color_key]['hash'], comp_Name,"Yearly")

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
                    components.html(key_data.replace("xx", comp_Name), height=1080)
                with coly:
                    components.html(comp_profile.replace("xxyy", comp_Name), height=1080)
            with st.expander(label='BALANCE SHEET'):
                st.dataframe(balancesht)
            with st.expander(label='YEARLY PNL'):
                st.dataframe(pnl)
            with st.expander(label='QUARTERLY PNL'):
                st.dataframe(qtr_pnl)

            keydata_col1, keydata_col2 = st.columns([1,1])
            with keydata_col1:
                fundamentals.bar_line(balancesht, "DEBTOR DAYS", "INVENTORY TURNOVER", color_dict[color_key]['hash'],comp_Name, "Yearly")
            with keydata_col2:
                fundamentals.bar_line(balancesht, "NET BLOCK", "CAPITAL WORK IN PROGRESS", color_dict[color_key]['hash'], comp_Name,"Yearly")
            with keydata_col1:
                fundamentals.bar_line(balancesht, "RESERVES", "BORROWINGS", color_dict[color_key]['hash'], comp_Name,"Yearly")
            with keydata_col2:
                fundamentals.bar_line(balancesht, "WORKING CAPITAL", "CASH & BANK", color_dict[color_key]['hash'],comp_Name,"Yearly")

            with keydata_col1:
                st.title("QUARTERLY")
                fundamentals.group_2_bars(qtr_pnl, "SALES", "OTHER INCOME", comp_Name, "Quarterly")

            with keydata_col2:
                st.title("YEARLY")
                fundamentals.group_2_bars(pnl, "SALES", "OTHER INCOME", comp_Name, "Yearly")

            with keydata_col1:
                fundamentals.both_lines(qtr_pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'],
                                        comp_Name, "Quarterly")
                fundamentals.bar_line(qtr_pnl, 'NET PROFIT', 'NPM %', color_dict[color_key]['hash'], comp_Name, "Quarterly")

            with keydata_col2:
                fundamentals.both_lines(pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'],
                                        comp_Name, "Yearly")
                fundamentals.bar_line(pnl, 'NET PROFIT', 'NPM %', color_dict[color_key]['hash'], comp_Name, "Yearly")

            fundamentals.go_group_bar(df_comp.loc['CASH FLOW'], "cash_flows", color_dict[color_key]['hash'], "Yearly")

        # for each in variables.metadata.keys():
        #     st.info(each)

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
        tech1_widget = tech_widget.replace("xxyyzz",comp_Name)
        components.html(tech1_widget.replace("xxyyzz",comp_Name), height = 1080)
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

    if funda_tech == "Analyse Watchlist":
        # lets get no of stocks in each recent_quarter of metadata
        reported_quarter = {}
        no_quarter_for = []
        for each in show_list_as:
            company_code, comp_Name = get_code(each)
            if company_code in variables.metadata.keys():
                metadata_info = variables.metadata[company_code]
                #lets get 'recent_quarter' from the metadata_info and it as a dictionary value and then add a number to its value            
                if 'recent_quarter' in metadata_info.keys():
                    recent_quarter = metadata_info['recent_quarter']
                    # get the str format for recent_quarter
                    recent_quarter = recent_quarter.strftime('%d-%m-%Y')
                    # Create a key as reported_quarter[recent_quarter] and assign it to 1 if first time or add if already number is available
                    if recent_quarter in reported_quarter.keys():
                        reported_quarter[recent_quarter]['tot'] = reported_quarter[recent_quarter]['tot'] + 1
                        reported_quarter[recent_quarter]['list of stocks'].append(each)
                    else:
                        reported_quarter[recent_quarter] = {}
                        reported_quarter[recent_quarter]['tot'] = 1
                        reported_quarter[recent_quarter]['list of stocks'] = [each]
                else:
                    no_quarter_for.append(each)
        # lets put this in weabpp
        if len(no_quarter_for) > 0:
            st.info(f"NO QUARTERLY DATA AVAILABLE FOR {no_quarter_for}")
        for each in reported_quarter.keys():
            st.info(f"({reported_quarter[each]['tot']}) reported Quarter is {each} : \n{reported_quarter[each]['list of stocks']}")
            txt_file_name = f"./watchlist/groups/still struck in {each}.txt"
            if st.button(label=f"Note to a TEXT FILE", key = each):
                with open(txt_file_name,'w') as file:
                    for each in reported_quarter[each]['list of stocks']:
                        file.write(f"{each}\n")
                st.success(f"Updated {txt_file_name}")

        st.markdown("""
            <style>
            .table-container {
                display: flex;
                flex-direction: column;
                width: 100%;
            }
            .table-row {
                display: flex;
                justify-content: space-between;
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            .table-cell {
                flex: 1;
                padding: 10px;
            }
            .table-cell.title {
                flex: 1;
                font-size: 32px; /* Title font size */
                font-weight: bold;
                color: white;      
            }
            .table-cell.success {
                flex: 2;
                color: green;
                background-color: #e6ffe6;
            }
            .table-cell.error {
                flex: 2;
                color: red;
                background-color: #ffe6e6;
            }
            .table-cell.buttons {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
            }
            </style>
        """, unsafe_allow_html=True)
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        # st.info(show_list_as)
        for each in show_list_as:
            company_code, comp_Name = get_code(each)
            if company_code in variables.metadata.keys():
                metadata_info = variables.metadata[company_code]
            else:
                tree_folder = comp_Name[0].upper()
                # st.info(f"comp_Name : {comp_Name}, Comp_code : {company_code}")
                if not os.path.exists(f'./pickl/{tree_folder}/{comp_Name} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{comp_Name} Yearly.pkl'):  # if Quarterly data not available
                    df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{comp_Name} Yearly.pkl')
                    # st.info(f"Reading ./pickl/{tree_folder}/{comp_Name} Yearly.pkl")
                    try:
                        df_comp.columns = pd.to_datetime(df_comp, '%d-%m-%Y')
                    except Exception as AttributeError:
                        pass
                    # st.dataframe(df_comp)
                    pnl, balancesht = fundamentals.develop_yearly(df_comp)

                elif os.path.exists(f'./pickl/{tree_folder}/{comp_Name} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{comp_Name} Yearly.pkl'):
                    df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{comp_Name} Yearly.pkl')
                    # st.info(f"PKL FILE EXISTS, thus Reading './pickl/{tree_folder}/{comp_Name} Yearly.pkl'   ")
                    # st.dataframe(df_comp)
                    try:
                        df_comp.columns = pd.to_datetime(df_comp, '%d-%m-%Y')
                        # df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
                    except Exception as AttributeError:
                        pass
                    pnl, balancesht = fundamentals.develop_yearly(df_comp)

                    qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{comp_Name} Quarterly.pkl')
                    # pnl, balancesht, qtr_pnl = fundamentals.develop_data(qtr_pnl, df_comp)
                    try:
                        qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
                        # qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
                    except Exception as AttributeError:
                        pass
                    qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)

                    metadata_info = fundamentals.analyse_df(pnl, balancesht, qtr_pnl)
                    metadata_info['code_names'] = nse_bse_search.process_code(company_code, comp_Name)
                    variables.metadata[company_code] = metadata_info
                    if 'tags' in metadata_info.keys():
                        if len(metadata_info['tags']) >=1:
                            for each in metadata_info['tags']:
                                text_file = f'./watchlist/groups/{each}.txt'
                                if each not in variables.user_data.keys():
                                    variables.user_data[each] = []
                                if metadata_info['code_names'][0] not in variables.user_data[each]:
                                    with open(text_file, 'a+') as file:
                                        file.write(f"{metadata_info['code_names'][0]}\n")
                                        st.success(f"Updated {metadata_info['code_names'][0]} in {text_file}")
                else:
                    st.error(f"PICKLE DATA is not available anywhere for {company_code}")

            # Create HTML for each piece of metadata
            code_names_html = "<br>".join(metadata_info["code_names"])
            pros_html = "<br>".join(metadata_info["pros"])
            cons_html = "<br>".join(metadata_info["cons"])

            st.markdown(f'''
                    <div class="table-row">
                        <div class="table-cell title">{code_names_html}</div>
                        <div class="table-cell success">{pros_html}</div>
                        <div class="table-cell error">{cons_html}</div>
                        
                    </div>
                    ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

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

#REFERENCE :
#FLASK : https://www.datasciencelearner.com/how-to-create-a-bar-chart-from-a-dataframe-in-python/#:~:text=There%20is%20also%20another%20method%20to%20create%20a,y-axis%20values%20you%20want%20to%20draw%20the%20bar.

#Streamlit Basics : https://www.datacamp.com/tutorial/streamlit#on-windows-

# https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb#:~:text=When%20building%20data%20apps%20using%20Streamlit%2C%20sometimes%20you,displayed%20in%20the%20app%20looks%20plain%20and%20static.

#https://towardsdatascience.com/create-a-bar-chart-race-animation-app-using-streamlit-and-raceplotly-e44495249f11


#   https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/