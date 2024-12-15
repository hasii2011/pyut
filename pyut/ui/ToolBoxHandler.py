
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Frame
from wx import ToolBar

from wx import NewIdRef as wxNewIdRef


from codeallybasic.SingletonV3 import SingletonV3

from pyut.ui.tools.Tool import Category
from pyut.ui.tools.Tool import Tool
from pyut.ui.tools.ToolboxOwner import ToolboxOwner
from pyut.ui.tools.ToolboxTypes import CategoryNames


PARAMETER_FRAME: str = 'frame'


class ToolBoxHandler(metaclass=SingletonV3):

    def __init__(self, **kwargs):

        self.logger:        Logger       = getLogger(__name__)

        assert PARAMETER_FRAME in kwargs, 'We need a frame to initialize ourselves'
        frame: Frame = kwargs[PARAMETER_FRAME]

        self._toolboxOwner: ToolboxOwner = ToolboxOwner(parent=frame)

        self._toolBar:      ToolBar      = cast(ToolBar, None)

        self.logger.debug('Executed ToolBoxHandler constructor')

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
            tools:  a list of the tool IDs
        """
        self._tools = tools

    @property
    def toolBoxCategoryNames(self) -> CategoryNames:
        """
        Return all toolbox category names

        Returns:  The category names
        """
        return self._toolboxOwner.getCategories()

    # noinspection PyTypeChecker
    toolBar      = property(fget=None, fset=_setToolBar)
    # noinspection PyTypeChecker
    toolBarTools = property(fget=None, fset=_setToolBarTools)

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

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
