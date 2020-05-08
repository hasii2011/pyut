
from logging import Logger
from logging import getLogger

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin


class ToTransforms(PyutToPlugin):
    """
    A plugin for making transformations : translation, rotations, ...

    """
    def __init__(self, oglObjects, umlFrame: UmlFrame):
        """
        Constructor.

        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : Pyut's UML frame

        """
        super().__init__(oglObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

        self._oglObjects = oglObjects
        self._umlFrame: UmlFrame = umlFrame

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        """
        return "Transformations"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        """
        return "C.Dutoit"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        """
        # Return the menu title as it must be displayed
        return "Transformations"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        """
        return True

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do move classes

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        """
        if umlFrame is None:
            # TODO : displayError "No frame opened"
            self.logger.error(f"No frame opened")
            return

        # (frameW, frameH) = self._umlFrame.GetSizeTuple()
        (frameW, frameH) = self._umlFrame.GetSize()
        self.logger.info(f'frameW: {frameW} - frameH: {frameH}')
        for obj in umlObjects:
            x, y = obj.GetPosition()
            newX: int = frameW - x
            self.logger.info(f"x,y: {x},{y} - newX: {newX}")
            obj.SetPosition(newX, y)
