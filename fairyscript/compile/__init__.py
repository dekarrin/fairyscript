__all__ = ['renpy', 'word']


class CompilerError(Exception):
	def __init__(self, msg):
		super(Exception, self).__init__(msg)
