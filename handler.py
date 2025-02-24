from constants import hoverColor, backgroundColor, eventMap
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename
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
    pattern = r"^\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*$"
    match = re.fullmatch(pattern, pagesEntry)
    pages = []
    if match:
        points = pagesEntry.split(',')
        for point in points:
            if '-' in point:
                startPage, endPage = map(int, point.split('-'))
                if startPage > endPage:
                    tkmb.showerror(title = "Invalid range", message = "The start page is greater than end page in given range")
                    return []
                pages.extend(range(startPage, endPage + 1))
            else:
                pages.append(int(point))
    else:
        tkmb.showerror(title = "Invalid input", message = "Please ensure the input contains only numbers")
    return pages

def checkBreakPoints(breakPoints, noOfPages):
    isValid = all(1 <= point <= noOfPages for point in breakPoints)
    if isValid == False:
        tkmb.showerror(title = "Error", message = "Cannot perform operations on page that is not in valid range. Valid range : 1 to no. of pages in PDF")
    return isValid

def getMetadata(pdf, entry):
    if pdf[0] != None:
        reader = pydf.PdfReader(pdf[0])
        noOfPages = len(reader.pages)
        breakPoints = parseEntry(entry)
        return checkBreakPoints(breakPoints, noOfPages), breakPoints, reader, noOfPages
    else:
        tkmb.showerror(title = "Error", message = "Add a pdf before clicking here.")
        return False, [], pydf.PdfReader("."), 0

def splitPDF(pdf, entry):
    flag, breakPoints, reader, noOfPages = getMetadata(pdf, entry)
    if flag:
        print(breakPoints)

def deletePages(pdf, entry):
    flag, pagesToDelete, reader, noOfPages = getMetadata(pdf, entry)
    if flag and pagesToDelete:
        writer = pydf.PdfWriter()
        currentPage = 1
        while (currentPage <= noOfPages):
            if currentPage not in pagesToDelete:
                writer.insert_page(reader.pages[currentPage - 1], currentPage)
            currentPage += 1
        saveFilePath = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if saveFilePath:
            writer.write(saveFilePath)
            tkmb.showinfo('Deleted Pages', ('The given pages were deleted successfully. PDF stored at : '+saveFilePath))
        else:
            tkmb.showerror('Error', 'No destination was specified')

def rotatePages(pdf, entry):
    flag, breakPoints, reader, noOfPages = getMetadata(pdf, entry)
    if flag:
        print(breakPoints)

