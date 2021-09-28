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


class Key:
    text = ""
    color = 0
    command = None
