#!/usr/bin/env python

"""Command-line runner

Starts an application for creating a visualization platform for observing arm movement.
	
Usage:
	
Called from command prompt with appropriate arguments.

"""

import optparse, config, sys, os.path

#
# Parse command line arguments
#

op = optparse.OptionParser(prog="run.py",
			   add_help_option=True,
			   description=config.program_description,
			   version=config.vers_desc,
			   usage="%prog [-d:] file",
			   formatter=optparse.IndentedHelpFormatter(),
			   option_class=optparse.Option)

# "Current Working Directory" for Data Files
op.add_option("-d", "--data", action="store", type="string", dest="data_dir", help="Directory of Data Files")

# A verbosity flag
op.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Show Verbose Output")

# Set defaults
op.set_defaults(help=False,
		verbose=False,
		data_dir=config.data_dir)

# Parse arguments and flags
f_list, args = op.parse_args()

#
# Format output to the console
#

class OverloadPrint:
	def __init__(self):
		self.stdout = sys.stdout
	def write(self, txt):
		self.stdout.write("  %s" % txt)

sys.stdout = OverloadPrint()

#
# Argument validation
# 

# check for validity of directory
if not os.path.isdir(f_list.data_dir):
	print "* [ERROR] Invalid data directory (" + f_list.data_dir + ")!"
	sys.exit(config.TYPEARGS_ERROR)

# set appropriate global variables (if any changes)
config.data_dir = f_list.data_dir

# check for correct number of arguments
if len(args) == 0:
	sys.stderr.write("Too few arguments given. Use --help for information on proper usage.\n\n")
	sys.exit(config.NUMARGS_ERROR)
elif len(args) > 1:
	sys.stderr.write("Too many arguments given. Operate on only one data file at a time. Use --help for information on proper usage.\n\n")
	sys.exit(config.NUMARGS_ERROR)

# Extract the correct file from the given information
config.data_file = os.path.abspath(os.path.join(config.data_dir, args[0]))

# check for validity of data file
if not os.path.isfile(config.data_file):
	print "* [ERROR] Invalid data file (" + config.data_file + ")!"
	sys.exit(config.DATA_ERROR)
#
# Display a program header
#

if f_list.verbose:
	print ""
	print "%s v%s" % (config.program_name, config.version)
	print "Written by %s" % config.author
	print config.date
	print "-------------------------------------------------"

# print out extra information

if f_list.verbose:
	print "Current Data Path: " + config.data_file


#
# Execute main program
#
		
import sparklemotion
sparklemotion.launch()

if f_list.verbose:
	print ""	# trailing endline
