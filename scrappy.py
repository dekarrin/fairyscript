import os.path
import parse.scp_lex
import parse.scp_yacc
from compile.renpy import RenpyCompiler

if __name__ == "__main__":
	import sys
	
	if len(sys.argv) < 3:
		sys.exit("Usage: %s [.scr file] [.rpy file]" % os.path.basename(sys.argv[0]))
	else:
		with open(sys.argv[1], 'r') as file:
			contents = file.read()
		script = parse_manuscript(contents)
		rpy = compile_to_renpy(script)
		with open(sys.argv[2], 'w') as file:
			file.write(rpy)
	
def lex_manuscript(script_text):
	symbols = []
	lexer = parse.scp_lex.lexer
	lexer.input(script_text)
	for tok in lexer:
		symbols.append(tok)
	return symbols

def parse_manuscript(script_text):
	parser = parse.scp_yacc.parser
	script = parser.parse(script_text)
	return script
	
def compile_to_renpy(manuscript):
	compiler = RenpyCompiler()
	return compiler.compile_script(manuscript)
	