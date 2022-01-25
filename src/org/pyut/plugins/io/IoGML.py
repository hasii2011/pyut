
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.plugins.base.PluginTypes import OglClasses
from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin
from org.pyut.plugins.base.PyutPlugin import InputFormatType
from org.pyut.plugins.base.PyutPlugin import OutputFormatType

from org.pyut.plugins.gml.GMLExporter import GMLExporter

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ui.UmlFrame import UmlFrame


class IoGML(PyutIoPlugin):
    """
    Sample class for input/output plug-ins.
    """
    def __init__(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            oglObjects:  list of ogl objects
            umlFrame:    A Pyut umlFrame
        """
        super().__init__(oglObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "Output GML"

    def getAuthor(self) -> str:
        """
        Returns: The author's name
        """
        return "Humberto A. Sanchez II"

    def getVersion(self) -> str:
        """
        Returns: The plugin version string
        """
        return "1.0"

    def getInputFormat(self) -> InputFormatType:
        """
        Returns:
            None, I don't read GML
        """
        return cast(InputFormatType, None)

    def getOutputFormat(self) -> OutputFormatType:
        """

        Returns:
            Return a specification tuple.
        """
        return OutputFormatType(('GML', 'gml', 'Graph Modeling Language - Portable Format for Graphs'))

    def setImportOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            if False, the import will be cancelled.
        """
        return False

    def setExportOptions(self) -> bool:
        """
        Prepare the export.
        This can be used to ask the user some questions

        Returns:
            if False, the export will be cancelled.
        """
        return True

    def read(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Read data from filename. Abstract.

        Args:
            oglObjects: list of imported objects
            umlFrame:   Pyut's UmlFrame
        """
        pass

    def write(self, oglObjects: OglClasses):
        """
        Write data

        Args:
            oglObjects:     list of exported objects
        """
        gmlExporter: GMLExporter = GMLExporter()

        gmlExporter.translate(umlObjects=oglObjects)

        fqFileName: str = self._askForFileExport()

        if fqFileName != '':
            gmlExporter.write(fqFileName)
        else:
            self.logger.debug('Export Cancelled no file name')
