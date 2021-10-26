from apps.key import KeyApp, Key
from commands import Command
from constants import PREVIOUS_APP_SETTING


class KeyAppWithSettings(KeyApp):
    name = "Base Settings"

    def __init__(self, app_pad, settings=None):
        if settings is None:
            self.settings = {}
        else:
            self.settings = settings

        super().__init__(app_pad)

    def get_setting(self, setting):
        return self.settings.get(setting, None)

    def put_setting(self, setting, value):
        self.settings[setting] = value


class SettingsValueKey(Key):
    setting = ""
    value = None
    marker = ">"
    template = "{marker} {text}"

    class BoundKey(Key.BoundKey):
        def __init__(self, key, app, key_number):
            super().__init__(key, app, key_number)
            self.related_keys = set()

            setting = key.setting
            for bound_key in app.keys:
                if not isinstance(bound_key, SettingsValueKey.BoundKey):
                    continue

                if bound_key.key.setting == setting:
                    self.related_keys.add(bound_key)
                    bound_key.related_keys.add(self)

        def press(self):
            self.key.press(self.app)
            self.pixel = self.color()
            self.label = self.text()

            for key in self.related_keys:
                key.pixel = key.color()
                key.label = key.text()

            self.app.macropad.display.refresh()
            self.app.macropad.pixels.show()

    def __init__(self, text="", color=0, setting="", value=None):
        super().__init__(text, color, None)
        self.setting = setting
        self.value = value

    def text(self, app):
        if app.get_setting(self.setting) == self.value:
            marker = self.marker
        else:
            marker = " "

        return self.template.format(marker=marker, text=self._text)

    def color(self, app):
        if app.get_setting(self.setting) == self.value:
            return self._color
        else:
            return 0

    def press(self, app):
        app.put_setting(self.setting, self.value)

    def release(self, app):
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.setting}: {self.value})"


class SwitchAppCommand(Command):
    def __init__(self, app: KeyAppWithSettings) -> None:
        super().__init__()
        self.app = app

    def execute(self, app: KeyAppWithSettings):
        app_stack = self.app.get_setting(PREVIOUS_APP_SETTING)
        app_stack.append(app)
        app.app_pad.current_app = self.app


class PreviousAppCommand(Command):
    def execute(self, app: KeyAppWithSettings):
        app_stack = app.get_setting(PREVIOUS_APP_SETTING)
        previous_app = app_stack.pop()
        if previous_app is not None:
            app.app_pad.current_app = previous_app
