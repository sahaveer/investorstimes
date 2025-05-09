import os
import shutil
import pandas as pd
import streamlit as st
import fundamentals
import create_database


#by clicking a button, this function is called; It gets all the necessary data from the database and writes to dbnotes folder
# def ami_notes_from_database():
#     for document in create_database.company_metadata_col.find():
#         key = document['_id']
#         #create and write a text file        
#         with open(f'./amibroker/dbnotes/{key}.txt', 'w') as f:
#             # write document('code_names') document('pros') document('tags') document('cons') document('YPNL_Statement') document('QPNL_Statement')
#             try:
#                 f.write(f"Code Names: {document['code_names']}\n")
#                 if len(document['pros']) > 1:
#                     f.write(f"\nPros: \n")
#                     for each in document['pros']:
#                         f.write(f"{each}\n")
#                 if len(document['tags']) > 1:
#                     f.write(f"\nTAGS: \n")
#                     for each in document['tags']:
#                         f.write(f"{each}\n")
#                 if len(document['cons']) > 1:
#                     f.write(f"\nCONS: \n")
#                     for each in document['cons']:
#                         f.write(f"{each}\n")

#                 if 'YPNL_Statement' in document.keys():
#                     f.write(f"\nYPNL Statement: {document['YPNL_Statement']}\n")
#                 if 'QPNL_Statement' in document.keys():
#                     f.write(f"\nQPNL Statement: {document['QPNL_Statement']}\n")
#             except Exception as KeyError:
#                 st.error(f"Error writing to file {key}.txt: {KeyError}")

def ami_notes_from_database1():
    for document in create_database.comp_metadata_col.find():
        # st.success(document)
        key = document['_id']
        #create and write a text file        
        try:
            for each1 in document['code_names']:
                metadata = each1
                with open(f"./amibroker/dbnotes/{document[each1]}.txt", 'w') as f:
                    code_names = metadata['code_names']
                    sentence = ""
                    if len(metadata['code_names']) == 1 and metadata['code_names'][0].isdigit():
                        sentence += f"CODE\tNAME\n"
                        sentence += f"{metadata['code_names'][0]} \n" #{st.session_state.bsecodenum_codename[int(metadata['code_names'][0])]}"
                    else:
                        sentence += f"CODES\n"
                        for each in metadata['code_names']: sentence += f"{each}\t"
                    # for each in metadata['code_names']: sentence += f"{each}\t"
                    sentence += "\n"
                    for each in metadata['metadata']['tags'] : sentence += f"{each}\n"
                    if 'cons' in metadata['metadata'].keys():
                        sentence += "\n***CONS***\n"
                        for each in metadata['metadata']['cons']: sentence += f"{each}\n"
                    if 'YPNL_Statement' in metadata['metadata'].keys(): 
                        sentence += "\n***YEARLY***" + metadata['metadata']['YPNL_Statement'] + "\n"
                    if 'QPNL_Statement' in metadata['metadata'].keys():     
                        sentence += "\n***QUARTERLY***" + metadata['metadata']['QPNL_Statement'] + "\n"
                    if 'pros' in metadata['metadata'].keys():
                        sentence += "\n***PROS***\n"
                        for each in metadata['metadata']['pros']: sentence += f"{each}\n"
                    if 'QPNL_tweet' in metadata['metadata'].keys():
                        sentence += f"\n{metadata['metadata']['QPNL_tweet']}\n"
                    if 'YPNL_tweet' in metadata['metadata'].keys():
                        sentence += f"\n{metadata['metadata']['YPNL_tweet']}\n"
                    message = sentence
                    f.write(message)
                    # if "comp_metadata" in document.keys():
                    #     # f.write(f"Code Names: ")
                    #     #how to read key and value in a dict?
                    #     for eachkey,eachval in document['comp_metadata']['code_names'].items():
                    #         f.write(f"{eachkey}:{eachval}\n")
                    #     f.write(f"{document['comp_metadata']['comp_fullname']}\n")
                    #     f.write(f"SECTOR : {document['comp_metadata']['sector']}; \nINDUSTRY : {document['comp_metadata']['industry']}\n")
                    # if "CONSOLIDATED" in document.keys() or "STANDALONE" in document.keys():
                    #     if "CONSOLIDATED" in document.keys():
                    #         # reqd_data = document['CONSOLIDATED']['metadata']
                    #         f.write(f"Both Standalone and Consolidated data are available.\nCONSOLIDATED DATA:\n")
                    #         if 'metadata' in document['CONSOLIDATED'].keys(): 
                    #             if 'tags' in document['CONSOLIDATED']['metadata'].keys():
                    #                 if len(document['CONSOLIDATED']['metadata']['tags'])>=1:
                    #                     f.write(f"TAGS:\n")
                    #                     for each in document['CONSOLIDATED']['metadata']['tags']:
                    #                         f.write(f"{each}\n")
                    #             if 'pros' in document['CONSOLIDATED']['metadata'].keys():
                    #                 if len(document['CONSOLIDATED']['metadata']['pros'])>0:
                    #                     f.write(f"PROS:\n")
                    #                     for each in document['CONSOLIDATED']['metadata']['pros']:
                    #                         f.write(f"{each}\n")
                    #             if 'cons' in document['CONSOLIDATED']['metadata'].keys():
                    #                 if len(document['CONSOLIDATED']['metadata']['cons'])>0:
                    #                     f.write(f"CONS:\n")
                    #                     for each in document['CONSOLIDATED']['metadata']['cons']:
                    #                         f.write(f"{each}\n")
                    #             if 'YPNL_Statement' in document['CONSOLIDATED']['metadata'].keys():
                    #                 f.write(f"{document['CONSOLIDATED']['metadata']['YPNL_Statement']}\n")
                    #             if 'QPNL_Statement' in document['CONSOLIDATED']['metadata'].keys():
                    #                 f.write(f"{document['CONSOLIDATED']['metadata']['QPNL_Statement']}\n")
                            
                    #     elif "STANDALONE" in document.keys():
                    #         f.write(f"STANDALONE DATA:\n")
                    #         if 'metadata' in document['STANDALONE'].keys(): 
                    #             if 'tags' in document['STANDALONE']['metadata'].keys():
                    #                 if len(document['STANDALONE']['metadata']['tags'])>0:
                    #                     f.write(f"TAGS:\n")
                    #                     for each in document['STANDALONE']['metadata']['tags']:
                    #                         f.write(f"{each}\n")
                    #             if 'pros' in document['STANDALONE']['metadata'].keys():
                    #                 if len(document['STANDALONE']['metadata']['pros'])>0:
                    #                     f.write(f"PROS:\n")
                    #                     for each in document['STANDALONE']['metadata']['pros']:
                    #                         f.write(f"{each}\n")

                    #             if 'cons' in document['STANDALONE']['metadata'].keys():
                    #                 if len(document['STANDALONE']['metadata']['cons'])>0:
                    #                     f.write(f"CONS:\n")
                    #                     for each in document['STANDALONE']['metadata']['cons']:
                    #                         f.write(f"{each}\n")
                    #             if 'YPNL_Statement' in document['STANDALONE']['metadata'].keys():
                    #                 f.write(f"{document['STANDALONE']['metadata']['YPNL_Statement']}\n")
                    #             if 'QPNL_Statement' in document['STANDALONE']['metadata'].keys():
                    #                 f.write(f"{document['STANDALONE']['metadata']['QPNL_Statement']}\n")

        except Exception as KeyError:
            st.error(f"Error writing to file {key}.txt: {KeyError}")

