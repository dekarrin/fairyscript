import os
import os.path

_language = None
_translator = None
_long_name = None
_language_strs = {}

_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
_default_lang = 'en'

def get_translator():
	global _translator
	return _translator

def get_language():
	global _language
	return _language
	
def get_language_name():
	global _long_name
	return _long_name
	
def get(index):
	global _language_strs
	if index in _language_strs:
		return _language_strs(index)
	else:
		return index
	
def set_language(lang):
	global _default_lang, _language_strs, _long_name, _translator, _language
	_long_name = None
	_language = None
	_translator = None
	_language_strs = {}
	lang = lang.lower()
	try:
		_load_langfile(lang)
		_language = lang
	except IOError:
		_load_langfile(_default_lang.lower())
		_language = _default_lang.lower()
	
def _load_langfile(lang):
	global _location, _long_name, _translator, _language_strs
	full_langfile = os.path.join(_location, lang + '.lang')
	with open(full_langfile, 'r') as langfile:
		config = True
		for line in langfile:
			line = line.strip()
			if line[0] == '#':
				continue
			parts = line.split('=', 1)
			name = parts[0].strip()
			value = parts[1].strip()
			if value.startswith('"') and value.endswith('"'):
				value = value[1:-1]
			if config:
				if name.lower() == 'name':
					_long_name = value
				elif name.lower() == 'translator':
					_translator = value
				else:
					config = False
			if not config:
				_language_strs[name] = value
	