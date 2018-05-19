from __future__ import print_function
import re
import sys
import logging.handlers

from . import pretty, fileinfo
from .parse import fey_lex
from .parse import fey_yacc
from .compile.renpy import RenpyCompiler
from .compile.word import DocxCompiler
from .compile.analyze import AnalysisCompiler


__version__ = '2.0.3'


_E_ARGS = 1
_E_WRITE = 2
_E_LEXER = 3
_E_PARSER = 4
_E_OTHER = 5


_log = logging.getLogger('fairyscript')  # explicitly give package here so we don't end up getting '__main__'
_log.setLevel(logging.DEBUG)


class ArgumentError(ValueError):
	def __init__(self, msg):
		super(ValueError, self).__init__(msg)


class FileFormatError(Exception):
	def __init__(self, msg):
		super(Exception, self).__init__(msg)


class OutputWriteError(Exception):
	def __init__(self, msg):
		super(Exception, self).__init__(msg)


class InvalidInputFormatError(ArgumentError):
	def __init__(self, msg):
		super(ArgumentError, self).__init__(msg)


class InvalidOutputFormatError(ArgumentError):
	def __init__(self, msg):
		super(ArgumentError, self).__init__(msg)


class LexerError(Exception):
	def __init__(self, errors, msg):
		super(Exception, self).__init__(msg)
		self.error_messages = errors


class ParserError(Exception):
	def __init__(self, errors, msg):
		super(Exception, self).__init__(msg)
		self.error_messages = errors


def _create_parser(filename, no_debug_symbols, inline_sources):
	# TODO: abstract into parser module
	parser = parse.fey_yacc.parser
	parser.successful = True
	parser.error_messages = []
	parser.filename = filename
	parser.no_debug = no_debug_symbols
	parser.header_info = {'has_debug_symbols': not no_debug_symbols}
	parser.inline_sources = inline_sources
	if not inline_sources:
		parser.header_info['sources'] = {}
	parser.reverse_sources = {}
	return parser


def _create_lexer():
	# TODO: abstract into lexer module
	lexer = parse.fey_lex.lexer
	lexer.successful = True
	lexer.error_messages = []
	return lexer


def _lex_manuscript(script_text, file_info):
	symbols = []
	lexer = _create_lexer()
	lexer.input(script_text)
	for tok in lexer:
		symbols.append(tok)
	if not lexer.successful:
		if file_info.is_stdin:
			error_file = "(stdin)"
		else:
			error_file = "file '" + file_info.name + "'"
		errors = [error_file + line for line in lexer.error_messages]
		raise LexerError(errors, "encountered problems during lex")
	lexed = {'symbols': symbols, 'file': file_info.name if not file_info.is_stdin else None}
	return lexed


def _load_lex_tokens(contents):
	from ply.lex import LexToken as Token

	# noinspection PyUnusedLocal,PyPep8Naming
	def LexToken(t_type, value, line, pos):
		t = Token()
		t.type = t_type
		t.value = value
		t.lineno = line
		t.lexpos = pos
		return t

	symbols = eval(contents)
	return symbols


def _parse_manuscript(script_text, file_info, strip_debug, inline_sources):
	fname = file_info.name if not file_info.is_stdin else None
	parser = _create_parser(fname, strip_debug, inline_sources)

	script_ast = parser.parse(script_text)
	if not parser.successful:
		if file_info.is_stdin:
			error_file = "(stdin)"
		else:
			error_file = "file '" + file_info.name + "'"
		errors = [error_file + line for line in parser.error_messages]
		raise ParserError(errors, "encountered problems during parse")
	header_info = parser.header_info
	return {'_meta': header_info, 'nodes': script_ast}


def _parse_symbols(lex_symbols, file_info, strip_debug, inline_sources):
	# need to use this 'dictionary indirection' solution for py 2 compat with closure
	v = {'cur_lex_series': 0}

	parser = _create_parser(lex_symbols[v['cur_lex_series']]['file'], strip_debug, inline_sources)

	def grab_token():
		symbols = lex_symbols[v['cur_lex_series']]['symbols']
		if len(symbols) > 0:
			return symbols.pop(0)
		else:
			v['cur_lex_series'] += 1
			if v['cur_lex_series'] >= len(lex_symbols):
				return None
			elif len(lex_symbols[v['cur_lex_series']]['symbols']) > 0:
				symbols = lex_symbols[v['cur_lex_series']]['symbols']
				if len(symbols) > 0:
					return symbols.pop(0)
		return None

	script_ast = parser.parse(tokenfunc=grab_token)
	if not parser.successful:
		if file_info.is_stdin:
			error_file = "(stdin)"
		else:
			error_file = "file '" + file_info.name + "'"
		errors = [error_file + line for line in parser.error_messages]
		raise ParserError(errors, "encountered problems during parse")
	header_info = parser.header_info
	return {'_meta': header_info, 'nodes': script_ast}


