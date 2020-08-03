
from sys import argv

import wx
from wx import App
from wx import BITMAP_TYPE_PNG
from wx import Bitmap

from wx import Button
from wx import ClientDC

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import Frame
from wx import Image
from wx import MemoryDC
from wx import MenuBar
from wx import Menu
from wx import NullBitmap

from wx import Rect
from wx import CommandEvent
from wx import ScrolledWindow
from wx._core import BitmapType

from wx.lib.ogl import Diagram
from wx.lib.ogl import OGLInitialize
from wx.lib.ogl import RectangleShape
from wx.lib.ogl import ShapeCanvas

from wx.lib.mixins.inspection import InspectionMixin
from wx.lib.inspection import InspectionTool


class RoundedRectangleShape(RectangleShape):

    def __init__(self, w=0.0, h=0.0):
        super().__init__(w, h)
        self.SetCornerRadius(-0.3)


class TestWindow(ShapeCanvas):

    def __init__(self, frame: Frame):

        super().__init__(frame)

        self.frame: Frame = frame

        maxWidth:  int = TestWxOgl.WINDOW_WIDTH
        maxHeight: int = TestWxOgl.FRAME_ID

        self.diagram: Diagram = Diagram()

        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)

        self.shapes   = []
        self.save_gdi = []

        self.SetScrollbars(20, 20, maxWidth//20, maxHeight//20)
        self.SetBackgroundColour("LIGHT BLUE")

        self.__addShapes()

    def __addShapes(self):

        self.__myAddShape(RoundedRectangleShape(95, 70), 345, 145,  "Rounded Rect")

    def __myAddShape(self, shape, x, y, text):

        shape.SetCanvas(self)
        shape.SetX(x)
        shape.SetY(y)
        if text:
            for line in text.split('\n'):
                shape.AddText(line)
        self.diagram.AddShape(shape)
        shape.Show(True)

        self.shapes.append(shape)
        return shape


class TestWxOgl(App, InspectionMixin):

    FRAME_ID:      int = wx.ID_ANY
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def __init__(self):
        App.__init__(self, redirect=False)

    def OnInit(self):

        self.InitInspection()

        frameTop: Frame = Frame(parent=None, id=TestWxOgl.FRAME_ID, title="Test WX Ogl",
                                size=(TestWxOgl.WINDOW_WIDTH, TestWxOgl.WINDOW_HEIGHT), style=DEFAULT_FRAME_STYLE)

        OGLInitialize()

        testWindow: TestWindow = TestWindow(frameTop)

        button = Button(testWindow, 1003, "Draw Me")
        button.SetPosition((15, 15))
        self.Bind(EVT_BUTTON, self.onDrawMe, button)

        frameTop.SetSize((800, 600))
        testWindow.SetFocus()

        self.window: TestWindow = testWindow
        self.frameRect: Rect = frameTop.GetRect()

        frameTop.Bind(EVT_CLOSE, self._onCloseFrame)

        menuBar: MenuBar = MenuBar()
        menu:    Menu    = Menu()

        item = menu.Append(-1, "&Widget Inspector\tF6", "Show the wxPython Widget Inspection Tool")
        self.Bind(wx.EVT_MENU, self.onWidgetInspector, item)

        menuBar.Append(menu, "&File")

        frameTop.SetMenuBar(menuBar)
        frameTop.Show(True)

        return True

    # noinspection PyUnusedLocal
    def onDrawMe(self, event: CommandEvent):

        extension: str = 'png'
        imageType: BitmapType = BITMAP_TYPE_PNG
        window: ScrolledWindow = self.window
        context: ClientDC = ClientDC(window)
        memory: MemoryDC = MemoryDC()

        x, y = window.ClientSize()
        emptyBitmap: Bitmap = Bitmap(x, y, -1)

        memory.SelectObject(emptyBitmap)
        memory.Blit(source=context, xsrc=0, height=y, xdest=0, ydest=0, ysrc=0, width=x)
        memory.SelectObject(NullBitmap)

        img: Image = emptyBitmap.ConvertToImage()
        filename: str = f'DiagramDump.{extension}'
        status: bool = img.SaveFile(filename, imageType)

    # noinspection PyUnusedLocal
    def onWidgetInspector(self, event: CommandEvent):
        InspectionTool().Show()

    def _onCloseFrame(self, evt: CommandEvent):
        evt.Skip()


# noinspection PyUnusedLocal
def main(sysArgv):
    testApp: App = TestWxOgl()
    testApp.MainLoop()


if __name__ == "__main__":
    main(argv)
