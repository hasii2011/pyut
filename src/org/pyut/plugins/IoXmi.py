
from io import StringIO

from wx import CENTRE
from wx import ICON_QUESTION
from wx import MessageBox
from wx import YES
from wx import YES_NO
from wx import CANCEL

from org.pyut.plugins.xmi.PyutXmi import PyutXmi
from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

from org.pyut.persistence.PyutXml import PyutXml

from org.pyut.general.PyutXmfFinder import PyutXmlFinder


class IoXmi(PyutIoPlugin):
    """
    To save XML file format.

    @version $Revision: 1.5 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "IoXmi"

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
        return "XMI", "xmi", "Pyut XMI file"        # typo here maybe xml --> xmi

    def getOutputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "XMI", "xmi", "Pyut XMI file"        # typo here maybe xml --> xmi

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

    def write(self, oglObjects):
        """
        Write data to filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param oglObjects : list of exported objects
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        # Ask the user which destination file he wants
        filename = self._askForFileExport()
        if filename == "":
            return False
        file = open(filename, "w")

        myXml = PyutXml()
        doc = myXml.save(oglObjects, self._umlFrame)

        if self.pretty:
            text = doc.toprettyxml()
        else:
            text = doc.toxml()

        updatedXml: str = PyutXmlFinder.setAsISOLatin(text)
        file.write(updatedXml)
        file.close()
        return True

    def read(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param oglObjects : list of imported objects
        @param umlFrame : Pyut's UmlFrame
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        from xml.dom.minidom import parse

        # Ask the user which destination file he wants
        filename = self._askForFileImport()
        if filename == "":
            return False

        dom = parse(StringIO(open(filename).read()))

        myXmi: PyutXmi = PyutXmi()
        myXmi.open(dom, umlFrame)
        return True
