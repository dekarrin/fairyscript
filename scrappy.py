import os.path
import parse.scp_lex
import parse.scp_yacc
from compile.renpy import RenpyCompiler
from compile.word import DocxCompiler

_parser = None
_lexer = None
_comp_renpy = None
_comp_word = None

def get_parser():
	global _parser
	if _parser is None:
		_parser = parse.scp_yacc.parser
	return _parser
	
def get_lexer():
	global _lexer
	if _lexer is None:
		_lexer = parse.scp_lex.lexer
	return _lexer
	
def get_renpy_compiler():
	global _comp_renpy
	if _comp_renpy is None:
		_comp_renpy = RenpyCompiler()
	return _comp_renpy
	
def get_word_compiler():
	global _comp_word
	if _comp_word is None:
		_comp_word = DocxCompiler()
	return _comp_word
	
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
	compiler = get_renpy_compiler()
	return compiler.compile_script(manuscript_ast)
	
def compile_to_word(manuscript_ast):
	compiler = get_word_compiler()
	return compiler.compile_script(manuscript_ast)
	
def show_warnings(compiler):
	warns = compiler.get_warnings()
	for w in warns:
		print "Compiler warning: " + w

if __name__ == "__main__":
	def set_word_compiler_options(args):
		c = get_word_compiler()
		c.paragraph_spacing = args.paragraph_spacing
		c.title = args.title
		c.include_flagsets = args.include_flags
		c.include_varsets = args.include_vars
		c.include_python = args.include_python
		
	def set_renpy_compiler_options(args):
		c = get_renpy_compiler()
		c.default_destination = args.default_destination
		c.default_origin = args.default_origin
		c.default_duration = args.default_duration
		c.quickly_rel = args.quick_speed
		c.slowly_rel = args.slow_speed
		c.tab_spaces = args.tab_spaces
		c.background_ent = args.background_ent

	import argparse
	import pprint
	import sys
	
	class InvalidInputFormatException(Exception):
		pass
		
	class InvalidOutputFormatException(Exception):
		pass
	try:
		argparser = argparse.ArgumentParser(description="Compiles manuscripts to other formats")
		argparser.add_argument('--input', '-i', action='append', help="The file(s) to be compiled. Will be compiled in order. If no input files are specified, scrappy will read from stdin.")
		argparser.add_argument('--output', '-o', nargs=1, help="The file to write the compiled manuscript to. If no output file is specified, scrappy will write to stdout.")
		argparser.add_argument('--pretty', action='store_true', help="Output pretty-print format. Only applies when output is a raw python type.")
		argparser.add_argument('--inputformat', '-f', nargs=1, dest='input_mode', default=['scp'], choices=('scp', 'lex', 'ast'), help="The format of the input(s).")
		argparser.add_argument('--quiet', '-q', action='store_true', help="Suppress compiler warnings. This will not suppress errors reported by the lexer and parser.")
		modegroup = argparser.add_mutually_exclusive_group()
		modegroup.add_argument('--renpy', '-r', dest='output_mode', action='store_const', const='renpy', help="Compile input(s) to Ren'Py-compatible .rpy format. This is the default mode.")
		modegroup.add_argument('--word', '-w', dest='output_mode', action='store_const', const='word', help="Compile input(s) to .docx format.")
		modegroup.add_argument('--lex', '-l', dest='output_mode', action='store_const', const='lex', help="Perform lexical analysis on the input(s) without parsing or compiling.")
		modegroup.add_argument('--ast', dest='output_mode', action='store_const', const='ast', help="Parse the input(s) into an abstract syntax tree without compiling.")
		wordopts = argparser.add_argument_group('human-readable (DOCX) compiler options')
		wordopts.add_argument('--h-paragraph-spacing', metavar='PTS_SPACING', dest='paragraph_spacing', type=int, default=0, help='Set the spacing in pts between each paragraph in the output.')
		wordopts.add_argument('--h-exclude-flags', dest='include_flags', action='store_false', help='Do not produce any output for FLAG statements in the input file.')
		wordopts.add_argument('--h-exclude-vars', dest='include_vars', action='store_false', help='Do not produce any output for VAR statements in the input file.')
		wordopts.add_argument('--h-exclude-python', dest='include_python', action='store_false', help='Produce minimal output for PYTHON statements in the input file.')
		wordopts.add_argument('--h-title', dest='title', default=None, help='Set the title for the script. This will be at the top of all output files.')
		renpyopts = argparser.add_argument_group("ren'py compiler options")
		renpyopts.add_argument('--r-default-destination', metavar='LOCATION', default='center', dest='default_destination', help='Set the destination for motion statements that do not explicitly include one.')
		renpyopts.add_argument('--r-default-origin', metavar='LOCATION', default='center', dest='default_origin', help='Set the origin for motion statements that do not explicitly include one.')
		renpyopts.add_argument('--r-default-duration', metavar='SECONDS', default=0.5, type=float, dest='default_duration', help='Set the default time for statements that use a duration but do not explicitly include one.')
		renpyopts.add_argument('--r-quick-speed', metavar='SECONDS', default=0.25, dest='quick_speed', type=float, help="Set the number of seconds that the phrase 'QUICKLY' is interpreted as.")
		renpyopts.add_argument('--r-slow-speed', metavar='SECONDS', default=2, dest='slow_speed', type=float, help="Set the number of seconds that the phrase 'SLOWLY' is interpreted as.")
		renpyopts.add_argument('--r-tab-spaces', metavar='SPACES', default=4, dest='tab_spaces', type=int, help='Set the number of spaces that are in a single tab in the output.')
		renpyopts.add_argument('--r-background-entity-name', metavar='NAME', default='bg', dest='background_ent', help='Set the name of the entity that is used for the background in scene statements.')
		
		
		argparser.set_defaults(output_mode='renpy', output=['--'])
		args = argparser.parse_args()
		pprint.pprint(args)
		args.input_mode = args.input_mode[0]
		args.output = args.output[0]
		
		if args.input is None:
			args.input = ['--'] # don't pass into set_defaults() or else '--' will always be present
		
		if args.output == '--':
			if args.output_mode == 'word':
				raise InvalidOutputFormatException("cannot output DOCX file to stdout")
			output_file = sys.stdout
		elif args.output_mode != 'word':
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
					set_renpy_compiler_options(args)
					output = compile_to_renpy(ast)
					if not args.quiet:
						show_warnings(get_renpy_compiler())
				elif args.output_mode == 'word':
					set_word_compiler_options(args)
					output = compile_to_word(ast)
					if not args.quiet:
						show_warnings(get_word_compiler())
					
			if (args.output_mode == 'lex' or args.output_mode == 'ast') and args.pretty:
				pprint.pprint(output, output_file)
			elif args.output_mode == 'word':
				try:
					output.save(args.output)
				except IOError, e:
					if e.errno == 13:
						print "Error writing file: permission denied"
						print "Make sure that '" + args.output + "' is not open in another application"
			else:
				output_file.write(str(output))
		if args.output != '--' and args.output_mode != 'word':
			output_file.close()
	except (InvalidInputFormatException, InvalidOutputFormatException), e:
		print("Fatal error: " + e.message)