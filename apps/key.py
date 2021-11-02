"""Defines a KeyApp which allows binding specific commands to each key.

Also defines a Key class which combines the text for the key, the color for
the key, and the command to execute for the key.
"""

try:
    from typing import List, Set, Optional, Union
except ImportError:
    pass

import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import displayio

from app_pad import AppPad
from apps.base import BaseApp
from commands import Command
from constants import DISPLAY_HEIGHT, DISPLAY_WIDTH
from event import DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent


def init_display_group_macro_app(
    display_width: int, display_height: int
) -> displayio.Group:
    """Set up displayio group with an app name and labels for each key.

    Args:
        display_width (int): The width of the display
        display_height (int): The height of the display

    Returns:
        displayio.Group: A display group"""
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
    """An App with a specific command bound to each key.

    A KeyApp has a Key instance (or None) bound to each key. You may also
    bind commands to the encoder button and the encoder rotation.

    To use this class, subclass KeyApp and specify values for each key you
    want to use.

    """

    name = "Key App"

    display_group = init_display_group_macro_app(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    # First row
    key_0: Optional["Key"] = None
    key_1: Optional["Key"] = None
    key_2: Optional["Key"] = None

    # Second row
    key_3: Optional["Key"] = None
    key_4: Optional["Key"] = None
    key_5: Optional["Key"] = None

    # Third row
    key_6: Optional["Key"] = None
    key_7: Optional["Key"] = None
    key_8: Optional["Key"] = None

    # Fourth row
    key_9: Optional["Key"] = None
    key_10: Optional["Key"] = None
    key_11: Optional["Key"] = None

    encoder_button: Optional[Command] = None

    encoder_increase: Optional[Command] = None
    encoder_decrease: Optional[Command] = None

    def __init__(self, app_pad: AppPad):
        """Initialize the KeyApp.

        Args:
            app_pad (AppPad): An AppPad instance
        """
        self.keys: List[Optional[Key.BoundKey]] = []
        self.double_tap_key_indices: Set[int] = set()

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
        """Code to execute when an app is focused.

        In addition to setting up the state of the display and pixels, instruct
        the app_pad to track double-taps for any keys with a double-tap command.

        """
        super().on_focus()
        self.app_pad.track_double_taps(self.double_tap_key_indices)

    def display_on_focus(self):
        """Set up the display when an app is focused.

        Set the display label to the name of the app, and set any key labels
        that have Keys defined.

        """
        self.display_group[13].text = self.name

        for i, key in enumerate(self.keys):
            try:
                key.label = key.text()
            except AttributeError:
                self.display_group[i].text = ""

    def pixels_on_focus(self):
        """Set up the pixels when an app is focused.

        Set the pixel colors for any keys that have Keys defined.

        """
        for i, key in enumerate(self.keys):
            try:
                key.pixel = key.color()
            except AttributeError:
                self.macropad.pixels[i] = 0

    def process_event(
        self, event: Union[DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent]
    ):
        """Process a single event.

        Args:
            event (Union[DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent]):
                An event from the app_pad
        """
        if isinstance(event, DoubleTapEvent):
            self.double_tap_event(event)
        else:
            super().process_event(event)

    def key_event(self, event: KeyEvent):
        """Process a key event.

        Delegate to the command defined on the Key.BoundKey object.

        Args:
            event (KeyEvent): An event triggered by pressing a key
        """
        key = self[event.number]

        if key is None:
            return

        if event.pressed:
            key.press()
        else:
            key.release()

    def encoder_button_event(self, event: EncoderButtonEvent):
        """Process an encoder button event.

        Delegate to the Command defined on the encoder_button attribute.

        Args:
            event (EncoderButtonEvent): An event triggered by pressing the
                encoder button
        """
        if self.encoder_button is None:
            return

        if event.pressed:
            self.encoder_button.execute(self)
        else:
            self.encoder_button.undo(self)

    def encoder_event(self, event: EncoderEvent):
        """Process an encoder event.

        Delegate to the commands defined on the encoder_increase and
        encoder_decrease attributes.

        Args:
            event (EncoderEvent): An event triggered by rotating the encoder
        """
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
        """Process a double tap event.

        Delegate to the command defined on the Key.BoundKey object.

        Args:
            event (DoubleTapEvent): An event triggered by double-tapping a key
        """
        key = self[event.number]

        if key is None:
            return

        if event.pressed:
            key.double_tap()
        else:
            key.double_tap_release()


class Key:
    """A class representing a key on a macropad.

    A Key has a label, a color for the pixel, a Command that executes when the
    key is pressed, and an optional double-tap Command that is executed when
    the key is pressed twice quickly.

    """

    class BoundKey:
        """A class representing a Key bound to a specific App and key number."""

        def __init__(self, key: "Key", app: KeyApp, key_number: int):
            """Initialize the BoundKey.

            Args:
                key (Key): A Key instance to bind to the App
                app (KeyApp): The App to bind the key to
                key_number (int): The number of the key

            """
            self.key = key
            self.app = app
            self.key_number = key_number

        @property
        def pixel(self) -> int:
            """Access the pixel on the app pad for the bound key.

            Returns:
                int: The color value for the pixel

            """
            return self.app.macropad.pixels[self.key_number]

        @pixel.setter
        def pixel(self, color: int):
            """Set the valud for the pixel on the app pad.

            Args:
                color (int): The color value for the pixel

            """
            self.app.macropad.pixels[self.key_number] = color

        @property
        def label(self) -> str:
            """Return the label text for the key currently in the display group.

            Returns:
                str: The currently displayed label text

            """
            self.app.display_group[self.key_number].text

        @label.setter
        def label(self, text: str):
            """Set the value for the label text on the app display group.

            Args:
                text (str): The text for the label

            """
            self.app.display_group[self.key_number].text = text

        def text(self) -> str:
            """Return the text for the key.

            Returns:
                str: The text for the key

            """
            return self.key.text(self.app)

        def color(self) -> int:
            """Return the color value defined for the key.

            Returns:
                int: The color value for the key
            """
            return self.key.color(self.app)

        def press(self):
            """Execute the Command defined for the key."""
            self.key.press(self.app)

        def release(self):
            """Undo the Command defined for the key."""
            self.key.release(self.app)

        def double_tap(self):
            """Execute the double-tap command defined for the key."""
            self.key.double_tap(self.app)

        def double_tap_release(self):
            """Undo the double-tap command defined for the key."""
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
        """Initialize the Key.

        Args:
            text (str, optional): The text for the label of the Key.
                Defaults to "".
            color (int, optional): The color value for the Key. Defaults to 0.
            command (Optional[Command], optional): The Command to execute when
                pressing the key. Defaults to None.
            double_tap_command (Optional[Command], optional): The Command to
                execute when double-tapping a Key. Defaults to None.

        """
        self.command = command
        self.double_tap_command = double_tap_command
        self._color = color
        self._text = text

    def text(self, app: KeyApp) -> str:
        """Return the text for the label of this key.

        Args:
            app (KeyApp): A KeyApp instance

        Returns:
            str: The text associated with this Key
        """
        return self._text

    def color(self, app: KeyApp) -> int:
        """Return the color for the pixel of this Key.

        Args:
            app (KeyApp): A KeyApp instance

        Returns:
            int: The color associated with this Key
        """
        return self._color

    def press(self, app: KeyApp):
        """Execute the command for this Key.

        Args:
            app (KeyApp): A KeyApp instance

        """
        if self.command:
            self.command.execute(app)

    def release(self, app: KeyApp):
        """Undo the command for this Key.

        Args:
            app (KeyApp): A KeyApp instance

        """
        if self.command:
            self.command.undo(app)

    def double_tap(self, app: KeyApp):
        """Execute the double-tap command for this Key.

        Args:
            app (KeyApp): A KeyApp instance

        """
        if self.double_tap_command:
            self.double_tap_command.execute(app)

    def double_tap_release(self, app):
        """Undo the double-tap command for this Key.

        Args:
            app (KeyApp): A KeyApp instance

        """
        if self.double_tap_command:
            self.double_tap_release(app)

    def bind(self, app: KeyApp, key_number: int) -> BoundKey:
        """Bind this Key to a KeyApp and return a BoundKey instance.

        Args:
            app (KeyApp): The KeyApp to bind to
            key_number (int): The number of the key to bind to

        Returns:
            BoundKey: A BoundKey instance, containing references to the App
                and the key number
        """
        return self.BoundKey(self, app, key_number)
