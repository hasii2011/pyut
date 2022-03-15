
from wx import ICON_ERROR
from wx import MessageDialog
from wx import OK

from org.pyut.ui.Mediator import Mediator

from org.pyut.plugins.base.PyutPlugin import PyutPlugin
from org.pyut.plugins.base.PluginTypes import OglClasses

from org.pyut.ui.UmlFrame import UmlFrame


class PyutToPlugin(PyutPlugin):
    """
    Note : Merge with PyutToPlugin
    """
    def __init__(self, umlObjects: OglClasses, umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    Pyut's UML Frame
        """
        super().__init__(umlFrame=umlFrame, ctrl=Mediator())
        self._umlObjects = umlObjects
        self._umlFrame = umlFrame

    @staticmethod
    def displayNothingSelected():
        booBoo: MessageDialog = MessageDialog(parent=None, message='Please select some frame objects',
                                              caption='Try Again!', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    @staticmethod
    def displayNoUmlFrame():
        booBoo: MessageDialog = MessageDialog(parent=None, message='No UML frame', caption='Try Again!', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    @staticmethod
    def displayNoUmlObjects():
        booBoo: MessageDialog = MessageDialog(parent=None, message='No UML objects', caption='Try Again!', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def getName(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "Unnamed tool plugin"

    def getAuthor(self) -> str:
        """
        Returns: The author's name
        """
        return "anonymous"

    def getVersion(self) -> str:
        """
        Returns: The plugin version string
        """
        return "0.0"

    def getMenuTitle(self) -> str:
        """
        Returns:  The menu title for this plugin
        """
        return "Untitled plugin"

    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns: if False, the import will be cancelled.
        """
        return True

    def callDoAction(self):
        """
        This is used internally, don't overload it.
        """
        if not self.setOptions():
            return
        selectedShapes = self._ctrl.getSelectedShapes()
        self.doAction(self._umlObjects, selectedShapes, self._umlFrame)

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram's frame

        Returns:
        """
        pass
