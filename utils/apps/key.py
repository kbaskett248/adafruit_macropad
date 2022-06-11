"""Defines a KeyApp which allows binding specific commands to each key.

Also defines a Key class which combines the text for the key, the color for
the key, and the command to execute for the key.
"""

try:
    from typing import Any, Dict, List, Optional, Set, Union
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
from utils.apps.base import BaseApp
from utils.commands import Command
from utils.constants import (
    COLOR_1,
    COLOR_2,
    COLOR_3,
    COLOR_4,
    COLOR_5,
    COLOR_6,
    COLOR_7,
    COLOR_8,
    COLOR_9,
    COLOR_10,
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    EMPTY_VALUE,
    ONE_MINUTE,
    OS_LINUX,
    OS_MAC,
    OS_WINDOWS,
    TIMER_DISABLE_PIXELS,
)
from utils.settings import BaseSettings


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


class KeyAppSettings(BaseSettings):
    color_scheme: Dict[str, int] = {
        COLOR_1: 0x4D0204,
        COLOR_2: 0x431A04,
        COLOR_3: 0x442602,
        COLOR_4: 0x4E1C02,
        COLOR_5: 0x4F3803,
        COLOR_6: 0x243417,
        COLOR_7: 0x112A22,
        COLOR_8: 0x132423,
        COLOR_9: 0x161D24,
        COLOR_10: 0x0A1F28,
    }
    host_os: str = OS_WINDOWS
    pixels_disabled: bool = False
    pixels_disabled_timeout: int = 20 * ONE_MINUTE

    def __init__(
        self,
        color_scheme: Optional[Dict[str, int]] = None,
        host_os: Optional[str] = None,
        pixels_disabled: Optional[bool] = None,
        pixels_disabled_timeout: Optional[int] = None,
        **kwargs,
    ):
        if color_scheme is not None:
            self.color_scheme = color_scheme
        if host_os is not None:
            self.host_os = host_os
        if pixels_disabled is not None:
            self.pixels_disabled = pixels_disabled
        if pixels_disabled_timeout is not None:
            self.pixels_disabled_timeout = pixels_disabled_timeout
        super().__init__(**kwargs)

    def color(self, color_name: str) -> int:
        for _ in range(5):
            color = self.color_scheme.get(color_name, 0x000000)
            if isinstance(color, int):
                return color
            color_name = color
        return 0x000000


