import pprint
from datetime import datetime
import pandas as pd
from pymongo.mongo_client import MongoClient
from pandas import json_normalize
# Replace the placeholder with your Atlas connection string
uri = "mongodb://demo.hive-worx.com:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.test_db
# for i in client.list_database_names():
#     print(i)
db = client.db_igt
accounts_collection = db.object
# Calculate the average balance of checking and savings accounts with balances of less than $1000.

# TODO 1: Select accounts with balances of less than $1000.
select_by_balance = {'$match': {'project_id': {'$exists': True}}}


# TODO 2: fields to inlcude
fields_to_include =  {
        '$project': {
            '_id': 1,
            'project_id': 1,
            'project_title': 1,
            'user_id': 1,
            'user_name': 1,
            'role_id': 1,
            'role_title': 1,
            'title': 1,
            'description': 1,
            'lifecycle_status': 1,
            'object_type._id': 1,
            'object_type.object_type_id': 1,
            'object_type.title': 1
        }
    }


# TODO 3: Create an aggegation pipeline using 'select_by_balance' and 'separate_by_account_calculate_avg_balance'.
pipeline = [
  select_by_balance,
  fields_to_include]

# TODO 4: Perform an aggregation on 'pipeline'.
results = accounts_collection.aggregate(pipeline)




dict=[]
for item in results:

    dict.append(item)
    break






df = json_normalize(dict,  sep='_')
print(df.columns)
# df.to_csv('test1.csv')
client.close()


