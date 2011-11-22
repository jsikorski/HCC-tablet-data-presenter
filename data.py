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
                          colorsTableMaxValue, rejectedValuesPercent):        
        loader = DataHTD(fileName)
        touchedPackages = self.__getPackagesWithoutNotTouchedPoints(loader.packages)
        
        if (colorBy == colorByNoneOption):
            return self.__getDataForColoringByNone(touchedPackages)
        
        self.__hsv = HSVGradientGenerator(colorsTableLength)
        self.__colorsTableMinValue = colorsTableMinValue
        self.__colorsTableMaxValue = colorsTableMaxValue
        
        if (colorBy == colorBySpeedOption):
            return self.__getDataForColoringBySpeed(touchedPackages, scaleType,
                                                    rejectedValuesPercent)
        
        return self.__getDataForColoringByDictValue(touchedPackages, scaleType,
                                                    colorBy, rejectedValuesPercent)
    
    def __getPackagesWithoutNotTouchedPoints(self, packages):
        return filter(lambda x: x[dataPressureNumber] > 0, packages)
    
    def __getDataForColoringByNone(self, packages):
        colorsList = self.__getColorsListForColoringByNone(len(packages))
        return self.__getDrawingData(packages, colorsList)
    
    def __getColorsListForColoringByNone(self, length):
        return [(0, 0, 0) for i in range(0, length)]
    
    def __getDataForColoringBySpeed(self, packages, scaleType, rejectedValuesPercent):
        speeds = self.__getAllSpeeds(packages)
        colorsList = self.__getColorsList(speeds, scaleType, rejectedValuesPercent)
        return self.__getDrawingData(packages, colorsList)
    
    def __getDataForColoringByDictValue(self, packages, scaleType,
                                        colorBy, rejectedValuesPercent):
        colorByNumber = colorByNumbersDictionary[colorBy]
        choosenList = [x[colorByNumber] for x in packages]     
        colorsList = self.__getColorsList(choosenList, scaleType, rejectedValuesPercent)
        return self.__getDrawingData(packages, colorsList)
    
    def __getColorsList(self, valuesList, scaleType, rejectedValuesPercent):
        sortedValuesList = sorted(valuesList)
        rejectedValuesAmount = len(valuesList) * rejectedValuesPercent / 100.0
        minAllowedValue = sortedValuesList[int(rejectedValuesAmount / 2)]
        maxAllowedValue = sortedValuesList[int(len(sortedValuesList) - rejectedValuesAmount / 2) - 1]

        if (scaleType == absoluteScaleType):
            minValue = self.__colorsTableMinValue
            maxValue = self.__colorsTableMaxValue
        else:
            minValue = float(minAllowedValue)
            maxValue = float(maxAllowedValue)
        
        colorsList = []
        for value in valuesList:
            if (value < minAllowedValue):
                colorsList.append((0, 0, 255))
                continue
            if (value > maxAllowedValue):
                colorsList.append((255, 0, 0))
                continue
            colorsList.append(self.__hsv.getColorByValue(minValue, maxValue, value))
        return colorsList
    
    def __getDrawingData(self, packages, colorsList):
        minimalCoordinates = self.__getMinimalCoordinates(packages)
        ratio = self.__getRatio(minimalCoordinates.minX,
                                minimalCoordinates.minY,
                                minimalCoordinates.maxX,
                                minimalCoordinates.maxY)
        drawingData = [];
        for i, package in enumerate(packages):
            drawingX = (package[dataXNumber] - minimalCoordinates.minX) * ratio
            drawingY = (package[dataYNumber] - minimalCoordinates.minY) * ratio
            color = self.__transformRGBToTkColor(colorsList[i])
            drawingData.append((drawingX, drawingY, color))
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
        dataPackages.sort(key=lambda x: x[dataTimeNumber])
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
        yy = secondY - firstY
        return sqrt(pow(xx, 2) + pow(yy, 2))
