
from org.pyut.plugins.base.PluginTypes import OglClasses
from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin
from org.pyut.plugins.dtd.DTDParser import DTDParser

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class IoDTD(PyutIoPlugin):
    """
    To save XML file format.

    @version $Revision: 1.8 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "IoDTD"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "C.Dutoit <dutoitc@hotmail.com>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "1.0"

    def getInputFormat(self):
        """
        Return a specification tuple.

        @return tuple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        # return None if this plugin can't read.
        # otherwise, return a tuple with
        # - name of the input format
        # - extension of the input format
        # - textual description of the plugin input format
        # example : return ("Text", "txt", "Tabbed text...")
        return "DTD", "dtd", "W3C DTD 1.0 file format"

    def getOutputFormat(self):
        """
        Return a specification tuple.

        @return tuple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return None

    def setExportOptions(self):
        """
        Prepare the export.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the export will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return False

    def write(self, oglObjects):
        """
        Write data to filename. Abstract.

        Args:
            oglObjects: list of exported objects

        Returns:  True if write was successful, False if error or canceled

        """
        return False

    def read(self, oglObjects: OglClasses, umlFrame: UmlClassDiagramsFrame):
        """

        Args:
            oglObjects:  Unused by this plugin;  It adds them directly to the frame; Note:  I wonder if this API needs updating

            umlFrame:  Pyut's UmlFrame

        Returns:  True if import succeeded, False if error or cancelled
        """
        # Ask the user which destination file he wants
        filename = self._askForFileImport()
        if filename == "":
            return False

        dtdParser: DTDParser = DTDParser(umlFrame=umlFrame)
        return dtdParser.open(filename=filename)
