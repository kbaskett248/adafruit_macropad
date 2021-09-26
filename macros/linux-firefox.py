# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import BaseApp


class LinuxFirefoxApp(BaseApp):
    name = "Linux Firefox"

    # First row
    key_1 = (0x004000, "< Back", [Keycode.CONTROL, "["])
    key_2 = (0x004000, "Fwd >", [Keycode.CONTROL, "]"])
    key_3 = (0x400000, "Up", [Keycode.SHIFT, " "])  # Scroll up

    # Second row
    key_4 = (0x202000, "< Tab", [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB])
    key_5 = (0x202000, "Tab >", [Keycode.CONTROL, Keycode.TAB])
    key_6 = (0x400000, "Down", " ")  # Scroll down

    # Third row
    key_7 = (0x000040, "Reload", [Keycode.CONTROL, "r"])
    key_8 = (0x000040, "Home", [Keycode.CONTROL, "h"])
    key_9 = (0x000040, "Private", [Keycode.CONTROL, Keycode.SHIFT, "p"])

    # Fourth row
    key_10 = (
        0x101010,
        "Ada",
        [Keycode.CONTROL, "t", -Keycode.CONTROL, "www.adafruit.com\n"],
    )  # adafruit.com in a new tab
    key_11 = (0x000040, "Dev Mode", [Keycode.F12])  # dev mode
    key_12 = (
        0x101010,
        "Digi",
        [Keycode.CONTROL, "t", -Keycode.CONTROL, "digikey.com\n"],
    )  # digikey in a new tab


LinuxFirefoxApp()
