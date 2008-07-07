import sys
from optparse import OptionParser
from sparklemotion.utils import readData, writeData
from sparklemotion.tools.utils import formatData

"""
Utility to modify coordinates in FoB data files.
"""

def main(argv=None):
    if argv == None:
        argv = sys.argv
        
    usage = "usage: %prog [options] inputfile num_sensors outputfile"
    parser = OptionParser(usage)
    parser.add_option("-n", "--negate", dest="negate_inds",
                      help="indices of columns to replace with complement value")

    (options, args) = parser.parse_args()
    (infile, numSensors, outfile) = args
    numSensors = int(numSensors)
    negate_inds = [int(x) for x in options.negate_inds.split(',')]

    data = readData(infile, numSensors)
    data = formatData(data)
    
    for i in negate_inds:
        data[:,:,i] = -data[:,:,i]

    writeData(outfile, data)

if __name__ == "__main__":
    sys.exit(main())
