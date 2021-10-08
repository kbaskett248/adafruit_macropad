import os

import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

from event import EncoderEvent, EncoderButtonEvent, KeyEvent

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64


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
                    display_height - 1 - (3 - y) * 12,
                ),
                anchor_point=(x / 2, 1.0),
            )
        )
    group.append(Rect(0, 0, display_width, 12, fill=0xFFFFFF))
    group.append(
        label.Label(
            terminalio.FONT,
            text="",
            color=0x000000,
            anchored_position=(display_width // 2, -2),
            anchor_point=(0.5, 0.0),
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


class MacroApp(KeyApp):
    name = "Macro App"

    def encoder_event(self, event):
        self.app_pad.app_index = event.position % len(self.app_pad.apps)
        self.app_pad.current_app = self.app_pad.apps[self.app_pad.app_index]

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
