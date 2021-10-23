from apps.key import KeyApp


class SettingsApp(KeyApp):
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

    def key_press(self, key, key_number):
        """Update the setting associated with the key.

        Args:
            key (Key): The Key object bound to the key
            key_number (int): Number for the key
        """
        key.press(self)

        for i, labeled_key in enumerate(self.keys):
            try:
                self.display_group[i].text = labeled_key.text(self)
                self.macropad.pixels[i] = labeled_key.color(self)
            except AttributeError:
                continue

        self.macropad.display.refresh()
        self.macropad.pixels.show()