class KeyApp(BaseApp):
    """An App with a specific command bound to each key.

    A KeyApp has a Key instance (or None) bound to each key. You may also
    bind commands to the encoder button and the encoder rotation.

    To use this class, subclass KeyApp and specify values for each key you
    want to use.

    """

    name = "Key App"

    settings: KeyAppSettings

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

    def __init__(self, app_pad: AppPad, settings: Optional[KeyAppSettings] = None):
        """Initialize the KeyApp.

        Args:
            app_pad (AppPad): An AppPad instance
            settings (KeyAppSettings): A KeyAppSettings instance
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

        if settings is None:
            settings = KeyAppSettings()

        super().__init__(app_pad, settings)

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

        Also add a timer to disable the pixels after a certain period of
        inactivity.

        """
        super().on_focus()
        self.app_pad.track_double_taps(self.double_tap_key_indices)

        if self.settings.pixels_disabled_timeout:
            self.app_pad.add_timer(
                TIMER_DISABLE_PIXELS,
                self.settings.pixels_disabled_timeout,
                self.disable_pixels,
            )

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
        self.settings.pixels_disabled = False

    def disable_pixels(self):
        """Turn off all the pixels on the keypad."""
        for i in range(len(self.keys)):
            self.app_pad.pixels[i] = 0
        self.app_pad.pixels.show()
        self.settings.pixels_disabled = True

    def process_event(
        self, event: Union[DoubleTapEvent, EncoderButtonEvent, EncoderEvent, KeyEvent]
    ):
        if self.settings.pixels_disabled:
            self.pixels_on_focus()
            self.app_pad.pixels.show()
        if self.settings.pixels_disabled_timeout:
            self.app_pad.add_timer(
                TIMER_DISABLE_PIXELS,
                self.settings.pixels_disabled_timeout,
                self.disable_pixels,
            )
        return super().process_event(event)

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
        color: Union[int, str] = 0,
        command: Optional[Command] = None,
        double_tap_command: Optional[Command] = None,
    ):
        """Initialize the Key.

        Args:
            text (str, optional): The text for the label of the Key.
                Defaults to "".
            color (int | str, optional): The color value for the Key.
                Defaults to 0. May be an int or a string. If a string, the
                color is looked up in the settings color scheme.
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
        if isinstance(self._color, str):
            return app.settings.color(self._color)
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
            self.double_tap_command.undo(app)

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


class SettingsValueKey(Key):
    """A Key whose color and text are dependent on the value of a setting.

    The text of the key is the value of the setting. The color of the key is
    the color determined by the value of the setting using color_mapping.

    """

    def __init__(
        self,
        setting: str,
        command: Optional[Command] = None,
        double_tap_command: Optional[Command] = None,
        color_mapping: Optional[Dict[str, Union[int, str]]] = None,
        text_template: str = "{value}",
    ):
        """Initialize the SettingsValueKey.

        Args:
            setting (str): The name of the setting
            command (Optional[Command], optional): A Command to execute when
                the key is pressed. Defaults to None.
            double_tap_command (Optional[Command], optional): A command to
                execute when the key is double-tapped. Defaults to None.
            color_mapping (Optional[Dict[str, int]], optional): A dictionary
                mapping values for the setting to colors. If None the key
                will have no color. Defaults to None. Colors may be ints or
                strings. If strings, the color names will be mapped to ints
                using the settings color scheme.
            text_template (str, optional): A template string to determine the
                text for the key. The keys for the template string are setting
                and value. Defaults to "{value}".

        """
        super().__init__(command=command, double_tap_command=double_tap_command)
        self.setting = setting
        self.color_mapping = color_mapping
        self.text_template = text_template

    def text(self, app) -> str:
        return self.text_template.format(
            setting=self.setting, value=app.settings.get(self.setting, "")
        )

    def color(self, app) -> int:
        if self.color_mapping is not None:
            color = self.color_mapping.get(app.settings.get(self.setting, ""), 0)
            if isinstance(color, str):
                color = app.settings.color(color)
            return color
        return 0


class SettingsSelectKey(Key):
    """A key which stores a value to a setting when pressed.

    Multiple keys can be linked to the same setting. The text and color for all
    keys will be updated whenever the key is pressed.

    """

    marker = ">"
    template = "{marker} {text}"

    class BoundKey(Key.BoundKey):
        """A SettingsSelectKey bound to a specific app and key number."""

        def __init__(self, key: "SettingsSelectKey", app: KeyApp, key_number: int):
            """Initialize the BoundKey.

            Args:
                key (SettingsSelectKey): A SettingsSelectKey instance
                app (KeyApp): A KeyApp instance to bind
                    to
                key_number (int): The key number to bind to
            """
            super().__init__(key, app, key_number)
            self.related_keys: Set[SettingsSelectKey.BoundKey] = set()

            setting = key.setting
            for bound_key in app.keys:
                if not isinstance(bound_key, SettingsSelectKey.BoundKey):
                    continue

                if bound_key.key.setting == setting:
                    self.related_keys.add(bound_key)
                    bound_key.related_keys.add(self)

        def press(self):
            """Logic to run when the key is pressed.

            Update the setting associated with the key.
            Optionally run the command tied to the key.
            Update the text and pixel for the key and any related keys.

            """
            self.key.press(self.app)
            self.pixel = self.color()
            self.label = self.text()

            for key in self.related_keys:
                key.pixel = key.color()
                key.label = key.text()

            self.app.macropad.display.refresh()
            self.app.macropad.pixels.show()

    def __init__(
        self,
        text: str = "",
        color: Union[int, str] = 0,
        setting: str = "",
        value: Any = None,
        command: Optional[Command] = None,
    ):
        """Initialize the SettingsSelectKey.

        Args:
            text (str, optional): The text to display for the key.
                Defaults to "".
            color (int | str, optional): The color to display when the value is
                the current setting. Defaults to 0. May be an int or string.
                If a string, the color is retrieved from the app settings.
            setting (str, optional): The name of the setting. Defaults to "".
            value (Any, optional): The value of the setting. Defaults to None.
            command (Optional[Command], optional): An additional command to run
                when the key is pressed. Defaults to None.

        """
        super().__init__(text, color, command)
        self.setting = setting
        self.value = value

    def text(self, app: KeyApp) -> str:
        """The text to display for the key.

        If the key's value is the current value for the setting, a marker is
        added to the key's text to indicate it is selected.

        Args:
            app (KeyApp): An instance of KeyApp

        Returns:
            str: The text to display for the key.

        """
        if app.settings.get(self.setting, None) == self.value:
            marker = self.marker
        else:
            marker = " "

        return self.template.format(marker=marker, text=self._text)

    def color(self, app: KeyApp) -> int:
        """The color of the key's pixel.

        If the key's value is the current value for the setting, the key's
        color is displayed. Otherwise no color is displayed.

        Args:
            app (KeyApp): An instance of KeyApp

        Returns:
            int: The color to display for the key's pixel

        """
        if app.settings.get(self.setting, None) == self.value:
            return super().color(app)
        return 0

    def press(self, app: KeyApp):
        """Update the setting for the key. Then run the command for the key.

        Args:
            app (KeyApp): An instance of KeyApp.

        """
        app.settings[self.setting] = self.value
        super().press(app)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.setting}: {self.value})"


class MacroKey(Key):
    class BoundKey(Key.BoundKey):
        def press(self):
            self.pixel = 0xFFFFFF
            self.app.macropad.pixels.show()
            self.key.press(self.app)

        def release(self):
            self.key.release(self.app)
            self.pixel = self.color()
            self.app.macropad.pixels.show()

    def __init__(
        self,
        text: str = "",
        color: Union[int, str] = 0,
        command: Optional[Command] = None,
        double_tap_command: Optional[Command] = None,
        linux_command=EMPTY_VALUE,
        mac_command=EMPTY_VALUE,
        windows_command=EMPTY_VALUE,
    ):
        super().__init__(text, color, command, double_tap_command)

        self.os_commands: Dict[str, Optional[Command]] = {
            os: com if (com is not EMPTY_VALUE) else self.command
            for os, com in zip(
                (OS_LINUX, OS_MAC, OS_WINDOWS),
                (linux_command, mac_command, windows_command),
            )
        }

    @staticmethod
    def _get_os(app) -> str:
        return app.settings.host_os

    def _get_command(self, app) -> Optional[Command]:
        os = self._get_os(app)
        return self.os_commands[os]

    def text(self, app) -> str:
        if self._get_command(app):
            return self._text
        return ""

    def color(self, app) -> int:
        if self._get_command(app):
            return super().color(app)
        return 0

    def press(self, app):
        command = self._get_command(app)
        if command:
            command.execute(app)

    def release(self, app):
        command = self._get_command(app)
        if command:
            command.undo(app)
