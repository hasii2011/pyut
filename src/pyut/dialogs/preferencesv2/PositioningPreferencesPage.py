
from wx import StockPreferencesPage
from wx import Window

from pyut.dialogs.preferences.PositioningPreferences import PositioningPreferences


class PositioningPreferencesPage(StockPreferencesPage):

    def __init__(self):
        super().__init__(kind=StockPreferencesPage.Kind_General
                         )

    def CreateWindow(self, parent) -> Window:

        return PositioningPreferences(parent=parent)
