
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BitmapButton

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_CLOSE
from wx import EXPAND
from wx import FRAME_EX_METAL
from wx import FRAME_FLOAT_ON_PARENT
from wx import GridSizer
from wx import ID_ANY
from wx import MiniFrame

from wx import Size
from wx import Window
from wx import DefaultPosition

from org.pyut.ui.tools.Tool import Tool


class Toolbox(MiniFrame):

    def __init__(self, parentWindow: Window, toolboxOwner):
        """

        Args:
            parentWindow:   wxWindow parentWindow
            toolboxOwner:   ToolboxOwner
        """

        from org.pyut.ui.tools.ToolboxOwner import ToolboxOwner

        self.logger: Logger = getLogger(__name__)

        # windowStyle = STATIC_BORDER | SYSTEM_MENU | CAPTION | FRAME_FLOAT_ON_PARENT
        windowStyle = DEFAULT_FRAME_STYLE | FRAME_EX_METAL | FRAME_FLOAT_ON_PARENT
        super().__init__(parentWindow, ID_ANY, "Tool Box", DefaultPosition, Size(100, 200), style=windowStyle)

        self._tools         = []
        self._category      = ""

        self._parentWindow: Window        = parentWindow
        self._toolboxOwner: ToolboxOwner  = toolboxOwner

        self._gridSizer: GridSizer = GridSizer(3, 6, 2, 2)      # rows, cols, vGap, hGap

        self.SetSizer(self._gridSizer)
        self.Bind(EVT_CLOSE, self.eventClose)

    def setCategory(self, category):
        """
        Define the toolbox category for this toolbox.  However, this toolbox has to go to
        the toolbox owner to get the tools of type 'category'

        Args:
            category:  The new category
        """
        self._category = category
        self._tools: List[Tool] = self._toolboxOwner.getCategoryTools(category)

        for tool in self._tools:

            tool: Tool = cast(Tool, tool)
            self.logger.warning(f'{tool.caption=}')
            bitMapButton: BitmapButton = BitmapButton(parent=self, id=tool.wxID, bitmap=tool.img)
            self._gridSizer.Add(bitMapButton, 0, EXPAND)

    # noinspection PyUnusedLocal
    def eventClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE
        """
        self.Destroy()
