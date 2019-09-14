from DiagramFrame import DiagramFrame
from PointShape import PointShape
from RectangleShape import RectangleShape
from AnchorPoint import AnchorPoint
from LineShape import LineShape
import wx


class MyApp(wx.App):
    def OnInit(self):
        frameTop = wx.Frame(None, -1, "", size=(400, 400))
        frameTop.Show(True)
        frame = DiagramFrame(frameTop)
        frame.SetSize((1200, 1200))
        frame.SetScrollbars(10, 10, 100, 100)
        frame.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
        frame.Show(True)
        self.SetTopWindow(frame)
        self._frame = frame
    
        self.initTest()

        return True


    def initTest(self):
        diag = self._frame.GetDiagram()

        shape = PointShape(50, 50)
        diag.AddShape(shape)

        for x in range(10):
            for y in range(3):
                shape = PointShape(300 + x*50, 300 + y*50)
                diag.AddShape(shape)


        shape = RectangleShape(100, 50, 130, 80)
        shape.SetDraggable(True)
        diag.AddShape(shape)

        anc1 = AnchorPoint(50, 100)
        anc1.SetDraggable(True)
        anc2 = AnchorPoint(70, 130)
        anc2.SetDraggable(True)
        shape = LineShape(anc1, anc2)
        shape.SetDrawArrow(False)
        shape.SetDraggable(True)
        diag.AddShape(shape)

        

app = MyApp(0)
app.MainLoop()
