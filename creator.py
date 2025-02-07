import tkinter as tk
from handler import callEventListener, handleHover
from render import renderButton
from constants import (
        backgroundColor,
        foregroundColor,
        borderColor,
        hoverColor,
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

def createLabel(parent, fontSize, text, type = ""):
    label = tk.Label(parent,
                     text = text,
                     font = (fontFamily, fontSize, type),
                     background = backgroundColor,
                     foreground = foregroundColor
                    )
    return label

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

