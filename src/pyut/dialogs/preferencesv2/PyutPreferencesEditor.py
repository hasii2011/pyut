from wx import EventLoop
from wx import EventLoopActivator
from wx import GUIEventLoop
from wx import GetApp
from wx import PreferencesEditor
from wx import Window
from wx import Yield
from wx import Sleep

from pyut.dialogs.preferencesv2.GeneralPrefencesPage import GeneralPreferencesPage
from pyut.dialogs.preferencesv2.PositioningPreferencesPage import PositioningPreferencesPage


class PyutPreferencesEditor(PreferencesEditor):
    """
    Not really a dialog;  Just some syntactic sugar
    """
    def __init__(self):

        super().__init__(title='Pyut PreferencesEditor')

    def addPanels(self):

        self.AddPage(page=PositioningPreferencesPage())
        self.AddPage(page=GeneralPreferencesPage())

    def ShowModal(self, parent: Window):
        print(f'{self.ShownModally()=}')
        self.Show(parent)
        app = GetApp()
        eventLoop = GUIEventLoop()
        ea = EventLoopActivator(eventLoop)
        while eventLoop.Pending():
            eventLoop.Dispatch()
        app.ProcessIdle()
        del ea