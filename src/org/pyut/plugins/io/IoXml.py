
from os import getcwd
from os import chdir

from wx import CANCEL
from wx import CENTRE
from wx import ICON_QUESTION
from wx import MessageBox
from wx import YES
from wx import YES_NO

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

from org.pyut.general.PyutXmlFinder import PyutXmlFinder


class IoXml(PyutIoPlugin):
    """
    To save XML file format.

    @version $Revision: 1.10 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "IoXml"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "Deve Roux <droux@eivd.ch>"

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
        Return a specification tupple.

        @return tupple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        # return None if this plugin can't read.
        # otherwise, return a tupple with
        # - name of the input format
        # - extension of the input format
        # - textual description of the plugin input format
        # example : return ("Text", "txt", "Tabbed text...")
        return "XML", "xml", "Pyut XML file"

    def getOutputFormat(self):
        """
        Return a specification tuple.

        @return tuple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        # return None if this plugin can't write.
        # otherwise, return a tupple with
        # - name of the output format
        # - extension of the output format
        # - textual description of the plugin output format
        # example : return ("Text", "txt", "Tabbed text...")
        return "XML", "xml", "Pyut XML file"

    def setExportOptions(self):
        """
        Prepare the export.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the export will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        rep = MessageBox("Do you want pretty xml ?", "Export option", style=YES_NO | CANCEL | CENTRE | ICON_QUESTION)
        self.pretty = (rep == YES)
        return rep != CANCEL

    def write(self, oglObjects) -> bool:
        """
        Write data to filename.

        Args:
            oglObjects:

        Returns: True if we succeeded with the write, Returns False if error occurred or if the operation was cancelled
        """
        oldPath = getcwd()
        # Ask the user which destination file he wants
        filename: str = self._askForFileExport()
        if filename == "":
            return False

        lastVersion: str = PyutXmlFinder.getLatestXmlVersion()
        myXml = PyutXmlFinder.getPyutXmlClass(theVersion=lastVersion)
        file = open(filename, "w")

        if int(lastVersion) >= 5:
            from org.pyut.ui.Mediator import Mediator

            mediator: Mediator = Mediator()

            fileHandling = mediator.getFileHandling()
            project      = fileHandling.getProjectFromOglObjects(oglObjects)
            doc          = myXml.save(project)
        else:
            doc = myXml.save(oglObjects)

        if self.pretty:
            text = doc.toprettyxml()
        else:
            text = doc.toxml()
        updatedXml: str = PyutXmlFinder.setAsISOLatin(text)

        file.write(updatedXml)
        file.close()
        chdir(oldPath)
        return True

    def read(self, oglObjects, umlFrame):
        """
        Read data from filename.

        Args:
            oglObjects:
            umlFrame: Pyut's UmlFrame

        Returns: True if succeeded, False if error or canceled
        """
        # Ask the user which destination file he wants
        filename = self._askForFileImport()
        if filename == "":
            return False

        # Open file
        from org.pyut.ui.Mediator import Mediator

        mediator: Mediator = Mediator()

        fileHandling = mediator.getFileHandling()
        project = fileHandling.getCurrentProject()
        for document in project.getDocuments():
            project.removeDocument(document, False)
        fileHandling.openFile(filename, project)
