define Aerith = Character("The Fair Maiden Aeirth", color="#cc0000")

image bg meadow = "meadow.jpg"
image bg uni = "uni.jpg"

image sylvie smile = "sylvie_smile.png"
image sylvie surprised = "sylvie_surprised.png"

define s = Character('Sylvie', color="#c8ffc8")
define m = Character('Me', color="#c8c8ff")

label start:
    scene bg meadow
    show sylvie smile

    "I'll ask her..."

    m "Um... will you..."
    m "Will you be my artist for a visual novel?"

    show sylvie surprised

    "Silence."
    "She is shocked, and then..."

    show sylvie smile

    s "Sure, but what is a \"visual novel?\""

image bg meadow = "meadow.jpg"
image bg uni = "uni.jpg"

image sylvie smile = "sylvie_smile.png"
image sylvie surprised = "sylvie_surprised.png"

define s = Character('Sylvie', color="#c8ffc8")
define m = Character('Me', color="#c8c8ff")

label start:
    scene bg meadow
    show sylvie smile

    "I'll ask her..."

    m "Um... will you..."
    m "Will you be my artist for a visual novel?"

    show sylvie surprised

    "Silence."
    "She is shocked, and then..."

    show sylvie smile

    s "Sure, but what is a \"visual novel?\""

#: scrappy-gfx flash image

jump choice-section

scene bg Bobs-garage-2

scene bg my-house
show Aerith

show Aerith pissed-off

show Aerith pissed-off annoyed

show Aerith pissed annoyed with-back-turned

with FADE

show Aerith

with DISSOLVE

show Aerith pissed-off

with DISSOLVE

show Aerith pissed-off annoyed

with DISSOLVE

show Aerith pissed annoyed with-back-turned

show Aerith
at LEFT
show Aerith
at center
with MoveTransition(0.5)

show Aerith
at DOOR

show Aerith
at center
show Aerith
at center
with MoveTransition(0.25)

with FADE

show Aerith
at center
show Aerith
at center
with MoveTransition(2)

with FADE

show Aerith
at LEFT
show Aerith
at DOOR
with MoveTransition(0.5)

with FADE

show Aerith
at LEFT
show Aerith
at DOOR
with MoveTransition(4.5)

with FADE

show Aerith pissed mean
at LEFT
show Aerith pissed mean
at DOOR
with MoveTransition(4.5)

with FADE

show Bob pissed

show Bob
at stage-front
with MoveTransition(0.5)

show Bob
at stage-left
with MoveTransition(0.25)

show Bob pissed happy
at bookshelf
with MoveTransition(2)

show Aerith
hide Aerith

show Aerith
hide Aerith

show Aerith
at door
show Aerith
at door
with MoveTransition(0.5)
hide Aerith

show Aerith
at east-stairwell
hide Aerith

show Aerith
at center
show Aerith
at center
with MoveTransition(2)
hide Aerith

with FADE

show Aerith
at center
show Aerith
at center
with MoveTransition(2)
hide Aerith

with FADE

show Aerith
at door
show Aerith
at door
with MoveTransition(9)
hide Aerith

with FADE

stop music

stop music fadeout 0.25

stop music fadeout 3

stop music

stop music fadeout 2

stop music

stop music fadeout 2

play music main-theme

play music "main.ogg" fadeout 5

play music "main.ogg" fadeout 5

show flash_img
at flash

show flash_loop_img
at flash_loop

hide flash_loop_img
hide flash_img

show layer master

with Dissolve(5)

show layer master
with Dissolve(0.25)

show layer master

show layer master
with Dissolve(2)

play sound bang

play sound "concrete-sprint.ogg"

play sound "swish.ogg" loop

play sound swish loop

stop sound

stop sound fadeout 2

stop sound fadeout 0.25

stop sound

stop sound fadeout 4

renpy.movie_cutscene(opening)

renpy.movie_cutscene("opening_video.mp4")

"[snap camera to middle]"

"[pan camera to center]"

"[zoom camera in]"

"[zoom camera out]"

"[zoom camera out]"

"[pan camera to middle]"

"[zoom camera out]"

"[pan camera to middle]"

"[zoom camera out]"

"[snap camera to bookshelf]"

menu:
    "Show her the 'private collection'":
        jump private
        
    "Show them the call logs" if True:
        jump call_logs
        
    "Show her the missing files" if have_hacked_computer:
        jump files
        
    "Show him the broken chair" if hacked_computer:
        jump files
        
    "Punch her" if False:
        $ have_punched_aerith = True
        jump punch
        
menu choice-section:
    "What should I tell him?"
    
    "Try to feign ignorance":
        $ goodness -= 5
        $ ignore += 1
        jump ignorance
        
    "Tell the truth":
        $ badness = goodness
        $ truth = True
        jump tell_truth
        
    "Run away." if x + 4 >= 39:
        jump run
        
scene bg ayase-bedroom

label punch:
    $ have_drank_tea = True
    
    $ drank_tea = True
    
    $ drank_tea = False
    
    $ have_drank_tea = True
    
    $ have_drank_tea = False
    
    $ impressed_aerith = have_hacked_computer
    
    $ have_impressed_aerith = have_hacked_computer
    
    $ impressed_aerith = hacked_computer
    
    $ have_impressed_aerith = hacked_computer
    
    $ runs = 1
    
    $ runs = "82"
    
    $ runs += 1
    
    $ have_run = False
    
    $ reps = 28
    
    $ reps -= 5
    
    window hide
    
    window show
    
    window auto
    
    jump aerith-punch
    
    jump bob-punch
    
    call expression "punch" pass (target="bob")
    
    call aerith-punch
    

return 5

image bg meadow = "meadow.jpg"
image bg uni = "uni.jpg"

image sylvie smile = "sylvie_smile.png"
image sylvie surprised = "sylvie_surprised.png"

define s = Character('Sylvie', color="#c8ffc8")
define m = Character('Me', color="#c8c8ff")

label start:
    scene bg meadow
    show sylvie smile

    "I'll ask her..."

    m "Um... will you..."
    m "Will you be my artist for a visual novel?"

    show sylvie surprised

    "Silence."
    "She is shocked, and then..."

    show sylvie smile

    s "Sure, but what is a \"visual novel?\""

while staff:
    $ runs += 1
    

while True:
    $ runs -= 1
    

while False:
    $ runs += 2
    

while (x > 8 and q is not 6):
    $ have_seen_god = True
    

if staff:
    $ runs += 1
    
if True:
    $ runs -= 1
    
elif False:
    $ runs += 2
    
    $ runs += 1
    
if (x > 8 and q is not 6):
    $ have_seen_god = True
    
    jump bob-world
    
    if have_seen_god:
        jump aerith-world
        
elif (35 + 14 > 4):
    call aerith-punch
    
else:
    $ have_seen_god = False
    
python:
    42+1
    for i in ziebel:
    print i

"It feels like everything has gone wrong."
"Never before have I felt so awful! I guess that's just how it goes..."
"One day it will be better."
Aerith "Hey man, what's up?"
"Aerith? What's she doing here?"
Aerith "I heard you were feeling down."
Aerith "So I decided to stop by."
Bob "I become the wall when I died."

scene bg bobs-house

if have_killed_bob:
    $ good += 1
    
"The Wall" "Don't forget about me!"
"The Wall" "I'm here too, you know!"
