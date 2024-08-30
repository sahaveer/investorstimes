import streamlit as st
import pandas as pd
import digyahoo

bse_data = pd.read_csv('./Select.csv', header=0, index_col=False)
bse_data.columns = bse_data.columns.str.replace(' ', '_')
#df = bse_data[['Security Code', 'Issuer Name', 'Security Id', 'ISIN No']]
bse_ISIN = bse_data["ISIN_No"].tolist()
bse_ycode = bse_data["Security_Id"].tolist()
bse_name = bse_data["Security_Name"].tolist()
bse_code = bse_data["Security_Code"].tolist()

nse_data = pd.read_csv('./cm12OCT2023bhav.csv')
nse_data.columns = nse_data.columns.str.replace(' ','_')
nse_ISIN = nse_data["ISIN"].tolist()
nse_code = nse_data["SYMBOL"].tolist()

#with st.expander("BACKGROUND CHECK FOR YAHOO DATABASE"):
    #st.markdown("Gives CODES or ISIN from the available data in csv files")
    #st.info("DOwnload BSE CSV FILE from here :")
    #st.write('https://www.bseindia.com/corporates/List_Scrips.html')
    #st.info("DOWNLOAD NSE file from NSE ALL REPORTS :")
    #st.write("https://www.nseindia.com/all-reports Then download Bhavcopy file (CSV) cm12OCT2023bhav.csv.zip")
    #st.dataframe(bse_data.head())
    #st.dataframe(nse_data.head())

def isin_to_ycode(isin):
    if isin in nse_ISIN:
        code = nse_data[nse_data["ISIN"] == isin]["SYMBOL"].values[0]
        return code
    if isin in bse_ISIN:
        ycode = bse_data[bse_data["ISIN_No"] == isin]["Security_Id"].values[0]
        return ycode

def isin_to_code(isin):                 # this returns CODE suitable for both SCREENER and YAHOO for NSE but for BSE, returns "BSECODE YCODE"
    if isin in nse_ISIN:
        code = nse_data[nse_data["ISIN"] == isin]["SYMBOL"].values[0]
        #st.info(f"Asked for {isin} giving back {code}")
        return code
    elif isin in bse_ISIN:
        code = bse_data[bse_data["ISIN_No"]==isin]["Security_Code"].values[0]
        ycode = bse_data[bse_data["ISIN_No"] == isin]["Security_Id"].values[0]
        #return str(code) + " " + str(ycode)
        #st.info(f"Asked for {isin} giving back {code}")
        return code
    else:
        return None


def search_df_nsebse(search):
    if search in nse_ISIN:
        code = nse_data[nse_data["ISIN"]==search]["SYMBOL"].values[0]
        return code
    elif search in nse_code:
        isin = nse_data[nse_data["SYMBOL"]==search]["ISIN"].values[0]
        return isin
    elif search in bse_ycode:
        isin = bse_data[bse_data["Security_Id"]==search]["ISIN_No"].values[0]
        return isin
    elif search in bse_ISIN:
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
