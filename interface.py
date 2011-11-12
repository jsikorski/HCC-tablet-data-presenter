from Tkinter import Tk, Canvas, LEFT, RIGHT, BOTH, X
from ttk import Frame, Button, Style
from settings import *

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
        imageCanvas = ImageCanvas(master=self)
        imageCanvas.pack(side=LEFT, padx=(windowPadding, 0), 
                         pady=windowPadding, fill=BOTH)
        
        buttonsFrame = ButtonsFrame(master=self)
        buttonsFrame.pack(side=RIGHT, padx=windowPadding, 
                          pady=windowPadding, fill=BOTH)
        
    def __setStyles(self):
        Style().configure("TButton", padding=buttonsPadding, font=buttonsFont)
        Style().configure("TFrame", background=backgroundColor)


class ImageCanvas(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master, width=imageCanvasWidth, 
                        height=windowElementsHeight)

class ButtonsFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=buttonsFrameWidth, 
                       height=windowElementsHeight)
        self.__initializeComponents()
        
    def __initializeComponents(self):
        self.propagate(0)
        loadFileButton = Button(master=self, text=loadFileButtonText)
        loadFileButton.pack(fill=X);
