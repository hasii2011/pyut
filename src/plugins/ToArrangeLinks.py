
from typing import List

from logging import Logger
from logging import getLogger

from org.pyut.ogl.OglLink import OglLink

from plugins.PyutToPlugin import PyutToPlugin


class ToArrangeLinks(PyutToPlugin):
    """
    Plugin to arrange all links
    Python code generation/reverse engineering

    @version $Revision: 1.2 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        Constructor.

        @param umlObjects  : list of ogl objects
        @param umlFrame : the umlframe of pyut
        """
        super().__init__(umlObjects, umlFrame)
        self._umlFrame = umlFrame
        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "Arrange links"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "C�dric DUTOIT <dutoitc@shimbawa.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @since 1.1
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Arrange links"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
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
                self.logger.info(f"Optimizing: {oglObject}")
                oglObject.optimizeLine()
            else:
                self.logger.info(f"No line optimizing for: {oglObject}")
