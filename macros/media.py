from apps.macro import MacroApp, MacroKey
from commands import ConsumerControlCode, Keycode, Media, Press, Sequence, Text


@MacroApp.register_app
class MediaApp(MacroApp):
    name = "Media"

    # First row
    key_0 = MacroKey(
        "Spotify",
        0x1ED760,
        Sequence(Press(Keycode.WINDOWS), Text("7")),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.S),
        ),
    )

    # Second row

    # Third row
    key_6 = MacroKey("Vol-", 0x000020, Media(ConsumerControlCode.VOLUME_DECREMENT))
    key_7 = MacroKey("Mute", 0x200000, Media(ConsumerControlCode.MUTE))
    key_8 = MacroKey("Vol+", 0x000020, Media(ConsumerControlCode.VOLUME_INCREMENT))

    # Fourth row
    key_9 = MacroKey("<<", 0x202000, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = MacroKey("Play/Pause", 0x002000, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = MacroKey(">>", 0x202000, Media(ConsumerControlCode.SCAN_NEXT_TRACK))
