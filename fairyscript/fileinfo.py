"""
Manage metadata on files and file objects. This module allows the metadata to be split from the file object itself.
"""
import sys


class FileInfo(object):
	"""
	Hold metadata about a file that was opened without actually including the file pointer itself.
	"""

	def __init__(self, mode, name=None, standard_stream=None):
		"""
		Create a new FileInfo object. If giving info on stderr, stdout, or stdin, the `name` argument is ignored and the
		`standard_stream` argument should be set to the name of the stream that the file object was opened on.

		:type name: str
		:param name: The name of the file. Can be a full path or just a filename. If `standard_stream` is set to a
		non-`None` value, this argument is ignored (a standard name will be used).
		:type mode: str
		:param mode: What mode the file was opened with at the time of access. Has the same arguments as the `mode`
		argument of the standard function `open()`.
		:type standard_stream: str
		:param standard_stream: The name of the standard stream that the file object was opened on. If set, must be one
		of 'stdin', 'stdout', or 'stderr' (not case-sensitive). If giving info on a regular file, the `standard_stream`
		argument should be set to `None` and the `name` argument should be set to the name of the file.
		"""
		self._mode = mode
		if standard_stream is not None:
			if not standard_stream.lower() in ['stderr', 'stdout', 'stdin']:
				raise ValueError("Bad value for standard_stream: '" + standard_stream)
			self._name = None
			self._standard_stream = standard_stream.lower()
		else:
			self._name = name
			self._standard_stream = None

	@property
	def name(self):
		"""
		Get the name of the file. If the file object was opened on a standard stream, this will be a standardized name
		of that stream. Note that the standardized name could also be a valid filename, so it should not be used to
		check if the file was opened on a standard stream; instead, the `is_stdX` functions should be used.

		:rtype: str
		:return: The name of the file.
		"""
		if self.is_stdin:
			return "<stdin>"
		elif self.is_stdout:
			return "<stdout>"
		elif self.is_stderr:
			return "<stderr>"
		else:
			return self._name

	@property
	def mode(self):
		"""
		Get the mode that the file object was opened with. Has the same structure as the `mode` property of a file
		object.

		:rtype: str
		:return: The mode.
		"""
		return self._mode

	@property
	def is_stderr(self):
		"""
		Check whether the file object was opened on stderr.

		:rtype: bool
		:return: Whether the file is stderr.
		"""
		return self._standard_stream == "stderr"

	@property
	def is_stdout(self):
		"""
		Check whether the file object was opened on stdout.

		:rtype: bool
		:return: Whether the file is stdout.
		"""
		return self._standard_stream == "stdout"

	@property
	def is_stdin(self):
		"""
		Check whether the file object was opened on stdin.

		:rtype: bool
		:return: Whether the file is stdin.
		"""
		return self._standard_stream == "stdin"

	@property
	def is_standard_stream(self):
		"""
		Check whether the file object was opened on a standard stream (stdout, stdin, or stderr).

		:rtype: bool
		:return: Whether the file is a standard stream.
		"""
		return self._standard_stream is not None


def from_file(file):
	"""
	Create a FileInfo object and populate it with metadata from the given file object.

	:param file: Any
	:param file: The file to create the metadata for.

	:rtype: FileInfo
	:return: The file metadata.
	"""
	if file == sys.stdin:
		return FileInfo(file.mode, standard_stream='stdin')
	elif file == sys.stdout:
		return FileInfo(file.mode, standard_stream='stdout')
	elif file == sys.stderr:
		return FileInfo(file.mode, standard_stream='stderr')
	else:
		return FileInfo(file.mode, name=file.name)
