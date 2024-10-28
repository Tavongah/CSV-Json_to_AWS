import mysql.connector
from mysql.connector import errorcode

# AWS RDS MySQL instance details
rds_endpoint = 'instance1.c5w8mwik4vdi.us-east-2.rds.amazonaws.com'  
db_user = 'admin'
db_password = 'Email1999?'
db_name = 'rds_1'

try:
    # Connect to the MySQL RDS instance
    connection = mysql.connector.connect(
        host=rds_endpoint,
        user=db_user,
        password=db_password
    )
    cursor = connection.cursor()

    # Create a new database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database '{db_name}' created successfully or already exists.")

    # Use the new database
    cursor.execute(f"USE {db_name}")

    # Create a new table in the new database
    create_table_query = """
    CREATE TABLE IF NOT EXISTS disease (
            Age INT,
            Gender VARCHAR(10),
            Polyuria VARCHAR(3),
            Polydipsia VARCHAR(3),
            sudden_weight_loss VARCHAR(3),
            weakness VARCHAR(3),
            Polyphagia VARCHAR(3),
            Genital_thrush VARCHAR(3),
            visual_blurring VARCHAR(3),
            Itching VARCHAR(3),
            Irritability VARCHAR(3),
            delayed_healing VARCHAR(3),
            partial_paresis VARCHAR(3),
            muscle_stiffness VARCHAR(3),
            Alopecia VARCHAR(3),
            Obesity VARCHAR(3),
            class VARCHAR(10)
    )
    """
    cursor.execute(create_table_query)
    print("Table 'users' created successfully or already exists.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access denied: Incorrect username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(f"Error: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

