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

        try:
            apps = list(sorted(BaseApp._instances, key=lambda app: app.name))
        except AttributeError:
            apps = []

        for app in apps:
            print("Loaded %s" % app.name)

        return apps

    def __init__(self, display_width=128, display_height=64):
        try:
            BaseApp._instances.add(self)
        except AttributeError:
            BaseApp._instances = {self}

        self.display_group = self._init_display_group(display_width, display_height)

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

    def __init__(self, display_width=128, display_height=64):
        self.macros = []
        for index in range(12):
            self.macros.append(self[index])

        super().__init__(display_width, display_height)

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
