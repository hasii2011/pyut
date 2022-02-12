from logging import Logger
from logging import getLogger
from typing import cast

from os import sep as osSep

from wx import BeginBusyCursor as wxBeginBusyCursor
from wx import EndBusyCursor as wxEndBusyCursor

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

from org.pyut.plugins.io.javasupport.ReverseJava import ReverseJava

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class IoJavaReverse(PyutIoPlugin):

    def __init__(self, oglObjects, umlFrame):

        super().__init__(oglObjects=oglObjects, umlFrame=umlFrame)

        self.logger: Logger = getLogger(__name__)

    """
    Java reverse engineering plugin.
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """
        return "Java code reverse engineering"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """
        return "C.Dutoit <dutoitc@hotmail.com>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author C.Dutoit - <dutoitc@hotmail.com>
        @since 1.1
        """
        return "1.0"

    def getInputFormat(self):
        return "Java", "java", "Java file format"

    def getOutputFormat(self):
        """
        Return a specification tuple.

        @return tuple
        @author C.Dutoit - dutoitc@hotmail.com
        @since 1.1
        """
        return None

    def read(self, oglObjects, umlFrame):
        """
        reverse engineering

        Args:
            oglObjects:     list of imported objects
            umlFrame:       a Pyut UmlFrame
        """
        # Ask for file import
        fileNames, directory = self._askForFileImport(True)
        if len(fileNames) == 0:
            return False

        # Reverse Java
        wxBeginBusyCursor()
        try:
            rj: ReverseJava = ReverseJava(cast(UmlClassDiagramsFrame, umlFrame))
            for filename in fileNames:
                fqnName: str = f'{directory}{osSep}{filename}'
                rj.analyseFile(fqnName)
            rj.layoutDiagram()
            # noinspection PyProtectedMember
            self.logger.warning(f'{len(rj._subClassMap)=}')
        finally:
            wxEndBusyCursor()
