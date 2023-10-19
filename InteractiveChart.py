import streamlit as st
import glob
import os
import pandas as pd
import numpy as np
import fundamentals
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import json
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

st.set_page_config(page_title="iTimesAlgo", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="expanded",)               # initial_sidebar_state can be set to 'collapsed'
# PARAMS
st.title('DIY Fundamentals :bar_chart:')
funda_keys = ['PROFIT&LOSS', 'BALANCE SHEET',
              'CASH FLOW']  # dont change the order of this list as it will affect the keys used in Yearly df

# **************************************************************************************************
listed_stocks = []
stocks_dict = {}
color_dict = {'Yellow_Lite': "#f8ba43", 'Yellow_Dark': "#D6D41B", 'Blue_Lite': "#0FBAEC", 'Blue_Dark': "#0971C9",
              'Green_Lite': "#11A694", 'Green_Dark': "#11A64B", "Purple_Lite": "#7019BF", 'Purple_Dark': "#9319BF"}
# color_list = ["#D6D41B","#f8ba43","#0971C9","#1959BF","#11A694","#11A64B","#7019BF","#9319BF"]
color_line = "Red"

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_bar = load_lottiefile("./lottie/barchart.json")  # replace link to local lottie file
lottie_data_analysis = load_lottiefile("./lottie/data-analysis.json")


#lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
for each_pickl in glob.glob('./pickl/**/*.pkl', recursive=True):
    each_pickl = each_pickl.replace('\\', '/')
    #st.info(each_pickl)
    file_name_only = os.path.basename(each_pickl)
    #file_name_only = each_pickl.split('/')[-1]
    if file_name_only.endswith('Yearly.pkl'):
        pickle_name = file_name_only.split('Yearly.pkl')[0].strip()  # Since all the pickle files are either Quartetrly or Yearly, we need to get the first company code only
    elif file_name_only.endswith('Quarterly.pkl'):
        pickle_name = file_name_only.split('Quarterly.pkl')[0].strip()  # st.info(pickle_name)
    #st.info(pickle_name)
    if pickle_name not in listed_stocks:
        listed_stocks.append(pickle_name)
    #stocks_dict[pickle_name] = each_pickl
    #listed_stocks += [pickle_name]

with st.sidebar:
    st_lottie(
        lottie_data_analysis,
        speed=0.7,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=None,
        width=None,
        key="barchart",)
    st.write(r"Chose among {} listed stocks available".format(str(len(listed_stocks))))
    #selected = st.selectbox("Chose Company", listed_stocks)

col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
with col1:
    selected = st.selectbox("Chose Company 📈 ", listed_stocks)
