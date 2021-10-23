import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

from apps.base import BaseApp
from constants import DISPLAY_HEIGHT, DISPLAY_WIDTH
from key import SettingsValueKey


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


class BaseSettingsApp(KeyApp):
    name = "Base Settings"

    def __init__(self, app_pad, initial_settings=None):
        if initial_settings is None:
            self.settings = {}
        else:
            self.settings = initial_settings

        super().__init__(app_pad)

    def get_setting(self, setting):
        return self.settings.get(setting, None)

    def put_setting(self, setting, value):
        self.settings[setting] = value

    def key_press(self, key_number):
        """Update the setting associated with the key.

        If there is no setting bound to this key, return early and do nothing.
        Otherwise, update the display and pixels.

        Args:
            key_number (int): The index of the key that was pressed
        """
        try:
            key = self[key_number]
        except IndexError:
            return

        if key is None:
            return

        key.press(self)
        for i, labeled_key in enumerate(self.keys):
            try:
                self.display_group[i].text = labeled_key.text(self)
                self.macropad.pixels[i] = labeled_key.color(self)
            except AttributeError:
                continue

        self.macropad.display.refresh()
        self.macropad.pixels.show()


class MacroSettingsApp(BaseSettingsApp):
    PREVIOUS_APP = "previous app"
    OS = "OS"
    OS_MAC = "MAC"
    OS_WINDOWS = "WIN"
    OS_LINUX = "LIN"

    name = "Macropad Settings"

    key_0 = SettingsValueKey("MAC", 0x555555, OS, OS_MAC)
    key_1 = SettingsValueKey("WIN", 0x00A4EF, OS, OS_WINDOWS)
    key_2 = SettingsValueKey("LIN", 0x25D366, OS, OS_LINUX)

    def encoder_button_event(self, event):
        if event.pressed:
            previous_app = self.get_setting(self.PREVIOUS_APP)
            self.put_setting(self.PREVIOUS_APP, None)
            self.app_pad.current_app = previous_app


class MacroApp(KeyApp):
    name = "Macro App"
    SETTINGS_APP = MacroSettingsApp

    @property
    def settings_app(self):
        try:
            return self._settings_app
        except AttributeError:
            MacroApp._settings_app = self.SETTINGS_APP(
                self.app_pad,
                {
                    MacroSettingsApp.OS: MacroSettingsApp.OS_MAC,
                    MacroSettingsApp.PREVIOUS_APP: None,
                },
            )
            return self._settings_app

    def encoder_event(self, event):
        self.app_pad.app_index = event.position % len(self.app_pad.apps)
        self.app_pad.current_app = self.app_pad.apps[self.app_pad.app_index]

    def encoder_button_event(self, event):
        if event.pressed:
            self.settings_app.put_setting(MacroSettingsApp.PREVIOUS_APP, self)
            self.app_pad.current_app = self.settings_app

    def key_press(self, key_number):
        """Execute the macro bound to the key.

        If there is no macro bound to this key, return early and do nothing.

        Args:
            key_number (int): The index of the key that was pressed
        """
        try:
            key = self[key_number]
        except IndexError:
            return

        if key is None:
            return

        self.macropad.pixels[key_number] = 0xFFFFFF
        self.macropad.pixels.show()
        key.press(self)

    def key_release(self, key_number):
        """Release the macro bound to the key.

        Release any still-pressed keys, consumer codes, mouse buttons
        Keys and mouse buttons are individually released this way (rather
        than release_all()) because pad supports multi-key rollover, e.g.
        could have a meta key or right-mouse held down by one macro and
        press/release keys/buttons with others. Navigate popups, etc.

        Args:
            key_number (int): The index of the key that was pressed
        """
        try:
            key = self[key_number]
        except IndexError:
            return

        if key is None:
            return

        key.release(self)
        self.macropad.pixels[key_number] = key.color(self)
        self.macropad.pixels.show()
