import numpy
from numpy import c_
from fob import FobStream

def smooth(x,window_len=10,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

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

def formatData(parsedData):
    """Put data parsed by the parseData function in a nice format.

    Format is column-oriented, and ordered by sensor and axis.

    Dimensions of returned array or as such:
    result[sensor, moment, axis]
    """
    def __formatData(sensorData):
        """Format data for a single sensor.
        """
        xs = [item[0] for item in sensorData]
        ys = [item[1] for item in sensorData]
        zs = [item[2] for item in sensorData]

        return c_[xs, ys, zs]

    return c_[[__formatData(sensorData) for sensorData in parsedData]]
