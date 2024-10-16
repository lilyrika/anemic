import mysql.connector
import hashlib

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

            cmd = """
            SELECT genre 
            FROM Genre_Vote_Results
            WHERE albumid = %s AND agreed = 1"""
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

    def update_genre_result(self, albumid, genre):
        cmd = """
        SELECT COUNT(agreed)
        FROM Genre_Votes
        WHERE albumid = %s AND genre = %s AND agreed = 1
        """

        self.cur.execute(cmd, (albumid, genre))
        agrees = self.cur.fetchone()[0] # Gets amount of people that agree on an album being a certain genre

        cmd = """
        SELECT COUNT(agreed)
        FROM Genre_Votes
        WHERE albumid = %s AND genre = %s AND agreed = 0
        """

        self.cur.execute(cmd, (albumid, genre))
        disagrees = self.cur.fetchone()[0] # Gets amount of people that disagree on an album being a certain genre

        if agrees > disagrees:
            result = 1
        else:
            result = 0 # Sets agreed to True if there are more agree votes than disagree votes
        
        cmd = """
        SELECT genre
        FROM Genre_Vote_Results
        WHERE albumid = %s AND genre = %s
        """
        
        self.cur.execute(cmd, (albumid, genre))

        if self.cur.fetchone() == None: # Checks if the genre already has already been proposed
            cmd = """
            INSERT INTO Genre_Vote_Results
            VALUES (%s, %s, %s)
            """
            self.cur.execute(cmd, (albumid, genre, result)) # Adds the genre proposal if it doesn't exist
        else:
            cmd = """
            UPDATE Genre_Vote_Results
            SET agreed = %s
            WHERE albumid = %s AND genre = %s
            """
            self.cur.execute(cmd, (result, albumid, genre)) # Updates the genre proposal to the result with the newly added vote

        self.cnx.commit()

    def add_genre_vote(self, albumid, userid, genre, agreed):
        if agreed == True:
            agreed = 1
        else:
            agreed = 0 # Changes True or False to 1 or 0 respectively

        cmd = """
        SELECT albumid, userid, genre, agreed
        FROM Genre_Votes
        WHERE albumid = %s AND userid = %s AND genre = %s AND agreed = %s
        """
        self.cur.execute(cmd, (albumid, userid, genre, agreed))

        if self.cur.fetchone() == None: # Checks if the user's genre vote already exists
            cmd = """
            INSERT INTO Genre_Votes
            VALUES (%s, %s, %s, %s)
            """

            self.cur.execute(cmd, (albumid, userid, genre, agreed)) 
        else:
            cmd = """
            UPDATE Genre_Votes
            SET agreed = %s
            WHERE albumid = %s AND userid = %s AND genre = %s
            """
            self.cur.execute(cmd, (agreed, albumid, userid, genre)) # Updates the user's vote if it already exists

        self.update_genre_result(albumid, genre)

    def update_descriptor_result(self, albumid, descriptor):
        cmd = """
        SELECT COUNT(agreed)
        FROM Descriptor_Votes
        WHERE albumid = %s AND descriptor = %s AND agreed = 1
        """

        self.cur.execute(cmd, (albumid, descriptor))
        agrees = self.cur.fetchone()[0] # Takes the amount of people who agree with the descriptor

        cmd = """
        SELECT COUNT(agreed)
        FROM Descriptor_Votes
        WHERE albumid = %s AND descriptor = %s AND agreed = 0
        """

        self.cur.execute(cmd, (albumid, descriptor))
        disagrees = self.cur.fetchone()[0] # Takes the amonut of people who disagree with the descriptor

        if agrees > disagrees:
            result = 1
        else:
            result = 0 # Sets agreed to True if it has more agree votes than disagree votes
        
        cmd = """
        SELECT descriptor
        FROM Descriptor_Vote_Results
        WHERE albumid = %s AND descriptor = %s
        """
        
        self.cur.execute(cmd, (albumid, descriptor))
        if self.cur.fetchone() == None: # Checks if the descriptor already exists
            cmd = """
            INSERT INTO Descriptor_Vote_Results
            VALUES (%s, %s, %s)
            """
            self.cur.execute(cmd, (albumid, descriptor, result)) # Adds the descriptor if it doesn't already exist
        else:
            cmd = """
            UPDATE Descriptor_Vote_Results
            SET agreed = %s
            WHERE albumid = %s AND descriptor = %s
            """
            self.cur.execute(cmd, (result, albumid, descriptor)) # Updates the descriptor if it does exist

        self.cnx.commit()

    def add_descriptor_vote(self, albumid, userid, descriptor, agreed):
        if agreed == True:
            agreed = 1
        else:
            agreed = 0 # Sets True or False to 1 or 0 respectively

        cmd = """
        SELECT albumid, userid, descriptor, agreed
        FROM Descriptor_Votes
        WHERE albumid = %s AND userid = %s AND descriptor = %s AND agreed = %s
        """
        self.cur.execute(cmd, (albumid, userid, descriptor, agreed)) 

        if self.cur.fetchone() == None: # Checks if the genre already exists
            cmd = """
            INSERT INTO Descriptor_Votes
            VALUES (%s, %s, %s, %s)
            """

            self.cur.execute(cmd, (albumid, userid, descriptor, agreed)) 
        else:
            cmd = """
            UPDATE Descriptor_Votes
            SET agreed = %s
            WHERE albumid = %s AND userid = %s AND descriptor = %s
            """
            self.cur.execute(cmd, (agreed, albumid, userid, descriptor))

        self.update_genre_result(albumid, descriptor)
    
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
        self.cur.execute(cmd, (userid, albumid, rating)) # Checks if the user has already rated the album

        if self.cur.fetchone() == None:
            cmd = """
            INSERT INTO Ratings (userid, albumid, rating)
            SELECT %s, %s, %s
            """
            self.cur.execute(cmd, (userid, albumid, rating)) # Adds the rating if it doesn't already exist
        else:
            cmd = """
            UPDATE Ratings
            SET rating = %s
            WHERE userid = %s AND albumid = %s
            """
            self.cur.execute(cmd, (rating, userid, albumid)) # Updates the rating if it does exist
        
        self.cnx.commit()

    def update_average(self, albumid):
        cmd = """
        SELECT AVG(rating) 
        FROM Ratings 
        WHERE albumid = %s
        """

        self.cur.execute(cmd, (albumid,))
        average_rating = self.cur.fetchone()[0] # Takes the average of every rating for an album

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