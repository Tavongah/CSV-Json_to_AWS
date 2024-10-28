from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
import os
import boto3
from botocore.exceptions import ClientError
import logging
import json
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from urllib.parse import quote_plus

app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
dynamo_table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'customers1')
dynamo_table = dynamodb.Table(dynamo_table_name)

# Initialize MongoDB
mongo_username = "tavongad"
mongo_password = quote_plus("Email1999?")
mongo_host = "documentdb1-537124946946.us-east-2.docdb-elastic.amazonaws.com"
mongo_port = 27017
mongo_db_name = "mongodb1"
mongo_collection_name = "new_collection1"

# Create MongoDB connection string
mongo_connection_string = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?ssl=true"
mongo_client = MongoClient(mongo_connection_string)
mongo_db = mongo_client[mongo_db_name]
mongo_collection = mongo_db[mongo_collection_name]

def upload_to_dynamodb(dataframe):
    for index, row in dataframe.iterrows():
        item = row.to_dict()
        try:
            dynamo_table.put_item(Item=item)
            logging.info(f"Uploaded item {item} to DynamoDB")
        except ClientError as e:
            logging.error(f"Error uploading to DynamoDB: {e.response['Error']['Message']}")

def upload_to_mongodb(dataframe):
    records = dataframe.to_dict(orient='records')
    try:
        mongo_collection.insert_many(records)
        logging.info(f"Uploaded {len(records)} items to MongoDB")
    except PyMongoError as e:
        logging.error(f"Error uploading to MongoDB: {e}")

def process_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    return df

def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for elem in root.findall('.//'):
        data.append(elem.attrib)
    df = pd.DataFrame(data)
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file_path = os.path.join('/tmp', filename)
    file.save(file_path)

    # Determine file type and process accordingly
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith('.json'):
            df = process_json(file_path)
        elif filename.endswith('.xml'):
            df = process_xml(file_path)
        else:
            return "Unsupported file type. Please upload a CSV, JSON, or XML file.", 400

        # Sanitize data
        df = df.drop_duplicates().fillna('')
        
        # Upload to DynamoDB and MongoDB
        upload_to_dynamodb(df)
        upload_to_mongodb(df)

        return render_template('index.html', message='File processed and uploaded successfully.')
    
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return render_template('index.html', message='An error occurred while processing the file.')

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up the temporary file

if __name__ == '__main__':
    app.run(debug=True)

