import os

import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

from constants import DISPLAY_HEIGHT, DISPLAY_WIDTH
from event import EncoderEvent, EncoderButtonEvent, KeyEvent


def init_display_group_base_app(display_width, display_height):
    """Set up displayio group with all the labels."""
    group = displayio.Group()
    group.append(Rect(0, 0, display_width, 12, fill=0xFFFFFF))
    group.append(
        label.Label(
            terminalio.FONT,
            text="",
            color=0x000000,
            anchored_position=(display_height // 2, -2),
            anchor_point=(0.5, 0.0),
        )
    )

    return group


class BaseApp:
    display_group = init_display_group_base_app(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    name = "Base App"

    @staticmethod
    def load_apps(directory):
        """Load all the macro key setups from .py files in directory.

        Args:
            directory (str): The directory from which to load macros.

        Returns:
            List[BaseApp]: A list of BaseApp objects
        """
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                try:
                    __import__(directory + "/" + filename[:-3])
                except (
                    SyntaxError,
                    ImportError,
                    AttributeError,
                    KeyError,
                    NameError,
                    IndexError,
                    TypeError,
                ) as err:
                    print("Error loading %s" % filename)
                    print(err)

        apps = BaseApp.list_registered_apps()

        for app in apps:
            print("Loaded %s" % app.name)

        return apps

    @staticmethod
    def register_app(app_class):
        try:
            BaseApp._registered_apps.add(app_class)
        except AttributeError:
            BaseApp._registered_apps = {app_class}

        return app_class

    @staticmethod
    def list_registered_apps():
        """Return a list of the apps that have been registered.

        Returns:
            List[BaseApp]: A list of apps that have been registered, sorted by name
        """
        try:
            return list(sorted(BaseApp._registered_apps, key=lambda app: app.name))
        except AttributeError:
            return []

    def __init__(self, app_pad):
        self.app_pad = app_pad
        self.macropad = app_pad.macropad

    def run(self):
        self.on_focus()

        while True:
            for event in self.app_pad.check_events():
                self.process_event(event)

    def on_focus(self):
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()

        self.display_on_focus()
        self.macropad.display.show(self.display_group)
        self.macropad.display.refresh()

        self.pixels_on_focus()
        self.macropad.pixels.show()

    def display_on_focus(self):
        self.display_group[0].text = self.name

    def pixels_on_focus(self):
        for i in range(12):
            self.macropad.pixels[i] = 0

    def process_event(self, event):
        if isinstance(event, EncoderEvent):
            self.encoder_event(event)
        elif isinstance(event, EncoderButtonEvent):
            self.encoder_button_event(event)
        elif isinstance(event, KeyEvent):
            self.key_event(event)

    def encoder_event(self, event):
        pass

    def encoder_button_event(self, event):
        pass

    def key_event(self, event):
        if event.pressed:
            self.key_press(event.number)
        else:
            self.key_release(event.number)

    def key_press(self, key_number):
        pass

    def key_release(self, key_number):
        pass
