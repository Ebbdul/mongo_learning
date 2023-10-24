import pprint
from datetime import datetime

from pymongo.mongo_client import MongoClient

# Replace the placeholder with your Atlas connection string
uri = "mongodb://demo.hive-worx.com:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
#
# except Exception as e:
#     print(e)


# list databses name
# for db_names in client.list_database_names():
#     print(db_names)

db = client["db_igt"]
# print(db)

accounts_collection = db.object
# print(accounts_collection)
# print(accounts_collection.find_one({"project_id": {"$exists": True, "$ne": None}}))
for i  in accounts_collection.find({"project_id": {"$exists": True, "$ne": None}}):
    print(i)
# new_account = [{
#     "account_holder": "Torvalds",
#     "account_id": "MDB829001337",
#     "account_type": "checking",
#     "balance": 50352434,
#     "last_updated": datetime.utcnow(),
# },
#     {
#         "account_holder": "Linus ",
#         "account_id": "MDB829001337",
#         "account_type": "checking",
#         "balance": 50352434,
#         "last_updated": datetime.utcnow(),
#     }
# ]

# # Write an expression that inserts the 'new_account' document into the 'accounts' collection.
# result = accounts_collection.insert_many(new_account)

# document_ids = result.inserted_ids
# print("# of documents inserted: " + str(len(document_ids)))
# print(f"_ids of inserted documents: {document_ids}")

client.close()