def _strip_ast_debug_symbols(ast):
	if not ast['_meta']['has_debug_symbols']:
		return

	for s in ast:
		if '_debug' in s:
			del s['_debug']
		if 'instruction' in s:
			if s['instruction'] == 'IF':
				for br in s['branches']:
					_strip_ast_debug_symbols(br['statements'])
			elif s['instruction'] == 'WHILE':
				_strip_ast_debug_symbols(s['statements'])

	# TODO: strip other debug symbols as well
	ast['_meta']['has_debug_symbols'] = False


def _combine_asts(ast_1, ast_2):
	meta_1 = ast_1['_meta']
	meta_2 = ast_2['_meta']

	if len(meta_1) == 0:
		return ast_2
	elif len(meta_2) == 0:
		return ast_1

	new_meta = {
		'has_debug_symbols': meta_1['has_debug_symbols'] and meta_2['has_debug_symbols']
	}

	new_nodes = ast_1['nodes'] + ast_2['nodes']

	return {
		'_meta': new_meta,
		'nodes': new_nodes
	}


def _show_warnings(compiler):
	warns = compiler.get_warnings()
	for w in warns:
		_log.warning("Warning: " + w)


def _preprocess(script_ast, target_lang, quiet=False, strip_ast_debugs=False, inline_sources=False):
	def preproc_includes(ast, lang):
		new_ast = {'_meta': dict(ast['_meta']), 'nodes': []}
		for s in ast['nodes']:
			if s['type'] == 'line' or s['type'] == 'comment':
				new_ast['nodes'].append(s)
			elif s['instruction'] == 'IF':
				if_struct = {'type': 'annotation', 'instruction': 'IF', 'branches': []}
				for br in s['branches']:
					# pass in new_ast['_meta'] so it is automatically mutated.
					br_ast = {'_meta': new_ast['_meta'], 'nodes': br['statements']}
					br_ast = preproc_includes(br_ast, lang)
					if_branch = {'condition': br['condition'], 'statements': br_ast['nodes']}
					if_struct['branches'].append(if_branch)
				new_ast['nodes'].append(if_struct)
			elif s['instruction'] == 'WHILE':
				# pass in new_ast['_meta'] so it is automatically mutated.
				wh_ast = {'_meta': new_ast['_meta'], 'nodes': s['statements']}
				wh_ast = preproc_includes(wh_ast, lang)
				wh_struct = {
					'type': 'annotation',
					'instruction': 'WHILE',
					'condition': s['condition'],
					'statements': wh_ast['nodes']
				}
				new_ast['nodes'].append(wh_struct)
			elif s['instruction'] == 'INCLUDE':
				if s['langs'] is None or lang in [x[1] for x in s['langs']]:
					if s['parsing'][1]:
						info = fileinfo.FileInfo(mode='r', name=s['file'][1])
						with open(s['file'][1], 'r') as inc_file:
							contents = inc_file.read()

						inc_ast = _parse_manuscript(contents, info, strip_ast_debugs, inline_sources)
						new_ast = _combine_asts(new_ast, preproc_includes(inc_ast, lang))
					else:
						new_ast['nodes'].append(s)
			else:
				new_ast['nodes'].append(s)
		return new_ast
	
	def preproc_chars(ast_nodes):
		chars_dict = {}
		for s in ast_nodes:
			if s['type'] != 'line' and s['type'] != 'comment':
				if s['instruction'] == 'IF':
					for br in s['branches']:
						preproc_chars(br['statements'])
				elif s['instruction'] == 'WHILE':
					preproc_chars(s['statements'])
				elif s['instruction'] == 'CHARACTERS':
					filename = s['file'][1]
					new_chars = {}
					try:
						new_chars = _read_chars_file(filename)
					except (IOError, FileFormatError) as e:
						if not quiet:
							msg = "Preprocessor warning: could not process characters file '%s':\n\t%s"
							_log.warning(msg % (filename, e.message))
					chars_dict.update(new_chars)
		return chars_dict

	new_script_ast = preproc_includes(script_ast, target_lang)
	chars = preproc_chars(new_script_ast)
	return new_script_ast, chars


