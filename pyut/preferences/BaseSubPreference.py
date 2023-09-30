
from typing import cast

from configparser import ConfigParser

from codeallybasic.Singleton import Singleton


class BaseSubPreference(Singleton):

    # noinspection PyAttributeOutsideInit
    def init(self, *args, **kwargs):

        self._config: ConfigParser = cast(ConfigParser, None)

        for name, value in kwargs.items():
            protectedName: str = f'_{name}'
            if not hasattr(self, protectedName):
                raise TypeError(f"Unexpected keyword argument {protectedName}")
            setattr(self, protectedName, value)

    @property
    def configParser(self) -> ConfigParser:
        return self._config

    @configParser.setter
    def configParser(self, newValue: ConfigParser):
        # noinspection PyAttributeOutsideInit
        self._config = newValue
