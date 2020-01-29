from typing import List
from typing import Tuple
from typing import cast

from org.pyut.general.Mediator import getMediator
from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.PyutPlugin import PyutPlugin
from org.pyut.ui.UmlFrame import UmlFrame


class PyutIoPlugin(PyutPlugin):
    """
    Base class for input/output plug-ins.

    If you want to do a new plugin, you must inherit from this class and
    redefine some methods.

    Information methods
    ---------------------

    These are:
        `getName`
        `getAuthor`
        `getVersion`
        `getInputFormat`
        `getOutputFormat`

    They must be redefined to return a simple string. See their respective doc.

    Interaction methods
    -------------------

    You can ask the user for plugin parameters. If you have to, just redefine
    these methods:
        `setImportOptions`
        `setExportOptions`

    Do whatever you need inside, and return True if all went good, or False
    to cancel the import/export.

    Real work
    ---------

    All the real import/export work is done in:
        `read(self, oglObjects, umlFrame)`
        `write(self, oglObjects)`

    Plugin call
    -----------

    To call a plugin, you need to instantiate it, and call one of:
        `doImport`
        `doExport`

    These two *Template Methods* (Design patterns) will call what needs to be.
    """
    def __init__(self, oglObjects, umlFrame):
        """
        Constructor.

        @param oglObjects : list of ogl objects
        @param umlFrame : the umlframe of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        super().__init__(umlFrame, getMediator())
        self.__oglObjects = oglObjects

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
        This can be used to ask the user some questions.

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
        return False

    def read(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            oglObjects: list of imported objects
            umlFrame: Pyut's UmlFrame
        """
        pass

    def write(self, oglObjects: List[OglClass]):
        """
         Write data to filename. Abstract.
        Args:
            oglObjects:  list of exported objects

        """
        pass

    def doImport(self) -> List[OglClass]:
        """
        Called by Pyut to begin the import process.
        Returns:
            None if cancelled, else a list of OglClass objects
        """

        # if this plugin can import
        if self.getInputFormat() is not None:
            # set user options for import
            if not self.setImportOptions():
                return cast(List[OglClass], None)
            # read it into the list
            self.read(self.__oglObjects, self._umlFrame)
            # return the new oglObjects list
            return self.__oglObjects
        else:
            return cast(List[OglClass], None)

    def doExport(self):
        """
        Called by Pyut to begin the export process.

        """
        # if this plugin can export
        outputFormat: Tuple[str, str, str] = self.getOutputFormat()
        if outputFormat is not None:
            # set user options for export
            if not self.setExportOptions():
                return None
            # write the file
            self.write(self.__oglObjects)
        else:
            print(f'Output format is None: {outputFormat}')