def _read_chars_file(file_path):
	field_names = ('id', 'name', 'color')
	rows = {}
	with open(file_path, 'r') as f:
		ln = 0
		for line in f:
			ln += 1
			fields = []
			line = line.strip()
			r = {}
			ended_with_comma = False
			while len(line) > 0:
				ended_with_comma = False
				if line[0] == ',':
					if len(fields) == 0:
						raise FileFormatError("Line %d: identifier field cannot be empty" % ln)
					fields.append(None)
					ended_with_comma = True
					line = line[1:].strip()
					
				else:
					m = re.match(r"\"[^\"\\]*(?:\\.[^\"\\]*)*\"", line)
					if m is None:
						raise FileFormatError("Line %d: bad format" % ln)
					stripped = ''
					escaping = False
					s = line[m.start():m.end()]
					s = s[1:-1]
					for c in s:
						if c == '\\' and not escaping:
							escaping = True
						else:
							stripped += c
							escaping = False
					fields.append(stripped)
					line = line[m.end():].strip()
					if len(line) > 0 and line[0] == ',':
						ended_with_comma = True
						line = line[1:].strip()
			if ended_with_comma:
				fields.append(None)
			if len(fields) < len(field_names):
				raise FileFormatError("Line %d: bad format" % ln)

			for name, value in zip(field_names, fields):
				r[name] = value
			r['other'] = fields[len(field_names):]
			rows[r['id']] = r
			if r['name'] is None:
				r['name'] = r['id']
	return rows


def _precompile(ast, args, compiler):
	ast, chars = _preprocess(
		ast, args.output_mode, quiet=args.quiet, strip_ast_debugs=args.no_debug_symbols,
		inline_sources=args.inline_sources
	)
	compiler.set_options(args)
	compiler.set_characters(chars)
	return ast


def _add_renpy_subparser(subparsers, parent):
	rpy_desc = "Compile input(s) to Ren'Py-compatible .rpy format."
	rpy = subparsers.add_parser(
		'renpy', help="Compile to Ren'Py.", description=rpy_desc, parents=[parent]
	)
	""":type : argparse.ArgumentParser"""

	dest_help = 'Set the destination for motion statements that do not explicitly include one.'
	rpy.add_argument('--default-destination', metavar='LOC', default='center', help=dest_help)

	origin_help = 'Set the origin for motion statements that do not explicitly include one.'
	rpy.add_argument('--default-origin', metavar='LOC', default='center', help=origin_help)

	dur_help = 'Set the default time for statements that use a duration but do not explicitly include one.'
	rpy.add_argument('--default-duration', metavar='SECS', default=0.5, type=float, help=dur_help)

	quick_help = "Set the number of seconds that the phrase 'QUICKLY' is interpreted as."
	rpy.add_argument('--quick-speed', metavar='SECS', default=0.25, type=float, help=quick_help)

	slow_help = "Set the number of seconds that the phrase 'SLOWLY' is interpreted as."
	rpy.add_argument('--slow-speed', metavar='SECS', default=2, type=float, help=slow_help)

	tab_help = "Set the number of spaces that are in a single tab in the output."
	# noinspection PyTypeChecker
	rpy.add_argument('--tab-width', metavar='SPACES', default=4, type=int, help=tab_help)

	back_help = 'Set the name of the entity that is used for the background in scene statements.'
	rpy.add_argument('--background-entity', metavar='NAME', default='bg', help=back_help)

	cam_help = 'Use the experimental camera system instead of just outputting camera instructions as dialog.'
	rpy.add_argument('--enable-camera', action='store_true', help=cam_help)


def _add_docx_subparser(subparsers, parent):
	docx_desc = "Compile input(s) to a human-readable, script-like .docx format."
	docx = subparsers.add_parser(
		'docx', help="Compile to DOCX.", description=docx_desc, parents=[parent]
	)
	""":type : argparse.ArgumentParser"""

	para_help = 'Set the spacing in pts between each paragraph in the output.'
	# noinspection PyTypeChecker
	docx.add_argument('--paragraph-spacing', metavar='PTS', type=int, default=0, help=para_help)

	flags_help = 'Do not produce any output for FLAG statements in the input file.'
	docx.add_argument('--exclude-flags', dest='include_flags', action='store_false', help=flags_help)

	vars_help = 'Do not produce any output for VAR statements in the input file.'
	docx.add_argument('--exclude-vars', dest='include_vars', action='store_false', help=vars_help)

	python_help = 'Produce minimal output for PYTHON statements in the input file.'
	docx.add_argument('--exclude-python', dest='include_python', action='store_false', help=python_help)

	title_help = 'Set the title for the script. This will be at the top of all output files.'
	docx.add_argument('--title', default=None, help=title_help)


