# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import MacroApp
from key import LabeledKey, Press, Release, Sequence, Text


new_tab = Sequence(Press(Keycode.CONTROL), Text("t"), Release(Keycode.CONTROL))


class LinuxFirefoxApp(MacroApp):
    name = "Linux Firefox"

    # First row
    key_0 = LabeledKey("< Back", 0x004000, Sequence(Press(Keycode.CONTROL), Text("[")))
    key_1 = LabeledKey("Fwd >", 0x400000, Sequence(Press(Keycode.CONTROL), Text("]")))
    key_2 = LabeledKey(
        "Up", 0x202000, Sequence(Press(Keycode.SHIFT), Text(" "))
    )  # Scroll up

    # Second row
    key_3 = LabeledKey(
        "< Tab",
        0x202000,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Press(Keycode.TAB)),
    )
    key_4 = LabeledKey(
        "Tab >", 0x400000, Sequence(Press(Keycode.CONTROL), Press(Keycode.TAB))
    )
    key_5 = LabeledKey("Down", 0x40000, Text(" "))  # Scroll down

    # Third row
    key_6 = LabeledKey("Reload", 0x000040, Sequence(Press(Keycode.CONTROL), Text("r")))
    key_7 = LabeledKey("Home", 0x000040, Sequence(Press(Keycode.CONTROL), Text("h")))
    key_8 = LabeledKey(
        "Private",
        0x000040,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Text("p")),
    )

    # Fourth row
    key_9 = LabeledKey(
        "Ada", 0x101010, Sequence(new_tab, Text("www.adafruit.com\n"))
    )  # adafruit.com in a new tab
    key_10 = LabeledKey("Dev Mode", 0x000040, Press(Keycode.F12))  # dev mode
    key_11 = LabeledKey(
        "Digi", 0x101010, Sequence(new_tab, Text("digikey.com\n"))
    )  # digikey in a new tab


LinuxFirefoxApp()
