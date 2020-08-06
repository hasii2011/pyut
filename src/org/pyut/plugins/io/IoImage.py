
from typing import List
from typing import Tuple

from logging import Logger
from logging import getLogger
from typing import cast

from pyumldiagrams import Defaults
from wx import OK

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin
from org.pyut.plugins.base.PyutPlugin import PyutPlugin
from org.pyut.plugins.io.pyumlsupport.DlgImageOptions import DlgImageOptions
from org.pyut.plugins.io.pyumlsupport.ImageOptions import ImageOptions

from org.pyut.ui.UmlFrame import UmlFrame


class IoImage(PyutIoPlugin):

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

    def getInputFormat(self) -> Tuple[str, str, str]:
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
        return 'Image', 'png', 'png, bmp, gif, or jpg'

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
        imageOptions: ImageOptions = ImageOptions()

        imageOptions.horizontalGap = Defaults.DEFAULT_HORIZONTAL_GAP
        imageOptions.verticalGap   = Defaults.DEFAULT_VERTICAL_GAP

        imageOptions.outputFileName = Defaults.DEFAULT_FILE_NAME

        with DlgImageOptions(self._umlFrame, imageOptions=imageOptions) as dlg:
            dlg: DlgImageOptions = cast(DlgImageOptions, dlg)
            if dlg.ShowModal() == OK:
                self.logger.warning(f'Options: {dlg.imageOptions}')
            else:
                self.logger.warning(f'Cancelled')

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
        pass
