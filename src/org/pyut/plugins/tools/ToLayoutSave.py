
from wx import FD_CHANGE_DIR
from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE

from wx import FileSelector

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin


class ToLayoutSave(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.5 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        Constructor.

        @param umlObjects : list of ogl objects
        @param umlFrame : the umlframe of pyut
        """
        super().__init__(umlObjects, umlFrame)
        self._umlFrame = umlFrame

    def getName(self) -> str:
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "Layout plugin (save)"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "Cedric DUTOIT <dutoitc@hotmail.com>"

    def getVersion(self) -> str:
        """
        This method returns the version of the plugin.

        @return string
        @since 1.1
        """
        return "1.0"

    def getMenuTitle(self) -> str:
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "Layout (save)"

    def setOptions(self) -> bool:
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
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        file = FileSelector(
            "Choose a file name to export layout",
            wildcard="Layout file (*.lay) |*.lay",
            flags=FD_SAVE | FD_OVERWRITE_PROMPT | FD_CHANGE_DIR
        )

        f = open(file, "w")
        for el in umlObjects:
            f.write(el.getPyutObject().getName() + "," +
                    str(el.GetPosition()[0]) + "," +
                    str(el.GetPosition()[1]) + "," +
                    str(el.GetSize()[0]) + "," +
                    str(el.GetSize()[1]) + "\n")
        f.close()
