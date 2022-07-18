import streamlit as st
import glob
import pandas as pd
import fundamentals

#st.set_page_config(page_title="ListedCharts",page_icon=":bar_chart:",layout="wide")
st.title('Listed Stocks 📈')
st.write("____")
listed_stocks = []
stocks_dict = {}

for each_pickl in glob.glob('./pickl/*.pkl',recursive=False):
    each_pickl = each_pickl.replace('\\','/')
    file_name_only = each_pickl.split('/')[-1]
    pickle_name = file_name_only.split('.pkl')[0]
    stocks_dict[pickle_name] = each_pickl
    listed_stocks += [pickle_name]

with st.sidebar:
    st.write(r"we have got now {} listed stocks data available".format(str(len(listed_stocks))))
    selected = st.selectbox("NSE Listed", listed_stocks)

if selected :
    df_comp = pd.read_pickle(stocks_dict[selected])
    try:
        df_comp.columns = df_comp.columns.strftime('%d-%m-%Y')
    except Exception as AttributeError:
        pass
    comp_Name = str(selected)
    col1, col2, col3 = st.columns([0.5, 0.4, 0.1])
    with col1:
        sub_choose = st.selectbox("Fundamentals", fundamentals.funda_keys)
    with col3:
        color_bar = st.color_picker("Bar", value="#ECE80F")   #blueshades"#0971C9""ECE80F"   #yellowshades"#f8ba43"

    if sub_choose == fundamentals.funda_keys[0]:
        with col2:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.selectbox("SubChose", index_list)
        if param == "key_params":
            with st.expander("YEARLY PROFIT & LOSS DATA"):
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
            fundamentals.qoq_growth(df_comp.loc[sub_choose], "SALES", color_bar, comp_Name)
            fundamentals.group_2_bars(df_comp.loc[sub_choose], "PROFIT BEFORE TAX", "NET PROFIT", comp_Name)
        else:
            if st.checkbox("Sequential_Growth_%"):
                fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar, comp_Name)
            else:
                fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar, comp_Name)

    if sub_choose == fundamentals.funda_keys[1]:
        with col2:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.selectbox("SubChose", index_list)
        if param == "key_params":
            with st.expander("YEARLY BALANCE SHEET DATA"):
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
    if sub_choose == fundamentals.funda_keys[2]:
        with col2:
            index_list = ["key_params"] + list(df_comp.loc[sub_choose].index)
            param = st.selectbox("SubChose", index_list)
        if param == "key_params":
            with st.expander("YEARLY CASH FLOWS DATA"):
                st.dataframe(df_comp.loc[sub_choose].style.format(formatter="{:.1f}"))
            fundamentals.go_group_bar(df_comp.loc[sub_choose], "cash_flows", color_bar)
        else:
            if st.checkbox("Sequential_Growth_%"):
                fundamentals.qoq_growth(df_comp.loc[sub_choose], param, color_bar, comp_Name)
            else:
                fundamentals.go_bar(df_comp.loc[sub_choose], param, color_bar, comp_Name)

st.write("____")
st.write('made with :green_heart: to Indian Stock Investors')
