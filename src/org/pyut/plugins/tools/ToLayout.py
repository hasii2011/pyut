from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OPEN
from wx import FileSelector

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin


class ToLayout(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.5 $
    """
    def __init__(self, umlObjects, umlFrame):
        """
        """
        super().__init__(umlObjects, umlFrame)
        self._umlFrame = umlFrame

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "Layout plugin (read)"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "Cedric DUTOIT <dutoitc@hotmail.com>"

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
        return "Layout (read)"

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
        Do the tool's action

        Args:
            umlObjects:      list of the uml objects of the diagram
            selectedObjects: list of the selected objects
            umlFrame:        the diagram frame
        """

        filename = FileSelector("Choose a layout file to import",
                                # wildcard="Layout file (*.lay) | *.lay",    # temp on OS X fixes it
                                flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR)

        if filename == '':
            return False
        f = open(filename, "r")
        lstFile = f.readlines()
        f.close()
        lst = []
        for el in lstFile:
            spl = el.split(",")
            lst.append(spl)
        print(f"Read {lst}")

        for oglObject in umlObjects:
            for line in lst:
                if line[0] == oglObject.pyutObject.name:
                    oglObject.SetPosition(int(line[1]), int(line[2]))
                    oglObject.SetSize(int(line[3]), int(line[4]))
