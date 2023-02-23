
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Frame
from wx import ToolBar

from wx import NewIdRef as wxNewIdRef

from hasiicommon.Singleton import Singleton

from pyut.ui.tools.Tool import Category
from pyut.ui.tools.Tool import Tool
from pyut.ui.tools.ToolboxOwner import ToolboxOwner
from pyut.ui.tools.ToolboxTypes import CategoryNames


class ToolBoxHandler(Singleton):

    # noinspection PyAttributeOutsideInit
    def init(self, **kwargs):
        self.logger:       Logger       = getLogger(__name__)
        self._toolboxOwner: ToolboxOwner = cast(ToolboxOwner, None)
        self._toolBar:      ToolBar      = cast(ToolBar, None)

    def _setToolboxOwner(self, appFrame: Frame):
        """
        Register the application's main frame.

        Args:
            appFrame:  Application's main frame
        """
        self._toolboxOwner = ToolboxOwner(appFrame)

    def _setToolBar(self, tb: ToolBar):
        """
        Register the toolbar.

        Args:
            tb: The toolbar
        """
        self._toolBar = tb

    def _setToolBarTools(self, tools: List[wxNewIdRef]):
        """
        Register the toolbar tools.

        Args:
            tools:  a list of the tools IDs
        """
        self._tools = tools

    def _setApplicationFrame(self, applicationFrame):
        self._toolboxOwner = ToolboxOwner(parent=applicationFrame)

    @property
    def toolBoxCategoryNames(self) -> CategoryNames:
        """
        Return all toolbox category names

        Returns:  The category names
        """
        return self._toolboxOwner.getCategories()

    toolBoxOwner     = property(fset=_setToolboxOwner)
    toolBar          = property(fset=_setToolBar)
    toolBarTools     = property(fset=_setToolBarTools)
    applicationFrame = property(fset=_setApplicationFrame)

    def addTool(self, tool: Tool):
        """
        Add a tool to a toolbox

        Args:
            tool:  The tool to add

        """
        self._toolboxOwner.registerTool(tool)

    def displayToolbox(self, category: Category):
        """
        Display a toolbox

        Args:
            category:  The tool category to display
        """
        self._toolboxOwner.displayToolbox(category)

    def getToolboxesCategories(self) -> CategoryNames:
        """
        Return all toolbox categories

        Returns:  The category names
        """
        return self._toolboxOwner.getCategories()
