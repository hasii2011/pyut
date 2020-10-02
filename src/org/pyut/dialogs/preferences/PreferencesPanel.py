
from wx import BORDER_SUNKEN

from wx import Panel
from wx import Window

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.general.Mediator import Mediator


class PreferencesPanel(Panel):

    def __init__(self, parent: Window,):

        super().__init__(parent=parent, style=BORDER_SUNKEN)

        self._prefs:    PyutPreferences = PyutPreferences()
        self._mediator: Mediator        = Mediator()

    def _createControls(self):
        """
        Abstract method
        Creates the main control and stashes them as private instance variables
        """
        pass

    def __setControlValues(self):
        """
        Set the default values on the controls.
        """
        pass
