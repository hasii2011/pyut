
from typing import TypeVar
from typing import cast

from logging import Logger
from logging import getLogger

from wx import FD_SAVE
from wx import FD_OVERWRITE_PROMPT
from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import EVT_TREE_SEL_CHANGED
from wx import ID_OK
from wx import ID_YES
from wx import OK
from wx import YES_NO
from wx import ICON_ERROR
from wx import ICON_QUESTION
from wx import TR_HIDE_ROOT
from wx import TR_HAS_BUTTONS
from wx import CLIP_CHILDREN
from wx import BITMAP_TYPE_BMP
from wx import BITMAP_TYPE_JPEG
from wx import BITMAP_TYPE_PNG

from wx import TreeEvent
from wx import TreeItemId
from wx import FileDialog
from wx import SplitterWindow
from wx import TreeCtrl
from wx import Notebook
from wx import MessageDialog
from wx import Yield

from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.PyutUtils import PyutUtils

from org.pyut.PyutConstants import DefaultFilename
from PyutProject import PyutProject

from org.pyut.general.Globals import _

TreeDataType = TypeVar('TreeDataType', PyutProject, UmlDiagramsFrame)
DialogType   = TypeVar('DialogType', FileDialog, MessageDialog)


def shorterFilename(filename):
    """
    Return a shorter filename to display

    @param filename file name to display
    @return String better file name
    @since 1.0
    @author C.Dutoit <dutoitc@hotmail.com>

    TODO Make this part of the class
    """
    import os
    aString = os.path.split(filename)[1]
    if len(aString) > 12:
        return aString[:4] + aString[-8:]
    else:
        return aString


