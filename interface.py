from Tkinter import Tk, Canvas, LEFT, RIGHT, BOTH, X, ALL, StringVar
from ttk import Frame, Button, Style, OptionMenu, Combobox
from settings import *
from loaderHTD import DataHTD
import tkFileDialog
from Tkconstants import DISABLED, NORMAL

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(mainWindowTitle)
        self.resizable(width=0, height=0)
        self.__setStyles()
        self.__initializeComponents()
        self.mainloop()
            
    def __initializeComponents(self):
        self.imageCanvas = Canvas(master=self, width=imageCanvasWidth,
                                  height=windowElementsHeight, bg="white")
        self.imageCanvas.pack(side=LEFT, padx=(windowPadding, 0),
                              pady=windowPadding, fill=BOTH)
        
        self.buttonsFrame = Frame(master=self, width=buttonsFrameWidth, 
                                  height=windowElementsHeight)
        self.buttonsFrame.propagate(0)
        self.loadFileButton = Button(master=self.buttonsFrame,
                                     text=loadFileButtonText, command=self.loadFileButtonClick)
        self.loadFileButton.pack(fill=X, pady=buttonsPadding);
        self.redrawButton = Button(master=self.buttonsFrame, text=redrawButtonText, 
                                   state=DISABLED, command=self.redrawButtonClick)
        self.redrawButton.pack(fill=X, pady=buttonsPadding)
        self.optionsComboBox = Combobox(self.buttonsFrame, values = ["a", "b", "c"])
        self.optionsComboBox.pack(fill=X, pady=buttonsPadding)
        self.buttonsFrame.pack(side=RIGHT, padx=windowPadding, pady=windowPadding, fill=BOTH)
        
    def __setStyles(self):
        Style().configure("TButton", padding=buttonsTextPadding, font=buttonsFont)
    
    def loadFileButtonClick(self):
        fileName = tkFileDialog.askopenfilename(filetypes=[('HTD files', '*.htd')])
        if (fileName):
            htd = DataHTD(fileName)
            self.draw(htd.packages)
            self.redrawButton.config(state = NORMAL)
        
    def redrawButtonClick(self):
        print "Redraw!"
        
    def draw(self, dataPackages):
        self.lastPackages = dataPackages
        self.imageCanvas.delete(ALL)

        minX = self.__getMinimum(dataPackages, dataXNumber)
        minY = self.__getMinimum(dataPackages, dataYNumber)
        maxX = self.__getMaximum(dataPackages, dataXNumber)
        maxY = self.__getMaximum(dataPackages, dataYNumber)
        ratio = self.__getRatio(minX, minY, maxX, maxY)
                
        for package in dataPackages:
            x = (package[dataXNumber] - minX) * ratio
            y = (package[dataYNumber] - minY) * ratio
            self.imageCanvas.create_rectangle(x, y, x, y)

    def redraw(self):
        self.draw(self.lastPackages)

    def __getRatio(self, minX, minY, maxX, maxY):
        xLength = maxX - minX
        yLength = maxY - minY
        
        if (xLength > yLength):
            return float(imageCanvasWidth) / xLength
        else:
            return float(windowElementsHeight) / yLength

    def __getMinimum(self, dataPackages, valueNumber):
        return min(dataPackages, key=lambda x: x[valueNumber])[valueNumber]
            
    def __getMaximum(self, dataPackages, valueNumber):
        return max(dataPackages, key=lambda x: x[valueNumber])[valueNumber]
    