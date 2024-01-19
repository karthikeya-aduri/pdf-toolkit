import tkinter as tk
import tkinter.font as tkf
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
from PyPDF2 import PdfWriter,PdfReader
from os import listdir

class Application:
    windowBgdColor = "#121212"
    windowFont = "Courier"
    fontColor = "#FFFFFF"
    borderColor = "#3B3B3B"
    hoverColor = "#3A3A3A"
    btnColor = "#0F3180"

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
                             command=lambda:self.displayMergePage(mainFrame),
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
                             command=lambda:self.displaySplitPage(mainFrame),
                             text="Split PDF",
                             font=(self.windowFont,17),
                             fg=self.fontColor,
                             background=self.windowBgdColor,
                             activebackground=self.windowBgdColor,
                             activeforeground=self.fontColor,
                             relief=tk.FLAT
                             )
        toolsLabel.pack()
        mergeBtn.pack()
        splitBtn.pack()

        mergeBtn.bind("<Enter>",self.onEnter)
        mergeBtn.bind("<Leave>",self.onLeave)
        splitBtn.bind("<Enter>",self.onEnter)
        splitBtn.bind("<Leave>",self.onLeave)

    def addPdf(self,label2):
        self.tempFilePath = tkfd.askopenfilename()
        if not self.tempFilePath:
            tkmb.showerror('Split Error', 'Error: No file was selected')
        else:
            reader = PdfReader(self.tempFilePath)
            noOfPages = len(reader.pages)
            label2.configure(text=("Number of Pages : "+str(noOfPages)))

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

    def checkPages(self,pagesList,noOfPages):
        flag=True
        for i in range(len(pagesList)):
            if pagesList[i].isnumeric() and int(pagesList[i])<noOfPages:
                pagesList[i]=int(pagesList[i])
            else:
                flag=False
                break
        if flag:
            pagesList.sort()
        return flag

    def splitLoop(self,reader,noOfPages,pagesList):
        flag=self.checkPages(pagesList,noOfPages)
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
                partNumber+=1
                pageIndex=0
                while(currentPage<noOfPages):
                    pageObject = reader.pages[currentPage]
                    writer.insert_page(pageObject,pageIndex)
                    currentPage+=1
                    pageIndex+=1
                fileName = directoryPath+'/Part '+str(partNumber+1)+'.pdf'
                writer.write(fileName)
                writer.close()
        else:
            tkmb.showerror('Split Error', 'Error: Invalid input was given. Please check number of pages in the given pdf')

    def splitPDF(self,pagesEntry):
        pages = pagesEntry.get()
        if not pages:
            tkmb.showerror('Split Error','Please enter the page numbers at which you wish to split')
        else:
            pagesList = pages.split(',')
            if not self.tempFilePath:
                tkmb.showerror('Split Error', 'Error: No file was selected')
            else:
                reader = PdfReader(self.tempFilePath)
                noOfPages = len(reader.pages)
                self.splitLoop(reader,noOfPages,pagesList)

    def clearMainFrame(self,mainFrame):
        for frame in mainFrame.winfo_children():
            frame.destroy()
        self.tempFilePath=''

    def displayMergePage(self,mainFrame):
        self.clearMainFrame(mainFrame)
        mergeFrame1 = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        mergeFrame1.configure(width=440,height=180)
        mergeFrame1.pack_propagate(False)
        
        mergeFrame2 = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        mergeFrame2.configure(width=440,height=300)
        mergeFrame2.pack_propagate(False)

        label1 = tk.Label(mergeFrame1,
                          text="Click the following button to merge all PDFs inside a folder/directory",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=400
                          )
        btn1 = tk.Button(mergeFrame1,
                         text="Add a directory",
                         command=lambda:self.addPdfsInDirectory(),
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
                          wraplength=440
                          )
        btn2 = tk.Button(mergeFrame2,
                         text="Add PDFs",
                         command=lambda:self.addPdfFiles(),
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
        splitFrame.configure(width=440,height=480)
        splitFrame.pack_propagate(False)
        label1 = tk.Label(splitFrame,
                          text="Click the following button to add the PDF and enter the number of pages after which the spliting occurs (seperated by ,)",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=390
                          )
        btn1 = tk.Button(splitFrame,
                         text="Add PDF",
                         command=lambda:self.addPdf(label2),
                         font=(self.windowFont,17),
                         fg=self.fontColor,
                         background=self.btnColor,
                         activebackground=self.hoverColor,
                         activeforeground=self.fontColor,
                         relief=tk.FLAT
                         )
        label2 = tk.Label(splitFrame,
                          text="Number of Pages : -",
                          font=(self.windowFont,17),
                          bg=self.windowBgdColor,
                          fg=self.fontColor,
                          wraplength=390
                          )
        pagesEntry = tk.Entry(splitFrame,
                             width=200,
                             font=(self.windowFont, 17),
                             bg=self.hoverColor,
                             fg=self.fontColor
                             )
        btn2 = tk.Button(splitFrame,
                         text="Split",
                         command=lambda:self.splitPDF(pagesEntry),
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

    def createWindow(self):
        window = tk.Tk()
        window.title("PDF Toolkit")

        window.geometry("640x480")
        window.minsize(width=640,height=480)
        window.maxsize(width=640,height=480)

        toolsFrame = tk.Frame(window, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        toolsFrame.configure(width=200,height=480)
        toolsFrame.pack_propagate(False)

        mainFrame = tk.Frame(window, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor)
        mainFrame.configure(width=440,height=480)
        mainFrame.pack_propagate(False)

        self.createWidgets(toolsFrame,mainFrame)

        toolsFrame.pack(side=tk.LEFT)
        mainFrame.pack(side=tk.RIGHT)

        window.mainloop()

app = Application()
