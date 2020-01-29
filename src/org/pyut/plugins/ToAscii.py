
from typing import List

from math import floor
from math import ceil

from os import path as osPath
from os import chdir
from os import getcwd

from wx import MessageDialog
from wx import DirDialog

from wx import OK
from wx import ID_CANCEL

from org.pyut.PyutPreferences import PyutPreferences
from org.pyut.plugins.PyutToPlugin import PyutToPlugin

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ui.UmlFrame import UmlFrame


class ToAscii(PyutToPlugin):
    """
    Python code generation/reverse engineering
    """
    def __init__(self, umlObjects, umlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    the umlframe of pyut
        """
        PyutToPlugin.__init__(self, umlObjects, umlFrame)
        self._umlFrame = umlFrame

    def getName(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "ASCII Class export"

    def getAuthor(self) -> str:
        """
        Returns: The author's name
        """
        return "Philippe Waelti <pwaelti@eivd.ch>"

    def getVersion(self) -> str:
        """
        Returns: The plugin version string
        """
        return "1.0"

    def getMenuTitle(self) -> str:
        """
        Returns:  The menu title for this plugin
        """
        return "ASCII Class Export"

    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns: if False, the import will be cancelled.
        """
        return True

    def write(self, oglObjects: List[OglClass]):
        """
        Write the data to a file
        Args:
            oglObjects:   The objects to export
        """

        saveDir:    str             = getcwd()
        prefs:      PyutPreferences = PyutPreferences()
        defaultDir: str             = prefs[PyutPreferences.STARTUP_DIRECTORY]

        dirDialog: DirDialog = DirDialog(parent=None, message='Save ASCII files to directory?', defaultPath=defaultDir)
        ans = dirDialog.ShowModal()
        if ans == ID_CANCEL:
            chdir(saveDir)
            return
        selectedDir = dirDialog.GetPath()
        print(f'selectedDir: {selectedDir}')
        chdir(selectedDir)

        for oglObject in oglObjects:

            if not isinstance(oglObject, OglClass):
                continue

            o = oglObject.getPyutObject()

            suffix = 2
            filename = o.getName()

            while osPath.exists(filename + ".acl"):
                print("File exists")
                filename += str(suffix)
                suffix += 1

            file = open(filename + ".acl", "w")

            # base = []
            base = [o.getName()]
            if o.getStereotype() is not None:
                base.append(str(o.getStereotype()))

            fields = [str(x) for x in o.getFields()]
            methods = [str(x) for x in o.getMethods()]

            lnlgth = max([len(x) for x in base + fields + methods]) + 4

            file.write(lnlgth * "-" + "\n")

            for line in base:
                spaces = lnlgth - 4 - len(line)
                file.write("| " + int(floor(spaces / 2.0)) * " " + line + int(ceil(spaces / 2.0)) * " " + " |\n")

            file.write("|" + (lnlgth - 2) * "-" + "|\n")

            for line in fields:
                file.write("| " + line + (lnlgth - len(line) - 4) * " " + " |\n")

            file.write("|" + (lnlgth - 2) * "-" + "|\n")

            for line in methods:
                file.write("| " + line + (lnlgth - len(line) - 4) * " " + " |\n")

            file.write(lnlgth * "-" + "\n\n")

            file.write(o.getDescription())

            file.close()

        chdir(saveDir)

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """
        if len(selectedObjects) < 1:
            booBoo: MessageDialog = MessageDialog(parent=None, message='Please select classes(es)',
                                                  caption='Try Again!', style=OK)
            booBoo.ShowModal()
            return
        self.write(selectedObjects)
