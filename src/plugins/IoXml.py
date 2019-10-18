
from os import getcwd
from os import chdir

from glob import glob

from io import StringIO

from wx import CANCEL
from wx import CENTRE
from wx import ICON_QUESTION
from wx import MessageBox
from wx import YES
from wx import YES_NO

from plugins.PyutIoPlugin import PyutIoPlugin

from Mediator import getMediator


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

    def write(self, oglObjects):
        """
        Write data to filename.

        Args:
            oglObjects:

        Returns: True if succeeded, False if error or canceled
        """
        oldPath = getcwd()
        # Ask the user which destination file he wants
        filename = self._askForFileExport()
        if filename == "":
            return False
        path = getMediator().getAppPath()
        chdir(path)

        candidates = glob("PyutXmlV*.py")
        numbers = [int(s[8:-3]) for s in candidates]
        lastVersion = str(max(numbers))
        print("Using version", lastVersion, " of the exporter")
        module = __import__("PyutXmlV" + lastVersion)
        myXml = module.PyutXml()
        file = open(filename, "w")

        if int(lastVersion) >= 5:   # Python 3 update
            import Mediator
            ctrl         = Mediator.getMediator()
            fileHandling = ctrl.getFileHandling()
            project      = fileHandling.getProjectFromOglObjects(oglObjects)
            doc          = myXml.save(project)
        else:
            doc = myXml.save(oglObjects)

        if self.pretty:
            text = doc.toprettyxml()
        else:
            text = doc.toxml()
        # add attribute encoding = "iso-8859-1"
        # this is not possible with minidom, so we use pattern matching
        text = text.replace(r'<?xml version="1.0" ?>', r'<?xml version="1.0" encoding="iso-8859-1"?>')

        file.write(text)
        file.close()
        chdir(oldPath)
        return True

    # noinspection PyUnusedLocal
    def readOld(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        Args:
            oglObjects:
            umlFrame:   Pyut's UmlFrame

        Returns: True if succeeded, False if error or canceled

        """
        # Note : xml.dom.minidom must be instancied here, since it redefines
        # the function '_', which is also used for i18n
        from xml.dom.minidom import parse
        oldpath = getcwd()
        path = getMediator().getAppPath()
        chdir(path)
        # Ask the user which destination file he wants
        filename = self._askForFileImport()
        if filename == "":
            return False

        dom = parse(StringIO(open(filename).read()))
        root = dom.getElementsByTagName("Pyut")[0]
        if root.hasAttribute('version'):
            version = root.getAttribute("version")
        else:
            version = 1

        if version == 1:
            from PyutXml import PyutXml
            myXml = PyutXml()
        else:
            module = __import__("PyutXmlV" + str(version))
            myXml = module.PyutXml()

        myXml.open(dom, umlFrame)
        chdir(oldpath)
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
        import Mediator
        ctrl = Mediator.getMediator()
        fileHandling = ctrl.getFileHandling()
        project = fileHandling.getCurrentProject()
        for document in project.getDocuments():
            project.removeDocument(document, False)
        fileHandling.openFile(filename, project)
