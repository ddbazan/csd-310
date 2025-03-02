"""
Tyler Moon, Destiny Bazan, Cassiany Noel
02/27/2025
Assignment 11.1
"""
import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    "user": "root",  # Replace with your actual MySQL username
    "password": "Jayden.2046291",  # Replace with your actual MySQL password
    "host": "localhost",  # Adjust as needed
    "database": "Winery",  # Ensure this database exists
}

# Connect to the database
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    print("Connected to the database.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
    exit(1)

# 1. Report Tracking Supplier Performance
def supplier_performance_report():
    query = """
    SELECT 
        S.Name as SupplierName,
        SO.OrderDate,
        SO.ExpectedDelivery,
        SO.ActualDelivery,
        DATEDIFF(SO.ActualDelivery, SO.ExpectedDelivery) as DeliveryDifference
    FROM 
        Supplier S
    JOIN 
        SupplyOrder SO ON S.SupplierID = SO.SupplierID
    WHERE 
        SO.ExpectedDelivery IS NOT NULL
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nSupplier Performance Report")
    print("-" * 50)
    for row in results:
        print(f"Supplier: {row[0]}, Order Date: {row[1]}, Expected Delivery: {row[2]}, Actual Delivery: {row[3]}, Delivery Difference: {row[4]} days")
    
# 2. Wine Sales by Type and Distributor
def wine_sales_report():
    query = """
    SELECT 
        W.WineName,
        W.WineType,
        D.Name as DistributorName,
        SUM(SR.SalesVolume) as TotalSales
    FROM 
        Wine W
    JOIN 
        WineDistribution WD ON W.WineID = WD.WineID
    JOIN 
        Distributor D ON WD.DistributorID = D.DistributorID
    JOIN 
        SalesReport SR ON W.WineID = SR.WineID
    GROUP BY 
        W.WineName, W.WineType, D.Name
    ORDER BY 
        TotalSales DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nWine Sales Report")
    print("-" * 50)
    best_selling = {}
    worst_selling = {}
    
    for row in results:
        print(f"Wine: {row[0]}, Type: {row[1]}, Distributor: {row[2]}, Total Sales: {row[3]}")
        
        # Tracking best and worst selling wines
        if row[1] not in best_selling:
            best_selling[row[1]] = (row[0], row[3])
            worst_selling[row[1]] = (row[0], row[3])
        else:
            if row[3] > best_selling[row[1]][1]:
                best_selling[row[1]] = (row[0], row[3])
            if row[3] < worst_selling[row[1]][1]:
                worst_selling[row[1]] = (row[0], row[3])
    
    print("\nBest Selling Wines by Type:")
    for wine_type, data in best_selling.items():
        print(f"Type: {wine_type}, Wine: {data[0]}, Total Sales: {data[1]}")
        
    print("\nWorst Selling Wines by Type:")
    for wine_type, data in worst_selling.items():
        print(f"Type: {wine_type}, Wine: {data[0]}, Total Sales: {data[1]}")
    
# 3. Employee Hours Report
def employee_hours_report():
    query = """
    SELECT 
        E.Name, 
        SUM(E.WorkWeekHours) as TotalHours
    FROM 
        Employee E
    GROUP BY 
        E.Name
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nEmployee Hours Report (Last Four Quarters)")
    print("-" * 50)
    for row in results:
        print(f"Employee: {row[0]}, Total Hours Worked: {row[1]} hours")

# Generate reports
supplier_performance_report()
wine_sales_report()
employee_hours_report()

# Close the cursor and connection
cursor.close()
connection.close()