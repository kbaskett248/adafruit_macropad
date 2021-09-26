# MACROPAD Hotkeys example: Microsoft Edge web browser for Windows

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import BaseApp


class WindowsEdgeApp(BaseApp):
    name = "Windows Edge"

    # First row
    key_1 = (0x004000, "< Back", [Keycode.ALT, Keycode.LEFT_ARROW])
    key_2 = (0x004000, "Fwd >", [Keycode.ALT, Keycode.RIGHT_ARROW])
    key_3 = (0x400000, "Up", [Keycode.SHIFT, " "])  # Scroll up

    # Second row
    key_4 = (0x202000, "- Size", [Keycode.CONTROL, Keycode.KEYPAD_MINUS])
    key_5 = (0x202000, "Size +", [Keycode.CONTROL, Keycode.KEYPAD_PLUS])
    key_6 = (0x400000, "Down", " ")  # Scroll down

    # Third row
    key_7 = (0x000040, "Reload", [Keycode.CONTROL, "r"])
    key_8 = (0x000040, "Home", [Keycode.ALT, Keycode.HOME])
    key_9 = (0x000040, "Private", [Keycode.CONTROL, "N"])

    # Fourth row
    key_10 = (
        0x000000,
        "Ada",
        [Keycode.CONTROL, "n", -Keycode.COMMAND, "www.adafruit.com\n"],
    )  # Adafruit in new window
    key_11 = (
        0x800000,
        "Digi",
        [Keycode.CONTROL, "n", -Keycode.COMMAND, "www.digikey.com\n"],
    )  # Digi-Key in new window
    key_12 = (
        0x101010,
        "Hacks",
        [Keycode.CONTROL, "n", -Keycode.COMMAND, "www.hackaday.com\n"],
    )  # Hack-a-Day in new win


WindowsEdgeApp()
