import sqlite3 as sql

class Database:
    def __init__(self):
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()
    
    def add_album(self, name, artist, year):
        command = """
        INSERT INTO Albums (albumid, name, artist, year)
        SELECT MAX(albumid)+1, ?, ?, ? FROM Albums
        """

        self.cursor.execute(command, (name, artist, year))
        database.conn.commit()
    
    def add_genre(self, albumid, genre):
        command = f"""
        INSERT INTO Genres (albumid, genre)
        SELECT '{albumid}', '{genre}'
        WHERE NOT EXISTS (SELECT * FROM Genres WHERE albumid = '{albumid}' AND genre = '{genre}')
        """

        self.cursor.execute(command)
        database.conn.commit()
    
    def album_profile(self, name):
        name = name.lower()
        command = """
        SELECT albumid, name, artist, year FROM Albums
        WHERE ? = LOWER(name)
        """
        self.cursor.execute(command, (name,))
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
        name = name.lower()
        command = """
        SELECT name, year FROM Albums
        WHERE LOWER(artist) = ?
        """

        print(name)
        self.cursor.execute(command, (name,))
        print(self.cursor.fetchall())

database = Database()
database.artist_profile('weatherday')
