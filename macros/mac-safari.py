# MACROPAD Hotkeys example: Safari web browser for Mac

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import MacroApp
from key import LabeledKey, Press, Release, Sequence, Text


new_tab = Sequence(Press(Keycode.COMMAND), Text("n"), Release(Keycode.COMMAND))


class MacSafariApp(MacroApp):
    name = "Mac Safari"

    # First row
    key_0 = LabeledKey("< Back", 0x004000, Sequence(Press(Keycode.COMMAND), Text("[")))
    key_1 = LabeledKey("Fwd >", 0x004000, Sequence(Press(Keycode.COMMAND), Text("]")))
    key_2 = LabeledKey(
        "Up", 0x400000, Sequence(Press(Keycode.SHIFT), Text(" "))
    )  # Scroll up

    # Second row
    key_3 = LabeledKey(
        "< Tab",
        0x202000,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Press(Keycode.TAB)),
    )
    key_4 = LabeledKey(
        "Tab >", 0x202000, Sequence(Press(Keycode.CONTROL), Press(Keycode.TAB))
    )
    key_5 = LabeledKey("Down", 0x400000, Text(" "))  # Scroll down

    # Third row
    key_6 = LabeledKey("Reload", 0x000040, Sequence(Press(Keycode.COMMAND), Text("r")))
    key_7 = LabeledKey("Home", 0x000040, Sequence(Press(Keycode.COMMAND), Text("H")))
    key_8 = LabeledKey("Private", 0x000040, Sequence(Press(Keycode.COMMAND), Text("N")))

    # Fourth row
    key_9 = LabeledKey(
        "Ada", 0x000000, Sequence(new_tab, Text("www.adafruit.com\n"))
    )  # Adafruit in new window
    key_10 = LabeledKey(
        "Digi", 0x800000, Sequence(new_tab, Text("www.digikey.com\n"))
    )  # Digi-Key in new window
    key_11 = LabeledKey(
        "Hacks", 0x101010, Sequence(new_tab, Text("www.hackaday.com\n"))
    )  # Hack-a-Day in new win


MacSafariApp()
