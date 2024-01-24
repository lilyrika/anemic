import sqlite3 as sql

#region Create Tables
# database.command("DROP TABLE IF EXISTS Artists")
# database.command(
#     """
#     CREATE TABLE Artists(
#     artistid INT PRIMARY KEY,
#     name VARCHAR(64)
#     )
#     """
# )

# database.command("DROP TABLE IF EXISTS Albums")
# database.command(
#     """
#     CREATE TABLE Albums(
#     albumid INT PRIMARY KEY NOT NULL,
#     name VARCHAR(64) NOT NULL,
#     artist VARCHAR(64) NOT NULL
#     )
#     """
# )

# database.command("DROP TABLE IF EXISTS Genres")
# database.command(
#     """
#     CREATE Table Genres(
#     genreid INT PRIMARY KEY NOT NULL, 
#     albumid INT NOT NULL, 
#     genre VARCHAR(64) NOT NULL
#     )
#     """
# )
#endregion

class Database:
    def __init__(self):
        self.conn = sql.connect("database.db")
        self.cursor = self.conn.cursor()
    
    def add_album(self, name, artist):
        command = """
        INSERT INTO Albums (albumid, name, artist)
        SELECT MAX(albumid)+1, ?, ? FROM Genres
        """

        self.cursor.execute(command, (name, artist))
        database.conn.commit()
    
    def add_genre(self, albumid, genre):
        command = """
        INSERT INTO Genres (genreid, albumid, genre)
        SELECT MAX(genreid)+1, ?, ? FROM Genres
        """

        self.cursor.execute(command, (albumid, genre))
        database.conn.commit()

database = Database()
database.add_album("To Be Kind", "Swans")
database.add_genre(2, "Post-Rock")

#