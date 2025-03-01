import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values

secrets = dotenv_values(".env")

config = {
	"user": "movies_user",
	"password": "popcorn",
	"host": "localhost",
	"database": "movies",
	"raise_on_warnings": True
}
try:
	db = mysql.connector.connect(**config)
	print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
	input("\n\n  Press any key to continue...")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("  The supplied username or password is invalid")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("  The specified database does not exist")
	else:
		print(f"Error: {err}")
finally:
	if 'db' in locals():
		db.close()