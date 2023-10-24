# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime
import pymongo
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Define your MongoDB and PostgreSQL connection settings
mongo_host = 'mongodb://demo.hive-worx.com:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'  # Replace with your MongoDB connection string
mongo_db_name = 'db_igt'  # Replace with your MongoDB database name
mongo_collection_name = 'property_type'  # Replace with your MongoDB collection name

pg_host = '192.168.2.49'  # Replace with your PostgreSQL host
pg_port = '5432'  # Replace with your PostgreSQL port
pg_db_name = 'BI_Data'  # Replace with your PostgreSQL database name
pg_user = 'postgres'  # Replace with your PostgreSQL username
pg_password = 'Red*St0ne'  # Replace with your PostgreSQL password


# Function to extract data from MongoDB
def extract_data():
    mongo_client = pymongo.MongoClient(mongo_host)
    mongo_db = mongo_client[mongo_db_name]
    mongo_collection = mongo_db[mongo_collection_name]
    # for i in  mongo_collection.find({"project_id": {"$exists": True}}):
    select_by_balance = {
        '$match': {
            '_id': {
                '$exists': True
            }, 'dml_status': {
                '$ne': 2
            }
        }
    }

    # TODO 2: fields to inlcude
    fields_to_include = {
        '$project': {
            '_id': 1,
            'hint': 1,
            'title': 1,
            'description': 1,
            'user_id': 1,
            'value_type': 1,
            'root_property_type_id': 1,
            'property_category': 1

        }
    }

    # TODO 3: Create an aggegation pipeline using 'select_by_balance' and 'separate_by_account_calculate_avg_balance'.
    pipeline = [
        select_by_balance,
        fields_to_include]

    # TODO 4: Perform an aggregation on 'pipeline'.
    results = mongo_collection.aggregate(pipeline)
    dict = []

    for item in results:
        dict.append(item)
    df = pd.DataFrame(dict)
    return df


# print(extract_data())

# Function to load data into PostgreSQL
def load_data(df):
    pg_connection = psycopg2.connect(
        host=pg_host,
        port=pg_port,
        dbname=pg_db_name,
        user=pg_user,
        password=pg_password
    )
    # data.to_sql('property_type',pg_connection, if_exists='append', index=False, schema='public')
    # try:
    #     cursor = pg_connection.cursor()
    #     cursor.execute('truncate table property_type')
    #     cursor.execute('select _id from property_type')
    #     for i in cursor.fetchall():
    #         print('result')
    #         print(i)
    #
    # except Exception as e:
    #     print(e)


    engine = create_engine('postgresql+psycopg2://postgres:Red*St0ne@192.168.2.49:5432/BI_Data')
    engine.connect()
    # # # print(df.shape)

    df.to_sql('property_type', engine, if_exists='replace', index=False, schema='public', method='multi', chunksize=1000)
    engine.dispose()
df=extract_data()
# print(df)
load_data(df)
# # Define default arguments for the DAG
# default_args = {
#     'owner': 'Abdul Wasay',
#     'start_date': datetime.now(),
#     'retries': 1,
# }
#
# # # Create a DAG instance
# dag = DAG(
#     'property_type',
#     default_args=default_args,
#     schedule=None,  # Set the schedule interval (or use a trigger or None)
#     catchup=False,
# )
#
# # # Define tasks
# extract_task = PythonOperator(
#     task_id='extract_data_task',
#     python_callable=extract_data,
#     dag=dag,
# )
#
# load_task = PythonOperator(
#     task_id='load_data_task',
#     python_callable=load_data,
#     op_args=[extract_task.output],  # Pass the output of the extract task as input to the load task
#     dag=dag,
# )
#
# # # Set task dependencies
# extract_task >> load_task