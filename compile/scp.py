# contains various functions useful for getting information out ouf a .scp script tree

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