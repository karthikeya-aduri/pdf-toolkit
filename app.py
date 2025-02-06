import tkinter as tk
from creator import createWindow, createFrame, createHeadingLabel, createTools

def main():
    window = createWindow('PDF Toolkit', '800x600', False)
    toolsContainer = createFrame(window, 230, 600)
    displayContainer = createFrame(window, 570, 600)

    toolsContainerLabel = createHeadingLabel(toolsContainer, "Tools:")
    toolsContainerLabel.pack(pady = 5)

    createTools(toolsContainer, displayContainer)

    toolsContainer.pack(side = tk.LEFT)
    displayContainer.pack(side = tk.RIGHT)

    window.mainloop()

main()
