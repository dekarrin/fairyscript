import scrlex

def convert_to_renpy(input_string):
	scrlex.lexer.input(input_string)
	for tok in scrlex.lexer:
		if tok.type not in scrlex.literals and tok.type not in scrlex.reserved:
			print(tok.type + ": '" + tok.value + "'")
		else:
			print(tok.type)