from backend import Database

import tkinter as tk
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk















database = Database()
database.update_average(8)
test = database.get_album_data("3d country")
print(test)