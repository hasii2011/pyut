
from io import StringIO
from .PyutToPlugin import PyutToPlugin
from PyutClass import PyutClass
from OglClass import OglClass
from PyutMethod import PyutMethod
from PyutParam import PyutParam
from PyutField import PyutField
from PyutConsts import *
# from wxPython.wx import *
import wx

import os


class ToAscii(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.4 $
    """
    def __init__(self, umlObjects, umlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    the umlframe of pyut
        """
        PyutToPlugin.__init__(self, umlObjects, umlFrame)
        self._umlFrame = umlFrame

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "ASCII Class export"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "Philippe Waelti <pwaelti@eivd.ch>"

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
        return "ASCII Class Export"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return True

    def write(self, oglObjects):
        """
        Write data to filename.

        @param OglObjects : Objects to export
        @author Philippe Waelti
        """
        import math
        import os.path

        for oglObject in oglObjects:

            if not isinstance(oglObject, OglClass):
                continue

            o = oglObject.getPyutObject()

            suffix = 2
            filename = o.getName()

            while os.path.exists(filename + ".acl"):
                print("File exists")
                filename += str(suffix)
                suffix += 1

            file = open(filename + ".acl", "w")

            base = []
            base.append(o.getName())
            if o.getStereotype() is not None:
                base.append(str(o.getStereotype()))

            fields = [str(x) for x in o.getFields()]
            methods = [str(x) for x in o.getMethods()]

            lnlgth = max([len(x) for x in base + fields + methods]) + 4

            file.write(lnlgth * "-" + "\n")

            for line in base:
                spaces = lnlgth - 4 - len(line)
                file.write("| " + int(math.floor(spaces / 2.0)) * " " +
                        line + int(math.ceil(spaces / 2.0)) * " " + " |\n")

            file.write("|" + (lnlgth - 2) * "-" + "|\n")

            for line in fields:
                file.write("| " + line + (lnlgth - len(line) - 4) * " "
                    + " |\n")

            file.write("|" + (lnlgth - 2) * "-" + "|\n")

            for line in methods:
                file.write("| " + line + (lnlgth - len(line) - 4) * " "
                    + " |\n")

            file.write(lnlgth * "-" + "\n\n")

            file.write(o.getDescription())

            file.close()

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if len(selectedObjects) < 1:
            print("Please select class(es)")
            return
        self.write(selectedObjects)
