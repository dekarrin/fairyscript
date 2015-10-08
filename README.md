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
* .SCP -> .DOCX (Word Office)

Stay tuned for more formats in the future!

### Installation
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

### Compiler Usage
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

### SCP: The Scrappy Language
The Scrappy language is designed to allow users to be as expressive as they
might be with a screenplay while still adhering to a regular language.

#### Language Basics
A manuscript written in Scrappy consists of a series of statements. These
statement can be broken down into the following types:
* Lines spoken by an actor or voiced internally
* Comments
* Instructions

In the Scrappy language, whitespace is unimportant. For readability,
instructions typically group together the start and ending characters along with
the actual instruction on a single line, but this is not necessary. Note that

```
[Scene: bobs-auto-shop]
```

is equivalent to

```
[Scene
:
bobs-auto-shop
]
```

In general, Scrappy is a case-sensitive language. There are only a few
exceptions to this, such as the names of instructions (which itself is excepted
in the ACTION directive, which uses the name of a character).

There may be times when a particular region of Scrappy code contains a character
that must be escaped (such as when a double quote character is used within a
string or a left-brace character is used within a python block). If that occurs,
simply escape the character with a backslash (\). Writing a literal backslash in
these situations requires escaping the backslash, so a double backslash is
needed (\\).

#### Lines
In Scrappy, a 'line' is a line of dialogue spoken by a character. It consists of
the character's name, followed by a colon, followed by what they are saying
enclosed within double quotes:

```
Mary: "Hello, John."
John: "Hiya, Mary. What's crackin'?"
```

To have the line be recited as internal dialogue, leave the name blank:

```
: "Heh-heh. No one knows I'm here!"
Mary: "I wonder where Bob has gone off to?"
: "Little does she realize, I'm standing behind her right now!"
```

If an actor's name contains spaces in it, it must also be enclosed in double
quotes:

```
John: "Well, I sure hope he shows up. We need him back at the office."
"Receptionist A": "I'm sure I saw him not too long ago!"
```

This works, and is valid Scrappy, but characters who's name contains a space
cannot be used with ACTION directives. Instead, it is better to define the
character in a characters file and use the mnemonic defined there to refer to
them in the main Scrappy manuscript for lines and ACTION directives.

#### Comments
Comments are used as supplementary information to the reader of the script.
Small notes and information about the script itself are often well-suited for
inclusion in a comment.

The '#' character begins a comment and it continues until the end of the line:

```
# This is a comment! This entire line is a comment!
(Flag: have_eaten) # But this comment doesn't start until a bit in to the line.
```

Comments are completely ignored when compiling Scrappy to another
machine-consumable language such as Ren'Py. They are not excluded from formats
that are intended to be read by humans, such as DOCX.

#### Instructions: Directives & Annotations
There are two types of insructions in Scrappy: directives and annotations. The
distinction between the two can seem a bit arbitrary, but the intent is to
separate screenplay instructions from computer instructions.

In general, directives represent instructions that would be intended for the
'crew' of a production, either to the actors themselves or to the
camera/lights/scenery/etc. Directives tend to result in a perceptual change for
the viewer.

Annotations are used for sending instructions to the engine powering the script.
They handle logic such as control flow, variable setting, and executing
arbitrary code, as well as ancillary functions such as marking sections of the
script. Annotations tend to result in a non-perceptual change, but they may
control the overall flow of the script.

An instruction begins with a particular character; for directives, it is the '['
character, and for annotations, it is the '(' character. The opening character
is followed by the name of the instruction immediately, with no spaces in
between. If there are any arguments to the instruction, they are given after a
colon. The instruction is then closed with the matching symbol; ']' for
directives and ')' for annotations. Whitespace is allowed before the closing
symbol.

The names of the instructions are not case-sensitive, with the exception of the
ACTION directive. This directive must be case-sensitive, as it uses the name of
the character for its 'name'.

##### CHOICE Directive
The CHOICE directive allows branching storylines to take place. The viewer is
presented with a series of options that they must select from, which each
contain at least the text of the option as well as the section to jump to upon
selection of that option:

```
[Choice]
* "Run away!": GO TO escape
* "Confront the problem.": GO TO problem-confrontation
```

