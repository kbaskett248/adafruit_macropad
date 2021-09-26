# Extra keys missing from my keyboard

from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values
from adafruit_hid.mouse import Mouse

app = {  # REQUIRED dict, must be named 'app'
    "name": "Extra keys",  # Application name
    "macros": [  # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, "Home", [Keycode.HOME]),
        (0x004000, "End", [Keycode.END]),
        (0x400000, "Up", [{"wheel": 5}]),  # Scroll up
        # 2nd row ----------
        (0x000000, "", []),
        (0x000000, "", []),
        (0x400000, "Down", [{"wheel": -5}]),  # Scroll down
        # 3rd row ----------
        (0x000040, "", []),
        (0x000040, "", []),
        (0x000040, "", []),
        # 4th row ----------
        (0x000000, "", []),
        (0x000000, "", []),
        (0x000000, "", []),
        # Encoder button ---
        (0x000000, "", []),
    ],
}
