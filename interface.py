from Tkinter import Tk, Canvas, LEFT, RIGHT, BOTH, X, ALL, DISABLED, NORMAL
from ttk import Frame, Button, Style, Combobox, Label, Labelframe, Entry
from settings import * #@UnusedWildImport
from localization import * #@UnusedWildImport
from loaderHTD import DataHTD
import tkFileDialog
import tkMessageBox
from colors import HSVGradientGenerator
from math import sqrt

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
        self.colorsTableMinLabel = Label(self.colorsSettingsPanel, text=colorsTableMinLabelText)
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
            if (not self.__getInputData()):
                self.__showInvalidInputMessage()
                return
            
            htd = DataHTD(fileName)
            self.__draw(htd.packages)
            
            self.redrawButton.config(state=NORMAL)
            self.colorByCombobox.config(state="readonly")
            self.colorsTableLengthEntry.config(state=NORMAL)
            self.scaleTypeCombobox.config(state="readonly")
            
    def redrawButtonClick(self):
        if (not self.__getInputData()):
            self.__showInvalidInputMessage()
            return
        
        self.__draw(self.lastPackages)

    def scaleTypeComboboxChange(self, event):
        if (self.scaleTypeCombobox.get() == relativeScaleType):
            self.colorsTableMinEntry.config(state=DISABLED)
            self.colorsTableMaxEntry.config(state=DISABLED)
        else:
            self.colorsTableMinEntry.config(state=NORMAL)
            self.colorsTableMaxEntry.config(state=NORMAL)
        
    def __draw(self, dataPackages):
        self.lastPackages = dataPackages
        self.imageCanvas.delete(ALL)

        hsv = HSVGradientGenerator(self.colorsTableLength)
        minX = self.__getMinimum(dataPackages, dataXNumber)
        minY = self.__getMinimum(dataPackages, dataYNumber)
        maxX = self.__getMaximum(dataPackages, dataXNumber)
        maxY = self.__getMaximum(dataPackages, dataYNumber)
        ratio = self.__getRatio(minX, minY, maxX, maxY)
            
        colorBy = self.colorByCombobox.get()
        if (colorBy == colorByNoneOption):
            self.__drawColorByNone(dataPackages, minX, minY, ratio)
            return
        if (colorBy == colorBySpeedOption):
            self.__drawColorBySpeed(dataPackages, minX, minY, ratio, hsv)
            return
            
        colorByNumber = colorByValuesDictionary[colorBy]
        
        if (self.scaleTypeCombobox.get() == relativeScaleType):
            colorsTableMinValue = float(self.__getMinimum(dataPackages, colorByNumber))
            colorsTableMaxValue = float(self.__getMaximum(dataPackages, colorByNumber))
        else:
            colorsTableMinValue = self.colorsTableMinValue
            colorsTableMaxValue = self.colorsTableMaxValue
            
        for package in dataPackages:
            x = (package[dataXNumber] - minX) * ratio
            y = (package[dataYNumber] - minY) * ratio
            
            color = hsv.getColorByValue(colorsTableMinValue,
                                        colorsTableMaxValue,
                                        package[colorByNumber])
                
            tk_rgb = "#%02x%02x%02x" % color
            self.imageCanvas.create_line(x, y, x + 1, y + 1, fill=tk_rgb)

    def __drawColorByNone(self, dataPackages, minX, minY, ratio):
        for package in dataPackages:
            x = (package[dataXNumber] - minX) * ratio
            y = (package[dataYNumber] - minY) * ratio
            
            self.imageCanvas.create_line(x, y, x + 1, y + 1, fill=defaultDrawingColor)
            
    def __drawColorBySpeed(self, dataPackages, minX, minY, ratio, hsv):   
        allSpeeds = self.__getAllSpeed(dataPackages)
        minSpeed = min(allSpeeds)
        maxSpeed = max(allSpeeds)
        
        if (self.scaleTypeCombobox.get() == relativeScaleType):
            colorsTableMinValue = minSpeed
            colorsTableMaxValue = maxSpeed
        else:
            colorsTableMinValue = self.colorsTableMinValue
            colorsTableMaxValue = self.colorsTableMaxValue
        
        i = 0
        for package in dataPackages:
            x = (package[dataXNumber] - minX) * ratio
            y = (package[dataYNumber] - minY) * ratio
            
            color = hsv.getColorByValue(colorsTableMinValue,
                                        colorsTableMaxValue,
                                        allSpeeds[i])
                
            tk_rgb = "#%02x%02x%02x" % color
            self.imageCanvas.create_line(x, y, x + 1, y + 1, fill=tk_rgb)
            i += 1
        
    def __getAllSpeed(self, dataPackages):
        allSpeeds = []
        
        lastPackage = None
        for package in dataPackages:
            if (not lastPackage):
                speed = 0
            else:
                currTime = package[dataTimeNumber]
                currX = package[dataXNumber]
                currY = package[dataYNumber]
                lastTime = lastPackage[dataTimeNumber]
                lastX = lastPackage[dataXNumber]
                lastY = lastPackage[dataYNumber]
                dx = self.__getDistance(lastX, lastY, currX, currY)
                dt = currTime - lastTime
                if (dt == 0):
                    speed = 0
                else:
                    speed = dx / dt
                
            lastPackage = package
            allSpeeds.append(speed)
        return allSpeeds
        
    def __getDistance(self, firstX, firstY, secondX, secondY):
        xx = secondX - firstX
        yy = secondY - firstX
        return sqrt(pow(xx, 2) + pow(yy, 2))

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
    
    def __showInvalidInputMessage(self):
        tkMessageBox.showinfo(invalidInputMessageTitle, invalidInputMessageText)
    
    def __getInputData(self):
        try:
            self.colorsTableLength = int(self.colorsTableLengthEntry.get())
            self.colorsTableMinValue = float(self.colorsTableMinEntry.get())
            self.colorsTableMaxValue = float(self.colorsTableMaxEntry.get())
        
            if (self.colorsTableLength < 1 or
                self.colorsTableMinValue >= self.colorsTableMaxValue):
                raise
            return True
        except:
            return False