class FileHandling:
    """
    FileHandling : Handle files in Pyut
    Used by AppFrame to contain all UML frames, the notebook and
    the project tree.

    All actions called from AppFrame are executing on the current frame

    :author: C.Dutoit
    :contact: <dutoitc@hotmail.com>
    :version: $Revision: 1.35 $
    """
    def __init__(self, parent, mediator):
        """
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self.logger: Logger = getLogger(__name__)

        self._projects = []
        self.__parent = parent
        self._ctrl = mediator
        self._currentProject: PyutProject      = cast(PyutProject, None)
        self._currentFrame:   UmlDiagramsFrame = cast(UmlDiagramsFrame, None)

        # Init graphic
        if not self._ctrl.isInScriptMode():
            self._initGraphicalElements()

    def registerUmlFrame(self, frame):
        """
        Register the current UML Frame
        """
        self._currentFrame = frame
        self._currentProject = self.getProjectFromFrame(frame)

    def _initGraphicalElements(self):
        """
        Define all graphical elements
        @author C.Dutoit
        """
        # window splitting
        self.__splitter: SplitterWindow = SplitterWindow(self.__parent, -1)

        # project tree
        self.__projectTree: TreeCtrl = TreeCtrl(self.__splitter, -1, style=TR_HIDE_ROOT + TR_HAS_BUTTONS)
        self.__projectTreeRoot       = self.__projectTree.AddRoot(_("Root"))

        #  self.__projectTree.SetPyData(self.__projectTreeRoot, None)
        # Expand root, since wx.TR_HIDE_ROOT is not supported under winx
        # Not supported for hidden tree since wx.Python 2.3.3.1 ?
        #  self.__projectTree.Expand(self.__projectTreeRoot)

        # diagram container
        self.__notebook = Notebook(self.__splitter, -1, style=CLIP_CHILDREN)

        # Set splitter
        self.__splitter.SetMinimumPaneSize(20)
        #  self.__splitter.SplitVertically(self.__projectTree, self.__notebook)
        #  self.__splitter.SetSashPosition(100)
        self.__splitter.SplitVertically(self.__projectTree, self.__notebook, 160)

        #  ...
        self.__notebookCurrentPage = -1

        # Callbacks
        self.__parent.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self.__onNotebookPageChanged)
        self.__parent.Bind(EVT_TREE_SEL_CHANGED,  self.__onProjectTreeSelChanged)

    def showFrame(self, frame):
        self._frame = frame
        frame.Show()

    def getProjects(self):
        """
        Return all projects

        @return PyutProject[] the projects
        @author C.Dutoit
        """
        return self._projects

    def isProjectLoaded(self, filename):
        """
        Return True if the project is already loaded
        @author C.Dutoit
        """
        for project in self._projects:
            if project.getFilename == filename:
                return True
        return False

    def isDefaultFilename(self, filename):
        """
        Return True if the filename is the default filename
        """
        return filename == DefaultFilename

    def openFile(self, filename, project=None):
        """
        Open a file

        Args:
            filename:
            project:

        Returns: True if succeeded

        """

        # Exit if the file is already loaded
        if not self.isDefaultFilename(filename) and self.isProjectLoaded(filename):
            PyutUtils.displayError(_("The selected file is already loaded !"))
            return False

        # Create a new project ?
        if project is None:
            project = PyutProject(DefaultFilename, self.__notebook, self.__projectTree, self.__projectTreeRoot)

        #  print ">>>FileHandling-openFile-3"
        # Load the project and add it
        try:
            if not project.loadFromFilename(filename):
                PyutUtils.displayError(_("The specified file can't be loaded !"))
                return False
            self._projects.append(project)
            #  self._ctrl.registerCurrentProject(project)
            self._currentProject = project
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_(f"An error occurred while loading the project ! {e}"))
            return False

        try:
            for document in project.getDocuments():
                if not self._ctrl.isInScriptMode():
                    self.__notebook.AddPage(document.getFrame(), document.getDiagramTitle())

            if not self._ctrl.isInScriptMode():
                self.__notebookCurrentPage = self.__notebook.GetPageCount()-1
                self.__notebook.SetSelection(self.__notebookCurrentPage)
            if len(project.getDocuments()) > 0:
                self._currentFrame = project.getDocuments()[0].getFrame()

        except (ValueError, Exception) as e:
            PyutUtils.displayError(_(f"An error occurred while adding the project to the notebook {e}"))
            return False
        return True

    def insertFile(self, filename):
        """
        Insert a file in the current project

        @param filename : filename of the project to insert
        @author C.Dutoit
        """
        # Get current project
        project = self._currentProject

        # Save number of initial documents
        nbInitialDocuments = len(project.getDocuments())

        # Load data...
        if not project.insertProject(filename):
            PyutUtils.displayError(_("The specified file can't be loaded !"))
            return False

        # ...
        if not self._ctrl.isInScriptMode():
            try:
                for document in project.getDocuments()[nbInitialDocuments:]:
                    self.__notebook.AddPage(document.getFrame(), document.getDiagramTitle())

                self.__notebookCurrentPage = self.__notebook.GetPageCount()-1
                self.__notebook.SetSelection(self.__notebookCurrentPage)
            except (ValueError, Exception) as e:
                PyutUtils.displayError(_(f"An error occurred while adding the project to the notebook {e}"))
                return False

        # Select first frame as current frame
        if len(project.getDocuments()) > nbInitialDocuments:
            self._frame = project.getDocuments()[nbInitialDocuments].getFrame()

    def saveFile(self):
        """
        save to the current filename

        @return bool True if succeeded
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        currentProject = self._currentProject
        if currentProject is None:
            PyutUtils.displayError(_("No diagram to save !"), _("Error"))
            return

        if currentProject.getFilename() is None or currentProject.getFilename() == DefaultFilename:
            return self.saveFileAs()
        else:
            return currentProject.saveXmlPyut()

    def saveFileAs(self):
        """
        Ask for a filename and save datas to it.

        @return bool True if succeeded
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if self._ctrl.isInScriptMode():
            PyutUtils.displayError(_("Save File As is not accessible in script mode !"))
            return

        # Test if no diagram exists
        if self._ctrl.getDiagram() is None:
            PyutUtils.displayError(_("No diagram to save !"), _("Error"))
            return

        # Ask for filename
        filenameOK = False
        # TODO revisit this to figure out how to get rid of Pycharm warning 'dlg referenced before assignment'
        # Bad thing is dlg can be either a FileDialog or a MessageDialog
        dlg: DialogType = cast(DialogType, None)
        while not filenameOK:
            dlg = FileDialog(self.__parent,
                             defaultDir=self.__parent.getCurrentDir(),
                             wildcard=_("Pyut file (*.put)|*.put"),
                             style=FD_SAVE | FD_OVERWRITE_PROMPT)

            # Return False if canceled
            if dlg.ShowModal() != ID_OK:
                dlg.Destroy()
                return False

            # Find if a specified filename is already opened
            filename = dlg.GetPath()

            if len([project for project in self._projects if project.getFilename() == filename]) > 0:
                dlg = MessageDialog(self.__parent,
                                    _("Error ! The filename '%s" + "' correspond to a project which is currently opened !" +
                                      " Please choose another filename !") % str(filename),
                                    _("Save change, filename error"), OK | ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                return
            filenameOK = True

        project = self._currentProject
        project.setFilename(dlg.GetPath())
        project.saveXmlPyut()

        # Modify notebook text
        for i in range(self.__notebook.GetPageCount()):
            frame = self.__notebook.GetPage(i)
            document = [document for document in project.getDocuments() if document.getFrame() is frame]
            if len(document) > 0:
                document = document[0]
                if frame in project.getFrames():
                    self.__notebook.SetPageText(i, document.getDiagramTitle())
            else:
                self.logger.info("Not updating notebook in FileHandling")

        self.__parent.updateCurrentDir(dlg.GetPath())

        project.setModified(False)
        dlg.Destroy()
        return True

    def newProject(self):
        """
        Begin a new project

        @author C.Dutoit
        """
        project = PyutProject(DefaultFilename, self.__notebook, self.__projectTree, self.__projectTreeRoot)
        self._projects.append(project)
        self._currentProject = project
        self._currentFrame = None

    def newDocument(self, docType):
        """
        Begin a new document

        Args:
            docType:  Type of document; one cited in PyutConsts.py

        @author C.Dutoit
        """
        project = self._currentProject
        if project is None:
            self.newProject()
            project = self.getCurrentProject()
        frame = project.newDocument(docType).getFrame()
        self._currentFrame  = frame
        self._currentProject = project

        if not self._ctrl.isInScriptMode():
            self.__notebook.AddPage(frame, shorterFilename(project.getFilename()))
            self.notebookCurrentPage  = self.__notebook.GetPageCount() - 1
            # self.notebook.SetSelection(self.__notebookCurrentPage)  # maybe __notebook ?  -- hasii

    # noinspection PyUnusedLocal
    def exportToImageFile(self, extension, imageType):
        """
        Export the current diagram to an image file
        @author C.Dutoit
        """
        # Exit if in scripting mode
        if self._ctrl.isInScriptMode():
            PyutUtils.displayError(_("Export to image file is not implemented in scripting mode now !"))
            return

    # noinspection PyUnusedLocal
    def exportToBmp(self, event):
        """
        Export the current diagram to bitmap

        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Exit if in scripting mode
        if self._ctrl.isInScriptMode():
            PyutUtils.displayError(_("Export to bitmap file is not implemented in scripting mode now !"))
            return

        self.exportToImageFile("bmp", BITMAP_TYPE_BMP)

    # noinspection PyUnusedLocal
    def exportToJpg(self, event):
        """
        Export the current diagram to a jpeg file

        @author C.Dutoit
        """
        self.exportToImageFile("jpg", BITMAP_TYPE_JPEG)

    # noinspection PyUnusedLocal
    def exportToPng(self, event):
        """
        Export the current diagram to a png file

        @author C.Dutoit
        """
        self.exportToImageFile("png", BITMAP_TYPE_PNG)

    # noinspection PyUnusedLocal
    def exportToPostscript(self, event):
        """
        Export the current diagram to postscript

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        dlg = MessageDialog(self.__parent, _("Not yet implemented !"), _("Sorry..."), OK | ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()
        return

    # noinspection PyUnusedLocal
    def __onNotebookPageChanged(self, event):
        """
        Callback for notebook page changed

        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.0
        """
        self.__notebookCurrentPage = self.__notebook.GetSelection()
        if self._ctrl is not None:      # hasii maybe I got this right from the old pre PEP-8 code
            #  self._ctrl.registerUMLFrame(self._getCurrentFrame())
            self._currentFrame = self._getCurrentFrameFromNotebook()
            self.__parent.notifyTitleChanged()
        # self.__projectTree.SelectItem(getID(self.getCurrentFrame()))
        # TODO : how can I do getID ???

        # Register the current project
        self._currentProject = self.getProjectFromFrame(self._currentFrame)

    def __onProjectTreeSelChanged(self, event: TreeEvent):
        """
        Callback for notebook page changed

        @author C.Dutoit
        """
        itm: TreeItemId = event.GetItem()
        pyutData: TreeDataType = self.__projectTree.GetItemData(itm)
        self.logger.info(f'Clicked on: `{pyutData}`')
        # Use our own base type
        if isinstance(pyutData, UmlDiagramsFrame):
            frame: UmlDiagramsFrame = pyutData
            self._currentFrame = frame
            self._currentProject = self.getProjectFromFrame(frame)

            # Select the frame in the notebook
            for i in range(self.__notebook.GetPageCount()):
                pageFrame = self.__notebook.GetPage(i)
                if pageFrame is frame:
                    self.__notebook.SetSelection(i)
                    return
        elif isinstance(pyutData, PyutProject):
            self._currentProject = pyutData

    def _getCurrentFrameFromNotebook(self):
        """
        Get the current frame in the notebook

        @return frame Current frame in the notebook; -1 if none selected
        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.0
        """
        # Return None if we are in scripting mode
        if self._ctrl.isInScriptMode():
            return None

        noPage = self.__notebookCurrentPage
        if noPage == -1:
            return None
        frame = self.__notebook.GetPage(noPage)
        return frame

    def getCurrentFrame(self):
        """
        Get the current frame
        @author C.Dutoit
        """
        return self._currentFrame

    def getCurrentProject(self):
        """
        Get the current working project

        @return Project : the current project or None if not found
        @author C.Dutoit
        """
        return self._currentProject

    def getProjectFromFrame(self, frame: UmlDiagramsFrame):
        """
        Return the project that owns a given frame

        @param wx.Frame frame : the frame to get his project
        @return PyutProject or None if not found
        @author C.Dutoit
        """
        for project in self._projects:
            if frame in project.getFrames():
                return project
        return None

    def getCurrentDocument(self):
        """
        Get the current document.

        @return PyutDocument : the current document or None if not found
        @author C.Dutoit
        """
        project = self.getCurrentProject()
        if project is None:
            return None
        for document in project.getDocuments():
            if document.getFrame() is self._currentFrame:
                return document
        return None

    def onClose(self):
        """
        Close all files

        @return True if everything's ok
        @author C.Dutoit
        """
        # Display warning if we are in scripting mode
        if self._ctrl.isInScriptMode():
            print("WARNING : in script mode, the non-saved projects are closed without warning")

        # Close projects and ask for unsaved but modified projects
        if not self._ctrl.isInScriptMode():
            for project in self._projects:
                if project.getModified() is True:
                    frames = project.getFrames()
                    if len(frames) > 0:
                        frame = frames[0]
                        frame.SetFocus()
                        Yield()
                        # if self._ctrl is not None:
                            # self._ctrl.registerUMLFrame(frame)
                        self.showFrame(frame)
                    dlg = MessageDialog(self.__parent,
                                        _("Your diagram has not been saved! Would you like to save it ?"),
                                        _("Save changes ?"), YES_NO | ICON_QUESTION)
                    if dlg.ShowModal() == ID_YES:
                        # save
                        if self.saveFile() is False:
                            return False
                    dlg.Destroy()

        # dereference all
        self.__parent = None
        self._ctrl = None
        self.__splitter = None
        self.__projectTree = None
        self.__notebook.DeleteAllPages()
        self.__notebook = None
        self.__splitter = None
        self._projects = None
        self._currentProject = None
        self._currentFrame = None

    def setModified(self, flag=True):
        """
        Set the Modified flag of the currently opened diagram

        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if self._currentProject is not None:
            self._currentProject.setModified(flag)
        self._ctrl.updateTitle()

    def closeCurrentProject(self):
        """
        Close the current project

        @return True if everything's ok
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # No frame left ?
        if self._currentProject is None and self._currentFrame is not None:
            self._currentProject = self.getProjectFromFrame(self._currentFrame)
        if self._currentProject is None:
            PyutUtils.displayError(_("No frame to close !"), _("Error..."))
            return

        # Display warning if we are in scripting mode
        if self._ctrl.isInScriptMode():
            print("WARNING : in script mode, the non-saved projects are closed without warning")

        # Close the file
        if self._currentProject.getModified() is True and not self._ctrl.isInScriptMode():
            # Ask to save the file
            frame = self._currentProject.getFrames()[0]
            frame.SetFocus()
            # self._ctrl.registerUMLFrame(frame)
            self.showFrame(frame)

            dlg = MessageDialog(self.__parent, _("Your project has not been saved. " 
                                                 "Would you like to save it ?"), _("Save changes ?"), YES_NO | ICON_QUESTION)
            if dlg.ShowModal() == ID_YES:
                if self.saveFile() is False:
                    return False

        # Remove the frame in the notebook
        if not self._ctrl.isInScriptMode():
            # Python 3 update
            pages = list(range(self.__notebook.GetPageCount()))
            pages.reverse()
            for i in pages:
                pageFrame = self.__notebook.GetPage(i)
                if pageFrame in self._currentProject.getFrames():
                    self.__notebook.DeletePage(i)
                    # RemovePage si erreur ??

        self._currentProject.removeFromTree()
        self._projects.remove(self._currentProject)
        #  del project

        self._currentProject = None
        self._currentFrame = None

    def removeAllReferencesToUmlFrame(self, umlFrame):
        """
        Remove all my references to a given uml frame

        @author C.Dutoit
        """
        # Current frame ?
        if self._currentFrame is umlFrame:
            self._currentFrame = None

        # Exit if we are in scripting mode
        if self._ctrl.isInScriptMode():
            return

        for i in range(self.__notebook.GetPageCount()):
            pageFrame = self.__notebook.GetPage(i)
            if pageFrame is umlFrame:
                self.__notebook.DeletePage(i)
                break

    def getProjectFromOglObjects(self, oglObjects):
        """
        Get a project that owns oglObjects

        @param oglObjects Objects to find their parents
        @return PyutProject if found, None else
        @author C.Dutoit
        """
        for project in self._projects:
            for frame in project.getFrames():
                diagram = frame.getDiagram()
                shapes = diagram.GetShapes()
                for obj in oglObjects:
                    if obj in shapes:
                        return project
        return None
