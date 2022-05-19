
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglLink import OglLink

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin


class ToArrangeLinks(PyutToPlugin):
    """
    Plugin to arrange all links
    """
    def __init__(self, umlObjects, umlFrame):
        """

        Args:
            umlObjects: list of ogl objects
            umlFrame:   A Pyut UML frame
        """
        super().__init__(umlObjects, umlFrame)
        self.logger: Logger = getLogger(__name__)
        self._umlFrame = umlFrame

    def getName(self) -> str:
        """

        Returns:
            The name of the plugin.

        """
        return "Arrange links"

    def getAuthor(self) -> str:
        """

        Returns:
            The author of the plugin.
        """
        return "Cedric DUTOIT <dutoitc@shimbawa.ch>"

    def getVersion(self) -> str:
        """

        Returns:
            The version of the plugin.
        """
        return "1.0"

    def getMenuTitle(self) -> str:
        """

        Returns:
            A menu title string
        """
        return "Arrange links"

    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            If `False`, the import is cancelled.
        """
        return True

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """

        Args:
            umlObjects: list of the uml objects of the diagram
            selectedObjects:  list of the selected objects
            umlFrame: the frame of the diagram
        """
        for oglObject in umlObjects:
            if isinstance(oglObject, OglLink):
                oglLink: OglLink = cast(OglLink, oglObject)
                self.logger.info(f"Optimizing: {oglLink}")
                oglLink.optimizeLine()
            else:
                self.logger.info(f"No line optimizing for: {oglObject}")
