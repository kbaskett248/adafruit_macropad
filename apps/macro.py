from apps.key import KeyApp, Key
from apps.settings import KeyAppWithSettings, SettingsValueKey
from constants import (
    EMPTY_VALUE,
    PREVIOUS_APP_SETTING,
    OS_SETTING,
    OS_MAC,
    OS_LINUX,
    OS_WINDOWS,
)


MacroAppSettings = {
    OS_SETTING: OS_MAC,
    PREVIOUS_APP_SETTING: None,
}


class MacroSettingsApp(KeyAppWithSettings):
    name = "Macropad Settings"

    key_0 = SettingsValueKey("MAC", 0x555555, OS_SETTING, OS_MAC)
    key_1 = SettingsValueKey("WIN", 0x00A4EF, OS_SETTING, OS_WINDOWS)
    key_2 = SettingsValueKey("LIN", 0x25D366, OS_SETTING, OS_LINUX)

    def __init__(self, app_pad):
        super().__init__(app_pad, settings=MacroAppSettings)

    def encoder_button_event(self, event):
        if event.pressed:
            previous_app = self.get_setting(PREVIOUS_APP_SETTING)
            self.put_setting(PREVIOUS_APP_SETTING, None)
            self.app_pad.current_app = previous_app


class MacroApp(KeyAppWithSettings):
    name = "Macro App"
    SETTINGS_APP = MacroSettingsApp

    def __init__(self, app_pad):
        super().__init__(app_pad, settings=MacroAppSettings)
        try:
            self.settings_app
        except AttributeError:
            MacroApp.settings_app = self.SETTINGS_APP(self.app_pad)

    def encoder_event(self, event):
        self.app_pad.app_index = event.position % len(self.app_pad.apps)
        self.app_pad.current_app = self.app_pad.apps[self.app_pad.app_index]

    def encoder_button_event(self, event):
        if event.pressed:
            self.settings_app.put_setting(PREVIOUS_APP_SETTING, self)
            self.app_pad.current_app = self.settings_app


class MacroKey(Key):
    class BoundKey(Key.BoundKey):
        def press(self):
            self.pixel = 0xFFFFFF
            self.app.macropad.pixels.show()
            self.key.press(self.app)

        def release(self):
            self.key.release(self.app)
            self.pixel = self.color()
            self.app.macropad.pixels.show()

    def __init__(
        self,
        text="",
        color=0,
        command=None,
        linux_command=EMPTY_VALUE,
        mac_command=EMPTY_VALUE,
        windows_command=EMPTY_VALUE,
    ):
        self.command = command
        self._color = color
        self._text = text

        self.os_commands = {
            os: com if (com is not EMPTY_VALUE) else self.command
            for os, com in zip(
                (OS_LINUX, OS_MAC, OS_WINDOWS),
                (linux_command, mac_command, windows_command),
            )
        }

    @staticmethod
    def _get_os(app):
        return app.get_setting(OS_SETTING)

    def _get_command(self, app):
        os = self._get_os(app)
        return self.os_commands[os]

    def text(self, app):
        if self._get_command(app):
            return self._text
        return ""

    def color(self, app):
        if self._get_command(app):
            return self._color
        return 0

    def press(self, app):
        command = self._get_command(app)
        if command:
            command.execute(app)

    def release(self, app):
        command = self._get_command(app)
        if command:
            command.undo(app)
