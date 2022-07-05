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

#st.set_page_config(page_title="InteractiveCharts",page_icon=":bar_chart:",layout="wide")
st.title('Excel Plotter 📈')
st.write("____")

with st.sidebar:
    st.markdown(""" <style> .font {
    font-size:22px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    # Add a file uploader to allow users to upload their csv file
    st.markdown('<p class="font">Upload One or Two xlsx/xlsm FILES from screener.in </p>',
                unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['xlsx', 'xlsm'],accept_multiple_files = True)  # Only accepts xlsx,xlsm file format

if uploaded_file is not None:
    if len(uploaded_file)==1:
        comp_Name = uploaded_file[0].name.split('.')[0]
        book = openpyxl.load_workbook(uploaded_file[0])
        qtr_pnl,df_comp = fundamentals.get_tables(book[fundamentals.tabs[-1]], uploaded_file[0])  # send a sheet(not whole workbook)
        # **************************************************************************************************
        if os.path.isdir('./pickl'):
            df_comp.to_pickle("./pickl/"+comp_Name + ".pkl")
        col1, col2,col3 = st.columns([0.5, 0.4, 0.1])
        with col1:
            sub_choose = st.selectbox("Fundamentals", fundamentals.funda_menu)
        with col3:
            color_bar = st.color_picker("Bar", value="#0f7eec")

        if sub_choose == fundamentals.funda_menu[0]:
            with col2:
                index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                #sns_bar(df_comp.loc[funda_menu[0]], "Sales", color_bar,comp_Name)
                fundamentals.qoq_growth(df_comp.loc[sub_choose], "SALES", color_bar,comp_Name)
                fundamentals.group_2_bars(df_comp.loc[sub_choose],"PROFIT BEFORE TAX","NET PROFIT",comp_Name)
            else:
                if st.checkbox("Sequential_Growth_%"):
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar,comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar,comp_Name)
        if sub_choose == fundamentals.funda_menu[3]:
            with col2:
                index_list = ["key_params"] + list(qtr_pnl.index)
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                st.dataframe(qtr_pnl.style.format(formatter="{:.1f}"))
                fundamentals.qoq_growth(qtr_pnl, "SALES", color_bar,comp_Name)
                fundamentals.group_2_bars(qtr_pnl, "PROFIT BEFORE TAX","NET PROFIT",comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "PROFIT BEFORE TAX", color_bar,comp_Name)
                fundamentals.qoq_growth(qtr_pnl, "NET PROFIT", color_bar,comp_Name)
            else:
                if st.checkbox("Sequential_Growth_%"):
                    fundamentals.qoq_growth(qtr_pnl, param, color_bar,comp_Name)
                else:
                    fundamentals.go_bar(qtr_pnl, param, color_bar,comp_Name)
    
        if sub_choose == fundamentals.funda_menu[1]:
            with col2:
                index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.bar_line(df_comp.loc[sub_choose],"RESERVES","BORROWINGS",color_bar,comp_Name)
                fundamentals.bar_line(df_comp.loc[sub_choose],"RECEIVABLES","INVENTORY",color_bar,comp_Name)
                fundamentals.go_bar(df_comp.loc[sub_choose], "CAPITAL WORK IN PROGRESS", color_bar,comp_Name)
                fundamentals.go_bar(df_comp.loc[sub_choose], "CASH & BANK", color_bar,comp_Name)
            else:
                if st.checkbox("Sequential_Growth_%"):
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar,comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar,comp_Name)
        if sub_choose == fundamentals.funda_menu[2]:
            with col2:
                index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
                param = st.selectbox("SubChose", index_list)
            if param == "key_params":
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
                fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_bar)
            else:
                if st.checkbox("Sequential_Growth_%"):
                    fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar,comp_Name)
                else:
                    fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar, comp_Name)
    if len(uploaded_file)==2:
        book1 = openpyxl.load_workbook(uploaded_file[0])
        qtr1_pnl, df1 = fundamentals.get_tables(book1[fundamentals.tabs[-1]], uploaded_file[0])  # send a sheet(not whole workbook)
        book2 = openpyxl.load_workbook(uploaded_file[1])
        qtr2_pnl, df2 = fundamentals.get_tables(book2[fundamentals.tabs[-1]], uploaded_file[1])  # send a sheet(not whole workbook)
        comp1_Name = uploaded_file[0].name.split('.')[0]
        comp2_Name = uploaded_file[1].name.split('.')[0]
        book1 = openpyxl.load_workbook(uploaded_file[0])
        qtr1_pnl, df1 = fundamentals.get_tables(book1[fundamentals.tabs[-1]], uploaded_file[0])  # send a sheet(not whole workbook)
        book2 = openpyxl.load_workbook(uploaded_file[1])
        qtr2_pnl, df2 = fundamentals.get_tables(book2[fundamentals.tabs[-1]], uploaded_file[1])  # send a sheet(not whole workbook)
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            main_menu = st.selectbox("Chose", fundamentals.funda_keys)
        with col2:
            sub_menu = st.selectbox("SubChose", list(df1.loc[main_menu].index))
        new_df = [df1.loc[main_menu].loc[sub_menu], df2.loc[main_menu].loc[sub_menu]]
        df_new = pd.concat(new_df, keys=[comp1_Name, comp2_Name], axis=1)
        fundamentals.peer_bar(df_new, sub_menu)
        st.dataframe(df_new)
    if len(uploaded_file) >= 3:
        st.error("Please, upload only 2 excel files")

st.write("____")
st.write('made with :green_heart: to Indian Stock Investors')
#Custom CSS to remove header,footer, hamburger icon
hide_st_style = """
                <style>
                MainMenu {visibility: hidden;} 
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)