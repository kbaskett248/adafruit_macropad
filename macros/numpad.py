# MACROPAD Hotkeys example: Universal Numpad

from app import BaseApp, MacroApp
from key import Key, Text


@BaseApp.register_app
class NumpadApp(MacroApp):
    name = "Numpad"

    # First row
    key_0 = Key("7", 0x202000, Text("7"))
    key_1 = Key("8", 0x202000, Text("8"))
    key_2 = Key("9", 0x202000, Text("9"))

    # Second row
    key_3 = Key("4", 0x202000, Text("4"))
    key_4 = Key("5", 0x202000, Text("5"))
    key_5 = Key("6", 0x202000, Text("6"))

    # Third row
    key_6 = Key("1", 0x202000, Text("1"))
    key_7 = Key("2", 0x202000, Text("2"))
    key_8 = Key("3", 0x202000, Text("3"))

    # Fourth row
    key_9 = Key("*", 0x101010, Text("*"))
    key_10 = Key("0", 0x800000, Text("0"))
    key_11 = Key("#", 0x101010, Text("#"))
