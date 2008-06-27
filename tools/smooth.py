import sys, os
sys.path.append(os.path.dirname(__file__))

from optparse import OptionParser
from fob import FobStream
from numpy import array, c_
from utils import smooth, formatData, readData, writeData

def main(argv=None):
    if argv == None:
        argv = sys.argv

    usage = "usage: %prog [options] inputfile num_sensors outputfile"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()
    (infile, numSensors, outfile) = args
    numSensors = int(numSensors)

    # Read in sensor data
    sensorData = readData(infile, numSensors)

    # Get it into a nice linear algebra form
    data = formatData(sensorData)

    # Smooth 'em all
    for sensorData in data:
        for vec in sensorData.T:
            vec[:] = smooth(vec)

    # Write it out in the standard FoB format
    writeData(outfile, data)

if __name__ == "__main__":
    sys.exit(main())
