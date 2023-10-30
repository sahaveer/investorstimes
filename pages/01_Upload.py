import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import openpyxl
from openpyxl.utils import get_column_letter
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
import os
import fundamentals
import json
from streamlit_lottie import st_lottie
import nse_bse_search


st.set_page_config(page_title="Upload", page_icon=":bar_chart:", layout="wide",initial_sidebar_state="expanded",)
st.title('Upload _Excel file_ from [***SCREENER***]({https://www.screener.in/}) ')
#color_dict = {'Yellow_Lite':"#f8ba43",'Yellow_Dark':"#D6D41B",'Blue_Lite':"#1959BF",'Blue_Dark':"#0971C9",'Green_Lite':"#11A694",'Green_Dark':"#11A64B","Purple_Lite":"#7019BF",'Purple_Dark':"#9319BF"}
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

uploaded_file = st.file_uploader("", type=['xlsx', 'xlsm'],
                                 accept_multiple_files=True)  # Only accepts xlsx,xlsm file format
st.markdown('<p class="font">Upload One or Two xlsx/xlsm FILES from screener.in </p>',
            unsafe_allow_html=True)


#color_list = ["#D6D41B","#f8ba43","#0971C9","#1959BF","#11A694","#11A64B","#7019BF","#9319BF"]
# Define a custom function to apply the condition
def OPM(row):
    if row['OPERATING PROFIT'] > 0:
        return round((row['OPERATING PROFIT'] / row['SALES'])*100,2)
    else:
        return 0

def NPM(row):
    if row['NET PROFIT'] > 0:
        return round((row['NET PROFIT'] / row['SALES'])*100,2)
    else:
        return 0
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
        #pnl, balancesht, qtr_pnl = fundamentals.develop_data(qtr_pnl, df_comp)
        pnl, balancesht = fundamentals.develop_yearly(df_comp)
        qtr_pnl = fundamentals.develop_quarterly(qtr_pnl)
        try:
            df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
        except Exception as AttributeError:
            pass
        try:
            qtr_pnl.columns = qtr_pnl.columns.strftime('%d-%m-%Y')
        except Exception as AttributeError:
            pass
        # **************************************************************************************************
        with col2:
            sub_choose = st.selectbox("Fundamentals", fundamentals.funda_menu)
        if sub_choose == fundamentals.funda_menu[0]:            # YEARLY PNL
            index_list = ["key_params"] + list(pnl.index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("YEARLY PROFIT & LOSS DATA"):
                    st.dataframe(pnl.style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(pnl, "SALES", color_dict[color_key]['hash'],comp_Name)
                fundamentals.group_2_bars(pnl,"PROFIT BEFORE TAX","NET PROFIT",comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(pnl, param, color_dict[color_key]['hash'],comp_Name)
                else:
                    fundamentals.go_bar(pnl, param, color_dict[color_key]['hash'],comp_Name)
        if sub_choose == fundamentals.funda_menu[3]:                #QUARTERLY PNL
            index_list = ["key_params"] + list(qtr_pnl.index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("QUARTERLY PROFIT & LOSS DATA"):
                    st.dataframe(qtr_pnl.style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(qtr_pnl, "SALES", color_dict[color_key]['hash'],comp_Name)
                fundamentals.group_2_bars(qtr_pnl, "PROFIT BEFORE TAX","NET PROFIT",comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "PROFIT BEFORE TAX", color_dict[color_key]['hash'],comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "NET PROFIT", color_dict[color_key]['hash'],comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(qtr_pnl, param, color_dict[color_key]['hash'],comp_Name)
                else:
                    fundamentals.go_bar(qtr_pnl, param, color_dict[color_key]['hash'],comp_Name)
    
        if sub_choose == fundamentals.funda_menu[1]:        #YEARLY BALANCE SHEET
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("YEARLY BALANCE SHEET DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.bar_line(df_comp.loc[sub_choose],"RESERVES","BORROWINGS",color_dict[color_key]['hash'],comp_Name)
                fundamentals.bar_line(df_comp.loc[sub_choose],"RECEIVABLES","INVENTORY",color_dict[color_key]['hash'],comp_Name)
                fundamentals.go_bar(df_comp.loc[sub_choose], "CAPITAL WORK IN PROGRESS", color_dict[color_key]['hash'],comp_Name)
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH & BANK", color_dict[color_key]['hash'],comp_Name)
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key]['hash'],comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key]['hash'],comp_Name)
        if sub_choose == fundamentals.funda_menu[2]:        # YEARLY CASH FLOWS
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            with col3:
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                with st.expander("YEARLY CASH FLOWS DATA"):
                    st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_dict[color_key]['hash'])
            else:
                with col4:
                    qoq_checked = st.checkbox("Sequential_Growth_%")
                if qoq_checked:
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_dict[color_key]['hash'],comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_dict[color_key]['hash'], comp_Name)
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


