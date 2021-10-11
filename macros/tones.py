# MACROPAD Hotkeys example: Tones

# The syntax for Tones in macros is highly peculiar, in order to maintain
# backward compatibility with the original keycode-only macro files.
# The third item for each macro is a list in brackets, and each value within
# is normally an integer (Keycode), float (delay) or string (typed literally).
# Consumer Control codes were added as list-within-list, and then mouse and
# tone further complicate this by adding dicts-within-list. Each tone-related
# item is the key 'tone' with either an integer frequency value, or 0 to stop
# the tone mid-macro (tone is also stopped when key is released).
# Helpful: https://en.wikipedia.org/wiki/Piano_key_frequencies

# This example ONLY shows tones (and delays), but really they can be mixed
# with other elements (keys, codes, mouse) to provide auditory feedback.

from app import BaseApp, MacroApp
from key import Key, Sequence, Tone, Wait


@BaseApp.register_app
class ToneApp(MacroApp):
    name = "Tones"

    # First row
    key_0 = Key("C3", 0x200000, Tone(131))
    key_1 = Key("C4", 0x202000, Tone(262))
    key_2 = Key("C5", 0x002000, Tone(523))

    # Second row
    key_3 = Key(
        "Rising",
        0x000020,
        Sequence(Tone(131), Wait(0.2), Tone(262), Wait(0.2), Tone(523)),
    )

    key_5 = Key(
        "Falling",
        0x000020,
        Sequence(Tone(523), Wait(0.2), Tone(262), Wait(0.2), Tone(131)),
    )
