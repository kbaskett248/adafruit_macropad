try:
    from typing import Any, Dict
except ImportError:
    pass

from utils.constants import EMPTY_VALUE


class BaseSettings:
    additional_settings: Dict[str, Any]

    def __init__(self, **kwargs):
        self.additional_settings = {}
        for key, value in kwargs.items():
            self[key] = value

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            return self.additional_settings[key]

    def __setitem__(self, key, value) -> None:
        try:
            setattr(self, key, value)
        except:
            self.additional_settings[key] = value

    def get(self, setting: str, default=EMPTY_VALUE) -> Any:
        try:
            return self[setting]
        except KeyError as err:
            if default is EMPTY_VALUE:
                raise err
            return default
