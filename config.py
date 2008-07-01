"""Contains useful global variables.

A header file containing information about the program version information, as well as various defaults for compilation, output folders and other variables which require a (somewhat) global scope.
	
Usage:
	
import pyglobals
# access shared variables

"""

#
# version info
#

program_name = "Sparkle Motion"
program_description = "A visualization platform for observing arm movement."
author = "Matt Revelle and Michael Sullivan"
version = "0.001"
date = "6/16/08"
vers_desc = "%%prog v%s (%s)" % (version, date)

#
# data info
#

import sys, os, os.path
__fldr_name__, __exec_name__ = os.path.split(sys.argv[0])	# get root directory holding script
# form the default directory which holds the data
data_dir = os.path.join(__fldr_name__, "data")
data_dir = os.path.join(data_dir, "fob")		
data_dir = os.path.join(data_dir, "2008_06_09")		
# store the data filename
data_file = ""		

#
# resource variables (provided for ease)
#
cwd = os.getcwd()						# working directory (from caller)
prog_path = __fldr_name__					# folder where framework scripts reside

# error codes
NUMARGS_ERROR = 1
TYPEARGS_ERROR = 2
DATA_ERROR = 3

#
# control values to override defaults
#

def set_globals(zdata_dir = ""):
	global data_dir
	
	# set the appropriate global variables
	if not zdata_dir == "":
		data_dir = zdata_dir

#
# set the data file location
#

def set_data_file(zdata_file = ""):
	global data_dir, data_file

	# join the paths in an appropriate way
	if not zdata_file == "":
		data_file = os.path.abspath(os.path.join(data_dir, zdata_file))	
	
