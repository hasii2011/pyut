
from abc import ABCMeta
from abc import abstractmethod

from wx import BORDER_SUNKEN

from wx import Panel
from wx import Window

from pyut.preferences.PyutPreferences import PyutPreferences

class MetaPreferencesPanel(ABCMeta, type(Panel)):        # type: ignore
    """
    I have know idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class PreferencesPanel(Panel, metaclass=MetaPreferencesPanel):
    """
    Make this abstract
    """
    def __init__(self, parent: Window):

        super().__init__(parent=parent, style=BORDER_SUNKEN)

        self._prefs:    PyutPreferences = PyutPreferences()

    @abstractmethod
    def _createControls(self):
        """
        Abstract method
        Creates the main control and stashes them as private instance variables
        """
        pass

    @abstractmethod
    def _setControlValues(self):
        """
        Set the default values on the controls.
        """
        pass
