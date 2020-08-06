
from typing import cast

from logging import Logger
from logging import getLogger

from sys import exit as sysExit

from unittest.mock import MagicMock

from wx import DEFAULT_FRAME_STYLE
from wx import OK

from wx import App
from wx import Frame

from org.pyut.MiniOgl.DiagramFrame import DiagramFrame

from org.pyut.PyutPreferences import PyutPreferences

from org.pyut.general.Mediator import Mediator

from org.pyut.plugins.io.pyumlsupport.DlgImageOptions import DlgImageOptions


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

        with DlgImageOptions(self._diagramFrame) as dlg:
            dlg: DlgImageOptions = cast(DlgImageOptions, dlg)
            if dlg.ShowModal() == OK:
                # self.logger.warning(f'Retrieved data: layoutWidth: {dlg.layoutWidth} layoutHeight: {dlg.layoutHeight}')
                self._diagramFrame.Close(force=True)
                self.logger.warning(f'Options: {dlg.imageOptions}')

            else:
                self.logger.warning(f'Cancelled')
                self._diagramFrame.Close(force=True)

        self.logger.info(f"After dialog show")
        sysExit()   # brutal !!


testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
