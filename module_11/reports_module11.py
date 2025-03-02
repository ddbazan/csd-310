"""
Tyler Moon, Destiny Bazan, Cassiany Noel
02/27/2025
Assignment 11.1
"""
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load environment variables from .env file
secrets = dotenv_values(".env")

# Database configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],          # Ensure this is '127.0.0.1' to use TCP
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

# Test connection
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    print(f"Connected to database: {config['database']}")  # Notify successful connection
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Access denied. Please check your username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: The specified database does not exist.")
    else:
        print(f"Error: {err}")  # Print other generic errors
    exit(1)  # Exit if connection fails

# Report 1: Supplier performance tracking (expected vs. actual delivery dates)
def report_supplier_performance():
    print("\n--- Report 1: Supplier Performance (Expected vs. Actual Delivery Dates) ---")
    cursor.execute("""
        SELECT supplier_id, 
               COUNT(*) AS total_orders,
               SUM(CASE WHEN actual_delivery_date <= expected_delivery_date THEN 1 ELSE 0 END) AS on_time_deliveries
        FROM Deliveries
        GROUP BY supplier_id
    """)
    
    rows = cursor.fetchall()
    
    print("Supplier ID | Total Orders | On-Time Deliveries")
    print("-" * 50)
    
    for supplier_id, total_orders, on_time_deliveries in rows:
        print(f"{supplier_id} | {total_orders} | {on_time_deliveries}")
    print("-" * 50)

# Report 2: Wine sales by type and distributor
def report_wine_sales():
    print("\n--- Report 2: Wine Sales by Type and Distributor ---")
    
    cursor.execute("""
        SELECT wine_type, distributor_id, 
               COUNT(*) AS wine_count
        FROM Sales 
        JOIN Wines ON Sales.wine_id = Wines.id 
        GROUP BY wine_type, distributor_id
        ORDER BY wine_count DESC
    """)
    
    rows = cursor.fetchall()
    
    print("Wine Type | Distributor ID | Wine Count")
    print("-" * 50)
    
    for wine_type, distributor_id, wine_count in rows:
        print(f"{wine_type} | {distributor_id} | {wine_count}")
    
    print("-" * 50)

# Report 3: Number of hours worked by each employee over the last four quarters
def report_hours_worked():
    print("\n--- Report 3: Hours Worked by Each Employee Over the Last Four Quarters ---")
    
    cursor.execute("""
        SELECT employee_id, 
               SUM(hours_worked) AS total_hours,
               COUNT(DISTINCT week_id) AS weeks_tracked
        FROM Hours
        WHERE week_id >= DATE_SUB(NOW(), INTERVAL 1 YEAR) 
        GROUP BY employee_id
    """)
    
    rows = cursor.fetchall()
    
    print("Employee ID | Total Hours | Weeks Tracked")
    print("-" * 50)
    
    for employee_id, total_hours, weeks_tracked in rows:
        print(f"{employee_id} | {total_hours} | {weeks_tracked}")
    print("-" * 50)

# Execute Reports
report_supplier_performance()
report_wine_sales()
report_hours_worked()

# Close the cursor and connection when done
cursor.close()
connection.close()
print("Reports generated successfully.")