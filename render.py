import tkinter as tk

def renderButton(button, index):
    if index % 2:
        button.pack(fill = tk.X, pady = 5)
    else:
        button.pack(fill = tk.X, pady = 20)

def clearDisplay(displayContainer):
    for frame in displayContainer.winfo_children():
        frame.destroy()

def renderMergePage(displayContainer):
    clearDisplay(displayContainer)
    print('Merge')

def renderSplitPage(displayContainer):
    clearDisplay(displayContainer)
    print('Split')

def renderDeletePage(displayContainer):
    clearDisplay(displayContainer)
    print('Delete')

def renderRotatePage(displayContainer):
    clearDisplay(displayContainer)
    print('Rotate')
