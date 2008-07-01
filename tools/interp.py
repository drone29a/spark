import sys, os
sys.path.append(os.path.dirname(__file__))

from optparse import OptionParser
from fob import FobStream
from numpy import array, c_, arange, zeros
from scipy.interpolate.interpolate import interp1d
from utils import formatData, readData, writeData

def main(argv=None):
    if argv == None:
        argv = sys.argv

    usage = "usage: %prog [options] inputfile num_sensors inputfreq outputfreq outputfile"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()
    (infile, num_sensors, infreq, outfreq, outfile) = args
    num_sensors = int(num_sensors)
    infreq = float(infreq)
    outfreq = float(outfreq)

    # Read data
    sensor_data = readData(infile, num_sensors)

    # Get it in numpy arrays
    data = formatData(sensor_data)

    # Get new interpolated values
    num_moments = data[0,:,0].size
    duration = num_moments/infreq
    in_xs = arange(0, duration, 1/infreq)
    out_xs = arange(0, duration, 1/outfreq) 
    # If out_xs goes out of bounds due to rounding, chop the end off
    while out_xs[-1] > in_xs[-1]:
        out_xs = out_xs[:-1]

    interp_data = zeros((num_sensors, out_xs.size, 3))
    for i in xrange(num_sensors):
        for j in xrange(data[0,0].size):
            interp = interp1d(in_xs, data[i].T[j], 'linear')
            interp_data[i].T[j] = interp(out_xs)

    # Write out interpolated values
    writeData(outfile, interp_data)
    
if __name__ == "__main__":
    sys.exit(main())
