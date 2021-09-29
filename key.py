import time


class Command:
    def execute(self, macropad):
        raise NotImplementedError("Command must be implemented")

    def undo(self, macropad):
        pass


class Sequence(Command):
    sequence = []

    def __init__(self, *sequence):
        super().__init__()
        self.sequence = sequence

    def execute(self, macropad):
        for command in self.sequence:
            command.execute(macropad)

    def undo(self, macropad):
        for command in self.sequence:
            command.undo(macropad)


class Press(Command):
    keycode = None

    def __init__(self, keycode):
        super().__init__()
        self.keycode = keycode

    def execute(self, macropad):
        macropad.keyboard.press(self.keycode)

    def undo(self, macropad):
        macropad.keyboard.release(self.keycode)


class Release(Command):
    keycode = None

    def __init__(self, keycode):
        super().__init__()
        self.keycode = keycode

    def execute(self, macropad):
        macropad.keyboard.release(self.keycode)


class Wait(Command):
    time = 0

    def __init__(self, time):
        super().__init__()
        self.time = time

    def execute(self, macropad):
        time.sleep(self.time)


class Text(Command):
    text = ""

    def __init__(self, text):
        super().__init__()
        self.text = text

    def execute(self, macropad):
        macropad.keyboard_layout.write(self.text)


class Media(Command):
    command = None

    def __init__(self, command):
        super().__init__()
        self.command = command

    def execute(self, macropad):
        macropad.consumer_control.release()
        macropad.consumer_control.press(self.command)


class MouseClick(Command):
    button = None

    def __init__(self, button):
        super().__init__()
        self.button = button

    def execute(self, macropad):
        macropad.mouse.press(self.button)

    def undo(self, macropad):
        macropad.mouse.release(self.button)


class MouseMove(Command):
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    def execute(self, macropad):
        macropad.mouse.move(self.x, self.y)


class Scroll(Command):
    lines = 0

    def __init__(self, lines):
        super().__init__()
        self.lines = lines

    def execute(self, macropad):
        macropad.mouse.move(0, 0, self.lines)


class Tone(Command):
    tone = 0

    def __init__(self, tone):
        super().__init__()
        self.tone = tone

    def execute(self, macropad):
        macropad.stop_tone()
        macropad.start_tone(self.tone)

    def undo(self, macropad):
        macropad.stop_tone()


class PlayFile(Command):
    file_ = None

    def __init__(self, file_):
        super().__init__()
        self.file_ = file_

    def execute(self, macropad):
        macropad.play_file(self.file_)


class Key:
    color = 0
    command = None

    def __init__(self, color=0, command=None):
        self.command = command
        self.color = color

    def press(self, macropad):
        if self.command:
            self.command.execute(macropad)

    def release(self, macropad):
        if self.command:
            self.command.undo(macropad)


class LabeledKey(Key):
    text = ""

    def __init__(self, text="", color=0, command=None):
        super().__init__(color, command)
        self.text = text
