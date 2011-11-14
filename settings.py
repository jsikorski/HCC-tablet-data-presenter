from localization import colorByTimeOption, colorByAzimuthOption, colorByAltitudeOption, \
    colorByPressureOption, colorByNoneOption

windowPadding = 20
buttonsTextPadding = (5, 5, 5, 5)
buttonsFont = "serif 10"
windowElementsHeight = 600
imageCanvasWidth = 600
buttonsFrameWidth = 200
loadFileButtonText = "Load file"
buttonsPadding = (0, 15)
dataXNumber = 1
dataYNumber = 2
colorByComboBoxValues = [colorByNoneOption,
                         colorByTimeOption,
                         colorByPressureOption,
                         colorByAzimuthOption,
                         colorByAltitudeOption]

colorByValuesDictionary = {colorByTimeOption: 0,
                           colorByPressureOption: 3,
                           colorByAzimuthOption: 4,
                           colorByAltitudeOption: 5}
