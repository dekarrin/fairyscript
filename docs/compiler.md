The FairyScript Compiler, Version 2.0.0
=======================================
This document is intended to be a complete reference to the compiler of the
FairyScript language. All information about the usage of the compiler is listed
here, including information common to all output formats as well as notes on
compiling to particular output formats.

## Table of Contents ##
1.  [Introduction](#introduction)
2.  [Basic Usage](#basic-usage)
3.  [Options](#options)
4.  [Actions](#actions)
	1.  [Lexed Symbols](#lexed-symbols)
	2.  [Abstract Syntax Tree](#abstract-syntax-tree)
	3.  [DOCX](#docx)
	4.  [Ren'Py](#ren-py)
	5.  [Static Analysis](#analysis)
	
## Introduction ##
The FairyScript compiler is used for converting FairyScript manuscripts into
other formats. It is invoked from the command line using `fairyc`. The compiler
has a requirement for lxml; this must be installed for the compiler to function
properly. All requirements can be satisfied automatically by pip during the
install process.

## Basic Usage ##
The most basic usage of the compiler is to use the `renpy` action to take a
single input file and compile its contents to an output file. The input file
is specified by passing it in as an argument and the output file is specified
with the `-o` option. By default, the input file is assumed to contain
FairyScript code.

```shell
# Compiles the FairyScript manuscript 'chapter1.fey' to the Ren'Py script
'chapter1.rpy':

fairyc renpy chapter1.fey -o chapter1.rpy
```

Multiple input files can be specified by using multiple arguments.

```shell
# Compiles three FairyScript manuscripts into a single Ren'Py script:

fairyc renpy chap1.fey chap2.fey chap3.fey -o my_story.rpy
```

If no non-option arguments are given, the input is read from stdin instead of
from a file.

```shell
# Compiles FairyScript code from stdin to a Ren'Py script:

fairyc renpy -o my_visual_novel.rpy < fairyscript_code.fey
```

Similarly, if no `-o` is given, the compiled code is written to stdout instead
of to a file.

```shell
# Compiles FairyScript code from a file and writes the Ren'Py code to stdout:

fairyc renpy chap1.fey > my_story.rpy
```

All messages, warnings, and errors from the compiler are printed to stderr, so
they will not interfere with the output if it is printed to stdout.

## Options ##
The FairyScript compiler has a variety of options that are used to control its
behavior. This section covers options that apply to multiple compiler actions; for
options that apply only to a particular output format, please see the section on
that format in the [Output Formats](#output-formats) chapter.
