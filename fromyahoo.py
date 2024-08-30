# THIS IS yfinance module
#https://aroussi.com/post/python-yahoo-finance
#https://pypi.org/project/yfinance/
#The top two gets all the info from yahoo site regarding the stock but only past data and also key information like fundamentals, split info, results calender and all

#but for LIVE price we need yahoo-fin module
# https://pypi.org/project/yahoo-fin/
#https://theautomatic.net/yahoo_fin-documentation/
import pprint
import pandas as pd
from yahoo_fin import stock_info
from yahoo_fin import news
import streamlit as st
import concurrent.futures

import requests
from bs4 import BeautifulSoup
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
statistics_XPATH = "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]"
statistics_valuation_table_XPATH = "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]"
statistics_shares = "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[2]/div/div[2]"

def getdriver():
    service = Service(executable_path=r'C://Users/sahaveer/PycharmProjects/chromedriver.exe')
    options = webdriver.ChromeOptions()
    #options.add_argument("user-data-dir=selenium")
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    # Initialize the Chrome driver
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Edge(r"C://Users/sahaveer/PycharmProjects/msedgedriver.exe", )
    return driver

def analysts(script):
    try:
        analysts_info = stock_info.get_analysts_info(script+".bo")
        return analysts_info
    except:
        analysts_info = stock_info.get_analysts_info(script + ".ns")
        return analysts_info

def company_info(script):
    try:
        comp_info = stock_info.get_company_info(script+".bo")
        return comp_info
    except:
        comp_info = stock_info.get_company_info(script + ".ns")
        return comp_info

def promoters(script):
    try:
        prom = stock_info.get_holders(script+"ns")
        return prom
    except:
        prom = stock_info.get_holders(script + "bo")
        return prom

def next_earnings(script):
    try:
        next_date_earnings= stock_info.get_next_earnings_date(script+"bo")
        return next_date_earnings
    except:
        next_date_earnings= stock_info.get_next_earnings_date(script+"ns")
        return next_date_earnings

def quote_table(script):
    try:
        quote_tab = stock_info.get_quote_table(script+".bo")
        return quote_tab
    except:
        quote_tab = stock_info.get_quote_table(script+".ns")
        return quote_tab

def stats_stock(script):
    try:
        quote_stats = stock_info.get_stats(script + ".bo")
        return quote_stats
    except:
        quote_stats = stock_info.get_stats(script + ".ns")
        return quote_stats

def valuations_stock(script):
    try:
        quote_valuation = stock_info.get_stats_valuation(script + ".bo")
        return quote_valuation
    except:
        quote_valuation = stock_info.get_stats_valuation(script + ".ns")
        return quote_stats


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

