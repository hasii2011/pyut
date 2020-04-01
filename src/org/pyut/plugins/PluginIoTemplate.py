
from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.plugins.PyutIoPlugin import PyutIoPlugin

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ui.UmlFrame import UmlFrame


class PluginName(PyutIoPlugin):
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
        return "No name"

    def getAuthor(self) -> str:
        """
        Returns: The author's name
        """
        return "No author"

    def getVersion(self) -> str:
        """
        Returns: The plugin version string
        """
        return "0.0"

    def getInputFormat(self) -> Tuple[str, str, str]:
        """
        return None if this plugin can't read.
        otherwise, return a tuple with
            name of the input format
            extension of the input format
            textual description of the plugin input format
            example :
                return ("Text", "txt", "Tabbed text...")

        Returns:
            Return a specification tuple.
        """
        return cast(Tuple[str, str, str], None)

    def getOutputFormat(self) -> Tuple[str, str, str]:
        """
        return None if this plugin can't write.
        otherwise, return a tupple with
            name of the output format
            extension of the output format
            textual description of the plugin output format
        example:
            return ("Text", "txt", "Tabbed text...")

        Returns:
            Return a specification tuple.
        """
        return cast(Tuple[str, str, str], None)

    def setImportOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            if False, the import will be cancelled.
        """
        return True

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

    def write(self, oglObjects: List[OglClass]):
        """
        Write data

        Args:
            oglObjects:     list of exported objects
        """
        pass
