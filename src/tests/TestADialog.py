
from typing import cast

from logging import Logger
from logging import getLogger

from sys import exit as sysExit

from wx import DEFAULT_FRAME_STYLE
from wx import ID_ANY
from wx import OK

from wx import App
from wx import Frame

from org.pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from org.pyut.model.PyutNote import PyutNote

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.general.Mediator import Mediator


from tests.TestBase import TestBase

from unittest.mock import MagicMock


class TestADialog(App):

    FRAME_ID: int = ID_ANY

    def OnInit(self):

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)
        frameTop:    Frame = Frame(parent=None, id=TestADialog.FRAME_ID, title="Test A Dialog", size=(600, 400), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(False)

        PyutPreferences.determinePreferencesLocation()

        self.SetTopWindow(frameTop)

        self._frameTop = frameTop
        self._preferences: PyutPreferences = PyutPreferences()
        #
        # Introduce a mock
        #
        fileHandler = MagicMock()
        self._mediator = Mediator()
        self._mediator.registerFileHandling(fileHandler)
        self.initTest()
        return True

    def initTest(self):

        pyutNote: PyutNote = PyutNote()
        with DlgEditNote(parent=self._frameTop, dialogIdentifier=ID_ANY, pyutNote=pyutNote) as dlg:
            dlg: DlgEditNote = cast(DlgEditNote, dlg)
            if dlg.ShowModal() == OK:
                self.logger.warning(f'Retrieved data: {pyutNote.content=}')
                self._frameTop.Close(force=True)

            else:
                self.logger.warning(f'Cancelled')
                self._frameTop.Close(force=True)

        self.logger.info(f"After dialog show")
        sysExit()   # brutal !!


testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
