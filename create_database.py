from pydoc import doc
import streamlit as st
import pandas as pd
import pymongo
from pymongo import MongoClient
# from pymongoarrow.api import write
import datetime
import os

import config
from datetime import date
import pprint
import variables

# CREATING AND CONNECTING TO DATABASE
Connection_String = config.get_mongodb_uri()
client = MongoClient(Connection_String)
db = client.get_database('Bhavcopy')
db2 = client.get_database('STOCKSINFO')

# DEFINING COLLECTIONS INSIDE THE DATABASE
NSE_col = db["NSEbhav"]
BSE_col = db["BSEbhav"]
BSECODE_col = db["BSECODEbhav"]
INDEX_col = db["INDEXbhav"]
FUTURE_col = db["FUTURESbhav"]
OPTIONS_col = db["OPTIONSbhav"]
userid_col = db["usersdata"]
topics_col = db["topics"]
OI_col = db["OI"]
EOD_col = db["EOD"]
reco_col = db["RECO"]
pf_col = db["Portfolio"]
eod_df_col = db["EODdataframe"]
# print(list(company_metadata_col.find()))
pfaccess_col = db["PFaccess"]
gtt_col = db["GTT"]
watchlist_col = db["Watchlist"]


company_metadata_col = db2["CompanyMetadata"]
comp_metadata_col = db2["CompMetadata"]
industry_col =  db2["Industry"]
stocks_list_col = db2["StocksList"]
reference_data_col = db2["ReferenceData"]

