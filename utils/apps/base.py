"""
Includes a BaseApp implementation which handles the basic app run loop.
"""

import os

from utils.settings import BaseSettings

try:
    from typing import Iterable, List, Optional, Union
except ImportError:
    pass

import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

from utils.app_pad import (
    AppPad,
    DoubleTapEvent,
    EncoderButtonEvent,
    EncoderEvent,
    KeyEvent,
)
from utils.constants import DISPLAY_HEIGHT, DISPLAY_WIDTH


def init_display_group_base_app(
    display_width: int, display_height: int
) -> displayio.Group:
    """Set up a displayio group with a single label."""
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
    def load_apps(directory: str) -> Iterable["BaseApp"]:
        """Load all the macro key setups from .py files in directory.

        Args:
            directory (str): The directory from which to load macros.

        Returns:
            Iterable[BaseApp]: A list of BaseApp objects that were registered.
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
    def register_app(app_class: "BaseApp") -> "BaseApp":
        """Register the specified app to the internal app list.

        Intended to be used as a decorator.

        Args:
            app_class (BaseApp): [description]

        Returns:
            [BaseApp]: The app that was registered
        """
        try:
            BaseApp._registered_apps.add(app_class)
        except AttributeError:
            BaseApp._registered_apps = {app_class}

        return app_class

    @staticmethod
    def list_registered_apps() -> List["BaseApp"]:
        """Return a list of the apps that have been registered.

        Returns:
            List[BaseApp]: A list of apps that have been registered,
                           sorted by name
        """
        try:
            return list(sorted(BaseApp._registered_apps, key=lambda app: app.name))
        except AttributeError:
            return []

    def __init__(self, app_pad: AppPad, settings: Optional[BaseSettings] = None):
        """Initialize the App.

        Args:
            app_pad (AppPad): An AppPad instance
            settings (Optional[BaseSettings]): The settings for the app.
                If you pass None, an empty settings object is created.
        """
        self.app_pad = app_pad
        self.macropad = app_pad.macropad

        if settings is None:
            self.settings = BaseSettings()
        else:
            self.settings = settings

    def run(self):
        """The main run loop for the app.

        Checks the app_pad object for any new events, then processes them.
        """
        self.on_focus()

        for event in self.app_pad.event_stream():
            self.process_event(event)

    def on_focus(self):
        """Code to execute when an app is focused.

        Resets the state of commands.
        Sets up the display.
        Sets up the pixels.

        """
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
        """Set up the display when an app is focused.

        Set the display label to the name of the app.

        """
        self.display_group[0].text = self.name

    def pixels_on_focus(self):
        """Set up the pixels when an app is focused.

        Disable the pixel for all the keys.

        """
        for i in range(12):
            self.macropad.pixels[i] = 0

    def process_event(
        self, event: Union[DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent]
    ):
        """Process a single event.

        Args:
            event (Union[DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent]):
                An event from the App Pad
        """
        if isinstance(event, EncoderEvent):
            self.encoder_event(event)
        elif isinstance(event, EncoderButtonEvent):
            self.encoder_button_event(event)
        elif isinstance(event, KeyEvent):
            self.key_event(event)
        elif isinstance(event, DoubleTapEvent):
            self.double_tap_event(event)

    def encoder_event(self, event: EncoderEvent):
        """Process an encoder event.

        Args:
            event (EncoderEvent): An event triggered by rotating the encoder
        """
        pass

    def encoder_button_event(self, event: EncoderButtonEvent):
        """Process an encoder button event.

        Args:
            event (EncoderButtonEvent): An event triggered by pressing the
                encoder button
        """
        pass

    def key_event(self, event: KeyEvent):
        """Process a key event.

        Args:
            event (KeyEvent): An event triggered by pressing a key
        """
        pass

    def double_tap_event(self, event: DoubleTapEvent):
        """Process a double tap event.

        Args:
            event (DoubleTapEvent): An event triggered by double-tapping a key
        """
        pass
