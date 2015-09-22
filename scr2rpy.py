import sys
import os.path
import script

if len(sys.argv) < 2:
	sys.exit("Usage: %s [script file]" % os.path.basename(sys.argv[0]))
else:
	with open(sys.argv[1], 'r') as file:
		contents = file.read()
	script.convert_to_renpy(contents)