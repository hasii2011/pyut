
from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import path as osPath

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import EVT_MENU
from wx import EVT_NOTEBOOK_PAGE_CHANGED
from wx import EVT_TREE_ITEM_RIGHT_CLICK
from wx import EVT_TREE_SEL_CHANGED
from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import ICON_ERROR
from wx import ICON_QUESTION
from wx import ID_ANY
from wx import ID_OK
from wx import ID_YES
from wx import YES_NO
from wx import ITEM_NORMAL
from wx import OK

from wx import SplitterWindow
from wx import Frame
from wx import TreeEvent
from wx import TreeItemId
from wx import CommandEvent
from wx import FileDialog
from wx import Menu
from wx import MessageDialog

from wx import BeginBusyCursor
from wx import EndBusyCursor

from wx import Yield as wxYield

from org.pyut.PyutConstants import PyutConstants

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.DlgEditDocument import DlgEditDocument

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.ui.IPyutDocument import IPyutDocument
from org.pyut.ui.IPyutProject import IPyutProject

from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
from org.pyut.uiv2.ProjectManager import ProjectManager
from org.pyut.uiv2.ProjectManager import PyutProjects
from org.pyut.uiv2.ProjectTree import ProjectTree
from org.pyut.uiv2.PyutDocumentV2 import PyutDocumentV2
from org.pyut.uiv2.PyutProjectV2 import PyutProjectV2
from org.pyut.uiv2.PyutProjectV2 import UmlFrameType

TreeDataType = Union[PyutProjectV2, UmlDiagramsFrame]

SASH_POSITION:                 int = 160        # TODO make this a preference and remember it
MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12         # TODO make this a preference


