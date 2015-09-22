import ply.lex as lex

reserved = [
	'TO',
	'IN',
	'OUT',
	'FROM',
	'FOR',
	'OFF',
	'ON',
	'INC',
	'DEC',
	'BY',
	'SET',
	'HIDE',
	'SHOW',
	'AUTO',
	'FADEOUT',
	'ZOOM',
	'LOOP',
	'STOP',
	'ALL',
	'SECONDS'
]

tokens = [
	'DIRECTIVEOPEN_SCENE',
	'DIRECTIVEOPEN_ENTER',
	'DIRECTIVEOPEN_ACTION',
	'DIRECTIVEOPEN_EXIT',
	'DIRECTIVEOPEN_MUSIC',
	'DIRECTIVEOPEN_SFX',
	'DIRECTIVEOPEN_GFX',
	'DIRECTIVEOPEN_FMV',
	'DIRECTIVEOPEN_DIALOG',
	'DIRECTIVEOPEN_CAMERA',
	'DIRECTIVEOPEN_CHOICE',
	'DIRECTIVECLOSE',
	'ANNOTATIONOPEN_SECTION',
	'ANNOTATIONOPEN_FLAGSET',
	'ANNOTATIONOPEN_VARSET',
	'ANNOTATIONOPEN_GOTO',
	'ANNOTATIONOPEN_EXECUTE',
	'ANNOTATIONOPEN_END',
	'ANNOTATIONOPEN_IF',
	'ANNOTATIONOPEN_ELSE',
	'ANNOTATIONOPEN_ELIF',
	'ANNOTATIONOPEN_WHILE',
	'ANNOTATIONCLOSE',
	'ID_PREDEF',
	'ID',
	'PARAMSOPEN',
	'STRING',
	'FADEOUT_OLD',
	'NUMBER',
	'PYTHON_BLOCK',
	'SNAP_TO',
	'PAN_TO',
	'EXPRESSION',
	'SHOW_IF',
	'COMMENT'
] + reserved

literals = [',', '=', ':', '*', '}', '{', '(', ')']

t_DIRECTIVEOPEN_SCENE = r"\[[Ss][Cc][Ee][Nn][Ee]"
t_DIRECTIVEOPEN_ENTER = r"\[[Ee][Nn][Tt][Ee][Rr]"
t_DIRECTIVEOPEN_ACTION = r"\["
t_DIRECTIVEOPEN_EXIT = r"\[[Ee][Xx][Ii][Tt]"
t_DIRECTIVEOPEN_MUSIC = r"\[[Mm][Uu][Ss][Ii][Cc]"
t_DIRECTIVEOPEN_SFX = r"\[[Ss][Ff][Xx]"
t_DIRECTIVEOPEN_GFX = r"\[[Gg][Ff][Xx]"
t_DIRECTIVEOPEN_FMV = r"\[[Ff][Mm][Vv]"
t_DIRECTIVEOPEN_DIALOG = r"\[[Di][Aa][Ll][Oo][Gg]"
t_DIRECTIVEOPEN_CAMERA = r"\[[Cc][Aa][Mm][Ee][Rr][Aa]"
t_DIRECTIVEOPEN_CHOICE = r"\[[Cc][Hh][Oo][Ii][Cc][Ee]"
t_DIRECTIVECLOSE = r"\]"
t_ANNOTATIONOPEN_SECTION = r"\([Ss][Ee][Cc][Tt][Ii][Oo][Nn]"
t_ANNOTATIONOPEN_FLAGSET = r"\([Ff][Ll][Aa][Gg]"
t_ANNOTATIONOPEN_VARSET = r"\([Vv][Aa][Rr]"
t_ANNOTATIONOPEN_GOTO = r"\([Gg][Oo]\s?[Tt][Oo]"
t_ANNOTATIONOPEN_EXECUTE = r"\([Ee][Xx][Ee][Cc][Uu][Tt][Ee]"
t_ANNOTATIONOPEN_END = r"\([Ee][Nn][Dd]"
t_ANNOTATIONOPEN_IF = r"\([Ii][Ff]"
t_ANNOTATIONOPEN_ELSE = r"\([Ee][Ll][Ss][Ee]"
t_ANNOTATIONOPEN_ELIF = r"\([Ee][Ll](?:[Ss][Ee]\s?)?[Ii][Ff]"
t_ANNOTATIONOPEN_WHILE = r"\([Ww][Hh][Ii][Ll][Ee]"
t_ANNOTATIONCLOSE = r"\)"
t_PARAMSOPEN = r"WITH\sPARAMS"
t_STRING = r"\"[^\"\\]*(?:\\.[^\"\\]*)*\""
t_FADEOUT_OLD = "FADEOUT\sOLD"
t_NUMBER = r"(?:(?:\+|-)\s*)?\d+(\.\d*)?"
t_PYTHON_BLOCK = r"\([Pp][Yy][Tt][Hh][Oo][Nn]\)\s*\{[^}\\]*(?:\\.[^}\\]*)*\}"
t_SNAP_TO = r"SNAP\sTO"
t_PAN_TO = r"PAN\sTO"
# master regex uses a capturing group, so group in this regex is really #2:
t_EXPRESSION = r"\(([^:]*):(?:[^:]|:(?!\2\))*):\2\)"
t_SHOW_IF = "SHOW\sIF"
t_COMMENT = r"\#.*"

def t_ID_PREDEF(t):
	r"[_A-Z][_A-Z0-9]*"
	if t.value in reserved:
		t.type = t.value
	else:
		t.type = 'ID_PREDEF'
	return t

def t_ID(t):
	r"[_a-zA-Z][_a-zA-Z0-9]*"
	if t.value in reserved:
		t.type = t.value
	else:
		t.type = 'ID'
	return t

def t_newline(t):
	r"\n+"
	t.lexer.lineno += len(t.value)
	
def t_error(t):
	print("Warning:")
	print("Line %d: Illegal character '%s'; skipping" % t.lexer.lineno, t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()