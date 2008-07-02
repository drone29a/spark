import sys, os
from optparse import OptionParser
from sparklemotion.fob import FobStream
from numpy import array, c_
import sparklemotion.utils as utils
import sparklemotion.tools.utils as tools_utils

def main(argv=None):
    if argv == None:
        argv = sys.argv

    usage = "usage: %prog [options] inputfile num_sensors outputfile"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()
    (infile, numSensors, outfile) = args
    numSensors = int(numSensors)

    # Read in sensor data
    sensorData = utils.readData(infile, numSensors)

    # Get it into a nice linear algebra form
    data = tools_utils.formatData(sensorData)

    # Smooth 'em all
    for sensorData in data:
        for vec in sensorData.T:
            vec[:] = tools_utils.smooth(vec)

    # Write it out in the standard FoB format
    utils.writeData(outfile, data)

if __name__ == "__main__":
    sys.exit(main())
