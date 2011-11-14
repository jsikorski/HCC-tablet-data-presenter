from Tkinter import Tk, Canvas, LEFT, RIGHT, BOTH, X, ALL, Spinbox
from ttk import Frame, Button, Style, Combobox, Label, Labelframe, Checkbutton,\
    Entry
from settings import *
from localization import *
from loaderHTD import DataHTD
import tkFileDialog
from Tkconstants import DISABLED, NORMAL
from colors import HSVGradientGenerator

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.hsv = HSVGradientGenerator(50)
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
        self.colorByLabel = Label(self.buttonsFrame, text=colorByLabelText)
        self.colorByLabel.pack(fill=X)
        self.colorByComboBox = Combobox(self.buttonsFrame, state=DISABLED,
                                        values=colorByComboBoxValues)
        self.colorByComboBox.set(colorByComboBoxValues[0])
        self.colorByComboBox.pack(fill=X, pady=buttonsPadding)
        self.colorsSettingsPanel = Labelframe(self.buttonsFrame, text=visualisationSettingsPanelText)
        self.colorsTableLengthLabel = Label(self.colorsSettingsPanel, text = colorsTableLengthLabelText)
        self.colorsTableLengthLabel.pack(fill=X)
        self.colorsTableLengthEntry = Entry(self.colorsSettingsPanel, state = DISABLED)
        self.colorsTableLengthEntry.pack(fill=X)
        self.colorsSettingsPanel.pack(fill=X, pady=buttonsPadding)
        self.redrawButton = Button(master=self.buttonsFrame, text=redrawButtonText,
                                   state=DISABLED, command=self.redrawButtonClick)
        self.redrawButton.pack(fill=X, pady=buttonsPadding)
        self.buttonsFrame.pack(side=RIGHT, padx=windowPadding, pady=windowPadding, fill=BOTH)
        
    def __setStyles(self):
        Style().configure("TButton", padding=buttonsTextPadding, font=buttonsFont)
    
    def loadFileButtonClick(self):
        fileName = tkFileDialog.askopenfilename(filetypes=[('HTD files', '*.htd')])
        if (fileName):
            htd = DataHTD(fileName)
            self.draw(htd.packages)
            self.redrawButton.config(state=NORMAL)
            self.colorByComboBox.config(state="readonly")
            self.colorsTableLengthEntry.config(state=NORMAL)
        
    def redrawButtonClick(self):
        self.draw(self.lastPackages)
        
    def draw(self, dataPackages):
        self.lastPackages = dataPackages
        self.imageCanvas.delete(ALL)

        minX = self.__getMinimum(dataPackages, dataXNumber)
        minY = self.__getMinimum(dataPackages, dataYNumber)
        maxX = self.__getMaximum(dataPackages, dataXNumber)
        maxY = self.__getMaximum(dataPackages, dataYNumber)
        ratio = self.__getRatio(minX, minY, maxX, maxY)
            
        colorBy = self.colorByComboBox.get()
        if (colorBy != colorByNoneOption):
            colorByNumber = colorByValuesDictionary[colorBy]
            a = float(self.__getMinimum(dataPackages, colorByNumber))
            b = float(self.__getMaximum(dataPackages, colorByNumber))
                
        for package in dataPackages:
            x = (package[dataXNumber] - minX) * ratio
            y = (package[dataYNumber] - minY) * ratio
            
            if (colorBy != colorByNoneOption):
                color = self.hsv.getColorByValue(a, b, package[colorByNumber])
            else:
                color = (0, 0, 0)
                
            tk_rgb = "#%02x%02x%02x" % color
            self.imageCanvas.create_line(x, y, x + 1, y + 1, fill=tk_rgb)

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
    
