"""Defines classes for each of the basic macropad commands.

A Command is a simple class with an execute method and an undo method. The
execute method runs when a key is pressed. The undo method runs when the key
is released.

"""


import time

# Expose these libraries to those that use commands
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values
from adafruit_hid.mouse import Mouse

from utils.apps.base import BaseApp
from utils.constants import OS_SETTING, PREVIOUS_APP_SETTING


class Command:
    """Simple base class representing a Command that an App can execute.

    Any command should extend this class.

    When a key is pressed, the execute method is called. When it is released,
    the undo method is called.

    """

    def execute(self, app: BaseApp):
        """Execute the command.

        Args:
            app (BaseApp): The running app

        """
        raise NotImplementedError("Command must be implemented")

    def undo(self, app: BaseApp):
        """Run cleanup actions for the command, like releasing keys, etc.

        Args:
            app (BaseApp): The running app

        """
        pass

    def __str__(self):
        return self.__class__.__name__ + "()"


class Sequence(Command):
    """Command that defines a sequence of subcommands."""

    def __init__(self, *sequence: Command):
        """Initialize the Sequence command.

        Args:
            sequence (Command): One or more commands to execute in sequence.
        """
        super().__init__()
        self.sequence = sequence

    def execute(self, app: BaseApp):
        """Execute the subcommands in sequence."""
        for command in self.sequence:
            command.execute(app)

    def undo(self, app: BaseApp):
        """Undo the subcommands in sequence"""
        for command in self.sequence:
            command.undo(app)

    def __str__(self):
        return "{0}({1})".format(
            self.__class__.__name__, ", ".join(str(com) for com in self.sequence)
        )


class Press(Command):
    """Press the given keycode. Release it to undo."""

    def __init__(self, *keycodes: int):
        """Initialize the Press command.

        Args:
            keycodes (Tuple[int, ...]): A tuple of Keycodes to press.
        """
        super().__init__()
        self.keycodes = keycodes

    def execute(self, app: BaseApp):
        """Send a keyboard press of the given keycodes."""
        for keycode in self.keycodes:
            app.macropad.keyboard.press(keycode)

    def undo(self, app: BaseApp):
        """Send a keyboard release of the given keycodes."""
        for keycode in reversed(self.keycodes):
            app.macropad.keyboard.release(keycode)

    def __str__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(map(str, self.keycodes)),
        )


class Release(Command):
    """Release the given keycode."""

    def __init__(self, *keycodes: int):
        """Initialize the Release command.

        Args:
            keycodes (Tuple[int, ...]): A tuple of Keycodes to release.
        """
        super().__init__()
        self.keycodes = keycodes

    def execute(self, app: BaseApp):
        """Send a keyboard release of the given keycode."""
        for keycode in self.keycodes:
            app.macropad.keyboard.release(keycode)

    def __str__(self):
        return "{0}({1})".format(
            self.__class__.__name__, ", ".join(map(str, self.keycodes))
        )


class Wait(Command):
    """Wait for a specified time."""

    def __init__(self, time: float):
        """Initialize the Wait command.

        Args:
            time (float): The time to wait in seconds.
        """
        super().__init__()
        self.time = time

    def execute(self, app: BaseApp):
        """Wait for the specified time."""
        time.sleep(self.time)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.time)


class Text(Command):
    """Type the specified text with the keyboard."""

    def __init__(self, text: str):
        """Initialize the Text command

        Args:
            text (str): The text to type
        """
        super().__init__()
        self.text = text

    def execute(self, app: BaseApp):
        """Type the specified text with the keyboard."""
        app.macropad.keyboard_layout.write(self.text)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.text)


class Media(Command):
    """Send the specified Media Control key."""

    def __init__(self, command: int):
        """Initialize the Media Command.

        Args:
            command (int): Value from ConsumerControlCode
        """
        super().__init__()
        self.command = command

    def execute(self, app: BaseApp):
        """Send the specified ConsumerControlCode value."""
        app.macropad.consumer_control.release()
        app.macropad.consumer_control.press(self.command)

    def undo(self, app: BaseApp):
        """Release the consumer control keys."""
        app.macropad.consumer_control.release()

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.command)


class MouseClick(Command):
    """Click the specified mouse button."""

    def __init__(self, button: int):
        """Initialize the MouseClick command.

        Args:
            button (int): A MouseButton constant defining the button to click.
        """
        super().__init__()
        self.button = button

    def execute(self, app: BaseApp):
        """Click the specified button."""
        app.macropad.mouse.press(self.button)

    def undo(self, app: BaseApp):
        """Release the specified button."""
        app.macropad.mouse.release(self.button)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.button)


