import os
import shutil
import pandas as pd
import streamlit as st
import fundamentals

def amibroker_notes_insights(code_names, message):
    # print(message)
    # st.info(f"RECEIVED in amibroker.py {code_names}")
    for each in code_names:
        # st.info(each)
        each = str(each)
        amibroker_txt = "./amibroker/notes/" + each.strip() + ".txt"
        # print(f"Writing in {amibroker_txt}")
        # amibroker_csv = "./amibroker/csv/" + each + " Yearly.csv"
        with open(amibroker_txt, "w") as f:
            f.write(message)
        # st.info(f"Amibroker notes saved in {amibroker_txt}")

def amibroker_notes_csv_yearly(code_names, yr_df):
    pnl, balancesht = fundamentals.develop_yearly(yr_df)
    sentence = ""
    # PREPARE THE FIRST STATEMENT
    if len(code_names) == 1:
        sentence += f"{str(code_names[0])} "
    else:
        for each in code_names:
            sentence += f"{str(each)} "

    # NOTES AND CSV FILES FOR AMIBROKER
    # TO SAVE IN AMIBROKER CSV
    developed_df = pd.concat([pnl, balancesht, yr_df.loc["CASH FLOW", :]], axis=0)
    # REMOVE THE NESTED 1ST COLUMN VALUES
    # yr_df1 = yr_df.reset_index()
    # yr_df2 = yr_df1.iloc[:, 1:].set_index("Report Date")
    for each in code_names:
        each = str(each)
        amibroker_txt = "./amibroker/notes/" + each + ".txt"
        amibroker_csv = "./amibroker/csv/" + each + " Yearly.csv"
        try:
            sentence += f"\n**********YEARLY**********\n"
            if len(developed_df.columns) >= 2:
                last_year = developed_df.columns[-1]
                prev_year = developed_df.columns[-2]
                get_from_yearly = ["SALES", "NET PROFIT", "NPM %", "NO. OF EQUITY SHARES", "FACE VALUE", "DEBTOR DAYS",
                                   "INVENTORY TURNOVER", "ROCE", "RESERVES", "BORROWINGS"]
                eq_last_year = round(developed_df.loc["NO. OF EQUITY SHARES", last_year] / 10000000, 2)
                eq_prev_year = round(developed_df.loc['NO. OF EQUITY SHARES', prev_year] / 10000000, 2)
                FV_last_year = round(developed_df.loc['FACE VALUE', last_year])
                FV_prev_year = round(developed_df.loc['FACE VALUE', prev_year])
                ROCE_last_year = developed_df.loc['ROCE', last_year]
                ROCE_prev_year = developed_df.loc['ROCE', prev_year]
                Yearly_sentence_in_Quarterly = f"Equity in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(eq_last_year)}cr; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(eq_prev_year)}cr\nFaceValue in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(FV_last_year)}; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(FV_prev_year)}\nROCE in {str(datetime.datetime.strftime(last_year, '%b-%Y'))}: {str(ROCE_last_year)}%; in {str(datetime.datetime.strftime(prev_year, '%b-%Y'))}: {str(ROCE_prev_year)}%\n"
                sentence += Yearly_sentence_in_Quarterly
                #st.info(Yearly_sentence_in_Quarterly)

            sentence += fundamentals.stmt_for_qoq(pnl)
            # st.info("trying to open amiboker txt file")
            with open(amibroker_txt, "a") as f:
                f.write(sentence)
                f.write("\n")
            # st.success(f"Written in {amibroker_txt} file")
        except Exception as e:
            print(f"Getting error {e} while trying to write txt file")

        try:
            # st.dataframe(developed_df)
            # trying to save the data in CSV file to load in AMIBROKER
            # yr_df2.to_csv(amibroker_csv)
            developed_df.to_csv(amibroker_csv)
        except Exception as e:
            print(f"Getting error {e} while trying to write csv files ")
def amibroker_notes_csv_quarterly(code_names, qtr_df):
    qtr_pnl = fundamentals.develop_quarterly(qtr_df)
    qtr_pnl.columns = pd.to_datetime(qtr_pnl.columns, format='%d-%m-%Y')
    sentence = ""
    # NOTES AND CSV FILES FOR AMIBROKER
    for each in code_names:
        each = str(each)
        #sentence = sentence1
        amibroker_txt = "./amibroker/notes/" + each + ".txt"
        amibroker_csv = "./amibroker/csv/" + each + " Quarterly.csv"
        try:
            sentence += f"\n**********QUARTERLY**********\n"
            sentence += f"Update Date: {datetime.datetime.strftime(datetime.datetime.now(), '%d-%b-%Y')}\n"
            sentence += fundamentals.stmt_for_qoq(qtr_pnl)
            with open(amibroker_txt, "a") as f:
                f.write(sentence)
                f.write("\n")
            # st.success(f"Written in {amibroker_txt} file")
        except Exception as e:
            print(f"Getting error {e} while trying to write txt file")
        try:
            # trying to save the data in CSV file to load in AMIBROKER
            qtr_df.to_csv(amibroker_csv)
        except Exception as e:
            print(f"Getting error {e} while trying to write csv files ")

                                                                                                                        # stripped code : either NSECODE or BSECODE



