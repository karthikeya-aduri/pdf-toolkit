import tkinter as tk
from handler import callEventListener, handleHover
from render import renderButton
from constants import (
        backgroundColor,
        foregroundColor,
        borderColor,
        hoverColor,
        buttonColor,
        entryColor,
        fontFamily
)

def createWindow(title, geometry, resizableFlag):
    window = tk.Tk()

    window.title(title)
    window.geometry(geometry)
    window.resizable(resizableFlag, resizableFlag)
    icon = tk.PhotoImage(file = "icon.png")
    window.iconphoto(True, icon)

    return window

def createFrame(parent, width, height, highlightthickness = 0.0):
    frame = tk.Frame(parent,
                     width = width,
                     height = height,
                     background = backgroundColor,
                     highlightthickness = highlightthickness,
                     highlightbackground = borderColor
                     )
    frame.pack_propagate(False)
    return frame

def createLabel(parent, fontSize, text, wraplength = 0, type = ""):
    label = tk.Label(parent,
                     text = text,
                     font = (fontFamily, fontSize, type),
                     background = backgroundColor,
                     foreground = foregroundColor,
                     wraplength = wraplength
                    )
    return label

def createButton(parent, text, fontSize):
    button = tk.Button(parent,
                       text = text,
                       font = (fontFamily, fontSize),
                       background = buttonColor,
                       foreground = foregroundColor,
                       activebackground = hoverColor,
                       activeforeground = foregroundColor,
                       relief = tk.FLAT
                       )
    return button

def createEntry(parent, width, fontSize):
    entry = tk.Entry(parent,
                     width = width,
                     font = (fontFamily, fontSize),
                     background = entryColor,
                     foreground = "#000000"
                     )
    return entry

def createRadioButton(parent, value, userInput, text):
    radioButton = tk.Radiobutton(parent,
                                 value = value,
                                 variable = userInput,
                                 text = text,
                                 font = (fontFamily, 19),
                                 background = backgroundColor,
                                 foreground = foregroundColor,
                                 activebackground = backgroundColor,
                                 activeforeground = foregroundColor,
                                 indicatoron = False,
                                 selectcolor = hoverColor,
                                 borderwidth = 0
                                 )
    return radioButton

def createTools(toolsContainer, displayContainer):
    userInput = tk.IntVar(value = -1)
    operations = ["Merge PDFs", "Split PDF", "Delete pages", "Rotate pages"]
    for index, value in enumerate(operations):
        button = createRadioButton(toolsContainer, index, userInput, value)
        button.configure(command = lambda idx = index : callEventListener(displayContainer, idx))
        handleHover(button)
        renderButton(button, index)

