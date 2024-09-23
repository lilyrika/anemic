import sqlite3 as sql
from random import randint

class Database:
    def __init__(self):
        self.conn = sql.connect("database.db")
        self.cur = self.conn.cursor()
        # Initialise connection to SQLite and create cursor

        command = """
        CREATE TABLE IF NOT EXISTS Albums(
        albumid INT,
        name VARCHAR(255),
        artist VARCHAR(255),
        year VARCHAR(255)
        )
        """ 
        self.cur.execute(command)
        # Creates a table named Albums (with integer column albumid, and string columns: name, artist, year) if it doesn't already exist

        command = """
        CREATE TABLE IF NOT EXISTS Genres(
        albumid INT,
        genre VARCHAR(255)
        )
        """
        self.cur.execute(command)
        # Creates a table named Genres (with integer column albumid and string column genre) if it doesn't already exist

        self.conn.commit() # Commits the changes to the database
    
    def add_album(self, name, artist, year, one=False):
        if one == False:
            command = """
            SELECT name, artist, year FROM Albums
            WHERE name = ?1 AND artist = ?2 AND year = ?3
            """
            self.cur.execute(command, (name, artist, year))
        # Checks if the album doesn't already exist, if it fetches None, it doesn't exist
            
            if self.cur.fetchone() == None: # If the album doesn't already exist
                command = """
                INSERT INTO Albums (albumid, name, artist, year)
                SELECT MAX(albumid)+1, ?1, ?2, ?3 FROM Albums
                """ # Adds a record with the parameters given in the add_album() function

                self.cur.execute(command, (name, artist, year)) # Adds album with parameters if album doesn't already exist
                self.conn.commit()

        else:
            command = """
            INSERT INTO Albums (albumid, name, artist, year)
            VALUES(1, ?1, ?2, ?3)
            """

            self.cur.execute(command, (name, artist, year)) # Adds album with parameters if album doesn't already exist, but the albumid is 1
            self.conn.commit()

    def album_profile(self, name):
        command = """
        SELECT albumid, name, artist, year, average_rating FROM Albums
        WHERE ? = LOWER(name)
        """

        self.cur.execute(command, (name.lower(),))
        album_data = self.cur.fetchone() # Fetches selected columns from the record if the name exists in the database

        album_id = album_data[0]
        album_name = album_data[1]
        album_artist = album_data[2]
        album_year = album_data[3]
        album_rating = album_data[4]
        # Creates variables for each data field to be displayed later

        command = "SELECT genre FROM Genres WHERE albumid = ?"
        self.cur.execute(command, (album_id,))
        
        album_genres = []
        for genre_tuple in self.cur.fetchall():
            album_genres.append(genre_tuple[0]) # Appends each genre with matching album ID to a list
        
        print(f"{album_name} - {album_artist}")
        print(album_rating)
        print(*album_genres, sep=', ')
        print(album_year) # Displays the data

    def artist_profile(self, name):
        command = """
        SELECT name, year 
        FROM Albums 
        WHERE LOWER(artist) = ?1 ORDER BY year
        """

        self.cur.execute(command, (name.lower(),))
        albums = self.cur.fetchall() # Fetches all albums under the artist's name and their release year

        command = """
        SELECT artist 
        FROM Albums 
        WHERE LOWER(artist) = ?1
        """

        self.cur.execute(command, (name.lower(),))
        artist = self.cur.fetchone()[0] # Fetches the artist's name with correct capitalisation

        print(artist)
        for album in albums:
            print(*album, sep = " | ") # Displays the data

    def add_genre(self, albumid, genre):
        command = """
        INSERT INTO Genres (albumid, genre) 
        SELECT ?1, ?2
        WHERE NOT EXISTS (SELECT * FROM Genres WHERE albumid = ?1 AND genre = ?2)
        """ 

        self.cur.execute(command, (albumid, genre)) # Adds the new genre to the Genres table if it doesn't already exist
        self.conn.commit()
    
    def genre_profile(self, genre):
        command = """
        SELECT genre 
        FROM Genres 
        WHERE LOWER(genre) = ?1
        """

        self.cur.execute(command, (genre.lower(),)) 
        genre_name = self.cur.fetchone()[0] # Retrieves genre from Genres table if it exists

        command = """
        SELECT DISTINCT name, artist, year, average_rating FROM Albums
        JOIN Genres
        WHERE Genres.albumid = Albums.albumid AND Genres.genre = ?1
        ORDER BY year, name
        """

        self.cur.execute(command, (genre_name,))
        albums = self.cur.fetchall() # Selects every album that has a genre specified in the parameters

        print(f"==== {genre_name} ====")
        for album in albums:
            print(*album, sep=' | ') # Displays the data
    
    def add_rating(self, userid, albumid, rating):
        command = """
        INSERT INTO Ratings (userid, albumid, rating)
        SELECT ?1, ?2, ?3
        WHERE NOT EXISTS (SELECT * FROM Ratings WHERE userid = ?1 AND albumid = ?2 AND rating = ?3)
        """ # Adds an entry to the Ratings database if the user hasn't already rated it

        self.cur.execute(command, (userid, albumid, rating))
        self.conn.commit()

    def update_average(self, albumid):
        command = """
        UPDATE Albums
        SET average_rating = (SELECT AVG(rating) FROM Ratings WHERE albumid = ?1)
        WHERE albumid = ?1
        """ # Finds the average of every rating with the matching album id, takes the mean, and updates the column for the album

        self.cur.execute(command, (albumid))
        self.conn.commit()
    
    def update_chart(self):
        self.cur.execute("SELECT albumid FROM Albums")

        for record in self.cur.fetchall():
            self.update_average(record) # Runs update_average() on every entry in the Albums table
