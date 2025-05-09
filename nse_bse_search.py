import streamlit as st
import pandas as pd
import digyahoo
import create_database
import variables
import screenerpage
import processdriver

if 'bsenames_list' not in st.session_state or 'bsecodes_list' not in st.session_state:  #if 'bse_ISIN' not in st.session_state or 'bse_ycode' not in st.session_state
    bse_data = pd.read_csv('./Select.csv', header=0, index_col=False)
    bse_data.columns = bse_data.columns.str.replace(' ', '_')
    #df = bse_data[['Security Code', 'Issuer Name', 'Security Id', 'ISIN No']]
    st.session_state.bse_ISIN = bse_data["ISIN_No"].tolist()
    st.session_state.bse_ycode = bse_data["Security_Id"].tolist()
    # bse_name = bse_data["Security_Name"].tolist()
    # bse_code = bse_data["Security_Code"].tolist()
    # st.session_state.bsenames_list = bse_name
    # st.session_state.bsecodes_list = bse_code

    st.session_state.bsenames_list = bse_data["Security_Name"].tolist()
    st.session_state.bsecodes_list = bse_data["Security_Code"].tolist()

if 'nsecode_list' not in st.session_state or 'nseISIN_list' not in st.session_state:
    nse_data = pd.read_csv('./cm21JUN2024bhav.csv')
    nse_data.columns = nse_data.columns.str.replace(' ','_')
    # nse_ISIN = nse_data["ISIN"].tolist()
    # nse_code = nse_data["SYMBOL"].tolist()
    # st.session_state.nseISIN_list = nse_ISIN
    # st.session_state.nsecode_list = nse_code
    st.session_state.nseISIN_list = nse_data["ISIN"].tolist()
    st.session_state.nsecode_list = nse_data["SYMBOL"].tolist()

#with st.expander("BACKGROUND CHECK FOR YAHOO DATABASE"):
    #st.markdown("Gives CODES or ISIN from the available data in csv files")
    #st.info("DOwnload BSE CSV FILE from here :")
    #st.write('https://www.bseindia.com/corporates/List_Scrips.html')
    #st.info("DOWNLOAD NSE file from NSE ALL REPORTS :")
    #st.write("https://www.nseindia.com/all-reports Then download Bhavcopy file (CSV) cm12OCT2023bhav.csv.zip")
    #st.dataframe(bse_data.head())
    #st.dataframe(nse_data.head())

def isin_to_ycode(isin):
    if isin in st.session_state.nseISIN_list:
        code = nse_data[nse_data["ISIN"] == isin]["SYMBOL"].values[0]
        return code
    elif isin in st.session_state.bse_ISIN:
        ycode = bse_data[bse_data["ISIN_No"] == isin]["Security_Id"].values[0]
        return ycode
    else:
        return None

def isin_to_code(isin):                 # this returns CODE suitable for both SCREENER and YAHOO for NSE but for BSE, returns "BSECODE YCODE"
    if isin in st.session_state.nseISIN_list:
        code = nse_data[nse_data["ISIN"] == isin]["SYMBOL"].values[0]
        #st.info(f"Asked for {isin} giving back {code}")
        return code
    elif isin in st.session_state.bse_ISIN:
        code = bse_data[bse_data["ISIN_No"]==isin]["Security_Code"].values[0]
        #return str(code) + " " + str(ycode)
        #st.info(f"Asked for {isin} giving back {code}")
        return code
    else:
        return None

def search_df_nsebse(search):
    if search in st.session_state.nseISIN_list:
        code = nse_data[nse_data["ISIN"]==search]["SYMBOL"].values[0]
        return code
    elif search in st.session_state.nsecode_list:
        isin = nse_data[nse_data["SYMBOL"]==search]["ISIN"].values[0]
        return isin
    elif search in st.session_state.bse_ycode:
        isin = bse_data[bse_data["Security_Id"]==search]["ISIN_No"].values[0]
        return isin
    elif search in st.session_state.bse_ISIN:
        ycode = bse_data[bse_data["ISIN_No"]==search]["Security_Id"].values[0]
        return ycode

