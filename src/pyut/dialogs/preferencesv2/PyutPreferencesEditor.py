
from wx import PreferencesEditor

from pyut.dialogs.preferencesv2.DefaultValuesPreferencesPage import DefaultValuesPreferencesPage
from pyut.dialogs.preferencesv2.DiagramPreferencesPage import DiagramPreferencesPage
from pyut.dialogs.preferencesv2.GeneralPrefencesPage import GeneralPreferencesPage
from pyut.dialogs.preferencesv2.MiscellaneousPreferencePage import MiscellaneousPreferencesPage
from pyut.dialogs.preferencesv2.PositioningPreferencesPage import PositioningPreferencesPage


class PyutPreferencesEditor(PreferencesEditor):
    """
    Not really a dialog;  Just some syntactic sugar
    Preferences editor provides a better specific platform look and feel
    """
    def __init__(self):

        super().__init__(title='Pyut PreferencesEditor')

    def addPanels(self):

        self.AddPage(page=GeneralPreferencesPage())
        self.AddPage(page=PositioningPreferencesPage())
        self.AddPage(page=MiscellaneousPreferencesPage())
        self.AddPage(page=DiagramPreferencesPage())
        self.AddPage(page=DefaultValuesPreferencesPage())
