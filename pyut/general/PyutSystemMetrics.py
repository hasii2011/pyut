
from logging import Logger
from logging import getLogger

from wx import DisplaySize
from wx import ScreenDC
from wx import Size

from codeallybasic.SingletonV3 import SingletonV3

from pyut.preferences.PyutPreferences import PyutPreferences


class PyutSystemMetrics(metaclass=SingletonV3):
    """
    Wrapper class for some simple stuff I want
    """

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    @property
    def displaySize(self) -> Size:
        return DisplaySize()

    @property
    def screenResolution(self) -> Size:
        return ScreenDC().GetPPI()

    @property
    def toolBarIconSize(self) -> str:
        return PyutPreferences().toolBarIconSize.value
