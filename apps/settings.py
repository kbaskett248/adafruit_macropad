"""Defines a KeyApp that includes customizable settings.

Also includes special Key subclasses and Command subclasses to interact with
settings.
"""

try:
    from typing import Any, Dict, Optional, Set
except ImportError:
    pass

from app_pad import AppPad
from apps.key import KeyApp, Key
from commands import Command
from constants import PREVIOUS_APP_SETTING


class KeyAppWithSettings(KeyApp):
    """A KeyApp that supports customizable settings.

    Settings are a dictionary. Apps can share settings by passing the same
    dictionary to each of them.

    """

    name = "Base Settings"

    def __init__(self, app_pad: AppPad, settings: Optional[Dict[str, Any]] = None):
        """Initialize the Key App with Settings.

        Args:
            app_pad (AppPad): An AppPad instance
            settings (Optional[Dict[str, Any]], optional): Settings dictionary.
                If you pass None, the settings dictionary is initialized to an
                empty dictionary. Defaults to None.
        """
        if settings is None:
            self.settings = {}
        else:
            self.settings = settings

        super().__init__(app_pad)

    def get_setting(self, setting: str) -> Any:
        """Return the setting value with the given name.

        If the setting isn't defined, None is returned.

        Args:
            setting (str): The setting name

        Returns:
            Any: The value for the setting, or None if it isn't defined
        """
        return self.settings.get(setting, None)

    def put_setting(self, setting: str, value: Any):
        """Store the value as a setting with the given name.

        Args:
            setting (str): The setting name
            value (Any): The value for the setting
        """
        self.settings[setting] = value


class SettingsValueKey(Key):
    """A Key whose color and text are dependent on the value of a setting.

    The text of the key is the value of the setting. The color of the key is
    the color determined by the value of the setting using color_mapping.

    """

    def __init__(
        self,
        setting: str,
        command: Optional[Command] = None,
        double_tap_command: Optional[Command] = None,
        color_mapping: Optional[Dict[str, int]] = None,
        text_template: str = "{value}",
    ):
        """Initialize the SettingsValueKey.

        Args:
            setting (str): The name of the setting
            command (Optional[Command], optional): A Command to execute when
                the key is pressed. Defaults to None.
            double_tap_command (Optional[Command], optional): A command to
                execute when the key is double-tapped. Defaults to None.
            color_mapping (Optional[Dict[str, int]], optional): A dictionary
                mapping values for the setting to color codes. If None the key
                will have no color. Defaults to None.
            text_template (str, optional): A template string to determine the
                text for the key. The keys for the template string are setting
                and value. Defaults to "{value}".

        """
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
    """A key which stores a value to a setting when pressed.

    Multiple keys can be linked to the same setting. The text and color for all
    keys will be updated whenever the key is pressed.

    """

    marker = ">"
    template = "{marker} {text}"

    class BoundKey(Key.BoundKey):
        """A SettingsSelectKey bound to a specific app and key number."""

        def __init__(
            self, key: "SettingsSelectKey", app: KeyAppWithSettings, key_number: int
        ):
            """Initialize the BoundKey.

            Args:
                key (SettingsSelectKey): A SettingsSelectKey instance
                app (KeyAppWithSettings): A KeyAppWithSettings instance to bind
                    to
                key_number (int): The key number to bind to
            """
            super().__init__(key, app, key_number)
            self.related_keys: Set[SettingsSelectKey.BoundKey] = set()

            setting = key.setting
            for bound_key in app.keys:
                if not isinstance(bound_key, SettingsSelectKey.BoundKey):
                    continue

                if bound_key.key.setting == setting:
                    self.related_keys.add(bound_key)
                    bound_key.related_keys.add(self)

        def press(self):
            """Logic to run when the key is pressed.

            Update the setting associated with the key.
            Optionally run the command tied to the key.
            Update the text and pixel for the key and any related keys.

            """
            self.key.press(self.app)
            self.pixel = self.color()
            self.label = self.text()

            for key in self.related_keys:
                key.pixel = key.color()
                key.label = key.text()

            self.app.macropad.display.refresh()
            self.app.macropad.pixels.show()

    def __init__(
        self,
        text: str = "",
        color: int = 0,
        setting: str = "",
        value: Any = None,
        command: Optional[Command] = None,
    ):
        """Initialize the SettingsSelectKey.

        Args:
            text (str, optional): The text to display for the key.
                Defaults to "".
            color (int, optional): The color to display when the value is the
                current setting. Defaults to 0.
            setting (str, optional): The name of the setting. Defaults to "".
            value (Any, optional): The value of the setting. Defaults to None.
            command (Optional[Command], optional): An additional command to run
                when the key is pressed. Defaults to None.

        """
        super().__init__(text, color, command)
        self.setting = setting
        self.value = value

    def text(self, app: KeyAppWithSettings) -> str:
        """The text to display for the key.

        If the key's value is the current value for the setting, a marker is
        added to the key's text to indicate it is selected.

        Args:
            app (KeyAppWithSettings): An instance of KeyAppWithSettings

        Returns:
            str: The text to display for the key.

        """
        if app.get_setting(self.setting) == self.value:
            marker = self.marker
        else:
            marker = " "

        return self.template.format(marker=marker, text=self._text)

    def color(self, app: KeyAppWithSettings) -> int:
        """The color of the key's pixel.

        If the key's value is the current value for the setting, the key's
        color is displayed. Otherwise no color is displayed.

        Args:
            app (KeyAppWithSettings): An instance of KeyAppWithSettings

        Returns:
            int: The color to display for the key's pixel

        """
        if app.get_setting(self.setting) == self.value:
            return self._color
        return 0

    def press(self, app: KeyAppWithSettings):
        """Update the setting for the key. Then run the command for the key.

        Args:
            app (KeyAppWithSettings): An instance of KeyAppWithSettings.

        """
        app.put_setting(self.setting, self.value)
        super().press(app)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.setting}: {self.value})"


