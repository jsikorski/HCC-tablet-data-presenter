from Tkinter import Tk, Canvas, LEFT, RIGHT, BOTH, X, ALL, DISABLED, NORMAL
from ttk import Frame, Button, Style, Combobox, Label, Labelframe, Entry
from settings import * #@UnusedWildImport
from localization import * #@UnusedWildImport
import tkFileDialog
import tkMessageBox
from data import DataController

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(mainWindowTitle)
        self.resizable(width=0, height=0)
        self.__setStyles()
        self.__initializeComponents()
        self.__dataController = DataController();
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
        self.colorByCombobox.bind("<<ComboboxSelected>>", self.colorByComboboxChange)
        self.colorByCombobox.pack(fill=X, pady=buttonsPadding)
        self.rejectedValuesPercentLabel = Label(self.buttonsFrame, text=rejectedMarginLabelText)
        self.rejectedValuesPercentLabel.pack(fill=X)
        self.rejectedValuesPercentEntry = Entry(self.buttonsFrame)
        self.rejectedValuesPercentEntry.insert(0, defaultRejectedValuesPercent)
        self.rejectedValuesPercentEntry.config(state=DISABLED)
        self.rejectedValuesPercentEntry.pack(fill=X, pady=buttonsPadding)        
        
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
            if (not self.__getInputParams()):
                self.__showInvalidInputMessage()
                return
            
            self.lastFileName = fileName;
            self.__draw(fileName)
            
            self.redrawButton.config(state=NORMAL)
            self.colorByCombobox.config(state="readonly")
            self.colorsTableLengthEntry.config(state=NORMAL)
            self.scaleTypeCombobox.config(state="readonly")
            
    def redrawButtonClick(self):
        if (not self.__getInputParams()):
            self.__showInvalidInputMessage()
            return
        
        self.__draw(self.lastFileName)

    def scaleTypeComboboxChange(self, event):
        if (self.scaleTypeCombobox.get() == relativeScaleType):
            self.colorsTableMinEntry.config(state=DISABLED)
            self.colorsTableMaxEntry.config(state=DISABLED)
        else:
            self.colorsTableMinEntry.config(state=NORMAL)
            self.colorsTableMaxEntry.config(state=NORMAL)
        
    def colorByComboboxChange(self, event):
        if (self.colorByCombobox.get() == colorByNoneOption):
            self.rejectedValuesPercentEntry.config(state=DISABLED)
        else:
            self.rejectedValuesPercentEntry.config(state=NORMAL)
        
    def __draw(self, fileName):
        self.imageCanvas.delete(ALL)

        dataForDrawing = self.__dataController.getDataForDrawing(
            fileName, self.colorByCombobox.get(), self.colorsTableLength,
            self.scaleTypeCombobox.get(), self.colorsTableMinValue,
            self.colorsTableMaxValue, self.rejectedValuesPercent)
        
        for package in dataForDrawing:
            x = package[0];
            y = package[1];
            color = package[2];
            self.imageCanvas.create_line(x, y, x + 1, y + 1, fill=color)
            
    def __drawColorBySpeed(self, dataPackages, minX, minY, ratio, hsv):   
        allSpeeds = self.__getAllSpeeds(dataPackages)
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
            
    def __showInvalidInputMessage(self):
        tkMessageBox.showinfo(invalidInputMessageTitle, invalidInputMessageText)
    
    def __getInputParams(self):
        try:
            self.colorsTableLength = int(self.colorsTableLengthEntry.get())
            self.colorsTableMinValue = float(self.colorsTableMinEntry.get())
            self.colorsTableMaxValue = float(self.colorsTableMaxEntry.get())
            self.rejectedValuesPercent = float(self.rejectedValuesPercentEntry.get())
        
            if (self.colorsTableLength < 1 or
                self.colorsTableMinValue >= self.colorsTableMaxValue or
                self.rejectedValuesPercent < 0 or self.rejectedValuesPercent >= 100):
                raise
            return True
        except:
            return False
