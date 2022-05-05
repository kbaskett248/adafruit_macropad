# MACROPAD Hotkeys example: Function keys

from utils.apps.key import Key, KeyApp
from utils.commands import ConsumerControlCode, Keycode, Media, Press, PreviousAppCommand, Sequence, Release, Text, SwitchAppCommand
from utils.constants import COLOR_FUNC
from utils.config import conf

def get_shortcut(name):
    return Sequence(
        Press(Keycode.WINDOWS),
        Text(conf.pinned_apps[name]),
        Release(Keycode.WINDOWS),
    )

class GPForms(KeyApp):
    name = "GPForms"

    key_0 = Key("Register", COLOR_FUNC, Sequence(
            Press(Keycode.INSERT),
            Release(Keycode.INSERT),
            PreviousAppCommand(),
        )
    )
    key_5 = Key("Tel", COLOR_FUNC, Sequence(Text("5555555555")), Text("8005558355"))
    key_2 = Key("@", COLOR_FUNC, Sequence(Text("some_email@somedomain.com")), Text("some_other_email@somedomain.com"))
    key_8 = Key("ADDR", COLOR_FUNC, Sequence(
            Text("777 Eastern Parkway"),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Text("Brooklyn"),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Text("New York"),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Text("11213"),
        ), 
        Sequence(
            Text("770 Eastern Parkway"),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Text("Brooklyn"),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Text("New York"),
            Press(Keycode.TAB), Release(Keycode.TAB),
            Text("11213"),
        )
    )
    key_11 = Key("<<<", COLOR_FUNC, PreviousAppCommand())

    encoder_button = PreviousAppCommand()

class Work(KeyApp):
    def __init__(self, app_pad, settings = None):
        self.name = "Default"

        # First row
        self.key_0 = Key("PHP", COLOR_FUNC, get_shortcut("phpstorm"))
        self.key_1 = Key(">_", COLOR_FUNC, get_shortcut("terminal"))
        self.key_2 = Key("@", COLOR_FUNC, Sequence(Text("some_email@somedomain.com")), Text("some_other_email@somedomain.com"))
        self.key_6 = Key("Code", COLOR_FUNC, get_shortcut("vscode"))
        self.key_3 = Key("Idea", COLOR_FUNC, get_shortcut("intellij"))
        self.key_4 = Key("Chrome", COLOR_FUNC, get_shortcut("chrome"))
        self.key_10 = Key("Slack", COLOR_FUNC, get_shortcut("slack"))
        self.key_9 = Key("Postman", COLOR_FUNC, get_shortcut("postman"))

        self.encoder_button = Media(ConsumerControlCode.MUTE)
 
        self.encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
        self.encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)

        self.key_11 = Key("GRP", COLOR_FUNC, SwitchAppCommand(GPForms(app_pad, settings))) 
        super().__init__(app_pad, settings)


class VSCode(KeyApp):
     def __init__(self, app_pad, settings = None):
        self.name = "VSCode"

        # First row
        self.key_0 = Key("PHP", COLOR_FUNC, get_shortcut("phpstorm"))
        self.key_1 = Key(">_", COLOR_FUNC, get_shortcut("terminal"))
        self.key_6 = Key("Code", COLOR_FUNC, get_shortcut("vscode"))
        self.key_3 = Key("Idea", COLOR_FUNC, get_shortcut("intellij"))
        self.key_4 = Key("Chrome", COLOR_FUNC, get_shortcut("chrome"))
        self.key_10 = Key("Slack", COLOR_FUNC, get_shortcut("slack"))
        self.key_9 = Key("Postman", COLOR_FUNC, get_shortcut("postman"))

        self.encoder_button = Media(ConsumerControlCode.MUTE)
 
        self.encoder_increase = Media(ConsumerControlCode.VOLUME_INCREMENT)
        self.encoder_decrease = Media(ConsumerControlCode.VOLUME_DECREMENT)

        self.key_11 = None
        super().__init__(app_pad, settings)