def dict_from_bse_csv(driver):
    # Initialize a list to store rows that meet the condition
    selected_rows = []
    not_in_yahoo = []
    isin_dict = {}
    bsecode_dict = {}
    try:
        #writer = csv.writer(csv_file)        # Iterate through each row and perform the web lookup
        for index, row in bse_data.iterrows():
            security_id = row['Security_Id']
            isin_with_bo = security_id + '.BO'
            ticker = digyahoo.get_yahoocode(driver, isin_with_bo)
            if ticker is not None:
                selected_rows.append(row)
                st.info(f"Found Yahoo for {security_id}")
                #txt.write(str(row['Security Code']) + ","+ str(row['Issuer Name'])+ ","+str(row['Security Id'])+ "," + str(row['ISIN No'])+"\n")
                isin = row['ISIN No']
                #print(row['ISIN No'].to_dict())
                isin_dict[isin] = row.drop('ISIN No').to_dict()
                st.info(isin_dict)
                bsecode = row['Security Code']
                bsecode_dict[bsecode] = row.drop('Security Code').to_dict()
                st.info(bsecode_dict)
            else:
                not_in_yahoo.append(row['Security Id'])
                st.info(not_in_yahoo)

    except:
        with open('./bseinfo.txt','a') as txt:
            for each in not_in_yahoo:
                txt.write(each + '\n')



    # Convert the selected rows to a DataFrame
    #selected_df = pd.DataFrame(selected_rows)
    #st.dataframe(selected_df)
    #selected_df.to_pickle('./bsecodes.pkl')
    # Save the selected data to a JSON file
    #selected_df.to_json('selected_data.json', orient='records')


def bsecodenum_bsecodename():
    bse_data = pd.read_csv('./Select.csv', header=0, index_col=False)
    bse_data.columns = bse_data.columns.str.replace(' ', '_')
    bse_data = bse_data[['Security_Code','Security_Id','Security_Name']].copy()
    bsecodenum_codename = bse_data.set_index('Security_Code')['Security_Id'].to_dict()
    bsecodename_codenum = bse_data.set_index('Security_Id')['Security_Code'].to_dict()
    bsecodenum_fullname = bse_data.set_index('Security_Code')['Security_Name'].to_dict()
    bsecodename_fullname = bse_data.set_index('Security_Id')['Security_Name'].to_dict()
    bsefullname_codenum = bse_data.set_index('Security_Name')['Security_Code'].to_dict()
    bsefullname_codename = bse_data.set_index('Security_Name')['Security_Id'].to_dict()
    return bsecodenum_codename,bsecodename_codenum,bsecodenum_fullname,bsecodename_fullname,bsefullname_codenum,bsefullname_codename

def bseSCNAME_SCCODE():
    bse_csv = pd.read_csv('sccodenames.CSV',header=0,index_col=False,usecols=["SC_CODE","SC_NAME"])
    bse_csv["SC_NAME"] = bse_csv["SC_NAME"].str.strip()
    bsesccode_scname = bse_csv.set_index('SC_CODE')['SC_NAME'].to_dict()
    bsescname_sccode = bse_csv.set_index('SC_NAME')['SC_CODE'].to_dict()
    return bsesccode_scname,bsescname_sccode

global bsecodenum_codename
global bsecodename_codenum
bsecodenum_codename, bsecodename_codenum, bsecodenum_fullname, bsecodename_fullname, bsefullname_codenum, bsefullname_codename = bsecodenum_bsecodename()
# This gets us the BSE NAME from the DAILY BHAVCOPY THAT WE ARE DOWNLOADING
bsesccode_scname, bsescname_sccode = bseSCNAME_SCCODE()


#needs to return NSE CODE and BSECODE as 
def process_code(code)->list:
    code_names = [str(code).upper()]
    query_code = str(code).upper()
    if create_database.comp_metadata_col.count_documents({"code_names":query_code}):
        code_names_obj = create_database.comp_metadata_col.find_one({"code_names":query_code})
        code_names = code_names_obj['code_names']
        return code_names
    else:
        return code_names

def get_code_name(code):
    query_code = str(code).upper()
    # st.success(query_code)
    if create_database.comp_metadata_col.count_documents({"code_names":query_code}):
        code_names_obj = create_database.comp_metadata_col.find_one({"code_names":query_code})
        return code_names_obj['code_names'][-1],code_names_obj["comp_metadata"]["comp_fullname"]

        


@st.cache_data
def remove_duplicate_in_watchlist(givenlist:list)->list:            #give LIST here
    print(f"Entered remove_duplicate_in_watchlist which gave {len(givenlist)} to process")
    # print(f"We hve metadata already {type(variables.metadata)}")
    unique_list = []
    duplicate_list = []
    for line in givenlist:
        codenames_watchlist = 0(str(line).strip())
        print(f"We got {codenames_watchlist} from DB in remove_duplicate_in_watchlist FUNC while trying for {line}")
        # st.info(codenames_watchlist)
        if len(codenames_watchlist) >=1:
            if len(codenames_watchlist)==1 :
                if line not in unique_list and line not in duplicate_list:
                    unique_list.append(codenames_watchlist[-1])
                    # st.info(unique_list)
            else:
                if codenames_watchlist[-1] not in unique_list and codenames_watchlist[0] not in duplicate_list:
                    unique_list.append(codenames_watchlist[-1])
                    duplicate_list.append(codenames_watchlist[0])
    print(f"We finalized {len(unique_list)} from given {len(givenlist)} in remove_duplicate_in_watchlist FUNC")
    return unique_list
