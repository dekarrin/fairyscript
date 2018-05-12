# custom implementation of pretty-printing for fully consistent results.
# for use only with lexer symbol lists and asts.

import sys

from ply.lex import LexToken


def pretty(obj, stream=sys.stdout):
	p = Prettifyer(stream)
	p.format(obj)


class Prettifyer(object):
	def __init__(self, stream):
		self._tabs = 0
		self._stream = stream

	def format(self, obj):
		self._format(obj)
		self.writeln()
		self._stream.flush()

	def _format(self, obj):
		t = type(obj)
		if issubclass(t, dict):
			self._format_dict(obj)
		elif issubclass(t, list):
			self._format_seq(obj, '[', ']')
		elif issubclass(t, tuple):
			self._format_seq(obj, '(', ')', multiline=False)
		elif issubclass(t, set):
			self._format_seq(obj, '([', '])')
		elif issubclass(t, LexToken):
			self._format_lex_token(obj)
		else:
			self.write(repr(obj))

	def _format_lex_token(self, obj):
		str_repr = "LexToken(%r,%r,%r,%r)" % (obj.type, obj.value, obj.lineno, obj.lexpos)
		self.write(str_repr)

	def _format_dict(self, obj):
		if len(obj) == 0:
			self.write("{}")
			return
		else:
			self.writeln("{")
		self.inc_tab()
		for i, k in enumerate(sorted(obj.keys())):
			self.tab()
			self.write(repr(k) + ": ")
			v = obj[k]
			self._format(v)
			if i < len(obj.keys()) - 1:
				self.writeln(",")
			else:
				self.writeln()
		self.dec_tab()
		self.tab()
		self.write("}")

	def _format_seq(self, obj, start, end, multiline=True):
		if len(obj) == 0:
			self.write(start + end)
			return
		if multiline:
			self.writeln(start)
		else:
			self.write(start)
		self.inc_tab()
		for i, v in enumerate(obj):
			if multiline:
				self.tab()
			self._format(v)
			if i < len(obj) - 1:
				if multiline:
					self.writeln(",")
				else:
					self.write(", ")
			elif multiline:
				self.writeln()
		self.dec_tab()
		if multiline:
			self.tab()
		self.write(end)

	def inc_tab(self):
		self._tabs += 1

	def dec_tab(self):
		self._tabs -= 1

	def tab(self):
		self.write(self._tabs * '\t')

	def write(self, text=""):
		self._stream.write(text)

	def writeln(self, text=""):
		self.write(text)
		self.write("\n")
