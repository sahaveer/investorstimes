import streamlit as st
import glob
import pandas as pd
import fundamentals

#st.set_page_config(page_title="ListedCharts",page_icon=":bar_chart:",layout="wide")
st.title('Listed Stocks 📈')
listed_stocks = []
stocks_dict = {}

for each_pickl in glob.glob('./pickl/*.pkl',recursive=False):
    each_pickl = each_pickl.replace('\\','/')
    file_name_only = each_pickl.split('/')[-1]
    pickle_name = file_name_only.split('.')[0]
    stocks_dict[pickle_name] = each_pickl
    listed_stocks += [pickle_name]

with st.sidebar:
    selected = st.selectbox("NSE Listed", listed_stocks)

if selected :
    df_comp = pd.read_pickle(stocks_dict[selected])
    comp_Name = str(selected)
    col1, col2, col3 = st.columns([0.5, 0.4, 0.1])
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
            # sns_bar(df_comp.loc[funda_menu[0]], "Sales", color_bar,comp_Name)
            fundamentals.qoq_growth(df_comp.loc[sub_choose], "SALES", color_bar, comp_Name)
            fundamentals.group_2_bars(df_comp.loc[sub_choose], "PROFIT BEFORE TAX", "NET PROFIT", comp_Name)
        else:
            if st.checkbox("Sequential_Growth_%"):
                fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar, comp_Name)
            else:
                fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar, comp_Name)
    if sub_choose == fundamentals.funda_menu[3]:
        with col2:
            index_list = ["key_params"] + list(qtr_pnl.index)
            param = st.selectbox("SubChose", index_list)
        if param == "key_params":
            st.dataframe(qtr_pnl.style.format(formatter="{:.1f}"))
            fundamentals.qoq_growth(qtr_pnl, "SALES", color_bar, comp_Name)
            fundamentals.group_2_bars(qtr_pnl, "PROFIT BEFORE TAX", "NET PROFIT", comp_Name)
            fundamentals.qoq_growth(qtr_pnl, "PROFIT BEFORE TAX", color_bar, comp_Name)
            fundamentals.qoq_growth(qtr_pnl, "NET PROFIT", color_bar, comp_Name)
        else:
            if st.checkbox("Sequential_Growth_%"):
                fundamentals.qoq_growth(qtr_pnl, param, color_bar, comp_Name)
            else:
                fundamentals.go_bar(qtr_pnl, param, color_bar, comp_Name)

    if sub_choose == fundamentals.funda_menu[1]:
        with col2:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.selectbox("SubChose", index_list)
        if param == "key_params":
            st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
            fundamentals.bar_line(df_comp.loc[sub_choose], "RESERVES", "BORROWINGS", color_bar, comp_Name)
            fundamentals.bar_line(df_comp.loc[sub_choose], "RECEIVABLES", "INVENTORY", color_bar, comp_Name)
            fundamentals.go_bar(df_comp.loc[sub_choose], "CAPITAL WORK IN PROGRESS", color_bar, comp_Name)
            fundamentals.go_bar(df_comp.loc[sub_choose], "CASH & BANK", color_bar, comp_Name)
        else:
            if st.checkbox("Sequential_Growth_%"):
                fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar, comp_Name)
            else:
                fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar, comp_Name)
    if sub_choose == fundamentals.funda_menu[2]:
        with col2:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.selectbox("SubChose", index_list)
        if param == "key_params":
            st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
            fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_bar)
        else:
            if st.checkbox("Sequential_Growth_%"):
                fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar, comp_Name)
            else:
                fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar, comp_Name)



