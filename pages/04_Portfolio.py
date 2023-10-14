import csv
import numpy as np
import pandas as pd
import streamlit as st
import nse_bse_search

st.title('Visualise your Portfolio')
tradebook = st.file_uploader("upload TradeBook from Zerodha", type= ['xlsx'])
#loc = "./TRADEBOOK.xlsx"
if tradebook is not None:
    xl = pd.read_excel(tradebook,parse_dates=['Trade Date'])
    xl = xl.dropna(axis=1)
    rows_list = []
    show_only = {}
    show_only['Symbol'] = []
    show_only['Quantity'] = []
    show_only['Price'] = []
    symb_dict = {}

    # DEFINING the dataframes ENDRESULT - its column names
    open_pf = pd.DataFrame(columns=['ISIN','Trade Date', 'Trade Type', 'Quantity', 'avg_price'])  # EMPTY DF
    closed_pf = pd.DataFrame({'ISIN' : [] ,'Buy Date': [], 'Sell Date': [], 'Quantity': [], 'Buy Price': [], 'Sell Price': [], 'PnL': []})
    only_sell_pf = pd.DataFrame(columns=['ISIN','Trade Date', 'Trade Type', 'Quantity', 'avg_price'])
    sold_data = []
    buy_queue = []  # to save all buy transactions temporarily, {} values in a list
    symbol_isin = {}

    # NOW LETS GROUP EVERY DF BY 'ISIN' instead of 'SYMBOL'
    for each in xl['ISIN'].unique():
        #phase-1
        # get the first group of SCRIPT
        xl_symbol = xl.groupby("ISIN").get_group(each)
        df_grouped = xl_symbol[["Symbol","ISIN", "Trade Date", "Trade Type", "Quantity", "Price"]].set_index("ISIN")
        #print(df_grouped)
        symbol_isin[each] = (df_grouped['Symbol'].iloc[0])
        #print(symbol_isin)

        #phase-2      All transactions per each day into one
        # CALCULATE THE TRADE VAL and then sums up the BUYS/SELLS which happened on the same DATES
        df_grouped['Investment'] = df_grouped['Quantity'] * df_grouped['Price']

        temp_df_grouped = df_grouped.groupby(["ISIN", "Trade Date", "Trade Type"])[['Quantity', 'Investment']].sum()  # .reset_index()
        # temp_df_grouped = pd.DataFrame(df_grouped).groupby(["Symbol","Trade Date","Trade Type"]).aggregate({'Quantity':'sum','Investment':sum})
        temp_df_grouped["avg_price"] = temp_df_grouped["Investment"] / temp_df_grouped["Quantity"]

        new_df = (temp_df_grouped.sort_values('Trade Date', ascending=True))
        # converts the multiline index to normal DF
        grouped_df = new_df.reset_index()
        grouped_df.drop("Investment", axis=1, inplace=True)
        #GROUPED_DF gives us so that all dates are combined to one and for each stock
        # SO, WE DID GROUPED AND THEN COMBINED DAY's SEVERAL ORDER FILLS
        # NOW, LETS work to get two Dataframes, one is SOLD_DF which keeps a record of closed orders
        # Second DF is the final OPEN positions which will be saved in open_pf : represents current portfolio

        buy_queue = []
        remaining_sell_quantity = 0
        # we will try to get 2 seperate dataframes from the grouped_df : 1 is sold_df and one is current_df
        for index, row in grouped_df.iterrows():
            if (grouped_df['Trade Type'] == 'sell').all() or grouped_df['Trade Type'].iloc[0] == 'sell':
                only_sell_pf = pd.concat([only_sell_pf,grouped_df],ignore_index=True)
            else:  # ensure the first row trate_type is not "sell" and the entire grouped df doesnt have only sell orders
                trade_date, trade_type, quantity, avg_price = row['Trade Date'], row['Trade Type'], row['Quantity'], row['avg_price']
                if trade_type == 'buy':
                    # Add 'buy' transactions to the queue
                    buy_queue.append(
                        {'ISIN': each, 'Trade Date': trade_date, 'Trade Type': trade_type, 'Quantity': quantity,
                         'avg_price': avg_price})
                    # print(" ADDING BUY in THE QUEUE : ")
                    # print(buy_queue)
                elif trade_type == 'sell':
                    # Process 'sell' transactions
                    remaining_sell_quantity = quantity
                    i = 0  # whenever sell comes, it shud start from the first index of buy_queue
                    # Check if there are 'buy' transactions in the queue to offset the 'sell' quantity
                    while remaining_sell_quantity > 0 and (buy_queue):
                        # get data from queue
                        # print("$$$$$$$$$$ PICKING THE FIRST QUEUE IS : $$$$$$$$$$$$$$$")
                        # print(buy_queue[0])
                        buy_transaction = buy_queue[0]  # Get the 'buy' transaction at index i
                        buy_date = buy_transaction['Trade Date']
                        buy_qty = buy_transaction['Quantity']
                        buy_price = buy_transaction['avg_price']
                        # get current sell data
                        sell_date = trade_date
                        sell_qty = quantity
                        sell_price = avg_price

                        if buy_qty == remaining_sell_quantity:
                            # print(f"SELL {remaining_sell_quantity} quantity @{sell_price} ")
                            # manage sold quantity
                            # sold_data = {'Symbol':each,'Buy Date':buy_date,'Sell Date':sell_date, 'Quantity': sell_qty, 'Buy Price': buy_price, 'Sell Price':sell_price, 'PnL':(sell_price-buy_price)*sell_qty}
                            # closed_pf = closed_pf.append(sold_data, ignore_index=True)
                            sold_data.append(
                                {'ISIN': each, 'Buy Date': buy_date, 'Sell Date': sell_date, 'Quantity': sell_qty,
                                 'Buy Price': buy_price, 'Sell Price': sell_price,
                                 'PnL': (sell_price - buy_price) * sell_qty})
                            # closed_pf = pd.DataFrame(sold_data)
                            # manage buy_queue
                            remaining_sell_quantity -= buy_qty
                            buy_queue.pop(0)

                        elif buy_qty > remaining_sell_quantity:  # 445>336
                            # print(f"SELL {remaining_sell_quantity} quantity @{sell_price} ")
                            # If the 'buy' quantity is greater or equal to the remaining 'sell' quantity, adjust the 'buy' quantity
                            # manage sold quantity
                            # sold_data = {'Symbol':each,'Buy Date': buy_date, 'Sell Date': sell_date, 'Quantity': remaining_sell_quantity,'Buy Price': buy_price, 'Sell Price': sell_price, 'PnL': (sell_price - buy_price)*remaining_sell_quantity}
                            sold_data.append({'ISIN': each, 'Buy Date': buy_date, 'Sell Date': sell_date,
                                              'Quantity': remaining_sell_quantity, 'Buy Price': buy_price,
                                              'Sell Price': sell_price,
                                              'PnL': (sell_price - buy_price) * remaining_sell_quantity})
                            # closed_pf = pd.DataFrame(sold_data)

                            # manage buy_queue
                            buy_queue[0][
                                'Quantity'] -= remaining_sell_quantity  # this checks the remaining buy_qty and update in the buy_queue
                            remaining_sell_quantity = 0  # checks remaining sell qty to ensure the while loop continues

                        else:  # if buy_qty<sell_qty               114,800 < 802
                            # print(f"SELL {remaining_sell_quantity} quantity @{sell_price} ")
                            # print("$$$$$$$$$$ BUY QUEUE IS : $$$$$$$$$$$$$$$")
                            # print(buy_queue[0])
                            # If the 'buy' quantity is less than the remaining 'sell' quantity, adjust the 'sell' quantity
                            # sold_data = {'Symbol':each,'Buy Date': buy_date, 'Sell Date': sell_date, 'Quantity': buy_qty,'Buy Price': buy_price, 'Sell Price': sell_price, 'PnL': (sell_price-buy_price)*buy_qty}
                            # closed_pf = closed_pf.append(sold_data, ignore_index=True)
                            sold_data.append(
                                {'ISIN': each, 'Buy Date': buy_date, 'Sell Date': sell_date, 'Quantity': buy_qty,
                                 'Buy Price': buy_price, 'Sell Price': sell_price,
                                 'PnL': (sell_price - buy_price) * buy_qty})
                            # Manage buy_queue now to get the next queue
                            buy_queue.pop(0)
                            remaining_sell_quantity -= buy_qty


        # Append any remaining 'buy' transactions to the result DataFrame
        open_pf = pd.concat([open_pf,pd.DataFrame(buy_queue)],ignore_index=True)
        closed_pf = pd.DataFrame(sold_data)

    # open_pf is the dataframe which needs to be worked upon if addition of Stock ttrades is happening
    open_pf['Investment'] = open_pf['Quantity'] * open_pf['avg_price']
    temp_open_pf = open_pf.groupby(["ISIN","Trade Type"])[['Quantity', 'Investment']].sum()  # .reset_index()
    temp_open_pf["Price"] = temp_open_pf["Investment"] / temp_open_pf["Quantity"]
    # converts the multiline index to normal DF
    final_pf = temp_open_pf.reset_index()
    # Create a dictionary mapping 'Symbol' values to 'PnL' values from 'closed_pf'
    symbol_pnl_mapping = closed_pf.set_index('ISIN')['PnL'].to_dict()
    # Use the map function to assign 'PnL' values to 'final_pf' based on 'Symbol' matching
    final_pf['prev_pnl'] = final_pf['ISIN'].map(symbol_pnl_mapping)
    final_pf['prev_pnl'].fillna('0',inplace=True)
    final_pf['YahooCode'] = final_pf['ISIN'].apply(nse_bse_search.isin_to_ycode)

    closed_pf['YahooCode'] = closed_pf['ISIN'].apply(nse_bse_search.search_df_nsebse)
    only_sell_pf['YahooCode'] = only_sell_pf['ISIN'].apply(nse_bse_search.isin_to_ycode)


    # this is to only SHOW the users by replacing ISIN to Symbol Name
    st.info("OPEN PORTFOLIO : ")
    show_pf = final_pf.copy()
    st.dataframe(show_pf.set_index('YahooCode').sort_values('Investment',ascending=False), use_container_width=True)
    #show_pf['Symbol'] = show_pf['Symbol'].replace(symbol_isin)             # Instead of replacing ISIN with Symbol. Best is to get the yahoo codes for these
    #print(show_pf.set_index('Symbol').sort_values('Investment',ascending=True))
    #st.dataframe(show_pf.set_index('Symbol').sort_values('Investment',ascending=False))

    #print("CLosed Portfolio")
    st.info("CLosed Portfolio")
    show_closed_pf = closed_pf.copy()
    st.dataframe(show_closed_pf.set_index('YahooCode').sort_values('PnL',ascending=False), use_container_width=True)
    #show_closed_pf['Symbol'] = show_closed_pf['Symbol'].replace(symbol_isin)
    #print(show_closed_pf.set_index('Symbol'))
    #st.dataframe(show_closed_pf.set_index('Symbol'))

    #print("INVALID ENTRIES : ")
    st.info("INVALID ENTRIES : ")
    show_only_sell_pf = only_sell_pf.copy()
    st.dataframe(show_only_sell_pf, use_container_width=True)
    #show_only_sell_pf['Symbol'] = show_only_sell_pf['Symbol'].replace(symbol_isin)
    #print(show_only_sell_pf.set_index('Symbol'))
    #st.dataframe(show_only_sell_pf.set_index('Symbol'))

    # IMPROVEMENTS
    #any new upload of the excel sheet shud only append the initial dataframe xl

