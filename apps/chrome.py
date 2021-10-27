# MACROPAD Hotkeys example: Firefox web browser for Linux

from apps.macro import MacroCommand, MacroKey
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press, Release, Sequence, Text, Wait
from constants import (
    COLOR_3,
    COLOR_7,
    COLOR_9,
    COLOR_BACK,
    COLOR_CHROME,
    COLOR_CLOSE,
    OS_MAC,
)


new_tab = Sequence(Press(Keycode.CONTROL), Text("t"), Release(Keycode.CONTROL))


class ChromeApp(KeyAppWithSettings):
    name = "Chrome"

    # First row
    key_2 = MacroKey(
        "Back",
        COLOR_BACK,
        Sequence(PreviousAppCommand()),
    )

    # Second row
    key_3 = MacroKey(
        COLOR_3,
        0x101010,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.D)),
        mac_command=Sequence(Press(Keycode.COMMAND), Text("d")),
    )
    key_4 = MacroKey(
        "Close",
        COLOR_CLOSE,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.W)),
        mac_command=Sequence(Press(Keycode.COMMAND), Text("w")),
    )

    # Third row
    key_6 = MacroKey(
        "<-",
        COLOR_7,
        Sequence(Press(Keycode.ALT), Press(Keycode.LEFT_ARROW)),
        mac_command=Sequence(Press(Keycode.COMMAND), Press(Keycode.LEFT_ARROW)),
    )
    key_7 = MacroKey(
        "Address",
        COLOR_9,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.L)),
        mac_command=Sequence(Press(Keycode.COMMAND), Press(Keycode.L)),
    )
    key_8 = MacroKey(
        "->",
        COLOR_7,
        Sequence(Press(Keycode.ALT), Press(Keycode.RIGHT_ARROW)),
        mac_command=Sequence(Press(Keycode.COMMAND), Press(Keycode.RIGHT_ARROW)),
    )

    # Fourth row
    key_9 = MacroKey(
        "Menu",
        COLOR_CHROME,
        Sequence(Press(Keycode.ALT), Press(Keycode.E)),
        mac_command=None,
    )
    key_10 = MacroKey(
        "Book",
        COLOR_CHROME,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Press(Keycode.O)),
        mac_command=Sequence(
            Press(Keycode.COMMAND), Press(Keycode.OPTION), Press(Keycode.B)
        ),
    )
    key_11 = MacroKey(
        "Hist",
        COLOR_CHROME,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.H)),
        mac_command=Sequence(Press(Keycode.COMMAND), Text("y")),
    )

    encoder_button = MacroCommand(
        Sequence(
            Press(Keycode.CONTROL),
            Press(Keycode.SHIFT),
            Press(Keycode.A),
            Wait(0.1),
            Release(Keycode.A),
            Release(Keycode.SHIFT),
            Release(Keycode.CONTROL),
        ),
        **{
            OS_MAC: Sequence(
                Press(Keycode.COMMAND),
                Press(Keycode.SHIFT),
                Press(Keycode.A),
                Wait(0.1),
                Release(Keycode.A),
                Release(Keycode.SHIFT),
                Release(Keycode.COMMAND),
            )
        },
    )

    encoder_decrease = MacroCommand(
        Sequence(Press(Keycode.CONTROL), Press(Keycode.PAGE_UP)),
        **{
            OS_MAC: Sequence(
                Press(Keycode.COMMAND), Press(Keycode.OPTION), Press(Keycode.LEFT_ARROW)
            )
        },
    )
    encoder_increase = MacroCommand(
        Sequence(Press(Keycode.CONTROL), Press(Keycode.PAGE_DOWN)),
        **{
            OS_MAC: Sequence(
                Press(Keycode.COMMAND),
                Press(Keycode.OPTION),
                Press(Keycode.RIGHT_ARROW),
            )
        },
    )
