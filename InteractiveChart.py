import streamlit as st
import glob
import os
import datetime
import pandas as pd
import numpy as np
import fundamentals
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import json
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import nse_bse_search


st.set_page_config(page_title="iTimesAlgo", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="expanded",)

global bsecodenum_codename
global bsecodename_codenum
#bsecodenum_codename, bsecodename_codenum,bsecodenum_fullname,bsecodename_fullname = nse_bse_search.bsecodenum_bsecodename()
bsecodenum_codename,bsecodename_codenum,bsecodenum_fullname,bsecodename_fullname,bsefullname_codenum,bsefullname_codename = nse_bse_search.bsecodenum_bsecodename()


# PARAMS
funda_keys = ['PROFIT&LOSS', 'BALANCE SHEET',
              'CASH FLOW']  # dont change the order of this list as it will affect the keys used in Yearly df

# **************************************************************************************************
listed_stocks = []
latest_quarterly_stocks = []
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


#lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
for each_pickl in glob.glob('./pickl/**/*.pkl', recursive=True):
    each_pickl = each_pickl.replace('\\', '/')
    #st.info(each_pickl)
    file_name_only = os.path.basename(each_pickl)
    #file_name_only = each_pickl.split('/')[-1]
    tree_folder = file_name_only[0].upper()
    if file_name_only.endswith('Yearly.pkl'):
        pickle_name = file_name_only.split('Yearly.pkl')[0].strip()  # Since all the pickle files are either Quartetrly or Yearly, we need to get the first company code only
    elif file_name_only.endswith('Quarterly.pkl'):
        pickle_name = file_name_only.split('Quarterly.pkl')[0].strip()#st.info(pickle_name)
        qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{file_name_only}')
        qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
        try:
            timedelta_90_days = pd.Timedelta(days=90)
            # st.info(datetime.datetime.now().strptime-qtr_pnl.columns[-1])
            # st.info(type(datetime.datetime.now()-qtr_pnl.columns[-1]))
            if (datetime.datetime.now() - qtr_pnl.columns[-1]) < timedelta_90_days and pickle_name not in latest_quarterly_stocks:
                latest_quarterly_stocks.append(pickle_name)
                last_announced_quarter = datetime.datetime.strftime(qtr_pnl.columns[-1],'%b%Y')

        except:
            pass

    if pickle_name not in listed_stocks:
        listed_stocks.append(pickle_name)




st.title(f"👇 Chose among {str(len(listed_stocks))} listed stocks")
st.subheader(f"{str(len(latest_quarterly_stocks))} stocks announced {last_announced_quarter} Quarterly Results")
#selected = st.selectbox("Chose Company", listed_stocks)

col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
with col1:
    show_latest_quarter = st.checkbox(label='Only latest Quarter',value=True)
    if show_latest_quarter:
        selected = st.selectbox("Chose Company 📈 ",latest_quarterly_stocks )
    else:
        selected = st.selectbox("Chose Company 📈 ", listed_stocks)


