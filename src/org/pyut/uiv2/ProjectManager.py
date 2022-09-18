
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from os import path as osPath

from wx import FD_OVERWRITE_PROMPT
from wx import FD_SAVE
from wx import FileDialog
from wx import ICON_ERROR
from wx import MessageDialog
from wx import OK
from wx import TreeItemId

from wx import BeginBusyCursor
from wx import EndBusyCursor

from org.pyut.PyutConstants import PyutConstants
from org.pyut.dialogs.DlgAbout import ID_OK
from org.pyut.preferences.PyutPreferences import PyutPreferences
from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.ui.IPyutProject import IPyutProject
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

        self._projects:       PyutProjects = PyutProjects([])
        self._currentProject: IPyutProject = cast(IPyutProject, None)

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

    def addProject(self, project: IPyutProject):
        """
        Add a new project to manage
        Args:
            project:   Should not already be managed
        """
        assert project not in self._projects
        self._projects.append(project)

    def removeProject(self, project: IPyutProject):
        """
        Remove a project from our purview

        Args:
            project:   The project to no longer manage; should have been
            previously managed
        """
        assert project in self._projects
        self._projects.remove(project)

    def updateTreeText(self, pyutProject: IPyutProject):
        """
        """
        self._projectTree.SetItemText(pyutProject.projectTreeRoot, self._justTheFileName(pyutProject.filename))
        for document in pyutProject.documents:
            self.logger.debug(f'updateTreeText: {document=}')
            document.updateTreeText()

    def newProject(self) -> IPyutProject:
        """
        Create a new project;  Adds it to the Project Tree;

        Returns:  A default empty project
        """
        project = PyutProjectV2(PyutConstants.DEFAULT_FILENAME, self._projectTree, self._projectTree.projectTreeRoot)

        projectTreeRoot: TreeItemId = self._projectTree.addProjectToTree(pyutProject=project)

        project.projectTreeRoot = projectTreeRoot

        # self._projects.append(project)
        # self._currentProject = project
        self.addProject(project)
        self.currentProject = project

        # self._currentFrame   = cast(UmlDiagramsFrame, None)   Caller needs to do this

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
            # 'Fixed in mypy 0.980'
            projectToSave.modified = False       # type: ignore

    def saveProjectAs(self, projectToSave: IPyutProject):
        """
        Will always query user for new project name

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
        # Find if a specified filename is already opened
        filename = fDialog.GetPath()
        if len([project for project in self.projects if project.filename == filename]) > 0:
            eMsg: str = f'Error ! This project {filename} is currently open.  Please choose another project name !'
            dlg: MessageDialog = MessageDialog(None, eMsg, "Save change, filename error", OK | ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # 'Fixed in mypy 0.980'
        projectToSave.filename = fDialog.GetPath()  # type: ignore
        self._writeProject(projectToWrite=projectToSave)

        # Modify notebook text
        for i in range(self._diagramNotebook.GetPageCount()):
            frame = self._diagramNotebook.GetPage(i)
            documents = [document for document in projectToSave.documents if document.diagramFrame is frame]
            if len(documents) > 0:
                document = documents[0]
                if frame in projectToSave.getFrames():
                    diagramTitle: str = document.title
                    shortName:    str = self._shortenNotebookPageDiagramName(diagramTitle)

                    self._diagramNotebook.SetPageText(i, shortName)
            else:
                self.logger.info("Not updating notebook in FileHandling")

        currentDirectoryHandler.currentDirectory = fDialog.GetPath()

        # 'Fixed in mypy 0.980'
        projectToSave.modified = False       # type: ignore

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
            self._updateTreeText(pyutProject=projectToWrite)
        except (ValueError, Exception) as e:
            msg:     str = f"An error occurred while saving project {e}"
            caption: str = 'Error from IoFile'
            booBoo: MessageDialog = MessageDialog(parent=None, message=msg, caption=caption, style=OK | ICON_ERROR)
            booBoo.ShowModal()
        finally:
            EndBusyCursor()

    def _updateTreeText(self, pyutProject: IPyutProject):
        """
        """
        self._projectTree.SetItemText(pyutProject.projectTreeRoot, self._justTheFileName(pyutProject.filename))
        for document in pyutProject.documents:
            self.logger.debug(f'updateTreeText: {document=}')
            document.updateTreeText()

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
