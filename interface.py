from Tkinter import Tk, Canvas, LEFT, RIGHT, BOTH, X
from ttk import Frame, Button, Style
from settings import *
import tkFileDialog
from loaderHTD import DataHTD

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.__setStyles()
        self.title(mainWindowTitle)
        self.resizable(width=0, height=0)
        self.configure(bg=backgroundColor)        
        self.__initializeComponents()
        self.mainloop()
            
    def __initializeComponents(self):
        self.imageCanvas = ImageCanvas(master=self)
        self.imageCanvas.pack(side=LEFT, padx=(windowPadding, 0), 
                              pady=windowPadding, fill=BOTH)
        
        buttonsFrame = ButtonsFrame(master=self)
        buttonsFrame.pack(side=RIGHT, padx=windowPadding, 
                          pady=windowPadding, fill=BOTH)
        
    def __setStyles(self):
        Style().configure("TButton", padding=buttonsTextPadding, font=buttonsFont)
        Style().configure("TFrame", background=backgroundColor)


class ImageCanvas(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master, width=imageCanvasWidth, 
                        height=windowElementsHeight)
        
    def draw(self, dataPackages):
        ratio = self.__getRatio(dataPackages)
        minX = self.__getMinimalValue(dataPackages, dataXNumber)
        minY = self.__getMinimalValue(dataPackages, dataYNumber)
        
        for package in dataPackages:
            x = (package[dataXNumber] - minX) * ratio
            y = (package[dataYNumber] - minY) * ratio
            self.create_rectangle(x, y, x, y)

    def __getRatio(self, dataPackages):
        minX = self.__getMinimalValue(dataPackages, dataXNumber)
        maxX = self.__getMaximalValue(dataPackages, dataXNumber)
        
        minY = self.__getMinimalValue(dataPackages, dataYNumber)
        maxY = self.__getMaximalValue(dataPackages, dataYNumber)
        
        xLength = maxX - minX
        yLength = maxY - minY
        
        if (xLength > yLength):
            return float(imageCanvasWidth) / xLength
        else:
            return float(windowElementsHeight) / yLength

    def __getMinimalValue(self, dataPackages, valueNumber):
        return min(dataPackages, key=lambda x: x[valueNumber])[valueNumber]
            
    def __getMaximalValue(self, dataPackages, valueNumber):
        return max(dataPackages, key=lambda x: x[valueNumber])[valueNumber]
        

class ButtonsFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=buttonsFrameWidth, 
                       height=windowElementsHeight)
        self.__initializeComponents()
        
    def __initializeComponents(self):
        self.propagate(0)
        loadFileButton = LoadFileButton(master=self)
        loadFileButton.pack(fill=X, pady = buttonsPadding);


class LoadFileButton(Button):  
    def onClick(self):
        fileName = tkFileDialog.askopenfilename(filetypes=[('HTD files', '*.htd')])
        if (fileName):
            htd = DataHTD(fileName)
            self.master.master.imageCanvas.draw(htd.packages)
      
    def __init__(self, master):
        Button.__init__(self, master, text=loadFileButtonText, 
                        command = self.onClick)        
