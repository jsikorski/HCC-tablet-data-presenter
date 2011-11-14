from math import floor

class HSVGradientGenerator(object):
    def __init__(self, listLength):
        self.listLength = listLength
        self.colorsList = []
        self.__initColorsByHSV()
           
    def getColorByValue(self, minValue, maxValue, value):
        if (value > maxValue):
            return (0, 0, 0)
        if (value < minValue):
            return (255, 255, 255)
        
        a = (self.listLength - 1) / (maxValue - minValue)
        b = -a * minValue
        index = int(floor(a * value + b))
        
        return self.colorsList[index]

    def __initColorsByHSV(self):
        step = 240.0 / self.listLength
        
        hue = 0.0
        saturation = 1.0
        value = 1.0
        
        i = self.listLength - 1
        while (i >= 0):
            color = self.__getRGBFromHSV(hue, saturation, value)
            self.colorsList.insert(0, color)
            hue += step
            i -= 1
            
    def __getRGBFromHSV(self, hue, saturation, value):
        hi = int(floor(hue / 60.0)) % 6
        f = hue / 60.0 - floor(hue / 60.0)
        
        value *= 255.0
        v = int(value)
        p = int(value * (1.0 - saturation))
        q = int(value * (1.0 - f * saturation))
        t = int(value * (1.0 - (1.0 - f) * saturation))
        
        if (hi == 0):
            return (v, t, p)
        if (hi == 1):
            return (q, v, p)
        if (hi == 2):
            return (p, v, t)
        if (hi == 3):
            return (p, q, v)
        if(hi == 4):
            return (t, p, v)
        
        return (v, p, q)
