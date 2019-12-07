
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import CAPTION
from wx import EVT_CLOSE
from wx import EVT_LEFT_DOWN
from wx import EVT_LEFT_UP
from wx import EVT_PAINT
from wx import FRAME_FLOAT_ON_PARENT
from wx import GREY_PEN
from wx import STATIC_BORDER
from wx import SYSTEM_MENU
from wx import WHITE_PEN

from wx import ClientDC
from wx import DefaultPosition
from wx import Frame
from wx import Size

from org.pyut.ui.tools.ToolData import ToolData

MARGIN      = 3                 # Margin between dialog border and buttons
MARGIN_TOP  = 20
BUTTON_PICTURE_SIZE = 16        # The size of a picture in one button
BUTTON_SIZE         = BUTTON_PICTURE_SIZE + 3   # The size of one button


class EventClone:
    """
    mini-clone of wxEvent to call callback
    wxWindows tell to not create wxEvent object in our applications !
    """
    def __init__(self, theId):
        self._id = theId

    def GetId(self):
        return self._id


class Toolbox(Frame):

    ToolDataList = NewType('ToolDataList', List[ToolData])

    """
    Toolbox : a toolbox for PyUt tools plugins

    """
    def __init__(self, parentWindow, toolboxOwner):
        """
        Constructor.

        @param
        @param  parentWindow  wxWindow parentWindow
        @param  toolboxOwner ToolboxOwner
        """
        self.logger: Logger = getLogger(__name__)

        windowStyle = STATIC_BORDER | SYSTEM_MENU | CAPTION | FRAME_FLOAT_ON_PARENT
        super().__init__(parentWindow, -1, "toolbox", DefaultPosition, Size(100, 200), style=windowStyle)

        self._tools         = []
        self._category      = ""
        self._clickedButton = None
        self._parentWindow  = parentWindow
        self._toolboxOwner  = toolboxOwner

        # Events
        self.Bind(EVT_PAINT, self.OnRefresh)
        self.Bind(EVT_CLOSE, self.evtClose)
        self.Bind(EVT_LEFT_UP, self.evtLeftUp)
        self.Bind(EVT_LEFT_DOWN, self.evtLeftDown)

        # Display myself
        self.Show(True)

    def setCategory(self, category):
        """
        Define the toolbox category

        @param string category : the new category
        """
        self._category = category
        self._tools = self._toolboxOwner.getCategoryTools(category)
        self.Refresh()

    # noinspection PyUnusedLocal
    def OnRefresh(self, event):
        """
        Refresh dialog box

        """
        (w, h) = self.GetSize()

        nbButtonsW = (w - MARGIN*2) / BUTTON_SIZE
        dc = ClientDC(self)
        oldPen = dc.GetPen()

        # Draw
        i = 0
        j = 0
        for tool in self._tools:
            # Calculate position
            x = MARGIN + i*BUTTON_SIZE
            y = MARGIN + j*BUTTON_SIZE + MARGIN_TOP

            # Draw
            dc.SetPen(BLACK_PEN)
            dc.DrawText("[" + tool._initialCategory + "]", MARGIN, MARGIN)
            dc.SetPen(WHITE_PEN)
            dc.DrawLine(x, y, x+BUTTON_SIZE-1, y)
            dc.DrawLine(x, y, x, y + BUTTON_SIZE-1)
            dc.SetPen(BLACK_PEN)
            dc.DrawLine(x, y+BUTTON_SIZE-1, x+BUTTON_SIZE-1, y+BUTTON_SIZE-1)
            dc.DrawLine(x + BUTTON_SIZE-1, y, x + BUTTON_SIZE-1, y + BUTTON_SIZE-1)
            dc.DrawBitmap(tool.getImg(), x+1, y+1)
            i += 1

            # Find next position
            if i > nbButtonsW-1:
                i = 0
                j += 1

        # Set old pen
        dc.SetPen(oldPen)

    def _getClickedButton(self, x, y):
        """
        Return the clicked button
        """
        # (w, h) = self.GetSizeTuple()
        (w, h) = self.GetSize()

        nbButtonsW = (w - MARGIN*2) / BUTTON_SIZE

        # Get position
        i = 0
        j = 0
        for tool in self._tools:
            # Calculate position
            bx = MARGIN + i*BUTTON_SIZE
            by = MARGIN + j*BUTTON_SIZE + MARGIN_TOP

            # Are we into the current tool ?
            #  if x > bx and x < bx + BUTTON_SIZE and y > by and y < by + BUTTON_SIZE:
            if bx < x < bx + BUTTON_SIZE and by < y < by + BUTTON_SIZE:
                return bx, by, bx+BUTTON_SIZE, by+BUTTON_SIZE, tool

            # Find next position
            i += 1
            if i > nbButtonsW-1:
                i = 0
                j += 1
        return 0, 0, 0, 0, None

    # noinspection PyUnusedLocal
    def evtLeftUp(self, event):
        """
        Handle left mouse button up
        """
        # Get clicked coordinates
        clickedCoordinates = self._clickedButton
        self.logger.debug(f'clickedCoordinates: {clickedCoordinates}')
        (x1, y1, x2, y2, tool) = self._clickedButton

        # Get dc
        dc = ClientDC(self)
        oldPen = dc.GetPen()

        # Draw normally button
        dc.SetPen(BLACK_PEN)
        dc.DrawLine(x2-1, y2-1, x2-1, y1)
        dc.DrawLine(x2-1, y2-1, x1, y2-1)
        dc.SetPen(WHITE_PEN)
        dc.DrawLine(x1, y1, x2-1, y1)
        dc.DrawLine(x1, y1, x1, y2-1)

        # Set old pen
        dc.SetPen(oldPen)

        # Remove clicked button
        self._clickedButton = None

        # Execute callback
        if tool is not None:
            callback = tool.getActionCallback()
            if callback is not None:
                callback(EventClone(tool.getWxId()))

    def evtLeftDown(self, event):
        """
        Handle left mouse button down
        """
        # Get the clicked tool
        x, y = event.GetPosition()
        (x1, y1, x2, y2, tool) = self._getClickedButton(x, y)
        self._clickedButton = (x1, y1, x2, y2, tool)

        # Get dc
        dc = ClientDC(self)
        oldPen = dc.GetPen()

        # Clicked illusion
        dc.SetPen(GREY_PEN)
        dc.DrawLine(x2-1, y2-1, x2-1, y1)
        dc.DrawLine(x2-1, y2-1, x1, y2-1)
        dc.SetPen(BLACK_PEN)
        dc.DrawLine(x1, y1, x2-1, y1)
        dc.DrawLine(x1, y1, x1, y2-1)

        # Set old pen
        dc.SetPen(oldPen)

    # noinspection PyUnusedLocal
    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE
        """
        self.Destroy()
