"""
An App program for Adafruit MACROPAD. Apps can send hotkeys or do pretty much
anything else.
"""

from apps.chrome import ChromeApp
from apps.func import FuncKeysApp
from apps.key import Key
from apps.macro import MacroKey, MacroSettingsApp
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
settings_app = MacroSettingsApp(app_pad, macro_settings)
spotify_app = SpotifyApp(app_pad, macro_settings)
window_manager_app = WindowManagementApp(app_pad, macro_settings)


class AppSwitcherApp(KeyAppWithSettings):
    name = "App Switcher"

    key_2 = Key("Back", 0x101010, PreviousAppCommand())

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

    encoder_button = Media(ConsumerControlCode.MUTE)

    encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)


app_switcher_app = AppSwitcherApp(app_pad, macro_settings)


class HomeApp(KeyAppWithSettings):
    name = "Home"

    key_0 = SettingsValueKey(
        OS_SETTING,
        SwitchAppCommand(settings_app),
        {OS_MAC: 0x555555, OS_WINDOWS: 0x00A4EF, OS_LINUX: 0x25D366},
        text_template="[ {value} ]",
    )

    key_3 = Key(text="Num", color=0x303030, command=SwitchAppCommand(numpad_app))
    key_4 = Key(text="Nav", color=0x303030, command=SwitchAppCommand(nav_app))
    key_5 = Key(text="Func", color=0x303030, command=SwitchAppCommand(func_keys_app))

    key_6 = Key(text="Apps", color=0x303030, command=SwitchAppCommand(app_switcher_app))
    key_8 = Key(
        text="WinMan", color=0x303030, command=SwitchAppCommand(window_manager_app)
    )

    # Fourth row
    key_9 = Key("<<", 0x202000, Media(ConsumerControlCode.SCAN_PREVIOUS_TRACK))
    key_10 = Key(">||", 0x002000, Media(ConsumerControlCode.PLAY_PAUSE))
    key_11 = Key(">>", 0x202000, Media(ConsumerControlCode.SCAN_NEXT_TRACK))

    encoder_button = Media(ConsumerControlCode.MUTE)

    encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)

    def __init__(self, app_pad):
        super().__init__(app_pad, settings=macro_settings)


app_pad.add_app(HomeApp)
app_pad.run()
