import sys
import os.path
import script

if len(sys.args) < 2:
	sys.exit("Usage: %s [script file]" % os.path.basename(sys.args[0]))
else:
	script.convert_to_renpy(sys.args[1])