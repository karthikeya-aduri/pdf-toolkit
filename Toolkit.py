import tkinter as tk
import tkinter.font as tkf
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
from PyPDF2 import PdfWriter,PdfReader
from os import defpath, listdir

class Application:
    windowBgdColor = "#121212"
    windowFont = "Courier"
    fontColor = "#FFFFFF"
    borderColor = "#3B3B3B"
    hoverColor = "#3A3A3A"
    btnColor = "#0F3180"
    entryColor = "#ACACAC"

    tempFilePath = ''

    def __init__(self):
        self.createWindow()

    def onEnter(self,e):
        e.widget['background']=self.hoverColor

    def onLeave(self,e):
        e.widget['background']=self.windowBgdColor

    def createWidgets(self,toolsFrame,mainFrame):
        toolsLabel = tk.Label(toolsFrame, 
                              text="Tools",
                              font=(self.windowFont,20,tkf.BOLD),
                              bg=self.windowBgdColor,
                              fg=self.fontColor
                              )
        mergeBtn = tk.Button(toolsFrame, 
                             width="200",
                             command=lambda: self.displayMergePage(mainFrame),
                             text="Merge PDFs",
                             font=(self.windowFont,17),
                             fg=self.fontColor,
                             background=self.windowBgdColor,
                             activebackground=self.windowBgdColor,
                             activeforeground=self.fontColor,
                             relief=tk.FLAT
                             )
        splitBtn = tk.Button(toolsFrame, 
                             width="200",
                             command=lambda: self.displaySplitPage(mainFrame),
                             text="Split PDF",
                             font=(self.windowFont,17),
                             fg=self.fontColor,
                             background=self.windowBgdColor,
                             activebackground=self.windowBgdColor,
                             activeforeground=self.fontColor,
                             relief=tk.FLAT
                             )
        deleteBtn = tk.Button(toolsFrame, 
                              width="200",
                              command=lambda: self.displayDeletePage(mainFrame),
                              text="Delete Pages",
                              font=(self.windowFont,17),
                              fg=self.fontColor,
                              background=self.windowBgdColor,
                              activebackground=self.windowBgdColor,
                              activeforeground=self.fontColor,
                              relief=tk.FLAT
                              )
        toolsLabel.pack(pady=10)
        mergeBtn.pack()
        splitBtn.pack(pady=10)
        deleteBtn.pack()

        mergeBtn.bind("<Enter>",self.onEnter)
        mergeBtn.bind("<Leave>",self.onLeave)
        splitBtn.bind("<Enter>",self.onEnter)
        splitBtn.bind("<Leave>",self.onLeave)
        deleteBtn.bind("<Enter>",self.onEnter)
        deleteBtn.bind("<Leave>",self.onLeave)

    def addPdf(self,label2):
        self.tempFilePath = tkfd.askopenfilename()
        if not self.tempFilePath:
            tkmb.showerror('Split Error', 'Error: No file was selected')
        else:
            reader = PdfReader(self.tempFilePath)
            noOfPages = len(reader.pages)
            label2.configure(text=("Total number of Pages : "+str(noOfPages)))

    def addPdfFiles(self):
        filePaths = []
        while True:
            heading = "Add files"
            tempPaths = tkfd.askopenfilenames(title=heading)
            if not tempPaths:
                break
            else:
                for eachFile in tempPaths:
                    filePaths.append(eachFile)
        noOfFilesSelected=len(filePaths)
        if noOfFilesSelected<2:
            tkmb.showerror('Merge Error', ('Error: Not enough files for merging. PDFs Selected = '+str(noOfFilesSelected)))
        else:
            self.mergePdfsIn(filePaths)

    def addPdfsInDirectory(self):
        directoryPath=tkfd.askdirectory()
        if not directoryPath:
            tkmb.showerror('Merge Error', 'Error: No directory was selected')
        else:
            filePaths = []
            for eachFile in listdir(directoryPath):
                if eachFile.endswith(".pdf"):
                    tempPath=directoryPath+'/'+eachFile
                    filePaths.append(tempPath)
            noOfFilesSelected=len(filePaths)
            if noOfFilesSelected<2:
                tkmb.showerror('Merge Error', ('Error: Not enough files for merging. PDFs Selected = '+str(noOfFilesSelected)))
            else:
                self.mergePdfsIn(filePaths)

    def mergePdfsIn(self,filePaths):
        merger = PdfWriter()
        for pdf in filePaths:
            merger.append(pdf)
        tkmb.showinfo('PDF Merge',('Merged successfully. Please specify the destination'))
        destPath = tkfd.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files","*.pdf")])
        if not destPath:
            tkmb.showerror('Merge Error', 'Error: Destination was not specified.')
        else:
            merger.write(destPath)
            tkmb.showinfo('PDF Merge', ('Merged file stored at '+destPath))
            merger.close()

    def checkPagesForSplit(self,pagesList,noOfPages):
        flag=True
        for i in range(len(pagesList)):
            if pagesList[i].isnumeric() and int(pagesList[i])<=noOfPages:
                pagesList[i]=int(pagesList[i])
            else:
                flag=False
                break
        if flag:
            pagesList.sort()
        return flag

    def splitLoop(self,reader,noOfPages,pagesList):
        flag=self.checkPagesForSplit(pagesList,noOfPages)
        if flag:
            noOfDivisions = len(pagesList)
            partNumber=0
            currentPage=0
            directoryPath = tkfd.askdirectory()
            if not directoryPath:
                tkmb.showerror('Merge Error', 'Error: No directory was selected')
            else:
                for partNumber in range(noOfDivisions):
                    writer = PdfWriter()
                    pageIndex=0
                    while(currentPage<pagesList[partNumber]):
                        pageObject = reader.pages[currentPage]
                        writer.insert_page(pageObject,pageIndex)
                        currentPage+=1
                        pageIndex+=1
                    fileName = directoryPath+'/Part '+str(partNumber+1)+'.pdf'
                    writer.write(fileName)
                    writer.close()
                writer = PdfWriter()
                partNumber+=2
                pageIndex=0
                while(currentPage<noOfPages):
                    pageObject = reader.pages[currentPage]
                    writer.insert_page(pageObject,pageIndex)
                    currentPage+=1
                    pageIndex+=1
                fileName = directoryPath+'/Part '+str(partNumber)+'.pdf'
                writer.write(fileName)
                writer.close()
                tkmb.showinfo('PDF Split', ('The resultant pdfs are stored at '+directoryPath+'/Part 1 - '+str(partNumber)+'.pdf'))
        else:
            tkmb.showerror('Split Error', 'Error: Invalid input was given. Please check number of pages in the given pdf')

    def splitPDF(self,pagesEntry):
        pages = pagesEntry.get()
        if not pages:
            tkmb.showerror('Split Error', 'Error: Please enter the page numbers at which you wish to split')
        else:
            pagesList = pages.split(',')
            if not self.tempFilePath:
                tkmb.showerror('Split Error', 'Error: No file was selected')
            else:
                reader = PdfReader(self.tempFilePath)
                noOfPages = len(reader.pages)
                self.splitLoop(reader,noOfPages,pagesList)

    def removeRedundancies(self,tempList1):
        for i in tempList1:
            for j in  tempList1:
                if ((i[0]<j[0] and i[1]>j[0]) and (i[0]<j[1] and i[1]>j[1])):
                    tempList1.remove(j)
                elif ((i[0]<j[0] and i[1]>j[0]) and (i[0]<j[1] and i[1]<j[1])):
                    i[1]=j[1];
                    tempList1.remove(j)
        return tempList1

    def mergeLists(self,tempList1,tempList2):
        tempList=[]
        tempList1.sort()
        tempList1=self.removeRedundancies(tempList1)
        tempList2.sort()
        i=0
        j=0
        while(i<len(tempList1) and j<len(tempList2)):
            if(tempList2[j]<tempList1[i][0]):
                tempList.append(tempList2[j])
                j+=1
            elif(tempList2[j]>tempList1[i][0] and tempList2[j]<tempList1[i][1]):
                if tempList1[i] not in tempList:
                    tempList.append(tempList1[i])
                j+=1
            else:
                if tempList1[i] not in tempList:
                    tempList.append(tempList1[i])
                i+=1
        while(i<len(tempList1)):
            if tempList1[i] not in tempList:
                tempList.append(tempList1[i])
            i+=1
        while(j<len(tempList2)):
            tempList.append(tempList2[j])
            j+=1
        return tempList

    def sortPagesList(self,pagesList,noOfPages):
        flag = True
        tempList1 = []
        tempList2 = []
        for i in range(len(pagesList)):
            if "-" in pagesList[i]:
                hyphenIndex = pagesList[i].rfind('-')
                limit1 = pagesList[i][:hyphenIndex]
                limit2 = pagesList[i][hyphenIndex+1:]
                if limit1.isnumeric() and limit2.isnumeric() and int(limit1)<=noOfPages and int(limit2)<=noOfPages:
                    temp = []
                    limit1 = int(limit1)
                    limit2 = int(limit2)
                    if limit1<limit2:
                        temp.append(limit1)
                        temp.append(limit2)
                    else:
                        temp.append(limit2)
                        temp.append(limit1)
                    tempList1.append(temp)
                else:
                    flag=False
                    break
            else:
                if pagesList[i].isnumeric() and int(pagesList[i])<=noOfPages:
                    tempList2.append(int(pagesList[i]))
                else:
                    flag=False
                    break
        tempList=[]
        if flag:
            tempList=self.mergeLists(tempList1,tempList2)
        return tempList

    def deleteLoop(self,reader,noOfPages,pagesList):
        pagesList=self.sortPagesList(pagesList,noOfPages)
        if pagesList:
            pageNumberList = []
            for i in pagesList:
                if type(i) is list:
                    for j in range(i[0],i[1]+1):
                        pageNumberList.append(j-1)
                else:
                    pageNumberList.append(i-1)
            writer = PdfWriter()
            currentPage=0
            index=0
            while(currentPage<noOfPages):
                if currentPage not in pageNumberList:
                    pageObj = reader.pages[currentPage]
                    writer.insert_page(pageObj,index)
                    index+=1
                currentPage+=1
            filePath = tkfd.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if filePath:
                writer.write(filePath)
                tkmb.showinfo('Delete Pages', ('The given pages were deleted successfully. PDF stored at : '+filePath))
            else:
                tkmb.showerror('Delete Error', 'Error: No destination was specified')
        else:
            tkmb.showerror('Delete Error', 'Error: Invalid input was found in the entry. Please check number of pages in the given pdf')

    def deletePages(self,pagesEntry):
        pages = pagesEntry.get()
        if not pages:
            tkmb.showerror('Delete Error','Error: Please enter the page numbers at which you wish to delete')
        else:
            pagesList = pages.split(',')
            if not self.tempFilePath:
                tkmb.showerror('Delete Error', 'Error: No file was selected')
            else:
                reader = PdfReader(self.tempFilePath)
                noOfPages = len(reader.pages)
                self.deleteLoop(reader,noOfPages,pagesList)

    def clearMainFrame(self,mainFrame):
        for frame in mainFrame.winfo_children():
            frame.destroy()
        self.tempFilePath=''

    def displayMergePage(self,mainFrame):
        self.clearMainFrame(mainFrame)
        mergeFrame1 = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        mergeFrame1.configure(width=500,height=200)
        mergeFrame1.pack_propagate(False)
        
        mergeFrame2 = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        mergeFrame2.configure(width=500,height=300)
        mergeFrame2.pack_propagate(False)

        label1 = tk.Label(mergeFrame1,
                          text="Click the following button to merge all PDFs inside a folder/directory",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=500
                          )
        btn1 = tk.Button(mergeFrame1,
                         text="Add a directory",
                         command=lambda: self.addPdfsInDirectory(),
                         font=(self.windowFont,17),
                         bg=self.btnColor,
                         fg=self.fontColor,
                         activebackground=self.hoverColor,
                         activeforeground=self.fontColor,
                         relief=tk.FLAT
                         )
        label2 = tk.Label(mergeFrame2,
                          text="Click the following button to merge PDFs from different directories. (Click cancel to stop adding)",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=500
                          )
        btn2 = tk.Button(mergeFrame2,
                         text="Add PDFs",
                         command=lambda: self.addPdfFiles(),
                         font=(self.windowFont,17),
                         bg=self.btnColor,
                         fg=self.fontColor,
                         activebackground=self.hoverColor,
                         activeforeground=self.fontColor,
                         relief=tk.FLAT
                         ) 
        label1.pack(pady=10)
        btn1.pack(pady=5)
        label2.pack(pady=20)
        btn2.pack()
        mergeFrame1.pack()
        mergeFrame2.pack()

    def displaySplitPage(self,mainFrame):
        self.clearMainFrame(mainFrame)
        splitFrame = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        splitFrame.configure(width=500,height=500)
        splitFrame.pack_propagate(False)
        label1 = tk.Label(splitFrame,
                          text="Click the following button to add the PDF and enter the number of pages after which the spliting occurs (seperated by ,)",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=500
                          )
        btn1 = tk.Button(splitFrame,
                         text="Add PDF",
                         command=lambda: self.addPdf(label2),
                         font=(self.windowFont,17),
                         fg=self.fontColor,
                         background=self.btnColor,
                         activebackground=self.hoverColor,
                         activeforeground=self.fontColor,
                         relief=tk.FLAT
                         )
        label2 = tk.Label(splitFrame,
                          text="Total number of Pages : -",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=500
                          )
        pagesEntry = tk.Entry(splitFrame,
                              width=35,
                              font=(self.windowFont, 15),
                              bg=self.entryColor,
                              fg="#000000"
                             )
        btn2 = tk.Button(splitFrame,
                         text="Split",
                         command=lambda: self.splitPDF(pagesEntry),
                         font=(self.windowFont,17),
                         fg=self.fontColor,
                         background=self.btnColor,
                         activebackground=self.hoverColor,
                         activeforeground=self.fontColor,
                         relief=tk.FLAT
                         )
        label1.pack(pady=10)
        btn1.pack()
        label2.pack(pady=10)
        pagesEntry.pack(pady=15)
        btn2.pack()
        splitFrame.pack()

    def displayDeletePage(self,mainFrame):
        self.clearMainFrame(mainFrame)
        delFrame = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        delFrame.configure(width=500,height=500)
        delFrame.pack_propagate(False)
        delFrame.pack()
        label1 = tk.Label(delFrame,
                          text="Click the following button to add the PDF and enter the page numbers that are to be removed (seperated by ,)",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=450
                          )
        btn1 = tk.Button(delFrame,
                         text="Add PDF",
                         command=lambda: self.addPdf(label2),
                         font=(self.windowFont,17),
                         fg=self.fontColor,
                         background=self.btnColor,
                         activebackground=self.hoverColor,
                         activeforeground=self.fontColor,
                         relief=tk.FLAT
                         )
        label2 = tk.Label(delFrame,
                          text="Total number of Pages : -",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=500
                          )
        label3 = tk.Label(delFrame,
                          text="(You may use '-' instead of writing every page number. For example: 1-3,10,15-20)",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=500
                          )
        pagesEntry = tk.Entry(delFrame,
                              width=35,
                              font=(self.windowFont, 15),
                              bg=self.entryColor,
                              fg="#000000"
                              )
        btn2 = tk.Button(delFrame,
                         text="Delete",
                         command=lambda: self.deletePages(pagesEntry),
                         font=(self.windowFont,17),
                         fg=self.fontColor,
                         background=self.btnColor,
                         activebackground=self.hoverColor,
                         activeforeground=self.fontColor,
                         relief=tk.FLAT
                         )
        label1.pack(pady=10)
        btn1.pack(pady=10)
        label2.pack(pady=5)
        label3.pack(pady=5)
        pagesEntry.pack(pady=10)
        btn2.pack(pady=5)

    def createWindow(self):
        window = tk.Tk()
        window.title("PDF Toolkit")

        window.geometry("700x500")
        window.minsize(width=700,height=500)
        window.maxsize(width=700,height=500)

        toolsFrame = tk.Frame(window, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        toolsFrame.configure(width=200,height=500)
        toolsFrame.pack_propagate(False)

        mainFrame = tk.Frame(window, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        mainFrame.configure(width=500,height=500)
        mainFrame.pack_propagate(False)

        mainLabel = tk.Label(mainFrame,
                             text="Click the buttons in the tools pane to use the application.",
                             font=(self.windowFont, 17),
                             bg=self.windowBgdColor,
                             fg=self.fontColor,
                             wraplength=500
                             )
        self.createWidgets(toolsFrame,mainFrame)

        toolsFrame.pack(side=tk.LEFT)
        mainFrame.pack(side=tk.RIGHT)
        mainLabel.place(x=250,y=250,anchor="center")

        window.mainloop()

app = Application()
