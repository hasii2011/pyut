
from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from org.pyut.general.PyutVersion import PyutVersion
from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

from org.pyut.ogl.OglClass import OglClass
from org.pyut.plugins.io.pyumlsupport.OglToPyUmlDefinition import OglToPdfDefinition

from org.pyut.ui.UmlFrame import UmlFrame


class IoPdf(PyutIoPlugin):
    """
    """
    def __init__(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            oglObjects:  list of ogl objects
            umlFrame:    A Pyut umlFrame
        """
        super().__init__(oglObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

        self._exportFileName: str = ''

    def getName(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "Output PDF"

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

    def getInputFormat(self) -> Tuple[str, str, str]:
        """
        Returns:
            None, I don't read PDF
        """
        return cast(Tuple[str, str, str], None)

    def getOutputFormat(self) -> Tuple[str, str, str]:
        """
        A Tuple with

            * name of the output format
            * extension of the output format
            * textual description of the plugin output format

        Returns:
            Return a specification tuple.
        """
        return 'PDF', 'pdf', 'A simple PDF for UML diagrams'

    def setImportOptions(self) -> bool:
        """
        Returns:
            if False, the import will be cancelled.
        """
        return False

    def setExportOptions(self) -> bool:
        """
        TODO:  Popup dialog of where to write .pdf file

        Returns:
            if False, the export will be cancelled.
        """
        fqFileName: str = self._askForFileExport(defaultFileName='PyutExport')  # TODO make this a preference

        if fqFileName == '':
            self.logger.debug('Export Cancelled no file name')
            return False
        else:
            self._exportFileName = fqFileName

        return True

    def read(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Read data from filename. Abstract.

        Args:
            oglObjects: list of imported objects
            umlFrame:   Pyut's UmlFrame
        """
        pass

    def write(self, oglObjects: List[OglClass]):
        """
        Write data

        Args:
            oglObjects:     list of exported objects
        """
        self.logger.info(f'export file name: {self._exportFileName}')
        wxYield()

        pluginVersion: str = self.getVersion()
        pyutVersion:   str = PyutVersion.getPyUtVersion()

        oglToPdf: OglToPdfDefinition = OglToPdfDefinition(fqFileName=self._exportFileName,
                                                          dpi=75,           # TODO get this from runtime query
                                                          pyutVersion=pyutVersion,
                                                          pluginVersion=pluginVersion
                                                          )

        oglToPdf.toClassDefinitions(oglObjects=oglObjects)
        oglToPdf.layoutLines(oglObjects=oglObjects)
        oglToPdf.write()
