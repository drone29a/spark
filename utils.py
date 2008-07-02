from fob import FobStream

def writer(data):
    numSensors = data.ndim
    numMoments = data[0,:,0].size

    for i in xrange(numMoments):
        for j in xrange(numSensors):
            yield "%s %s %s %s\n" % tuple([j+1] + data[j,i].tolist())

def writeData(outfile, data):
    out = open(outfile, 'w')
    out.writelines(writer(data))

    out.close()

def readData(infile, numSensors):
    """Parse out the x, y, z signals for each sensor.

    Returns a list of signal tuples, grouped by sensor.

    Example:

    [[(x1,y1,z1),(x2,y2,z2)...],  # sensor 1
    [(x1,y1,z1),(x2,y2,z2)...],   # sensor 2
    ...]                          # sensor n
    """
    fs = FobStream(infile, numSensors)

    sensorDataLines = [[] for i in range(numSensors)]
    for momentData in fs:
        for i in range(numSensors):
            sensorDataLines[i].append(momentData[i])

    def __readData(lines):
        """Parse lines containing data for a single sensor.
        """
        return [tuple([float(val) for val in line.split()[1:4]]) for line in lines]
            
    return [__readData(lines) for lines in sensorDataLines]        
