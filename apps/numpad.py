# MACROPAD Hotkeys example: Universal Numpad

from apps.key import Key
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press, Text
from constants import COLOR_8, COLOR_NUMPAD, COLOR_WARNING


class NumpadApp(KeyAppWithSettings):
    name = "Numpad"

    # First row
    key_0 = Key("7", COLOR_NUMPAD, Text("7"))
    key_1 = Key("8", COLOR_NUMPAD, Text("8"))
    key_2 = Key("9", COLOR_NUMPAD, Text("9"), double_tap_command=PreviousAppCommand())

    # Second row
    key_3 = Key("4", COLOR_NUMPAD, Text("4"))
    key_4 = Key("5", COLOR_NUMPAD, Text("5"))
    key_5 = Key("6", COLOR_NUMPAD, Text("6"))

    # Third row
    key_6 = Key("1", COLOR_NUMPAD, Text("1"))
    key_7 = Key("2", COLOR_NUMPAD, Text("2"))
    key_8 = Key("3", COLOR_NUMPAD, Text("3"))

    # Fourth row
    key_9 = Key(".", COLOR_8, Text("."))
    key_10 = Key("0", COLOR_NUMPAD, Text("0"))
    key_11 = Key("Entr", COLOR_WARNING, Press(Keycode.KEYPAD_ENTER))

    encoder_button = PreviousAppCommand()
