from localization import colorBySpeedOption, colorByAzimuthOption, colorByAltitudeOption, \
    colorByPressureOption, colorByNoneOption, relativeScaleType,\
    absoluteScaleType
import sys

windowPadding = 20
buttonsTextPadding = (5, 5, 5, 5)
buttonsFont = "serif 10"
windowElementsHeight = 600
imageCanvasWidth = 600
buttonsFrameWidth = 200
loadFileButtonText = "Load file"
buttonsPadding = (0, 15)
dataTimeNumber = 0
dataXNumber = 1
dataYNumber = 2
colorByComboboxValues = [colorByNoneOption,
                         colorBySpeedOption,
                         colorByPressureOption,
                         colorByAzimuthOption,
                         colorByAltitudeOption]
colorByNumbersDictionary = {colorByPressureOption: 3,
                           colorByAzimuthOption: 4,
                           colorByAltitudeOption: 5}
defaultColorsTableLength = 50
defaultColorsTableMin = 0
defaultColorsTableMax = 100
scaleTypesComboboxValues = [relativeScaleType, 
                            absoluteScaleType]
defaultDrawingColor = "black"
defaultRejectedMarginValue = 5
maxint = sys.maxint;
minint = -sys.maxint - 1;