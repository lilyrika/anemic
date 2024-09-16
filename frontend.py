from backend import Database

import tkinter as tk
from tkinter import ttk 

database = Database()

def cur(cmd): # Shortcut for the execute
    database.cur.execute(cmd)

def wipe():
    cur("DELETE FROM Albums")
    cur("DELETE FROM Ratings")
    cur("DELETE FROM Genres") # Wipes all the tables for debugging

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

searchbutton = ttk.Button(root, text="Search", command=search)
searchbutton.place(x=530, y=10) # Places the search button, which gets inputs from the searchbar

root.mainloop()
