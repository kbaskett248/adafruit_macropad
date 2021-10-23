from apps.key import KeyApp
from apps.settings import SettingsApp
from key import SettingsValueKey


class MacroSettingsApp(SettingsApp):
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

    def key_press(self, key, key_number):
        """Execute the macro bound to the key.

        Args:
            key (Key): The Key object bound to this key
            key_number (int): Number for the key
        """

        self.macropad.pixels[key_number] = 0xFFFFFF
        self.macropad.pixels.show()
        key.press(self)

    def key_release(self, key, key_number):
        """Release the macro bound to the key.

        Release any still-pressed keys, consumer codes, mouse buttons
        Keys and mouse buttons are individually released this way (rather
        than release_all()) because pad supports multi-key rollover, e.g.
        could have a meta key or right-mouse held down by one macro and
        press/release keys/buttons with others. Navigate popups, etc.

        Args:
            key (Key): The Key object bound to this key
            key_number (int): Number for the key
        """
        key.release(self)
        self.macropad.pixels[key_number] = key.color(self)
        self.macropad.pixels.show()
