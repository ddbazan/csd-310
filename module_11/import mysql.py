import mysql.connector

try:
    connection = mysql.connector.connect(
        user= 'winery_user',
        password= 'Jayden.2046291',
        host= '127.0.0.1',
        database= 'winery'
    )
    print("Connected to the database.")
    connection.close()
except mysql.connector.Error as err:
    print(err)