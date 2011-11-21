from settings import * #@UnusedWildImport
from math import sqrt; #@UnusedImport
from loaderHTD import DataHTD
from colors import HSVGradientGenerator

class MinimalCoordinates(object):
    __slots__ = ["minX", "minY", "maxX", "maxY"]
    def __init__(self, minX, minY, maxX, maxY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY

class DataController(object):
    def getDataForDrawing(self, fileName, colorBy, colorsTableLength, 
                          scaleType, colorsTableMinValue, 
                          colorsTableMaxValue, rejectedMargin):        
        loader = DataHTD(fileName)
        
        if (colorBy == colorByNoneOption):
            return self.__getDataForColoringByNone(loader.packages)
        
        self.__hsv = HSVGradientGenerator(colorsTableLength)
        self.__colorsTableMinValue = colorsTableMinValue
        self.__colorsTableMaxValue = colorsTableMaxValue
        
        if (colorBy == colorBySpeedOption):
            return self.__getDataForColoringBySpeed(loader.packages, scaleType)
        
        
        
#        self.__hsv = HSVGradientGenerator(colorsTableLength)        
#        self.speeds = self.__getAllSpeeds(loader.packages)
#        
#        self.colorBy = colorBy;
#        if (self.colorBy != colorByNoneOption and
#            self.colorBy != colorBySpeedOption):
#            self.colorByNumber = colorByValuesDictionary[self.colorBy]
#        
#        if (scaleType == absoluteScaleType):
#            self.colorsTableMinValue = colorsTableMinValue
#            self.colorsTableMaxValue = colorsTableMaxValue
#        else:
#            if (self.colorBy == colorBySpeedOption):
#                self.colorsTableMinValue = min(self.speeds)
#                self.colorsTableMaxValue = max(self.speeds)
#            elif (self.colorBy != colorByNoneOption):
#                self.colorsTableMinValue = float(self.__getMinimum(loader.packages, self.colorByNumber))
#                self.colorsTableMaxValue = float(self.__getMaximum(loader.packages, self.colorByNumber))
#        
#        if (self.colorBy != colorByNoneOption and
#            self.colorBy != colorBySpeedOption):
#            loader.packages = self.__filterData(loader.packages, 
#                              self.colorsTableMinValue, 
#                              self.colorsTableMaxValue, 
#                              rejectedMargin)
#            self.colorsTableMinValue = float(self.__getMinimum(loader.packages, self.colorByNumber))
#            self.colorsTableMaxValue = float(self.__getMaximum(loader.packages, self.colorByNumber))
#            
#        minX = maxint;
#        minY = maxint;
#        maxX = minint;
#        maxY = minint;
#        for package in loader.packages:
#            currX = package[dataXNumber]
#            currY = package[dataYNumber]
#            if (currX < minX):
#                minX = currX
#            if (currX > maxX):
#                maxX = currX
#            if (currY < minY):
#                minY = currY
#            if (currY > maxY):
#                maxY = currY
#        
#        ratio = self.__getRatio(minX, minY, maxX, maxY)
#        return self.__getDrawingData(loader.packages, minX, minY, ratio)
    
    def __getDataForColoringByNone(self, packages):
        colorsList = self.__getColorsListForColoringByNone(len(packages))
        return self.__getDrawingData(packages, colorsList)
    
    def __getColorsListForColoringByNone(self, length):
        return [(0, 0, 0) for i in range(0, length)]
    
    def __getDataForColoringBySpeed(self, packages, scaleType):
        speeds = self.__getAllSpeeds(packages)
        if (scaleType == absoluteScaleType):
            minValue = self.__colorsTableMinValue
            maxValue = self.__colorsTableMaxValue
        else:
            minValue = min(speeds)
            maxValue = max(speeds)
        
        colorsList = self.__getColorsListForColoringBySpeed(speeds, minValue, maxValue)
        return self.__getDrawingData(packages, colorsList)
    
    def __getColorsListForColoringBySpeed(self, speedsList, minValue, maxValue):
        colorsList = []
        for speed in speedsList:
            colorsList.append(self.__hsv.getColorByValue(minValue, maxValue, speed))
        return colorsList
    
    def __getDrawingData(self, packages, colorsList):
        minimalCoordinates = self.__getMinimalCoordinates(packages)
        ratio = self.__getRatio(minimalCoordinates.minX, 
                                minimalCoordinates.minY, 
                                minimalCoordinates.maxX, 
                                minimalCoordinates.maxY)
        i = 0;
        drawingData = [];
        for package in packages:
            drawingX = (package[dataXNumber] - minimalCoordinates.minX) * ratio
            drawingY = (package[dataYNumber] - minimalCoordinates.minY) * ratio
            color = self.__transformRGBToTkColor(colorsList[i])
            drawingData.append((drawingX, drawingY, color))
            i += 1            
        return drawingData;

    def __getMinimalCoordinates(self, packages):
        minX = maxint;
        minY = maxint;
        maxX = minint;
        maxY = minint;
        for package in packages:
            currX = package[dataXNumber]
            currY = package[dataYNumber]
            if (currX < minX):
                minX = currX
            if (currX > maxX):
                maxX = currX
            if (currY < minY):
                minY = currY
            if (currY > maxY):
                maxY = currY
        return MinimalCoordinates(minX, minY, maxX, maxY)

    #TODO
    
    def __getDrawingColor(self, package, packageIndex):
        if (self.colorBy == colorByNoneOption):
            color = (0, 0, 0)
        else:
            if (self.colorBy == colorBySpeedOption):
                speed = self.speeds[packageIndex]
                color = self.__hsv.getColorByValue(self.colorsTableMinValue, 
                                                 self.colorsTableMaxValue, 
                                                 speed)
            else:
                color = self.__hsv.getColorByValue(self.colorsTableMinValue, 
                                                 self.colorsTableMaxValue, 
                                                 package[self.colorByNumber])
        return self.__transformRGBToTkColor(color)
    
    def __transformRGBToTkColor(self, color):
        return "#%02x%02x%02x" % color
        
    def __getAllSpeeds(self, dataPackages):
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
    
    def __getMinimum(self, dataPackages, valueNumber):
        return min(dataPackages, key=lambda x: x[valueNumber])[valueNumber]
            
    def __getMaximum(self, dataPackages, valueNumber):
        return max(dataPackages, key=lambda x: x[valueNumber])[valueNumber]

    def __getRatio(self, minX, minY, maxX, maxY):
        xLength = maxX - minX
        yLength = maxY - minY
        
        if (xLength > yLength):
            return float(imageCanvasWidth) / xLength
        else:
            return float(windowElementsHeight) / yLength
        
    def __getDistance(self, firstX, firstY, secondX, secondY):
        xx = secondX - firstX
        yy = secondY - firstX
        return sqrt(pow(xx, 2) + pow(yy, 2))
    
    def __filterData(self, packages, minimum, maximum, rejectedMargin):
        minimumValue = minimum + maximum * rejectedMargin / 100.0
        maximumValue = maximum - maximum * rejectedMargin / 100.0
        filteredData = filter(lambda x: x[self.colorByNumber] >= minimumValue and 
                                        x[self.colorByNumber] <= maximumValue, packages)
        return filteredData