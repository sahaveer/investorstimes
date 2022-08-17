import streamlit as st
import glob
import pandas as pd
import fundamentals
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

st.set_page_config(page_title="iTimesAlgo", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="expanded",)
funda_keys = ['PROFIT&LOSS', 'BALANCE SHEET',
              'CASH FLOW']  # dont change the order of this list as it will affect the keys used in Yearly df
# **************************************************************************************************
listed_stocks = []
stocks_dict = {}
color_dict = {'Yellow_Lite': "#f8ba43", 'Yellow_Dark': "#D6D41B", 'Blue_Lite': "#0FBAEC", 'Blue_Dark': "#0971C9",
              'Green_Lite': "#11A694", 'Green_Dark': "#11A64B", "Purple_Lite": "#7019BF", 'Purple_Dark': "#9319BF"}
# color_list = ["#D6D41B","#f8ba43","#0971C9","#1959BF","#11A694","#11A64B","#7019BF","#9319BF"]
color_line = "Red"
for each_pickl in glob.glob('./pickl/*.pkl', recursive=False):
    each_pickl = each_pickl.replace('\\', '/')
    file_name_only = each_pickl.split('/')[-1]
    pickle_name = file_name_only.split('.pkl')[0]
    stocks_dict[pickle_name] = each_pickl
    listed_stocks += [pickle_name]

with st.sidebar:
    st.write(r"we have got now {} listed stocks data available".format(str(len(listed_stocks))))
    selected = st.selectbox("NSE Listed", listed_stocks)

if selected:
    funda_tech = option_menu("", ["Funda_Chart", 'Tech_Chart'],
                             icons=['house', '📈 '], menu_icon="cast", default_index=0, orientation="horizontal")
    if funda_tech == "Funda_Chart":
        screener_address = "https://www.screener.in/company/" + str(selected)
        st.markdown(f"[***SCREENER***]({screener_address})", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
        with col1:
            st.subheader('📈 ' + selected)
        with col3:
            color_key = st.selectbox("Bar Color", color_dict.keys())
            # color_bar = st.color_picker("Bar Color",value="#ECE80F")  # blueshades"#0971C9""ECE80F"   #yellowshades"#f8ba43"
        st.write("____")
        df_comp = pd.read_pickle(stocks_dict[selected])
        try:
            df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
        except Exception as AttributeError:
            pass
        comp_Name = str(selected)
        st.info(comp_Name)
        sub_choose = st.sidebar.selectbox("Fundamentals", fundamentals.funda_keys,index=0)
        if sub_choose == fundamentals.funda_keys[3]:
            st.subheader("THIS IS STILL IN PROGRESS")
            key_data = """<!-- TradingView Widget BEGIN -->
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
                              "symbol": "balamines",
                              "locale": "en"
                            }
                              </script>
                            </div>
                            <!-- TradingView Widget END -->"""
            comp_profile = """<!-- TradingView Widget BEGIN -->
                            <div class="tradingview-widget-container">
                              <div class="tradingview-widget-container__widget"></div>
                              <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text"> Profile</span></a> by TradingView</div>
                              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
                              {
                              "width": "100%",
                              "height": 880,
                              "colorTheme": "dark",
                              "isTransparent": false,
                              "symbol": "BALAMINES",
                              "locale": "en"
                            }
                              </script>
                            </div>
                            <!-- TradingView Widget END -->"""
            col1,col2 = st.columns([0.7,0.3])
            with col1:
                components.html(key_data, height=1080)
            with col2:
                components.html(comp_profile, height=1080)

        if sub_choose == fundamentals.funda_keys[0]:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.sidebar.selectbox("Params", index_list)
            if param == "key_params":
                with st.expander("YEARLY PROFIT & LOSS DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(df_comp.loc[sub_choose], "SALES", color_dict[color_key], comp_Name)
                fundamentals.group_2_bars(df_comp.loc[sub_choose], "PROFIT BEFORE TAX", "NET PROFIT", comp_Name)
            else:
                with col2:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)

        if sub_choose == fundamentals.funda_keys[1]:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.sidebar.selectbox("Params", index_list)
            if param == "key_params":
                with st.expander("YEARLY BALANCE SHEET DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.bar_line(df_comp.loc[sub_choose], "RESERVES", "BORROWINGS", color_dict[color_key],
                                      comp_Name)
                fundamentals.bar_line(df_comp.loc[sub_choose], "DEBTOR DAYS", "INVENTORY TURNOVER",
                                      color_dict[color_key], comp_Name)
                fundamentals.both_lines(df_comp.loc[sub_choose], "ROCE", "ROE", color_dict[color_key], color_line,
                                        comp_Name)
                # fundamentals.bar_line(df_comp.loc[sub_choose], "RECEIVABLES", "INVENTORY", color_dict[color_key], comp_Name)
                # fundamentals.go_bar(df_comp.loc[sub_choose], "CAPITAL WORK IN PROGRESS", color_dict[color_key], comp_Name)
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH & BANK", color_dict[color_key], comp_Name)
            else:
                with col2:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)
        if sub_choose == fundamentals.funda_keys[2]:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.sidebar.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("YEARLY CASH FLOWS DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_dict[color_key])
            else:
                with col2:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)
    if funda_tech == "Tech_Chart":
        st.subheader("TECH CHART IS STILL IN PROGRESS")
        tech_analytics_widget = """<!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
          <div id="analytics-platform-chart-demo"></div>
          <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Chart</span></a> by TradingView</div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget(
          {
          "container_id": "analytics-platform-chart-demo",
          "width": "100%","height": "680",
          "symbol": "ADANIPORTS",
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
        components.html(tech_analytics_widget, height=1080)
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