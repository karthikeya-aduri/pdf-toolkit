import tkinter as tk
from handler import handleHover, placeButtons
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

def createFrame(parent, width, height):
    frame = tk.Frame(parent,
                     width = width,
                     height = height,
                     background = backgroundColor,
                     highlightthickness = 0.75,
                     highlightbackground = borderColor
                     )
    frame.pack_propagate(False)
    return frame

def createHeadingLabel(parent, text):
    headingLabel = tk.Label(parent,
                     text = text,
                     font = (fontFamily, 24, "underline"),
                     background = backgroundColor,
                     foreground = foregroundColor
                    )
    return headingLabel

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
        handleHover(button)
        placeButtons(button, index)

