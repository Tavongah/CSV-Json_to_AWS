from pymongo import MongoClient
from pymongo.errors import PyMongoError
from urllib.parse import quote_plus

# Connection details
username = "tavongad"
password = quote_plus("Email1999?")  # URL encode the password
host = "documentdb1-537124946394.us-east-2.docdb-elastic.amazonaws.com"
port = 27017

# Create the connection string
connection_string = f"mongodb://{username}:{password}@{host}:{port}/?ssl=true"

client = None  # Initialize client to None

try:
    # Create a MongoClient
    client = MongoClient(connection_string)

    # Create a new database
    database_name = "mongodb1"  # Replace with your desired database name
    db = client[database_name]

    # Optionally, create a collection to ensure the database is created
    collection = db['new_collection1']  # Replace with your desired collection name
    collection.insert_one({"example_key": "example_value"})  # Insert a sample document

    print(f"Database '{database_name}' created with a collection '{collection.name}'.")

except PyMongoError as e:
    print("An error occurred while connecting to MongoDB:", e)

finally:
    if client is not None:
        client.close()