def soup_Statistics(script):
    headers = {
        'User-Agent': 'Your User Agent String',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    cookies = {
        'cookie_name': 'cookie_value'
    }
    script_in_url = script.upper() + ".BO"
    url = f"https://finance.yahoo.com/quote/{script_in_url}/key-statistics?p={script_in_url}"
    encoded_url = urllib.parse.quote(url, safe=':/?&=')
    # Make a GET request to fetch the webpage content
    response = requests.get(encoded_url, headers=headers, cookies=cookies)
    print(response.status_code)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find specific elements or tables you want to extract
        # For example, find a table with a specific class
        table = soup.find('table', {'class': "W(100%) Bdcl(c) "})

        # Process the table or extract information as needed
        if table:
            # Process or extract data from the table
            # For example, loop through rows and columns to extract data
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                # Process each column data or store it as needed
                print(columns)
        # Or extract other specific elements using BeautifulSoup's functions
        # For example:
        # specific_element = soup.find('div', {'id': 'specific_id'})
        # Extract data from specific_element
        else:
            print("There is no such table")
    else:
        print('Failed to fetch the webpage')


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


def statistics(driver,script):
    try:
        script_in_url = script.upper() + ".NS"
        url = f"https://finance.yahoo.com/quote/{script_in_url}/key-statistics?p={script_in_url}"
        driver.get(url)
        all_tables = driver.find_element(by=By.XPATH, value=statistics_XPATH).get_attribute('outerHTML')
        table_valuations = pd.read_html(driver.find_element(by=By.XPATH, value=statistics_valuation_table_XPATH).get_attribute('outerHTML'))
        table_shares = pd.read_html(driver.find_element(by=By.XPATH, value=statistics_shares).get_attribute('outerHTML'))
        return table_valuations,table_shares
    except:
        script_in_url = script.upper() + ".BO"
        url = f"https://finance.yahoo.com/quote/{script_in_url}/key-statistics?p={script_in_url}"
        driver.get(url)
        all_tables = driver.find_element(by=By.XPATH, value=statistics_XPATH).get_attribute('outerHTML')
        table_valuations = pd.read_html(driver.find_element(by=By.XPATH, value=statistics_valuation_table_XPATH).get_attribute('outerHTML'))
        table_shares = pd.read_html(driver.find_element(by=By.XPATH, value=statistics_shares).get_attribute('outerHTML'))
        return table_valuations,table_shares

def main():
    script = "COALINDIA"

    #driver = getdriver()
    #table_valuation, table_shares_info = statistics(driver,script)
    #print(table_valuation)
    #pprint.pprint(table_shares_info)

    #SOUP
    soup_Statistics(script)

    #print("ANALYSTS:")
    #pprint.pprint(analysts(script)['Earnings Estimate'])
    '''
        {'Earnings Estimate':   Earnings Estimate  Current Qtr. (Dec 2023)  Next Qtr. (Mar 2024)  Current Year (2024)  Next Year (2025)
    0   No. of Analysts                     3.00                  3.00                26.00             26.00
    1     Avg. Estimate                     2.59                  5.63                12.27             13.78
    2      Low Estimate                     0.68                  4.00                10.10             10.64
    3     High Estimate                     3.60                  8.40                16.30             18.27
    4      Year Ago EPS                     0.37                  0.92                 8.04             12.27, 'Revenue Estimate':           Revenue Estimate Current Qtr. (Dec 2023) Next Qtr. (Mar 2024) Current Year (2024) Next Year (2025)
    0          No. of Analysts                       3                    3                  26               26
    1            Avg. Estimate                 346.33B              355.37B               1.34T            1.32T
    2             Low Estimate                 340.58B              335.68B               1.04T          835.51B
    3            High Estimate                 354.64B              382.61B               1.62T            1.83T
    4           Year Ago Sales                  353.8B              328.58B               1.44T            1.34T
    5  Sales Growth (year/est)                  -2.10%                8.20%              -7.10%           -1.40%, 'Earnings History':   Earnings History 12/31/2022 3/31/2023 6/30/2023 9/30/2023
    0         EPS Est.       2.27       1.7       5.1      3.32
    1       EPS Actual       0.37      0.92      2.15      3.66
    2       Difference       -1.9     -0.78     -2.95      0.34
    3       Surprise %    -83.70%   -45.90%   -57.80%    10.20%, 'EPS Trend':           EPS Trend  Current Qtr. (Dec 2023)  Next Qtr. (Mar 2024)  Current Year (2024)  Next Year (2025)
    0  Current Estimate                     2.59                  5.63                12.27             13.78
    1        7 Days Ago                     2.59                  5.63                12.27             13.78
    2       30 Days Ago                     2.09                  6.45                13.76             14.92
    3       60 Days Ago                     2.09                  6.45                13.21             14.74
    4       90 Days Ago                     2.09                  6.45                13.18             14.75, 'EPS Revisions':        EPS Revisions  Current Qtr. (Dec 2023)  Next Qtr. (Mar 2024)  Current Year (2024)  Next Year (2025)
    0     Up Last 7 Days                      NaN                   NaN                  NaN               NaN
    1    Up Last 30 Days                      NaN                   NaN                  8.0              11.0
    2   Down Last 7 Days                      NaN                   NaN                  NaN               NaN
    3  Down Last 30 Days                      NaN                   NaN                  NaN               NaN, 'Growth Estimates':            Growth Estimates  GAIL.NS  Industry  Sector(s)  S&P 500
    0              Current Qtr.  600.00%       NaN        NaN      NaN
    1                 Next Qtr.  512.00%       NaN        NaN      NaN
    2              Current Year   52.60%       NaN        NaN      NaN
    3                 Next Year   12.30%       NaN        NaN      NaN
    4  Next 5 Years (per annum)    4.00%       NaN        NaN      NaN
    5  Past 5 Years (per annum)   -7.36%       NaN        NaN      NaN}
                               0        1
    0      Market Cap (intraday)  828.79B
    1           Enterprise Value  964.88B
    2               Trailing P/E    15.66
    3                Forward P/E      NaN
    4  PEG Ratio (5 yr expected)      NaN
    5          Price/Sales (ttm)     0.62
    6           Price/Book (mrq)     1.14
    7   Enterprise Value/Revenue     0.72
    8    Enterprise Value/EBITDA     9.30

    '''

    #print(company_info(script))             #ERROR

    #print(promoters(script))
    #{'Major Holders':          Symbol            Name  Last Price Industry / Category    Type Exchange       0  COALINDIA.NS  COAL INDIA LTD       331.8              Energy  Stocks      NSI}

    #print("************QUOTE TABLE************")
    #print(quote_table(script))

    #{'1y Target Est': nan, '52 Week Range': '88.05 - 132.45', 'Ask': '126.20 x 0', 'Avg. Volume': 890228.0,
    #'Beta (5Y Monthly)': 0.66, 'Bid': '126.10 x 0', "Day's Range": '125.45 - 127.25',
    # 'EPS (TTM)': 8.05,
    #'Earnings Date': 'Jan 29, 2024 - Feb 02, 2024', 'Ex-Dividend Date': 'Mar 21, 2023',
    #'Forward Dividend & Yield': '8.00 (6.35%)',
    # 'Market Cap': '828.791B',
    # 'Open': 126.5,
    # 'PE Ratio (TTM)': 15.66,
    #'Previous Close': 126.4, 'Quote Price': 126.05000305175781,
    # 'Volume': 508792.0}

    '''
    print("************STATS************")
    print(stats_stock(script))
    shares_outstanding = "Shares Outstanding 5"
    shares_float = "Float 8"
    shares_insider = "% Held by Insiders 1"
    shares_inst = "% Held by Institutions 1"
    attrib = "Attribute"
    val = "Value"
    #"50-Day Moving Average 3"
    #"200-Day Moving Average 3"
    #"Shares Outstanding 5"
    #"Float 8"
    #"% Held by Insiders 1"
    #"% Held by Institutions 1"
    '''
    '''
                                   Attribute         Value
    0                  Beta (5Y Monthly)          0.66
    1                   52-Week Change 3        40.29%
    2            S&P500 52-Week Change 3        10.52%
    3                     52 Week High 3        132.45
    4                      52 Week Low 3         88.05
    5            50-Day Moving Average 3        123.81
    6           200-Day Moving Average 3        110.33
    7                Avg Vol (3 month) 3       890.23k
    8                 Avg Vol (10 day) 3       711.34k
    9               Shares Outstanding 5         6.58B
    10      Implied Shares Outstanding 6         6.58B
    11                           Float 8         2.67B
    12              % Held by Insiders 1        58.98%
    13          % Held by Institutions 1        25.72%
    14                    Shares Short 4           NaN
    15                     Short Ratio 4           NaN
    16                Short % of Float 4           NaN
    17   Short % of Shares Outstanding 4           NaN
    18     Shares Short (prior month ) 4           NaN
    19    Forward Annual Dividend Rate 4             8
    20   Forward Annual Dividend Yield 4         6.35%
    21   Trailing Annual Dividend Rate 3          0.00
    22  Trailing Annual Dividend Yield 3         0.00%
    23   5 Year Average Dividend Yield 4          4.51
    24                    Payout Ratio 4        49.69%
    25                   Dividend Date 3           NaN
    26                Ex-Dividend Date 4  Mar 21, 2023
    27               Last Split Factor 2         1.5:1
    28                 Last Split Date 3  Sep 06, 2022
    29                  Fiscal Year Ends  Mar 31, 2023
    30         Most Recent Quarter (mrq)  Sep 30, 2023
    31                     Profit Margin         3.92%
    32            Operating Margin (ttm)         8.31%
    33            Return on Assets (ttm)         2.68%
    34            Return on Equity (ttm)         7.59%
    35                     Revenue (ttm)         1.35T
    36           Revenue Per Share (ttm)        205.04
    37    Quarterly Revenue Growth (yoy)       -14.70%
    38                Gross Profit (ttm)           NaN
    39                            EBITDA        73.06B
    40    Net Income Avi to Common (ttm)        52.84B
    41                 Diluted EPS (ttm)          8.05
    42   Quarterly Earnings Growth (yoy)        85.80%
    43                  Total Cash (mrq)        25.85B
    44        Total Cash Per Share (mrq)          3.93
    45                  Total Debt (mrq)       179.51B
    46           Total Debt/Equity (mrq)        24.58%
    47               Current Ratio (mrq)          0.96
    48        Book Value Per Share (mrq)        110.90
    49         Operating Cash Flow (ttm)        126.6B
    50      Levered Free Cash Flow (ttm)        -45.5B
    '''
    '''
    print(f"SCRIPT : {script}")
    print("***********VALUATIONS*************")
    #print(valuations_stock(script))
    print("************QUOTE TABLE************")
    print(f"EPS TTM : {quote_table(script)['EPS (TTM)']}")
    print(f"MarketCap : {quote_table(script)['Market Cap']}")
    print(f"PE TTM : {quote_table(script)['PE Ratio (TTM)']}")
    print("************STATS************")
    print(f"Shares Outstanding : {stats_stock(script).loc[shares_outstanding, val]}")
    print(f"Shares Floating : {stats_stock(script).loc[shares_float, val]}")
    print(f"Shares Insider : {stats_stock(script).loc[shares_insider, val]}")
    print(f"Shares Institutions : {stats_stock(script).loc[shares_inst, val]}")
    print("***********VALUATIONS*************")
    print(valuations_stock(script).loc["Trailing P/E","1"])
    #"Market Cap (intraday)"
    #"Trailing P/E"
    #"Forward P/E"
    '''

    '''
                                   0        1
    0      Market Cap (intraday)  828.79B
    1           Enterprise Value  964.88B
    2               Trailing P/E    15.66
    3                Forward P/E      NaN
    4  PEG Ratio (5 yr expected)      NaN
    5          Price/Sales (ttm)     0.62
    6           Price/Book (mrq)     1.14
    7   Enterprise Value/Revenue     0.72
    8    Enterprise Value/EBITDA     9.30
    '''

if __name__ == '__main__':
    main()