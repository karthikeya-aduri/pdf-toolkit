import tkinter as tk
from constants import hoverColor, backgroundColor

def onEnter(element):
    element.widget['background'] = hoverColor

def onLeave(element):
    element.widget['background'] = backgroundColor

def handleHover(button):
    button.bind("<Enter>", onEnter)
    button.bind("<Leave>", onLeave)

def placeButtons(button, index):
    if index % 2:
        button.pack(fill = tk.X, pady = 5)
    else:
        button.pack(fill = tk.X, pady = 20)
