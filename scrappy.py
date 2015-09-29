import os.path
import parse.scp_lex
import parse.scp_yacc
from compile.renpy import RenpyCompiler
	
def lex_manuscript(script_text):
	symbols = []
	lexer = parse.scp_lex.lexer
	lexer.input(script_text)
	for tok in lexer:
		symbols.append(tok)
	return symbols

def parse_manuscript(script_text):
	parser = parse.scp_yacc.parser
	script_ast = parser.parse(script_text)
	return script_ast
	
def parse_symbols(symbols):
	def grab_token():
		for s in symbols:
			yield s
	parser = parse.scp_yacc.parser
	script_ast = parser.parse(tokenfunc=grab_token)
	return script_ast
	
def compile_to_renpy(manuscript_ast):
	compiler = RenpyCompiler()
	return compiler.compile_script(manuscript_ast)
	
def compile_to_word(manuscript_ast):
	return ""

if __name__ == "__main__":
	import argparse
	import pprint
	import sys
	
	class InvalidInputFormatException(Exception):
		pass
	
	argparser = argparse.ArgumentParser(description="Compiles manuscripts to other formats")
	argparser.add_argument('--input', '-i', action='append', help="The file(s) to be compiled. Will be compiled in order. If no input files are specified, scrappy will read from stdin.")
	argparser.add_argument('--output', '-o', nargs=1, help="The file to write the compiled manuscript to. If no output file is specified, scrappy will write to stdout.")
	argparser.add_argument('--pretty', action='store_true', help="Output pretty-print format. Only applies when output is a raw python type.")
	argparser.add_argument('--inputformat', '-f', nargs=1, dest='input_mode', default=['scp'], choices=('scp', 'lex', 'ast'), help="The format of the input(s).")
	modegroup = argparser.add_mutually_exclusive_group()
	modegroup.add_argument('--renpy', '-r', dest='output_mode', action='store_const', const='renpy', help="Compile input(s) to Ren'Py-compatible .rpy format. This is the default mode.")
	modegroup.add_argument('--word', '-w', dest='output_mode', action='store_const', const='word', help="Compile input(s) to .docx format.")
	modegroup.add_argument('--lex', '-l', dest='output_mode', action='store_const', const='lex', help="Perform lexical analysis on the input(s) without parsing or compiling.")
	modegroup.add_argument('--ast', dest='output_mode', action='store_const', const='ast', help="Parse the input(s) into an abstract syntax tree without compiling.")
	argparser.set_defaults(output_mode='renpy', output=['--'])
	args = argparser.parse_args()
	args.input_mode = args.input_mode[0]
	args.output = args.output[0]
	
	if args.input is None:
		args.input = ['--'] # don't pass into set_defaults() or else '--' will always be present
	
	if args.output == '--':
		output_file = sys.stdout
	else:
		output_file = open(args.output, 'w')
	
	for filename in args.input:
		if filename == '--':
			file_contents = sys.stdin.read()
		else:
			with open(filename, 'r') as file:
				file_contents = file.read()
			
		if args.output_mode == 'lex':
			if args.input_mode == 'scp':
				output = lex_manuscript(file_contents)
			elif args.input_mode == 'lex':
				output = eval(file_contents)
			else:
				raise InvalidInputFormatException("to output lexer symbols, input format must be scp or lex")
		else:
			if args.input_mode == 'scp':
				ast = parse_manuscript(file_contents)
			elif args.input_mode == 'lex':
				ast = parse_symbols(eval(file_contents))
			elif args.input_mode == 'ast':
				ast = eval(file_contents)
			else:
				raise InvalidInputFormatException("to output AST or compiled formats, input format must be scp, lex, or ast")
				
			if args.output_mode == 'ast':
				output = ast
			elif args.output_mode == 'renpy':
				output = compile_to_renpy(ast)
			elif args.output_mode == 'word':
				output = compile_to_word(ast)
				
		if (args.output_mode == 'lex' or args.output_mode == 'ast') and args.pretty:
			pprint.pprint(output, output_file)
		else:
			output_file.write(str(output))
	if args.output != '--':
		output_file.close()
		