import os


class BaseApp:
    name = "Base App"

    # First row
    key_1 = None
    key_2 = None
    key_3 = None

    # Second row
    key_4 = None
    key_5 = None
    key_6 = None

    # Third row
    key_7 = None
    key_8 = None
    key_9 = None

    # Fourth row
    key_10 = None
    key_11 = None
    key_12 = None

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

        apps = list(sorted(BaseApp._instances, key=lambda app: app.name))
        for app in apps:
            print("Loaded %s" % app.name)
        return apps

    def __init__(self):
        try:
            BaseApp._instances.add(self)
        except AttributeError:
            BaseApp._instances = {self}

        self.macros = []
        for index in range(12):
            self.macros.append(self[index + 1])

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise IndexError("Index %s is not an int" % index)
        return getattr(self, "key_%s" % index)
