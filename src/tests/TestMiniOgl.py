from wx import App
from wx import BITMAP_TYPE_PNG
from wx import Bitmap
from wx import Button
from wx import ClientDC
from wx import CommandEvent

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_BUTTON
from wx import Frame
from wx import Image
from wx import MemoryDC
from wx import NullBitmap
from wx import ScrolledWindow
from wx._core import BitmapType

from org.pyut.miniogl.DiagramFrame import DiagramFrame
from org.pyut.miniogl.Diagram import Diagram
from org.pyut.miniogl.LollipopLine import LollipopLine

from org.pyut.miniogl.PointShape import PointShape
from org.pyut.miniogl.RectangleShape import RectangleShape
from org.pyut.miniogl.AnchorPoint import AnchorPoint
from org.pyut.miniogl.LineShape import LineShape
from org.pyut.miniogl.ControlPoint import ControlPoint
from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint

from org.pyut.enums.AttachmentPoint import AttachmentPoint

from org.pyut.preferences.PyutPreferences import PyutPreferences


class TestMiniOglApp(App):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def OnInit(self):

        PyutPreferences.determinePreferencesLocation()

        frameTop: Frame = Frame(parent=None, id=TestMiniOglApp.FRAME_ID, title="Test miniogl",
                                size=(TestMiniOglApp.WINDOW_WIDTH, TestMiniOglApp.WINDOW_HEIGHT), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(True)

        diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        diagramFrame.SetSize((TestMiniOglApp.WINDOW_WIDTH, TestMiniOglApp.WINDOW_HEIGHT))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        button = Button(frameTop, 1003, "Draw Me")
        button.SetPosition((15, 15))
        self.Bind(EVT_BUTTON, self.onDrawMe, button)

        diagramFrame.Show(True)

        self.SetTopWindow(diagramFrame)

        self._diagramFrame: DiagramFrame = diagramFrame

        self.initTest()

        return True

    def initTest(self):

        diagramFrame: Diagram = self._diagramFrame.GetDiagram()

        pointShape: PointShape = PointShape(50, 50)
        diagramFrame.AddShape(pointShape)

        for x in range(10):
            for y in range(3):
                pointShape: PointShape = PointShape(300 + x*50, 300 + y*50)
                diagramFrame.AddShape(pointShape)

        rectShape: RectangleShape = RectangleShape(100, 50, 130, 80)
        rectShape.SetDraggable(True)
        diagramFrame.AddShape(rectShape)

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

        diagramFrame.AddShape(lineShape)

        self.drawLollipops()

    def drawLollipops(self):

        diagramFrame: Diagram = self._diagramFrame.GetDiagram()

        rectShape: RectangleShape = RectangleShape(400, 50, 130, 80)
        rectShape.SetDraggable(True)
        diagramFrame.AddShape(rectShape)

        dw, dh     = rectShape.GetSize()

        eastX, eastY   = dw, dh / 2

        destAnchor = SelectAnchorPoint(parent=rectShape, attachmentPoint=AttachmentPoint.EAST, x=eastX, y=eastY)
        destAnchor.SetDraggable(False)

        lollipopLine: LollipopLine = LollipopLine(destAnchor)

        diagramFrame.AddShape(lollipopLine)

    # noinspection PyUnusedLocal
    def onDrawMe(self, event: CommandEvent):

        extension: str = 'png'
        imageType: BitmapType = BITMAP_TYPE_PNG
        window: ScrolledWindow = self._diagramFrame
        context: ClientDC = ClientDC(window)
        memory: MemoryDC = MemoryDC()

        x, y = window.ClientSize
        emptyBitmap: Bitmap = Bitmap(x, y, -1)

        memory.SelectObject(emptyBitmap)
        memory.Blit(source=context, xsrc=0, height=y, xdest=0, ydest=0, ysrc=0, width=x)
        memory.SelectObject(NullBitmap)

        img: Image = emptyBitmap.ConvertToImage()
        filename: str = f'DiagramDump.{extension}'
        status: bool = img.SaveFile(filename, imageType)


testApp: App = TestMiniOglApp(redirect=False)

testApp.MainLoop()
