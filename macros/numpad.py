# MACROPAD Hotkeys example: Universal Numpad

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import BaseApp


class NumpadApp(BaseApp):
    name = "Numpad"

    # First row
    key_1 = (0x202000, "7", ["7"])
    key_2 = (0x202000, "8", ["8"])
    key_3 = (0x202000, "9", ["9"])

    # Second row
    key_4 = (0x202000, "4", ["4"])
    key_5 = (0x202000, "5", ["5"])
    key_6 = (0x202000, "6", ["6"])

    # Third row
    key_7 = (0x202000, "1", ["1"])
    key_8 = (0x202000, "2", ["2"])
    key_9 = (0x202000, "3", ["3"])

    # Fourth row
    key_10 = (0x101010, "*", ["*"])
    key_11 = (0x800000, "0", ["0"])
    key_12 = (0x101010, "#", ["#"])


NumpadApp()