if selected:
    funda_tech = option_menu("", ["Funda_Chart", 'Tech_Chart'],
                             icons=['house', '📈 '], menu_icon="cast", default_index=0, orientation="horizontal")
    comp_Name = str(selected)
    if funda_tech == "Funda_Chart":
        screener_address = "https://www.screener.in/company/" + str(selected)
        with col4:
            st.markdown(f"[***SCREENER***]({screener_address})", unsafe_allow_html=True)
        with col3:
            color_key = st.selectbox("Bar Color", color_dict.keys())
            # color_bar = st.color_picker("Bar Color",value="#ECE80F")  # blueshades"#0971C9""ECE80F"   #yellowshades"#f8ba43"

        #df_comp = pd.read_pickle(stocks_dict[selected])
        tree_folder = comp_Name[0].upper()
        df_comp = pd.read_pickle(f'./pickl/{tree_folder}/{selected} Yearly.pkl')
        qtr_pnl = pd.read_pickle(f'./pickl/{tree_folder}/{selected} Quarterly.pkl')
        pnl = df_comp.loc['PROFIT&LOSS']
        pnl.fillna(0, inplace=True)
        pnl.index = pnl.index.str.strip()
        pnl = pnl.transpose()
        pnl['EXPENSES'] = pnl['RAW MATERIAL COST'] - pnl['CHANGE IN INVENTORY'] + pnl['POWER AND FUEL'] + pnl[
            'OTHER MFR. EXP'] + pnl['EMPLOYEE COST'] + pnl['SELLING AND ADMIN'] + pnl['OTHER EXPENSES']
        pnl = pnl.drop(
            columns=['RAW MATERIAL COST', 'CHANGE IN INVENTORY', 'POWER AND FUEL', 'OTHER MFR. EXP', 'EMPLOYEE COST',
                     'SELLING AND ADMIN', 'OTHER EXPENSES'], axis=1)
        pnl['OPERATING PROFIT'] = pnl['SALES'] - pnl['EXPENSES']
        pnl['OPM %'] = pnl.apply(fundamentals.OPM, axis=1)
        pnl['NPM %'] = pnl.apply(fundamentals.NPM, axis=1)
        # Calculate the QoQ percentage increase for SALES, NET PROFIT, and OPERATING PROFIT
        pnl['SALES_QoQ'] = pnl['SALES'].pct_change() * 100
        pnl['NET PROFIT_QoQ'] = pnl['NET PROFIT'].pct_change() * 100

        balancesht = df_comp.loc['BALANCE SHEET'].drop(index='TOTAL', errors='ignore')
        balancesht.fillna(0, inplace=True)
        balancesht.index = balancesht.index.str.strip()
        balancesht = balancesht.transpose()
        balancesht['WORKING CAPITAL'] = balancesht['OTHER ASSETS'] - balancesht['OTHER LIABILITIES']
        balancesht['DEBTOR DAYS'] = np.where(pnl['SALES'] > 0, balancesht['RECEIVABLES'] / (pnl['SALES'] / 365), 0)
        balancesht['INVENTORY TURNOVER'] = np.where(balancesht['INVENTORY'] > 0, pnl['SALES'] / balancesht['INVENTORY'],
                                                    0)
        balancesht['ROCE'] = np.where(balancesht['NET BLOCK'] + balancesht['WORKING CAPITAL'] > 0, (
                (pnl['OPERATING PROFIT'] - pnl['DEPRECIATION'] - pnl['TAX']) / (
                balancesht['NET BLOCK'] + balancesht['WORKING CAPITAL'])) * 100, 0)

        qtr_pnl.fillna(0, inplace=True)
        qtr_pnl.index = qtr_pnl.index.str.strip()
        qtr_pnl = qtr_pnl.transpose()
        qtr_pnl['OPM %'] = qtr_pnl.apply(fundamentals.OPM, axis=1)
        qtr_pnl['NPM %'] = qtr_pnl.apply(fundamentals.NPM, axis=1)
        pnl = pnl.transpose()
        pnl = pnl.round(2)
        # st.dataframe(pnl)
        balancesht = balancesht.transpose()
        balancesht = balancesht.round(2)
        # st.dataframe(balancesht)
        qtr_pnl = qtr_pnl.transpose()
        qtr_pnl = qtr_pnl.round(2)
        # qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
        # st.dataframe(qtr_pnl)
        try:
            df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
        except Exception as AttributeError:
            pass

        sub_choose = option_menu("", fundamentals.funda_menu,default_index=0,orientation="horizontal")
        #sub_choose = st.sidebar.selectbox("Fundamentals", fundamentals.funda_menu,index=0)

        # KEY DATA PULLED FROM TRADINGVIEW
        if sub_choose == fundamentals.funda_menu[3]:                  #QUARTERLY
            index_list = ["key_params"] + list(qtr_pnl.index)
            with col2:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("QUARTERLY PROFIT & LOSS DATA"):
                    st.dataframe(qtr_pnl.style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(qtr_pnl, "SALES", color_dict[color_key], comp_Name)
                fundamentals.group_2_bars(qtr_pnl, "PROFIT BEFORE TAX", "NET PROFIT", comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "PROFIT BEFORE TAX", color_dict[color_key], comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "NET PROFIT", color_dict[color_key], comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("QoQ Growth%")
                if qoq_checked:
                    fundamentals.qoq_growth(qtr_pnl, param, color_dict[color_key], comp_Name)
                else:
                    fundamentals.go_bar(qtr_pnl, param, color_dict[color_key], comp_Name)

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

        # YEARLY SALES
        if sub_choose == fundamentals.funda_menu[0]:
            index_list = ["key_params"] + list(pnl.index)
            with col2:
                param = st.selectbox("Params", index_list)
            if param == "key_params":
                with st.expander("YEARLY PROFIT & LOSS DATA"):
                    st.dataframe(pnl.style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(pnl, "SALES", color_dict[color_key], comp_Name)
                fundamentals.group_2_bars(pnl, "PROFIT BEFORE TAX", "NET PROFIT", comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("QoQ Growth%")
                if qoq_checked:
                    fundamentals.qoq_growth(pnl, param, color_dict[color_key], comp_Name)
                else:
                    fundamentals.go_bar(pnl, param, color_dict[color_key], comp_Name)

        # YEARLY BALANCE SHEET
        if sub_choose == fundamentals.funda_menu[1]:
            index_list = ["key_params"] + list(balancesht.index)
            #param = st.sidebar.selectbox("Params", index_list)
            with col2:
                param = st.selectbox("Params", index_list)
            if param == "key_params":
                with st.expander("YEARLY BALANCE SHEET DATA"):
                    st.dataframe(balancesht.style.format(formatter="{:.1f}"))
                fundamentals.bar_line(balancesht, "RESERVES", "BORROWINGS", color_dict[color_key],
                                      comp_Name)
                fundamentals.bar_line(balancesht, "DEBTOR DAYS", "INVENTORY TURNOVER",color_dict[color_key], comp_Name)
                fundamentals.bar_line(balancesht, "CAPITAL WORK IN PROGRESS", "INVESTMENTS",color_dict[color_key], comp_Name)
                #fundamentals.both_lines(balancesht, "ROCE", "ROE", color_dict[color_key], color_line,comp_Name)
                fundamentals.bar_line(balancesht, "RECEIVABLES", "INVENTORY", color_dict[color_key], comp_Name)
                # fundamentals.go_bar(balancesht, "CAPITAL WORK IN PROGRESS", color_dict[color_key], comp_Name)
                fundamentals.go_bar(balancesht, "CASH & BANK", color_dict[color_key], comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("QoQ Growth%")
                if qoq_checked:
                    fundamentals.qoq_growth(balancesht, param, color_dict[color_key], comp_Name)
                else:
                    fundamentals.go_bar(balancesht,param, color_dict[color_key], comp_Name)


        # YEARLY CASH AND FLOW
        if sub_choose == fundamentals.funda_menu[2]:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            # param = st.sidebar.selectbox("SubChose", index_list)
            # param = st.sidebar.selectbox("Params", index_list)
            with col2:
                param = st.selectbox("Params", index_list)
            if param == "key_params":
                with st.expander("YEARLY CASH FLOWS DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_dict[color_key])
            else:
                with col4:
                    qoq_checked = st.checkbox("QoQ Growth%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)


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
