from Tkinter import Tk, Canvas, LEFT, RIGHT, BOTH, X, ALL, DISABLED, NORMAL
from ttk import Frame, Button, Style, Combobox, Label, Labelframe, Entry
from settings import * #@UnusedWildImport
from localization import * #@UnusedWildImport
from loaderHTD import DataHTD
import tkFileDialog
import tkMessageBox
from colors import HSVGradientGenerator

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
        
        self.colorByLabel = Label(self.buttonsFrame, text=colorByLabelText)
        self.colorByLabel.pack(fill=X)
        self.colorByCombobox = Combobox(self.buttonsFrame, state=DISABLED,
                                        values=colorByComboboxValues)
        self.colorByCombobox.set(colorByComboboxValues[0])
        self.colorByCombobox.pack(fill=X, pady=buttonsPadding)
        
        self.colorsSettingsPanel = Labelframe(self.buttonsFrame, text=visualisationSettingsPanelText)
        self.colorsTableLengthLabel = Label(self.colorsSettingsPanel, text=colorsTableLengthLabelText)
        self.colorsTableLengthLabel.pack(fill=X)
        self.colorsTableLengthEntry = Entry(self.colorsSettingsPanel)
        self.colorsTableLengthEntry.insert(0, defaultColorsTableLength)
        self.colorsTableLengthEntry.config(state=DISABLED)
        self.colorsTableLengthEntry.pack(fill=X)
        self.scaleTypeLabel = Label(self.colorsSettingsPanel, text=scaleTypeLabelText)
        self.scaleTypeLabel.pack(fill=X)
        self.scaleTypeCombobox = Combobox(self.colorsSettingsPanel, state=DISABLED,
                                          values=scaleTypesComboboxValues)
        self.scaleTypeCombobox.set(scaleTypesComboboxValues[0])
        self.scaleTypeCombobox.bind("<<ComboboxSelected>>", self.scaleTypeComboboxChange)
        self.scaleTypeCombobox.pack(fill=X)
        self.colorsTableMinLabel = Label(self.colorsSettingsPanel, text=colorsTableMaxLabelText)
        self.colorsTableMinLabel.pack(fill=X)
        self.colorsTableMinEntry = Entry(self.colorsSettingsPanel)
        self.colorsTableMinEntry.insert(0, defaultColorsTableMin)
        self.colorsTableMinEntry.config(state=DISABLED)
        self.colorsTableMinEntry.pack(fill=X)
        self.colorsTableMaxLabel = Label(self.colorsSettingsPanel, text=colorsTableMaxLabelText)
        self.colorsTableMaxLabel.pack(fill=X)
        self.colorsTableMaxEntry = Entry(self.colorsSettingsPanel)
        self.colorsTableMaxEntry.insert(0, defaultColorsTableMax)
        self.colorsTableMaxEntry.config(state=DISABLED)
        self.colorsTableMaxEntry.pack(fill=X)
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
            self.colorByCombobox.config(state="readonly")
            self.colorsTableLengthEntry.config(state=NORMAL)
            self.scaleTypeCombobox.config(state="readonly")
            
    def redrawButtonClick(self):
        self.draw(self.lastPackages)

    def scaleTypeComboboxChange(self, event):
        if (self.scaleTypeCombobox.get() == relativeScaleType):
            self.colorsTableMinEntry.config(state=DISABLED)
            self.colorsTableMaxEntry.config(state=DISABLED)
        else:
            self.colorsTableMinEntry.config(state=NORMAL)
            self.colorsTableMaxEntry.config(state=NORMAL)
        
    def draw(self, dataPackages):
        self.lastPackages = dataPackages
        self.imageCanvas.delete(ALL)

        try:
            colorsTableLength = int(self.colorsTableLengthEntry.get())
        except:
            tkMessageBox.showinfo(errorMessageTitle, errorMessageText)
            return

        hsv = HSVGradientGenerator(colorsTableLength)
        minX = self.__getMinimum(dataPackages, dataXNumber)
        minY = self.__getMinimum(dataPackages, dataYNumber)
        maxX = self.__getMaximum(dataPackages, dataXNumber)
        maxY = self.__getMaximum(dataPackages, dataYNumber)
        ratio = self.__getRatio(minX, minY, maxX, maxY)
            
        colorBy = self.colorByCombobox.get()
        if (colorBy != colorByNoneOption):
            colorByNumber = colorByValuesDictionary[colorBy]
            a = float(self.__getMinimum(dataPackages, colorByNumber))
            b = float(self.__getMaximum(dataPackages, colorByNumber))
                
        for package in dataPackages:
            x = (package[dataXNumber] - minX) * ratio
            y = (package[dataYNumber] - minY) * ratio
            
            if (colorBy != colorByNoneOption):
                color = hsv.getColorByValue(a, b, package[colorByNumber])
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
    