def save_reference_data(key, df):
    """Save a DataFrame as reference data in MongoDB."""
    try:
        data_dict = df.to_dict(orient='records')
        reference_data_col.update_one(
            {"_id": key},
            {"$set": {"data": data_dict, "timestamp": datetime.datetime.now()}},
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error saving reference data: {e}")
        return False

def get_reference_data(key):
    """Fetch reference data from MongoDB as a DataFrame."""
    try:
        doc = reference_data_col.find_one({"_id": key})
        if doc:
            return pd.DataFrame(doc["data"])
    except Exception as e:
        print(f"Error fetching reference data: {e}")
    return pd.DataFrame()
stocks_list_col = db2["StocksList"]

def get_all_listed_stocks():
    """Fetch all listed stocks from MongoDB."""
    try:
        doc = stocks_list_col.find_one({"_id": "all_listed"})
        if doc:
            return doc.get("stocks", [])
    except Exception as e:
        print(f"Error fetching stocks from DB: {e}")
    return []

def seed_stocks_from_file(file_path):
    """Seed the StocksList collection from a local text file."""
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r') as f:
        stocks = [line.strip() for line in f.readlines()]
    stocks_list_col.update_one({"_id": "all_listed"}, {"$set": {"stocks": stocks}}, upsert=True)
    return stocks
#EODBhavcopy : Bhavcopy : INDEXbhav
#EODBhavcopy : Bhavcopy : NSEbhav

def users_db(user_id,user_name,visited):                     # COL should alwas be userid_col
    my_dict = {"month":str(date.today().month) + "/" + str(date.today().year),"user_id": user_id, "user_name":user_name,"visits":visited}
    #my_dict = {"user_id": user_id, "user_name":user_name}
    try:
        userid_col.insert_one(my_dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def allow_my_pf(my_id, my_name, add_id):
    if pfaccess_col.count_documents({"by_id": my_id}):
        users_list = pfaccess_col.find_one({"user_id": my_id})["add_user"]
        users_list.append(add_id)
        pfaccess_col.find_one_and_update({"user_id": my_id},{"$set": {"add_user": users_list}})
    else:
        my_dict = {"user_id":my_id, "user_name":my_name, "add_user":[add_id]}
        try:
            pfaccess_col.insert_one(my_dict)
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def insert_db(col,fileid,date):
    #my_dict["file_id"] = fileid
    #my_dict["date"] = date

    my_dict = {"file_id":fileid, "date":date}                       # date in yyyymmdd
    try:
        col.insert_one(my_dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")


def edit_database_by_rules():
    # lets iterate through variables.metadata
    for key, value in variables.metadata.items():
        #lets see if 'BestQ Sep' is available in variables.metadata[key]['tags']
        try:
            if 'BestQ Dec' in variables.metadata[key]['tags']:
                #lets get the value of 'BestQ Sep' from variables.metadata[key]['tags']
                # st.error(f"Found BESTQ in {key}")
                #replace list variables.metadata[key]['tags'] value 'BestQ Sep' with 'BestQ Sep 2024'
                variables.metadata[key]['tags'].remove('BestQ Dec')
                variables.metadata[key]['tags'].append('BestQ Dec 2023')
                
        except Exception as TypeError:
            st.error(f"Error {TypeError} in  {key}")
            pass


# def edit_metadata():
#     for document in company_metadata_col.find():
#         try:
#             if 'BestQ Dec' in document['tags']:
#                 st.error(f"Found BEstQ Dec in {document['_id']}")
#                 st.error(document['tags'])
#                 # Replace in the list
#                 updated_tags = ['BestQ Dec 2023' if tag == 'BestQ Dec' else tag for tag in document['tags']]
#                 #lets get only unique values in the list object 
#                 updated_tags = list(set(updated_tags))
#                 st.success(updated_tags)
#                 # Update the document in MongoDB
#                 company_metadata_col.update_one({'_id': document['_id']}, {'$set': {'tags': updated_tags}})
#                 # st.success(updated_tags)
#         except  Exception as TypeError:
#             st.error(f"Error {TypeError} in  {document['_id']}")

@st.cache_resource
def get_metadata(recent_quarter_txt,last_quarter_text):
    latest_quarterly_stocks = []
    available_stocks = []
    not_latest_quarterly = []
    last_announced_quarter1 = ""

    print("Fetching Stock Metadata from MongoDB (Optimized)...")
    send_metadata = {}
    
    # Fetch metadata and quarterly keys (latest only)
    projection = {
        "_id": 1, 
        "code_names": 1, 
        "comp_metadata": 1, 
        "metadata": 1,
        "CONSOLIDATED.QUARTERLY": {"$slice": -1},
        "STANDALONE.QUARTERLY": {"$slice": -1}
    }

    for document in comp_metadata_col.find({}, projection):
        if document is None:
            continue
        
        key = document.get('_id', 'unknown')
        send_metadata[key] = document
        available_stocks.append(key)
        
        # 1. Try to get last quarter from metadata object
        meta_obj = document.get('metadata', {})
        last_q = meta_obj.get('recent_quarter', "")
        
        # Convert datetime objects to string if needed
        if isinstance(last_q, (datetime.datetime, pd.Timestamp)):
            last_q = last_q.strftime('%Y-%m-%d')
        
        # 2. Fallback: Peek at the QUARTERLY keys if metadata is missing/empty
        if not last_q:
            if "CONSOLIDATED" in document and document["CONSOLIDATED"].get("QUARTERLY"):
                keys = list(document["CONSOLIDATED"]["QUARTERLY"].keys())
                if keys: last_q = keys[-1]
            elif "STANDALONE" in document and document["STANDALONE"].get("QUARTERLY"):
                keys = list(document["STANDALONE"]["QUARTERLY"].keys())
                if keys: last_q = keys[-1]
        
        # Final comparison
        if last_q:
            last_announced_quarter1 = last_q
            if str(last_q) == recent_quarter_txt or str(last_q) == last_quarter_text:
                latest_quarterly_stocks.append(key)
            else:
                not_latest_quarterly.append(key)
        else:
            not_latest_quarterly.append(key)

    return send_metadata, latest_quarterly_stocks, last_announced_quarter1, available_stocks, not_latest_quarterly

def insert_stock_metadata(col,dict,id):
    try:
        dict["_id"] = id
        dict['timestamp'] = (datetime.datetime.now())
        # check if dict['Code'] is already available in the database, and update that record
        if col.count_documents({"Code": dict['Code']}):
            col.find_one_and_update({"Code": dict['Code']}, {"$set": dict})
        else:
            col.insert_one(dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")



def create_doc(id_value, dict,col):
    # st.success(dict)
    try:
        dict["_id"] = id_value
        dict['timestamp'] = (datetime.datetime.now())
        if col.count_documents({"_id": id_value}):
            # st.success(col.find_one({"_id": id_value}))
            col.find_one_and_update({"_id": id_value}, {"$set": dict})
        else:
            col.insert_one(dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")



#processes dict values
def insert_dict(col, id_value, save_within_document, dict,task):
    try:
        # check if dict['Code'] is already available in the database, and update that record
        #the below code directly replaces
        if task == 'REPLACE':
            if col.count_documents({"_id": id_value}):
                #in the beow code line, want to save the dict in this result["Yearly"]["Consoilidated"]?
                col.find_one_and_update({"_id": id_value},{"$set": {save_within_document: dict}})            
                # check if dict['Code'] is already available in the database, and update that record
            else:
                my_dict = {}
                my_dict["_id"] = id_value
                my_dict[save_within_document] = dict
                col.insert_one(dict)            
        
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def insert_list(id_value,list_data):
    try:
        industry_name = id_value
        col = industry_col
        my_dict = {industry_name : list_data}
        my_dict["_id"] = industry_name
        #check if database already has key value with industry_name
        if col.count_documents({industry_name: {"$exists": True}}):
            #lets get the existing list in the database
            existing_list = col.find_one({industry_name: {"$exists": True}})[industry_name]
            # add existing list with new list_data and remove the duplicate values
            new_list = list(set(existing_list + list_data))
            col.find_one_and_update({industry_name: {"$exists": True}}, {"$set":
                                                                         {industry_name: new_list}})
        else:
            col.insert_one(my_dict)

    except:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")
    




# def insert_EODdf(df):
#     try:
#         # Assuming df['DATE'][0] contains the condition for deletion
#         # Convert the integer date to a datetime object
#         print(df['DATE'][0])
#         print(str(document['DATE']))
#         date_from_df = datetime.strptime(str(df['DATE'][0]), '%Y%m%d')
#         print(date_from_df)
#         # Convert the integer date from the MongoDB document to a datetime object
#         document = eod_df_col.find_one({}, {'DATE': 1})
#         date_from_mongodb = datetime.strptime(str(document['DATE']), '%Y%m%d')
#         print(date_from_mongodb)
#         # Compare the datetime objects
#         if date_from_df > date_from_mongodb:
#             # Delete documents in the collection based on your condition
#             eod_df_col.delete_many({'DATE': {'$gte': df['DATE'][0]}})
#             write(eod_df_col,df)
#             #for doc in eod_df_col.find({}):
#                 #pprint.pprint(doc)

#     except pymongo.errors.ServerSelectionTimeoutError:
#         print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def insert_topic(topic_dict):
    try:
        topics_col.insert_one(topic_dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def insert_reco(dict):
    try:
        reco_col.insert_one(dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def insert_pf(dict):
    try:
        pf_col.insert_one(dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def insert_gtt(dict):
    try:
        gtt_col.insert_one(dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

def del_db(col,field):
    try:
        col.delete_many({"date":field})
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")


if __name__ == "__main__":
    # List databases
    databases = client.list_database_names()
    #print("Databases: {}".format(databases))
    date_in_db = "05012023"
    fileid1 = "NSEsuccessful"
    fileid2 = "INDEXsuccessful"
    fileid3 = "BSE Succesful"
    #insert_db(NSE_col, fileid1, date)
    #insert_db(INDEX_col, fileid2, date)
    #insert_db(BSE_col,fileid3,date)

    if NSE_col.count_documents({"date":date_in_db}):
        get_data =  NSE_col.find_one({"date":date_in_db})
        print(get_data)
        print(type(get_data))
        print(f'we got fileid for ' + get_data['date'] + ' : ' + get_data['file_id'])
    else :
        print("files doesnt exist")

    '''
    if hasattr(db, 'NSEbhav'):          # gives TRUE
        insert_db(db, NSE_col, fileid1, date)
    '''

    client.close()
