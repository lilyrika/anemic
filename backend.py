import mysql.connector
import hashlib
from random import randint  

class Database:
    def __init__(self):
        self.cnx = mysql.connector.connect(user="root", password="PowerApproaches", host="127.0.0.1")
        self.cur = self.cnx.cursor()
        # Initialise connection to MySQL and creates cursor

        cmd = "USE music;"
        self.cur.execute(cmd)
    
    def register(self):
        username = str(input("Enter username: "))

        cmd = """
        SELECT username
        FROM users
        WHERE username = %s
        """

        self.cur.execute(cmd, (username,))
        
        if self.cur.fetchone() == None:
            password = ""
            while len(password) <= 8:
                password = str(input("Enter password: "))
                if len(password) <= 8:
                    print("Password must be longer than 8 characters.") # Prompts the user for username and password
            
            bytes = password.encode('utf-8')
            hash_object = hashlib.sha256(bytes)
            hashed_password = hash_object.hexdigest() # Hashes the password

            cmd = """
            INSERT INTO Users (userid, username, password)
            SELECT MAX(userid)+1, %s, %s FROM Users
            """ # Adds the password to the database
            
            self.cur.execute(cmd, (username, hashed_password))
            self.cnx.commit()

            print("Account registered successfully")
        else:
            print("Username already exists")
    
    def login(self):
        client_username = str(input("Enter username: "))
        client_password = str(input("Enter password: "))

        bytes = client_password.encode('utf-8')
        hash_object = hashlib.sha256(bytes)
        client_hash = hash_object.hexdigest() # Hashes the password

        cmd = """
        SELECT userid, username, password FROM Users
        WHERE username = %s
        """

        self.cur.execute(cmd, (client_username,))
        data = self.cur.fetchone()
        
        if data != None:
            user_id = data[0]
            username = data[1]
            server_hash = data[2]

            if client_hash == server_hash:
                self.user_id = user_id 
                self.username = username
            else:
                print("Incorrect username/password")
        else:
            print("Incorrect username/password")

    def add_album(self, name, artist, year, one=False):
        if one == False:
            cmd = """
            SELECT name, artist, year FROM Albums
            WHERE name = %s AND artist = %s AND year = %s
            """
            self.cur.execute(cmd, (name, artist, year))
            # Checks if the album doesn't already exist, if it fetches None, it doesn't exist
            
            if self.cur.fetchone() == None: # If the album doesn't already exist
                cmd = """
                INSERT INTO Albums (albumid, name, artist, year)
                SELECT MAX(albumid)+1, %s, %s, %s FROM Albums
                """ # Adds a record with the parameters given in the add_album() function

                self.cur.execute(cmd, (name, artist, year)) # Adds album with parameters if album doesn't already exist
                self.cnx.commit()

        else:
            cmd = """
            INSERT INTO Albums (albumid, name, artist, year)
            VALUES(1, %s, %s, %s)
            """

            self.cur.execute(cmd, (name, artist, year)) # Adds album with parameters if album doesn't already exist, but the albumid is 1
            self.cnx.commit()

    def album_profile(self, name):
        cmd = """
        SELECT albumid, name, artist, year, average_rating FROM Albums
        WHERE %s = LOWER(name)
        """

        self.cur.execute(cmd, (name.lower(),))
        album_data = self.cur.fetchone() # Fetches selected columns from the record if the name exists in the database

        if album_data != None:
            album_id = album_data[0]
            album_name = album_data[1]
            album_artist = album_data[2]
            album_year = album_data[3]
            album_rating = album_data[4]
            # Creates variables for each data field to be displayed later

            cmd = "SELECT genre FROM Genres WHERE albumid = %s"
            self.cur.execute(cmd, (album_id,))
            
            album_genres = []
            for genre_tuple in self.cur.fetchall():
                album_genres.append(genre_tuple[0]) # Appends each genre with matching album ID to a list
            
            print(f"{album_name} - {album_artist}")
            print(album_rating)
            print(*album_genres, sep=', ')
            print(album_year) # Displays the data

    def artist_profile(self, name):
        cmd = """
        SELECT name, year 
        FROM Albums 
        WHERE LOWER(artist) = %s ORDER BY year
        """

        self.cur.execute(cmd, (name.lower(),))
        albums = self.cur.fetchall() # Fetches all albums under the artist's name and their release year

        cmd = """
        SELECT artist 
        FROM Albums 
        WHERE LOWER(artist) = %s
        """

        self.cur.execute(cmd, (name.lower(),))
        artist = self.cur.fetchone()[0] # Fetches the artist's name with correct capitalisation

        print(artist)
        for album in albums:
            print(*album, sep = " | ") # Displays the data

    def add_genre(self, albumid, genre):
        cmd = """
        SELECT albumid, genre
        FROM Genres
        WHERE albumid = %s AND genre = %s
        """
        self.cur.execute(cmd, (albumid, genre))

        if self.cur.fetchone() == None:
            cmd = """
            INSERT INTO Genres 
            VALUES (%s, %s) 
            """ 

            self.cur.execute(cmd, (albumid, genre)) 
            # Adds the new genre to the Genres table if it doesn't already exist
        self.cnx.commit()
    
    def genre_profile(self, genre):
        cmd = """
        SELECT genre 
        FROM Genres 
        WHERE LOWER(genre) = %s
        """

        self.cur.execute(cmd, (genre.lower(),)) 
        genre_name = self.cur.fetchone()[0] # Retrieves genre from Genres table if it exists

        cmd = """
        SELECT DISTINCT name, artist, year, average_rating FROM Albums
        JOIN Genres
        WHERE Genres.albumid = Albums.albumid AND Genres.genre = %s
        ORDER BY year, name
        """

        self.cur.execute(cmd, (genre_name,))
        albums = self.cur.fetchall() # Selects every album that has a genre specified in the parameters

        print(f"==== {genre_name} ====")
        for album in albums:
            print(*album, sep=' | ') # Displays the data
    
    def add_rating(self, userid, albumid, rating):
        cmd = """
        SELECT *
        FROM Ratings
        WHERE userid = %s AND albumid = %s AND rating = %s
        """
        self.cur.execute(cmd, (userid, albumid, rating))

        if self.cur.fetchone() == None:
            cmd = """
            INSERT INTO Ratings (userid, albumid, rating)
            SELECT %s, %s, %s
            """ 
            # Adds an entry to the Ratings database if the user hasn't already rated it

        self.cur.execute(cmd, (userid, albumid, rating))
        self.cnx.commit()

    def update_average(self, albumid):
        cmd = """
        SELECT AVG(rating) 
        FROM Ratings 
        WHERE albumid = %s
        """

        self.cur.execute(cmd, (albumid,))
        average_rating = self.cur.fetchone()[0]

        cmd = """
        UPDATE Albums
        SET average_rating = %s
        WHERE albumid = %s
        """ # Finds the average of every rating with the matching album id, takes the mean, and updates the column for the album

        self.cur.execute(cmd, (average_rating, albumid))
        self.cnx.commit()
    
    def update_chart(self):
        self.cur.execute("SELECT albumid FROM Albums")

        for record_id in self.cur.fetchall():
            self.update_average(record_id[0]) # Runs update_average() on every entry in the Albums table