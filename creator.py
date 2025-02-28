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

def createWindow(title, geometry, resizableFlag, iconFlag):
    window = tk.Tk()

    window.title(title)
    window.geometry(geometry)
    window.resizable(resizableFlag, resizableFlag)
    icon = tk.PhotoImage(file = "icon.png")
    if iconFlag:
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

def createMenuButton(parent, value, userInput, text):
    menuButton = tk.Radiobutton(parent,
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
    return menuButton

def createListbox(parent, width, height):
    listbox = tk.Listbox(parent,
                         width = width,
                         height = height,
                         background = backgroundColor,
                         foreground = foregroundColor
                        )
    return listbox

def createRadioButton(parent, width, text, variable, value):
    radioButton = tk.Radiobutton(parent,
                                 width = width,
                                 text = text,
                                 variable = variable,
                                 value = value,
                                 font = (fontFamily, 15),
                                 background = backgroundColor,
                                 foreground = foregroundColor,
                                 activebackground = backgroundColor,
                                 activeforeground = foregroundColor,
                                 selectcolor = hoverColor,
                                 indicatoron = False,
                                 relief = tk.FLAT
                                 )
    return radioButton

def createRotateOptions(frame, usrChoice1, usrChoice2):
    rotateOptions = createFrame(frame, 570, 20)
    clockwiseButton = createRadioButton(rotateOptions, 14, "Clockwise", usrChoice1, 1)
    clockwiseButton.grid(row = 0, column = 0, padx = 3, pady = 10)
    antiClockwiseButton = createRadioButton(rotateOptions, 14, "Anti-clockwise", usrChoice1, 2)
    antiClockwiseButton.grid(row = 0, column = 1, padx = 3, pady = 10)
    rotate90 = createRadioButton(rotateOptions, 14, "90°", usrChoice2, 1)
    rotate90.grid(row = 1, column = 0, padx = 3, pady = 10)
    rotate180 = createRadioButton(rotateOptions, 14, "180°", usrChoice2, 2)
    rotate180.grid(row = 1, column = 1, padx = 3, pady = 10)
    rotate270 = createRadioButton(rotateOptions, 14, "270°", usrChoice2, 3)
    rotate270.grid(row = 1, column = 2, padx = 3, pady = 10)
    return rotateOptions

def createTools(toolsContainer, displayContainer):
    userInput = tk.IntVar(value = -1)
    operations = ["Merge PDFs", "Split PDF", "Delete pages", "Rotate pages"]
    for index, value in enumerate(operations):
        button = createMenuButton(toolsContainer, index, userInput, value)
        button.configure(command = lambda idx = index : callEventListener(displayContainer, idx))
        handleHover(button)
        renderButton(button, index)


