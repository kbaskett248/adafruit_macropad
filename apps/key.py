"""
KeyApp is a basic framework for apps with functionality bound to each key.
"""

import displayio
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

    def __init__(self, app_pad):
        self.keys = []
        for index in range(12):
            self.keys.append(self[index])

        super().__init__(app_pad)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise IndexError("Index %s is not an int" % index)
        return getattr(self, "key_%s" % index)

    def __iter__(self):
        return iter(self.keys)

    def __len__(self):
        return len(self.keys)

    def display_on_focus(self):
        self.display_group[13].text = self.name

        for i, labeled_key in enumerate(self.keys):
            try:
                text = labeled_key.text(self)
            except AttributeError:
                text = ""
            finally:
                self.display_group[i].text = text

    def pixels_on_focus(self):
        for i, labeled_key in enumerate(self.keys):
            try:
                color = labeled_key.color(self)
            except AttributeError:
                color = 0
            finally:
                self.macropad.pixels[i] = color

    def key_event(self, event):
        try:
            key = self[event.number]
        except IndexError:
            return

        if key is None:
            return

        if event.pressed:
            self.key_press(key, event.number)
        else:
            self.key_release(key, event.number)

    def key_press(self, key, key_number):
        pass

    def key_release(self, key, key_number):
        pass
