class FobStream(object):

    def __init__(self, filePath, numSensors):
        self.filePath = filePath
        self.f = open(filePath, 'r')
        self.numSensors = numSensors

    def __lines(self, num):
        result = []
        for i in range(num):
            result.append(self.f.readline())
        return result

    def __iter__(self):
        return self

    def next(self):
        lines = self.__lines(self.numSensors)
        if len(lines[0]) == 0:
            self.f.close()
            raise StopIteration
        return lines


        
