scrappy
-------
Write manuscripts in screenplay style and export them to various formats.

![build-status](https://travis-ci.org/dekarrin/scrappy.svg?branch=master)

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

### Installation ###
To install scrappy to the system, do `python setup.py install`. This will make the
`scpcompile` command available on the system.

As a python script, scrappy does not need to be installed; simply having it
will allow it to be executed. However, scrappy does have some requirements:
* Python 2
* lxml, which can be installed from pip.
* ply, which can be installed from pip.

To execute it this way, without installing, run the local `scpcompile.py` (and
substitute executing this file with the `scpcompile` command found in the
documentation). Note that the above dependencies must first be resolved.

Scrappy also requires python-docx (for writing to Word documents). However, the
original codebase has been modified to support additional features that scrappy
requires, and so it is included in the scrappy codebase. For license information
on this package, please see the appropriate LICENSE file.

### Compiler Usage ###
The scrappy compiler is used to compile .SCP format manuscript files into other
file types. It is invoked by execution from the command line.

The typical usage of scrappy is to either compile .SCP files to prettier, more
human-readable formats or to compile .SCP files to executable scripts.

To compile an SCP manuscript to Ren'Py:

```shell
$ scpcompile renpy input_file.scp -o renpy_script.rpy
```

To compile an SCP manuscript to Microsoft Office:
```shell
$ scpcompile renpy input_file.scp -o my_script.docx --word
```

When invoked with no arguments, scrappy will read manuscript statements from 
stdin, compile them to Ren'Py script format, and then output them to stdout:

```shell
$ generate_scp | scpcompile renpy | process_output
```

Input files are specified by passing each as an argument; to specify multiple
input files, pass in multiple arguments. All input files are read in the order
that they are given. If no input files are given, scrappy will read from stdin.

In this example, three files are compiled to a single Ren'Py script:

```shell
$ scpcompile renpy main_path.scp branch1.scp branch2.scp -o my_script.rpy
```

The output file is specified with the `-o` option. Only one output file may be
specified. If the `-o` is not given, scrappy will write the output to stdout.
Note that due to the inherent limitations of the DOCX format, writing to stdout
is not permitted when compiling to Microsoft Word format.

Without any additional specification, scrappy will compile the input to Ren'Py
script format. This can be changed by changing the subcommand given. `renpy` is
used to specify Ren'Py, `docx` specifies DOCX format output, `lex` specifies
lexer symbols only, `ast` specifies outputting the abstract syntax tree without
compiling, and `analyze` performs static analysis on the code and outputs the
results as plain text.

By default, scrappy expects input to be in SCP manuscript format, but it can
also parse files that have already been lexed as well as compile abstract syntax
trees. Use the `-f` (long version `--format`) option to set the type of file
being processed. The argument to `-f` option must be `scp` for processing SCP
manuscript format, `lex` for processing lexed symbols directly, or `ast` for
processing abstract syntax trees.

The following example parses a file containing pre-lexed symbols and then
compiles the result to a Ren'Py format script:

```shell
$ scpcompile renpy -f lex script_symbols.lex -o my_script.rpy
```

In addition to the options listed above, there are many options that are
specific to the compiler for a particular format. For a full list of options,
invoke scrappy with the `-h` option:

```shell
$ scpcompile -h
```

### SCP: The Scrappy Language ###
The Scrappy Language is documented in full in the file
[scrappy.md](docs/scrappy.md) in the docs directory of scrappy.
