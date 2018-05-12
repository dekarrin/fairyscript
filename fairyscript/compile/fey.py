# contains various functions useful for getting information out ouf a .fey script tree

import re


def typed_check(var, type, val=None):
	if var is None:
		return False
	if val is None:
		return var[0] == type
	else:
		return var[0] == type and var[1] == val


def get_expr(var, non_incdec_prefix=None):
	if non_incdec_prefix is None:
		non_incdec_prefix = ""
	if typed_check(var, 'string'):
		return non_incdec_prefix + quote(var[1])
	elif typed_check(var, 'expr'):
		return non_incdec_prefix + '(' + var[1] + ')'
	elif typed_check(var, 'incdec'):
		return get_incdec_str(var)
	else:
		return non_incdec_prefix + str(var[1])


def get_incdec_str(var):
	val = var[1]
	if typed_check(val['type'], 'rel', 'INC'):
		return '+= ' + str(val['amount'][1])
	elif typed_check(val['type'], 'rel', 'DEC'):
		return '-= ' + str(val['amount'][1])


def quote(str, quote_char='"'):
	str = str.replace('\\', '\\\\')
	str = str.replace(quote_char, '\\' + quote_char)
	return quote_char + str + quote_char


def get_duration(source, quickly_time, slowly_time, default_time):
	time = None
	if typed_check(source, 'rel', 'QUICKLY'):
		time = quickly_time
	elif typed_check(source, 'rel', 'SLOWLY'):
		time = slowly_time
	elif typed_check(source, 'number'):
		time = source[1]
	else:
		time = default_time
	return time


def get_duration_words(source, num_fmt):
	if source is not None:
		if typed_check(source, 'rel'):
			dur = source[1].lower()
		else:
			dur = num_fmt % source[1]
		return ' ' + dur
	else:
		return ''


def to_words(identifier):
	step1 = " ".join(identifier.split('_'))
	return " ".join(step1.split('-'))


def extract_comment(source):
	return source.lstrip('#').lstrip()


def indef_article(noun):
	start = noun.lower().lstrip()[0]
	if start in ('a', 'e', 'i', 'o', 'u'):
		return 'an'
	else:
		return 'a'


def to_human_readable(expr):
	readable_versions = [
		('==', 'is equal to'),
		('>=', 'is greater than or equal to'),
		('<=', 'is less than or equal to'),
		('>', 'is greater than'),
		('<', 'is less than'),
		('!=', 'is not equal to'),
		(r'(\w+)\s*\+=', r'increase \1 by'),
		(r'(\w+)\s*-=', r'decrease \1 by'),
		(r'\+', 'plus'),
		('-', 'minus'),
		(r'\*', 'times'),
		('/', 'divided by'),
		('%', 'modulo')
	]
	for readable in readable_versions:
		search = r'\s*' + readable[0] + r'\s*'
		replacement = ' ' + readable[1] + ' '
		expr = re.sub(search, replacement, expr)
	if expr.startswith('(') and expr.endswith(')'):
		expr = expr[1:-1]
	return expr


def pluralize(num, word, append="s"):
	if num != 1:
		out = str(num) + " " + word + append
	else:
		out = str(num) + " " + word
	return out
