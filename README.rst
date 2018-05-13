FairyScript
-----------

Write manuscripts in screenplay style and export them to various
formats.

.. figure:: https://travis-ci.org/dekarrin/fairyscript.svg?branch=master
   :alt: build-status

Description
~~~~~~~~~~~

FairyScript provides a human-readable yet still regular format for
writing manuscripts in plaintext. These manuscripts can then be compiled
with fairyscript to various other formats, either for consumption by
other programs or for ease-of-use by humans.

There are three main values that FairyScript provides:

* Storing manuscripts as plaintext rather than as binary or XML-based files (such
  as those used by Microsoft Word) consumes less space.
* Using the .FEY format allows the manuscript to be compiled to other formats when
  necessary.
* The .FEY format provided by FairyScript is easier to read than formats that are
  directly used by manuscript execution systems, such as Ren’py.

Supported Formats
~~~~~~~~~~~~~~~~~

FairyScript provides the .FEY format for files. It is capable of
interpreting manuscripts written in this format, and compiling them to
the following formats:

* .FEY -> .RPY (Ren’py Script)
* .FEY -> .DOCX (Word Office)

Installation
~~~~~~~~~~~~

To install FairyScript to the system, do ``pip install fairyscript``.
This will make the ``fairyc`` command available on the system.

Requirements:

* Python (2.7, or 3.3 or later)
* lxml, which can be installed from pip.
* ply, which can be installed from pip.

To execute the FairyScript compiler from a local download without
installing it, run the local ``fairyc.py`` (and substitute executing
this file for the ``fairyc`` command found in the documentation). Note
that the above dependencies must first be resolved.

FairyScript also requires python-docx (for writing to Word documents).
However, the original codebase has been modified to support additional
features that FairyScript requires, and so it is included in the
FairyScript codebase. For license information on this package, please
see the appropriate LICENSE file.

Compiler Usage
~~~~~~~~~~~~~~

The FairyScript compiler (``fairyc``) is used to compile .FEY format
manuscript files into other file types. It is invoked by execution from
the command line.

The typical usage of ``fairyc`` is to either compile .FEY files to
prettier, more human-readable formats or to compile .FEY files to
executable scripts.

To compile a FEY manuscript to Ren’Py:

.. code:: shell

   $ fairyc renpy input_file.fey -o renpy_script.rpy

To compile a FEY manuscript to Microsoft Office:

.. code:: shell

   $ fairyc renpy input_file.fey -o my_script.docx --word

When invoked with no arguments, ``fairyc`` will read manuscript
statements from stdin, compile them to Ren’Py script format, and then
output them to stdout:

.. code:: shell

   $ generate_fey | fairyc renpy | process_output

Input files are specified by passing each as an argument; to specify
multiple input files, pass in multiple arguments. All input files are
read in the order that they are given. If no input files are given,
``fairyc`` will read from stdin.

In this example, three files are compiled to a single Ren’Py script:

.. code:: shell

   $ fairyc renpy main_path.fey branch1.fey branch2.fey -o my_script.rpy

The output file is specified with the ``-o`` option. Only one output
file may be specified. If the ``-o`` is not given, ``fairyc`` will write
the output to stdout. Note that due to the inherent limitations of the
DOCX format, writing to stdout is not permitted when compiling to
Microsoft Word format.

Without any additional specification, ``fairyc`` will compile the input
to Ren’Py script format. This can be changed by changing the subcommand
given. ``renpy`` is used to specify Ren’Py, ``docx`` specifies DOCX
format output, ``lex`` specifies lexer symbols only, ``ast`` specifies
outputting the abstract syntax tree without compiling, and ``analyze``
performs static analysis on the code and outputs the results as plain
text.

By default, ``fairyc`` expects input to be in FEY manuscript format, but
it can also parse files that have already been lexed as well as compile
abstract syntax trees. Use the ``-f`` (long version ``--format``) option
to set the type of file being processed. The argument to ``-f`` option
must be ``fey`` for processing FEY manuscript format, ``lex`` for
processing lexed symbols directly, or ``ast`` for processing abstract
syntax trees.

The following example parses a file containing pre-lexed symbols and
then compiles the result to a Ren’Py format script:

.. code:: shell

   $ fairyc renpy -f lex script_symbols.lex -o my_script.rpy

In addition to the options listed above, there are many options that are
specific to the compiler for a particular format. For a full list of
options, invoke ``fairyc`` with the ``-h`` option:

.. code:: shell

   $ fairyc -h

FEY: The FairyScript Language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The FairyScript Language is documented in full in the file
`fairyscript.md
<https://github.com/dekarrin/fairyscript/blob/master/docs/fairyscript.md>`__
in the docs directory of fairyscript.
