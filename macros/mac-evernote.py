# MACROPAD Hotkeys: Evernote web application for Mac
# Contributed by Redditor s010sdc

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values

from app import BaseApp


class MacEvernoteApp(BaseApp):
    name = "Mac Evernote"

    # First row
    key_1 = (0x004000, "New Nt", [Keycode.COMMAND, "n"])
    key_2 = (0x004000, "New Bk", [Keycode.SHIFT, Keycode.COMMAND, "n"])
    key_3 = (
        0x004000,
        "CP Lnk",
        [Keycode.CONTROL, Keycode.OPTION, Keycode.COMMAND, "c"],
    )

    # Second row
    key_4 = (0x004000, "Move", [Keycode.CONTROL, Keycode.COMMAND, "m"])
    key_5 = (0x004000, "Find", [Keycode.OPTION, Keycode.COMMAND, "f"])
    key_6 = (0x004000, "Emoji", [Keycode.CONTROL, Keycode.COMMAND, " "])

    # Third row
    key_7 = (0x004000, "Bullets", [Keycode.SHIFT, Keycode.COMMAND, "u"])
    key_8 = (0x004000, "Nums", [Keycode.SHIFT, Keycode.COMMAND, "o"])
    key_9 = (0x004000, "Check", [Keycode.SHIFT, Keycode.COMMAND, "t"])

    # Fourth row
    key_10 = (0x004000, "Date", [Keycode.SHIFT, Keycode.COMMAND, "D"])
    key_11 = (0x004000, "Time", [Keycode.OPTION, Keycode.SHIFT, Keycode.COMMAND, "D"])
    key_12 = (0x004000, "Divider", [Keycode.SHIFT, Keycode.COMMAND, "H"])


MacEvernoteApp()
