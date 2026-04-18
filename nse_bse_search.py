import streamlit as st
import pandas as pd
import os
import create_database
import digyahoo
import variables
import screenerpage
import processdriver

if 'bse_data' not in st.session_state:
    # Fetch from MongoDB ReferenceData first
    bse_df = create_database.get_reference_data('bse_select')
    
    # Try local file as fallback if DB is empty
    if bse_df.empty and os.path.exists('./Select.csv'):
        bse_df = pd.read_csv('./Select.csv', header=0, index_col=False)
        # Only try to save if it's not giant
        if len(bse_df) < 50000:
            create_database.save_reference_data('bse_select', bse_df)
    
    st.session_state.bse_data = bse_df

if not st.session_state.bse_data.empty:
    bse_data = st.session_state.bse_data
    # Ensure column names are clean
    bse_data.columns = [c.replace(' ', '_') for c in bse_data.columns]
    
    st.session_state.bse_ISIN = bse_data["ISIN_No"].tolist() if 'ISIN_No' in bse_data.columns else []
    st.session_state.bse_ycode = bse_data["Security_Id"].tolist() if 'Security_Id' in bse_data.columns else []
    st.session_state.bsenames_list = bse_data["Security_Name"].tolist() if 'Security_Name' in bse_data.columns else []
    st.session_state.bsecodes_list = bse_data["Security_Code"].tolist() if 'Security_Code' in bse_data.columns else []
else:
    st.session_state.bse_ISIN = []
    st.session_state.bse_ycode = []
    st.session_state.bsenames_list = []
    st.session_state.bsecodes_list = []

if 'nse_data' not in st.session_state:
    # Fetch from MongoDB first
    nse_df = create_database.get_reference_data('nse_bhav')
    
    # Fallback to local
    if nse_df.empty and os.path.exists('./cm21JUN2024bhav.csv'):
        nse_df = pd.read_csv('./cm21JUN2024bhav.csv')
        create_database.save_reference_data('nse_bhav', nse_df)
        
    st.session_state.nse_data = nse_df

if not st.session_state.nse_data.empty:
    nse_data = st.session_state.nse_data
    if 'SYMBOL' not in nse_data.columns:
        nse_data.columns = nse_data.columns.str.replace(' ','_')
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
    if not st.session_state.bse_data.empty:
        df = st.session_state.bse_data
    else:
        # Fallback if session state is not ready (shouldn't happen with the new init)
        df = create_database.get_reference_data('bse_select')
    
    if df.empty:
        return {}, {}, {}, {}, {}, {}

    df.columns = df.columns.str.replace(' ', '_')
    # Filter only necessary columns
    needed = ['Security_Code','Security_Id','Security_Name']
    available = [c for c in needed if c in df.columns]
    df = df[available].copy()
    
    bsecodenum_codename = df.set_index('Security_Code')['Security_Id'].to_dict() if 'Security_Code' in df.columns and 'Security_Id' in df.columns else {}
    bsecodename_codenum = df.set_index('Security_Id')['Security_Code'].to_dict() if 'Security_Code' in df.columns and 'Security_Id' in df.columns else {}
    bsecodenum_fullname = df.set_index('Security_Code')['Security_Name'].to_dict() if 'Security_Code' in df.columns and 'Security_Name' in df.columns else {}
    bsecodename_fullname = df.set_index('Security_Id')['Security_Name'].to_dict() if 'Security_Id' in df.columns and 'Security_Name' in df.columns else {}
    bsefullname_codenum = df.set_index('Security_Name')['Security_Code'].to_dict() if 'Security_Name' in df.columns and 'Security_Code' in df.columns else {}
    bsefullname_codename = df.set_index('Security_Name')['Security_Id'].to_dict() if 'Security_Name' in df.columns and 'Security_Id' in df.columns else {}
    return bsecodenum_codename,bsecodename_codenum,bsecodenum_fullname,bsecodename_fullname,bsefullname_codenum,bsefullname_codename

def bseSCNAME_SCCODE():
    # Attempt MongoDB ReferenceData first
    bse_csv = create_database.get_reference_data('sccodenames')
    
    # Fallback to local
    if bse_csv.empty and os.path.exists('sccodenames.CSV'):
        bse_csv = pd.read_csv('sccodenames.CSV',header=0,index_col=False,usecols=["SC_CODE","SC_NAME"])
        # Save to MongoDB for future use
        create_database.save_reference_data('sccodenames', bse_csv)
    
    if bse_csv.empty:
        return {}, {}

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
        codenames_watchlist = process_code(str(line).strip())
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
