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


import re

def format_financial_text(raw_text: str) -> str:
    lines = [line.strip() for line in raw_text.strip().split('\n')]
    table = []

    # Split lines using regex that handles multiple tabs or spaces
    for line in lines:
        parts = re.split(r'[\t ]{2,}', line)
        # Ensure the label and values are separated
        label_and_values = []
        for part in parts:
            subparts = part.strip().split('\t')
            label_and_values.extend([p for p in subparts if p])
        table.append(label_and_values)

    # Transpose to calculate max width for each column
    col_widths = [max(len(row[i]) for row in table if i < len(row)) for i in range(len(table[0]))]

    output = []
    for row in table:
        formatted_row = " | ".join(
            row[i].center(col_widths[i]) if i < len(row) else " " * col_widths[i]
            for i in range(len(col_widths))
        )
        output.append(formatted_row)

    # Add divider after header
    divider = "-+-".join("-" * w for w in col_widths)
    output.insert(1, divider)

    return "\n".join(output)



# def format_financial_text1(raw_text: str) -> str:
#     lines = [line.strip() for line in raw_text.strip().split('\n')]
#     headers = lines[0].split('\t')
#     data_rows = [line.split('\t') for line in lines[1:]]

#     # Clean up and align
#     headers = [col.strip(': ') for col in headers]
#     rows = []
#     for row in data_rows:
#         row = [cell.strip() for cell in row if cell.strip()]
#         rows.append(row)

#     # Format into a single string
#     col_width = 10
#     output = []

#     header_line = "Metric".ljust(col_width) + "| " + " | ".join(h.center(col_width) for h in headers[1:])
#     divider = "-" * len(header_line)
#     output.append(header_line)
#     output.append(divider)

#     for row in rows:
#         row_line = row[0].ljust(col_width) + "| " + " | ".join(cell.center(col_width) for cell in row[1:])
#         output.append(row_line)

#     return "\n".join(output)

def ami_notes_from_database1():
    for document in create_database.comp_metadata_col.find():
        st.success(f"Trying to save notes for {document['code_names']}")
        sentence = amibroker_notes_insights(metadata=document)
        #create and write a text file        
        for each1 in document['code_names']:
            with open(f"./amibroker/dbnotes/{each1}.txt", 'w') as f:
                f.write(sentence)
    
def amibroker_notes_insights(metadata):
    # st.success(f"In amibroker_notes_insights FUNC, the Metadata is \n{metadata}")
    code_names = metadata['code_names']
    sentence = ""
    if len(metadata['code_names']) == 1 and metadata['code_names'][0].isdigit():
        sentence += f"CODE\tNAME\n"
        sentence += f"{metadata['code_names'][0]} \n" #{st.session_state.bsecodenum_codename[int(metadata['code_names'][0])]}"
    else:
        sentence += f"CODES\n"
        for each in metadata['code_names']: sentence += f"{each}\t"
    if 'comp_metadata' in metadata.keys():
        sentence += f"\nSECTOR : {metadata['comp_metadata']['sector']}\nINDUSTRY : {metadata['comp_metadata']['industry']}"
    sentence += "\n"
    if 'metadata' in metadata.keys():
        if 'tags' in metadata['metadata'].keys():
            for each in metadata['metadata']['tags'] : sentence += f"{each}\n"        
        if 'cons' in metadata['metadata'].keys():
            sentence += "\n***CONS***\n"
            for each in metadata['metadata']['cons']: sentence += f"{each}\n"
        if 'YPNL_Statement' in metadata['metadata'].keys(): 
            # sentence += "\n***YEARLY***" + metadata['metadata']['YPNL_Statement'] + "\n"
            sentence += format_financial_text(raw_text=metadata['metadata']['YPNL_Statement'])
            sentence += "\n"
        if 'QPNL_Statement' in metadata['metadata'].keys():     
            # sentence += "\n***QUARTERLY***" + metadata['metadata']['QPNL_Statement'] + "\n"
            sentence += format_financial_text(raw_text=metadata['metadata']['QPNL_Statement'])
            sentence += "\n"
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
    # for each in code_names:
    #     each = str(each)
    #     amibroker_txt = "./amibroker/notes/" + each.strip() + ".txt"
    #     with open(amibroker_txt, "w") as f:
    #         f.write(message)
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



