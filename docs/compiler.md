The FairyScript Compiler, Version 2.0.0
=======================================
This document is intended to be a complete reference to the compiler of the
FairyScript language. All information about the usage of the compiler is listed
here, including information common to all output formats as well as notes on
compiling to particular output formats.

## Table of Contents ##
1.  [Introduction](#introduction)
2.  [Basic Usage](#basic-usage)
3.  [Arguments](#arguments)
4.  [Options](#options)
5.  [Actions](#actions)
	1.  [Lexed Symbols](#lexed-symbols)
	2.  [Abstract Syntax Tree](#abstract-syntax-tree)
	3.  [DOCX](#docx)
	4.  [Ren'py](#ren-py)
	5.  [Static Analysis](#static-analysis)
	
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

## Arguments ##
The FairyScript compiler has only a single set of non-option arguments, and
that is the input files.

* `[INPUT_FILE, [INPUT_FILE...]]` - Gives the input files to process. As many
input files can be listed as is desired; input files will be processed in the
order that they are given and combined into a single output. If no input files
are given, the input is read from stdin.

## Options ##
The FairyScript compiler has a variety of options that are used to control its
behavior. This section covers options that apply to multiple compiler actions;
for options that apply only to a particular subcommand, please see the section
on that action in the [Actions](#actions) chapter.

* `--format <FMT>`, `-f <FMT>` - **Set the format of input files.** When this
option is set, all inputs are assumed to contain data in the given format.
There are three options for the format, `fey`, `lex`, and `ast`. `fey` is the
default when the `--format` option is not present, and indicates that the input
contains FairyScript code. `lex` indicates that the input contains a symbol
list from a previous lexing of FairyScript code, and parsing can continue from
that point rather than having to re-lex code. `ast` indicates that the input
contains abstract syntax trees from a previous parse, and that it can be used
to immediately compile to other formats without requiring additional parsing.

* `--logfile <FILE>`, `-l <FILE>` - **Write log to file.** When this option is
set, all log messages are written to a file. This file will contain every
single message generated during compilation, and is unaffected by the `-q`
option.

* `--output <FILE>`, `-o <FILE>` - **Write output to a file.** When this option
is enabled, the output will be written to the specified file. If this option is
not present, the output will instead be written to stdout. Note that all
warnings, errors, and messages during compilation are written to stderr, so
this will not interfere with the stdout output. Note further that due to the
structure of the DOCX format, it makes no sense to write to stdout, so this
option *must* be present when compiling to DOCX.

* `--quiet`, `-q` - **Suppress all warning output.** When this option is
enabled, all warnings and supplementary information from the compilation
process is not shown. Critical errors which cause compilation to abort will
still be shown, but only as a single line of information. All output is still
written to the log file.

## Actions ##
A variety of subcommands, also known as actions, are available to the
FairyScript compiler. Each one will cause the compiler to perform a slightly
different action, and have different options available to them.

### Lexed Symbols ###
Subcommand: `lex`.

Causes `fairyc` to run the lexer on the input(s) without parsing or compiling,
and to then output the lexed FairyScript tokens. These tokens can then later be
fed back into the compiler during future invocations by passing the format
option `-f lex` when specifying the lexed symbols as input.

The `lex` subcommand only accepts the `fey` or `lex` formats for its input; it
is not capable of 'deparsing' an abstract syntax tree back into a token list.

The following options are available when outputting lexed symbols:

* `--pretty` - **Output pretty-printed list of symbols.** When this option is
given, it causes the output to be formatted nicely in a more human-readable
format; however, this will result in a slightly larger file size. If not
present, the output will not be formatted with whitespace at all.

### Abstract Syntax Tree ###
Subcommand: `ast`.

Causes `fairyc` to parse the inputs into an abstract syntax tree without
compiling, and to then output it. Parsing to AST can be useful as it separates
the FairyScript syntax checking and parsing from the compilation itself. This
AST can then later be fed back into the compiler during future invocations by
passing the format option `-f ast` when specifying the AST as input.

The `ast` subcommand accepts all input formats.

The following options are available when outputting an abstract syntax tree:

* `--pretty` - **Output pretty-printed list of symbols.** When this option is
given, it causes the output to be formatted nicely in a more human-readable
format; however, this will result in a slightly larger file size. If not
present, the output will not be formatted with whitespace at all.

### DOCX ###
Subcommand: `docx`.

Causes `fairyc` to compile the inputs to a human-readable, natural language
screenplay-style document in Microsoft Office format. All FairyScript keywords
are converted to natural language equivalents, except in cases where it is not
possible (as in `PYTHON` annotations).

The names for the states of the actors are used as targets for saying how the
actor appears. Therefore, the names of the states need to be carefully chosen
if the DOCX output is to make syntactic sense in natural language.

The `docx` subcommand accepts all input formats.

The following options are available when outputting a DOCX file:

* `--exclude-flags` - **Exclude FLAG statements.** When this option is given,
`FLAG` annotations that are present in the original FairyScript will not be
shown in the outputted document. When this option is not present, `FLAG`
annotations will result in human-readable text that indicates that a flag is
modified.

* `--exclude-python` - **Exclude PYTHON content.** When this option is given,
`PYTHON` annotations that are present in the original FairyScript will have
their contents minimized such that the only text present in the outputted
document will be such that indicates that Python code was present. When this
option is not present, the entire contents of `PYTHON` annotations are preserved
in the final output.

* `--exclude-vars` - **Exclude VAR statements.** When this option is given,
`VAR` annotations that are present in the original FairyScript will not be
shown in the outputted document. When this option is not present, `VAR`
annotations will result in human-readable text that indicates that a variable
is modified.

* `--paragraph-spacing <PTS>` - **Set the spacing between paragraphs**. When
this option is set, sequences of paragraphs within a single character's set
of consecutive lines will be separated by the given number of points.
The default is to have no latent separation between paragraphs; separation
is only made between different characters' lines and/or other types script
directions.

* `--title <TITLE>` - **Set the title of the document**. When this option is
set, the given title will be used in the header of the outputted document. If
this option is not given, a default title will be used.


### Ren'Py ###
Subcommand: `renpy`.

Causes `fairyc` to compile the inputs to a Ren'Py-formatted script. All
FairyScript is converted to the equivalent Ren'Py statements where possible.

The `renpy` subcommand accepts all input formats.

The following options are available when outputting a Ren'Py script:

* `--default-destination <ID>` - **Set the default destination for movement.**
When this option is given, the default identifier for the destination of `EXIT`
and `ENTER` directives is set to the given identifier. The `EXIT` and `ENTER`
directives that do not have a `TO` clause in them will be compiled as though
they pointed to the given destination. If this option is not given, the default
destination is set to `center`.

* `--default-origin <ID>` - **Set the default origin for movement.** When this
option is given, the default identifier for the origin of `EXIT` and `ENTER`
directives is set to the given identifier. The `EXIT` and `ENTER` directives
that do not have a `FROM` clause in them will be compiled as though they started
from the given origin. If this option is not given, the default origin is set to
`center`.

* `--default-duration <SECS>` - **Set the default duration of directives.** When
this option is given, the default amount of time that motion takes is set to the
given number of seconds (which can be a fractional time). For the applicable
directives that do not specify a duration, they will be compiled as though they
specified the default duration. If this option is not given, the default
duration is set to `0.5`. This option applies to the following directives:
  * `ENTER` directives
  * `ACTION` directives
  * `EXIT` directives
  * `MUSIC` directives with a `FADEOUT OLD` clause or a `STOP` clause
  * `GFX` directives with a `STOP` clause
  * `SFX` directives with a `STOP` clause
  * `CAMERA` directives with a `ZOOM` action or `PAN` action.

* `--quick-speed <SECS>` - **Set the number of seconds to use for `QUICKLY`.**
When this option is present, it sets the number of seconds that the FairyScript
keyword `QUICKLY` is interpreted as. The number of seconds can be fractional. If
this option is not given, `QUICKLY` will be interpreted to be the default value
of `0.25`.

* `--slow-speed <SECS>` - **Set the number of seconds to use for `SLOWLY`.**
When this option is present, it sets the number of seconds that the FairyScript
keyword `SLOWLY` is interpreted as. The number of seconds can be fractional. If
this option is not given, `SLOWLY` is interpreted to be the default value of
`2.0`.

* `--tab-width <SPACES>` - **Set the width of tabs.** When this option is
present, the width of a single tab in the Ren'py script is set to the given
number of spaces. If this option is not given, tabs will default to being `4`
spaces wide.

* `--background-entity <ID>` - **Set the background for scene statements.** When
this option is present, the entity that is used for changing the scene in Ren'Py
is set to the given identifier. This is used when compiling `SCENE` directives.
If this option is not given, the entity will be set to the default value of
`bg`.

* `--enable-camera` - **Enable experimental camera system.** When this option is
present, the experimental ren'py camera system is used. This is an experimental
system and may not work properly. When this option is not present, `CAMERA`
directives are compiled to lines of internal dialog.


### Static Analysis ###
Subcommand: `analyze`.

Causes `fairyc` to analyze the input and provide information and statistics on
the identifiers, directives, and annotations in the FairyScript input. This is
compiled into a plain text format and output in a human-readable format.

The `analyze` subcommand accepts all input formats.

The following options are available when outputting static analysis results:

* `--order <ORDER>` - **Set the ordering of the lists.** When this option is
given, it specifies the order for each of the lists in the output. Each list
of names/identifiers used in the individual commands is affected by this option.
The order specified must be one of `usage` or `name`. `name` is the default and
causes the lists to be sorted in alphabetical order by name/identifier. `usage`
causes the lists to be sorted by the number of times each name/identifier is
used, with alphabetical being used as a secondary sort.
