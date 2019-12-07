
from org.pyut.ui.tools.Tool import Tool
from org.pyut.ui.tools.Toolbox import Toolbox

# TODO : add observer-observable model to support dynamic plugins


class ToolboxOwner:
    """
    ToolboxOwner : a toolbox owner
    """

    def __init__(self, parent):
        """
        Constructor.

        @param wxWindow parent : parent window
        """
        # Members vars
        self._toolCategories = {}
        self._parent = parent

    def displayToolbox(self, category):
        """
        display a toolbox

        @param string category : category of tools to display
        """
        toolbox = Toolbox(self._parent, self)
        toolbox.setCategory(category)

    def registerTool(self, tool: Tool):
        """
        Add a tool to toolboxes

        @param Tool tool : The tool to add
        """
        if tool.initialCategory not in self._toolCategories:
            self._toolCategories[tool.initialCategory] = [tool]
        else:
            self._toolCategories[tool.initialCategory].append(tool)

    def getCategoryTools(self, category):
        """
        Return all tools for a specified category

        @param string category : the category of tools to get
        """
        return self._toolCategories[category]

    def getCategories(self):
        """
        Return all categories of tools

        @return string[] of categories
        """
        return list(self._toolCategories.keys())
