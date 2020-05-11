
from typing import List

from math import floor
from math import ceil

from os import path as osPath
from os import chdir
from os import getcwd

from org.pyut.PyutPreferences import PyutPreferences
from org.pyut.model.PyutClass import PyutClass
from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ui.UmlFrame import UmlFrame


class ToAscii(PyutToPlugin):
    """
    Python code generation/reverse engineering
    """
    def __init__(self, umlObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    A Pyut UML Frame
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
        defaultDir: str             = prefs.userDirectory

        selectedDir = self._askForDirectoryExport(preferredDefaultPath=defaultDir)
        if selectedDir == '':
            return
        print(f'selectedDir: {selectedDir}')
        chdir(selectedDir)

        for oglObject in oglObjects:

            if not isinstance(oglObject, OglClass):
                continue

            o: PyutClass = oglObject.getPyutObject()

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

            fields = [str(x) for x in o.fields]
            methods = [str(x) for x in o.getMethods()]

            lineLength = max([len(x) for x in base + fields + methods]) + 4

            file.write(lineLength * "-" + "\n")

            for line in base:
                spaces = lineLength - 4 - len(line)
                file.write("| " + int(floor(spaces / 2.0)) * " " + line + int(ceil(spaces / 2.0)) * " " + " |\n")

            file.write("|" + (lineLength - 2) * "-" + "|\n")

            for line in fields:
                file.write("| " + line + (lineLength - len(line) - 4) * " " + " |\n")

            file.write("|" + (lineLength - 2) * "-" + "|\n")

            for line in methods:
                file.write("| " + line + (lineLength - len(line) - 4) * " " + " |\n")

            file.write(lineLength * "-" + "\n\n")

            file.write(o.description)

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
            self.displayNothingSelected()
            return
        self.write(selectedObjects)
