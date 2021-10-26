# MACROPAD Hotkeys example: Firefox web browser for Linux

from apps.macro import MacroApp, MacroKey
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press, Release, Sequence, Text, Wait


new_tab = Sequence(Press(Keycode.CONTROL), Text("t"), Release(Keycode.CONTROL))


class ChromeApp(KeyAppWithSettings):
    name = "Chrome"

    # First row
    key_0 = MacroKey(
        "BkMrk",
        0x101010,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.D)),
        mac_command=Sequence(Press(Keycode.COMMAND), Text("d")),
    )
    key_1 = MacroKey(
        "Close",
        0x101010,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.W)),
        mac_command=Sequence(Press(Keycode.COMMAND), Text("w")),
    )
    key_2 = MacroKey(
        "Back",
        0x101010,
        Sequence(
            Press(Keycode.ALT),
            Press(Keycode.TAB),
            Wait(0.1),
            Release(Keycode.TAB),
            Release(Keycode.ALT),
            PreviousAppCommand(),
        ),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.C),
            PreviousAppCommand(),
        ),
    )

    # Second row
    key_3 = MacroKey(
        "<-",
        0x004000,
        Sequence(Press(Keycode.ALT), Press(Keycode.LEFT_ARROW)),
        mac_command=Sequence(Press(Keycode.COMMAND), Press(Keycode.LEFT_ARROW)),
    )
    key_4 = MacroKey(
        "Address",
        0x400000,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.L)),
        mac_command=Sequence(Press(Keycode.COMMAND), Press(Keycode.L)),
    )
    key_5 = MacroKey(
        "->",
        0x004000,
        Sequence(Press(Keycode.ALT), Press(Keycode.RIGHT_ARROW)),
        mac_command=Sequence(Press(Keycode.COMMAND), Press(Keycode.RIGHT_ARROW)),
    )

    # Third row
    key_6 = MacroKey(
        "<<",
        0x202000,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.PAGE_UP)),
        mac_command=Sequence(
            Press(Keycode.COMMAND), Press(Keycode.OPTION), Press(Keycode.LEFT_ARROW)
        ),
    )
    key_7 = MacroKey(
        "Tab Search",
        0x202000,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Press(Keycode.A)),
        mac_command=Sequence(
            Press(Keycode.COMMAND), Press(Keycode.SHIFT), Press(Keycode.A)
        ),
    )
    key_8 = MacroKey(
        "    >>",
        0x202000,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.PAGE_DOWN)),
        mac_command=Sequence(
            Press(Keycode.COMMAND), Press(Keycode.OPTION), Press(Keycode.RIGHT_ARROW)
        ),
    )

    # Fourth row
    key_9 = MacroKey(
        "Menu",
        0x000040,
        Sequence(Press(Keycode.ALT), Press(Keycode.E)),
        mac_command=None,
    )
    key_10 = MacroKey(
        "Book",
        0x000040,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.SHIFT), Press(Keycode.O)),
        mac_command=Sequence(
            Press(Keycode.COMMAND), Press(Keycode.OPTION), Press(Keycode.B)
        ),
    )
    key_11 = MacroKey(
        "Hist",
        0x000040,
        Sequence(Press(Keycode.CONTROL), Press(Keycode.H)),
        mac_command=Sequence(Press(Keycode.COMMAND), Text("y")),
    )
