"""
    Author: Tyler Moon, Destiny Bazan, Cassuany Noel
    Date: 24 February 2025
    Description: Winery database initialization script.
"""
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration
config = {
    "user": os.getenv("USER"),          # These will be loaded from the .env file
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),          # Should be '127.0.0.1' to avoid named pipes
    "database": os.getenv("DATABASE"),
}

# Test connection and create database
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # Create the Winery database if it does not exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS Winery")
    cursor.execute("USE Winery")
    
    print("Connected to the database and selected Winery")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        # Instead of printing sensitive info, describe the error
        print("Error: Access denied. Please check your username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: The specified database does not exist.")
    else:
        print(f"Error: {err}")  # Print other errors without detail
    exit(1)

# Continue with your SQL operations...

# Function to run SQL commands from a file
def execute_sql_file(filename):
    with open(filename, 'r') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except mysql.connector.Error as e:
                    print(f"Error executing command: {command} - {e}")

# Replace with the path to your SQL file
execute_sql_file(r'C:\CSD\csd_310\module_11\db_init_2025.sql')

# Commit all changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()
print("Database initialized and data inserted successfully.")