# Nav cluster

from apps.key import Key
from apps.macro import MacroKey
from apps.settings import KeyAppWithSettings, PreviousAppCommand
from commands import Keycode, Press, Sequence


class AppSwitcherApp(KeyAppWithSettings):
    name = "App Switcher"

    key_3 = MacroKey(
        "Term",
        0x101010,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.FOUR)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.SHIFT),
            Press(Keycode.ENTER),
        ),
    )
    key_4 = MacroKey(
        "Files",
        0x101010,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.TWO)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.F),
        ),
    )
    key_5 = MacroKey(
        "Spotify",
        0x1ED760,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.SEVEN)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.S),
        ),
    )

    key_6 = MacroKey(
        "PyCharm",
        0x1ED760,
        Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.H),
        ),
        windows_command=None,
    )
    key_7 = MacroKey(
        "Code",
        0x1ED760,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.FIVE)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.V),
        ),
    )
    key_8 = MacroKey(
        "Merge",
        0x1ED760,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.SIX)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.M),
        ),
    )

    key_9 = MacroKey(
        "Chrome",
        0x101010,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.ONE)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.C),
        ),
    )
    key_10 = MacroKey(
        "Notion",
        0x101010,
        Sequence(Press(Keycode.WINDOWS), Press(Keycode.THREE)),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.N),
        ),
    )
    key_11 = MacroKey(
        "Slack",
        0x101010,
        Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.L),
        ),
        windows_command=None,
    )

    encoder_button = PreviousAppCommand()

    def encoder_button_event(self, event):
        if event.pressed:
            self.encoder_button.execute(self)
        else:
            self.encoder_button.undo(self)
