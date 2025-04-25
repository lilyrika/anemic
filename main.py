from backend import Database

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
from io import BytesIO
from PIL import Image, ImageTk

database = Database()

database.cur.execute("DELETE FROM Albums")
database.cur.execute("DELETE FROM Ratings")
database.cur.execute("DELETE FROM Genre_Votes")
database.cur.execute("DELETE FROM Genre_Vote_Results")
# Wipes all the tables for debugging

database.add_album("Carrie & Lowell", "Sufjan Stevens", 2015, True)
database.add_album("In The Aeroplane Over The Sea", "Neutral Milk Hotel", 1998)
database.add_album("PetroDragonic Apocalypse", "King Gizzard & The Lizard Wizard", 2023)
database.add_album("Diamond Jubilee", "Cindy Lee", 2024)
database.add_album("Crumbling", "Mid-air Thief", 2018)
database.add_album("IGOR", "Tyler, The Creator", 2019)
database.add_album("The Ooz", "King Krule", 2017)
database.add_album("3D Country", "Geese", 2023)

database.add_genre_vote(1, 1, "Indie Folk", True)

database.add_genre_vote(2, 1, "Indie Folk", True)
database.add_genre_vote(2, 1, "Indie Rock", True)

database.add_genre_vote(3, 1, "Thrash Metal", True)
database.add_genre_vote(3, 1, "Progressive Metal", True)

database.add_genre_vote(4, 1, "Hypnagogic Pop", True)
database.add_genre_vote(4, 1, "Psychedelic Pop", True)

database.add_genre_vote(5, 1, "Folktronica", True)
database.add_genre_vote(5, 1, "Neo-Psychedelia", True)

database.add_genre_vote(6, 1, "Neo-Soul", True)

database.add_genre_vote(7, 1, "Art Rock", True)

database.add_genre_vote(8, 1, "Indie Rock", True)
database.add_genre_vote(8, 1, "Art Punk", True)
database.add_genre_vote(8, 1, "Alt-Country", True)

database.add_descriptor_vote(2, 1, 'sad', True)
database.add_descriptor_vote(5, 1, "ethereal", True)
database.add_descriptor_vote(8, 1, "quirky", True)

database.add_rating(1, 1, 9)
database.add_rating(1, 2, 10)
database.add_rating(1, 3, 10)
database.add_rating(1, 4, 10)
database.add_rating(1, 5, 10)
database.add_rating(1, 6, 9)
database.add_rating(1, 7, 10)
database.add_rating(1, 8, 10)

database.update_chart()

###############

def open_main_window():
    search_elements = []
    def search(none=None, search_elements=search_elements):
        destroy_search()
        table = choice.get()
        query = searchbar.get()

        if table == "Album":
            data = database.get_album_data(query)
            # Returns albumid, album_name, album_artist, album_rating, album_genres, album_descriptors, album_year, album_rating_count

            if data != None:
                title = tk.Label(text=f"{data[2]} - {data[1]} [{data[6]}]", font=("Bahnschrift", 16))
                title.place(x=10, y=50) # Places artist, title and year
                search_elements.append(title)

                rating = tk.Label(text=f"Rating: {data[3]} from {data[7]} ratings", font=("Bahnschrift", 12))
                rating.place(x=10, y=90) # Places rating
                search_elements.append(rating)

                genres = tk.Label(text=f"Genres: {', '.join(data[4])}", font=("Bahnschrift", 12))
                genres.place(x=10, y=119) # Places genres
                search_elements.append(genres)

                descriptors = tk.Label(text=f"Descriptors: {', '.join(data[5])}", font=("Bahnschrift", 12))
                descriptors.place(x=10, y=148) # Places descriptors
                search_elements.append(descriptors)

                image_blob = database.get_image(data[0])
                place_image(image_blob)

                rating = get_album_rating(data[0])

                ratings = [
                    rating, # Default choice
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10
                ]

                rating_choice = tk.StringVar() # Creates a variable for the user's choice to be stored
                rating_box = ttk.OptionMenu(root, rating_choice, *ratings) 
                rating_box.place(x=10, y=389) # Places the dropdown menu for the user to select what rating they want to give to the album
                search_elements.append(rating_box)

                rate_button = ttk.Button(root, text="Rate", command=lambda:database.add_rating(database.userid, data[0], rating_choice))
                rate_button.place(x=32, y=388) # Places the rating button, which uses the dropdown as a parameter
                search_elements.append(rate_button)

                genre_bar = tk.Entry(root, width=30)
                genre_bar.place(x=200, y=13)

        elif table == "Artist":
            data = database.get_artist_data(query)
            # Returns artist, albums

            if data != None:
                artist = tk.Label(text=f"{data[0]}", font=("Bahnschrift", 16))
                artist.place(x=10, y=50) # Places artist, title and year
                search_elements.append(artist)

                y_value = 90
                for album in data[1]:
                    album_label = tk.Label(text=f"{album[0]} [{album[1]}] ({album[2]} from {album[3]} ratings)", font=("Bahnschrift", 12))
                    album_label.place(x=10, y=y_value) # Places rating
                    search_elements.append(album_label)
                    y_value += 30
                    

        elif table == "Genre":
            data = database.get_genre_data(query)
            # Returns genre_name, albums

            if data != None:
                genre = tk.Label(text=f"{data[0]}", font=("Bahnschrift", 16))
                genre.place(x=10, y=50)
                search_elements.append(genre)

                y_value = 90
                for album in data[1]:
                    album_label = tk.Label(text=f"{album[0]} - {album[1]} [{album[2]}] ({album[3]} from {album[4]} rating)", font=("Bahnschrift", 12))
                    album_label.place(x=10, y=y_value) # Places rating
                    search_elements.append(album_label)
                    y_value += 30

        # Retrieves the query from the searchbar, checks choice for the table, then calls the appropriate function, displaying the data in the terminal

    def destroy_search(search_elements=search_elements):
        for element in search_elements:
            element.destroy() # Removes all elements created by the search

    def place_image(image_blob):
        if image_blob != None:
            file_object = BytesIO(image_blob) # Converts blob to file object
            image = Image.open(file_object) # Loads the image

            resized_image = image.resize((200, 200)) # Resizes the image to 200x200
            rendered_image = ImageTk.PhotoImage(resized_image) # Converts the opened resized image for display

            img = tk.Label(image=rendered_image)
            img.image = rendered_image # Sets the label's image to the rendered image
            img.place(x=10, y=178) # Places image
            search_elements.append(img) # Adds to the search_elements list

    def get_album_rating(albumid):
            cmd = """
            SELECT rating FROM Ratings
            WHERE userid = %s AND albumid = %s
            """
            database.cur.execute(cmd, (database.userid, albumid))
            rating = database.cur.fetchone()[0]

            if rating != None:
                return rating
            else:
                return 0

    root = tk.Tk()
    root.geometry("1280x720")
    root.configure(background="#0b0f14")
    root.title("Anemic") # Initialises the window and changes the background colour

    title = tk.Label(root, text="Welcome to Anemic!", font="Bahnschrift", anchor="w")
    title.place(x=10, y=10) # Places the title for the app onto the window

    searchbar = tk.Entry(root, width=60)
    searchbar.place(x=165, y=13) # Places the searchbar next to the title
    searchbar.bind('<Return>', search) # Makes it so if you press Enter, it also calls the search function  

    searchbutton = ttk.Button(root, text="Search", command=search)
    searchbutton.place(x=530, y=10) # Places the search button, which gets inputs from the searchbar

    search_types = [
        "Album", # Default choice
        "Album",
        "Artist",
        "Genre"
    ]

    choice = tk.StringVar() # Creates a variable for the user's choice to be stored
    dropdown = ttk.OptionMenu(root, choice, *search_types) 
    dropdown.place(x=607, y=11) # Places the dropdown menu for the user to select what category they want to search

    root.mainloop()

