
from wx import BORDER_SUNKEN

from wx import Panel
from wx import Window

from pyut.preferences.PyutPreferences import PyutPreferences


class PreferencesPanel(Panel):
    """
    Make this abstract
    """
    def __init__(self, parent: Window):

        super().__init__(parent=parent, style=BORDER_SUNKEN)

        self._prefs:    PyutPreferences = PyutPreferences()

    def _createControls(self):
        """
        Abstract method
        Creates the main control and stashes them as private instance variables
        """
        pass

    def _setControlValues(self):
        """
        Set the default values on the controls.
        """
        pass
