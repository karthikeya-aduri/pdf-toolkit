import tkinter as tk
import tkinter.font as tkf
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
from PyPDF2 import PdfWriter
from os import listdir

class Application:
    windowBgdColor = "#121212"
    windowFont = "Courier New"
    fontColor = "#FFFFFF"
    borderColor = "#3B3B3B"
    hoverColor = "#3A3A3A"
    btnColor = "#0F3180"

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
        
    def clearMainFrame(self,mainFrame):
        for frame in mainFrame.winfo_children():
            frame.destroy()

    def displayMergePage(self,mainFrame):
        self.clearMainFrame(mainFrame)
        mergeFrame1 = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor) 
        mergeFrame1.configure(width=440,height=170)
        mergeFrame1.pack_propagate(False)
        
        mergeFrame2 = tk.Frame(mainFrame, bg=self.windowBgdColor, highlightthickness=0.75, highlightbackground=self.borderColor) 
        mergeFrame2.configure(width=440,height=310)
        mergeFrame2.pack_propagate(False)

        addFolderLabel = tk.Label(mergeFrame1,
                                  text="Click the following button to merge all PDFs inside a folder/directory",
                                  font=(self.windowFont,17),
                                  bg=self.windowBgdColor, 
                                  fg=self.fontColor,
                                  wraplength=400
        )
        addFolderBtn = tk.Button(mergeFrame1,
                                 text="Add a directory",
                                 command=self.mergePdfsInDirectory,
                                 font=(self.windowFont,17),
                                 bg=self.btnColor, 
                                 fg=self.fontColor,
                                 activebackground=self.hoverColor,
                                 activeforeground=self.fontColor, 
                                 relief=tk.FLAT
        )
        addPDFsLabel = tk.Label(mergeFrame2,
                                text="Click the following button to merge PDFs from different directories. (Click cancel to stop adding)",
                                font=(self.windowFont,17),
                                bg=self.windowBgdColor, 
                                fg=self.fontColor,
                                wraplength=440
        )
        addPDFsBtn = tk.Button(mergeFrame2,
                               text="Add PDFs",
                               command=self.mergePdfFiles,
                               font=(self.windowFont,17),
                               bg=self.btnColor, 
                               fg=self.fontColor,
                               activebackground=self.hoverColor,
                               activeforeground=self.fontColor, 
                               relief=tk.FLAT
        ) 
        addFolderLabel.pack()
        addFolderBtn.pack(pady=15)
        addPDFsLabel.pack(pady=20)
        addPDFsBtn.pack()
        mergeFrame1.pack()
        mergeFrame2.pack()

    def mergePdfFiles(self):
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

    def mergePdfsInDirectory(self):
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
