from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.ui.Mediator import Mediator
from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.base.PyutPlugin import PyutPlugin

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
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, oglObjects, umlFrame):
        """

        Args:
            oglObjects: list of ogl objects
            umlFrame:   The Pyut UML Frame
        """
        super().__init__(umlFrame, Mediator())
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

    def getInputFormat(self) -> PyutPlugin.INPUT_FORMAT_TYPE:
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
        return cast(PyutPlugin.INPUT_FORMAT_TYPE, None)

    def getOutputFormat(self) -> PyutPlugin.OUTPUT_FORMAT_TYPE:
        """
        return None if this plugin can't write.
        otherwise, return a tuple with
            name of the output format
            extension of the output format
            textual description of the plugin output format
        example:
            return ("Text", "txt", "Tabbed text...")

        Returns:
            Return a specification tuple.
        """
        return cast(PyutPlugin.OUTPUT_FORMAT_TYPE, None)

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

    def write(self, oglObjects: PyutPlugin.OglClasses):
        """
         Write data to filename. Abstract.
        Args:
            oglObjects:  list of exported objects

        """
        pass

    def doImport(self) -> PyutPlugin.OglClasses:
        """
        Called by Pyut to begin the import process.

        Returns:
            None if cancelled, else a list of OglClass objects
        """
        if self.getInputFormat() is not None:
            if not self.setImportOptions():
                return cast(PyutPlugin.OglClasses, None)
            self.read(self.__oglObjects, self._umlFrame)
            return self.__oglObjects
        else:
            return cast(PyutPlugin.OglClasses, None)

    def doExport(self):
        """
        Called by Pyut to begin the export process.
        """
        if self._umlFrame is None:
            self.displayNoUmlFrame()
            return

        outputFormat: Tuple[str, str, str] = self.getOutputFormat()
        if outputFormat is not None:
            if not self.setExportOptions():
                return None

            mediator: Mediator = Mediator()
            prefs: PyutPreferences = PyutPreferences()
            if prefs.pyutIoPluginAutoSelectAll is True:
                mediator.selectAllShapes()
            self.__oglObjects = mediator.getSelectedShapes()
            if len(self.__oglObjects) == 0:
                self.displayNoSelectedUmlObjects()
            else:
                # write the file
                self.write(self.__oglObjects)
                mediator.deselectAllShapes()
        else:
            PyutIoPlugin.clsLogger.info(f'Output format is: {outputFormat}')
