from apps.key import Key
from apps.macro import MacroApp
from commands import Sequence, Tone, Wait


@MacroApp.register_app
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
