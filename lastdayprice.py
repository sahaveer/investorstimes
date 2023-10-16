import csv
import os
import pandas as pd
import streamlit as st
# List all files in the directory
files = os.listdir('./')
# Filter files that start with 'EQ' or 'sec' and end with '.csv'
csv_files = [file for file in files if (file.startswith('EQ') or file.startswith('sec')) and (file.endswith('.csv') or file.endswith('.CSV'))]

code_price = pd.DataFrame()
for each in csv_files:
    #print(each)
    df = pd.read_csv('./' + each)
    #print(df.head())
    if each.startswith('EQ'):
        df = df[['SC_CODE', 'CLOSE']]
        df = df.rename(columns={'SC_CODE':'CODE'})
    else :
        df = df[['SYMBOL',' CLOSE_PRICE']]
        df = df.rename(columns={'SYMBOL':'CODE',' CLOSE_PRICE':'CLOSE'})
    code_price = pd.concat([code_price,df])
#print(code_price)


def getltp(code):
    try:
        df1 = code_price[code_price['CODE']==code]
        if not df1.empty:
            price = df1['CLOSE'].iloc[0]
            #st.info(f"Asked for {code}, the price is {price}")
            return price
        else:
            return 0
    except KeyError:
        return None

def main():
    ltp = getltp(500033)
    print(ltp)
if __name__ == '__main__':
    main()
#print(code_price.head())
#print(code_price.tail())


