
from typing import List
from typing import Tuple

from logging import Logger
from logging import getLogger
from typing import cast

from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

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

