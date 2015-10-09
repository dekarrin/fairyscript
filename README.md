scrappy
-------
Write manuscripts in screenplay style and export them to various formats.

### Description ###
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

### Supported Formats ###
Scrappy provides the .SCP format for files. It is capable of interpreting
manuscripts written in this format, and compiling them to the following formats:
* .SCP -> .RPY (Ren'py Script)
* .SCP -> .DOCX (Word Office)

Stay tuned for more formats in the future!

### Installation ###
As a python script, scrappy does not need to be installed; simply having it
will allow it to be executed. However, scrappy does have some requirements:
* Python 2
* lxml, which can often be installed from repositories on Unix-based systems and
can be installed from binaries on Windows.

Scrappy also requires PLY (for parsing files) and python-docx (for writing to
Word documents). However, both of these packages have been included in the
scrappy distribution for convenience. In the case of python-docx, the original
codebase has been modified to support additional features that scrappy requires,
and so it is necessary even if python-docx is already installed. Again, it is
included as part of the distribution, and so no action is necessary in order to
properly install it. For license information on these packages, please see the
appropriate LICENSE files.

### Compiler Usage ###
The scrappy compiler is used to compile .SCP format manuscript files into other
file types. It is invoked by execution from the command line.

The typical usage of scrappy is to either compile .SCP files to prettier, more
human-readable formats or to compile .SCP files to executable scripts.

To compile an SCP manuscript to Ren'Py:

```shell
$ python scrappy.py -i input_file.scp -o renpy_script.rpy
```

To compile an SCP manuscript to Microsoft Office:
```shell
$ python scrappy.py -i input_file.scp -o my_script.docx --word
```

When invoked with no arguments, scrappy will read manuscript statements from 
stdin, compile them to Ren'Py script format, and then output them to stdout:

```shell
$ generate_scp | python scrappy.py | process_output
```

Input files are specified with the `-i` option; to specify multiple input files,
pass in multiple `-i` options. All `-i` options are read in the order that they
are given. If no `-i` option is given, scrappy will read from stdin.

In this example, three files are compiled to a single Ren'Py script:

```shell
$ python scrappy.py -i main_path.scp -i branch1.scp -i branch2.scp -o my_script.rpy
```

The output file is specified with the `-o` option. Only one output file may be
specified. If the `-o` is not given, scrappy will write the output to stdout.
Note that due to the inherent limitations of the DOCX format, writing to stdout
is not permitted when compiling to Microsoft Word format.

Without any additional specification, scrappy will compile the input to Ren'Py
script format. This can be changed with the use of one of the output format
flags. `--renpy` (short option `-r`) can be used to explicitly specify Ren'Py,
`--word` (short option `-w`) specifies DOCX format output, `-lex` (short option
`-l`) specifies lexer symbols only, and `--ast` specifies outputting the
abstract syntax tree without compiling.

By default, scrappy expects input to be in SCP manuscript format, but it can
also parse files that have already been lexed as well as compile abstract syntax
trees. Use the `-f` (long version `--inputformat`) option to set the type of
file being processed. The argument to `-f` option must be `scp` for processing
SCP manuscript format, `lex` for processing lexed symbols directly, or `ast` for
processing abstract syntax trees.

The following example parses a file containing pre-lexed symbols and then
compiles the result to a Ren'Py format script:

```shell
$ python scrappy.py -f lex -i script_symbols.lex -o my_script.rpy
```

In addition to the options listed above, there are many options that are
specific to the compiler for a particular format. For a full list of options,
invoke scrappy with the `-h` option:

```shell
$ python scrappy.py -h
```

### SCP: The Scrappy Language ###
The Scrappy Language is documented in full in the file `scrappy.md` in the docs
directory of scrappy.