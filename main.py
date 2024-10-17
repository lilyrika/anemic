from backend import Database

import tkinter as tk
from tkinter import ttk 

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

database.add_genre_vote(1, 1, "Indie Folk", True)
database.add_genre_vote(2, 1, "Indie Folk", True)
database.add_genre_vote(3, 1, "Thrash Metal", True)
database.add_genre_vote(3, 1, "Progressive Metal", True)
database.add_genre_vote(4, 1, "Hypnagogic Pop", True)

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