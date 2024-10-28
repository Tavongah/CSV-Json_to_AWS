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
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import pymysql


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
mongo_host = "documentdb1-537124946394.us-east-2.docdb-elastic.amazonaws.com"
mongo_port = 27017
mongo_db_name = "mongodb1"
mongo_collection_name = "new_collection1"



# RDS configuration
rds_endpoint = 'instance1.c5w8mwik4vdi.us-east-2.rds.amazonaws.com'  # Replace with your RDS endpoint
rds_username = 'admin'    # Replace with your RDS username
rds_password = 'Email1999?'     # Replace with your RDS password
rds_database = 'rds_1'         # Existing RDS database name
rds_table_name = 'disease'    # Existing table name



# Create MongoDB connection string
mongo_connection_string = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?ssl=true"
mongo_client = MongoClient(mongo_connection_string)
mongo_db = mongo_client[mongo_db_name]
mongo_collection = mongo_db[mongo_collection_name]

# Neptune configuration
neptune_endpoint = os.environ.get('NEPTUNE_ENDPOINT', 'db-neptune-1.cluster-ro-c5w8mwik4vdi.us-east-2.neptune.amazonaws.com')
graph = Graph()
neptune_conn = DriverRemoteConnection(f'wss://{neptune_endpoint}/gremlin', 'g')

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



def upload_to_neptune(dataframe):
    try:
        # Connect to Neptune
        g = graph.traversal().withRemote(neptune_conn)
        
        for index, row in dataframe.iterrows():
            # Use Age as the unique identifier
            vertex_id = str(row['Age'])  # Convert Age to string if needed

            # Start creating the vertex
            vertex = g.addV('Person').property('id', vertex_id).property('Age', row['Age'])

            # Add other properties
            for prop_key in dataframe.columns:
                if prop_key != 'Age':
                    vertex.property(prop_key, row[prop_key])

            # If there is a relationship, handle it accordingly (if applicable)
            # For example, if you have a column that signifies a relationship:
            if 'relationship' in row and pd.notnull(row['relationship']):
                relationship = row['relationship']
                g.V(vertex_id).addE('knows').to(g.V(relationship)).next()  # Adjust based on your schema

        logging.info("Uploaded data to AWS Neptune")
    
    except Exception as e:
        logging.error(f"Error uploading to Neptune: {e}")
        raise  # Optionally re-raise to handle higher up in the call stack
    



def upload_to_rds(dataframe):
    try:
        # Connect to the RDS instance
        connection = pymysql.connect(
            host=rds_endpoint,
            user=rds_username,
            password=rds_password,
            database=rds_database
        )
        cursor = connection.cursor()

        # Insert data into the table
        for index, row in dataframe.iterrows():
            insert_query = f"""
            INSERT INTO {rds_table_name} (Age, Gender, Polyuria, Polydipsia, sudden_weight_loss,
            weakness, Polyphagia, Genital_thrush, visual_blurring, Itching, Irritability,
            delayed_healing, partial_paresis, muscle_stiffness, Alopecia, Obesity, class)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        logging.info(f"Uploaded {len(dataframe)} items to RDS MySQL")

    except Exception as e:
        logging.error(f"Error uploading to RDS: {e}")

    finally:
        cursor.close()
        connection.close()

        




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

        # Upload to databases
        upload_to_dynamodb(df)
        upload_to_mongodb(df)
        upload_to_neptune(df)
        upload_to_rds(df)

        return render_template('index.html', message='File processed and uploaded successfully.')

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return render_template('index.html', message='An error occurred while processing the file.')
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up the temporary file

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

