The FairyScript Language, Version 1.0
======================================
This document is intended to be a complete reference to the FairyScript
language. All information about the usage of the language is listed here.

## Table of Contents ##
1.  [Introduction](#introduction)
2.  [Language Basics](#language-basics)
	1.  [Whitespace](#whitespace)
	2.  [Case-Sensitivity](#case-sensitivity)
	3.  [Escaping](#escaping)
	4.  [Types](#types)
		1.  [Numbers](#numbers)
		2.  [Strings](#strings)
		3.  [Boolean Literals](#boolean-literals)
		4.  [Identifiers](#identifiers)
		5.  [Raw Expressions](#raw-expressions)
	5.  [Special Parameter Formats](#special-parameter-formats)
		1.  [Boolean Expressions](#boolean-expressions)
		2.  [Expressions](#expressions)
		3.  [Durations](#durations)
	6.  [Reserved Words](#reserved-words)
3.  [Lines](#lines)
4.  [Comments](#comments)
5.  [Instructions](#instructions)
	1.  [ACTION Directive](#action-directive)
	2.  [CAMERA Directive](#camera-directive)
	3.  [CHOICE Directive](#choice-directive)
	4.  [ENTER Directive](#enter-directive)
	5.  [EXIT Directive](#exit-directive)
	6.  [FMV Directive](#fmv-directive)
	7.  [GFX Directive](#gfx-directive)
	8.  [MUSIC Directive](#music-directive)
	9.  [SCENE Directive](#scene-directive)
	10. [SFX Directive](#sfx-directive)
	11. [CHARACTERS Annotation](#characters-annotation)
	12. [DESCRIPTION Annotation](#description-annotation)
	13. [DIALOG Annotation](#dialog-annotation)
	14. [END Annotation](#end-annotation)
	15. [EXECUTE Annotation](#execute-annotation)
	16. [FLAG Annotation](#flag-annotation)
	17. [GOTO Annotation](#goto-annotation)
	18. [IF Annotation](#if-annotation)
	19. [INCLUDE Annotation](#include-annotation)
	20. [PYTHON Annotation](#python-annotation)
	21. [SECTION Annotation](#section-annotation)
	22. [WHILE Annotation](#while-annotation)
	23. [VAR Annotation](#var-annotation)
6.  [Supplemental Files](#supplemental-files)
	1.  [Character Files](#character-files)
	2.  [GFX Bindings](#gfx-bindings)
7.  [Appendix: Syntax Reference](#appendix-syntax-reference)

## Introduction ##
The FairyScript language is an intermediate language for writing manuscripts.
It is designed to allow users to be as expressive as they might be with a
screenplay while still adhering to a regular language.

Manuscripts that are written in FairyScript are never executed. Instead, they
are compiled to another format using the FairyScript compiler. Because of this,
it is possible to create structures in FairyScript that can cause odd behavior
in target languages. However, the FairyScript compiler (`fairyc`) is designed
to be as flexible as possible. It will not attempt to check that a manuscript
makes sense in a target language; it only checks the FairyScript language
itself.

## Language Basics ##
A manuscript written in FairyScript consists of a series of statements. These
statement can be broken down into the following types:
- [Lines](#lines) spoken by an actor or voiced internally
- [Comments](#comments) to the reader of the manuscript
- [Instructions](#instructions) to the actors, crew, or engine

### Whitespace ###
In the FiaryScript language, whitespace is unimportant. For readability,
instructions typically group together the opening and closing characters along
with the name of the instruction on a single line, but this is not necessary.

```
[Scene: bobs-auto-shop]

# is equivalent to
		
[Scene
:
bobs-auto-shop
]
```

Note that whitespace between an instruction's opening character and the word
that identifies the instruction is not allowed.

```
# This is okay:
[Scene: bobs-auto-shop
]

# This is not okay:
[
Scene: bobs-auto-shop]
```

### Case-Sensitivity ###
In general, FairyScript is a case-sensitive language. There are only a few
exceptions to this, such as the names of instructions (which itself has an
exception in the ACTION directive, which uses the name of a character).

### Escaping ###
There may be times when a particular region of FairyScript code contains a
character that must be escaped (such as when a double quote character is used
within a string or a left-brace character is used within a PYTHON annotation).
If that occurs, the character can be escaped with a backslash (`\`). Writing a
literal backslash in these situations requires escaping the backslash, so a
double backslash is needed.

### Types ###
FairyScript has a system of types of parameters that are given to instructions.
This document will often refer to parameter types, and this section of this
document identifies exactly what is meant by each term.

#### Numbers ####
Numbers are a series of digits. They can contain a decimal point, and can be
preceeded by a positive or negative sign. Numbers must always be written out
fully; scientific notation numbers are not allowed. In addition, numbers must
always be specified in decimal base; other bases are not allowed.

```
# Number examples:

4
5.2
+2.7
-2234.63
```

#### Strings ####
Strings are a series of characters. They are started and ended with a double
quote character (`"`). Any double quote characters inside the string must be
escaped.

```
# String examples:

"Hi! This is a string."
"This a string with an escaped \" character."
```

#### Boolean Literals ####
Boolean literals specify whether something is true or false. In FairyScript, by
far the most common use for this is in setting the values of flags, and so
FairyScript uses the keywords `ON` and `OFF` to refer to true and false,
respectively.

```
# Boolean literal examples:

ON
OFF
```

#### Identifiers ####
Identifiers reference a particular object. They are used for the names of
variables, flags, sections, characters, and more.

In FairyScript, identifiers do not need to be defined before they are used. It
is possible that they will need to be defined before compiled output will be
valid (usually the case with a program-consumed output), but this can be solved
by [including](#include-annotation) a file in the target language that contains
the definitions. For information on which identifiers a target output format
requires to be defined, see the compiler notes for that output format.

Identifiers are case-sensitive; two identifiers with the same spelling but
different case refer to two different objects. Allowed characters in identifiers
are underscores (`_`), hyphens (`-`), the letters A-Z (either upper or lower
case), and the digits 0-9; however, identifiers cannot start with a digit and
they cannot be a reserved word. Also, though hyphens are allowed in FairyScript
identifiers, they will be converted to underscores during compilation if the
target language does not support them.

```
# Identifier examples:

a
times_attacked
bobs-house-1

# These two identifiers are distinct within FairyScript itself but might become
# the same when it is compiled:

bobs_house
bobs-house
```

#### Raw Expressions ####
Raw expressions are expressions that are contained between single quote
characters (`'`). They exist for when FairyScript does not support the
expression that is desired. Raw expressions are passed directly through to other
languages unchanged during compilation (unless FairyScript is being compiled to
a human-readable format), and so they may consist of any expression that is
valid in the target language. Because this could introduce reliance on a target
language, it is best to only use raw expressions when necessary.

```
# Raw expression examples:

'times_attacked > 6'
'x + 9 < y'
'3542 >= 9'

# This raw expression contains single quotes, which must be escaped:
'mappings[\'x\'] > 37'

# This raw expression is noticably dependent on having a compilation target of
# C# or a similar language. It could also be very difficult for non-coders to
# read. This is allowed in FairyScript, but should be avoided if possible:
'mappings.Where(x => x.Width > 2).Any(x => x.Height > 10)'
```

### Special Parameter Formats ###
Some instructions accept parameters that are of a particular format. These are
not strictly 'types', but rather a sequence of keywords or a set of allowable
types. These formats may be used throughout this document as shorthand for their
full definitions, which are listed in this section.

#### Boolean Expressions ####
A boolean expression consists of any expression that may result in a true/false
value. They are required for parameters that state a conditional, for example in
arguments to IF annotations or arguments to options of a CHOICE directive.
[Boolean literals](#boolean-literals), [raw expressions](#raw-expressions), and
[identifiers](#identifiers) are all considered valid boolean expressions.

If a raw expression is used as a boolean expression, it is the responsibility of
the author to ensure that it actually results in a boolean value. FairyScript
does not restrict the contents of raw expressions, but using a raw expression
that does not result in a boolean value may result in incorrect syntax in a
target language after compilation.

```
# Boolean expression examples:

have_seen_bob          # identifiers
OFF                    # boolean literals
'times_attacked > 32'  # raw expressions that appear to result in boolean values

# Raw expressions that appear to result in non-boolean values are considered
# valid boolean expressions in FairyScript, but using one might result in
# unexpected behavior once it has been compiled to another format:
'health + 6'
```

#### Expressions ####
Expressions are the most general type format of a parameter. All types listed in
the [Types section](#types) are considered valid expressions.

```
# Expression examples:

have_seen_john  # identifiers
ON              # boolean literals
14              # numbers
"Bob is lost"   # strings
'hunger <= 5'   # raw expressions that appear to result in boolean values
'health + 6'    # raw expressions that appear to result in non-boolean values
```

#### Durations ####
A duration is an amount of time. Some instructions allow a duration to be
specified to indicate how long the instruction should take to complete. If an
instruction accepts a duration, it will always be the last parameter.

Durations take on two forms. They can be an exact amount of time, given as a
number of seconds, or they can be a relative speed.

Durations that give an exact amount of time begin with either the keyword `FOR`
or the keyword `OVER`. The two keywords are interchangeable; whichever one reads
more naturally in context is the one that should be used. After the opening
keyword, the number of seconds is given, which can be made fractional with the
use of a decimal point. Finally, the unit of time can be given as the keyword
`SECONDS`, though this can be omitted if desired.

Durations that give a relative speed are given by using either one of the
keywords `QUICKLY` or `SLOWLY`. The exact meaning of each may depend on the
target language and compiler options.

```
# Duration examples:

# FOR and OVER are interchangeable, so the following two durations are the same:
FOR 6 SECONDS
OVER 6 SECONDS  

# If SECONDS is omitted, it is assumed
FOR 6.5
OVER 6.5

# The relative durations:
QUICKLY
SLOWLY
```

### Reserved Words ###
Some words used as part of the FairyScript language are known as reserved words.
Not all keywords in FairyScript are reserved; keywords that always come in sets,
such as `WITH` and `PARAMS`, are not reserved. Only the keywords that can occur
as single units are reserved. Identifiers cannot be a reserved word, but note
that they are not considered a reserved word if they contain the same letters as
a reserved word but with different capitalization.

The following is a list of all reserved words in FairyScript:
- `AND`
- `ALL`
- `AUTO`
- `BY`
- `DEC`
- `FOR`
- `FROM`
- `GO`
- `HIDE`
- `IN`
- `INC`
- `LOOP`
- `OFF`
- `ON`
- `OUT`
- `QUICKLY`
- `RETURN`
- `SECONDS`
- `SET`
- `SHOW`
- `SLOWLY`
- `STOP`
- `TO`
- `ZOOM`

## Lines ##
In FairyScript, a 'line' is a line of dialogue spoken by a character. It
consists of the character's name, followed by a colon, followed by what
they are saying enclosed within double quotes.

```
Mary: "Hello, John."
John: "Hiya, Mary. What's crackin'?"
```

To have the line be recited as internal dialogue, leave the name blank.

```
: "Heh-heh. No one knows I'm here!"
Mary: "I wonder where Bob has gone off to?"
: "Little does she realize, I'm standing behind her right now!"
```

If an actor's name contains spaces in it, it must also be enclosed in double
quotes.

```
John: "Well, I sure hope he shows up. We need him back at the office."
"Receptionist A": "I'm sure I saw him not too long ago!"
```

This works, and is valid FairyScript, but characters whose name contains a space
cannot be used with ACTION directives. Instead of using the name with quotes, it
is better to define the character in a [character file](#character-files) and
use the identifier defined there to refer to them in lines and ACTION
directives.

If desired, the appearance states of an actor can be listed in parentheses
before the colon that starts the actual line. Multiple states must be separated
by commas (`,`).

```
Mary (angry): "What have you done with Bob?"
John (angry, arms-cross): "I haven't done anything."
```

#### See Also ####
- [CHARACTERS Annotation](#characters-annotation)
- [Character Files](#character-files)

## Comments ##
Comments are used as supplementary information to the reader of the script.
Small notes and information about the script itself are often well-suited for
inclusion in a comment.

The `#` character begins a comment and it continues until the end of the line:

```
# This is a comment! This entire line is a comment!
(Flag: have_eaten) # But this comment doesn't start until part way in the line.
```

Comments are completely ignored when compiling FairyScript to another
machine-consumable language such as Ren'Py. They are not excluded from formats
that are intended to be read by humans, such as DOCX.

## Instructions ##
There are two types of instructions in FairyScript: directives and annotations.
The intent of this separation is to provide a clear distinction between
instructions intended for the manuscript and instructions intended for the
computer.

In general, directives represent instructions that would be intended for the
'crew' of a production, either to the actors themselves or to the
camera/lights/scenery/etc. Directives tend to result in a perceptual change for
the viewer.

Annotations are used for sending instructions to the engine powering the script.
They handle logic such as control flow, variable setting, and executing
arbitrary code, as well as ancillary functions such as marking sections of the
script. Annotations tend to result in a non-perceptual change, but they may
control the overall flow of the script.

An instruction begins with a particular character; for directives, it is the `[`
character, and for annotations, it is the `(` character. The opening character
is followed by the name of the instruction immediately, with no spaces in
between. Most instructions require parameters; they are given after a colon 
character (`:`). The instruction is then closed with the matching symbol; `]`
for directives and `)` for annotations. Whitespace is allowed before the closing
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
and mixing the cases of parameters that are [identifiers](#identifiers) could
result in confusion.

```
# This annotation:
(FLAG: have_seen_bob ON)

# is the same as this one:
(flag: have_seen_bob ON)

# but this annotation uses a different case for its variable, and so it does not
# refer to the same one as above:
(Flag: Have_Seen_Bob ON)

# Now, there are two different flags, 'have_seen_bob' and 'Have_Seen_Bob'.

# This annotation has the wrong case for a reserved-word argument, and is thus
# not valid FairyScript:
(Flag: have_seen_bob on)
```

### ACTION Directive ###
The ACTION Directive is an instruction to an actor to take some sort of action.
The action can be to move somewhere in the scene, to change appearance, or both.

This directive is unique among instructions in that it is not written by using
its name. Instead, the [identifier](#identifiers) of the actor that the
instruction is to is used as the 'name' of the instruction.

```
# This is an instruction for Bob to appear sad:
[Bob: sad]

# This is an instruction for Mary to appear sad:
[Mary: sad]

# This is only valid if there is a character named 'Action'!
[Action: sad]
```

To have an actor change their appearance, list the [identifiers](#identifiers)
for all the different ways in which they are to change, separated by commas
(`,`). Generally, there should not be more than one of a particular type of
appearance. That is to say, it is valid FairyScript to have an actor appear sad
and happy, but it certainly doesn't make any sense!

```
# An instruction for Bob to appear sad:
[Bob: sad]

# An instruction for Bob to appear sad with his back to the viewers:
[Bob: sad, back-turned]

# Valid FairyScript, but a bit confusing:
[Bob: sad, happy, back-turned]

# Makes a bit more sense:
[Bob: bittersweet, back-turned]
```

An actor can also be instructed to move somewhere on the screen. To do this, use
the `GO TO` keywords followed by an [identifier](#identifiers) for the
destination.

```
# An instruction for Bob to move to the right of the screen:
[Bob: GO TO stage-right]
```

For ACTION directives that include move instructions, an amount of time for the
move can be specified as a [duration](#durations).

```
[Bob: GO TO bedroom-door OVER 5 SECONDS]
[Bob: GO TO bed SLOWLY]
```

Appearance change instructions and movement instructions can be combined in a
single ACTION directive. In this case, the appearance instructions are separated
from the move instruction by a comma (`,`).

```
[Bob: sad, arms-crossed, GO TO bed SLOWLY]
```

Any actor can be given an ACTION directive; however, it would be very strange if
it is given to an actor who has not yet come on to the scene with an ENTER
directive.

#### See Also ####
- [ENTER directive](#enter-directive)

### CAMERA Directive ###
The CAMERA Directive gives directions to the camera of the scene. It contains
a series of actions for the camera to do, separated by the `AND` keyword. Valid
camera actions are:
- Panning
- Snapping
- Zooming

Panning is a translation of the camera to point to a particular object/location.
To do a pan, use the `PAN TO` keywords followed by an [identifier](#identifiers)
for the location to pan to.

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

For zooming and panning, an amount of time for the action can be specified as a
[duration](#durations).

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

### CHOICE Directive ###
The CHOICE directive allows branching storylines to take place. The viewer is
presented with a series of options that they must select from. Upon selection of
an option, relevant flags are set and the script jumps to the appropriate
section.

In order to work properly, the section that an option points to must exist
somewhere in the completed script. Sections can be created either by using the
section parameter to a CHOICE directive or by using the SECTION annotation.

In FairyScript, the CHOICE directive is more limited than comparable structures
in other languages, such as `menu` in Ren'Py. Each option must jump to a
section, which is not required in the Ren'Py `menu` statement. However, this
helps to enforce simplicity of design within the code; CHOICE statements are
kept short and succinct rather than having the possibility of stretching into a
very long block.

A minimal CHOICE directive consists of `[Choice]` followed by a series of
options. Each option begins with an asterisk (`*`) character and gives the text
of the option that is shown to the viewer, followed by a colon (`:`) and then
the keywords `GO TO` followed by the [identifier](#identifiers) for the section
that the option causes the script to jump to upon selection.

```
[Choice]
* "Run away!": GO TO escape
* "Confront the problem.": GO TO problem-confrontation
```

A CHOICE directive may also mark the beginning of a new section. This is
accomplished by including an [identifier](#identifiers) for a section name as
part of the instruction parameters.

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
the options. This can be useful for displaying a question at the same time as
the options. The title is given as a string immediately after the directive
itself but before any choices.

```
[Choice]
"What should I do?"
* "Run away!": GO TO escape
* "Confront the problem.": GO TO problem-confrontation
```

Options in a choice can specify whether they have a condition for appearing,
which is done by including the keywords `SHOW IF` followed by a flag variable or
other [boolean expression](#boolean-expressions) immediately after the colon.
The `SHOW IF` clause is separated from the rest of the option parameters by a
comma (`,`).

```
[Choice]
* "I haven't seen him anywhere.": GO TO bob-is-missing
* "Ah, I saw him just a minute ago.": SHOW IF have_seen_bob, GO TO find-bob
* "Who cares about Bob, anyways?": GO TO bob-is-boring
```

Options may also specify flags and variables to set before jumping to their
associated section. This is done with the `SET` keyword, which is followed by
the variable/flag to set and then by what to set it to, which has nearly the
same rules as in VAR annotations; unlike a VAR annotation, a value is required.
Any number of flags/variables may be set by including multiple `SET` clauses,
separated by the keyword `AND`. `SET` clauses come after the `SHOW IF` clause
(if there is one) but before the `GO TO` clause, which is separated from `SET`
clauses with the `AND` keyword.

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
- [SECTION annotation](#section-annotation)
- [VAR annotation](#var-annotation)

### ENTER Directive ###
The ENTER directive is used to instruct an actor to appear in the scene. There
are several different ways that the entrance can be customized.

To instuct an actor to appear on the scene, give the identifier of the actor as
a parameter to the instruction.

```
[Enter: Bob]
```

In order to specify the appearance of the actor, the appearance states can be
given in parentheses. Multiple appearance states are separated by commas (`,`).

```
[Enter: Bob (angry)]
[Enter: Bob (angry, with-arms-crossed)]
```

An actor's entrance can use a transition, such as fade or dissolve. To include a
transition in the entrance, use the identifier of the transition followed by the
keyword `IN`. Place this clause after any actor appearance states.

```
[Enter: Bob FADE IN]
[Enter: Bob (angry, with-arms-crossed) DISSOLVE IN]
```

To have an actor transition in with the previous object that used a transition
(such as a SCENE directive or another ENTER directive), use the keywords
`WITH PREVIOUS`.

```
# This causes Mary to fade in, then Bob to fade in after her entrance is
# complete:
[Enter: Mary FADE IN]
[Enter: Bob (angry) FADE IN]

# This causes Mary and Bob to fade in at the same time:
[Enter: Mary FADE IN]
[Enter: Bob (angry) WITH PREVIOUS]

# This causes Mary, Bob, and John to all fade in at the same time:
[Enter: Mary FADE IN]
[Enter: John (upset, eyes-closed) WITH PREVIOUS]
[Enter: Bob (angry) WITH PREVIOUS]
```

An actor's entrance can be given a particular path; they can be instructed to
come in to the scene from a particular side or at a particular location. To
specify the origin of the entrance path, use the `FROM` keyword followed by the
identifier for the location the path is to start at. Place this clause after any
actor appearance states and the transition (if there is one).

```
# Some entrance origins:
[Enter: Bob FROM offscreenleft]
[Enter: Mary (upset) FROM offscreenright]
[Enter: Ghost (angry, arms-crossed) DISSOLVE IN FROM center]
```

An ENTER directive can also be given the destination of an entrance. This will
be the final position that the actor is in after the entrance is complete. To
specify the destination of the entrance path, use the `TO` keyword followed by
the identifier for the location the path is to end at. Place this clause after
any actor appearance states, the transition (if there is one), and the origin
(if there is one).

```
# Some entrance destinations:
[Enter: Bob TO center]
[Enter: Mary (upset) FROM offscreenright TO stage-right]
[Enter: Ghost (angry, arms-crossed) DISSOLVE IN FROM center TO stage-left]
```

An ENTER directive can also be given a [duration](#durations) for the entrance.

```
# Some entrance destinations with explicit durations:
[Enter: Bob OVER 10 SECONDS]
[Enter: Mary (upset) FROM offscreenright TO stage-right SLOWLY]
[Enter: Ghost (angry, arms-crossed) DISSOLVE IN
	FROM center TO stage-left QUICKLY]
```

It is important to ensure that the order of operations of the entrance is
specified clearly. What the ENTER directive means is that the actor should enter
the scene with the given transition if there is one or appear instantly if there
is not one, at the specified origin if one is given, otherwise at an understood
origin. After the transition in is complete, the actor then moves to the
specified destination if there is one. If no origin is given but a destination
is given, the actor is to appear/transition to that location and not move at
all.

Note that this means that specififying an off-screen origin or an off-screen
destintation with no origin means that any transition will not be visible to the
viewer.

#### See Also ####
- [EXIT Directive](#exit-directive)
- [SCENE Directive](#scene-directive)

### EXIT Directive ###
The EXIT directive is an instruction to the actor to exit from the scene. There
are several different ways that the exit can be customized.

To instuct an actor to exit from the scene, give the identifier of the actor as
a parameter to the instruction.

```
[Exit: Bob]
```

An actor's exit can use a transition, such as fade or dissolve. To include a
transition in the exit, use the identifier of the transition followed by the
keyword `OUT`. Place this clause after the name of the actor.

```
[Exit: Bob FADE OUT]
```

To have an actor transition out with the previous object that used a transition
(such as another EXIT directive), use the keywords `WITH PREVIOUS`.

```
# This causes Mary to fade out, then Bob to fade out after her exit is complete:
[Exit: Mary FADE OUT]
[Exit: Bob FADE OUT]

# This causes Mary and Bob to fade out at the same time:
[Exit: Mary FADE OUT]
[Exit: Bob WITH PREVIOUS]

# This causes Mary, Bob, and John to all fade out at the same time:
[Exit: Mary FADE OUT]
[Exit: John WITH PREVIOUS]
[Exit: Bob WITH PREVIOUS]
```

An actor's exit can be given a particular path; they can be instructed to exit
from the scene at a particular side or at a particular location. To specify the
origin of the exit path, use the `FROM` keyword followed by the identifier for
the location the path is to start at. Place this after the transition (if there
is one).

```
# Some exit origins:
[Exit: Bob FROM stage-left]
[Exit: Mary FROM stage-right]
[Exit: Ghost DISSOLVE OUT FROM center]
```

An EXIT directive can also be given the destination of an exit. This will be the
final position that the actor is in before the exit occurs. To specify the
destination of the exit path, use the `TO` keyword followed by the identifier
for the location the path is to end at. Place this clause after the transition
(if there is one) and the origin (if there is one).

```
# Some exit destinations:
[Exit: Bob TO offscreenleft]
[Exit: Mary FROM stage-right TO offscreenright]
[Exit: Ghost DISSOLVE OUT FROM center TO stage-left]
```

An EXIT directive can also be given a [duration](#durations) for the exit.

```
# Some exit destinations with explicit duration:
[Exit: Bob OVER 10 SECONDS]
[Exit: Mary FROM stage-right TO offscreenright SLOWLY]
[Exit: Ghost DISSOLVE OUT FROM center TO stage-left QUICKLY]
```

It is important to ensure that the order of operations of the exit is specified
clearly. What the EXIT directive means is that the actor should first appear
instantly at the origin of the exit path if he is not already there, and then
move to the destination of the exit path. Finally, once there, they are to exit
the scene, either by using the given transition or by disappearing if no
transition is specified.

Note that this means that specififying an off-screen destination or an
off-screen origin with no destination means that any transition will not be
visible to the viewer.

#### See Also ####
- [ENTER Directive](#enter-directive)

### FMV Directive ###
The FMV directive gives a full-motion video (also referred to as 'cutscene')
that is to play. Script execution stops until the movie clip has completed
playing.

To play a full-motion video, give the name of it as a parameter to the
directive. This can be a string containing the name of the video file or the
identifier for the movie clip.

```
# The two forms of the FMV directive:
[FMV: intro-movie]
[FMV: "intro.mp4"]
```

### GFX Directive ###
The GFX directive is used to control visual (graphical) effects.

To show a visual effect that is intended to show once and then disappear
quickly, such as a white flash on the screen, give the identifier for that
visual effect as a parameter to the instruction.

```
[GFX: flash]
```

To specify that the visual effect is intended to start showing and remain
visible indefinitely, such as a shimmer effect in a mirage, use the `LOOP`
keyword before the effect identifier.

```
[GFX: LOOP shimmer]
```

To stop a particular effect that is looping, use the `STOP` keyword before the
name of the effect. To stop all currently looping visual effects, use the
keyword `ALL` instead of an effect identifer. If no target is given to the `STOP`
keyword, it is assumed to be `ALL`.

```
# Stop a particular visual effect:
[GFX: STOP shimmer]

# Stop all continuous visual effects currently being shown:
[GFX: STOP ALL]

# This is equivalent to the above statement:
[GFX: STOP]
```

Normally, the visual effect will disappear instantly when instructed to stop;
however, this can be changed by giving a [duration](#durations). The visual
effect will then take the given amount of time to fade away.

```
[GFX: STOP shimmer OVER 5 SECONDS]
[GFX: STOP ALL QUICKLY]
[GFX: STOP ALL SLOWLY]
```

#### See Also ####
- [SFX Directive](#sfx-directive)

### MUSIC Directive ###
The MUSIC directive is used to control the background music.

To change to a particular track of music, give the name of the song as a
parameter to the instruction. This can be a string containing the name of the
audio file or the identifier for the music track.

```
# The two forms of the MUSIC directive for playing a particular track:
[Music: main-theme]
[Music: "theme.mp3"]
```

To fade out any music currently playing before starting the new song, use the
`FADEOUT OLD` keywords.

```
# Both of the below instructions start a track after fading out the old music:
[Music: everyday-life FADEOUT OLD]
[Music: "everyday_life.mp3" FADEOUT OLD]
```

To stop playing music, use the `STOP` keyword before the name of the track. To
stop all music currently playing, use the keyword `ALL` instead of the name of
the song. If no target is given to the `STOP` keyword, it is assumed to be
`ALL`.

```
# Both of the below instructions stop a particular track:
[Music: STOP everyday-life]
[Music: STOP "everyday_life.mp3"]

# Both of the below instructions stop all music:
[Music: STOP ALL]
[Music: STOP]
```

Both music-stopping instructions and music-starting instructions that fade out
the already-playing music can be given a [duration](#durations) to specify how
long it takes to fade out the music.

```
# Some example MUSIC directives that use durations:
[Music: STOP everyday-life SLOWLY]
[Music: STOP ALL OVER 9.5 SECONDS]
[Music: STOP QUICKLY]
[Music: "everyday_life.mp3" FADEOUT OLD OVER 2 SECONDS]
[Music: everyday-life FADEOUT OLD SLOWLY]
```

#### See Also ####
- [SFX Directive](#sfx-directive)

### SCENE Directive ###
The SCENE directive specifies where the current scene is taking place. Any time
a SCENE directive is in a FairyScript manuscript, it indicates the start of a
new location, or at least a new sub-location within the current location.

To switch to a new scene, give the identifier for the scene to change to as a
parameter to the instruction.

```
[Scene: bobs-house]
```

Noramlly, the new scene is shown immediately. This can be changed by specifying
an identifier for a transition followed by the keyword `TO` before the name of
the new scene.

```
[Scene: FADE TO bobs-house]
```

#### See Also ####
- [ENTER Directive](#enter-directive)

### SFX Directive ###
The SFX directive is used to control sound effects.

To play a sound effect once, give the name of the sound effect as a parameter to
the instruction. The name can be a string containing the audio file to play or
the identifier of the sound effect.

```
[SFX: bang]
[SFX: "whack.wav"]
```

To specify that the sound effect is to loop indefinitely, use the `LOOP` keyword
before the sound name.

```
[SFX: LOOP sprinting-footsteps]
[SFX: LOOP "heavy_breathing.mp3"]
```

To stop a particular sound that is looping, use the `STOP` keyword before the
name of the sound. To stop all looping sound effects, use the keyword `ALL`
instead of the name of the sound. If no target is given to the `STOP` keyword,
it is assumed to be `ALL`.

```
[SFX: STOP sprinting-footsteps]
[SFX: STOP "heavy_breathing.mp3"]

# The following two directives are equivalent:
[SFX: STOP ALL]
[SFX: STOP]
```

Normally, the looping sound will stop instantly when instructed to stop;
however, this can be changed by giving a [duration](#durations). The sound
effect will then take the given amount of time to fade away.

```
[SFX: STOP sprinting-footsteps OVER 5 SECONDS]
[SFX: STOP "heavy_breathing.mp3" SLOWLY]
[SFX: STOP ALL QUICKLY]
[SFX: STOP SLOWLY]
```

### CHARACTERS Annotation ###
The CHARACTERS annotation is used to give the name of a file that contains
character definitions. This file contains information that is used for
formatting the characters during compilation.

To include a character file in the manuscript, give a string containing the path
to the file as a parameter to the instruction.

```
(Characters: "chars.csv")
```

The CHARACTERS annotation is a pre-processed annotation; all such annotations
are found and their character files read before compilation takes place. Then,
the list of character definitions is given to the compiler.

#### See Also ####
- [Character Files](#character-files)
- [INCLUDE Annotation](#include-annotation)

### DESCRIPTION Annotation ###
The DESCRIPTION annotation is used to provide a description about something.
Generally this is used after SCENE directives to describe to the manuscript
reader what the scene should look like, but it can be used to describe anything.

To provide a description of the last object that was introduced, give the
description as a parameter to the instruction. If the description begins with a
colon (`:`) character, it must be escaped by putting another colon in front of
it, or else the initial colon will not be displayed after compilation. If the
description contains a left parenthesis (`)`), it must be escaped by putting a
backslash character before it.

```
# A description of the current scene:
(Description: We see the office of John, Mary, and Bob. There are several
workstations, with a kitchen area in the corner.)

# This description must have its initial colon escaped with a second one:
(Description: ::This description starts with a colon.)

# This description must have the left parenthesis escaped with a backslash:
(Description: We see the office (of John, Mary, and Bob\). There are several
workstations, with a kitchen area in the corner.)

# This description must have its backslash escaped with a second one:
(Description: We see the contents of the file 'C:\\accounts.txt'.)
```

To indicate that the description is for a particular object, the identifier of
the object followed by a colon (`:`) is given before the description.

```
(Description: Bob: Bob is a larger man, about 6'2" tall. He looks to be about
thirty years old.)
```

If the identifier is to be omitted, but the first word of the description could
be an identifier followed by a colon, a colon can be written before the
description to indicate that there is no identifier.

```
# This describes 'Crying' as 'being sad. Laughing: being happy.', which is
# probably not the intent:
(Description: Crying: being sad. Laughing: being happy)

# Because an initial colon explitly marks the beginning of the description
# words, the description is now 'Crying: being sad. Laughing: being happy'
(Description: : Crying: being sad. Laughing: being happy)
```

### DIALOG Annotation ###
The DIALOG annotation controls the dialog window shown to the user. This is useful
for writing manuscripts for visual and kinetic novels.

To hide the dialog window, use the `HIDE` keyword.

```
(Dialog: HIDE)
```

To show the dialog window, use the `SHOW` keyword

```
(Dialog: SHOW)
```

To set the dialog window to automatically show and hide, use the `AUTO` keyword.

```
(Dialog: AUTO)
```

### END Annotation ###
The END annotation is used to mark the end of a section.

To mark the end of the current section, use the instruction without any
parameters.

```
(End)
```

If the current section is intended to be executed, and a value returned, use the
`RETURN` keyword followed by an [expression](#expressions) to return.

```
# Some example END annotations with return values:
(End: RETURN 5)
(End: RETURN "my_name")
(End: RETURN 'hunger + 2')
```

#### See Also ####
- [EXECUTE Annotation](#execute-annotation)
- [SECTION Annotation](#section-annotation)

### EXECUTE Annotation ###
The EXECUTE annotation is an instruction to go to a particular section, do
everything in it, and to then return to the instruction once complete.

To execute a section, give the identifier of the section as a parameter to the
instruction.

```
(Execute: afterschool-club-monday)
```

If the section being executed accepts arguments, these can be specified by using
the keywords `WITH PARAMS` after the section name, followed by the arguments.
Each section argument must be an [expression](#expressions), or, if the section
argument is a keyword argument, the name of the argument followed by an equals
(`=`) followed by an expression. Multiple section arguments must be separated by
comma characters (`,`).

```
# A single positional argument:
(Execute: shorten-life WITH PARAMS Bob)

# Multiple positional arguments:
(Execute: shorten-life WITH PARAMS Bob, 6)

# A single keyword argument:
(Execute: shorten-life WITH PARAMS target=Bob)

# Multiple keyword arguments:
(Execute: shorten-life WITH PARAMS target=Bob, amount=6)

# Mixed keyword / positional arguments:
(Execute: shorten-life WITH PARAMS Bob, amount=6)
```

#### See Also ####
- [SECTION Annotation](#section-annotation)
- [END Annotation](#end-annotation)
- [GOTO Annotation](#goto-annotation)

### FLAG Annotation ###
The FLAG annotation is used for setting and unsetting flag variables. This is
useful in interactive stories where something needs to occur depending on
whether a flag is set.

To set a flag's state, give the name of the flag as a parameter to the
instruction. If no other parameters are given, the flag is set to the 'on'
state, but a [boolean expression](#boolean-expressions) can be given for the
value of the flag instead.

```
# These statements are equivalent:
(Flag: have_seen_bob)
(Flag: have_seen_bob ON)

# This unsets a flag:
(Flag: have_seen_bob OFF)

# Some more examples:
(Flag: have_seen_bob 'knowledge > 10 && bob_affinity > 2')
(Flag: have_seen_bob have_followed_bob)
```

#### See Also ####
- [VAR Annotation](#var-annotation)

### GOTO Annotation ###
The GOTO annotation is an instruction to jump to a section.

To jump to a section, give the identifier of the section as a parameter to the
instruction.

```
(Goto: afterschool-club-monday)
```

If desired, a space can be inserted in between 'go' and 'to' in the instruction
name. Doing so may improve readability.

```
# The following two statements are equivalent:
(Goto: afterschool-club-monday)
(Go to: afterschool-club-monday)
```

#### See Also ####
- [SECTION Annotation](#section-annotation)
- [EXECUTE Annotation](#execute-annotation)
- [END Annotation](#end-annotation)

### IF Annotation ###
The IF annotation is used to perform actions only if a particular condition is
true. Multiple alternatives can be specified, each with their own conditions
and actions to perform.

To use the IF annotation, give a [boolean expression](#boolean-expressions) as
a parameter to the instruction, then after the instruction put the statements to
execute between braces (`{`, `}`).

```
(if: have_seen_bob)
{
	(Var: bobs_happiness DEC)
	Bob: "This guy saw me; I'm not sure how, though."
}
```

To specify an alternative set of actions to perform when the condition is not
true, the ELSE annotation can be used immediately after the closing brace of the
IF annotation, followed by its own actions in braces.

```
(If: have_seen_bob)
{
	(Var: bobs_happiness DEC)
	Bob: "This guy saw me; I'm not sure how, though."
}
(Else)
{
	(Var: bobs_happiness INC)
	Bob: "No one saw me, because I'm sneaky!"
}
```

To specify an alternative set of actions to perform when the initial condition
is not true, but which also has a different condition that must be true, the
ELSE IF annotation can be used. The name of the ELSE IF annotation can be given
as `elseif`, `else if` or `elif`; whichever one reads more naturally is the one
that should be used. As always, case does not matter for the instruction name.
Besides the name, the syntax of the ELSE IF annotation is identical to the IF
annotation.

```
(If: 'times_seen_bob > 10')
{
	(Var: bobs_happiness DEC BY 2)
	(Flag: have_super_stealth)
	Bob: "This guy has been stalking me like a tiger! You bet he saw me."
}
(Else If: 'times_seen_bob > 1')
{
	(Var: bobs_happiness DEC BY 2)
	Bob: "This guy saw me; I'm not sure how, though."
}
```

Multiple ELSE IF annotations can be chained for more cases. Each annotation's
actions will only be performed if its condition is checked and found to be true,
and its condition will only be checked if the previous annotation's condition is
not true. The first alternative whose condition is true is the one and only
alternative whose actions will be performed.

```
(If: 'times_seen_bob > 10')
{
	(Var: bobs_happiness DEC BY 3)
	(Flag: have_super_stealth)
	Bob: "This guy has been stalking me like a tiger! You bet he saw me."
}
(Elif: 'times_seen_bob > 5')       # 'elif' is the same as 'else if'
{
	(Var: bobs_happiness DEC BY 2)
	Bob: "We've run into each other a few times; I'm sure he's seen me."
}
(Elseif: 'times_seen_bob > 1')     # 'elseif' is the same as 'else if'
{
	(Var: bobs_happiness DEC)
	Bob: "This guy saw me; I'm not sure how, though."
}
```

An ELSE annotation may be placed at the end of any number of ELSE IF
annotations. Its actions are performed only if all previous conditions are
false.

```
(If: 'times_seen_bob > 10')
{
	(Var: bobs_happiness DEC BY 3)
	(Flag: have_super_stealth)
	Bob: "This guy has been stalking me like a tiger! You bet he saw me."
}
(Else If: 'times_seen_bob > 5')
{
	(Var: bobs_happiness DEC BY 2)
	Bob: "We've run into each other a few times; I'm sure he's seen me."
}
(Else If: 'times_seen_bob > 1')
{
	(Var: bobs_happiness DEC)
	Bob: "This guy saw me; I'm not sure how, though."
}
(Else)
{
	(Var: bobs_happiness INC)
	Bob: "No one saw me, because I'm sneaky!"
}
```

#### See Also ####
- [WHILE Annotation](#while-annotation)

### INCLUDE Annotation ###
The INCLUDE annotation specifies that the contents of another file should be
included at the location of the instruction.

To include a file whose contents are to be parsed as FairyScript code, give a
string containing the path to the file as a parameter to the instruction.

```
# include the file 'chapter2.fey' located in the current directory:
(Include: "chapter2.fey")

# include the file 'chapter2.fey' located in the 'files' directory of the
# current directory:
(Include: "files/chapter2.fey")
```

To specify that the file should only be included when compiling to a particular
format, use the keywords `FOR TARGET` followed by the identifier for the target
format. Multiple formats are separated with the `AND` keyword. The target
identifier is the same as the command line option required to compile to that
format; please see [compiler.md](compiler.md) for a complete list of target
formats supported by the FairyScript compiler.

```
# include the file 'chapter2.fey' when the script is compiled to DOCX format:
(Include: "chapter2.fey" FOR TARGET word)

# include the file 'chapter2.fey' when the script is compiled to DOCX format and
# when the script is compiled to Ren'Py format:
(Include: "chapter2.fey" FOR TARGET word AND renpy)
```

To specify whether the contents of the file are to be parsed as FairyScript
code, use the keywords `WITH PARSING` after the name of the file and after the
`FOR TARGET` clause if it exists. The `WITH PARSING` keywords are optionally
followed by either the keyword `ON` or the keyword `OFF`. If `ON` is given, the
contents of the included file will be parsed as FairyScript code and included
in the current file before compilation. If `OFF` is given, the contents of the
file are not parsed as FairyScript code and are instead placed unchanged in the
output during compilation. If neither keyword is given, `ON` is assumed.

```
# all three statements below will include chapter2.fey, parsed as FairyScript:
(Include: "chapter2.fey")
(Include: "chapter2.fey" WITH PARSING)
(Include: "chapter2.fey" WITH PARSING ON)

# include constants.rpy without modification in the compiled output:
(Include: "constants.rpy" WITH PARSING OFF)

# include constants.rpy without modification only when compiling to Ren'Py:
(Include: "constants.rpy" FOR TARGET renpy WITH PARSING OFF)
```

#### See Also ####
- [CHARACTERS Annotation](#characters-annotation)

### PYTHON Annotation ###
The PYTHON annotation gives python code that is to be executed.

This annotation is not recommended unless absolutely necessary, since it is
specific to compilation targets that can handle the execution of python code, or
that will display it to the reader.

To use the PYTHON annotation, write the annotation followed by python code
enclosed within braces (`{`, `}`). Any left brace character (`{`) within the
python code must be escaped with a backslash. Because the code within the braces
is python, spacing does matter there. Any initial whitespace that the lines of
code have in common will be stripped from each line before it is output.

```
(Python)
{
	for x in character:
		print x['name']
}
```

### SECTION Annotation ###
The SECTION annotation marks the start of section. This section can be jumped to
by using the GOTO and EXECUTE annotations.

To mark the start of a section, give an identifier for the current section as a
parameter to the instruction.

```
(Section: afterschool-club-monday)
```

The section can accept arguments that the EXECUTE annotation can pass in when
calling the section. Section arguments are specified by using the keywords `WITH
PARAMS` after the section name, followed by the arguments. Each section
argument must be an identifier, optionally followed by an equals (`=`) followed
by an [expression](#expressions) that is the default value of the section
argument. Multiple section parameters must be separated by commas (`,`).

```
# A single argument:
(Section: shorten-life WITH PARAMS target)

# Multiple arguments:
(Section: shorten-life WITH PARAMS target, amount)

# A single argument with a default value:
(Section: shorten-life WITH PARAMS target=Villain)

# Multiple arguments with default values:
(Section: shorten-life WITH PARAMS target=Villain, amount=10)

# Mixed arguments, one with a default value:
(Section: shorten-life WITH PARAMS target, amount=10)
```

If this section is intended to be called from an EXECUTE annotation, it is
important to mark where the section ends with the END annotation. Otherwise, the
section will never return.

#### See Also ####
- [END Annotation](#end-annotation)
- [EXECUTE Annotation](#execute-annotation)
- [GOTO Annotation](#goto-annotation)

### WHILE Annotation ###
The WHILE annotation is used to perform actions for as long as some condition is
true.

To use a WHILE annotation, pass a [boolean expression](#boolean-expressions) as
a parameter to the instruction for the condition. After the instruction, give
the statements to be performed between brace characters (`{`, `}`). The
statements between the braces will be performed as long as the conditional is
true (which will be never if the conditional is never true).

```
# Keep prompting the player to apologize to Bob until he feels better:
(While: 'bob_is_angry')
{
	Bob: "I am really upset right now!"
	
	(Choice)
	"Apologize to Bob?"
	* "Yes": SET bob_is_angry OFF AND GO TO after-choice
	* "No": GO TO after-choice
	
	(Section: after-choice)
}
```

#### See Also ####
- [IF Annotation](#if-annotation)

### VAR Annotation ###
The VAR annotation is used for setting the value of a variable. It can also be
used for setting the value of a flag, but it may be better to use the FLAG
annotation for that, as doing so may improve readability.

To set the value of a variable to a default value of the number 1, give the
identifier of the variable as a parameter to the instruction.

```
# Set the variable times_seen_bob to the default value of 1:
(Var: times_seen_bob)
```

Variables can also be increased or decreased by using the `INC` or `DEC`
keywords respectively after the name of the variable.

```
# Increase bobs_anger by 1:
(Var: bobs_anger INC)

# Decrease bobs_anger by 1:
(Var: bobs_anger DEC)
```

Normally, the variable is increased or decreased by 1; however, the amount to
change the variable by can be specified by using the `BY` keyword after `INC` or
`DEC`, followed by the amount.

```
# Increase bobs_anger by 4:
(Var: bobs_anger INC BY 4)

# Decrease bobs_anger by 0.4:
(Var: bobs_anger DEC BY 0.4)
```

To specify exactly what to set the variable to, give an [expression]
(#expressions) after the name of the variable instead of an `INC` or a `DEC`
clause.

```
# Set the variable bobs_anger to the result of a raw expression:
(Var: bobs_anger 'times_seen_bob / 2')

# Set the variable bobs_line to "Wait, what?"
(Var: bobs_line "Wait, what?")

# Set bobs_anger directly to 5.7:
(Var: bobs_anger 5.7)
```

## Supplemental Files ##
Sometimes, the information that can be provided using FairyScript is not quite
enough for compilation. In order to provide additional information, manuscripts
can specify supplemental files that contain the information needed.

The method for specifying the supplemental files depends on the type of file
being specified.

### Character Files ###
Character files contain information for characters in the manuscript. The
information is in a modified CSV format, with one character per line, and one
character attribute per field. Fields are separated by commas, and the values
of fields must be quoted.

Character files are included in a manuscript by using the
[CHARACTERS annotation](#characters-annotation). Multiple character files can be
included with multiple CHARACTERS annotations; any character that is defined
more than once across all included character files will be defined only by the
last definition. Placement of CHARACTERS annotation within the manuscript is
irrelevant; CHARACTERS annotations are pre-scanned before compilation.

Inside the character file, each character must have a field for the following
attributes, though it can have an empty field to specify the default value:
- The [identifier](#identifiers) of the character as it is used in the
manuscript. This cannot be blank.
- The name of the character; this is how the character will appear after
compilation. The default is the same as the identifier.
- A hex code that is the color of the character's label. This is what color
their name is after compilation. The default is black (#000000).

The following is an example of a character file:

```
"Bob",  "Billy-Bob Jr, III",    "#ff0000"
"Mary", "Marianne Johnson",     "#00ff00"
"John", ,                       "#0000ff"
"Boss", "Evil Overlord",
"Jim",  "James Samuel",         "#cccccc"
```

### GFX Bindings ###
GFX bindings, located in files external to the compiled manuscript, indicate to
the FairyScript compiler how to interpret a particular GFX identifier. This is
used for compilation to Ren'Py only.

GFX bindings must be in an external file that is brought in using the
[INCLUDE annotation](#include-annotation) that disables parsing. This must be a
Ren'Py-formatted file that defines all of the objects used in GFX statements.
The binding is then given as a specially-formatted comment, of the form:

`#: fairyscript-gfx <IDENTIFIER> <BINDING-TYPE>`

In this format, the identifier is the identifier to be used in `GFX` directives
and the binding type is one of `scene`, `image`, or `displayable`. The
identifier is case-sensitive; the rest of the statement is not case-sensitive.

Scene effects are applied to the entire scene in the list of the scene
transforms. 

Image effects are displayed by simply showing the image on the screen using the
GFX identifier as a transform. The image definition itself must also exist, and
have the same name as the identifier but with `_img` appended to it.

Displayable effects are displayed as-is with no additional modification, but
they cannot be looped.

For effects to be looped, there must be a definition identical to the effect
but with `_loop` appended to it. This combines with the image-bound GFX to
require a definition of identifier + `_loop_img`.

## Appendix: Syntax Reference ##
This is the complete grammar for FairyScript as denoted in a modified BNF syntax
that includes repetition markers and character classes from regular expression
syntax.

Please note that the actual grammar used by the parser is slightly different, as
it uses lexed symbols as terminals, which resolves any ambiguities introduced by
the grammar given here. Also, some of the names of the classes have been changed
to improve readability.

For the exact grammar that is used by the parser, please see the file `cfg.txt`
in the docs directory of FairyScript.

```
<manuscript>          ::= <block>

<block>               ::= <statement> <block>?							  

<statement>           ::= <directive>
                        | <annotation>
                        | <comment>
                        | <line>
                              
<comment>             ::= "#" .*

<directive>           ::= <scene>
                        | <enter>
                        | <action>
                        | <exit>
                        | <music>
                        | <gfx>
                        | <sfx>
                        | <fmv>
                        | <camera>
                        | <choice>

<annotation>          ::= <description>
                        | <section>
                        | <flag>
                        | <var>
                        | <dialog>
                        | <goto>
                        | <execute>
                        | <end>
                        | <while>
                        | <if>
                        | <include>
                        | <characters>
                        | <python>                              

<line>                ::= ( <id> | <string> )? ( "(" <appearance> ")" )? ":"
                            <string>                             

<scene>               ::= <scene-open> ":" <transition-to>? <id> "]"                            

<enter>               ::= <enter-open> ":" <id> ( "(" <appearance> ")" )?
                            <transition-in>? <motion>? "]"

<action>              ::= "[" <id> ":" <appearance> "]"
                        | "[" <id> ":" "GO" <destination> <duration>? "]"
                        | "[" <id> ":" <appearance> "," "GO" <destination>
                            <duration>? "]"

<exit>                ::= <exit-open> ":" <id> <transition-out>? <motion>? "]"

<music>               ::= <music-open> ":" "STOP" ( <name> | "ALL" )?
                            <duration>? "]"
                        | <music-open> ":" <name> ( "," "FADEOUT" <whitespace>
                            "OLD" <duration>? )? "]"

<gfx>                 ::= <gfx-open> ":" "LOOP"? <id> "]"
                        | <gfx-open> ":" "STOP" ( <id> | "ALL" )? <duration>?
                            "]"

<sfx>                 ::= <sfx-open> ":" "LOOP"? <name> "]"
                        | <sfx-open> ":" "STOP" ( <name> | "ALL" )? <duration>?
                            "]"

<fmv>                 ::= <fmv-open> ":" <name> "]"

<camera>              ::= <camera-open> ":" <camera-action> "]"

<choice>              ::= <choice-open> ( ":" <id> )? "]" <string>? <option>

<option>              ::= "*" <string> ":" ( "SHOW" <whitespace> "IF"
                            <boolean-expression> "," )? ( <varset> "AND" )? "GO"
                            <destination> <option>?

<varset>              ::= ( <varset> "AND" )? "SET" <id> ( <inc-dec> |
                            <expression> )

<description>         ::= <description-open> ":" ( <id>? ":" )?
                            <unquoted-string> ")"

<section>             ::= <section-open> ":" <id> ( "WITH" <whitespace> "PARAMS"
                            <param-declaration> )? ")"

<flag>                ::= <flag-open> ":" <id> <boolean-expression>? ")"

<var>                 ::= <var-open> ":" <id> ( <inc-dec> | <expression> )? ")"

<dialog>              ::= <dialog-open> ":" ( "HIDE" | "SHOW" | "AUTO" ) ")"

<goto>                ::= <goto-open> ":" <id> ")"

<execute>             ::= <execute-open> ":" <id> ( "WITH" <whitespace> "PARAMS"
                            <param-set> )? ")"

<end>                 ::= <end-open> ( ":" "RETURN" <expression> )? ")"

<while>               ::= <while-open> ":" <boolean-expression> ")" "{" <block>
                            "}"

<if>                  ::= <if-open> ":" <boolean-expression> ")" "{" <block> "}"
                            <else-if>? <else>?

<else-if>             ::= <else-if-open> ":" <boolean-expression> ")" "{"
                            <block> "}" <else-if>?

<else>                ::= <else-open> ")" "{" <block> "}"

<include>             ::= <include-open> ":" <string> ( "FOR" <whitespace>
                            "TARGET" <id-list> )? ( "WITH" <whitespace>
                            "PARSING" <boolean-literal>? )? ")"

<characters>          ::= <characters-open> ":" <string> ")"

<python>              ::= <python-open> ")" "{" <python-block> "}"

<python-block>        ::= <non-rbrace>* ( <backslash> . <non-rbrace>* )*

<transition-to>       ::= <id> "TO"

<transition-in>       ::= <id> "IN"
                        | "WITH" <whitespace> "PREVIOUS"

<transition-out>      ::= <id> "OUT"
                        | "WITH" <whitespace> "PREVIOUS"
                              
<appearance>          ::= ( <appearance> "," )? <id>

<motion>              ::= <origin> <destination>? <duration>?
                        | <destination> <duration>?
                        | <duration>
                              
<destination>         ::= "TO" <id>

<origin>              ::= "FROM" <id>

<duration>            ::= ( "FOR" | "OVER" ) <number> "SECONDS"?
                        | "QUICKLY"
                        | "SLOWLY"

<name>                ::= <string>
                        | <id>

<camera-action>       ::= <cam-instruction> ( "AND" <camera-action> )?

<cam-instruction>     ::= "SNAP" <whitespace> "TO" <id>
                        | "PAN" <whitespace> "TO" <id> <duration>?
                        | "ZOOM" ( "OUT" | "IN" ) <duration>?

<param-declaration>   ::= <id> ( "=" <expression> )? ( "," <param-declaration>
                            )?

<param-set>           ::= ( <id> "=" )? <expression> ( "," <param-set> )?

<boolean-literal>     ::= "OFF"
                        | "ON"

<boolean-expression>  ::= <boolean-literal>
                        | <raw-expression>
                        | <id>
                              
<expression>          ::= <boolean-expression>
                        | <string>
                        | <number>
                              
<inc-dec>             ::= ( "INC" | "DEC" ) ( "BY" <number> )?

<scene-open>          ::= "[" ( "S" | "s" ) ( "C" | "c" ) ( "E" | "e" ) ( "N" |
                            "n" ) ( "E" | "e" )

<enter-open>          ::= "[" ( "E" | "e" ) ( "N" | "n" ) ( "T" | "t" ) ( "E" |
                            "e" ) ( "R" | "r" )

<exit-open>           ::= "[" ( "E" | "e" ) ( "X" | "x" ) ( "I" | "i" ) ( "T" |
                            "t" )

<music-open>          ::= "[" ( "M" | "m" ) ( "U" | "u" ) ( "S" | "s" ) ( "I" |
                            "i" ) ( "C" | "c" )

<gfx-open>            ::= "[" ( "G" | "g" ) ( "F" | "f" ) ( "X" | "x" )

<sfx-open>            ::= "[" ( "S" | "s" ) ( "F" | "f" ) ( "X" | "x" )

<fmv-open>            ::= "[" ( "F" | "f" ) ( "M" | "m" ) ( "V" | "v" )

<camera-open>         ::= "[" ( "C" | "c" ) ( "A" | "a" ) ( "M" | "m" ) ( "E" |
                            "e" ) ( "R" | "r" ) ( "A" | "a" )

<choice-open>         ::= "[" ( "C" | "c" ) ( "H" | "h" ) ( "O" | "o" ) ( "I" |
                            "i" ) ( "C" | "c" ) ( "E" | "e" )

<description-open>    ::= "(" ( "D" | "d" ) ( "E" | "e" ) ( "S" | "s" ) ( "C" |
                            "c" ) ( "R" | "r" ) ( "I" | "i" ) ( "P" | "p" ) (
                            "T" | "t" ) ( "I" | "i" ) ( "O" | "o" ) ( "N" | "n" )

<section-open>        ::= "(" ( "S" | "s" ) ( "E" | "e" ) ( "C" | "c" ) ( "T" |
                            "t" ) ( "I" | "i" ) ( "O" | "o" ) ( "N" | "n" )

<flag-open>           ::= "(" ( "F" | "f" ) ( "L" | "l" ) ( "A" | "a" ) ( "G" |
                            "g" )

<var-open>            ::= "(" ( "V" | "v" ) ( "A" | "a" ) ( "R" | "r" )

<dialog-open>         ::= "(" ( "D" | "d" ) ( "I" | "i" ) ( "A" | "a" ) ( "L" |
                            "l" ) ( "O" | "o" ) ( "G" | "g" )

<goto-open>           ::= "(" ( "G" | "g" ) ( "O" | "o" ) <whitespace>? ( "T" |
                            "t" ) ( "O" | "o" )

<execute-open>        ::= "(" ( "E" | "e" ) ( "X" | "x" ) ( "E" | "e" ) ( "C" |
                            "c" ) ( "U" | "u" ) ( "T" | "t" ) ( "E" | "e" )

<end-open>            ::= "(" ( "E" | "e" ) ( "N" | "n" ) ( "D" | "d" )

<while-open>          ::= "(" ( "W" | "w" ) ( "H" | "h" ) ( "I" | "i" ) ( "L" |
                            "l" ) ( "E" | "e" )

<if-open>             ::= "(" ( "I" | "i" ) ( "F" | "f" )

<else-if-open>        ::= "(" ( "E" | "e" ) ( "L" | "l" ) ( ( "S" | "s" )
                            <whitespace>? ( "E" | "e" ) )? ( "I" | "i" ) ( "F" |
                            "f" )

<else-open>           ::= "(" ( "E" | "e" ) ( "L" | "l" ) ( "S" | "s" ) ( "E" |
                            "e" )

<include-open>        ::= "(" ( "I" | "i" ) ( "N" | "n" ) ( "C" | "c" ) ( "L" |
                            "l" ) ( "U" | "u" ) ( "D" | "d" ) ( "E" | "e" )

<characters-open>     ::= "(" ( "C" | "c" ) ( "H" | "h" ) ( "A" | "a" ) ( "R" |
                            "r" ) ( "A" | "a" ) ( "C" | "c" ) ( "T" | "t" ) (
                            "E" | "e" ) ( "R" | "r" ) ( "S" | "s" )

<id>                  ::= <alpha> ( <alphanumeric> | "-" )*

<id-list>             ::= ( <id-list> "AND" )? <id>

<string>              ::= '"' <non-dquote>* ( <backslash> . <non-dquote>* )* '"'

<number>              ::= ( ( "+" | "-" ) <whitespace>? )? <digit>+ ( "."
                            <digit>* )?

<unquoted-string>     ::= <non-rparen>* ( <backslash> . <non-rparen>* )*

<raw-expression>      ::= "'" <non-squote>* ( <backslash> . <non-squote>* )* "'"

<non-rbrace>          ::= [^ "}" <backslash> ]

<non-rparen>          ::= [^ ")" <backslash> ]

<non-dquote>          ::= [^ '"' <backslash> ]

<non-squote>          ::= [^ "'" <backslash> ]

<backslash>           ::= "\"

<whitespace>          ::= \s

<alphanumeric>        ::= <alpha> | <digit>

<digit>               ::= "0"
                        | "1"
                        | "2"
                        | "3"
                        | "4"
                        | "5"
                        | "6"
                        | "7"
                        | "8"
                        | "9"

<alpha>               ::= [ "A" - "Z" "a" - "z" "_" ]
```
