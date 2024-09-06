import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("1280x720")
root.configure(background="#0b0f14")
root.title("Anemic")

title = tk.Label(root, text = "Welcome to Anemic!", font = "Bahnschrift", anchor = "w")
title.grid(row = 1, column = 1)

searchbar_var = tk.StringVar()
searchbar = tk.Entry(root, width=90)
searchbar.grid(row = 2, column = 1, padx=10, pady=10)

root.mainloop()