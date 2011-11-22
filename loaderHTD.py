import struct

class DataHTD:
    def __init__(self, fileName):
        self.data = ""
        self.header = []
        self.packages = []
        self.noPackage = 0
        self.load(fileName)

    def load(self, fileName):
        self.data = file(fileName, "rb").read()
        par = self.__loadHeader()
        return self.__loadBody(par)

    def __loadHeader(self):
        off = 0
        size = struct.unpack("i", self.data[off:off+4])[0]
        off += 4
        # read file name
        self.header = struct.unpack(str(size)+"s", self.data[off:off+size])
        off += size
        size = struct.unpack("i", self.data[off:off+4])[0]
        off += 4
        # read time stamp
        self.header += struct.unpack(str(size)+"s", self.data[off:off+size])
        off += size
        size = struct.unpack("i", self.data[off:off+4])[0]
        off += 4
        #read memo
        self.header += struct.unpack(str(size)+"s", self.data[off:off+size])
        off += size
        #read OUT_ORGX, OUT_ORGY, OUT_EXTX, OUT_EXTY
        for x in xrange(4):
            self.header += struct.unpack("i", self.data[off:off+4])
            off += 4
        self.noPackage = struct.unpack("i", self.data[off:off+4])[0]
        off += 4
        return off

    def __loadBody(self, param):
        off = param
        self.packages = []
        #read packages
        for x in xrange(self.noPackage):
            self.packages += (struct.unpack("6i", self.data[off:off+6*4]),)
            off += 6*4
#        noLabels = struct.unpack("i", self.data[off:off+4])
