import sys
import os.path
import script
from pprint import pprint

if len(sys.argv) < 3:
	sys.exit("Usage: %s [.scr file] [.rpy file]" % os.path.basename(sys.argv[0]))
else:
	with open(sys.argv[1], 'r') as file:
		contents = file.read()
	rpy = script.convert_to_renpy(contents)
	with open(sys.argv[2], 'w') as file:
		file.write(rpy)