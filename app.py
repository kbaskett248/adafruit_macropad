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

    def __init__(self):
        self.macros = []
        for index in range(12):
            self.macros.append(self[index + 1])

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise IndexError
        return getattr(self, "key_%s" % index)
