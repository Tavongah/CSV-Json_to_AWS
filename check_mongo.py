from pymongo import MongoClient
from urllib.parse import quote_plus

# MongoDB connection details
mongo_username = "tavongad"
mongo_password = quote_plus("Email1999?")
mongo_host = "documentdb1-537124946394.us-east-2.docdb-elastic.amazonaws.com"
mongo_port = 27017
mongo_db_name = "mongodb1"
mongo_collection_name = "new_collection1"

# Create MongoDB connection string
mongo_connection_string = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?ssl=true"

# Connect to MongoDB
mongo_client = MongoClient(mongo_connection_string)
mongo_db = mongo_client[mongo_db_name]
mongo_collection = mongo_db[mongo_collection_name]

# Fetch all documents from the collection
try:
    documents = mongo_collection.find()
    for doc in documents:
        print(doc)
except Exception as e:
    print(f"Error fetching data from MongoDB: {e}")
finally:
    mongo_client.close()

