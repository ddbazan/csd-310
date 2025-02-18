import mysql.connector
from mysql.connector import Error

# Database connection configuration (adapt to your .env or direct config)
config = {
    "host": "localhost",
    "database": "movies",
    "user": "movies_user",
    "password": "popcorn" 
}

def show_films(cursor, title):
    """
    Displays film information with a given title.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor object.
        title (str): The title to display for the output.
    """
    print(f"\n--- {title} ---")
    try:
        select_statement = """
        SELECT
            f.film_name AS Name,
            f.film_director AS Director,
            g.genre_id,
            g.genre_name,
            s.studio_name
        FROM
            film f
        INNER JOIN
            genre g ON f.genre_id = g.genre_id
        INNER JOIN
            studio s ON f.studio_id = s.studio_id
        """
        cursor.execute(select_statement)
        results = cursor.fetchall()

        if results:
            for row in results:
                if row[0] == 'Gladiator':
                    print(f"film name: {row[0]} Director: {row[1]} Genre ID: {row[2]} Studio Name: {row[4]}")
                elif row[0] == 'Alien':
                    print(f"film name: {row[0]} Director: {row[1]} Genre Name ID: {row[3]} Studio Name: {row[4]}")
                elif row[0] == 'The Matrix':
                    print(f"film name: {row[0]} Director: {row[1]} Genre Name ID: {row[3]} Studio Name: {row[4]}")
                else:
                    print(f"Name: {row[0]}, Director: {row[1]}, Genre: {row[2]}, Studio: {row[3]}")
        else:
            print("No films found in the database.")

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")

def insert_film(cursor, film_name, film_director, genre_name, studio_name, conn):
    """
    Inserts a new film record into the database.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor object.
        film_name (str): The name of the film to insert.
        film_director (str): The director of the film.
        genre_name (str): The name of the genre.
        studio_name (str): The name of the studio.
        conn (mysql.connector.connection.MySQLConnection): The database connection object.
    """
    try:
        genre_query = "SELECT genre_id FROM genre WHERE genre_name = %s"
        cursor.execute(genre_query, (genre_name,))
        genre_result = cursor.fetchone()
        if not genre_result:
            print(f"Error: Genre '{genre_name}' not found.")
            return
        genre_id = genre_result[0]

        studio_query = "SELECT studio_id FROM studio WHERE studio_name = %s"
        cursor.execute(studio_query, (studio_name,))
        studio_result = cursor.fetchone()
        if not studio_result:
            print(f"Error: Studio '{studio_name}' not found.")
            return
        studio_id = studio_result[0]

        insert_statement = """
        INSERT INTO film (film_name, film_director, genre_id, studio_id)
        VALUES (%s, %s, %s, %s)
        """
        film_data = (film_name, film_director, genre_id, studio_id)
        cursor.execute(insert_statement, film_data)
        conn.commit()
        print(f"\n--- Inserted '{film_name}' ---")
    except mysql.connector.Error as err:
        print(f"Error inserting film: {err}")
        conn.rollback()

def update_film_genre(cursor, film_name, genre_name, conn):
    """
    Updates a film's genre.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor object.
        film_name (str): The name of the film to update.
        genre_name (str): The new genre for the film.
        conn (mysql.connector.connection.MySQLConnection): The database connection object.
    """
    try:
        genre_query = "SELECT genre_id FROM genre WHERE genre_name = %s"
        cursor.execute(genre_query, (genre_name,))
        genre_result = cursor.fetchone()
        if not genre_result:
            print(f"Error: Genre '{genre_name}' not found.")
            return
        genre_id = genre_result[0]

        update_statement = """
        UPDATE film
        SET genre_id = %s
        WHERE film_name = %s
        """
        update_data = (genre_id, film_name)
        cursor.execute(update_statement, update_data)
        conn.commit()
        print(f"\n--- Updated '{film_name}' to '{genre_name}' ---")
    except mysql.connector.Error as err:
        print(f"Error updating film: {err}")
        conn.rollback()

def delete_film(cursor, film_name, conn):
    """
    Deletes a film from the database.

    Args:
        cursor (mysql.connector.cursor.MySQLCursor): The database cursor object.
        film_name (str): The name of the film to delete.
        conn (mysql.connector.connection.MySQLConnection): The database connection object.
    """
    try:
        delete_statement = "DELETE FROM film WHERE film_name = %s"
        cursor.execute(delete_statement, (film_name,))
        conn.commit()
        print(f"\n--- Deleted '{film_name}' ---")
    except mysql.connector.Error as err:
        print(f"Error deleting film: {err}")
        conn.rollback()

def connect_to_database(config):
    """
    Establish a connection to the MySQL database.

    Args:
        config (dict): A dictionary containing the database connection configuration.

    Returns:
        conn (mysql.connector.connection.MySQLConnection): The database connection object.
        cur (mysql.connector.cursor.MySQLCursor): The database cursor object.
    """
    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        print("Connected to the database successfully.")
        return conn, cur
    except Error as e:
        print(f"Error connecting to the database: '{e}'")
        return None, None

def main():
    conn, cur = connect_to_database(config)
    if conn and cur:
        # --- Initial Display ---
        show_films(cur, "DISPLAYING FILMS")

        # --- Insert a New Film ---
        insert_film(cur, "The Matrix", "Lana Wachowski", "Action", "Warner Bros.", conn)

        # --- Display Films After Insert ---
        show_films(cur, "DISPLAYING FILMS AFTER INSERT")

        # --- Update a Film (Alien to Horror) ---
        update_film_genre(cur, "Alien", "Horror", conn)

        # --- Display Films After Update ---
        show_films(cur, "DISPLAYING FILMS AFTER UPDATE")

        # --- Delete a Film (Gladiator) ---
        delete_film(cur, "Gladiator", conn)

        # --- Display Films After Delete ---
        show_films(cur, "DISPLAYING FILMS AFTER DELETE")

        # Close the connection
        cur.close()
        conn.close()
        print("\n--- Database connection closed ---")
    else:
        print("Database connection failed. Exiting.")

if __name__ == "__main__":
    main()