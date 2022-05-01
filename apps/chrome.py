# MACROPAD Hotkeys example: Firefox web browser for Linux

from utils.apps.key import KeyApp, MacroKey
from utils.commands import (
    Keycode,
    MacroCommand,
    Press,
    PreviousAppCommand,
    Release,
    Sequence,
    Text,
    Wait,
)
from utils.constants import (
    COLOR_3,
    COLOR_7,
    COLOR_9,
    COLOR_BACK,
    COLOR_CHROME,
    COLOR_CLOSE,
    OS_MAC,
)


class ChromeApp(KeyApp):
    name = "Chrome"

    # First row
    key_0 = MacroKey(
        "Exit",
        COLOR_CLOSE,
        Sequence(
            Press(Keycode.ALT, Keycode.F4),
            PreviousAppCommand(),
        ),
        mac_command=Sequence(Press(Keycode.COMMAND, Keycode.Q), PreviousAppCommand()),
    )
    key_1 = MacroKey(
        "Switch",
        COLOR_CHROME,
        Sequence(
            Press(Keycode.WINDOWS, Keycode.ONE),
            Wait(0.1),
            Release(Keycode.ONE, Keycode.WINDOWS),
        ),
        mac_command=Press(Keycode.COMMAND, Keycode.CONTROL, Keycode.OPTION, Keycode.C),
    )
    key_2 = MacroKey(
        "Back",
        COLOR_BACK,
        PreviousAppCommand(),
        double_tap_command=PreviousAppCommand(),
    )

    # Second row
    key_3 = MacroKey(
        "Bkmk",
        COLOR_3,
        Press(Keycode.CONTROL, Keycode.D),
        mac_command=Press(Keycode.COMMAND, Keycode.D),
    )
    key_4 = MacroKey(
        "Close",
        COLOR_CLOSE,
        Press(Keycode.CONTROL, Keycode.W),
        mac_command=Press(Keycode.COMMAND, Keycode.W),
    )

    # Third row
    key_6 = MacroKey(
        "<-",
        COLOR_7,
        Press(Keycode.ALT, Keycode.LEFT_ARROW),
        mac_command=Press(Keycode.COMMAND, Keycode.LEFT_ARROW),
    )
    key_7 = MacroKey(
        "Address",
        COLOR_9,
        Press(Keycode.CONTROL, Keycode.L),
        mac_command=Press(Keycode.COMMAND, Keycode.L),
    )
    key_8 = MacroKey(
        "->",
        COLOR_7,
        Press(Keycode.ALT, Keycode.RIGHT_ARROW),
        mac_command=Press(Keycode.COMMAND, Keycode.RIGHT_ARROW),
    )

    # Fourth row
    key_9 = MacroKey(
        "Menu",
        COLOR_CHROME,
        Press(Keycode.ALT, Keycode.E),
        mac_command=None,
    )
    key_10 = MacroKey(
        "Book",
        COLOR_CHROME,
        Press(Keycode.CONTROL, Keycode.SHIFT, Keycode.O),
        mac_command=Press(Keycode.COMMAND, Keycode.OPTION, Keycode.B),
    )
    key_11 = MacroKey(
        "Hist",
        COLOR_CHROME,
        Press(Keycode.CONTROL, Keycode.H),
        mac_command=Press(Keycode.COMMAND, Keycode.Y),
    )

    encoder_button = MacroCommand(
        Sequence(
            Press(Keycode.CONTROL, Keycode.SHIFT, Keycode.A),
            Wait(0.1),
            Release(Keycode.A, Keycode.SHIFT, Keycode.CONTROL),
        ),
        **{
            OS_MAC: Sequence(
                Press(Keycode.COMMAND, Keycode.SHIFT, Keycode.A),
                Wait(0.1),
                Release(Keycode.A, Keycode.SHIFT, Keycode.COMMAND),
            )
        },
    )

    encoder_decrease = MacroCommand(
        Press(Keycode.CONTROL, Keycode.PAGE_UP),
        **{OS_MAC: Press(Keycode.COMMAND, Keycode.OPTION, Keycode.LEFT_ARROW)},
    )
    encoder_increase = MacroCommand(
        Press(Keycode.CONTROL, Keycode.PAGE_DOWN),
        **{OS_MAC: Press(Keycode.COMMAND, Keycode.OPTION, Keycode.RIGHT_ARROW)},
    )
