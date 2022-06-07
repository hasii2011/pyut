
from typing import cast

from logging import Logger
from logging import getLogger

from math import ceil

from wx import CAPTION
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EXPAND
from wx import FRAME_FLOAT_ON_PARENT
from wx import ID_ANY
from wx import STATIC_BORDER
from wx import SYSTEM_MENU

from wx import BitmapButton
from wx import MiniFrame
from wx import GridSizer
from wx import Size
from wx import Window
from wx import DefaultPosition
from wx import WindowIDRef
from wx import NewIdRef as wxNewIdRef

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.ui.tools.Tool import Category
from org.pyut.ui.tools.Tool import Tool

from org.pyut.ui.tools.ToolboxTypes import Tools


class Toolbox(MiniFrame):
    """
    This is version 2 of a toolbox.  Rather than manually drawing all the bitmaps, I
    re-implemented it as a mini frame and used a grid sizer to create it.  Then, a
    bit of computational magic to get the window size and the number of columns.
    """

    TOOLBOX_NUM_COLUMNS: int = 4
    TOOLBOX_V_GAP:       int = 2
    TOOLBOX_H_GAP:       int = 2

    TOOLBOX_SIZE_ADJUSTMENT: int = 8    # For toolbox aesthetics

    def __init__(self, parentWindow: Window, toolboxOwner):
        """

        Args:
            parentWindow:   wxWindow parentWindow
            toolboxOwner:   ToolboxOwner
        """

        from org.pyut.ui.tools.ToolboxOwner import ToolboxOwner

        self.logger: Logger = getLogger(__name__)

        windowStyle = STATIC_BORDER | SYSTEM_MENU | CAPTION | FRAME_FLOAT_ON_PARENT
        super().__init__(parentWindow, ID_ANY, "Tool Box", DefaultPosition, Size(100, 200), style=windowStyle)

        self._tools:    Tools = Tools([])
        self._category: Category  = Category("")

        self._parentWindow: Window          = parentWindow
        self._toolboxOwner: ToolboxOwner    = toolboxOwner
        self._preferences:  PyutPreferences = PyutPreferences()

        self.Bind(EVT_CLOSE, self.eventClose)

    def setCategory(self, category):
        """
        Define the toolbox category for this toolbox.  However, this toolbox has to ask
        the toolbox owner to get the tools of type 'category'

        Args:
            category:  The category of tools that we want to display
        """
        self._category = category
        self._tools = self._toolboxOwner.getCategoryTools(category)

        rowCount: int = Toolbox.computeToolboxNumberRows(toolCount=len(self._tools), numColumns=Toolbox.TOOLBOX_NUM_COLUMNS)
        gridSizer: GridSizer = GridSizer(rowCount, Toolbox.TOOLBOX_NUM_COLUMNS, Toolbox.TOOLBOX_V_GAP, Toolbox.TOOLBOX_H_GAP)      # rows, cols, vGap, hGap

        self.SetSizer(gridSizer)

        for tool in self._tools:

            tool: Tool = cast(Tool, tool)
            self.logger.debug(f'{tool.caption=}')
            if isinstance(tool.wxID, WindowIDRef) is True:
                buttonID = tool.wxID
            else:
                buttonID = wxNewIdRef()

            bitMapButton: BitmapButton = BitmapButton(parent=self, id=buttonID, bitmap=tool.img)
            self.logger.warning(f'{buttonID=} - {tool.actionCallback=}')
            bitMapButton.Bind(EVT_BUTTON, tool.actionCallback, buttonID)

            gridSizer.Add(bitMapButton, 0, EXPAND)

        iconSize:    int  = int(self._preferences.toolBarIconSize.value) + Toolbox.TOOLBOX_SIZE_ADJUSTMENT
        toolBoxSize: Size = Toolbox.computeSizeBasedOnRowColumns(numColumns=Toolbox.TOOLBOX_NUM_COLUMNS, numRows=rowCount, iconSize=iconSize)

        self.SetSize(toolBoxSize)

    # noinspection PyUnusedLocal
    def eventClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE
        """
        self.Destroy()

    @classmethod
    def computeToolboxNumberRows(cls, toolCount: int, numColumns: int) -> int:

        rowCount: int = ceil(toolCount / numColumns)

        return rowCount

    @classmethod
    def computeSizeBasedOnRowColumns(cls, numColumns: int, numRows: int, iconSize: int):

        width:  int = round(iconSize * numColumns) + (numColumns * Toolbox.TOOLBOX_H_GAP)
        height: int = round(iconSize * numRows)    + (numRows    * Toolbox.TOOLBOX_V_GAP)

        return Size(width, height)
