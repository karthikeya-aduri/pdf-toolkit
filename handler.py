from constants import hoverColor, backgroundColor, eventMap
from tkinter.filedialog import askopenfilename, askopenfilenames
import tkinter.messagebox as tkmb
import PyPDF2 as pydf
import re

def onEnter(element):
    element.widget['background'] = hoverColor

def onLeave(element):
    element.widget['background'] = backgroundColor

def handleHover(button):
    button.bind("<Enter>", onEnter)
    button.bind("<Leave>", onLeave)

def callEventListener(displayContainer, index):
    func = eventMap[index]
    if func:
        func(displayContainer)

def addPDFs(pdfs, flag, label):
    filenames = askopenfilenames()
    if filenames:
        pass

def addPDF(pdf, label):
    filename = askopenfilename()
    if filename:
        reader = pydf.PdfReader(filename)
        noOfPages = len(reader.pages)
        label.configure(text = 'Total no. of pages : ' + str(noOfPages))
        pdf[0] = filename

def parseEntry(entry):
    pagesEntry = entry.get().replace(' ', '')
    pattern = r"^\d+(, \d+)*$"
    match = re.fullmatch(pattern, pagesEntry)
    pages = []
    if match:
        points = pagesEntry.split(',')
        for point in points:
            if '-' in point:
                index = point.find('-')
                startPage = int(point[:index])
                endPage = int(point[index+1:])
                for i in range(startPage, endPage + 1):
                    pages.append(i)
            else:
                pages.append(int(point))
    else:
        tkmb.showerror(title = "Invalid input", message = "Please ensure the input contains only numbers")
    return pages

def splitPDF(pdf, entry):
    if pdf[0] != None:
        reader = pydf.PdfReader(pdf[0])
        breakPoints = parseEntry(entry)
        print(breakPoints)
    else:
        tkmb.showerror(title = "No PDF found", message = "Please add a pdf before clicking here.")

def deletePages(pdf, entry):
    if pdf[0] != None:
        reader = pydf.PdfReader(pdf[0])
        breakPoints = parseEntry(entry)
        print(breakPoints)
    else:
        tkmb.showerror(title = "No PDF found", message = "Please add a pdf before clicking here.")

def rotatePages(pdf, entry):
    if pdf[0] != None:
        reader = pydf.PdfReader(pdf[0])
        breakPoints = parseEntry(entry)
        print(breakPoints)
    else:
        tkmb.showerror(title = "No PDF found", message = "Please add a pdf before clicking here.")
