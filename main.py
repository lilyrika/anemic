import sqlite3 as sql

    # def create_artists_table(self):
    #     self.command("DROP TABLE IF EXISTS Artists")
    #     self.command(
    #         """
    #         CREATE TABLE Artists(
    #         artistid INT PRIMARY KEY,
    #         name VARCHAR(64)
    #         )
    #         """
    #     )

    # def create_albums_table(self):
    #     self.command("DROP TABLE IF EXISTS Albums")
    #     self.command(
    #         """
    #         CREATE TABLE Albums(
    #         albumid INT PRIMARY KEY NOT NULL,
    #         name VARCHAR(64) NOT NULL,
    #         artist VARCHAR(64) NOT NULL,
    #         genre1 VARCHAR(64),
    #         genre2 VARCHAR(64),
    #         genre3 VARCHAR(64)
    #         )
    #         """
    #     )

class Database:
    def __init__(self):
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()
    
    def command(self, text):
        self.cursor.execute(text)
    
    def add_album(self):
        self.command(
        """
        INSERT INTO Albums (albumid, name, artist, genre1, genre2) 
        SELECT MAX(albumid)+1, 'SCARING THE HOES', 'JPEGMAFIA', 'Experimental Hip Hop', 'Hardcore Hip Hop' FROM Albums
        """
        )

        database.conn.commit()




database = Database()
database.command("DELETE FROM Albums where albumid=9")