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

st.set_page_config(page_title="InteractiveCharts",page_icon=":bar_chart:",layout="wide")
st.title('Excel Plotter 📈')
st.subheader('Upload your Excel file and have fun')

tabs = ['Profit & Loss', 'Quarters','Balance Sheet', 'Cash Flow' ,'Data Sheet']
table = ['PROFIT & LOSS', 'Quarters', 'BALANCE SHEET' ]
# lets define the first and last table keys to extract the exact table size
DataSheet_Key_Values = ['PROFIT & LOSS', 'Dividend Amount', 'Quarters', 'Operating Profit', 'BALANCE SHEET', 'Cash & Bank',
                        'CASH FLOW:', 'Net Cash Flow']

results_saved_at = 'C:/Users/sahaveer/OneDrive/Documents/bhavcopy/'
xlsx_to_read = 'Cravatex'
type_of_file_chart = '.xlsx'
#color_hover = "#0D7292"
#color_background = "#32B7D6"
color_hover = "darkgrey"
color_background = "grey"
def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)

def go_bar(df, row_name,color_bar,color_line,comp):
    #fig = ff.create_table(df)
    #st.plotly_chart(fig)
    #st.write(df)                                                   # this is givng data conversion error sometimes
    fig = go.Figure(data = [go.Bar(x = df.columns,y = df.loc[row_name],
                                   text = df.loc[row_name], textposition = 'auto')])
    # go.bar has another attribute - hovertext = ['27% market share', '24% market share', '19% market share']
    fig.update_traces(marker_color=color_bar, marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=1, texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(height=600,width=900,
                      title={'text': "<b>" + comp_Name.upper() + "</b> : <i>" + row_name + ' Report</i>',
                             'y': 0.9,'x': 0.5,'xanchor': 'center','yanchor': 'bottom'},
                      xaxis_tickfont_size=14, xaxis_tickangle=-45,
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False, title='INR (cr)',titlefont_size=16,tickfont_size=14,),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      bargap=0.15)     #legend=dict(x=0,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)'),
    st.markdown("---")
    st.plotly_chart(fig)
    #st.subheader('Downloads:')
    #generate_html_download_link(fig)