if selected:
    #st.text_area(label="COPY THESE", value=latest_quarterly_stocks, height=180)
    comp_Name = str(selected)
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
    coltw1, coltw2 = st.columns([2, 2])
    with coltw1:
        components.html(ticker_symbol_info.replace("xyx", comp_Name), height=200)
    sentence = f"{comp_Name}: "

    funda_tech = option_menu("", ["Funda_Chart", 'Tech_Chart'],
                             icons=['house', '📈 '], menu_icon="cast", default_index=0, orientation="horizontal")
    nsecode = nse_bse_search.nse_code

    if funda_tech == "Funda_Chart":
        if selected in nsecode:
            nse_screener_address = "https://www.screener.in/company/" + str(selected)
            with st.sidebar:
                st.markdown(f"[***NSE SCREENER***]({nse_screener_address})", unsafe_allow_html=True)
        elif selected in bsecodename_codenum.keys():
            codenum = bsecodename_codenum[selected]
            bse_screener_address = "https://www.screener.in/company/" + str(codenum)
            with st.sidebar:
                st.markdown(f"[***BSE SCREENER***]({bse_screener_address})", unsafe_allow_html=True)
        with st.sidebar:
            #color_key = st.selectbox("Bar Color", color_dict.keys())
            color_key = 'blue3'
        tree_folder = comp_Name[0].upper()


        if not os.path.exists(f'./pickl/{tree_folder}/{selected} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{selected} Yearly.pkl'):
            Yearly_sentence_in_Quarterly = ""
            df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{selected} Yearly.pkl')
            try:
                df_comp.columns = pd.to_datetime(df_comp,'%d-%m-%Y')
                #df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
            except Exception as AttributeError:
                pass
            # st.dataframe(df_comp)
            if len(balancesht.columns) >= 2 and "NO. OF EQUITY SHARES" in balancesht.index:
                last_year = balancesht.columns[-1]
                prev_year = balancesht.columns[-2]
                eq_last_year = round(balancesht.loc["NO. OF EQUITY SHARES", last_year] / 10000000, 2)
                eq_prev_year = round(balancesht.loc['NO. OF EQUITY SHARES', prev_year] / 10000000, 2)
                FV_last_year = round(balancesht.loc['FACE VALUE', last_year])
                FV_prev_year = round(balancesht.loc['FACE VALUE', prev_year])
                ROCE_last_year = balancesht.loc['ROCE', last_year]
                ROCE_prev_year = balancesht.loc['ROCE', prev_year]
                Yearly_sentence_in_Quarterly += f"*****\nEquity in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(eq_last_year)}cr; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(eq_prev_year)}cr\nFaceValue in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(FV_last_year)}; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(FV_prev_year)}\nROCE in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(ROCE_last_year)}%; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(ROCE_prev_year)}%\n*****\n"

            pnl, balancesht = fundamentals.develop_yearly(df_comp)
            with col2:
                sub_choose = st.selectbox("Fundamentals:", fundamentals.funda_keys)


        elif os.path.exists(f'./pickl/{tree_folder}/{selected} Quarterly.pkl') and os.path.exists(f'./pickl/{tree_folder}/{selected} Yearly.pkl'):
            Yearly_sentence_in_Quarterly = ""
            df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{selected} Yearly.pkl')
            #st.dataframe(df_comp)
            try:
                df_comp.columns = pd.to_datetime(df_comp,'%d-%m-%Y')
                #df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
            except Exception as AttributeError:
                pass
            pnl, balancesht = fundamentals.develop_yearly(df_comp)

            if len(balancesht.columns) >= 2 and "NO. OF EQUITY SHARES" in balancesht.index:
                last_year = balancesht.columns[-1]
                prev_year = balancesht.columns[-2]
                eq_last_year = round(balancesht.loc["NO. OF EQUITY SHARES", last_year] / 10000000, 2)
                eq_prev_year = round(balancesht.loc['NO. OF EQUITY SHARES', prev_year] / 10000000, 2)
                FV_last_year = round(balancesht.loc['FACE VALUE', last_year])
                FV_prev_year = round(balancesht.loc['FACE VALUE', prev_year])
                ROCE_last_year = balancesht.loc['ROCE', last_year]
                ROCE_prev_year = balancesht.loc['ROCE', prev_year]
                Yearly_sentence_in_Quarterly += f"*****\nEquity in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(eq_last_year)}cr; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(eq_prev_year)}cr\nFaceValue in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(FV_last_year)}; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(FV_prev_year)}\nROCE in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(ROCE_last_year)}%; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(ROCE_prev_year)}%\n*****\n"

            qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{selected} Quarterly.pkl')
            try:
                qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
                #qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
            except Exception as AttributeError:
                pass
            qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)
            with col2:
                sub_choose = st.selectbox("Fundamentals", fundamentals.funda_menu)

        sentence += fundamentals.stmt_for_qoq(pnl)
        sentence += Yearly_sentence_in_Quarterly
        sentence += fundamentals.stmt_for_qoq(qtr_pnl)

        with coltw2:
            st.text_area(label="👉 INSIGHTS", value=sentence, height=180)


        #with col_sub1:
            #st.subheader('📊 ' + comp_Name)
        #sub_choose = option_menu("", fundamentals.funda_menu,default_index=3,orientation="horizontal")
        if sub_choose == "PROFIT&LOSS":            # YEARLY PNL
            Ykeydata,YSales, YOtherIncome,YExpenses,YOperatingProfit,YNetProfit,Ytable = st.tabs(['Key Data','SALES','OTHER INCOME','EXPENSES','OPERATING PROFIT','NET PROFIT','Table'])

            with Ytable:
                # THE FOLLOWIGN CODE CALCULATES THE GROWTH OR DEGROWTH
                st.dataframe(pnl.style.format(formatter="{:.1f}"))
            with Ykeydata:
                fundamentals.group_2_bars(pnl, "SALES", "PROFIT BEFORE TAX","NET PROFIT",comp_Name)
                fundamentals.both_lines(pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'], comp_Name)
            with YSales:
                fundamentals.qoq_growth(pnl, 'SALES', color_dict[color_key]['hash'], comp_Name)
            with YOtherIncome:
                fundamentals.go_bar(pnl, 'OTHER INCOME', color_dict[color_key]['hash'], comp_Name)
            with YExpenses:
                fundamentals.go_bar(pnl, 'EXPENSES', color_dict[color_key]['hash'], comp_Name)
            with YOperatingProfit:
                fundamentals.bar_line(pnl, 'OPERATING PROFIT','OPM %', color_dict[color_key]['hash'], comp_Name)
            with YNetProfit:
                fundamentals.bar_line(pnl,'NET PROFIT','NPM %',color_dict[color_key]['hash'],comp_Name)

        if sub_choose == 'QTR PnL':                #QUARTERLY PNL
            Qkeydata, QSales, QOtherIncome, QExpenses, QOperatingProfit, QNetProfit, Qtable = st.tabs(
                ['Key Data', 'SALES', 'OTHER INCOME', 'EXPENSES', 'OPERATING PROFIT', 'NET PROFIT', 'Table'])
            with Qtable:
                st.dataframe(qtr_pnl)
                # Replace the first row with NaN for the QoQ columns
                #df.loc[0, ['SALES_QoQ', 'NET PROFIT_QoQ', 'OPERATING PROFIT_QoQ']] = np.nan
                #df = df.transpose()
                #st.dataframe(qtr_pnl.style.format(formatter="{:.1f}"))

            with Qkeydata:
                fundamentals.group_2_bars(qtr_pnl, "SALES",  "PROFIT BEFORE TAX","NET PROFIT",comp_Name)
                fundamentals.both_lines(qtr_pnl, "OPM %", "NPM %", color_dict['red1']['hash'], color_dict['green1']['hash'],comp_Name)
                fundamentals.bar_line(qtr_pnl,'NET PROFIT','NPM %',color_dict[color_key]['hash'],comp_Name)
            with QSales:
                fundamentals.qoq_growth(qtr_pnl,"SALES", color_dict[color_key]['hash'],comp_Name)
            with QOtherIncome:
                fundamentals.go_bar(qtr_pnl, 'OTHER INCOME', color_dict[color_key]['hash'], comp_Name)
            with QExpenses:
                fundamentals.go_bar(qtr_pnl, 'EXPENSES', color_dict[color_key]['hash'], comp_Name)
            with QOperatingProfit:
                fundamentals.bar_line(qtr_pnl, 'OPERATING PROFIT','OPM %', color_dict[color_key]['hash'], comp_Name)
            with QNetProfit:
                fundamentals.bar_line(qtr_pnl,'NET PROFIT','NPM %',color_dict[color_key]['hash'],comp_Name)


        if sub_choose == 'BALANCE SHEET':        #YEARLY BALANCE SHEET
            BSKeyData, BStable, BSReserves, BSBorrowings, BSOtherAssets, BSOtherLiabilities, BSReceivables, BSInventory, BSCWIP = st.tabs(['KeyData','table','Reserves','Borrowings','OtherAssets','OtherLiabilities','Receivables','Inventory','CWIP'])
            with BSKeyData:
                fundamentals.bar_line(balancesht,"RESERVES","BORROWINGS",color_dict[color_key]['hash'],comp_Name)
                fundamentals.bar_line(balancesht,"RECEIVABLES","INVENTORY",color_dict[color_key]['hash'],comp_Name)
                fundamentals.bar_line(balancesht, "DEBTOR DAYS", "INVENTORY TURNOVER",color_dict[color_key]['hash'], comp_Name)
                fundamentals.bar_line(balancesht, "CAPITAL WORK IN PROGRESS", "INVESTMENTS",color_dict[color_key]['hash'], comp_Name)
                #fundamentals.both_lines(balancesht, "ROCE", "ROE", color_dict[color_key]['hash'], color_line,comp_Name)
            with BStable:
                st.dataframe(balancesht.style.format(formatter="{:.1f}"))
            with BSCWIP:
                fundamentals.go_bar(balancesht, "CAPITAL WORK IN PROGRESS", color_dict[color_key]['hash'],comp_Name)
            with BSInventory:
                fundamentals.go_bar(balancesht, "INVENTORY", color_dict[color_key]['hash'],comp_Name)
            with BSReserves:
                fundamentals.qoq_growth(balancesht, "RESERVES", color_dict[color_key]['hash'],comp_Name)
            with BSBorrowings:
                fundamentals.qoq_growth(balancesht, "BORROWINGS", color_dict[color_key]['hash'],comp_Name)
            with BSReceivables:
                fundamentals.qoq_growth(balancesht, "RECEIVABLES", color_dict[color_key]['hash'],comp_Name)
            with BSOtherAssets:
                fundamentals.qoq_growth(balancesht, "OTHER ASSETS", color_dict[color_key]['hash'],comp_Name)
            with BSOtherLiabilities:
                fundamentals.qoq_growth(balancesht, "OTHER LIABILITIES", color_dict[color_key]['hash'],comp_Name)

        if sub_choose == 'CASH FLOW':        # YEARLY CASH FLOWS
            CF, CFTab, CFop, CFinv, CFfin, NetCF = st.tabs(["KeyData","Table","Operating Cash","Investing Cash","Financing Cash","Net Cash Flow"])
            with CFTab:
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
            with CF:
                fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_dict[color_key]['hash'])
            with CFop:
                fundamentals.qoq_growth(df_comp.loc[sub_choose], "CASH FROM OPERATING ACTIVITY", color_dict[color_key]['hash'],comp_Name)
            with CFfin:
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH FROM FINANCING ACTIVITY", color_dict[color_key]['hash'], comp_Name)
            with CFinv:
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH FROM INVESTING ACTIVITY", color_dict[color_key]['hash'],comp_Name)
            with NetCF:
                fundamentals.go_bar(df_comp.loc[sub_choose], "NET CASH FLOW", color_dict[color_key]['hash'], comp_Name)
        if sub_choose == fundamentals.funda_menu[4]:
            key_data = str("""<!-- TradingView Widget BEGIN -->
                            <div class="tradingview-widget-container">
                              <div class="tradingview-widget-container__widget"></div>
                              <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
                              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-financials.js" async>
                              {
                              "colorTheme": "dark",
                              "isTransparent": false,
                              "largeChartUrl": "",
                              "displayMode": "regular",
                              "width": "100%",
                              "height": 830,
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
            colx,coly = st.columns([1.5,1])
            with colx:
                search_sym = "NSE:" + comp_Name
                components.html(key_data.replace("xx",comp_Name), height=1080)
            with coly:
                components.html(comp_profile.replace("xxyy",comp_Name), height=1080)


    if funda_tech == "Tech_Chart":
        with st.expander("IF ERROR / FETCHING APPLE STOCK"):
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