class MouseMove(Command):
    """Move the mouse the specified delta in the x and y directions."""

    def __init__(self, x: int = 0, y: int = 0):
        """Initialize the MouseMove command.

        Args:
            x (int, optional): The direction to move in the x direction.
                               Defaults to 0.
            y (int, optional): The direction to move in the y direction.
                               Defaults to 0.
        """
        super().__init__()
        self.x = x
        self.y = y

    def execute(self, app: BaseApp):
        """Move the mouse by the specified amount."""
        app.macropad.mouse.move(self.x, self.y)

    def __str__(self):
        return "{0}(x={1}, y={2})".format(self.__class__.__name__, self.x, self.y)


class Scroll(Command):
    """Scroll with the mouse wheel by the specified amount."""

    def __init__(self, lines: int):
        """Initialize the Scroll command.

        Args:
            lines (int): The amount to scroll
        """
        super().__init__()
        self.lines = lines

    def execute(self, app: BaseApp):
        """Scroll by the specified amount."""
        app.macropad.mouse.move(0, 0, self.lines)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.lines)


class Tone(Command):
    """Play the specified tone through the built-in speaker."""

    def __init__(self, tone: int):
        """Initialize the Tone command.

        Args:
            tone (int): A value describing the tone to play.
        """
        super().__init__()
        self.tone = tone

    def execute(self, app: BaseApp):
        """Play the specified tone, stopping previous tones."""
        app.macropad.stop_tone()
        app.macropad.start_tone(self.tone)

    def undo(self, app: BaseApp):
        """Stop any playing tones."""
        app.macropad.stop_tone()

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.tone)


class PlayFile(Command):
    """Play a file through the built-in speaker."""

    def __init__(self, file_: str):
        """Initialize the PlayFile command.

        Args:
            file_ (str): The path to the file to play.
        """
        super().__init__()
        self.file_ = file_

    def execute(self, app: BaseApp):
        """Play the file."""
        app.macropad.play_file(self.file_)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.file_)


class AppSwitchException(Exception):
    """Raise this exception to switch the currently running app."""

    def __init__(self, app: BaseApp):
        super().__init__()
        self.app = app


class SwitchAppCommand(Command):
    """A command to switch to a new App."""

    def __init__(self, app: BaseApp):
        super().__init__()
        self.app = app

    def execute(self, app: BaseApp):
        """Switch to the new app.

        Add the current app to the stack stored in PREVIOUS_APP_SETTING.

        Args:
            app (BaseApp): The current app
        """
        try:
            app_stack = self.app.settings[PREVIOUS_APP_SETTING]
        except KeyError:
            app_stack = []
            self.app.settings[PREVIOUS_APP_SETTING] = app_stack
        app_stack.append(app)
        raise AppSwitchException(self.app)


class PreviousAppCommand(Command):
    """A command to switch back to the previous app."""

    def execute(self, app: BaseApp):
        """Switch back to the last App in the App stack.

        Pop the last App from the stack stored in PREVIOUS_APP_SETTING and
        switch back to that app.

        Args:
            app (BaseApp): The current app

        """
        app_stack = app.settings.get(PREVIOUS_APP_SETTING, [])
        previous_app = app_stack.pop()
        if previous_app is not None:
            raise AppSwitchException(previous_app)


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

    def execute(self, app: BaseApp):
        """Execute the Command.

        If the specified setting has the value of one of the keys in
        self.override_commands, the corresponding command is run. Otherwise the
        default_command is run.

        Args:
            app (BaseApp): The current app

        """
        try:
            setting = app.settings[self.setting]
            command = self.override_commands[setting]
        except Exception:
            command = self.default_command

        if command is not None:
            command.execute(app)

    def undo(self, app: BaseApp):
        """Undo the Command.

        If the specified setting has the value of one of the keys in
        self.override_commands, the corresponding command is run. Otherwise the
        default_command is run.

        Args:
            app (BaseApp): The current app

        """
        try:
            setting = app.settings[self.setting]
            command = self.override_commands[setting]
        except Exception:
            command = self.default_command

        if command is not None:
            command.undo(app)


class MacroCommand(SettingsDependentCommand):
    def __init__(self, default_command: Command, **override_commands: Command):
        super().__init__(OS_SETTING, default_command, **override_commands)
