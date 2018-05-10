The Scrappy Compiler, Version 0.1
=================================
This document is intended to be a complete reference to the compiler of the
Scrappy language. All information about the usage of the compiler is listed
here, including information common to all output formats as well as
notes on compiling to particular output formats.

## Table of Contents ##
1.  [Introduction](#introduction)
2.  [Basic Usage](#basic-usage)
3.  [Options](#options)
4.  [Output Formats](#output-formats)
	1.  [Lexed Symbols](#lexed-symbols)
	2.  [Abstract Syntax Tree](#abstract-syntax-tree)
	3.  [DOCX](#docx)
	4.  [Ren'Py](#ren-py)
	
## Introduction ##
The Scrappy compiler is used for converting Scrappy manuscripts into other
formats. It is invoked from the command line using Python. The compiler has a
requirement for lxml; this must be installed for the compiler to function
properly.

## Basic Usage ##
The most basic usage of the compiler is to take a single input file and compile
its contents to an output file. The input file is specified by passing it in as
an argument and the output file is specified with the `-o` option. By default,
the input file is assumed to contain Scrappy code.

```shell
# Compiles the Scrappy manuscript 'chapter1.scp' to the Ren'Py script
'chapter1.rpy':

scpcompile renpy chapter1.scp -o chapter1.rpy
```

Multiple input files can be specified by using multiple arguments.

```shell
# Compiles three Scrappy manuscripts into a single Ren'Py script:

scpcompile renpy chap1.scp chap2.scp chap3.scp -o my_story.rpy
```

If no non-option arguments are given, the input is read from stdin instead of
from a file.

```shell
# Compiles Scrappy code from stdin to a Ren'Py script:

scpcompile renpy -o my_visual_novel.rpy < scrappy_code.scp
```

Similarly, if no `-o` is given, the compiled code is written to stdout instead
of to a file.

```shell
# Compiles Scrappy code from a file and writes the Ren'Py code to stdout:

scpcompile renpy chap1.scp > my_story.rpy
```

All messages, warnings, and errors from the compiler are printed to stderr, so
they will not interfere with the output if it is printed to stdout.

## Options ##
The Scrappy compiler has a variety of options that are used to control its
behavior. This section covers options that apply to multiple output formats; for
options that apply only to a particular output format, please see the section on
that format in the [Output Formats](#output-formats) chapter.