class PyutUIV2(SplitterWindow):

    def __init__(self, topLevelWindow: Frame):

        super().__init__(parent=topLevelWindow, id=ID_ANY)

        self.logger: Logger = getLogger(__name__)

        self._parentWindow:    Frame           = topLevelWindow
        self._projectTree:     ProjectTree     = ProjectTree(parentWindow=self)
        self._diagramNotebook: DiagramNotebook = DiagramNotebook(parentWindow=self)

        # Set splitter
        self.SetMinimumPaneSize(20)
        self.SplitVertically(self._projectTree, self._diagramNotebook, SASH_POSITION)

        self._notebookCurrentPageNumber: int                = -1

        # self._projects:                  List[IPyutProject] = []
        # self._currentProject:            IPyutProject       = cast(IPyutProject, None)

        self._currentFrame:              UmlDiagramsFrame   = cast(UmlDiagramsFrame, None)
        self._projectPopupMenu:          Menu               = cast(Menu, None)
        self._documentPopupMenu:         Menu               = cast(Menu, None)

        self._projectManager: ProjectManager = ProjectManager(projectTree=self._projectTree)

        self._parentWindow.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onDiagramNotebookPageChanged)
        self._parentWindow.Bind(EVT_TREE_SEL_CHANGED,      self._onProjectTreeSelectionChanged)
        self._projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK,  self._onProjectTreeRightClick)

    @property
    def currentProject(self) -> IPyutProject:
        return self._projectManager.currentProject

    @currentProject.setter
    def currentProject(self, newProject: IPyutProject):

        self.logger.info(f'{self._diagramNotebook.GetRowCount()=}')
        self._projectManager.currentProject = newProject

        self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount() - 1
        self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        self.logger.info(f'{self._notebookCurrentPageNumber=}')

    @property
    def currentDocument(self) -> IPyutDocument:
        """
        Get the current document.

        Returns:
            the current document or None if not found
        """
        project: IPyutProject = self._projectManager.currentProject
        if project is None:
            return cast(IPyutDocument, None)
        for document in project.documents:
            if document.diagramFrame is self._currentFrame:
                return document
        return cast(IPyutDocument, None)

    @property
    def currentFrame(self) -> UmlDiagramsFrame:
        return self._currentFrame

    @currentFrame.setter
    def currentFrame(self, newFrame: UmlDiagramsFrame):
        self._currentFrame = newFrame

    @property
    def modified(self) -> bool:
        if self._projectManager.currentProject is not None:
            return self._projectManager.currentProject.modified
        else:
            return False

    @modified.setter
    def modified(self, theNewValue: bool = True):
        """
        Set the modified flag of the currently opened project

        Args:
            theNewValue:
        """
        if self._projectManager.currentProject is not None:
            # mypy does not handle property setters
            self._projectManager.currentProject.modified = theNewValue     # type: ignore
        # self._mediator.updateTitle()      TODO Fix V2 version

    @property
    def diagramNotebook(self) -> DiagramNotebook:
        """
        This will be removed when we use eventing from the mediator to send messages

        Returns:  The UI component
        """
        return self._diagramNotebook

    def registerUmlFrame(self, frame: UmlDiagramsFrame):
        """
        Register the current UML Frame

        Args:
            frame:
        """
        self._currentFrame = frame
        self._currentProject = self.getProjectFromFrame(frame)

    def showFrame(self, frame: UmlDiagramsFrame):
        self._frame = frame
        frame.Show()

    def getProjectFromFrame(self, frame: UmlDiagramsFrame) -> IPyutProject:
        """
        Return the project that owns a given frame

        Args:
            frame:  the frame to get This project

        Returns:
            PyutProject or None if not found
        """
        # for project in self._projects:
        for project in self._projectManager.projects:
            if frame in project.getFrames():
                return project
        return cast(PyutProjectV2, None)

    def newProject(self) -> IPyutProject:
        """
        Create a new project;  Adds it to the Project Tree;
        The caller should be responsible
        for updating ._currentProject and the _projects list; but because of
        architecture problems I have to do it here;
        TODO V2 UI refactor needs to fix this

        Returns:  A default empty project
        """
        project = PyutProjectV2(PyutConstants.DEFAULT_FILENAME, self._diagramNotebook, self._projectTree, self._projectTree.projectTreeRoot)

        projectTreeRoot: TreeItemId = self._projectTree.addProjectToTree(pyutProject=project)

        project.projectTreeRoot = projectTreeRoot

        # self._projects.append(project)
        # self._currentProject = project
        self._projectManager.addProject(project)
        self._projectManager.currentProject = project

        self._currentFrame   = cast(UmlDiagramsFrame, None)

        return project

    def newDocument(self, docType: DiagramType) -> IPyutDocument:
        """
        Create a new document;  It is up to the caller to update the PyutProject document list
        It is up to the caller to add it to the notebook

        Args:
            docType:  Type of document

        Returns: The newly created document
        """
        pyutProject: IPyutProject = self._projectManager.currentProject
        if pyutProject is None:
            self.newProject()
            pyutProject = self._projectManager.currentProject

        document: PyutDocumentV2  = PyutDocumentV2(parentFrame=self._diagramNotebook, project=pyutProject, docType=docType)

        document.addToTree(self._projectTree, pyutProject.projectTreeRoot)

        self.currentFrame    = document.diagramFrame
        self._currentProject = pyutProject      # TODO do not use property it does a bunch of stuff

        wxYield()
        self._notebookCurrentPageNumber  = self._diagramNotebook.GetPageCount() - 1
        self.logger.info(f'Current notebook page: {self._notebookCurrentPageNumber}')
        # self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

        return document

    def closeCurrentProject(self):
        """
        Close the current project

        Returns:
            True if everything is ok
        """
        currentProject: IPyutProject = self._projectManager.currentProject
        if currentProject is None and self._currentFrame is not None:
            currentProject = self.getProjectFromFrame(self._currentFrame)
        if currentProject is None:
            PyutUtils.displayError("No frame to close !", "Error...")
            return False

        # Close the project
        if currentProject.modified is True:
            # frame = self._currentProject.getFrames()[0]
            frame = self._projectManager.currentProject.getFrames()[0]
            frame.SetFocus()
            self.showFrame(frame)

            dlg = MessageDialog(None, "Your project has not been saved. Would you like to save it ?", "Save changes ?", YES_NO | ICON_QUESTION)
            if dlg.ShowModal() == ID_YES:
                if self.saveFile() is False:
                    return False

        # Remove the frame in the notebook
        pages = list(range(self._diagramNotebook.GetPageCount()))
        pages.reverse()
        for i in pages:
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame in self._projectManager.currentProject.getFrames():
                self._diagramNotebook.DeletePage(i)

        # self._currentProject.removeFromTree()
        self._removeProjectFromTree(pyutProject=currentProject)
        # self._projects.remove(self._currentProject)
        self._projectManager.removeProject(self._projectManager.currentProject)

        self.logger.debug(f'{self._projectManager.currentProject.filename=}')
        # self._currentProject = None

        self._currentFrame = None

        # nbrProjects: int = len(self._projects)
        currentProjects: PyutProjects = self._projectManager.projects
        nbrProjects: int = len(currentProjects)
        self.logger.debug(f'{nbrProjects=}')
        if nbrProjects > 0:
            newCurrentProject: IPyutProject = currentProjects[0]
            self._updateTreeNotebookIfPossible(project=newCurrentProject)

        # self._mediator.updateTitle()  TODO V2 API update needed  Send event

        return True

    @deprecated(reason='use property .currentProject')
    def getCurrentProject(self) -> IPyutProject:
        """
        Get the current working project

        Returns:
            the current project or None if not found
        """
        return self._currentProject

    def isProjectLoaded(self, filename: str) -> bool:
        """

        Args:
            filename:

        Returns:
            `True` if the project is already loaded
        """
        # for project in self._projects:
        for project in self._projectManager.projects:
            if project.filename == filename:
                return True
        return False

    def openFile(self, filename, project: IPyutProject = None) -> bool:
        """
        Open a file
        TODO:  Fix V2 this does 2 things loads from a file or from a project

        Args:
            filename:
            project:

        Returns:
            `True` if operation succeeded
        """
        self.logger.info(f'{filename=} {project=}')
        # Exit if the file is already loaded
        if self.isProjectLoaded(filename) is True:
            PyutUtils.displayError("The selected file is already loaded !")
            return False

        # Create a new project ?
        if project is None:
            # project = PyutProjectV2(PyutConstants.DEFAULT_FILENAME, self._diagramNotebook, self._projectTree, self._projectTree.projectTreeRoot)
            project = self.newProject()

        # Load the project and add it
        try:
            if not project.loadFromFilename(filename):
                eMsg: str = f'{"The file cannot be loaded !"} - {filename}'
                PyutUtils.displayError(eMsg)
                return False
            # TODO V2 UI bogus fix .newProject added to the list
            # Need to keep it this way unit we get the new IOXml plug
            if project in self._projectManager.projects:
                pass
            else:
                # self._projects.append(project)
                self._projectManager.addProject(project)
            # self._currentProject = project
            self._projectManager.currentProject = project
        except (ValueError, Exception) as e:
            self.logger.error(f"An error occurred while loading the project ! {e}")
            raise e

        success: bool = self._addProjectToNotebook(project)
        # self.logger.debug(f'{self._currentFrame=} {self.currentProject=} {self._diagramNotebook.GetSelection()=}')
        self.logger.debug(f'{self._currentFrame=} {project=} {self._diagramNotebook.GetSelection()=}')
        return success

    def saveFile(self) -> bool:
        """
        Save the current project
        TODO: Fix V2 code

        Returns:
            `True` if the save succeeds else `False`
        """
        currentProject = self._projectManager.currentProject
        if currentProject is None:
            PyutUtils.displayError("No diagram to save !", "Error")
            return False

        if currentProject.filename is None or currentProject.filename == PyutConstants.DEFAULT_FILENAME:
            return self.saveFileAs()
        else:
            # return currentProject.saveXmlPyut()
            return self.saveProject(pyutProject=currentProject)

    def saveFileAs(self):
        """
        Ask for a filename and save the diagram data
        TODO:  method is too big and too complicated fix in V2 UI
        Returns:
            `True` if the save succeeds else `False`
        """
        project: IPyutProject = self._projectManager.currentProject
        if len(project.documents) == 0:
            PyutUtils.displayError("No diagram to save !", "Error")
            return

        currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()

        # Ask for filename

        fDialog: FileDialog = FileDialog(self, defaultDir=currentDirectoryHandler.currentDirectory,
                                         wildcard="Pyut file (*.put)|*.put",
                                         style=FD_SAVE | FD_OVERWRITE_PROMPT)

        # Return False if canceled
        if fDialog.ShowModal() != ID_OK:
            fDialog.Destroy()
            return False

        # Find if a specified filename is already opened
        filename = fDialog.GetPath()

        # if len([project for project in self._projects if project.filename == filename]) > 0:
        if len([project for project in self._projectManager.projects if project.filename == filename]) > 0:
            eMsg: str = f'Error ! This project {filename} is currently open.  Please choose another project name !'
            dlg: MessageDialog = MessageDialog(None, eMsg, "Save change, filename error", OK | ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        project = self._projectManager.currentProject
        project.filename = fDialog.GetPath()
        # project.saveXmlPyut()
        self.saveProject(pyutProject=project)

        # Modify notebook text
        for i in range(self._diagramNotebook.GetPageCount()):
            frame = self._diagramNotebook.GetPage(i)
            document = [document for document in project.documents if document.diagramFrame is frame]
            if len(document) > 0:
                document = document[0]
                if frame in project.getFrames():
                    diagramTitle: str = document.title
                    shortName:    str = self._shortenNotebookPageDiagramName(diagramTitle)

                    self._diagramNotebook.SetPageText(i, shortName)
            else:
                self.logger.info("Not updating notebook in FileHandling")

        currentDirectoryHandler.currentDirectory = fDialog.GetPath()

        project.modified = False
        # dlg.Destroy()
        return True

    def saveProject(self, pyutProject: IPyutProject) -> bool:
        """
        save the project
        """
        from org.pyut.persistence.IoFile import IoFile
        io: IoFile = IoFile()
        BeginBusyCursor()
        try:
            io.save(pyutProject)
            self._modified = False
            self.updateTreeText(pyutProject=pyutProject)
        except (ValueError, Exception) as e:
            PyutUtils.displayError(f"An error occurred while saving project {e}")
        EndBusyCursor()

        return True

    def removeAllReferencesToUmlFrame(self, umlFrame: UmlDiagramsFrame):
        """
        Remove all my references to a given uml frame

        Args:
            umlFrame:
        """
        # Current frame ?
        if self._currentFrame is umlFrame:
            self._currentFrame = cast(UmlDiagramsFrame, None)

        pageCount: int = self._diagramNotebook.GetPageCount()
        for i in range(pageCount):
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame is umlFrame:
                self._diagramNotebook.DeletePage(i)
                break

    def updateTreeText(self, pyutProject: IPyutProject):
        """
        TODO: V2 moved it out of PyutProject
        Update the tree text for this document
        """
        # self._tree.SetItemText(self._treeRoot, self._justTheFileName(self._filename))
        self._projectTree.SetItemText(pyutProject.projectTreeRoot, self._justTheFileName(pyutProject.filename))
        for document in pyutProject.documents:
            self.logger.debug(f'updateTreeText: {document=}')
            document.updateTreeText()

    def _justTheFileName(self, filename):
        """
        Return just the file name portion of the fully qualified path

        Args:
            filename:  file name to display

        Returns:
            A better file name
        """
        regularFileName: str = osPath.split(filename)[1]
        if PyutPreferences().displayProjectExtension is False:
            regularFileName = osPath.splitext(regularFileName)[0]

        return regularFileName

    # noinspection PyUnusedLocal
    def _onDiagramNotebookPageChanged(self, event):
        """
        Callback for notebook page changed

        Args:
            event:
        """
        self._notebookCurrentPageNumber = self._diagramNotebook.GetSelection()
        self.logger.info(f'{self._notebookCurrentPageNumber=}')
        self._currentFrame = self._getCurrentFrameFromNotebook()

        # self._mediator.updateTitle()      # TODO to fill out V2
        self._getTreeItemFromFrame(self._currentFrame)

        # Register the current project
        self._currentProject = self.getProjectFromFrame(self._currentFrame)

    def _onProjectTreeSelectionChanged(self, event: TreeEvent):
        """
        Called when the selection in the project changes

        Args:
            event:
        """
        itm:      TreeItemId   = event.GetItem()
        pyutData: TreeDataType = self._projectTree.GetItemData(itm)
        self.logger.debug(f'Clicked on: {itm=} `{pyutData=}`')

        # Use our own base type
        if isinstance(pyutData, UmlDiagramsFrame):
            frame: UmlDiagramsFrame = pyutData
            self._currentFrame = frame
            self._currentProject = self.getProjectFromFrame(frame)
            self._syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, PyutProjectV2):
            project: PyutProjectV2 = pyutData
            projectFrames: List[UmlFrameType] = project.getFrames()
            if len(projectFrames) > 0:
                self._currentFrame = projectFrames[0]
                self._syncPageFrameAndNotebook(frame=self._currentFrame)
                # self._mediator.updateTitle()      TODO: V2 needs update
            self._currentProject = project

    def _onProjectTreeRightClick(self, treeEvent: TreeEvent):

        itemId: TreeItemId = treeEvent.GetItem()
        data = self._projectTree.GetItemData(item=itemId)
        self.logger.info(f'Item Data: `{data}`')
        if isinstance(data, IPyutProject):
            self._popupProjectMenu()
        elif isinstance(data, UmlDiagramsFrame):            # TODO  We should put the IPyutDocument on the node
            self._popupProjectDocumentMenu()

    def _popupProjectMenu(self):

        # self._mediator.resetStatusText()      TODO V2 UI;  should send message

        if self._projectPopupMenu is None:
            self.logger.info(f'Create the project popup menu')
            [closeProjectMenuID] = PyutUtils.assignID(1)
            popupMenu: Menu = Menu('Actions')
            popupMenu.AppendSeparator()
            popupMenu.Append(closeProjectMenuID, 'Close Project', 'Remove project from tree', ITEM_NORMAL)
            popupMenu.Bind(EVT_MENU, self._onCloseProject, id=closeProjectMenuID)
            self._projectPopupMenu = popupMenu

        self.logger.info(f'currentProject: `{self._projectManager.currentProject}`')
        self._parentWindow.PopupMenu(self._projectPopupMenu)

    def _popupProjectDocumentMenu(self):

        if self._documentPopupMenu is None:

            self.logger.info(f'Create the document popup menu')

            [editDocumentNameMenuID, removeDocumentMenuID] = PyutUtils.assignID(2)

            popupMenu: Menu = Menu('Actions')
            popupMenu.AppendSeparator()
            popupMenu.Append(editDocumentNameMenuID, 'Edit Document Name', 'Change document name', ITEM_NORMAL)
            popupMenu.Append(removeDocumentMenuID,   'Remove Document',    'Delete it',            ITEM_NORMAL)

            popupMenu.Bind(EVT_MENU, self._onEditDocumentName, id=editDocumentNameMenuID)
            popupMenu.Bind(EVT_MENU, self._onRemoveDocument,   id=removeDocumentMenuID)

            self.__documentPopupMenu = popupMenu

        self.logger.info(f'Current Document: `{self.currentDocument}`')
        self._parentWindow.PopupMenu(self.__documentPopupMenu)

    # noinspection PyUnusedLocal
    def _onCloseProject(self, event: CommandEvent):
        self.closeCurrentProject()

    # noinspection PyUnusedLocal
    def _onEditDocumentName(self, event: CommandEvent):

        self.logger.info(f'{self._notebookCurrentPageNumber=}  {self._diagramNotebook.GetSelection()=}')
        if self._notebookCurrentPageNumber == -1:
            self._notebookCurrentPageNumber = self._diagramNotebook.GetSelection()    # must be default empty project

        currentDocument: IPyutDocument   = self.currentDocument
        dlgEditDocument: DlgEditDocument = DlgEditDocument(parent=self.currentFrame, dialogIdentifier=ID_ANY, document=currentDocument)
        dlgEditDocument.Destroy()

        #
        # TODO can cause
        #     self.__notebook.SetPageText(page=self.__notebookCurrentPage, text=currentDocument.title)
        # wx._core.wxAssertionError: C++ assertion ""((nPage) < GetPageCount())""
        # failed at dist-osx-py38/build/ext/wxWidgets/src/osx/notebook_osx.cpp(120)
        # in SetPageText(): SetPageText: invalid notebook page
        #
        self._diagramNotebook.SetPageText(page=self._notebookCurrentPageNumber, text=currentDocument.title)
        currentDocument.updateTreeText()

    # noinspection PyUnusedLocal
    def _onRemoveDocument(self, event: CommandEvent):
        """
        Invoked from the popup menu in the tree

        Args:
            event:
        """
        project:         IPyutProject  = self._projectManager.currentProject
        currentDocument: IPyutDocument = self.currentDocument
        project.removeDocument(currentDocument)

    def _getCurrentFrameFromNotebook(self):
        """
        Get the current frame in the notebook

        Returns:
        """

        noPage: int = self._notebookCurrentPageNumber
        self.logger.info(f'{noPage=}')
        if noPage == -1:
            return None
        frame = self._diagramNotebook.GetPage(noPage)
        return frame

    def _getTreeItemFromFrame(self, frame: UmlDiagramsFrame) -> TreeItemId:

        projectTree: ProjectTree = self._projectTree

        treeRootItemId: TreeItemId   = projectTree.GetRootItem()
        pyutData:       TreeDataType = projectTree.GetItemData(treeRootItemId)

        self.logger.info(f'{treeRootItemId=} {pyutData=} {frame=}')

        self.logger.info(f'{projectTree.GetCount()=}')
        return treeRootItemId

    def _addProjectToNotebook(self, project: IPyutProject) -> bool:

        success: bool = True
        self.logger.info(f'{project=}')
        try:
            for document in project.documents:
                diagramTitle: str = document.title
                shortName:    str = self._shortenNotebookPageDiagramName(diagramTitle)
                self._diagramNotebook.AddPage(document.diagramFrame, shortName)

            self._notebookCurrentPageNumber = self._diagramNotebook.GetPageCount()-1
            self._diagramNotebook.SetSelection(self._notebookCurrentPageNumber)

            self._updateTreeNotebookIfPossible(project=project)

        except (ValueError, Exception) as e:
            PyutUtils.displayError(f"An error occurred while adding the project to the notebook {e}")
            success = False

        return success

    def _updateTreeNotebookIfPossible(self, project: IPyutProject):
        """

        Args:
            project:
        """
        project.selectFirstDocument()

        if len(project.documents) > 0:
            self._currentFrame = project.documents[0].diagramFrame
            self._syncPageFrameAndNotebook(frame=self._currentFrame)

    def _syncPageFrameAndNotebook(self, frame: UmlDiagramsFrame):
        """

        Args:
            frame:
        """

        for i in range(self._diagramNotebook.GetPageCount()):
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame is frame:
                self._diagramNotebook.SetSelection(i)
                break

    def _shortenNotebookPageDiagramName(self, diagramTitle: str) -> str:
        """
        Return a shorter filename to display; For file names longer
        than `MAX_NOTEBOOK_PAGE_NAME_LENGTH` this method takes the first
        four characters and the last eight as the shortened file name

        Args:
            diagramTitle:  The diagram name to display

        Returns:
            A short diagram name
        """
        justFileName: str = osPath.split(diagramTitle)[1]
        if len(justFileName) > MAX_NOTEBOOK_PAGE_NAME_LENGTH:
            firstFour: str = justFileName[:4]
            lastEight: str = justFileName[-8:]
            return f'{firstFour}{lastEight}'
        else:
            return justFileName

    def _removeProjectFromTree(self, pyutProject: IPyutProject):
        """
        Remove the project from the tree
        TODO: V2 UI this belongs in the project tree component itself
        Args:
            pyutProject:

        """
        """
        """
        projectTreeRoot: TreeItemId = pyutProject.projectTreeRoot
        self._projectTree.Delete(projectTreeRoot)
