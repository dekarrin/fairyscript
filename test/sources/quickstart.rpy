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