from direct.task import Task

class FobStream(object):

    def __init__(self):
        pass

class FobPointUpdateTask(object):
    """
    Task for updating a position of points from FoB data.
    """
    def __init__(self, filePath, points):
        self.filePath = filePath
        self.f = open(filePath, 'r')
        self.points = points

    def __lines(self, num):
        result = []
        for i in range(num):
            result.append(self.f.readline())
        return result

    def __call__(self, task):
        newPositions = [[float(val) for val in line.split()[1:4]] for line in self.__lines(3)]
        if len(newPositions[0]) is 0:
            self.f.close()
            return Task.done
        
        for i in range(3):
            (x, y, z) = newPositions[i]
            z = -z
            self.points[i].setPos(x, y, z)
            
        return Task.cont

    def reset(self):
        """
        Reset to start of data stream.
        """
        if not self.f.closed():
            self.f.seek(0)
        else:
            self.f = open(self.filePath, 'r')


        
