import parse.scp_yacc
from compile.renpy import RenpyCompiler

def convert_to_renpy(input_string):
	parser = parse.scp_yacc.parser
	script = parser.parse(input_string)
	compiler = RenpyCompiler()
	return compiler.compile_script(script)