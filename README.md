# CSV-Json_to_AWS
Flask Application for CSV Data Upload to AWS Services
This Flask application provides a web interface to upload CSV files, process the data, and upload it to multiple AWS services, including RDS MySQL, DynamoDB, MongoDB, and Neptune.

Features
Upload CSV Data to AWS RDS MySQL: Inserts data into an existing database and table in MySQL hosted on Amazon RDS.
Integration with AWS DynamoDB: Uploads records to DynamoDB for fast NoSQL storage.
Integration with MongoDB: Uploads records to a MongoDB instance.
Integration with AWS Neptune: Inserts data into a Neptune graph database.
Prerequisites
AWS Account: For RDS, DynamoDB, and Neptune.
MongoDB Instance: A DocumentDB or MongoDB instance (self-hosted or on a service).
Python 3.6+: This application uses Python 3 and requires specific packages listed in requirements.txt.
Setup

Set Up Environment Variables
The application requires environment variables for DynamoDB and Neptune configuration. Set these in your environment or create a .env file:

export DYNAMODB_TABLE_NAME="your_dynamo_table_name"
export NEPTUNE_ENDPOINT="your_neptune_endpoint"
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Update RDS, MongoDB, and AWS Credentials
Edit the application code in app.py and provide your RDS endpoint, MongoDB URI, and AWS credentials:

python
# RDS Configuration
rds_endpoint = 'your-rds-endpoint.amazonaws.com'
rds_username = 'your_rds_username'
rds_password = 'your_rds_password'
rds_database = 'rds_1'   # Name of the existing RDS MySQL database
rds_table_name = 'disease'  # Name of the existing table in the RDS database

# MongoDB Configuration
mongo_username = "your_mongo_username"
mongo_password = "your_mongo_password"
mongo_host = "your_mongo_host"
mongo_port = 27017
mongo_db_name = "your_mongo_db_name"
mongo_collection_name = "your_mongo_collection_name"

Run the Application
python app.py
The application will start on http://0.0.0.0:5000 by default.

Usage
Upload CSV File:

Open the application in your browser at http://localhost:5000.
Use the provided upload form to select and upload a CSV file.
Data Processing:

The uploaded CSV file will be read, and duplicate rows will be removed.
The data will then be uploaded to DynamoDB, MongoDB, Neptune, and RDS MySQL.
Confirm Upload:

After uploading, a success or error message will appear, indicating whether the data was processed and uploaded successfully.
File Structure
app.py: Main Flask application code.
requirements.txt: Lists dependencies to install.
templates/: Contains HTML templates for the web interface.
Dependencies
The following libraries are used in this application:

Flask: Web framework
pandas: Data processing
boto3: AWS SDK for Python (for DynamoDB and Neptune connections)
pymysql: MySQL connection library
pymongo: MongoDB connection library
gremlin_python: Neptune Gremlin connection library
Install these with pip install -r requirements.txt.

Error Handling
RDS Connection Errors: Ensure your RDS endpoint, database name, and credentials are correct.
AWS Authentication: Ensure your AWS credentials are properly configured for accessing DynamoDB and Neptune.
File Format: Only CSV files are supported. Ensure the file structure matches the database schema.
