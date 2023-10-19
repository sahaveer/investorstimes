import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import openpyxl
from openpyxl.utils import get_column_letter
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
import os
import fundamentals
import json
from streamlit_lottie import st_lottie
st.set_page_config(page_title="Upload", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="expanded",)
st.title('Upload _Excel file_ from [***SCREENER***]({https://www.screener.in/}) ')
color_dict = {'Yellow_Lite':"#f8ba43",'Yellow_Dark':"#D6D41B",'Blue_Lite':"#1959BF",'Blue_Dark':"#0971C9",'Green_Lite':"#11A694",'Green_Dark':"#11A64B","Purple_Lite":"#7019BF",'Purple_Dark':"#9319BF"}
#color_list = ["#D6D41B","#f8ba43","#0971C9","#1959BF","#11A694","#11A64B","#7019BF","#9319BF"]
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_data_analytics = load_lottiefile("./lottie/data-analytics.json")

with st.sidebar:
    st.markdown(""" <style> .font {
    font-size:22px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    # Add a file uploader to allow users to upload their csv file

    uploaded_file = st.file_uploader("", type=['xlsx','xlsm'],accept_multiple_files = True)  # Only accepts xlsx,xlsm file format
    st.markdown('<p class="font">Upload One or Two xlsx/xlsm FILES from screener.in </p>',
                unsafe_allow_html=True)
    st_lottie(
        lottie_data_analytics,
        speed=0.7,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=None,
        width=None,
        key="barchart", )
if uploaded_file is not None:
    if len(uploaded_file)==1:
        comp_Name = uploaded_file[0].name.split('.xlsx')[0]
        comp_Name = comp_Name.split('.xlsm')[0]
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        with col1:
            st.subheader('📈 ' + comp_Name)
        with col4:
            color_key = st.selectbox("Bar Color",color_dict.keys())
            #color_bar = st.color_picker("Bar Color", value="#ECE80F")  # blueshades"#0971C9""ECE80F"   #yellowshades"#f8ba43"
        st.write("____")
        book = openpyxl.load_workbook(uploaded_file[0])
        #comp_name = book['Data Sheet']['B1'].value
        qtr_pnl,df_comp = fundamentals.get_tables(book[fundamentals.tabs[-1]], uploaded_file[0])  # send a sheet(not whole workbook)

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
        qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
        # st.dataframe(qtr_pnl)
        try:
            df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
        except Exception as AttributeError:
            pass
        try:
            qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
        except Exception as AttributeError:
            pass
        # **************************************************************************************************
        colx, coly = st.columns([0.5, 0.5])
        with colx:
            save_code = st.text_input(label='Comp Code')
        with coly:
            if save_code :
                save_code = str(save_code)
                first_letter = save_code[0].upper()
                alphabetic_folder = os.path.join("./pickl/", first_letter)
                # Create the folder if it doesn't exist
                if not os.path.exists(alphabetic_folder):
                    os.makedirs(alphabetic_folder)
                df_comp.to_pickle("./pickl/" + first_letter + '/' + save_code + " Yearly.pkl")
                qtr_pnl.to_pickle("./pickl/" + first_letter + '/' + save_code + " Quarterly.pkl")
        with col2:
            sub_choose = st.selectbox("Fundamentals", fundamentals.funda_menu)
        if sub_choose == fundamentals.funda_menu[0]:            # YEARLY PNL
            index_list = ["key_params"] + list(pnl.index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("YEARLY PROFIT & LOSS DATA"):
                    st.dataframe(pnl.style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(pnl, "SALES", color_dict[color_key],comp_Name)
                fundamentals.group_2_bars(pnl,"PROFIT BEFORE TAX","NET PROFIT",comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(pnl, param, color_dict[color_key],comp_Name)
                else:
                    fundamentals.go_bar(pnl, param, color_dict[color_key],comp_Name)
        if sub_choose == fundamentals.funda_menu[3]:                #QUARTERLY PNL
            index_list = ["key_params"] + list(qtr_pnl.index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("QUARTERLY PROFIT & LOSS DATA"):
                    st.dataframe(qtr_pnl.style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(qtr_pnl, "SALES", color_dict[color_key],comp_Name)
                fundamentals.group_2_bars(qtr_pnl, "PROFIT BEFORE TAX","NET PROFIT",comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "PROFIT BEFORE TAX", color_dict[color_key],comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "NET PROFIT", color_dict[color_key],comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(qtr_pnl, param, color_dict[color_key],comp_Name)
                else:
                    fundamentals.go_bar(qtr_pnl, param, color_dict[color_key],comp_Name)
    
        if sub_choose == fundamentals.funda_menu[1]:        #YEARLY BALANCE SHEET
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("YEARLY BALANCE SHEET DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.bar_line(df_comp.loc[sub_choose],"RESERVES","BORROWINGS",color_dict[color_key],comp_Name)
                fundamentals.bar_line(df_comp.loc[sub_choose],"RECEIVABLES","INVENTORY",color_dict[color_key],comp_Name)
                fundamentals.go_bar(df_comp.loc[sub_choose], "CAPITAL WORK IN PROGRESS", color_dict[color_key],comp_Name)
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH & BANK", color_dict[color_key],comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key],comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key],comp_Name)
        if sub_choose == fundamentals.funda_menu[2]:        # YEARLY CASH FLOWS
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("YEARLY CASH FLOWS DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_dict[color_key])
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key],comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key], comp_Name)
    if len(uploaded_file)==2:
        comp1_Name = uploaded_file[0].name.split('.')[0]
        comp2_Name = uploaded_file[1].name.split('.')[0]
        col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
        with col1:
            st.subheader('📈 ' + comp1_Name + '📈 ' + comp2_Name )
        with col2:
            qoq_checked = st.checkbox("Sequential_Growth_%")
        with col3:
            color_bar = st.color_picker("Bar Color",
                                        value="#ECE80F")  # blueshades"#0971C9""ECE80F"   #yellowshades"#f8ba43"
        st.write("____")
        book1 = openpyxl.load_workbook(uploaded_file[0])
        qtr1_pnl, df1 = fundamentals.get_tables(book1[fundamentals.tabs[-1]], uploaded_file[0])  # send a sheet(not whole workbook)
        book2 = openpyxl.load_workbook(uploaded_file[1])
        qtr2_pnl, df2 = fundamentals.get_tables(book2[fundamentals.tabs[-1]], uploaded_file[1])  # send a sheet(not whole workbook)
        book1 = openpyxl.load_workbook(uploaded_file[0])

        qtr1_pnl, df1 = fundamentals.get_tables(book1[fundamentals.tabs[-1]], uploaded_file[0])  # send a sheet(not whole workbook)
        book2 = openpyxl.load_workbook(uploaded_file[1])
        qtr2_pnl, df2 = fundamentals.get_tables(book2[fundamentals.tabs[-1]], uploaded_file[1])  # send a sheet(not whole workbook)
        main_menu = st.sidebar.selectbox("Chose", fundamentals.funda_keys)
        sub_menu = st.sidebar.selectbox("SubChose", list(df1.loc[main_menu].index))
        new_df = [df1.loc[main_menu].loc[sub_menu], df2.loc[main_menu].loc[sub_menu]]
        df_new = pd.concat(new_df, keys=[comp1_Name, comp2_Name], axis=1)
        fundamentals.peer_bar(df_new, sub_menu,comp1_Name,comp2_Name)
    if len(uploaded_file) >= 3:
        st.error("Please, upload only 2 excel files")

st.write("____")
st.write('made with :green_heart: to my Indian Stock Investors')


