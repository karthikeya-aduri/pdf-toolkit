import os
import tkinter as tk
from constants import hoverColor, backgroundColor, eventMap
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames, asksaveasfilename
import tkinter.messagebox as tkmb
import PyPDF2 as pydf
import re
import creator

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

def addPDFs(pdfs, flag):
    counter = 1
    while True:
        filenames = askopenfilenames(title = f"Add PDFs - {counter}", defaultextension = ".pdf", filetypes = [("PDF Files", "*.pdf")])
        if filenames:
            for filename in filenames:
                pdfs.append(filename)
            counter += 1
        else:
            break
    noOfFilesSelected = len(pdfs)
    if noOfFilesSelected < 2:
        tkmb.showerror(title = "Merge error", message = "Not enough files for merging.")
    else:
        flag[0] = True

def addPDF(pdf, label):
    filename = askopenfilename()
    if filename:
        reader = pydf.PdfReader(filename)
        noOfPages = len(reader.pages)
        label.configure(text = 'Total no. of pages : ' + str(noOfPages))
        pdf[0] = filename

def moveUp(fileList):
    selectedIndices = fileList.curselection()
    for index in selectedIndices:
        if index > 0:
            text = fileList.get(index)
            fileList.delete(index)
            fileList.insert(index - 1, text)
            fileList.selection_set(index - 1)

def moveDown(fileList):
    selectedIndices = fileList.curselection()
    for index in reversed(selectedIndices):
        if index < fileList.size() - 1:
            text = fileList.get(index)
            fileList.delete(index)
            fileList.insert(index + 1, text)
            fileList.selection_set(index + 1)

def clearList(fileList, pdfs = None, flag = None):
    fileList.delete(0, tk.END)
    if flag != None and pdfs != None:
        flag[0] = False
        pdfs.clear()

def addToListbox(pdfs, fileList):
    for file in pdfs:
        fileList.insert(tk.END, file)

def mergePDFs(fileList):
    files = fileList.get(0, tk.END)
    if files:
        saveFilePath = asksaveasfilename(defaultextension = ".pdf", filetypes = [("PDF Files", "*.pdf")])
        if saveFilePath:
            merger = pydf.PdfMerger()
            for file in files:
                merger.append(file)
            merger.write(saveFilePath)
            merger.close()
            tkmb.showinfo(title = "Success", message = f"PDFs merged successfully at {saveFilePath}")
        else:
            tkmb.showerror(title = "Error", message = "No folder was selected to save the output")
    else:
        tkmb.showerror(title = "Merge Error", message = "Please add 2 or more pdfs before trying to merge.")

def openMergeWindow(pdfs, flag):
    if flag[0] == True:
        mergeWindow = creator.createWindow("PDF Merger", "640x480", False, False)
        frame = creator.createFrame(mergeWindow, 640, 480)
        label = creator.createLabel(frame, 15, "Selected PDFs:")
        fileList = creator.createListbox(frame, 100, 10)
        moveUpButton = creator.createButton(frame, "Move up", 15)
        moveDownButton = creator.createButton(frame, "Move down", 15)
        mergeButton = creator.createButton(frame, "Merge PDFs", 15)
        clearListButton = creator.createButton(frame, "Clear List", 15)
        moveUpButton.configure(command = lambda: moveUp(fileList))
        moveDownButton.configure(command = lambda: moveDown(fileList))
        mergeButton.configure(command = lambda: mergePDFs(fileList))
        clearListButton.configure(command = lambda: clearList(fileList, pdfs, flag))
        clearList(fileList)
        addToListbox(pdfs, fileList)
        label.pack()
        fileList.pack(pady = 10)
        moveUpButton.pack()
        moveDownButton.pack(pady = 10)
        mergeButton.pack()
        clearListButton.pack(pady = 10)
        frame.pack()
        mergeWindow.mainloop()
    else:
        tkmb.showerror(title = "Error", message = "Add a pdf before clicking here.")

def parseEntry(entry, pattern):
    pagesEntry = entry.get().replace(' ', '')
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
        tkmb.showerror(title = "Invalid input", message = "Please ensure the input contains only numbers. Also note that \"-\" is invalid in split operation.")
    return pages

def checkBreakPoints(breakPoints, noOfPages):
    isValid = all(1 <= point <= noOfPages for point in breakPoints)
    if isValid == False:
        tkmb.showerror(title = "Error", message = "Cannot perform operations on page that is not in valid range. Valid range : 1 to no. of pages in PDF")
    return isValid

def getMetadata(pdf, entry, pattern):
    if pdf[0] != None:
        reader = pydf.PdfReader(pdf[0])
        noOfPages = len(reader.pages)
        breakPoints = parseEntry(entry, pattern)
        return checkBreakPoints(breakPoints, noOfPages), breakPoints, reader, noOfPages
    else:
        tkmb.showerror(title = "Error", message = "Add a pdf before clicking here.")
        return False, [], pydf.PdfReader("."), 0

def splitPDF(pdf, entry):
    pattern = r"^\d+(,\d+)*$"
    flag, breakPoints, reader, noOfPages = getMetadata(pdf, entry, pattern)
    if flag:
        breakPoints.append(noOfPages)
        baseName = os.path.splitext(os.path.basename(pdf[0]))[0]
        noOfSplits = len(breakPoints)
        currentSplit = 1
        currentPage = 1
        baseFolder = askdirectory()
        if baseFolder:
            while (currentSplit <= noOfSplits):
                writer = pydf.PdfWriter()
                pageIndex = 1
                while (currentPage <= breakPoints[currentSplit - 1]):
                    writer.insert_page(reader.pages[currentPage - 1], pageIndex)
                    currentPage += 1
                    pageIndex += 1
                    writer.write(f"{baseFolder}/{baseName} part - {currentSplit}.pdf")
                    writer.close()
                currentSplit += 1
            tkmb.showinfo(title = "Split Operation", message = ("The partitions are stored at " + baseFolder))
        else:
            tkmb.showerror(title = "Error", message = "No folder was selected for saving the partitions.")

def deletePages(pdf, entry):
    pattern = r"^\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*$"
    flag, pagesToDelete, reader, noOfPages = getMetadata(pdf, entry, pattern)
    if flag and pagesToDelete:
        saveFilePath = asksaveasfilename(defaultextension = ".pdf", filetypes = [("PDF Files", "*.pdf")])
        if saveFilePath:
            writer = pydf.PdfWriter()
            currentPage = 1
            while (currentPage <= noOfPages):
                if currentPage not in pagesToDelete:
                    writer.insert_page(reader.pages[currentPage - 1], currentPage)
                currentPage += 1
            saveFilePath = asksaveasfilename(defaultextension = ".pdf", filetypes = [("PDF Files", "*.pdf")])
            writer.write(saveFilePath)
            writer.close()
            tkmb.showinfo('Deleted Pages', ('The given pages were deleted successfully. PDF stored at : '+saveFilePath))
        else:
            tkmb.showerror('Error', 'No destination was specified for saving the modified pdf file.')

def rotatePages(pdf, entry):
    pattern = r"^\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*$"
    flag, pagesToRotate, reader, noOfPages = getMetadata(pdf, entry, pattern)
    if flag:
        pass

