
from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.base.PyutPlugin import PyutPlugin
from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

from org.pyut.plugins.io.pyumlsupport.ImageFormat import ImageFormat
from org.pyut.plugins.io.pyumlsupport.ImageOptions import ImageOptions
from org.pyut.plugins.io.pyumlsupport.OglToPyUmlDefinition import OglToPyUmlDefinition

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutUtils import ScreenMetrics

from org.pyut.general.PyutVersion import PyutVersion


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

        self._imageOptions: ImageOptions = ImageOptions()

        self._imageOptions.imageFormat = ImageFormat.PDF

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
        return "1.1"

    def getInputFormat(self) -> PyutPlugin.INPUT_FORMAT_TYPE:
        """
        Returns:
            None, I don't read PDF
        """
        return cast(PyutPlugin.INPUT_FORMAT_TYPE, None)

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
        Popup dialog to determine where to write .pdf file

        Returns:
            if False, the export will be cancelled.
        """
        defaultFileName: str = PyutPreferences().pdfExportFileName
        fqFileName: str = self._askForFileExport(defaultFileName=defaultFileName)

        if fqFileName == '':
            self.logger.debug('Export Cancelled no file name')
            return False
        else:
            self._imageOptions.outputFileName = fqFileName

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
        self.logger.info(f'export file name: {self._imageOptions.outputFileName}')
        wxYield()

        pluginVersion: str = self.getVersion()
        pyutVersion:   str = PyutVersion.getPyUtVersion()

        screenMetrics: ScreenMetrics = PyutUtils.getScreenMetrics()
        dpi: int = screenMetrics.dpiX

        oglToPdf: OglToPyUmlDefinition = OglToPyUmlDefinition(imageOptions=self._imageOptions,
                                                              dpi=dpi,
                                                              pyutVersion=pyutVersion,
                                                              pluginVersion=pluginVersion
                                                              )

        oglToPdf.toClassDefinitions(oglObjects=oglObjects)
        oglToPdf.layoutLines(oglObjects=oglObjects)
        oglToPdf.write()
