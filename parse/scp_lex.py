import ply.lex as lex

states = (
	('descopen', 'exclusive'),
	('descscan', 'exclusive'),
	('descid', 'exclusive'),
	('descescapedwords', 'exclusive'),
	('descwords', 'exclusive'),
)

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
	'ZOOM',
	'LOOP',
	'STOP',
	'ALL',
	'SECONDS',
	'RETURN',
	'QUICKLY',
	'SLOWLY',
	'GO',
	'AND'
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
	'DIRECTIVEOPEN_CAMERA',
	'DIRECTIVEOPEN_CHOICE',
	'ANNOTATIONOPEN_DESCRIPTION',
	'ANNOTATIONOPEN_SECTION',
	'ANNOTATIONOPEN_DIALOG',
	'ANNOTATIONOPEN_FLAGSET',
	'ANNOTATIONOPEN_VARSET',
	'ANNOTATIONOPEN_GOTO',
	'ANNOTATIONOPEN_EXECUTE',
	'ANNOTATIONOPEN_END',
	'ANNOTATIONOPEN_IF',
	'ANNOTATIONOPEN_ELSE',
	'ANNOTATIONOPEN_ELIF',
	'ANNOTATIONOPEN_WHILE',
	'ANNOTATIONOPEN_INCLUDE',
    'ANNOTATIONOPEN_CHARACTERS',
	'ID',
	'PARAMSOPEN',
	'STRING',
	'FADEOUT_OLD',
	'NUMBER',
	'PYTHON_BLOCK',
	'SNAP_TO',
	'PAN_TO',
	'BARE_EXPRESSION',
	'SHOW_IF',
	'COMMENT',
	'UNQUOTED_STRING',
	'WITH_PREVIOUS'
] + reserved

literals = [',', '=', ':', '*', '}', '{', '(', ')', ']']

t_DIRECTIVEOPEN_SCENE = r"\[[Ss][Cc][Ee][Nn][Ee]"
t_DIRECTIVEOPEN_ENTER = r"\[[Ee][Nn][Tt][Ee][Rr]"
t_DIRECTIVEOPEN_ACTION = r"\["
t_DIRECTIVEOPEN_EXIT = r"\[[Ee][Xx][Ii][Tt]"
t_DIRECTIVEOPEN_MUSIC = r"\[[Mm][Uu][Ss][Ii][Cc]"
t_DIRECTIVEOPEN_SFX = r"\[[Ss][Ff][Xx]"
t_DIRECTIVEOPEN_GFX = r"\[[Gg][Ff][Xx]"
t_DIRECTIVEOPEN_FMV = r"\[[Ff][Mm][Vv]"
t_DIRECTIVEOPEN_CAMERA = r"\[[Cc][Aa][Mm][Ee][Rr][Aa]"
t_DIRECTIVEOPEN_CHOICE = r"\[[Cc][Hh][Oo][Ii][Cc][Ee]"
t_ANNOTATIONOPEN_DIALOG = r"\([Dd][Ii][Aa][Ll][Oo][Gg]"
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
t_ANNOTATIONOPEN_CHARACTERS = r"\([Cc][Hh][Aa][Rr][Aa][Cc][Tt][Ee][Rr][Ss]"
t_ANNOTATIONOPEN_INCLUDE = r"\([Ii][Nn][Cc][Ll][Uu][Dd][Ee]"
t_STRING = r"\"[^\"\\]*(?:\\.[^\"\\]*)*\""
t_NUMBER = r"(?:(?:\+|-)\s*)?\d+(\.\d*)?"
t_PYTHON_BLOCK = r"\([Pp][Yy][Tt][Hh][Oo][Nn]\)\s*\{[^}\\]*(?:\\.[^}\\]*)*\}"
# master regex uses a capturing group, so group in this regex is really #2:
t_BARE_EXPRESSION = r"'[^'\\]*(?:\\.[^'\\]*)*'"
t_COMMENT = r"\#.*"

t_ANY_ignore = ' \t'


def t_ANNOTATIONOPEN_DESCRIPTION(t):
	r"\([Dd][Ee][Ss][Cc][Rr][Ii][Pp][Tt][Ii][Oo][Nn]"
	t.lexer.desc_id = False
	t.lexer.begin('descopen')
	return t
	
def t_descopen_colon(t):
	':'
	t.lexer.desc_start = t.lexer.lexpos
	t.lexer.begin('descscan')
	t.type = ':'
	return t

def t_FADEOUT_OLD(t):
	r"FADEOUT\sOLD"
	return t
	
def t_WITH_PREVIOUS(t):
	r"WITH\sPREVIOUS"
	return t
	
def t_SNAP_TO(t):
	r"SNAP\sTO"
	return t

def t_PAN_TO(t):
	r"PAN\sTO"
	return t
	
def t_SHOW_IF(t):
	r"SHOW\sIF"
	return t

def t_PARAMSOPEN(t):
	r"WITH\sPARAMS"
	return t

def t_INITIAL_descscan_descid_ID(t):
	r"[_A-Za-z][_A-Za-z0-9-]*"
	if t.value in reserved:
		t.type = t.value
	elif t.value == 'OVER':
		t.type = 'FOR'
	else:
		t.type = 'ID'
	if t.lexer.lexstate == 'descscan':
		t.lexer.desc_id = True
	else:
		return t
	
def t_descscan_colon(t):
	':'
	t.lexer.lexpos = t.lexer.desc_start
	if t.lexer.desc_id:
		t.lexer.begin('descid')
	else:
		t.lexer.begin('descescapedwords')
		
def t_descid_colon(t):
	':'
	t.type = ':'
	t.lexer.begin('descwords')
	return t
	
def t_descescapedwords_colon(t):
	':'
	t.type = ':'
	t.lexer.begin('descwords')
	return t
	
def t_descscan_descwords_UNQUOTED_STRING(t):
	r"(?:[^)\\]*(?:\\.[^)\\]*)+|[^)\\]+(?:\\.[^)\\]*)*)"
	if t.lexer.lexstate == 'descscan':
		t.lexer.lexpos = t.lexer.desc_start
		t.lexer.begin('descwords')
	else:
		t.lexer.begin("INITIAL")
		return t

def t_ANY_newline(t):
	r"\n+"
	t.lexer.lineno += len(t.value)
	
def t_ANY_error(t):
	print("Illegal character '%s' on line %d" % (t.value[0], t.lexer.lineno))
	t.lexer.skip(1)

lexer = lex.lex()