def go_bar_line(df,row_name,color_bar,color_line):
    temp_df = df.loc[row_name]
    df_sales_qoq = (temp_df.pct_change() * 100)
    df_sales_qoq.name = row_name + '_QoQ'
    df2 = df.append(df_sales_qoq)
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace( go.Bar(x=df2.columns, y=df2.loc[row_name], name=row_name, textposition = 'auto',text = df.loc[row_name]),
                   secondary_y=False)
    fig.update_traces(marker_color=color_bar, marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=1, texttemplate='%{text:.2s}', textposition='outside')
    fig.add_trace( go.Scatter(x=df2.columns, y=df2.iloc[-1], name=row_name + " QoQ", text = df.iloc[-1]),
                   secondary_y=True)
    # Add figure title
    fig.update_layout( height=600, width=900,
                       title={'text': "<b>" + comp_Name.upper() + "</b> : <i>" + row_name + ' Report</i>',
                              'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                       xaxis_tickfont_size=14, xaxis_tickangle=-45,
                       yaxis=dict(title='INR (cr)', titlefont_size=16, tickfont_size=14,),
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                       bargap=0.15)#legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),bargap = 0.15)
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>" + row_name + "</b> in cr ", secondary_y=False,showgrid=False)
    fig.update_yaxes(title_text="<b>" + row_name + " QoQ</b> in % ", secondary_y=True,showgrid=False)
    st.markdown("---")
    st.plotly_chart(fig)

    #st.subheader('Downloads:')
    #generate_excel_download_link(df2)
    #generate_html_download_link(fig)

def go_group_bar(df, row_name,color_bar,color_line):
    bar_list = list(df.index)
    fig = go.Figure(data=[ go.Bar(name=bar_list[0], x=df.columns, y=df.iloc[0], textposition = 'auto', text = df.iloc[0]),
                           go.Bar(name=bar_list[1],  x=df.columns, y=df.iloc[1], textposition = 'auto', text = df.iloc[1]),
                           go.Bar(name=bar_list[2], x=df.columns, y=df.iloc[2], textposition='auto', text=df.iloc[2]),
                           go.Bar(name=bar_list[3], x=df.columns, y=df.iloc[3], textposition='auto', text=df.iloc[3])
                           ])
    # Change the bar mode
    fig.update_layout(barmode='group', bargroupgap=0.1,
                      height=600, width=900,
                      title={'text': row_name + ' Report',
                             'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      xaxis_tickfont_size=14, xaxis_tickangle=-45,
                      yaxis=dict(title='INR (cr)', titlefont_size=16, tickfont_size=14, ),
                      legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),)   # this barmode = 'group | stack | 'relative''
    #fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'}) # WHILE USING STACK
    st.plotly_chart(fig)

def get_tables(datasht,file):
    for i in range(1,datasht.max_row+1) :
        if datasht['A'+str(i)].value == DataSheet_Key_Values[0] :
            pnl_start_row = i
        if datasht['A' + str(i)].value == DataSheet_Key_Values[1]:
            pnl_end_row = i-1
        if datasht['A' + str(i)].value == DataSheet_Key_Values[2]:
            quarterly_start_row = i
        if datasht['A' + str(i)].value == DataSheet_Key_Values[3]:
            quarterly_end_row = i-1
        if datasht['A' + str(i)].value == DataSheet_Key_Values[4]:
            BS_start_row = i
        if datasht['A' + str(i)].value == DataSheet_Key_Values[5]:
            BS_end_row = i-1
        if datasht['A' + str(i)].value == DataSheet_Key_Values[6]:
            cash_start_row = i
        if datasht['A' + str(i)].value == DataSheet_Key_Values[7]:
            cash_end_row = i-1
    reqd_cols = "A :" + str(get_column_letter(datasht.max_column))

    if pnl_start_row is not None and pnl_end_row is not None :
        pnl = pd.read_excel(file, index_col=0, sheet_name=tabs[-1], header=pnl_start_row,usecols=reqd_cols,
                            nrows=pnl_end_row-pnl_start_row )
    if quarterly_start_row is not None and quarterly_end_row is not None :
        qtr_pnl = pd.read_excel(file, index_col=0, sheet_name=tabs[-1], header=quarterly_start_row, usecols=reqd_cols,
                                nrows=quarterly_end_row - quarterly_start_row)
    if BS_start_row is not None and BS_end_row is not None:
        balancesht = pd.read_excel(file, index_col=0, sheet_name=tabs[-1], header=BS_start_row,usecols=reqd_cols,
                                   nrows=BS_end_row-BS_start_row )
    if cash_start_row is not None and cash_end_row is not None:
        cashflow = pd.read_excel(file, index_col=0, sheet_name=tabs[-1], header=cash_start_row,usecols=reqd_cols,
                                   nrows=cash_end_row-cash_start_row )
    return pnl,qtr_pnl, balancesht,cashflow



with st.sidebar:
    st.markdown(""" <style> .font {
    font-size:22px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    # Add a file uploader to allow users to upload their csv file
    st.markdown('<p class="font">Upload your xlsx/xlsm from screener.in </p>',
                unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=['xlsx', 'xlsm'])  # Only accepts xlsx,xlsm file format

if uploaded_file is not None:
    comp_Name = uploaded_file.name.split('.')[0]
    book = openpyxl.load_workbook(uploaded_file)
    pnl, qtr_pnl, balance_sht, cash_flow = get_tables(book[tabs[-1]], uploaded_file)  # send a sheet(not whole workbook)
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        sub_choose = option_menu("Fundamentals", ["Yearly PnL", "Quarterly PnL", "Balance Sheet", "Cash Flow"],
                                 styles={"container": {"padding": "5!important"},
                                         "icon": {"color": "yellow", "font-size": "18px"},
                                         "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                      "--hover-color": color_hover},
                                         "nav-link-selected": {"background-color": color_background}},
                                 menu_icon="cast", default_index=0, orientation="horizontal")
        with col2:
            color_bar = st.color_picker("Bar", value="#0f7eec")
            color_line = st.color_picker("Line", value="#D60A10")
    if sub_choose == "Yearly PnL":
        index_list = ["key_params"] + list(pnl.index)
        # param = st.selectbox("Select  column", pnl.index)
        with st.sidebar:
            param = option_menu(sub_choose, index_list,
                                styles={"container": {"padding": "5!important"},
                                        "icon": {"color": "orange", "font-size": "25px"},
                                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                     "--hover-color": color_hover},
                                        "nav-link-selected": {"background-color": color_background}},
                                menu_icon="cast", default_index=0, orientation="vertical")
        if param == "key_params":
            go_bar_line(pnl, "Sales", color_bar, color_line)
            go_bar_line(pnl, "Profit before tax", color_bar, color_line)
            go_bar_line(pnl, "Net profit", color_bar, color_line)
        else:
            if st.checkbox("Sequential_Growth_%"):
                go_bar_line(pnl, param, color_bar, color_line)
            else:
                go_bar(pnl, param, color_bar, color_line,comp_Name)

    if sub_choose == "Quarterly PnL":
        # param = st.selectbox("Select  column", qtr_pnl.index)
        index_list = ["key_params"] + list(qtr_pnl.index)
        with st.sidebar:
            param = option_menu(sub_choose, index_list,
                                styles={"container": {"padding": "5!important"},
                                        "icon": {"color": "orange", "font-size": "25px"},
                                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                     "--hover-color": color_hover},
                                        "nav-link-selected": {"background-color": color_background}},
                                menu_icon="cast", default_index=0, orientation="vertical")
        if param == "key_params":
            go_bar_line(qtr_pnl, "Sales", color_bar, color_line)
            go_bar_line(qtr_pnl, "Profit before tax", color_bar, color_line)
            go_bar_line(qtr_pnl, "Net profit", color_bar, color_line)
        else:
            if st.checkbox("Sequential_Growth_%"):
                go_bar_line(qtr_pnl, param, color_bar, color_line)
            else:
                go_bar(qtr_pnl, param, color_bar, color_line,comp_Name)

    if sub_choose == "Balance Sheet":
        # param = st.selectbox("Select  column", balance_sht.index)
        index_list = ["key_params"] + list(balance_sht.index)
        with st.sidebar:
            param = option_menu(sub_choose, index_list,
                                styles={"container": {"padding": "5!important"},
                                        "icon": {"color": "orange", "font-size": "25px"},
                                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                     "--hover-color": color_hover},
                                        "nav-link-selected": {"background-color": color_background}},
                                menu_icon="cast", default_index=0, orientation="vertical")
        if param == "key_params":
            go_bar_line(balance_sht, "Reserves", color_bar, color_line)
            go_bar_line(balance_sht, "Borrowings", color_bar, color_line)
            go_bar_line(balance_sht, "Capital Work in Progress", color_bar, color_line)
            go_bar_line(balance_sht, "Cash & Bank", color_bar, color_line)
        else:
            if st.checkbox("Sequential_Growth_%"):
                go_bar_line(balance_sht, param, color_bar, color_line)
            else:
                go_bar(balance_sht, param, color_bar, color_line,comp_Name)
    if sub_choose == "Cash Flow":
        index_list = ["key_params"] + list(cash_flow.index)
        # param = st.selectbox("Select  column", cash_flow.index)
        with st.sidebar:
            param = option_menu(sub_choose, index_list,
                                styles={"container": {"padding": "5!important"},
                                        "icon": {"color": "orange", "font-size": "25px"},
                                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                     "--hover-color": color_hover},
                                        "nav-link-selected": {"background-color": color_background}},
                                menu_icon="cast", default_index=0, orientation="vertical")
        if param == "key_params":
            go_group_bar(cash_flow, "cash_flows", color_bar, color_line)
        else:
            if st.checkbox("Sequential_Growth_%"):
                go_bar_line(cash_flow, param, color_bar, color_line)
            else:
                go_bar(cash_flow, param, color_bar, color_line,comp_Name)



#Custom CSS to remove header,footer, hamburger icon
hide_st_style = """
                <style>
                MainMenu {visibility: hidden;} 
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)