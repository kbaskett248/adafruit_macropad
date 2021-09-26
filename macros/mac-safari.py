# MACROPAD Hotkeys example: Safari web browser for Mac

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import BaseApp


class MacSafariApp(BaseApp):
    name = "Mac Safari"

    # First row
    key_1 = (0x004000, "< Back", [Keycode.COMMAND, "["])
    key_2 = (0x004000, "Fwd >", [Keycode.COMMAND, "]"])
    key_3 = (0x400000, "Up", [Keycode.SHIFT, " "])  # Scroll up

    # Second row
    key_4 = (0x202000, "< Tab", [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB])
    key_5 = (0x202000, "Tab >", [Keycode.CONTROL, Keycode.TAB])
    key_6 = (0x400000, "Down", " ")  # Scroll down

    # Third row
    key_7 = (0x000040, "Reload", [Keycode.COMMAND, "r"])
    key_8 = (0x000040, "Home", [Keycode.COMMAND, "H"])
    key_9 = (0x000040, "Private", [Keycode.COMMAND, "N"])

    # Fourth row
    key_10 = (
        0x000000,
        "Ada",
        [Keycode.COMMAND, "n", -Keycode.COMMAND, "www.adafruit.com\n"],
    )  # Adafruit in new window
    key_11 = (
        0x800000,
        "Digi",
        [Keycode.COMMAND, "n", -Keycode.COMMAND, "www.digikey.com\n"],
    )  # Digi-Key in new window
    key_12 = (
        0x101010,
        "Hacks",
        [Keycode.COMMAND, "n", -Keycode.COMMAND, "www.hackaday.com\n"],
    )  # Hack-a-Day in new win


MacSafariApp()
