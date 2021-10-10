# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import BaseApp, MacroApp
from key import MacroKey, Press, Release, Sequence, Text


new_tab = Sequence(Press(Keycode.CONTROL), Text("t"), Release(Keycode.CONTROL))


@BaseApp.register_app
class LinuxFirefoxApp(MacroApp):
    name = "Linux Firefox"

    # First row
    key_0 = MacroKey("< Back", 0x004000, Sequence(Press(Keycode.CONTROL), Text("[")))
    key_1 = MacroKey("Fwd >", 0x400000, Sequence(Press(Keycode.CONTROL), Text("]")))
    key_2 = MacroKey(
        "Up", 0x202000, Sequence(Press(Keycode.SHIFT), Text(" "))
    )  # Scroll up

    # Second row
    key_3 = MacroKey(
        "< Tab",
        0x202000,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Press(Keycode.TAB)),
    )
    key_4 = MacroKey(
        "Tab >", 0x400000, Sequence(Press(Keycode.CONTROL), Press(Keycode.TAB))
    )
    key_5 = MacroKey("Down", 0x40000, Text(" "))  # Scroll down

    # Third row
    key_6 = MacroKey("Reload", 0x000040, Sequence(Press(Keycode.CONTROL), Text("r")))
    key_7 = MacroKey("Home", 0x000040, Sequence(Press(Keycode.CONTROL), Text("h")))
    key_8 = MacroKey(
        "Private",
        0x000040,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Text("p")),
    )

    # Fourth row
    key_9 = MacroKey(
        "Ada", 0x101010, Sequence(new_tab, Text("www.adafruit.com\n"))
    )  # adafruit.com in a new tab
    key_10 = MacroKey("Dev Mode", 0x000040, Press(Keycode.F12))  # dev mode
    key_11 = MacroKey(
        "Digi", 0x101010, Sequence(new_tab, Text("digikey.com\n"))
    )  # digikey in a new tab
