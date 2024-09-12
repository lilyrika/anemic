from backend import Database

import tkinter as tk
from tkinter import ttk 

database = Database()

def cur(cmd): 
    database.cur.execute(cmd)

def wipe():
    cur("DELETE FROM Albums")
    cur("DELETE FROM Ratings")
    cur("DELETE FROM Genres")

###############

root = tk.Tk()
root.geometry("1280x720")
root.configure(background="#0b0f14")
root.title("Anemic")

#implement tabs

title = tk.Label(root, text="Welcome to Anemic!", font="Bahnschrift", anchor="w")
title.place(x=10, y=10)

searchbar = tk.Entry(root, width=60)
searchbar.place(x=165, y=13)

def search():
    query = searchbar.get()

searchbutton = ttk.Button(root, text="Search", command=search)
searchbutton.place(x=530, y=10)

root.mainloop()