The Scrappy Language Reference
==============================

The Scrappy language is designed to allow users to be as expressive as they
might be with a screenplay while still adhering to a regular language.

## Language Basics ##
A manuscript written in Scrappy consists of a series of statements. These
statement can be broken down into the following types:
* Lines spoken by an actor or voiced internally
* Comments
* Instructions

### Whitespace ###
In the Scrappy language, whitespace is unimportant. For readability,
instructions typically group together the start and ending characters along with
the actual instruction on a single line, but this is not necessary.

```
[Scene: bobs-auto-shop]

# is equivalent to
		
[Scene
:
bobs-auto-shop
]
```

### Case-Sensitivity ###
In general, Scrappy is a case-sensitive language. There are only a few
exceptions to this, such as the names of instructions (which itself is excepted
in the ACTION directive, which uses the name of a character).

### Escaping ###
There may be times when a particular region of Scrappy code contains a character
that must be escaped (such as when a double quote character is used within a
string or a left-brace character is used within a python block). If that occurs,
simply escape the character with a backslash ('\'). Writing a literal backslash
in these situations requires escaping the backslash, so a double backslash is
needed ('\\').

### Types and Expressions ###
Scrappy has a system of types of parameters that are given to instructions. This
document will often refer to parameter types, and this section of this document
identifies exactly what is meant by each term.

Numbers are a series of digits. They can contain a decimal point, and can be
preceeded by a positive or negative sign. Numbers must always be written out
fully; scientific notation numbers are not allowed. In addition, numbers must
always be specified in decimal base; other bases are not allowed.

Strings are a series of characters. They are started and ended with a double
quote character ('"'). Any double quote characters inside the string must be
escaped.

Boolean literals specify whether something is true or false. In Scrappy, by far
the most common use for this is in setting the values of flags, and so Scrappy
uses the literal keywords `ON` and `OFF` (which must be in all-caps) to refer to
true and false, respectively.

Identifiers reference a particular thing. They are used for the names of
variables, flags, sections, characters, and more. Identifiers are
case-sensitive; two identifiers with the same spelling but different case refer
to two different things. Allowed characters in identifiers are underscores
('_'), hyphens ('-'), the letters A-Z (either upper or lower case), and the
digits 0-9; however, identifiers cannot start with a digit and they cannot be a
reserved word. Also, though hyphens are allowed in Scrappy identifiers, they
will be converted to underscores during compilation if the target language does
not support them.

Raw expressions are expressions that are contained between single quote
characters ('). They exist for when Scrappy does not support the expression
that is desired. Raw expressions are passed directly through to other languages
unchanged during compilation (unless Scrappy is being compiled to a
human-readable format), and so they may consist of any expression that is valid
in the target language. Because this could introduce reliance on a target
language, it is best to only use raw expressions when necessary.

Boolean expressions consist of any expression that may result in a true/false
value. They required for parameters that state a conditional, for example in
arguments to IF annotations or arguments to options of a CHOICE directive. In
Scrappy, boolean literals, raw expressions, and identifiers are all considered
valid boolean expressions.

Expressions are the most general type of a parameter. All other previously
mentioned types are considered valid expressions.

```
# Type examples (note: this is NOT valid Scrappy; it is only a demonstration of
# the different types!)

# Numbers:
4
5.2
+2.7
-2234.63

# Strings:
"Hi! This is a string."
"This a string with an escaped \" character."

# Boolean literals
ON
OFF

# Identifiers:
a
times_attacked
bobs-house-1

# Raw Expressions:
'times_attacked > 6'
'x + 9 < y'
'3542 >= 9'

# Boolean Expressions:
'times_attacked > 32'
have_seen_bob
OFF

# Expressions:
'hunger <= 5'
have_seen_john
ON
14
```

## Lines ##
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

## Comments ##
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

## Instructions: Directives & Annotations ##
There are two types of insructions in Scrappy: directives and annotations. The
intent of this separation is to provide a clear distinction between instructions
intended for the manuscript and instructions intended for the computer.

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
between. Most instructions require parameters; they are given after a colon 
character (':'). The instruction is then closed with the matching symbol; ']'
for directives and ')' for annotations. Whitespace is allowed before the closing
symbol.

```
# An ENTER directive with one instruction parameter, 'Bob'
[Enter: Bob]

# A FLAG annotation with two parameters, 'have_seen_bob', and 'ON'
(Flag: have_lost_bob ON)
```

The names of the instructions are not case-sensitive, with the exception of the
ACTION directive. This directive must be case-sensitive, as it uses the name of
the character for its 'name'. Note that case-insensitivity does not apply to the
parameters of instructions; reserved-word parameters must always be upper-case,
and mixing the cases of parameters that contain the names of things could result
in confusion.

```
# This annotation:
(FLAG: have_seen_bob ON)

# is the same as this one:
(flag: have_seen_bob ON)

# but this annotation uses a different case its variable, and so does not refer
# to the same one as above:
(Flag: Have_Seen_Bob ON)

# Now, there are two different flags, 'have_seen_bob' and 'Have_Seen_Bob'.

# This annotation has the wrong case for a reserved-word argument, and is thus
# not valid Scrappy:
(Flag: have_seen_bob on)
```

### CAMERA Directive ### <a name="camera-dir"></a>
The CAMERA Directive gives directions to the camera of the scene. It contains
a series of actions for the camera to do, separated by the `AND` keyword. Valid
camera actions are:
* Panning
* Snapping
* Zooming

Panning is a translation of the camera to point to a particular object/location.
To do a pan, use the `PAN TO` keywords followed by an identifier for the
location to pan to.

```
[Camera: PAN TO garage-door]
```

Snapping is similar to panning, but has no wait time; the camera jumps instantly
to the specified location. A snap is specified with the `SNAP TO` keywords.

```
[Camera: SNAP TO garage-door]
```

Zooming moves the camera closer or farther away from the scene. A zoom is
specified with the `ZOOM` keyword, followed by either `IN` or `OUT`.

```
[Camera: ZOOM IN]
[Camera: ZOOM OUT]
```

For zooming and panning, an amount of time for the action can be specified. The
duration of the action can be specified in seconds with the `OVER` or `FOR`
keyword followed by a number of seconds and then the `SECONDS` keyword, or a
relative duration by using `QUICKLY` or `SLOWLY`.

```
[Camera: ZOOM IN OVER 5 SECONDS]
[Camera: PAN TO front-door FOR 2.4 SECONDS]
[Camera: ZOOM OUT QUICKLY]
[Camera: ZOOM IN QUICKLY]
```

Actions can be chained in a single CAMERA directive by using the `AND` keyword.

```
[Camera: SNAP TO bedroom-door AND ZOOM IN QUICKLY AND
ZOOM OUT OVER 6 SECONDS AND PAN TO center SLOWLY]
```

### CHOICE Directive ### <a name="choice-dir"></a>
The CHOICE directive allows branching storylines to take place. The viewer is
presented with a series of options that they must select from. Upon selection of
an option, relevant flags are set and the script jumps to the appropriate
section.

In order to work properly, the section that an option points to must exist
somewhere in the completed script. Sections can be created either by using the
section parameter to a CHOICE directive or by using the SECTION annotation.

In Scrappy, the CHOICE directive is more limited than comparable structures in
other languages, such as `menu` in Ren'Py. Each option must jump to a section,
which is not required in the Ren'Py `menu` statement. However, this helps to
enforce simplicity of design within the code; CHOICE statements are kept short
and succinct rather than having the possibility of stretching into a very long
block.

A minimal CHOICE directive consists of `[Choice]` followed by a series of
options. Each option begins with an asterisk ('*') character and gives the text
of the option that is shown to the viewer, followed by a colon (':') and then
the keywords `GO TO` followed by the section that the option causes the script
to jump to upon selection.

```
[Choice]
* "Run away!": GO TO escape
* "Confront the problem.": GO TO problem-confrontation
```

A CHOICE directive may also mark the beginning of a new section. This is
accomplished by including a section name as part of the directive parameters:

```
[Choice: what-to-do]
* "Run away!": GO TO escape
* "Confront the problem.": GO TO problem-confrontation
```

This is equivalent to writing a SECTION annotation directly before the CHOICE
directive.

```
# This code is syntactically equivalent to the above example

(Section: what-to-do)

[Choice]
* "Run away!": GO TO escape
* "Confront the problem.": GO TO problem-confrontation
```

CHIOCE directives may also give a title for the choice, which is shown before
the options. This can be useful for displaying the question at the same time as
the options. The title is given as as string immediately after the directive
itself but before any choices.

```
[Choice]
"What should I do?"
* "Run away!": GO TO escape
* "Confront the problem.": GO TO problem-confrontation
```

Options in a choice can specify whether they have a condition for appearing,
which is done by including the key words `SHOW IF` followed by a flag variable
or other boolean expression immediately after the colon. The `SHOW IF`
parameter is separated from the rest of the option parameters by a comma (',').

```
[Choice]
* "I haven't seen him anywhere.": GO TO bob-is-missing
* "Ah, I saw him just a minute ago.": SHOW IF have_seen_bob, GO TO find-bob
* "Who cares about Bob, anyways?": GO TO bob-is-boring
```

Options may also specify flags and variables to set before jumping to their
associated section. This is done with the `SET` keyword, which is followed by
the variable/flag to set and then by what to set it to, which has the same rules
as in VAR annotations. Any number of flags/variables may be set by including
multiple `SET` clauses, separated by the keyword `AND`. `SET` clauses come after
the `SHOW IF` clause (if there is one) but before the `GO TO` clause, which is
separated from `SET` clauses with the `AND` keyword.

```
[Choice]
* "Who cares about Bob, anyways?":
SET have_dissed_bob AND GO TO bob-is-boring
* "Ah, I saw him just a minute ago.": SHOW IF have_seen_bob,
GO TO find-bob
* "(lie) Bob? No idea.": SHOW IF have_seen_bob,
SET have_lied ON AND GO TO bob-is-missing
* "Bob sucks. I'm the one who you should care about!":
SET have_dissed_bob ON AND SET arrogance 1 AND GO TO bob-is-missing
```

#### See Also ####
* [SECTION annotation](#section-ann)
* [VAR annotation](#var-ann)

