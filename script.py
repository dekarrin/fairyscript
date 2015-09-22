import scrlex

def convert_to_renpy(input_string):
	scrlex.lexer.input(input_string)
	for tok in lexer:
		print(tok)