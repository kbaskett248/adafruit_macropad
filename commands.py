import time

# Expose these libraries to those that use commands
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode  # REQUIRED if using Keycode.* values
from adafruit_hid.mouse import Mouse
from apps.base import BaseApp
from apps.settings import KeyAppWithSettings
from constants import PREVIOUS_APP_SETTING


class Command:
    def execute(self, app):
        raise NotImplementedError("Command must be implemented")

    def undo(self, app):
        pass

    def __str__(self):
        return self.__class__.__name__ + "()"


class Sequence(Command):
    sequence = []

    def __init__(self, *sequence):
        super().__init__()
        self.sequence = sequence

    def execute(self, app):
        for command in self.sequence:
            command.execute(app)

    def undo(self, app):
        for command in self.sequence:
            command.undo(app)

    def __str__(self):
        return "{0}({1})".format(
            self.__class__.__name__, ", ".join(str(com) for com in self.sequence)
        )


class Press(Command):
    keycode = None

    def __init__(self, keycode):
        super().__init__()
        self.keycode = keycode

    def execute(self, app):
        app.macropad.keyboard.press(self.keycode)

    def undo(self, app):
        app.macropad.keyboard.release(self.keycode)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.keycode)


class Release(Command):
    keycode = None

    def __init__(self, keycode):
        super().__init__()
        self.keycode = keycode

    def execute(self, app):
        app.macropad.keyboard.release(self.keycode)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.keycode)


class Wait(Command):
    time = 0

    def __init__(self, time):
        super().__init__()
        self.time = time

    def execute(self, app):
        time.sleep(self.time)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.time)


class Text(Command):
    text = ""

    def __init__(self, text):
        super().__init__()
        self.text = text

    def execute(self, app):
        app.macropad.keyboard_layout.write(self.text)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.text)


class Media(Command):
    command = None

    def __init__(self, command):
        super().__init__()
        self.command = command

    def execute(self, app):
        app.macropad.consumer_control.release()
        app.macropad.consumer_control.press(self.command)

    def undo(self, app):
        app.macropad.consumer_control.release()

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.command)


class MouseClick(Command):
    button = None

    def __init__(self, button):
        super().__init__()
        self.button = button

    def execute(self, app):
        app.macropad.mouse.press(self.button)

    def undo(self, app):
        app.macropad.mouse.release(self.button)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.button)


class MouseMove(Command):
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    def execute(self, app):
        app.macropad.mouse.move(self.x, self.y)

    def __str__(self):
        return "{0}(x={1}, y={2})".format(self.__class__.__name__, self.x, self.y)


class Scroll(Command):
    lines = 0

    def __init__(self, lines):
        super().__init__()
        self.lines = lines

    def execute(self, app):
        app.macropad.mouse.move(0, 0, self.lines)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.lines)


class Tone(Command):
    tone = 0

    def __init__(self, tone):
        super().__init__()
        self.tone = tone

    def execute(self, app):
        app.macropad.stop_tone()
        app.macropad.start_tone(self.tone)

    def undo(self, app):
        app.macropad.stop_tone()

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.tone)


class PlayFile(Command):
    file_ = None

    def __init__(self, file_):
        super().__init__()
        self.file_ = file_

    def execute(self, app):
        app.macropad.play_file(self.file_)

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.file_)


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
