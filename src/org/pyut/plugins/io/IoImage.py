
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import OK
from wx import Yield as wxYield

from org.pyut.general.PyutVersion import PyutVersion

from ogl.OglClass import OglClass

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin
from org.pyut.plugins.base.PyutPlugin import InputFormatType
from org.pyut.plugins.base.PyutPlugin import OutputFormatType

from org.pyut.plugins.io.pyumlsupport.DlgImageOptions import DlgImageOptions
from org.pyut.plugins.io.pyumlsupport.ImageOptions import ImageOptions
from org.pyut.plugins.io.pyumlsupport.OglToPyUmlDefinition import OglToPyUmlDefinition

from org.pyut.ui.UmlFrame import UmlFrame

from pyumldiagrams import Defaults


class IoImage(PyutIoPlugin):

    def __init__(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Args:
            oglObjects:  list of ogl objects
            umlFrame:    A Pyut umlFrame
        """
        super().__init__(oglObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

        imageOptions: ImageOptions = ImageOptions()

        imageOptions.horizontalGap = Defaults.DEFAULT_HORIZONTAL_GAP
        imageOptions.verticalGap   = Defaults.DEFAULT_VERTICAL_GAP

        imageOptions.outputFileName = Defaults.DEFAULT_FILE_NAME

        self._imageOptions = imageOptions

    def getName(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "Out Images"

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
            None, I don't read images
        """
        return cast(InputFormatType, None)

    def getOutputFormat(self) -> OutputFormatType:
        """
        A Tuple with

            * name of the output format
            * extension of the output format
            * textual description of the plugin output format

        Returns:
            Return a specification tuple.
        """
        return OutputFormatType(('Image', 'png', 'png, bmp, gif, or jpg'))

    def setImportOptions(self) -> bool:
        """

        Returns:
            if False, the import will be cancelled.
        """
        return False

    def setExportOptions(self) -> bool:
        """
        Popup options dialog
        """

        with DlgImageOptions(self._umlFrame, imageOptions=self._imageOptions) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.warning(f'Options: {self._imageOptions}')
            else:
                self.logger.warning(f'Cancelled')
                return False

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

        oglToPyUmlDef: OglToPyUmlDefinition = OglToPyUmlDefinition(imageOptions=self._imageOptions,
                                                                   pyutVersion=pyutVersion,
                                                                   pluginVersion=pluginVersion
                                                                   )

        oglToPyUmlDef.toClassDefinitions(oglObjects=oglObjects)
        oglToPyUmlDef.layoutLines(oglObjects=oglObjects)
        oglToPyUmlDef.write()