def _add_lex_subparser(subparsers, parent):
	lex_desc = "Perform lexical tokenization on the input(s) without parsing or compiling, and output the symbol list."
	lex = subparsers.add_parser(
		'lex', help="Lex the contents without parsing.", description=lex_desc, parents=[parent]
	)
	""":type : argparse.ArgumentParser"""

	lex.add_argument('--pretty', action='store_true', help="Output pretty-print formatted list of symbols.")


def _add_ast_subparser(subparsers, parent):
	ast_desc = "Parse the input(s) into an abstract syntax tree without compiling, and output the AST."
	ast = subparsers.add_parser(
		'ast', help="Parse the contents without compiling.", description=ast_desc, parents=[parent]
	)
	""":type : argparse.ArgumentParser"""

	ast.add_argument('--pretty', action='store_true', help="Output pretty-print formatted AST.")
	ast.add_argument('--no-debug-symbols', action='store_true', help="Do not include debug symbols in AST.")

	inline_help = "Attach full source file name directly to each node's debug symbol list"
	ast.add_argument('--inline-sources', action='store_true', help=inline_help)


def _add_analyze_subparser(subparsers, parent):
	ana_desc = "Perform an analysis on the identifiers and references that the final output will require"
	ana_desc += " implementations for."
	ana = subparsers.add_parser(
		'analyze', help="Perform static analysis.", description=ana_desc, parents=[parent]
	)
	""":type : argparse.ArgumentParser"""

	order_help = "Select the order of entries in the analysis output."
	ana.add_argument('--order', default='name', choices=('usage', 'name'), help=order_help)


def _parse_args():
	# TODO: argparse not available before python 2.7; if we want compat before then we need a rewrite
	import argparse

	parser = argparse.ArgumentParser(description="Compiles manuscripts to other formats")

	parser.add_argument('--version', action='version', version="%(prog)s " + __version__)

	# these args will not be properly parsed if we just add them to the root parser
	parent = argparse.ArgumentParser(add_help=False)
	input_help = "The file(s) to be compiled. Will be compiled in order. If no input files are specified, fairyc will"
	input_help += " read from stdin."
	parent.add_argument('input', nargs='*', type=argparse.FileType('r'), default=[sys.stdin], help=input_help)

	quiet_help = "Suppress compiler warnings, as well as lexer and parser errors."
	parent.add_argument('--quiet', '-q', action='store_true', help=quiet_help)

	output_help = "The file to write the compiled manuscript to. If no output file is specified, fairyc will write to"
	output_help += " stdout."
	parent.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout, help=output_help)

	parent.add_argument('--logfile', '-l', default=None, help="Sets a logfile to write all output to.")

	fmt_help = "The format of the input(s)."
	parent.add_argument('--format', '-f', default='fey', choices=('fey', 'lex', 'ast'), help=fmt_help)

	# space at the end of metavar is not a typo; we need it so help output is prettier
	subparsers = parser.add_subparsers(
		description="Functionality to execute.", metavar="SUBCOMMAND", dest='output_mode'
	)
	subparsers.required = True

	_add_renpy_subparser(subparsers, parent)
	_add_docx_subparser(subparsers, parent)
	_add_lex_subparser(subparsers, parent)
	_add_ast_subparser(subparsers, parent)
	_add_analyze_subparser(subparsers, parent)

	try:
		parser.set_defaults(no_debug_symbols=False)
		args = parser.parse_args()
	except argparse.ArgumentError as e:
		raise ArgumentError(str(e))

	if args.output == sys.stdout and args.output_mode == 'docx':
		raise InvalidOutputFormatError("cannot output DOCX file to stdout")

	return args


