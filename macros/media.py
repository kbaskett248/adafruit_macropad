# MACROPAD Hotkeys example: Consumer Control codes (media keys)

# The syntax for Consumer Control macros is a little peculiar, in order to
# maintain backward compatibility with the original keycode-only macro files.
# The third item for each macro is a list in brackets, and each value within
# is normally an integer (Keycode), float (delay) or string (typed literally).
# Consumer Control codes are distinguished by enclosing them in a list within
# the list, which is why you'll see double brackets [[ ]] below.
# Like Keycodes, Consumer Control codes can be positive (press) or negative
# (release), and float values can be inserted for pauses.

# To reference Consumer Control codes, import ConsumerControlCode like so...
from adafruit_hid.consumer_control_code import ConsumerControlCode

from app import BaseApp, MacroApp
from key import MacroKey, Media


@BaseApp.register_app
class MediaApp(MacroApp):
    name = "Media"

    # First row
    key_1 = MacroKey("Vol+", 0x000020, Media(ConsumerControlCode.VOLUME_INCREMENT))
    key_2 = MacroKey(
        "Bright+", 0x202020, Media(ConsumerControlCode.BRIGHTNESS_INCREMENT)
    )

    # Second row
    key_4 = MacroKey("Vol-", 0x000020, Media(ConsumerControlCode.VOLUME_DECREMENT))
    key_5 = MacroKey(
        "Bright-", 0x202020, Media(ConsumerControlCode.BRIGHTNESS_DECREMENT)
    )

    # Third row
    key_7 = MacroKey("Mute", 0x200000, Media(ConsumerControlCode.MUTE))

    # Fourth row
    key_9 = MacroKey("<<", 0x202000, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = MacroKey("Play/Pause", 0x002000, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = MacroKey(">>", 0x202000, Media(ConsumerControlCode.SCAN_NEXT_TRACK))
