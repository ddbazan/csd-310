"""
    Author: Tyler Moon, Destiny Bazan, Cassuany Noel
    Date: 24 February 2025
    Description: Winery database initialization script.
"""

import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    "user": "root",
    "password": "Jayden.2046291",
    "host": "localhost",  # Adjust as needed
}

# Test connection and create database
try:
    # Attempt to connect to MySQL server with the provided config
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # Create the Winery database and select it
    cursor.execute("CREATE DATABASE IF NOT EXISTS Winery")
    cursor.execute("USE Winery")
    
    print("Connected to the database and selected Winery")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
    exit(1)

# Function to run SQL commands from a file
def execute_sql_file(filename):
    with open(filename, 'r') as file:
        sql_commands = file.read().split(';')  # Split commands by semicolon
        for command in sql_commands:
            command = command.strip()  # Remove whitespace
            if command:  # Check if the command is not empty
                try:
                    cursor.execute(command)
                except mysql.connector.Error as e:
                    print(f"Error executing command: {command} - {e}")

# Replace the original call with the absolute path to your SQL file
execute_sql_file(r'C:\CSD\csd_310\module_11\db_init_2025.sql')

# Commit all changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()
print("Database initialized and data inserted successfully.")