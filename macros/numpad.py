# MACROPAD Hotkeys example: Universal Numpad

from app import BaseApp
from key import LabeledKey, Text


class NumpadApp(BaseApp):
    name = "Numpad"

    # First row
    key_1 = LabeledKey("7", 0x202000, Text("7"))
    key_2 = LabeledKey("8", 0x202000, Text("8"))
    key_3 = LabeledKey("9", 0x202000, Text("9"))

    # Second row
    key_4 = LabeledKey("4", 0x202000, Text("4"))
    key_5 = LabeledKey("5", 0x202000, Text("5"))
    key_6 = LabeledKey("6", 0x202000, Text("6"))

    # Third row
    key_7 = LabeledKey("1", 0x202000, Text("1"))
    key_8 = LabeledKey("2", 0x202000, Text("2"))
    key_9 = LabeledKey("3", 0x202000, Text("3"))

    # Fourth row
    key_10 = LabeledKey("*", 0x101010, Text("*"))
    key_11 = LabeledKey("0", 0x800000, Text("0"))
    key_12 = LabeledKey("#", 0x101010, Text("#"))


NumpadApp()
