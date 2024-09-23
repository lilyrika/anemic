from backend import Database

import tkinter as tk
from tkinter import ttk 

database = Database()

def wipe():
    database.cur.execute("DELETE FROM Albums")
    database.cur.execute("DELETE FROM Ratings")
    database.cur.execute("DELETE FROM Genres") # Wipes all the tables for debugging

wipe()

database.add_album("Carrie & Lowell", "Sufjan Stevens", "2015", True)
database.add_album("In The Aeroplane Over The Sea", "Neutral Milk Hotel", "1998")
database.add_album("PetroDragonic Apocalypse", "King Gizzard & The Lizard Wizard", "2023")
database.add_album("Diamond Jubilee", "Cindy Lee", "2024")

database.add_genre(1, "Indie Folk")
database.add_genre(2, "Indie Folk")
database.add_genre(3, "Thrash Metal")
database.add_genre(3, "Progressive Metal")
database.add_genre(4, "Hypnagogic Pop")

database.add_rating(1, 1, 9)
database.add_rating(1, 2, 10)
database.add_rating(1, 3, 10)
database.add_rating(1, 4, 10)

database.update_chart()

###############

root = tk.Tk()
root.geometry("1280x720")
root.configure(background="#0b0f14")
root.title("Anemic") # Initialises the window and changes the background colour

title = tk.Label(root, text="Welcome to Anemic!", font="Bahnschrift", anchor="w")
title.place(x=10, y=10) # Places the title for the app onto the window

searchbar = tk.Entry(root, width=60)
searchbar.place(x=165, y=13) # Places the searchbar next to the title

def search():
    query = searchbar.get()
    database.album_profile(query)
    # Retrieves the query from the searchbar and checks the database for the album, displaying the data in the terminal

searchbutton = ttk.Button(root, text="Search", command=search)
searchbutton.place(x=530, y=10) # Places the search button, which gets inputs from the searchbar

root.mainloop()
