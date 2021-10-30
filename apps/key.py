"""
KeyApp is a basic framework for apps with functionality bound to each key.
"""

try:
    from typing import Optional
except ImportError:
    pass

from app_pad import AppPad
from commands import Command
import displayio
from event import DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

from apps.base import BaseApp
from constants import DISPLAY_HEIGHT, DISPLAY_WIDTH


def init_display_group_macro_app(display_width, display_height):
    """Set up displayio group with all the labels."""
    group = displayio.Group()
    for key_index in range(12):
        x = key_index % 3
        y = key_index // 3

        group.append(
            label.Label(
                terminalio.FONT,
                text="",
                color=0xFFFFFF,
                anchored_position=(
                    (display_width - 1) * x / 2,
                    display_height - 1 - (4 - y) * 12,
                ),
                anchor_point=(x / 2, 1.0),
            )
        )
    group.append(Rect(0, display_height - 11, display_width, 12, fill=0xFFFFFF))
    group.append(
        label.Label(
            terminalio.FONT,
            text="",
            color=0x000000,
            anchored_position=(display_width // 2, display_height),
            anchor_point=(0.5, 1.0),
        )
    )

    return group


class KeyApp(BaseApp):
    name = "Key App"

    display_group = init_display_group_macro_app(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    # First row
    key_0 = None
    key_1 = None
    key_2 = None

    # Second row
    key_3 = None
    key_4 = None
    key_5 = None

    # Third row
    key_6 = None
    key_7 = None
    key_8 = None

    # Fourth row
    key_9 = None
    key_10 = None
    key_11 = None

    encoder_button: Optional[Command] = None

    encoder_increase: Optional[Command] = None
    encoder_decrease: Optional[Command] = None

    def __init__(self, app_pad: AppPad):
        self.keys = []
        self.double_tap_key_indices = set()

        for index in range(12):
            key = getattr(self, "key_%s" % index)

            try:
                bound_key = key.bind(self, index)
            except AttributeError:
                bound_key = None
            else:
                if key.double_tap_command is not None:
                    self.double_tap_key_indices.add(index)

            self.keys.append(bound_key)

        super().__init__(app_pad)

    def __getitem__(self, index):
        try:
            return self.keys[index]
        except IndexError as err:
            if 0 <= index <= 11:
                return None
            raise err

    def __iter__(self):
        return iter(self.keys)

    def __len__(self):
        return len(self.keys)

    def on_focus(self):
        super().on_focus()
        self.app_pad.track_double_taps(self.double_tap_key_indices)

    def display_on_focus(self):
        self.display_group[13].text = self.name

        for i, key in enumerate(self.keys):
            try:
                key.label = key.text()
            except AttributeError:
                self.display_group[i].text = ""

    def pixels_on_focus(self):
        for i, key in enumerate(self.keys):
            try:
                key.pixel = key.color()
            except AttributeError:
                self.macropad.pixels[i] = 0

    def process_event(self, event):
        if isinstance(event, DoubleTapEvent):
            self.double_tap_event(event)
        else:
            super().process_event(event)

    def key_event(self, event: KeyEvent):
        key = self[event.number]

        if key is None:
            return

        if event.pressed:
            key.press()
        else:
            key.release()

    def encoder_button_event(self, event: EncoderButtonEvent):
        if self.encoder_button is None:
            return

        if event.pressed:
            self.encoder_button.execute(self)
        else:
            self.encoder_button.undo(self)

    def encoder_event(self, event: EncoderEvent):
        if (
            event.position > event.previous_position
            and self.encoder_increase is not None
        ):
            self.encoder_increase.execute(self)
            self.encoder_increase.undo(self)
        elif (
            event.position < event.previous_position
            and self.encoder_decrease is not None
        ):
            self.encoder_decrease.execute(self)
            self.encoder_decrease.undo(self)

    def double_tap_event(self, event: DoubleTapEvent):
        key = self[event.number]

        if key is None:
            return

        if event.pressed:
            key.double_tap()
        else:
            key.double_tap_release()


class Key:
    class BoundKey:
        def __init__(self, key: "Key", app: KeyApp, key_number: int):
            self.key = key
            self.app = app
            self.key_number = key_number

        @property
        def pixel(self):
            return self.app.macropad.pixels[self.key_number]

        @pixel.setter
        def pixel(self, color):
            self.app.macropad.pixels[self.key_number] = color

        @property
        def label(self):
            self.app.display_group[self.key_number].text

        @label.setter
        def label(self, text):
            self.app.display_group[self.key_number].text = text

        def text(self):
            return self.key.text(self.app)

        def color(self):
            return self.key.color(self.app)

        def press(self):
            self.key.press(self.app)

        def release(self):
            self.key.release(self.app)

        def double_tap(self):
            self.key.double_tap(self.app)

        def double_tap_release(self):
            self.key.double_tap_release(self.app)

        def __str__(self) -> str:
            return f"{self.__class__.__name__}({self.key_number} - {self.key})"

    def __init__(
        self,
        text: str = "",
        color: int = 0,
        command: Optional[Command] = None,
        double_tap_command: Optional[Command] = None,
    ):
        self.command = command
        self.double_tap_command = double_tap_command
        self._color = color
        self._text = text

    def text(self, app):
        return self._text

    def color(self, app):
        return self._color

    def press(self, app):
        if self.command:
            self.command.execute(app)

    def release(self, app):
        if self.command:
            self.command.undo(app)

    def double_tap(self, app):
        if self.double_tap_command:
            self.double_tap_command.execute(app)

    def double_tap_release(self, app):
        if self.double_tap_command:
            self.double_tap_release(app)

    def bind(self, app: KeyApp, key_number: int):
        return self.BoundKey(self, app, key_number)
