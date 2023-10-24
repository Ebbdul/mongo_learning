import pprint
from datetime import datetime

from pymongo.mongo_client import MongoClient

# Replace the placeholder with your Atlas connection string
uri = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.test_db
# for i in client.list_database_names():
#     print(i)
db = client.test_db
accounts_collection = db.accounts
# Return the account type, original balance, and balance converted to Great British Pounds (GBP) of all checking accounts with an original balance of greater than $1,500 US dollars, in order from highest original balance to lowest.

# To calculate the balance in GBP, divide the original balance by the conversion rate.
conversion_rate_usd_to_gbp = 1.3

# TODO 1: Select checking accounts with balances of more than $1,500.
select_accounts = {"$match": {"account_type": "checking", "balance": {"$gt": 1500}}}

# TODO 2: Organizes documents in order from highest balance to lowest.
organize_by_original_balance = {"$sort": {"balance": -1}}

# TODO 3: Return only the account type & balance fields, plus a new field containing balance in Great British Pounds (GBP). Name the new field "gbp_balance".
return_specified_fields = {
    "$project": {
        "account_type": 1,
        "balance": 1,
        "gbp_balance": {"$divide": ["$balance", conversion_rate_usd_to_gbp]},
        "_id": 0,
    }
}

# TODO 4: Create an aggegation pipeline containing the four stages created above.
pipeline = [
    select_accounts,
    organize_by_original_balance,
    return_specified_fields,
]

# TODO 5: Perform an aggregation on 'pipeline'.
results = accounts_collection.aggregate(pipeline)


print(
    "Account type, original balance and balance in GDP of checking accounts with original balance greater than $1,500, in order from highest original balance to lowest: "
)

for item in results:
    pprint.pprint(item)

client.close()