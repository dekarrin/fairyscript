import scryacc

def convert_to_renpy(input_string):
	parser = scryacc.parser
	result = parser.parse(input_string)
	return result