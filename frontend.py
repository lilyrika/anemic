import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("1280x720")
root.configure(background="#0b0f14")
root.title("Anemic")

title = tk.Label(root, text = "Welcome to Anemic!", font = "Bahnschrift", anchor = "w")
title.place(x=10, y=10)

searchbar_var = tk.StringVar()
searchbar = tk.Entry(root, width=60)
searchbar.place(x=165, y=13)

searchbutton = tk.Button(root, text = "Search")
searchbutton.place(x=530, y=10)

root.mainloop()