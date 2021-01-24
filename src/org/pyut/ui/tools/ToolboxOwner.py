
from typing import Dict
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger
from wx import Window

from org.pyut.ui.tools.Tool import Tool
from org.pyut.ui.tools.Toolbox2 import Toolbox

Category       = NewType('Category',       str)
Tools          = NewType('NewType',        List[Tool])
CategoryNames  = NewType('CategoryNames',  List[Category])
ToolCategories = NewType('ToolCategories', Dict[Category, Tools])


class ToolboxOwner:

    """
    ToolboxOwner : a toolbox owner
    """

    def __init__(self, parent: Window):
        """

        Args:
            parent:  The parent window
        """
        self._toolCategories: ToolCategories = cast(ToolCategories, {})
        self._parent:         Window = parent

        self.logger: Logger = getLogger(__name__)

    def displayToolbox(self, category: Category):
        """
        Display a toolbox
        TODO:  Don't redisplay toolbox if we have already done so

        Args:
            category:  Category of tools to display
        """
        toolbox = Toolbox(self._parent, self)
        toolbox.setCategory(category)
        toolbox.Show(True)

    def registerTool(self, tool: Tool):
        """
        Add a tool to toolboxes

        Args:
            tool: The tool to add
        """

        if tool.category not in self._toolCategories:
            self._toolCategories[tool.category] = [tool]
            self.logger.info(f'Creating tool category: {tool.category}')
        else:
            self._toolCategories[tool.category].append(tool)

    def getCategoryTools(self, category: Category) -> Tools:
        """

        Args:
            category:  the category of tools to get

        Returns:  all tools for a specified category
        """
        toolsOfCategory: Tools = self._toolCategories[category]
        return toolsOfCategory

    def getCategories(self) -> CategoryNames:
        """
        Return all tool category names

        Returns:  The category names
        """
        categoryNames: CategoryNames = cast(CategoryNames, list(self._toolCategories.keys()))
        return categoryNames
