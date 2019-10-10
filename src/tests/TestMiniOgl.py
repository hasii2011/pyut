from wx import App
from wx import CURSOR_PENCIL
from wx import Cursor
from wx import DEFAULT_FRAME_STYLE
from wx import Frame

from MiniOgl.DiagramFrame import DiagramFrame
from MiniOgl.Diagram import Diagram

from MiniOgl.PointShape import PointShape
from MiniOgl.RectangleShape import RectangleShape
from MiniOgl.AnchorPoint import AnchorPoint
from MiniOgl.LineShape import LineShape


class TestMiniOglApp(App):

    FRAME_ID: int = 0xDeadBeef

    def OnInit(self):

        frameTop: Frame = Frame(parent=None, id=TestMiniOglApp.FRAME_ID, title="Test MiniOgl", size=(400, 400), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(True)

        diagFrame: DiagramFrame = DiagramFrame(frameTop)
        diagFrame.SetSize((1200, 1200))
        diagFrame.SetScrollbars(10, 10, 100, 100)
        diagFrame.SetCursor(Cursor(CURSOR_PENCIL))
        diagFrame.Show(True)

        self.SetTopWindow(diagFrame)

        self._diagFrame: DiagramFrame = diagFrame

        self.initTest()

        return True

    def initTest(self):

        diagFrame: Diagram = self._diagFrame.GetDiagram()

        pointShape: PointShape = PointShape(50, 50)
        diagFrame.AddShape(pointShape)

        for x in range(10):
            for y in range(3):
                pointShape: PointShape = PointShape(300 + x*50, 300 + y*50)
                diagFrame.AddShape(pointShape)

        rectShape: RectangleShape = RectangleShape(100, 50, 130, 80)
        rectShape.SetDraggable(True)
        diagFrame.AddShape(rectShape)

        anchor1 = AnchorPoint(50, 100)
        anchor1.SetDraggable(True)
        anchor2 = AnchorPoint(70, 130)
        anchor2.SetDraggable(True)

        lineShape: LineShape = LineShape(anchor1, anchor2)
        lineShape.SetDrawArrow(False)
        lineShape.SetDraggable(True)
        diagFrame.AddShape(lineShape)


testApp: App = TestMiniOglApp(redirect=False)

testApp.MainLoop()