def _run_compiler(args):
	# first, load in all source files and convert to a single AST, or symbol list (if only lexing):
	input_data = [] if args.output_mode == 'lex' else {'_meta': {}, 'nodes': []}
	for input_file in args.input:
		file_contents = input_file.read()
		input_file.close()

		if args.output_mode == 'lex':
			if args.format == 'fey':
				info = fileinfo.from_file(input_file)
				lex_symbols = _lex_manuscript(file_contents, info)
			elif args.format == 'lex':
				lex_symbols = _load_lex_tokens(file_contents)
			else:
				raise InvalidInputFormatError("to output lexer symbols, input format must be fey or lex")
			input_data.append(lex_symbols)
		else:
			# note that args.no_debug_symbols can only be true if we are in ast output format mode
			# (guaranteed by argument parsing at time of this writing)

			if args.format == 'fey':
				info = fileinfo.from_file(input_file)
				ast = _parse_manuscript(file_contents, info, args.no_debug_symbols, args.inline_sources)
			elif args.format == 'lex':
				info = fileinfo.from_file(input_file)
				ast = _parse_symbols(_load_lex_tokens(file_contents), info, args.no_debug_symbols, args.inline_sources)
			elif args.format == 'ast':
				ast = eval(file_contents)
				if args.no_debug_symbols:
					_strip_ast_debug_symbols(ast)
			else:
				raise InvalidInputFormatError(
					"to output AST or compiled formats, input format must be fey, lex, or ast")
			input_data = _combine_asts(input_data, ast)

	# now compile as necessary
	if args.output_mode == 'ast' or args.output_mode == 'lex':
		# already done, we got the desired format during input processing
		output_data = input_data
	else:
		# preprocess and compile
		if args.output_mode == 'renpy':
			compiler = RenpyCompiler()
		elif args.output_mode == 'docx':
			compiler = DocxCompiler()
		elif args.output_mode == 'analyze':
			compiler = AnalysisCompiler()
		else:
			raise ValueError("Unknown output mode '" + args.output_mode + "'")

		ast = _precompile(input_data, args, compiler)
		output_data = compiler.compile_script(ast)
		if not args.quiet:
			_show_warnings(compiler)

	# finally, write the output to disk
	if (args.output_mode == 'lex' or args.output_mode == 'ast') and args.pretty:
		pretty.pretty(output_data, args.output)
	elif args.output_mode == 'docx':
		# docx is saved via framework's save() method
		args.output.close()
		try:
			output_data.save(args.output.name)
		except IOError as e:
			if e.errno == 13:
				raise OutputWriteError("permission denied")
			else:
				raise
	else:
		args.output.write(str(output_data))

	# close the file
	args.output.close()


def run():
	stderr_handler = _setup_logger()

	try:
		args = _parse_args()
	except ArgumentError as e:
		_log.critical("Bad arguments: " + str(e))
		_log.debug("Exception Details\n", exc_info=True)
		sys.exit(_E_ARGS)

	if args.quiet:
		stderr_handler.setLevel(logging.CRITICAL)
	if args.logfile:
		_setup_file_log(args.logfile)

	try:
		_run_compiler(args)
	except OutputWriteError as e:
		_log.critical("Critical error: " + str(e))
		_log.error("Make sure that the output file is not open in another application")
		_log.debug("Exception Details\n", exc_info=True)
		sys.exit(_E_WRITE)
	except LexerError as e:
		for msg in e.error_messages:
			_log.error(msg)
		_log.critical("Critical error: Lexing failed")
		_log.debug("Exception Details\n", exc_info=True)
		sys.exit(_E_LEXER)
	except ParserError as e:
		for msg in e.error_messages:
			_log.error(msg)
		_log.critical("Critical error: Parsing failed")
		_log.debug("Exception Details\n", exc_info=True)
		sys.exit(_E_PARSER)
	# This is the top-level exception handler for any we might have missed. It's okay to catch 'Exception' here.
	# noinspection BroadException
	except Exception as e:
		err_type = type(e).__name__
		_log.critical("Critical " + err_type + ": " + str(e))
		_log.debug("Exception Details\n", exc_info=True)
		sys.exit(_E_OTHER)


def _setup_logger():
	"""
	Setup logging facilities.
	:return: the stderr_handler so we can set set the level after arguments are parsed.
	"""
	stderr_handler = logging.StreamHandler(stream=sys.stderr)
	stderr_handler.setLevel(logging.INFO)
	stderr_handler.setFormatter(logging.Formatter("%(message)s"))
	logging.getLogger().addHandler(stderr_handler)

	return stderr_handler


def _setup_file_log(filename):
	# max bytes = 100 MB
	file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=104857600, backupCount=5)
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(logging.Formatter("[%(asctime)-15s] - (%(levelname)-8s): %(message)s"))
	logging.getLogger().addHandler(file_handler)


if __name__ == "__main__":
	run()
