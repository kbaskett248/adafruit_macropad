# Extra keys missing from my keyboard

from apps.macro import MacroApp, MacroKey
from commands import Keycode, ConsumerControlCode, Media, Press, Scroll


@MacroApp.register_app
class ExtraKeysApp(MacroApp):
    name = "Extra keys"

    key_0 = MacroKey("Home", 0x004000, Press(Keycode.HOME))
    key_1 = MacroKey("End", 0x004000, Press(Keycode.END))
    key_2 = MacroKey("Up", 0x400000, Scroll(5))

    key_5 = MacroKey("Down", 0x400000, Scroll(-5))

    key_6 = MacroKey("Vol-", 0x000020, Media(ConsumerControlCode.VOLUME_DECREMENT))
    key_7 = MacroKey("Mute", 0x200000, Media(ConsumerControlCode.MUTE))
    key_8 = MacroKey("Vol+", 0x000020, Media(ConsumerControlCode.VOLUME_INCREMENT))

    key_9 = MacroKey("<<", 0x202000, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = MacroKey("Play/Pause", 0x002000, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = MacroKey(">>", 0x202000, Media(ConsumerControlCode.SCAN_NEXT_TRACK))
