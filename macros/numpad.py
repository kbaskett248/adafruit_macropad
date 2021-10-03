# MACROPAD Hotkeys example: Universal Numpad

from app import MacroApp
from key import LabeledKey, Text


class NumpadApp(MacroApp):
    name = "Numpad"

    # First row
    key_0 = LabeledKey("7", 0x202000, Text("7"))
    key_1 = LabeledKey("8", 0x202000, Text("8"))
    key_2 = LabeledKey("9", 0x202000, Text("9"))

    # Second row
    key_3 = LabeledKey("4", 0x202000, Text("4"))
    key_4 = LabeledKey("5", 0x202000, Text("5"))
    key_5 = LabeledKey("6", 0x202000, Text("6"))

    # Third row
    key_6 = LabeledKey("1", 0x202000, Text("1"))
    key_7 = LabeledKey("2", 0x202000, Text("2"))
    key_8 = LabeledKey("3", 0x202000, Text("3"))

    # Fourth row
    key_9 = LabeledKey("*", 0x101010, Text("*"))
    key_10 = LabeledKey("0", 0x800000, Text("0"))
    key_11 = LabeledKey("#", 0x101010, Text("#"))


NumpadApp()
