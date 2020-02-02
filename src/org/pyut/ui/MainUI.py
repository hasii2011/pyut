from typing import List
from typing import TypeVar
from typing import cast

from logging import Logger
from logging import getLogger

from os import path as osPath

from wx import CommandEvent
from wx import EVT_MENU
from wx import EVT_TREE_ITEM_RIGHT_CLICK
from wx import FD_SAVE
from wx import FD_OVERWRITE_PROMPT
from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import EVT_TREE_SEL_CHANGED
from wx import ID_ANY
from wx import ID_OK
from wx import ID_YES
from wx import ITEM_NORMAL
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
from wx import Menu

from org.pyut.ui.PyutDocument import PyutDocument
from org.pyut.ui.PyutProject import PyutProject

from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutConstants import PyutConstants

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.general.Globals import _

TreeDataType = TypeVar('TreeDataType', PyutProject, UmlDiagramsFrame)
DialogType   = TypeVar('DialogType', FileDialog, MessageDialog)


class MainUI:
    """
    The main portion of the User Interface.
    Used by the main application frame (AppFrame) to host all UML frames,
    the notebook and the project tree.

    Handles the the project files, projects, documents and
    their relationship to the various UI Tree elements and the
    notebook tabs in the UI

    All actions called from AppFrame are executed on the current frame
    """
    MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12

    def __init__(self, parent, mediator):
        """

        Args:
            parent:
            mediator:
        """
        self.logger: Logger = getLogger(__name__)

        self.__parent = parent
        self._ctrl    = mediator
        self._projects:       List[PyutProject] = []
        self._currentProject: PyutProject       = cast(PyutProject, None)
        self._currentFrame:   UmlDiagramsFrame  = cast(UmlDiagramsFrame, None)

        if not self._ctrl.isInScriptMode():

            self.__splitter:        SplitterWindow = cast(SplitterWindow, None)
            self.__projectTree:     TreeCtrl       = cast(TreeCtrl, None)
            self.__projectTreeRoot: TreeItemId     = cast(TreeItemId, None)
            self.__notebook:        Notebook       = cast(Notebook, None)
            self._initializeUIElements()

    def registerUmlFrame(self, frame):
        """
        Register the current UML Frame

        Args:
            frame:
        """
        self._currentFrame = frame
        self._currentProject = self.getProjectFromFrame(frame)

    def showFrame(self, frame):
        self._frame = frame
        frame.Show()

    def getProjects(self):
        """

        Returns:
            Return all projects
        """
        return self._projects

    def isProjectLoaded(self, filename) -> bool:
        """

        Args:
            filename:

        Returns:
            `True` if the project is already loaded
        """
        for project in self._projects:
            if project.getFilename == filename:
                return True
        return False

    def isDefaultFilename(self, filename: str) -> bool:
        """

        Args:
            filename:

        Returns:
            `True` if the filename is the default filename
        """
        return filename == PyutConstants.DefaultFilename

    def openFile(self, filename, project=None) -> bool:
        """
        Open a file

        Args:
            filename:
            project:

        Returns:
            `True` if operation succeeded
        """
        # Exit if the file is already loaded
        if not self.isDefaultFilename(filename) and self.isProjectLoaded(filename):
            PyutUtils.displayError(_("The selected file is already loaded !"))
            return False

        # Create a new project ?
        if project is None:
            project = PyutProject(PyutConstants.DefaultFilename, self.__notebook, self.__projectTree, self.__projectTreeRoot)

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
            if not self._ctrl.isInScriptMode():
                for document in project.getDocuments():
                    diagramTitle: str = document.getFullyQualifiedName()
                    shortName: str = self.shortenNotebookPageFileName(diagramTitle)
                    self.__notebook.AddPage(document.getFrame(), shortName)

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

        Args:
            filename: filename of the project to insert

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
                    self.__notebook.AddPage(document.getFrame(), document.getFullyQualifiedName())

                self.__notebookCurrentPage = self.__notebook.GetPageCount()-1
                self.__notebook.SetSelection(self.__notebookCurrentPage)
            except (ValueError, Exception) as e:
                PyutUtils.displayError(_(f"An error occurred while adding the project to the notebook {e}"))
                return False

        # Select first frame as current frame
        if len(project.getDocuments()) > nbInitialDocuments:
            self._frame = project.getDocuments()[nbInitialDocuments].getFrame()

    def saveFile(self) -> bool:
        """
        save to the current filename

        Returns:
            `True` if the save suceeds else `False`
        """
        currentProject = self._currentProject
        if currentProject is None:
            PyutUtils.displayError(_("No diagram to save !"), _("Error"))
            return False

        if currentProject.getFilename() is None or currentProject.getFilename() == PyutConstants.DefaultFilename:
            return self.saveFileAs()
        else:
            return currentProject.saveXmlPyut()

    def saveFileAs(self):
        """
        Ask for a filename and save the diagram data

        Returns:
            `True` if the save suceeds else `False`
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
                    self.__notebook.SetPageText(i, document.getFullyQualifiedName())
            else:
                self.logger.info("Not updating notebook in FileHandling")

        self.__parent.updateCurrentDir(dlg.GetPath())

        project.setModified(False)
        dlg.Destroy()
        return True

    def newProject(self):
        """
        Begin a new project
        """
        project = PyutProject(PyutConstants.DefaultFilename, self.__notebook, self.__projectTree, self.__projectTreeRoot)
        self._projects.append(project)
        self._currentProject = project
        self._currentFrame = None

    def newDocument(self, docType: DiagramType):
        """
        Begin a new document

        Args:
            docType:  Type of document
        """
        project = self._currentProject
        if project is None:
            self.newProject()
            project = self.getCurrentProject()
        frame = project.newDocument(docType).getFrame()
        self._currentFrame  = frame
        self._currentProject = project

        if not self._ctrl.isInScriptMode():
            shortName: str = self.shortenNotebookPageFileName(project.getFilename())
            self.__notebook.AddPage(frame, shortName)
            self.notebookCurrentPage  = self.__notebook.GetPageCount() - 1
            # self.notebook.SetSelection(self.__notebookCurrentPage)  # maybe __notebook ?  -- hasii

    # noinspection PyUnusedLocal
    def exportToImageFile(self, extension, imageType):
        """
        Export the current diagram to an image file

        Args:
            extension:
            imageType:
        """
        # Exit if in scripting mode
        if self._ctrl.isInScriptMode():
            PyutUtils.displayError(_("Export to image file is not implemented in scripting mode now !"))
            return

    # noinspection PyUnusedLocal
    def exportToBmp(self, event):
        """
        Export the current diagram to bitmap

        Args:
            event:
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

        Args:
            event:

        """
        self.exportToImageFile("jpg", BITMAP_TYPE_JPEG)

    # noinspection PyUnusedLocal
    def exportToPng(self, event):
        """
        Export the current diagram to a png file

        Args:
            event:
        """
        self.exportToImageFile("png", BITMAP_TYPE_PNG)

    # noinspection PyUnusedLocal
    def exportToPostscript(self, event):
        """
        Export the current diagram to postscript

        Args:
            event:
        """
        dlg = MessageDialog(self.__parent, _("Not yet implemented !"), _("Sorry..."), OK | ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()
        return

    def getCurrentFrame(self):
        """

        Returns:
            Get the current frame
        """
        return self._currentFrame

    def getCurrentProject(self) -> PyutProject:
        """
        Get the current working project

        Returns:
            the current project or None if not found
        """
        return self._currentProject

    def getProjectFromFrame(self, frame: UmlDiagramsFrame) -> PyutProject:
        """
        Return the project that owns a given frame

        Args:
            frame:  the frame to get This project

        Returns:
            PyutProject or None if not found
        """
        for project in self._projects:
            if frame in project.getFrames():
                return project
        return cast(PyutProject, None)

    def getCurrentDocument(self) -> PyutDocument:
        """
        Get the current document.

        Returns:
            the current document or None if not found
        """
        project = self.getCurrentProject()
        if project is None:
            return cast(PyutDocument, None)
        for document in project.getDocuments():
            if document.getFrame() is self._currentFrame:
                return document
        return cast(PyutDocument, None)

    def onClose(self) -> bool:
        """
        Close all files

        Returns:
            True if everything is ok
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

    def setModified(self, theNewValue: bool = True):
        """
        Set the Modified flag of the currently opened diagram

        Args:
            theNewValue:

        """
        if self._currentProject is not None:
            self._currentProject.setModified(theNewValue)
        self._ctrl.updateTitle()

    def closeCurrentProject(self):
        """
        Close the current project

        Returns:
            True if everything is ok
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

        Args:
            umlFrame:

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

    def getProjectFromOglObjects(self, oglObjects) -> PyutProject:
        """
        Get a project that owns oglObjects

        Args:
            oglObjects: Objects to find their parents

        Returns:
            PyutProject if found, None else
        """
        for project in self._projects:
            for frame in project.getFrames():
                diagram = frame.getDiagram()
                shapes = diagram.GetShapes()
                for obj in oglObjects:
                    if obj in shapes:
                        return project

        return cast(PyutProject, None)

    def _initializeUIElements(self):
        """
        Instantiate all the UI elements
        """
        self.__splitter        = SplitterWindow(self.__parent, ID_ANY)
        self.__projectTree     = TreeCtrl(self.__splitter, ID_ANY, style=TR_HIDE_ROOT + TR_HAS_BUTTONS)
        self.__projectTreeRoot = self.__projectTree.AddRoot(_("Root"))

        #  self.__projectTree.SetPyData(self.__projectTreeRoot, None)
        # Expand root, since wx.TR_HIDE_ROOT is not supported under winx
        # Not supported for hidden tree since wx.Python 2.3.3.1 ?
        #  self.__projectTree.Expand(self.__projectTreeRoot)

        # diagram container
        self.__notebook = Notebook(self.__splitter, ID_ANY, style=CLIP_CHILDREN)

        # Set splitter
        self.__splitter.SetMinimumPaneSize(20)
        self.__splitter.SplitVertically(self.__projectTree, self.__notebook, 160)

        self.__notebookCurrentPage = -1

        # Callbacks
        self.__parent.Bind(EVT_NOTEBOOK_PAGE_CHANGED,      self.__onNotebookPageChanged)
        self.__parent.Bind(EVT_TREE_SEL_CHANGED,           self.__onProjectTreeSelChanged)
        self.__projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK, self.__onProjectTreeRightClick)

    # noinspection PyUnusedLocal
    def __onNotebookPageChanged(self, event):
        """
        Callback for notebook page changed

        Args:
            event:
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

        Args:
            event:
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

        Returns:
        """
        # Return None if we are in scripting mode
        if self._ctrl.isInScriptMode():
            return None

        noPage = self.__notebookCurrentPage
        if noPage == -1:
            return None
        frame = self.__notebook.GetPage(noPage)
        return frame

    def __onProjectTreeRightClick(self, treeEvent: TreeEvent):

        itemId: TreeItemId = treeEvent.GetItem()
        data = self.__projectTree.GetItemData(item=itemId)
        self.logger.info(f'Item Data: {data}  currentProject: {self._currentProject.getFilename()}')
        if isinstance(data, PyutProject):
            self.__popupProjectMenu()

    def __popupProjectMenu(self):

        [closeProjectMenuID] = PyutUtils.assignID(1)
        popupMenu: Menu = Menu('Actions')
        popupMenu.AppendSeparator()
        popupMenu.Append(closeProjectMenuID, 'Close Project', 'Remove project from tree', ITEM_NORMAL)
        popupMenu.Bind(EVT_MENU, self.__onCloseProject, id=closeProjectMenuID)
        self.__parent.PopupMenu(popupMenu)

    # noinspection PyUnusedLocal
    def __onCloseProject(self, event: CommandEvent):
        self.logger.info(f'I have arrived')
        self.closeCurrentProject()

    def shortenNotebookPageFileName(self, filename: str) -> str:
        """
        Return a shorter filename to display; For file names longer
        than `MAX_NOTEBOOK_PAGE_NAME_LENGTH` this method takes the first
        four characters and the last eight as the shortened file name

        Args:
            filename:  The file name to display

        Returns:
            A better file name
        """
        justFileName: str = osPath.split(filename)[1]
        if len(justFileName) > MainUI.MAX_NOTEBOOK_PAGE_NAME_LENGTH:
            firstFour: str = justFileName[:4]
            lastEight: str = justFileName[-8:]
            return f'{firstFour}{lastEight}'
        else:
            return justFileName
