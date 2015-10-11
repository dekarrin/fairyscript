The Scrappy Language Reference
==============================
This document is intended to be a complete reference to Scrappy language. All
information about the usage of the language is listed here.

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

## Introduction ##
The Scrappy language is an intermediate language for writing manuscripts. It is
designed to allow users to be as expressive as they might be with a screenplay
while still adhering to a regular language.

Manuscripts that are written in Scrappy are never executed. Instead, they are
compiled to another format using the Scrappy compiler. Because of this, it is
possible to create structures in Scrappy that can cause odd behavior in target
languages. However, Scrappy is designed to be as flexible as possible. It will
not attempt to check that a manuscript makes sense in a target language; only
the Scrappy language itself.

## Language Basics ##
A manuscript written in Scrappy consists of a series of statements. These
statement can be broken down into the following types:
- Lines spoken by an actor or voiced internally
- Comments
- Instructions

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
simply escape the character with a backslash (`\`). Writing a literal backslash
in these situations requires escaping the backslash, so a double backslash is
needed.

### Types ###
Scrappy has a system of types of parameters that are given to instructions. This
document will often refer to parameter types, and this section of this document
identifies exactly what is meant by each term.

#### Numbers ####
Numbers are a series of digits. They can contain a decimal point, and can be
preceeded by a positive or negative sign. Numbers must always be written out
fully; scientific notation numbers are not allowed. In addition, numbers must
always be specified in decimal base; other bases are not allowed.

```
# Number examples (note: these are valid numbers, but this is NOT valid Scrappy
# as-is):

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
# String examples (note: these are valid strings, but this is NOT valid Scrappy
# as-is):

"Hi! This is a string."
"This a string with an escaped \" character."
```

#### Boolean Literals ####
Boolean literals specify whether something is true or false. In Scrappy, by far
the most common use for this is in setting the values of flags, and so Scrappy
uses the literal keywords `ON` and `OFF` (which must be in all-caps) to refer to
true and false, respectively.

```
# Boolean literal examples (note: these are valid boolean literals, but this is
# NOT valid Scrappy as-is):

ON
OFF
```

#### Identifiers ####
Identifiers reference a particular thing. They are used for the names of
variables, flags, sections, characters, and more. Identifiers are
case-sensitive; two identifiers with the same spelling but different case refer
to two different things. Allowed characters in identifiers are underscores
(`_`), hyphens (`-`), the letters A-Z (either upper or lower case), and the
digits 0-9; however, identifiers cannot start with a digit and they cannot be a
reserved word. Also, though hyphens are allowed in Scrappy identifiers, they
will be converted to underscores during compilation if the target language does
not support them.

```
# Identifier examples (note: these are valid identifiers, but this is NOT valid
# Scrappy as-is):

a
times_attacked
bobs-house-1

# These two identifiers are distinct within Scrappy itself but might become the
# same when it is compiled:

bobs_house
bobs-house
```

#### Raw Expressions ####
Raw expressions are expressions that are contained between single quote
characters (`'`). They exist for when Scrappy does not support the expression
that is desired. Raw expressions are passed directly through to other languages
unchanged during compilation (unless Scrappy is being compiled to a
human-readable format), and so they may consist of any expression that is valid
in the target language. Because this could introduce reliance on a target
language, it is best to only use raw expressions when necessary.

```
# Raw expression examples (note: these are valid raw expressions, but this is
# NOT valid Scrappy as-is):

'times_attacked > 6'
'x + 9 < y'
'3542 >= 9'

# This raw expression contains single quotes, which must be escaped:
'mappings[\'x\'] > 37'

# This raw expression is noticably dependent on having a compilation target of
# C# or a similar language. It could also be very difficult for non-coders to
# read. This is allowed in Scrappy, but should be avoided if possible:
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
the author to ensure that it actually results in a boolean value. Scrappy does
not check the contents of raw expressions, but using a raw expression that does
not result in a boolean value may result in incorrect syntax in a target
language.

```
# Boolean expression examples (note: these are valid boolean expressions, but
# this is NOT valid Scrappy as-is):

have_seen_bob          # identifiers
OFF                    # boolean literals
'times_attacked > 32'  # raw expressions that appear to result in boolean values

# Raw expressions that appear to result in non-boolean values are considered
# valid boolean expression by Scrappy, but using one might result in unexpected
# behavior once it has been compiled to another format:
'health + 6'
```

#### Expressions ####
Expressions are the most general type format of a parameter. All types listed in
the [Types section](#types) are considered valid expressions.

```
# Expression examples (note: these are valid expressions, but this is NOT valid
# Scrappy as-is):

have_seen_john  # identifiers
ON              # boolean literals
14              # numbers
"Bob is lost"   # strings
'hunger <= 5'   # raw expressions that appear to result in boolean values
'health + 6'    # raw expressions that appear to result in non-boolean values
```

#### Durataions ####
A duration is an amount of time. Some instructions allow a duration to be
specified to indicate how long the instruction should take to complete. If an
instruction accepts a duration, it will always be the last parameter.

Durations take on two forms. They can be an exact amount of time, given as a
number of seconds, or they can be a relative speed.

Durations that give an exact amount of time begins with either the keyword `FOR`
or the keyword `OVER`. The two keywords are interchangeable; whichever one reads
more naturally in context is the one that should be used. After the opening
keyword, the number of seconds is given, which can be made fractional with the
use of a decimal point. Finally, the unit of time can be given as the keyword
`SECONDS`, though this can be omitted if desired.

Durations that give a relative speed are given by using one of the keywords
`QUICKLY` or `SLOWLY`. The exact meaning of each may depend on the target
language and compiler options.

```
# Duration examples (note: these are valid durations, but this is NOT valid
# Scrappy as-is):

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

The `#` character begins a comment and it continues until the end of the line:

```
# This is a comment! This entire line is a comment!
(Flag: have_eaten) # But this comment doesn't start until a bit in to the line.
```

Comments are completely ignored when compiling Scrappy to another
machine-consumable language such as Ren'Py. They are not excluded from formats
that are intended to be read by humans, such as DOCX.

## Instructions ##
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

### ACTION Directive ###
The ACTION Directive is an instruction to an actor to take some sort of action.
The action can be to move somewhere in the scene, to change appearance, or both.

This directive is unique among instructions in that it is not written by using
its name. Instead, the name of the actor that the instruction is to is used as
the 'name' of the instruction.

```
# This is an instruction for Bob to appear sad:
[Bob: sad]

# This is an instruction for Mary to appear sad:
[Mary: sad]

# This is only valid if there is a character named 'Action'!
[Action: sad]
```

To have an actor change their appearance, list all the different ways in which
they are to change, separated by commas (`,`). Generally, there should not be
more than one of a particular type of appearance. That is to say, it is valid
Scrappy to have an actor appear sad and happy, but it certainly doesn't make any
sense!

```
# An instruction for Bob to appear sad:
[Bob: sad]

# An instruction for Bob to appear sad with his back to the viewers:
[Bob: sad, back-turned]

# Valid Scrappy, but a bit confusing:
[Bob: sad, happy, back-turned]

# Makes a bit more sense:
[Bob: bittersweet, back-turned]
```

An actor can also be instructed to move somewhere on the screen. To do this, use
the `GO TO` keywords followed by an identifier for the destination.

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

In Scrappy, the CHOICE directive is more limited than comparable structures in
other languages, such as `menu` in Ren'Py. Each option must jump to a section,
which is not required in the Ren'Py `menu` statement. However, this helps to
enforce simplicity of design within the code; CHOICE statements are kept short
and succinct rather than having the possibility of stretching into a very long
block.

A minimal CHOICE directive consists of `[Choice]` followed by a series of
options. Each option begins with an asterisk (`*`) character and gives the text
of the option that is shown to the viewer, followed by a colon (`:`) and then
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
parameter is separated from the rest of the option parameters by a comma (`,`).

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
- [SECTION annotation](#section-annotation)
- [VAR annotation](#var-annotation)

### ENTER Directive ###
The ENTER directive is used to instruct an actor to appear in the scene. There
are several different ways that the entrance can be customized.

Every ENTER directive needs an actor that it is addressing. A minimal ENTER
consists only of the actor.

```
[Enter: Bob]
```

In order to specify the appearance of the actor, the appearance can be given in
parenthesis. Multiple appearance instructions are separated by commas.

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
# Some entrance destinations with explicit duration:
[Enter: Bob OVER 10 SECONDS]
[Enter: Mary (upset) FROM offscreenright TO stage-right SLOWLY]
[Enter: Ghost (angry, arms-crossed) DISSOLVE IN
	FROM center TO stage-left QUICKLY]
```

It is important to ensure that the order of operations of the entrance is
specified clearly. What the ENTER directive means is that the actor should enter
the scene with the given transition if there is one, or appear instantly if
there is not one, at the specified origin if one is given, otherwise at an
understood origin. After the transition in is complete, the actor then moves to
the specified destination if there is one. If no origin is given but a
destination is given, the actor is to appear/transition to that location and not
move at all.

Note that this means that specififying an off-screen origin or an off-screen
destintation with no origin means that any transition will not be visible to the
viewer.

#### See Also ####
- [EXIT Directive](#exit-directive)
- [SCENE Directive](#scene-directive)

### EXIT Directive ###
The EXIT directive is an instruction to the actor to exit from the scene. There
are several different ways that the exit can be customized.

Every EXIT directive needs an actor that it is addressing. A minimal EXIT
consists only of the actor.

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

It is important to ensure that the order of operations of the entrance is
specified clearly. What the EXIT directive means is that the actor should first
move to the origin of the exit path if he is not already there, and then move to
the destination of the exit path. Finally, once there, they are to exit the
scene, either by using the given transition or by disappearing if no transition
is specified.

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
directive. This can be a string containing the name of a video file or an
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
visual effect.

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

Normally, the visual effect will disappear instantly when stopped; however, this
can be changed by giving a [duration](#durations). The visual effect will then
take the given amount of time to fade away.

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
parameter to the directive. This can be a string containing the name of the
audio file or an identifier for the music track.

```
# The two forms for playing a particular track
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
a SCENE directive is in a Scrappy manuscript, it indicates the start of a new
location, or at least a new sub-location within the current location.

To transition to a new scene, the identifier for the scene to change to is given
as a parameter to the directive.

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
- [Enter Directive](#enter-directive)

### SFX Directive ###
The SFX directive is used to control sound effects.

To play a sound effect once, give the name of the sound effect. The name can be
a string containing the audio file to play or the identifier of the effect.

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

Normally, the looping sound will stop instantly when stopped; however, this can
be changed by giving a [duration](#durations). The sound effect will then take
the given amount of time to fade away.

```
[SFX: STOP sprinting-footsteps OVER 5 SECONDS]
[SFX: STOP "heavy_breathing.mp3" SLOWLY]
[SFX: STOP ALL QUICKLY]
[SFX: STOP SLOWLY]
```