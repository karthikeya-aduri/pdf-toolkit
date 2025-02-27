import tkinter as tk
from creator import createWindow, createFrame, createLabel, createTools

def main():
    window = createWindow('PDF Toolkit', '800x600', False, True)
    toolsContainer = createFrame(window, 230, 600, 0.75)
    displayContainer = createFrame(window, 570, 600, 0.75)

    toolsContainerLabel = createLabel(toolsContainer, 24, "Tools", 0, "underline")
    toolsContainerLabel.pack(pady = 5)

    displayContainerLabel = createLabel(displayContainer, 20,
                                        "Click the buttons in the tools pane to use the application.")
    displayContainerLabel.configure(wraplength = 500)
    displayContainerLabel.place(x = 285, y = 300, anchor = "center")

    createTools(toolsContainer, displayContainer)

    toolsContainer.pack(side = tk.LEFT)
    displayContainer.pack(side = tk.RIGHT)

    window.mainloop()

main()
