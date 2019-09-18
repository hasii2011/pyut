
from wx import ID_NO
from wx import YES_NO

from wx import MessageDialog
from wx import TreeItemData
from wx import BeginBusyCursor
from wx import EndBusyCursor

from pyutUtils import displayError
from PyutDocument import PyutDocument
from globals import _


def shorterFilename(filename):
    """
    Return a shorter filename to display

    @param filename file name to display
    @return String better file name
    @since 1.0
    @author C.Dutoit <dutoitc@hotmail.com>
    """
    import os
    return os.path.split(filename)[1]


DefaultFilename = _("Untitled.put")


class PyutProject:
    """
    Project : contain multiple documents

    :author: C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.19 $
    """

    def __init__(self, filename, parentFrame, tree, treeroot):
        """
        Constructor

        @author C.Dutoit
        """
        import mediator
        self._parentFrame = parentFrame # Parent frame
        self._ctrl = mediator.getMediator()
        self._documents = []       # List of documents
        self._filename = filename  # Project filename
        self._modified = False     # Was the project modified ?
        self._treeRootParent = treeroot  # Parent of the project root entry
        self._tree     = tree      # Tree i'm belonging to
        self._treeRoot = None      # Root of the project entry in the tree
        self._codePath = ""
        self.addToTree()

    def setFilename(self, filename):
        """
        Get the project's filename

        @author C.Dutoit
        @return String : The project filename
        """
        self._filename = filename
        self.updateTreeText()

    def getFilename(self):
        """
        Get the project's filename

        @author C.Dutoit
        @return String : The project filename
        """
        return self._filename

    def getCodePath(self):
        """
        Get the root path where the corresponding code relies.

        @return string
        """
        return self._codePath

    def setCodePath(self, codepath):
        """
        Set the root path where the corresponding code relies.

        @param codepath
        """
        self._codePath = codepath

    def getDocuments(self):
        """
        Return the documents

        @author C.Dutoit
        """
        return self._documents

    def setModified(self, value = True):
        """
        Define the modified attribute

        @author C.Dutoit
        """
        self._modified = value

    def getModified(self):
        """
        Return the modified attribute

        @author C.Dutoit
        """
        return self._modified

    def addToTree(self):
        # Add the project to the project tree
        # self._treeRoot = self._tree.AppendItem(self._treeRootParent, shorterFilename(self._filename), data=TreeItemData(self))
        self._treeRoot = self._tree.AppendItem(self._treeRootParent, shorterFilename(self._filename), data=self)
        self._tree.Expand(self._treeRoot)

        # Add the frames
        for document in self._documents:
            document.addToTree(self, self._tree, self._treeRoot)

    def removeFromTree(self):
        """
        Remove the project from the tree

        @author C.Dutoit
        """
        self._tree.Delete(self._treeRoot)

    def loadFromFilename(self, filename):
        """
        Load a project from a file

        @author C.Dutoit
        @param String filename : filename to open
        @return boolean: True if succeeded
        """
        # Load the file
        import IoFile
        BeginBusyCursor()
        io = IoFile.IoFile()
        #wx.Yield() # to treat the umlframe refresh in newDiagram before loading

        #Load the file
        self._filename = filename
        try:
            io.open(filename, self)
            self._modified = False
        except (ValueError, Exception) as e:
            EndBusyCursor()
            displayError(_(f"Error loading file: {e}"))
            return False
        # print ">>>PyutProject-loadFromFilename-5"
        EndBusyCursor()
        # print ">>>PyutProject-loadFromFilename-6"
        # Update text
        self.updateTreeText()

        # Register to mediator
        # if len(self._documents)>0:
        # self._ctrl.registerUMLFrame(self._documents[0].getFrame())
        # print ">>>PyutProject-loadFromFilename-7"
        if len(self._documents)>0:
            self._ctrl.getFileHandling().showFrame(self._documents[0].getFrame())
            # print ">>>PyutProject-loadFromFilename-8"
            self._documents[0].getFrame().Refresh()
            # print ">>>PyutProject-loadFromFilename-9"
            return True
        else:
            return False

    def insertProject(self, filename):
        """
        Insert another project into this one

        @author C.Dutoit
        @param String filename : filename to open
        @return boolean: True if succeeded
        """
        # Load the file
        import IoFile
        BeginBusyCursor()
        io = IoFile.IoFile()

        try:
            io.open(filename, self)
            self._modified = False
        except (ValueError, Exception) as e:
            displayError(_(f"Error loading file {e}"))
            EndBusyCursor()
            return False
        EndBusyCursor()

        # Update text
        self.updateTreeText()

        # Register to mediator
        if len(self._documents)>0:
            frame = self._documents[0].getFrame()
            self._ctrl.getFileHandling().registerUmlFrame(frame)

        # Return
        return True

    def newDocument(self, type):
        """
        Create a new document

        @author C.Dutoit
        @param type : Type of document; one cited in PyutConsts.py
        @return the newly created PyutDocument
        """
        document = PyutDocument(self._parentFrame, self, type)
        self._documents.append(document)
        document.addToTree(self._tree, self._treeRoot)
        frame = document.getFrame()
        self._ctrl.getFileHandling().registerUmlFrame(frame)
        return document

    def getFrames(self):
        """
        Get all the project's frames

        @author C.Dutoit
        @return List of frames
        """

        return [document.getFrame() for document in self._documents]

    def saveXmlPyut(self):
        """
        save the project

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import IoFile
        io = IoFile.IoFile()
        BeginBusyCursor()
        try:
             #io.save(self._filename, self._ctrl.getUmlObjects(), \
              #   self._documents[0].getFrame())
            io.save(self)
            self._modified = False

            self.updateTreeText()
        except (ValueError, Exception) as e:
            displayError(_(f"An error occured while saving project {e}"))
        EndBusyCursor()

    def updateTreeText(self):
        """
        Update the tree text for this document

        @author C.Dutoit
        """
        self._tree.SetItemText(self._treeRoot, shorterFilename(self._filename))
        for document in self._documents:
            document.updateTreeText()

    def removeDocument(self, document, confirmation=True):
        """
        Remove a given document from the project.

        Args:
            document: PyutDocument to remove from this project
            confirmation:
        """

        # Get frame
        frame = document.getFrame()

        # Confirmation
        # self._ctrl.registerUMLFrame(frame)
        if confirmation:
            self._ctrl.getFileHandling().showFrame(frame)
            dlg = MessageDialog(self._parentFrame, _("Are you sure to remove the document ?"), _("Remove a document from a project"), YES_NO)
            if dlg.ShowModal() == ID_NO:
                dlg.Destroy()
                return
            dlg.Destroy()

        # Remove references
        import mediator
        ctrl = mediator.getMediator()
        fileHandling = ctrl.getFileHandling()
        fileHandling.removeAllReferencesToUmlFrame(frame)

        # Remove frame
        # frame.Close()  # DONE by fileHandling.removeAllRef...
        # self._ctrl.registerUMLFrame(None)

        # Remove from tree
        document.removeFromTree()

        # Remove document from documents list
        self._documents.remove(document)
