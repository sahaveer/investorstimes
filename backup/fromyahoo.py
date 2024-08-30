# THIS IS yfinance module
#https://aroussi.com/post/python-yahoo-finance
#https://pypi.org/project/yfinance/
#The top two gets all the info from yahoo site regarding the stock but only past data and also key information like fundamentals, split info, results calender and all

#but for LIVE price we need yahoo-fin module
# https://pypi.org/project/yahoo-fin/
#https://theautomatic.net/yahoo_fin-documentation/
from yahoo_fin import stock_info
from yahoo_fin import news
import streamlit as st
import concurrent.futures

def liveprice(script):
    def get_price(script):
        try:
            return stock_info.get_live_price(script)
        except Exception:
            return None  # Use None instead of 0 to indicate failure

    try:
        if script is None:
            return 0

        # Try ".bo" first
        price = get_price(script + ".bo")
        if price is not None:
            return round(price)

        # Try ".ns" if ".bo" fails
        price = get_price(script + ".ns")
        if price is not None:
            return round(price)

        # If both attempts fail, return 0
        return 0
    except Exception as e:
        return 0

'''
def liveprice(script):          # the INPUT should be .ns or .bo to get the live price
    try:
        st.info(f"Trying {script} to get :")
        if script is None :
            price = 0
        else:
            if len(script.split())>1:
                script1 = script.split(' ')[-1]
                script1 = script1 + ".bo"
                price = stock_info.get_live_price(script1)
            else :
                script1 = script + ".ns"
                #st.info(script)
                price = stock_info.get_live_price(script1)
        st.info(f"fOR {script1} : price is {price}")
        return price
    except Exception as e:
        st.error(f"Got exception as {e} for {script}")
        return 0

'''