def amibroker_notes_insights( metadata):
    # st.success(f"In amibroker_notes_insights FUNC, the Metadata is \n{metadata}")
    code_names = metadata['code_names']
    sentence = ""
    if len(metadata['code_names']) == 1 and metadata['code_names'][0].isdigit():
        sentence += f"CODE\tNAME\n"
        sentence += f"{metadata['code_names'][0]} \n" #{st.session_state.bsecodenum_codename[int(metadata['code_names'][0])]}"
    else:
        sentence += f"CODES\n"
        for each in metadata['code_names']: sentence += f"{each}\t"
    # for each in metadata['code_names']: sentence += f"{each}\t"
    sentence += "\n"
    for each in metadata['metadata']['tags'] : sentence += f"{each}\n"
    if 'cons' in metadata['metadata'].keys():
        sentence += "\n***CONS***\n"
        for each in metadata['metadata']['cons']: sentence += f"{each}\n"
    if 'YPNL_Statement' in metadata['metadata'].keys(): 
        sentence += "\n***YEARLY***" + metadata['metadata']['YPNL_Statement'] + "\n"
    if 'QPNL_Statement' in metadata['metadata'].keys():     
        sentence += "\n***QUARTERLY***" + metadata['metadata']['QPNL_Statement'] + "\n"
    if 'pros' in metadata['metadata'].keys():
        sentence += "\n***PROS***\n"
        for each in metadata['metadata']['pros']: sentence += f"{each}\n"
    if 'QPNL_tweet' in metadata['metadata'].keys():
        sentence += f"\n{metadata['metadata']['QPNL_tweet']}\n"
    if 'YPNL_tweet' in metadata['metadata'].keys():
        sentence += f"\n{metadata['metadata']['YPNL_tweet']}\n"
    message = sentence
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
    return sentence

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



