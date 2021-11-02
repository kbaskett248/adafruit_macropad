"""Defines a KeyApp that includes customizable settings.

Also includes special Key subclasses and Command subclasses to interact with
settings.
"""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass

from app_pad import AppPad
from apps.key import KeyApp, Key
from commands import Command
from constants import PREVIOUS_APP_SETTING


class KeyAppWithSettings(KeyApp):
    """A KeyApp that supports customizable settings."""

    name = "Base Settings"

    def __init__(self, app_pad: AppPad, settings: Optional[Dict[str, Any]] = None):
        if settings is None:
            self.settings = {}
        else:
            self.settings = settings

        super().__init__(app_pad)

    def get_setting(self, setting):
        return self.settings.get(setting, None)

    def put_setting(self, setting, value):
        self.settings[setting] = value


class SettingsValueKey(Key):
    def __init__(
        self,
        setting: str,
        command: Optional[Command] = None,
        double_tap_command: Optional[Command] = None,
        color_mapping: Optional[Dict[str, int]] = None,
        text_template: str = "{value}",
    ):
        super().__init__(command=command, double_tap_command=double_tap_command)
        self.setting = setting
        self.color_mapping = color_mapping
        self.text_template = text_template

    def text(self, app) -> str:
        return self.text_template.format(
            setting=self.setting, value=app.get_setting(self.setting)
        )

    def color(self, app) -> int:
        if self.color_mapping is not None:
            return self.color_mapping.get(app.get_setting(self.setting), 0)
        return 0


class SettingsSelectKey(Key):
    setting = ""
    value = None
    marker = ">"
    template = "{marker} {text}"

    class BoundKey(Key.BoundKey):
        def __init__(self, key, app, key_number):
            super().__init__(key, app, key_number)
            self.related_keys = set()

            setting = key.setting
            for bound_key in app.keys:
                if not isinstance(bound_key, SettingsSelectKey.BoundKey):
                    continue

                if bound_key.key.setting == setting:
                    self.related_keys.add(bound_key)
                    bound_key.related_keys.add(self)

        def press(self):
            self.key.press(self.app)
            self.pixel = self.color()
            self.label = self.text()

            for key in self.related_keys:
                key.pixel = key.color()
                key.label = key.text()

            self.app.macropad.display.refresh()
            self.app.macropad.pixels.show()

    def __init__(self, text="", color=0, setting="", value=None, command=None):
        super().__init__(text, color, command)
        self.setting = setting
        self.value = value

    def text(self, app):
        if app.get_setting(self.setting) == self.value:
            marker = self.marker
        else:
            marker = " "

        return self.template.format(marker=marker, text=self._text)

    def color(self, app):
        if app.get_setting(self.setting) == self.value:
            return self._color
        else:
            return 0

    def press(self, app):
        app.put_setting(self.setting, self.value)
        super().press(app)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.setting}: {self.value})"


class SwitchAppCommand(Command):
    def __init__(self, app: KeyAppWithSettings) -> None:
        super().__init__()
        self.app = app

    def execute(self, app: KeyAppWithSettings):
        app_stack = self.app.get_setting(PREVIOUS_APP_SETTING)
        app_stack.append(app)
        app.app_pad.current_app = self.app


class PreviousAppCommand(Command):
    def execute(self, app: KeyAppWithSettings):
        app_stack = app.get_setting(PREVIOUS_APP_SETTING)
        previous_app = app_stack.pop()
        if previous_app is not None:
            app.app_pad.current_app = previous_app


class SettingsDependentCommand(Command):
    def __init__(
        self, setting: str, default_command: Command, **override_commands: Command
    ):
        self.setting = setting
        self.default_command = default_command
        self.override_commands = override_commands

    def execute(self, app: KeyAppWithSettings):
        try:
            setting = app.get_setting(self.setting)
            command = self.override_commands[setting]
        except Exception:
            command = self.default_command

        command.execute(app)

    def undo(self, app: KeyAppWithSettings):
        try:
            setting = app.get_setting(self.setting)
            command = self.override_commands[setting]
        except Exception:
            command = self.default_command

        command.undo(app)