class SwitchAppCommand(Command):
    """A command to switch to a new App."""

    def __init__(self, app: KeyAppWithSettings):
        super().__init__()
        self.app = app

    def execute(self, app: KeyAppWithSettings):
        """Switch to the new app.

        Add the current app to the stack stored in PREVIOUS_APP_SETTING.

        Args:
            app (KeyAppWithSettings): The current app
        """
        app_stack = self.app.get_setting(PREVIOUS_APP_SETTING)
        app_stack.append(app)
        app.app_pad.current_app = self.app


class PreviousAppCommand(Command):
    """A command to switch back to the previous app."""

    def execute(self, app: KeyAppWithSettings):
        """Switch back to the last App in the App stack.

        Pop the last App from the stack stored in PREVIOUS_APP_SETTING and
        switch back to that app.

        Args:
            app (KeyAppWithSettings): The current app

        """
        app_stack = app.get_setting(PREVIOUS_APP_SETTING)
        previous_app = app_stack.pop()
        if previous_app is not None:
            app.app_pad.current_app = previous_app


class SettingsDependentCommand(Command):
    """A command which can run different override commands depending on the
    value of a setting.

    """

    def __init__(
        self, setting: str, default_command: Command, **override_commands: Command
    ):
        """Initialize the SettingsDependentCommand.

        Args:
            setting (str): The setting name to check
            default_command (Command): A default command to run if the setting
                doesn't match an override command.
            override_commands (Dict[str, Command]): A dictionary mapping a
                settings value to a Command. If the specified setting has the
                value of one of these keys, the corresponding command is run.
                Otherwise the default_command is run.

        """
        self.setting = setting
        self.default_command = default_command
        self.override_commands = override_commands

    def execute(self, app: KeyAppWithSettings):
        """Execute the Command.

        If the specified setting has the value of one of the keys in
        self.override_commands, the corresponding command is run. Otherwise the
        default_command is run.

        Args:
            app (KeyAppWithSettings): The current app

        """
        try:
            setting = app.get_setting(self.setting)
            command = self.override_commands[setting]
        except Exception:
            command = self.default_command

        if command is not None:
            command.execute(app)

    def undo(self, app: KeyAppWithSettings):
        """Undo the Command.

        If the specified setting has the value of one of the keys in
        self.override_commands, the corresponding command is run. Otherwise the
        default_command is run.

        Args:
            app (KeyAppWithSettings): The current app

        """
        try:
            setting = app.get_setting(self.setting)
            command = self.override_commands[setting]
        except Exception:
            command = self.default_command

        if command is not None:
            command.undo(app)
