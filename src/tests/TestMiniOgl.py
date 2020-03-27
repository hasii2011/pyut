from wx import App

from wx import DEFAULT_FRAME_STYLE
from wx import Frame

from org.pyut.MiniOgl.DiagramFrame import DiagramFrame
from org.pyut.MiniOgl.Diagram import Diagram

from org.pyut.MiniOgl.PointShape import PointShape
from org.pyut.MiniOgl.RectangleShape import RectangleShape
from org.pyut.MiniOgl.AnchorPoint import AnchorPoint
from org.pyut.MiniOgl.LineShape import LineShape
from org.pyut.MiniOgl.ControlPoint import ControlPoint


class TestMiniOglApp(App):

    FRAME_ID: int = 0xDeadBeef

    def OnInit(self):

        frameTop: Frame = Frame(parent=None, id=TestMiniOglApp.FRAME_ID, title="Test MiniOgl", size=(400, 400), style=DEFAULT_FRAME_STYLE)
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

        diagFrame: Diagram = self._diagramFrame.GetDiagram()

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
        anchor2 = AnchorPoint(200, 300)
        anchor2.SetDraggable(True)

        lineShape: LineShape = LineShape(anchor1, anchor2)
        lineShape.SetDrawArrow(False)
        lineShape.SetDraggable(True)
        lineShape.SetSpline(False)

        controlPoint: ControlPoint = ControlPoint(50, 150)
        lineShape.AddControl(controlPoint)
        controlPoint = ControlPoint(200, 150)
        lineShape.AddControl(controlPoint)

        diagFrame.AddShape(lineShape)


testApp: App = TestMiniOglApp(redirect=False)

testApp.MainLoop()
