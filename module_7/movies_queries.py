import mysql.connector
from mysql.connector import Error
#connect to database
try:
    conn = mysql.connector.connect(
        host = "localhost", 
        database = "movies",
        user = "movies_user",
        password = "popcorn"
    )
    cur = conn.cursor()

    #Query 1: selecting all fields from the studio table
    cur.execute("SELECT * FROM studio;")
    studios = cur.fetchall()
    for studio in studios:
        print(studio)

    #Query 2: selecting all fields from the genre table
    cur.execute("SELECT * FROM genre;")
    genres = cur.fetchall()
    for genre in genres:
        print(genre)

#Query 3: Select movie names with a run time of less than 120 minutes

    cur.execute("SELECT film_name from film WHERE film_runtime < 120;")
    short_movies = cur.fetchall()
    for movie in short_movies:
        print(movie[0])

#Query 4: Select film names and directors, showing all films by each director
    cur.execute("SELECT film_director, GROUP_CONCAT(film_name ORDER BY film_name SEPARATOR ', ') AS films FROM film GROUP BY film_director;")
    directors_grouped = cur.fetchall()
    for entry in directors_grouped:
        print(f"Director: {entry[0]}, Films: {entry[1]}")
    # Close the connection
    conn.close()
except Error as e:
    print(f"Error: '{e}' occurred")