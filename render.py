import tkinter as tk
import creator
import handler

def renderButton(button, index):
    if index % 2:
        button.pack(fill = tk.X, pady = 5)
    else:
        button.pack(fill = tk.X, pady = 20)

def clearDisplay(displayContainer):
    for frame in displayContainer.winfo_children():
        frame.destroy()

def setupPage(displayContainer):
    clearDisplay(displayContainer)
    frame = creator.createFrame(displayContainer, 570, 600)
    frame.pack_propagate(False)
    return frame

def renderPage(frame, elements):
    for element in elements:
        element.pack(pady = 10)
    frame.pack()

def renderMergePage(displayContainer):
    pdfs = []
    flag = [False]
    frame = setupPage(displayContainer)
    elements = [
        creator.createLabel(frame, 20, "Click the following button to add PDF files and click cancel in the dialog box to stop adding the files.", 500),
        creator.createButton(frame, "Add PDFs", 20),
        creator.createLabel(frame, 20, "Click the following button to reorder, merge PDFs.", 500),
        creator.createButton(frame, "Reorder and Merge PDFs", 20),
    ]
    elements[1].configure(command = lambda: handler.addPDFs(pdfs, flag))
    elements[3].configure(command = lambda: handler.openMergeWindow(pdfs, flag))
    renderPage(frame, elements)

def renderSplitPage(displayContainer):
    pdf = [None]
    frame = setupPage(displayContainer)
    elements = [
        creator.createLabel(frame, 20, "Click the following button to add a PDF file.", 500),
        creator.createButton(frame, "Add PDF", 20),
        creator.createLabel(frame, 20, "Total no. of pages : -"),
        creator.createLabel(frame, 19, "Enter the page numbers seperated by \",\". (For example: 1, 3, 15). This results in the following partitions: (1, 2-3, 4-15, 16-END)", 500),
        creator.createEntry(frame, 35, 19),
        creator.createButton(frame, "Split PDF", 20)
    ]
    elements[1].configure(command = lambda: handler.addPDF(pdf, elements[2]))
    elements[5].configure(command = lambda: handler.splitPDF(pdf, elements[4]))
    renderPage(frame, elements)


def renderDeletePage(displayContainer):
    pdf = [None]
    frame = setupPage(displayContainer)
    elements = [
        creator.createLabel(frame, 20, "Click the following button to add a PDF file.", 500),
        creator.createButton(frame, "Add PDF", 20),
        creator.createLabel(frame, 20, "Total no. of pages : -"),
        creator.createLabel(frame, 19, "Enter the page numbers seperated by \",\". (For example: 1, 3, 11-15)", 500),
        creator.createEntry(frame, 35, 19),
        creator.createButton(frame, "Delete pages", 20)
    ]
    elements[1].configure(command = lambda: handler.addPDF(pdf, elements[2]))
    elements[5].configure(command = lambda: handler.deletePages(pdf, elements[4]))
    renderPage(frame, elements)

def renderRotatePage(displayContainer):
    pdf = [None]
    frame = setupPage(displayContainer)
    elements = [
        creator.createLabel(frame, 20, "Click the following button to add a PDF file.", 500),
        creator.createButton(frame, "Add PDF", 20),
        creator.createLabel(frame, 20, "Total no. of pages : -"),
        creator.createLabel(frame, 19, "Enter the page numbers seperated by \",\". (For example: 1, 3, 11-15)", 500),
        creator.createEntry(frame, 35, 19),
        creator.createButton(frame, "Rotate pages", 20)
    ]
    elements[1].configure(command = lambda: handler.addPDF(pdf, elements[2]))
    elements[5].configure(command = lambda: handler.rotatePages(pdf, elements[4]))
    renderPage(frame, elements)

