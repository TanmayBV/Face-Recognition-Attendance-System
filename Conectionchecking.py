import mysql.connector
from mysql.connector import Error

# Replace with your MySQL server details
host="sql200.infinityfree.com",
user="if0_37728532",
password="P4rex01234",
database="if0_37728532_employee_db"  # Optional, can be None

def check_mysql_connection(host, user, password, database=None):
    """
    Checks the connection to a MySQL database.
    
    Parameters:
    - host: The hostname or IP address of the MySQL server.
    - user: The MySQL username.
    - password: The MySQL password.
    - database: (Optional) The specific database to connect to.
    
    Returns:
    - None: Prints the status of the connection.
    """
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            server_info = connection.get_server_info()
            print(f"Successfully connected to MySQL server version {server_info}.")
            if database:
                print(f"Connected to database: {database}")
        else:
            print("Failed to connect to the MySQL server.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")



# Check the connection
check_mysql_connection(host, user, password, database)
