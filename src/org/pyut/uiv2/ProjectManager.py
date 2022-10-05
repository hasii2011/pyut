
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from os import path as osPath

from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import ICON_ERROR
from wx import ID_NO
from wx import ID_OK
from wx import OK
from wx import YES_NO

from wx import FileDialog
from wx import MessageDialog
from wx import TreeItemId

from wx import BeginBusyCursor
from wx import EndBusyCursor

from wx import Yield as wxYield

from org.pyut.PyutConstants import PyutConstants

from org.pyut.general.exceptions.UnsupportedXmlFileFormat import UnsupportedXmlFileFormat

from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler

from org.pyut.uiv2.IPyutDocument import IPyutDocument
from org.pyut.uiv2.IPyutProject import IPyutProject

from org.pyut.uiv2.DiagramNotebook import DiagramNotebook
from org.pyut.uiv2.ProjectTree import ProjectTree
from org.pyut.uiv2.PyutProjectV2 import PyutProjectV2

from org.pyut.persistence.IoFile import IoFile

PyutProjects = NewType('PyutProjects', List[IPyutProject])

MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12         # TODO make this a preference


class ProjectManager:
    """
    This project manages interactions to the UI project tree
    """

    def __init__(self, projectTree: ProjectTree, diagramNoteBook: DiagramNotebook):
        """

        Args:
            projectTree:  The UI component that displays project nodes
        """

        self.logger:  Logger = getLogger(__name__)

        self._projectTree:     ProjectTree    = projectTree
        self._diagramNotebook: DiagramNotebook = diagramNoteBook

        self._projects:        PyutProjects     = PyutProjects([])
        self._currentProject:  IPyutProject     = cast(IPyutProject, None)
        self._currentDocument: IPyutDocument    = cast(IPyutDocument, None)
        self._currentFrame:    UmlDiagramsFrame = cast(UmlDiagramsFrame, None)

    @property
    def projects(self) -> PyutProjects:
        """
        The list of currently managed projects

        Returns:  Only a copy of the projects
        """
        return copy(self._projects)

    @property
    def currentProject(self) -> IPyutProject:
        """
        Returns:  The currently managed project
        """
        return self._currentProject

    @currentProject.setter
    def currentProject(self, newProject: IPyutProject):
        """
        Set the currently managed project

        Args:
            newProject:   Must have been previously managed
        """
        assert newProject in self._projects
        self._currentProject = newProject

    @property
    def currentDocument(self) -> IPyutDocument:
        return self._currentDocument

    @currentDocument.setter
    def currentDocument(self, newDocument: IPyutDocument):
        self._currentDocument = newDocument

    @property
    def currentFrame(self) -> UmlDiagramsFrame:
        return self._currentFrame

    @currentFrame.setter
    def currentFrame(self, newFrame: UmlDiagramsFrame):
        self._currentFrame = newFrame

    def isProjectLoaded(self, filename: str) -> bool:
        """

        Args:
            filename:

        Returns:
            `True` if the project is already loaded
        """
        for project in self.projects:
            if project.filename == filename:
                return True
        return False

    def addProject(self, project: IPyutProject):
        """
        Add a new project to manage
        Args:
            project:   Should not already be managed
        """
        assert project not in self._projects
        self._projects.append(project)

    def addDocumentNodeToTree(self, pyutProject: IPyutProject, documentNode: IPyutDocument):
        """

        Args:
            pyutProject:
            documentNode:

        """
        nodeID: TreeItemId = self._projectTree.AppendItem(pyutProject.projectTreeRoot, documentNode.title)

        documentNode.treeRoot = nodeID
        self._projectTree.SetItemData(nodeID, documentNode)

    def removeProject(self, project: IPyutProject):
        """
        Remove a project from our purview

        Args:
            project:   The project to no longer manage; should have been
            previously managed
        """
        assert project in self._projects
        self._projects.remove(project)

    def deleteDocument(self, project: IPyutProject, document: IPyutDocument, confirmation: bool = True):
        """
        Remove a given document from the project.

        Args:
            project
            document: PyutDocument to remove from this project
            confirmation:  If `True` ask for confirmation
        """
        if confirmation:
            dlg = MessageDialog(None, f'Are you sure to remove "{document.title}"?', "Remove a document from a project", YES_NO)
            if dlg.ShowModal() == ID_NO:
                dlg.Destroy()
                return
            dlg.Destroy()

        # Remove references
        self._removeAllReferencesToUmlFrame(document.diagramFrame)
        # update the UI
        self._projectTree.Delete(document.treeRoot)

        # Remove document from documents list
        project.documents.remove(document)
        project.modified = True

    def updateProjectTreeText(self, pyutProject: IPyutProject):
        """
        Updates the project's name and all of its document names

        Args:
            pyutProject:  The project data to use
        """
        self._projectTree.SetItemText(pyutProject.projectTreeRoot, self._justTheFileName(pyutProject.filename))
        for document in pyutProject.documents:
            self.logger.debug(f'Update document name: {document=}')
            self._projectTree.SetItemText(document.treeRoot, document.title)

    # noinspection PyUnusedLocal
    def updateTreeText(self, pyutProject: IPyutProject):
        assert False, 'Use .updateProjectTreeText'

    def updateDocumentName(self, pyutDocument: IPyutDocument):
        self._projectTree.SetItemText(pyutDocument.treeRoot, pyutDocument.title)

    def updateDiagramNotebookIfPossible(self, project: IPyutProject):
        """

        Args:
            project:
        """
        project.selectFirstDocument()

        if len(project.documents) > 0:
            self._currentFrame = project.documents[0].diagramFrame
            self.syncPageFrameAndNotebook(frame=self._currentFrame)

    def syncPageFrameAndNotebook(self, frame: UmlDiagramsFrame):
        """

        Args:
            frame:
        """
        for i in range(self._diagramNotebook.GetPageCount()):
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame is frame:
                self._diagramNotebook.SetSelection(i)
                break

    def newProject(self) -> IPyutProject:
        """
        Create a new project;  Adds it to the Project Tree;

        Returns:  A default empty project
        """
        project = PyutProjectV2(PyutConstants.DEFAULT_FILENAME, self._projectTree, self._projectTree.projectTreeRoot)

        projectTreeRoot: TreeItemId = self._projectTree.addProjectToTree(pyutProject=project)

        project.projectTreeRoot = projectTreeRoot
        self.addProject(project)
        self.currentProject = project

        wxYield()
        return project

    def saveProject(self, projectToSave: IPyutProject):
        """
        Save the project;  If the project has no name or the default file name,
        then it will invoke .saveProjectAs

        Args:
            projectToSave:
        """

        if projectToSave is None:
            booBoo: MessageDialog = MessageDialog(parent=None, message='No diagram to save !', caption='Error', style=OK | ICON_ERROR)
            booBoo.ShowModal()

        if projectToSave.filename is None or projectToSave.filename == PyutConstants.DEFAULT_FILENAME:
            self.saveProjectAs(projectToSave=projectToSave)
            return
        else:
            self._writeProject(projectToWrite=projectToSave)
            PyutPreferences().addNewLastOpenedFilesEntry(projectToSave.filename)

            projectToSave.modified = False

    def openProject(self, filename, project: IPyutProject = None):
        """
        Open a file
        TODO:  Fix V2 this does 2 things loads from a file or from a project

        Args:
            filename:
            project:
        """
        self.logger.info(f'{filename=} {project=}')
        # Exit if the project is already loaded
        if self.isProjectLoaded(filename) is True:
            self._displayError("The selected project is already loaded !")
            return
        # Create a new project ?
        if project is None:
            project = self.newProject()
        # Load the project and add it
        try:
            self._readProject(filename=filename, projectToRead=project)

            # TODO V2 UI bogus fix .newProject added to the list
            # Need to keep it this way until we get the new IOXml plug
            if project in self.projects:
                pass
            else:
                self.addProject(project)
            self.currentProject = project
            PyutPreferences().addNewLastOpenedFilesEntry(project.filename)

        except (ValueError, Exception) as e:
            self.logger.error(f"An error occurred while loading the project ! {e}")
            raise e

        # self._addProjectDocumentsToNotebook(project)
        # self.logger.debug(f'{self._currentFrame=} {self.currentProject=} {self._diagramNotebook.GetSelection()=}')

    def saveProjectAs(self, projectToSave: IPyutProject):
        """
        Will always query user for new project name

        TODO:  Break up in sub methods
            1 Get a new project name (or not)
            2 Update the Notebook view (I do not think we need to do this)
        TODO:  Do we really need to keep track of the current directory
        Args:
            projectToSave:
        """

        if len(projectToSave.documents) == 0:
            booBoo: MessageDialog = MessageDialog(parent=None, message='No diagram to save !', caption='Error', style=OK | ICON_ERROR)
            booBoo.ShowModal()
            return

        currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()
        fDialog:                 FileDialog              = FileDialog(None, defaultDir=currentDirectoryHandler.currentDirectory,
                                                                      wildcard="Pyut file (*.put)|*.put",
                                                                      style=FD_SAVE | FD_OVERWRITE_PROMPT)
        # Return False if canceled
        if fDialog.ShowModal() != ID_OK:
            fDialog.Destroy()
            return
        # Find if a specified project is already open
        filename = fDialog.GetPath()
        if len([project for project in self.projects if project.filename == filename]) > 0:
            eMsg: str = f'Error ! This project {filename} is currently open.  Please choose another project name !'
            dlg: MessageDialog = MessageDialog(None, eMsg, "Save change, filename error", OK | ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        projectToSave.filename = fDialog.GetPath()
        self._writeProject(projectToWrite=projectToSave)
        self.updateProjectTreeText(pyutProject=projectToSave)

        PyutPreferences().addNewLastOpenedFilesEntry(projectToSave.filename)
        # Modify notebook text
        # for i in range(self._diagramNotebook.GetPageCount()):
        #     frame = self._diagramNotebook.GetPage(i)
        #     documents = [document for document in projectToSave.documents if document.diagramFrame is frame]
        #     if len(documents) > 0:
        #         document = documents[0]
        #         if frame in projectToSave.getFrames():
        #             diagramTitle: str = document.title
        #             shortName:    str = self._shortenNotebookPageDiagramName(diagramTitle)
        #
        #             self._diagramNotebook.SetPageText(i, shortName)
        #     else:
        #         self.logger.info("Not updating notebook in FileHandling")

        currentDirectoryHandler.currentDirectory = fDialog.GetPath()

        projectToSave.modified = False

    def _writeProject(self, projectToWrite: IPyutProject):
        """
        Interface to the actual I/O code

        Args:
            projectToWrite:
        """
        io: IoFile = IoFile()
        BeginBusyCursor()
        try:
            io.save(projectToWrite)
            self._modified = False
        except (ValueError, Exception) as e:
            msg:     str = f"An error occurred while saving project {e}"
            caption: str = 'Error from IoFile'
            booBoo: MessageDialog = MessageDialog(parent=None, message=msg, caption=caption, style=OK | ICON_ERROR)
            booBoo.ShowModal()
        finally:
            EndBusyCursor()

    # def loadFromFilename(self, filename: str) -> bool:
    def _readProject(self, filename: str, projectToRead: IPyutProject):
        """
        Interface to the actual I/O code

        Load a project from a file

        Args:
            filename: filename to open

        Returns:
            `True` if the operation succeeded
        """
        self.logger.info(f'loadFromFilename: {filename=}')
        BeginBusyCursor()
        from org.pyut.persistence.IoFile import IoFile  # Avoid Nuitka cyclical dependency

        io: IoFile = IoFile()
        wxYield()

        projectToRead.filename = filename
        try:
            io.open(filename, projectToRead)
            self._modified = False
        except (ValueError, Exception, UnsupportedXmlFileFormat) as e:
            EndBusyCursor()
            self.logger.error(f"Error loading file: {e}")
            raise e

        EndBusyCursor()
        self.updateProjectTreeText(pyutProject=projectToRead)
        wxYield()

    def _justTheFileName(self, filename):
        """
        Return just the file name portion of the fully qualified path

        Args:
            filename:  long file name

        Returns: A better file name to display
        """
        regularFileName: str = osPath.split(filename)[1]
        if PyutPreferences().displayProjectExtension is False:
            regularFileName = osPath.splitext(regularFileName)[0]

        return regularFileName

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

    def _addProjectDocumentsToNotebook(self, project: IPyutProject):

        self.logger.info(f'{project=}')

        for document in project.documents:
            diagramTitle: str = document.title
            shortName:    str = self._shortenNotebookPageDiagramName(diagramTitle)
            self._diagramNotebook.AddPage(document.diagramFrame, shortName)

        notebookCurrentPageNumber: int  = self._diagramNotebook.GetPageCount()-1
        if notebookCurrentPageNumber >= 0:
            self._diagramNotebook.SetSelection(notebookCurrentPageNumber)

        self.updateDiagramNotebookIfPossible(project=project)

    def _removeAllReferencesToUmlFrame(self, umlFrame: UmlDiagramsFrame):
        """
        Remove all my references to a given uml frame

        Args:
            umlFrame:
        """
        # Current frame ?
        if self.currentFrame is umlFrame:
            self.currentFrame = cast(UmlDiagramsFrame, None)

        pageCount: int = self._diagramNotebook.GetPageCount()
        for i in range(pageCount):
            pageFrame = self._diagramNotebook.GetPage(i)
            if pageFrame is umlFrame:
                self._diagramNotebook.DeletePage(i)
                break

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()
