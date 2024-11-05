from backend import Database

import tkinter as tk
from tkinter import ttk
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

database.add_rating(1, 1, 9)
database.add_rating(1, 2, 10)
database.add_rating(1, 3, 10)
database.add_rating(1, 4, 10)
database.add_rating(1, 5, 10)
database.add_rating(1, 6, 9)
database.add_rating(1, 7, 10)
database.add_rating(1, 8, 9)

database.update_chart()

###############

root = tk.Tk()
root.geometry("1280x720")
root.configure(background="#0b0f14")
root.title("Anemic") # Initialises the window and changes the background colour

title = tk.Label(root, text="Welcome to Anemic!", font="Bahnschrift", anchor="w")
title.place(x=10, y=10) # Places the title for the app onto the window

search_elements = []

def search(arg="None"):
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

    elif table == "Artist":
        data = database.get_artist_data(query)
        # Returns artist, albums

        if data != None:
            pass

    elif table == "Genre":
        data = database.get_genre_data(query)
        # Returns genre_name, albums

        if data != None:
            pass

    # Retrieves the query from the searchbar, checks choice for the table, then calls the appropriate function, displaying the data in the terminal

def destroy_search():
    global search_elements

    for element in search_elements:
        element.destroy() # Removes all elements created by the search

def place_image(image_blob):
    file_object = BytesIO(image_blob) # Converts blob to file object
    image = Image.open(file_object) # Loads the image

    resized_image = image.resize((200, 200)) # Resizes the image to 200x200
    rendered_image = ImageTk.PhotoImage(resized_image) # Converts the opened resized image for display

    img = tk.Label(image=rendered_image)
    img.image = rendered_image # Sets the label's image to the rendered image
    img.place(x=10, y=178) # Places image
    search_elements.append(img) # Adds to the search_elements list

searchbar = tk.Entry(root, width=60)
searchbar.place(x=165, y=13) # Places the searchbar next to the title
searchbar.bind('<Return>', search) # Makes it so if you press 

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

