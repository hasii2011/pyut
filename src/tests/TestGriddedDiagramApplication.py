from wx import BOTTOM
from wx import DEFAULT_FRAME_STYLE
from wx import EXPAND
from wx import ID_ANY
from wx import VERTICAL

from wx import App
from wx import Frame
from wx import BoxSizer

from org.pyut.MiniOgl.DiagramFrame import DiagramFrame
from org.pyut.preferences.PyutPreferences import PyutPreferences
from tests.TestBase import TestBase

WINDOW_WIDTH:  int = 900
WINDOW_HEIGHT: int = 500


class TestGriddedDiagramApplication(App):

    def OnInit(self):

        PyutPreferences.determinePreferencesLocation()

        TestBase.setUpLogging()

        frameTop: Frame = Frame(parent=None, id=ID_ANY, title="Test Gridded Diagram", size=(WINDOW_WIDTH, WINDOW_HEIGHT), style=DEFAULT_FRAME_STYLE)

        diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        diagramFrame.SetSize((WINDOW_WIDTH, WINDOW_HEIGHT))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        frameTop.SetAutoLayout(True)

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        mainSizer.Add(diagramFrame, 1, EXPAND | BOTTOM, 10)
        frameTop.SetSizer(mainSizer)
        mainSizer.Fit(frameTop)

        frameTop.Show(True)

        return True


testApp: App = TestGriddedDiagramApplication(redirect=False)

testApp.MainLoop()
