from logging import Logger
from logging import getLogger

from wx import App

from wx import DEFAULT_FRAME_STYLE
from wx import Frame
from wx import OK

from org.pyut.MiniOgl.DiagramFrame import DiagramFrame

from org.pyut.plugins.orthogonal.DlgOrthogonalOptions import DlgOrthogonalOptions


class TestADialog(App):

    FRAME_ID: int = 0xDeadBeef

    def OnInit(self):

        self.logger: Logger = getLogger(__name__)
        frameTop: Frame = Frame(parent=None, id=TestADialog.FRAME_ID, title="Test A Dialog", size=(400, 400), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(True)

        diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        diagramFrame.SetSize((1200, 1200))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        diagramFrame.Show(True)

        self.SetTopWindow(diagramFrame)

        self._diagramFrame: DiagramFrame = diagramFrame

        self.initTest()

        return True

    def initTest(self):

        with DlgOrthogonalOptions(self._diagramFrame) as dlg:
            if dlg.ShowModal() == OK:
                options = dlg.options
                self.logger.warning(f'Retrieved Options: {options}')
            else:
                self.logger.info(f'Cancelled')

        self.logger.info(f"After dialog show")


testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
