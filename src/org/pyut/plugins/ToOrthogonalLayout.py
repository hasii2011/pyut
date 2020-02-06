
from typing import List

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ui.UmlFrame import UmlFrame


from org.pyut.plugins.PyutToPlugin import PyutToPlugin


class ToOrthogonalLayout(PyutToPlugin):
    """
    Layout the UML class diagram by changing the links to an orthogonal layout
    """
    def __init__(self, umlObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    the umlframe of pyut
        """
        super().__init__(umlObjects, umlFrame)

    def getName(self):
        """
        Returns: the name of the plugin.
        """
        return "Orthogonal Layout"

    def getAuthor(self):
        """
        Returns:
            The author's name
        """
        return "Humberto A. Sanchez II"

    def getVersion(self):
        """
        Returns:
            The plugin version string
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Returns:
            The menu title for this plugin
        """
        return "Orthogonal Layout"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            If False, the import will be cancelled.
        """
        return True

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Do the tool's action

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """
        pass
