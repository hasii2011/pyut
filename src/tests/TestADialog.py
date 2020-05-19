
from typing import cast

from logging import Logger
from logging import getLogger
from unittest.mock import MagicMock

from wx import DEFAULT_FRAME_STYLE
from wx import ID_ANY
from wx import OK

from wx import App
from wx import Frame

from org.pyut.MiniOgl.DiagramFrame import DiagramFrame
from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.dialogs.DlgEditInterface import DlgEditInterface
from org.pyut.general.Mediator import Mediator
from org.pyut.model.PyutInterface import PyutInterface

from tests.TestBase import TestBase


class TestADialog(App):

    FRAME_ID: int = 0xDeadBeef

    def OnInit(self):

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)
        frameTop: Frame = Frame(parent=None, id=TestADialog.FRAME_ID, title="Test A Dialog", size=(600, 400), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(True)

        PyutPreferences.determinePreferencesLocation()

        diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        diagramFrame.SetSize((1200, 1200))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        diagramFrame.Show(True)

        self.SetTopWindow(diagramFrame)

        self._diagramFrame: DiagramFrame = diagramFrame

        #
        # Introduce a mock
        #
        fileHandler = MagicMock()
        self._mediator = Mediator()
        self._mediator.registerFileHandling(fileHandler)
        self.initTest()
        return True

    def initTest(self):
        pyutInterface: PyutInterface = PyutInterface()

        with DlgEditInterface(self._diagramFrame, ID_ANY, pyutInterface) as dlg:
            dlg: DlgEditInterface = cast(DlgEditInterface, dlg)
            if dlg.ShowModal() == OK:
                self.logger.warning(f'Retrieved data')
                self.logger.info(f'model: {dlg._pyutModel}')
            else:
                self.logger.warning(f'Cancelled')

        self.logger.info(f"After dialog show")


testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
