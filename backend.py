import sqlite3 as sql
from random import randint

class Database:
    def __init__(self):
        self.conn = sql.connect("database.db")
        self.cur = self.conn.cursor()
        self.chartcur = self.conn.cursor()

        command = """
        CREATE TABLE IF NOT EXISTS Albums(
        albumid INT,
        name VARCHAR(255),
        artist VARCHAR(255),
        year VARCHAR(255)
        )
        """
        self.cur.execute(command)

        command = """
        CREATE TABLE IF NOT EXISTS Genres(
        albumid INT,
        genre VARCHAR(255)
        )
        """
        self.cur.execute(command)

        self.conn.commit()
    
    def add_album(self, name, artist, year, one=False):
        if one == False:
            command = """
            SELECT name, artist, year FROM Albums
            WHERE name = ?1 AND artist = ?2 AND year = ?3
            """
            self.cur.execute(command, (name, artist, year))

            if self.cur.fetchone() == None:
                command = """
                INSERT INTO Albums (albumid, name, artist, year)
                SELECT MAX(albumid)+1, ?1, ?2, ?3 FROM Albums
                """

                self.cur.execute(command, (name, artist, year)) # Adds album with parameters if album doesn't already exist
                self.conn.commit()

        else:
            command = """
            INSERT INTO Albums (albumid, name, artist, year)
            VALUES(1, ?1, ?2, ?3)
            """

            self.cur.execute(command, (name, artist, year)) # Does the same thing but the albumid is 1
            self.conn.commit()

    def album_profile(self, name):
        command = """
        SELECT albumid, name, artist, year FROM Albums
        WHERE ? = LOWER(name)
        """

        self.cur.execute(command, (name.lower(),))
        album_data = self.cur.fetchone() # Fetches album data if name matches

        album_id = album_data[0]
        album_name = album_data[1]
        album_artist = album_data[2]
        album_year = album_data[3]
        # Creates variables for each data field to be displayed later

        command = "SELECT genre FROM Genres WHERE albumid = ?"
        self.cur.execute(command, (album_id,))
        
        album_genres = []
        for genre_tuple in self.cur.fetchall():
            album_genres.append(genre_tuple[0]) # Appends each genre with matching album ID to a list
        
        print(album_id)
        print(album_name)
        print(album_artist)
        print(album_year)
        print(*album_genres, sep=', ')

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
            print(*album, sep = " | ")

    def add_genre(self, albumid, genre):
        command = """
        INSERT INTO Genres (albumid, genre) 
        SELECT ?1, ?2
        WHERE NOT EXISTS (SELECT * FROM Genres WHERE albumid = ?1 AND genre = ?2)
        """

        self.cur.execute(command, (albumid, genre))
        self.conn.commit()
    
    def genre_profile(self, genre):
        command = """
        SELECT genre 
        FROM Genres 
        WHERE LOWER(genre) = ?1
        """

        self.cur.execute(command, (genre.lower(),))
        genre_name = self.cur.fetchone()[0]

        command = """
        SELECT DISTINCT name, artist, year, average_rating FROM Albums
        JOIN Genres
        WHERE Genres.albumid = Albums.albumid AND Genres.genre = ?1
        ORDER BY year, name
        """

        print(f"==== {genre_name} ====")
        self.cur.execute(command, (genre_name,))
        albums = self.cur.fetchall()
        for album in albums:
            print(*album, sep=' | ')
    
    def add_rating(self, userid, albumid, rating):
        command = """
        INSERT INTO Ratings (userid, albumid, rating)
        SELECT ?1, ?2, ?3
        WHERE NOT EXISTS (SELECT * FROM Ratings WHERE userid = ?1 AND albumid = ?2 AND rating = ?3)
        """

        self.cur.execute(command, (userid, albumid, rating))
        self.conn.commit()

    def update_average(self, albumid):
        command = """
        UPDATE Albums
        SET average_rating = (SELECT AVG(rating) FROM Ratings WHERE albumid = ?1)
        WHERE albumid = ?1
        """

        self.cur.execute(command, (albumid))
        self.conn.commit()
    
    def update_chart(self):
        self.cur.execute("SELECT albumid FROM Albums")

        for record in self.cur.fetchall():
            self.update_average(record)
