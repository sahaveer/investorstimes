import pandas as pd
import pymongo
from pymongo import MongoClient
import datetime
# CONNECTION STRING : mongodb+srv://EODBhavcopy:bhavcopy@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority
# client = pymongo.MongoClient("mongodb+srv://EODBhavcopy:<password>@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority")
# db = client.test
global my_dict
global db
global db2
global NSE_col
global BSE_col
global INDEX_col
global userid_col
global topics_col
global OI_col
global eod_df_col
global company_metadata_col
from datetime import date
import pprint

my_dict = {}
# CREATING AND CONNECTING TO DATABASE
Connection_String = "mongodb+srv://EODBhavcopy:bhavcopy@eodbhavcopy.4tbvocy.mongodb.net/?retryWrites=true&w=majority"
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
company_metadata_col = db2["CompanyMetadata"]
# print(list(company_metadata_col.find()))
pfaccess_col = db["PFaccess"]
gtt_col = db["GTT"]
watchlist_col = db["Watchlist"]
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

@st.cache_data
def get_metadata():
    print("Trying to get data from PYMONGODB")
    send_metadata = {}
    for document in company_metadata_col.find():
        key = document['_id']
        send_metadata[key] = document
    # st.success(send_metadata)
    return send_metadata


def insert_stock_metadata(dict):
    try:
        col = company_metadata_col
        dict["_id"] = dict['Code']
        dict['timestamp'] = (datetime.datetime.now())
        # check if dict['Code'] is already available in the database, and update that record
        if col.count_documents({"Code": dict['Code']}):
            col.find_one_and_update({"Code": dict['Code']}, {"$set": dict})
        else:
            col.insert_one(dict)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Hey buddy, we Couldnt update to the Database. \nOpen NETWORK ACCESS in MongoDB and add your IP address")

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