def open_login_window():
    def register():
        username = username_box.get() 
        password = password_box.get() # Gets the user's entries from username and password boxes
        
        cmd = """
        SELECT username
        FROM users
        WHERE username = %s
        """

        database.cur.execute(cmd, (username,))
        
        if database.cur.fetchone() == None:
            if len(password) <= 8:
                messagebox.showerror("Error", "Password must be longer than 8 characters.") # Gives error if under 9 characters
            elif len(username) <= 3:
                messagebox.showerror("Error", "Username must be longer than 3 characters.") # Gives error if under 4 characters
            else:
                bytes = password.encode('utf-8')
                hash_object = hashlib.sha256(bytes)
                hashed_password = hash_object.hexdigest() # Hashes the password

                cmd = """
                INSERT INTO Users (userid, username, password)
                SELECT MAX(userid)+1, %s, %s FROM Users
                """ # Adds the password to the database
                
                database.cur.execute(cmd, (username, hashed_password))
                database.cnx.commit()

                messagebox.showerror("Anemic", "Account registered successfully")
        else:
            messagebox.showerror("Error", "Username already exists") # Displays errors

    def login():
        client_username = username_box.get()
        client_password = password_box.get()

        bytes = client_password.encode('utf-8')
        hash_object = hashlib.sha256(bytes)
        client_hash = hash_object.hexdigest() # Hashes the password

        cmd = """
        SELECT userid, username, password FROM Users
        WHERE username = %s
        """

        database.cur.execute(cmd, (client_username,))
        data = database.cur.fetchone()
        
        if data != None:
            userid = data[0]
            username = data[1]
            server_hash = data[2]

            if client_hash == server_hash:
                database.userid = userid 
                database.username = username
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Incorrect username/password")
        else:
            messagebox.showerror("Error", "Incorrect username/password")

    login_window = tk.Tk()
    login_window.title("Anemic Login")
    login_window.configure(background="#0b0f14")
    login_window.geometry("270x160")

    login_title = tk.Label(login_window, text="Anemic", font="Bahnschrift", anchor="w")
    login_title.place(x=91, y=10)

    username_label = tk.Label(login_window, text="Username")
    username_label.place(x=10, y=50)
    username_box = tk.Entry(login_window, width=30)
    username_box.place(x=70, y=51)

    password_label = tk.Label(login_window, text="Password")
    password_label.place(x=13, y=80)
    password_box = tk.Entry(login_window, width=30, show='*')
    password_box.place(x=70, y=81)

    register_button = ttk.Button(login_window, text="Register", command=register)
    register_button.place(x=47, y=111)

    login_button = ttk.Button(login_window, text="Login", command=login)
    login_button.place(x=127, y=111)

    login_window.mainloop()

logged_in = False

open_login_window()

if database.username != "":
    open_main_window()
