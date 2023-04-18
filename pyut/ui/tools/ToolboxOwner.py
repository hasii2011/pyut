
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Window

from pyut.ui.tools.Tool import Category
from pyut.ui.tools.Tool import Tool
from pyut.ui.tools.Toolbox import Toolbox

from pyut.ui.tools.ToolboxTypes import CategoryNames
from pyut.ui.tools.ToolboxTypes import ToolCategories
from pyut.ui.tools.ToolboxTypes import Tools


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
            self._toolCategories[tool.category] = Tools([tool])
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
