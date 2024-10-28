import mysql.connector

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
        password=db_password,
        database=db_name  
    )
    
    cursor = connection.cursor()

    # Query to select all 
    cursor.execute("SELECT * FROM disease")
    
    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Print the retrieved data
    for row in rows:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

