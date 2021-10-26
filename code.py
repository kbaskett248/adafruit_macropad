"""
An App program for Adafruit MACROPAD. Apps can send hotkeys or do pretty much
anything else.
"""

from apps.chrome import ChromeApp
from apps.func import FuncKeysApp
from apps.key import Key
from apps.macro import MacroKey
from apps.nav import NavApp
from apps.numpad import NumpadApp
from apps.settings import (
    KeyAppWithSettings,
    SettingsValueKey,
    SwitchAppCommand,
    PreviousAppCommand,
)
from apps.spotify import SpotifyApp
from app_pad import AppPad
from apps.window import WindowManagementApp
from commands import (
    ConsumerControlCode,
    Keycode,
    Media,
    Press,
    Release,
    Sequence,
    Wait,
)
from constants import OS_SETTING, OS_LINUX, OS_MAC, OS_WINDOWS, PREVIOUS_APP_SETTING

app_pad = AppPad()


macro_settings = {
    OS_SETTING: OS_MAC,
    PREVIOUS_APP_SETTING: [],
}


chrome_app = ChromeApp(app_pad, macro_settings)
func_keys_app = FuncKeysApp(app_pad, macro_settings)
nav_app = NavApp(app_pad, macro_settings)
numpad_app = NumpadApp(app_pad, macro_settings)
spotify_app = SpotifyApp(app_pad, macro_settings)
window_manager_app = WindowManagementApp(app_pad, macro_settings)


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
        Sequence(
            Press(Keycode.WINDOWS), Press(Keycode.SEVEN), SwitchAppCommand(spotify_app)
        ),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.OPTION),
            Press(Keycode.CONTROL),
            Press(Keycode.S),
            SwitchAppCommand(spotify_app),
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
        Sequence(
            Press(Keycode.WINDOWS),
            Press(Keycode.ONE),
            Wait(0.1),
            Release(Keycode.ONE),
            Release(Keycode.WINDOWS),
            SwitchAppCommand(chrome_app),
        ),
        mac_command=Sequence(
            Press(Keycode.COMMAND),
            Press(Keycode.CONTROL),
            Press(Keycode.OPTION),
            Press(Keycode.C),
            SwitchAppCommand(chrome_app),
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


app_switcher_app = AppSwitcherApp(app_pad, macro_settings)


class HomeApp(KeyAppWithSettings):
    name = "Home"

    key_0 = SettingsValueKey("MAC", 0x555555, OS_SETTING, OS_MAC)
    key_1 = SettingsValueKey("WIN", 0x00A4EF, OS_SETTING, OS_WINDOWS)
    key_2 = SettingsValueKey("LIN", 0x25D366, OS_SETTING, OS_LINUX)

    key_3 = Key(text="Num", color=0x303030, command=SwitchAppCommand(numpad_app))
    key_4 = Key(text="Nav", color=0x303030, command=SwitchAppCommand(nav_app))
    key_5 = Key(
        text="WinMan", color=0x303030, command=SwitchAppCommand(window_manager_app)
    )

    key_6 = Key(text="Apps", color=0x303030, command=SwitchAppCommand(app_switcher_app))
    key_7 = Key(text="Func", color=0x303030, command=SwitchAppCommand(func_keys_app))

    # Fourth row
    key_9 = Key("<<", 0x202000, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = Key(">||", 0x002000, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = Key(">>", 0x202000, Media(ConsumerControlCode.SCAN_NEXT_TRACK))

    encoder_button = Media(ConsumerControlCode.MUTE)
    encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)

    def __init__(self, app_pad):
        super().__init__(app_pad, settings=macro_settings)

    def encoder_event(self, event):
        if event.position > event.previous_position:
            self.encoder_increase.execute(self)
            self.encoder_increase.undo(self)
        elif event.position < event.previous_position:
            self.encoder_decrease.execute(self)
            self.encoder_decrease.undo(self)

    def encoder_button_event(self, event):
        if event.pressed:
            self.encoder_button.execute(self)
        else:
            self.encoder_button.undo(self)


app_pad.add_app(HomeApp)
app_pad.run()
