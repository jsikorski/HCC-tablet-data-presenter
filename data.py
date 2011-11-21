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
        
        return self.__getDataForColoringByDictValue(loader.packages, scaleType, colorBy)
    
    def __getDataForColoringByNone(self, packages):
        colorsList = self.__getColorsListForColoringByNone(len(packages))
        return self.__getDrawingData(packages, colorsList)
    
    def __getColorsListForColoringByNone(self, length):
        return [(0, 0, 0) for i in range(0, length)]
    
    def __getDataForColoringBySpeed(self, packages, scaleType):
        speeds = self.__getAllSpeeds(packages)
        colorsList = self.__getColorsList(speeds, scaleType)
        return self.__getDrawingData(packages, colorsList)
    
    def __getDataForColoringByDictValue(self, packages, scaleType, colorBy):
        colorByNumber = colorByNumbersDictionary[colorBy]
        choosenList = [x[colorByNumber] for x in packages]     
        colorsList = self.__getColorsList(choosenList, scaleType)
        return self.__getDrawingData(packages, colorsList)
    
    def __getColorsList(self, valuesList, scaleType):
        if (scaleType == absoluteScaleType):
            minValue = self.__colorsTableMinValue
            maxValue = self.__colorsTableMaxValue
        else:
            minValue = float(min(valuesList))
            maxValue = float(max(valuesList))
        
        colorsList = []
        for speed in valuesList:
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