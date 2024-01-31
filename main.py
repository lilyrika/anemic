import sqlite3 as sql

class Database:
    def __init__(self):
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()

    def add_album(self, name, artist, year):
        command = """
        INSERT INTO Albums (albumid, name, artist, year)
        SELECT MAX(albumid)+1, ?1, ?2, ?3 FROM Albums
        WHERE NOT EXISTS (SELECT * FROM Genres WHERE name = ?1 AND artist = ?2 AND year = ?3)
        """

        self.cursor.execute(command, (name, artist, year))
        database.conn.commit()
    
    def add_genre(self, albumid, genre):
        command = """
        INSERT INTO Genres (albumid, genre)
        SELECT ?1, ?2
        WHERE NOT EXISTS (SELECT * FROM Genres WHERE albumid = ?1 AND genre = ?2)
        """

        self.cursor.execute(command, (albumid, genre))
        database.conn.commit()
    
    def album_profile(self, name):
        command = """
        SELECT albumid, name, artist, year FROM Albums
        WHERE ? = LOWER(name)
        """
        self.cursor.execute(command, (name.lower(),))
        album_data = self.cursor.fetchone()

        album_id = album_data[0]
        album_name = album_data[1]
        album_artist = album_data[2]
        year = album_data[3]

        command = "SELECT genre FROM Genres WHERE albumid = ?"
        self.cursor.execute(command, (album_id,))
        
        genre_list = []
        for genre_tuple in self.cursor.fetchall():
            genre_list.append(genre_tuple[0])
        
        print(f"[{album_id}]\n{album_artist} - {album_name} ({year})")
        print(*genre_list, sep=', ')
    
    def artist_profile(self, name):
        command = "SELECT name, year FROM Albums WHERE LOWER(artist) = ?1 ORDER BY year"
        self.cursor.execute(command, (name.lower(),))
        albums = self.cursor.fetchall()

        command = "SELECT artist FROM Albums WHERE LOWER(artist) = ?1"
        self.cursor.execute(command, (name.lower(),))
        artist = self.cursor.fetchone()[0]

        print(artist)
        for album in albums:
            print(*album, sep = " | ")
        

database = Database()
database.album_profile("for the first time")