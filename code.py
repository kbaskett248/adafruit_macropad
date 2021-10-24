"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

from apps.key import Key
from apps.numpad import NumpadApp
from apps.settings import KeyAppWithSettings, SettingsValueKey
from app_pad import AppPad
from commands import Media, ConsumerControlCode, SwitchAppCommand
from constants import OS_SETTING, OS_LINUX, OS_MAC, OS_WINDOWS, PREVIOUS_APP_SETTING

app_pad = AppPad()


macro_settings = {
    OS_SETTING: OS_MAC,
    PREVIOUS_APP_SETTING: None,
}


numpad_app = NumpadApp(app_pad, macro_settings)


class HomeApp(KeyAppWithSettings):
    name = "Home"

    key_0 = SettingsValueKey("MAC", 0x555555, OS_SETTING, OS_MAC)
    key_1 = SettingsValueKey("WIN", 0x00A4EF, OS_SETTING, OS_WINDOWS)
    key_2 = SettingsValueKey("LIN", 0x25D366, OS_SETTING, OS_LINUX)

    key_3 = Key(text="Num", color=0x303030, command=SwitchAppCommand(numpad_app))

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
