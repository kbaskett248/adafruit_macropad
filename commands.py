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

from apps.base import BaseApp


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

    def __init__(self, keycode: int):
        """Initialize the Press command.

        Args:
            keycode (int): The Keycode of the key to press.
        """
        super().__init__()
        self.keycode = keycode

    def execute(self, app: BaseApp):
        """Send a keyboard press of the given keycode."""
        app.macropad.keyboard.press(self.keycode)

    def undo(self, app: BaseApp):
        """Send a keyboard release of the given keycode."""
        app.macropad.keyboard.release(self.keycode)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.keycode)


class Release(Command):
    """Release the given keycode."""

    def __init__(self, keycode: int):
        """Initialize the Release command.

        Args:
            keycode (int): A Keycode value for the key to release.
        """
        super().__init__()
        self.keycode = keycode

    def execute(self, app: BaseApp):
        """Send a keyboard release of the given keycode."""
        app.macropad.keyboard.release(self.keycode)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.keycode)


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
