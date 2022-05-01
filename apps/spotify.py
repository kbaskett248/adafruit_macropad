"""Hotkeys for Spotify."""

from utils.apps.key import Key, KeyApp, MacroKey
from utils.commands import (
    ConsumerControlCode,
    Keycode,
    MacroCommand,
    Media,
    Press,
    PreviousAppCommand,
    Sequence,
)
from utils.constants import (
    COLOR_2,
    COLOR_BACK,
    COLOR_CLOSE,
    COLOR_MEDIA,
    COLOR_SPOTIFY,
    OS_MAC,
)


class SpotifyApp(KeyApp):
    name = "Spotify"

    key_0 = MacroKey(
        "Exit",
        COLOR_CLOSE,
        Sequence(
            Press(Keycode.CONTROL, Keycode.SHIFT, Keycode.Q),
            PreviousAppCommand(),
        ),
        mac_command=Sequence(Press(Keycode.COMMAND, Keycode.Q), PreviousAppCommand()),
    )
    key_1 = MacroKey(
        "Switch",
        COLOR_SPOTIFY,
        Press(Keycode.WINDOWS, Keycode.SEVEN),
        mac_command=Press(Keycode.COMMAND, Keycode.OPTION, Keycode.CONTROL, Keycode.S),
    )
    key_2 = Key(
        "Back",
        COLOR_BACK,
        PreviousAppCommand(),
        double_tap_command=PreviousAppCommand(),
    )

    key_3 = MacroKey(
        "Search",
        COLOR_SPOTIFY,
        Press(Keycode.CONTROL, Keycode.L),
        mac_command=Press(Keycode.COMMAND, Keycode.L),
    )
    key_4 = MacroKey(
        "Shuffle",
        COLOR_2,
        Press(Keycode.CONTROL, Keycode.S),
        mac_command=Press(Keycode.COMMAND, Keycode.S),
    )
    key_5 = MacroKey(
        "Filter",
        COLOR_SPOTIFY,
        Press(Keycode.CONTROL, Keycode.F),
        mac_command=Press(Keycode.COMMAND, Keycode.F),
    )

    key_6 = MacroKey(
        "<-",
        COLOR_MEDIA,
        Press(Keycode.SHIFT, Keycode.LEFT_ARROW),
    )
    key_7 = MacroKey(
        "Repeat",
        COLOR_2,
        Press(Keycode.CONTROL, Keycode.R),
        mac_command=Press(Keycode.COMMAND, Keycode.R),
    )
    key_8 = MacroKey(
        "->",
        COLOR_MEDIA,
        Press(Keycode.SHIFT, Keycode.RIGHT_ARROW),
    )

    # Fourth row
    key_9 = Key("<<", COLOR_MEDIA, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = Key(">||", COLOR_MEDIA, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = Key(">>", COLOR_MEDIA, Media(ConsumerControlCode.SCAN_NEXT_TRACK))

    encoder_button = Media(ConsumerControlCode.MUTE)
    encoder_increase = MacroCommand(
        Press(Keycode.CONTROL, Keycode.UP_ARROW),
        **{OS_MAC: Press(Keycode.COMMAND, Keycode.UP_ARROW)}
    )
    encoder_decrease = MacroCommand(
        Press(Keycode.CONTROL, Keycode.DOWN_ARROW),
        **{OS_MAC: Press(Keycode.COMMAND, Keycode.DOWN_ARROW)}
    )
