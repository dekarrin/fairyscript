## scrappy
----------
Write manuscripts in screenplay style and export them to various formats.

### Description
Scrappy, the SCRipt APplication written in PYthon, provides a human-readable yet
still regular format for writing manuscripts in plaintext. These manuscripts can
then be compiled with scrappy to various other formats, either for consumption
by other programs or for ease-of-use by humans.

There are three main values that scrappy provides:
* Storing manuscripts as plaintext rather than as binary or XML-based files
(such as those used by Microsoft Word) consumes less space.
* Using the .SCP format allows the manuscript to be compiled to other formats
when necessary.
* The .SCP format provided by scrappy is easier to read than formats that are
directly used by manuscript execution systems, such as Ren'py.

### Supported Formats
Scrappy provides the .SCP format for files. It is capable of interpreting
manuscripts written in this format, and compiling them to the following formats:
* .SCP -> .RPY (Ren'py Script)