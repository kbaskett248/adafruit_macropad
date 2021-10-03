import os

import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label


class BaseApp:
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

    def __init__(self, macropad):
        self.macropad = macropad

        self.display_group = self._init_display_group(
            self.macropad.display.width, self.macropad.display.height
        )

    def _init_display_group(self, display_width, display_height):
        """Set up displayio group with all the labels."""
        group = displayio.Group()
        group.append(Rect(0, 0, display_width, 12, fill=0xFFFFFF))
        group.append(
            label.Label(
                terminalio.FONT,
                text=self.name,
                color=0x000000,
                anchored_position=(display_width // 2, -2),
                anchor_point=(0.5, 0.0),
            )
        )

        return group

    def on_focus(self):
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()

    def key_press(self, key_number):
        pass

    def key_release(self, key_number):
        pass


class MacroApp(BaseApp):
    name = "Base App"

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

    def __init__(self, macropad):
        self.macros = []
        for index in range(12):
            self.macros.append(self[index])

        super().__init__(macropad)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise IndexError("Index %s is not an int" % index)
        return getattr(self, "key_%s" % index)

    def __iter__(self):
        return iter(self.macros)

    def __len__(self):
        return len(self.macros)

    def _init_display_group(self, display_width, display_height):
        """Set up displayio group with all the labels."""
        group = displayio.Group()
        for key_index in range(12):
            x = key_index % 3
            y = key_index // 3
            try:
                text = self[key_index].text
            except:
                text = ""
            group.append(
                label.Label(
                    terminalio.FONT,
                    text=text,
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
                text=self.name,
                color=0x000000,
                anchored_position=(display_width // 2, -2),
                anchor_point=(0.5, 0.0),
            )
        )

        return group

    def on_focus(self):
        super().on_focus()

        for i, labeled_key in enumerate(self.macros):
            try:
                self.macropad.pixels[i] = labeled_key.color
            except AttributeError:
                self.macropad.pixels[i] = 0

        self.macropad.pixels.show()
        self.macropad.display.show(self.display_group)
        self.macropad.display.refresh()

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

        self.macropad.pixels[key_number] = 0xFFFFFF
        self.macropad.pixels.show()
        key.press(self.macropad)

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

        key.release(self.macropad)
        self.macropad.pixels[key_number] = key.color
        self.macropad.pixels.show()
