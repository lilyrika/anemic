import sqlite3 as sql

class Database:
    def __init__(self):
        self.conn = sql.connect("database.db")
        self.cur = self.conn.cursor()

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
    
    def add_album(self, name, artist, year):
        command = """
        INSERT INTO Albums (albumid, name, artist, year)
        SELECT MAX(albumid)+1, ?1, ?2, ?3 FROM Albums
        WHERE NOT EXISTS (SELECT * FROM Albums WHERE name = ?1 AND artist = ?2 AND year = ?3)
        """

        self.cur.execute(command, (name, artist, year)) # Adds album with parameters if album doesn't already exist
        self.conn.commit()
    

    def album_profile(self, name):
        command = """
        SELECT albumid, name, artist, year FROM Albums
        WHERE ? = LOWER(name)
        """

        self.cur.execute(command, (name,))
        album_data = self.cur.fetchone() # Fetches album data if name matches

        album_id = album_data[0]
        album_name = album_data[1]
        album_artist = album_data[2]
        year = album_data[3]
        # Creates variables for each data field to be displayed later

        command = "SELECT genre FROM Genres WHERE albumid = ?"
        self.cur.execute(command, (album_id,))
        
        album_genres = []
        for genre_tuple in self.cur.fetchall():
            album_genres.append(genre_tuple[0]) # Appends each genre with matching album ID to a list
        
        print(album_id)
        print(f"{album_artist} - {album_name} ({year})")
        print(*album_genres, sep=', ')

    def artist_profile(self, name):
        command = """
        SELECT name, year 
        FROM Albums 
        WHERE LOWER(artist) = ?1 ORDER BY year
        """

        self.cur.execute(command, (name,))
        albums = self.cur.fetchall() # Fetches all albums under the artist's name and their release year

        command = """
        SELECT artist 
        FROM Albums 
        WHERE LOWER(artist) = ?1
        """

        self.cur.execute(command, (name,))
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

        self.cur.execute(command, (genre,))
        genre_name = self.cur.fetchone()[0]

        command = """
        SELECT DISTINCT name, artist, year FROM Albums
        JOIN Genres
        WHERE Genres.albumid = Albums.albumid AND LOWER(Genres.genre) = ?1
        ORDER BY year, name
        """

        print(genre_name)
        albums = self.cur.execute(command, (genre,))
        for album in albums:
            print(*album, sep=' | ')

database = Database()
database.add_album("You Won't Get What You Want", "Daughters", 2018)
database.album_profile("you won't get what you want")