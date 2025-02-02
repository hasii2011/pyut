
from typing import List
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from xml.sax import SAXParseException

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

from pyut.PyutConstants import PyutConstants
from pyut.PyutUtils import PyutUtils

from pyut.errorcontroller.ErrorManager import ErrorManager

from pyut.general.exceptions.UnsupportedFileTypeException import UnsupportedFileTypeException

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from pyut.ui.umlframes.UmlFrame import UmlFrame
from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.ui.IPyutDocument import IPyutDocument
from pyut.ui.IPyutDocument import PyutDocuments
from pyut.ui.IPyutProject import IPyutProject

from pyut.ui.DiagramNotebook import DiagramNotebook
from pyut.ui.ProjectException import ProjectException
from pyut.ui.ProjectException import ProjectExceptionType
from pyut.ui.ProjectTree import ProjectTree
from pyut.ui.PyutDocument import PyutDocument
from pyut.ui.PyutProject import PyutProject

from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from oglio.Writer import Writer
from oglio.Reader import Reader
from oglio.Types import OglProject
from oglio.Types import OglDocument
from oglio.Types import OglDocumentTitle
from ogl.OglActor import OglActor
from ogl.OglUseCase import OglUseCase

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from oglio.toXmlV11.OglToXml import XML_VERSION

PyutProjects = NewType('PyutProjects', List[IPyutProject])

MAX_NOTEBOOK_PAGE_NAME_LENGTH: int = 12         # TODO make this a preference


def defaultProjectNumber():
    for i in range(9999):
        yield i


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

        self._defaultProjectNumber = defaultProjectNumber()

    @property
    def projects(self) -> PyutProjects:
        """
        The list of currently managed projects;  You get a copy;  So any manipulations
        will be 'por nada`'

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

        assert newProject in self._projects or newProject is None or newProject.projectName == PyutConstants.DEFAULT_PROJECT_NAME, ''
        if newProject is None:
            self.logger.debug(f'Project set to None')
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

    def getProject(self, projectName: str) -> IPyutProject:
        """
        Return the project that has the input name
        Args:
            projectName: The project name

        Returns:  The project associated with the name;  May return 'None' if
        there is no such project
        """
        foundProject: IPyutProject = cast(IPyutProject, None)
        for currentProject in self._projects:
            if currentProject.projectName == projectName:
                foundProject = currentProject
                break

        return foundProject

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

    def deleteDocument(self, project: IPyutProject, document: IPyutDocument, askForConfirmation: bool = True):
        """
        Remove a given document from the project.

        Args:
            project
            document: PyutDocument to remove from this project
            askForConfirmation:  If `True` ask for confirmation
        """
        if askForConfirmation is True:
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

    def newProject(self) -> IPyutProject:
        """
        Create a new project;  Adds it to the Project Tree;  Adds it to our managed list

        Returns:  A default empty project
        """
        fileName: str = f'{PyutConstants.DEFAULT_FILE_NAME}'
        if self.getProject(PyutConstants.DEFAULT_PROJECT_NAME) is not None:
            sequenceNumber: int = next(self._defaultProjectNumber)
            fileName = f'{PyutConstants.DEFAULT_PROJECT_NAME}_{sequenceNumber}{PyutConstants.PYUT_EXTENSION}'

        project = PyutProject(fileName, self._projectTree, self._projectTree.projectTreeRoot)

        return self._manageProject(pyutProject=project)

    def newNamedProject(self, filename: str) -> IPyutProject:
        """
        Creates a skeletal project for a specific file
        Args:
            filename:
        """
        project: PyutProject = PyutProject(filename=filename, tree=self._projectTree, treeRoot=self._projectTree.projectTreeRoot)

        return self._manageProject(pyutProject=project)

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

        if projectToSave.filename is None or PyutConstants.DEFAULT_PROJECT_NAME in projectToSave.filename:
            self.saveProjectAs(projectToSave=projectToSave)

        else:
            self._writeProject(projectToWrite=projectToSave)
            projectToSave.modified = False
            self.logger.info(f'{projectToSave.filename} saved.')

    def openProject(self, filename: str) -> Tuple[OglProject, IPyutProject]:
        """
        Open a file, creates PyutProject, update myself, make the new project
        the current one;  Update the UI

        Supports .put and .xml extensions
        Args:
            filename:

        Returns:  Tuple: The OglProject that was read and a newly created PyutProject
        """
        self.logger.info(f'{filename=}')

        project: IPyutProject = self.newProject()
        project.filename = filename

        try:
            oglProject: OglProject = self._readFile(filename=filename)
        except SAXParseException:
            ErrorManager.addToLogFile(title='Invalid Project Content', msg='Recovery Started')
            raise ProjectException(exceptionType=ProjectExceptionType.INVALID_PROJECT, message='Invalid Project Content', project=project)
        except FileNotFoundError:
            ErrorManager.addToLogFile(title='Project not found', msg='Recovery Started')
            raise ProjectException(exceptionType=ProjectExceptionType.PROJECT_NOT_FOUND, message='Project not found', project=project)
        except AttributeError as ae:
            ErrorManager.addToLogFile(title='Attribute Error', msg=f'{ae}')
            raise ProjectException(exceptionType=ProjectExceptionType.ATTRIBUTE_ERROR, message='Incompatible XML', project=project)
        except TypeError as te:
            ErrorManager.addToLogFile(title='Type Error', msg=f'{te}')
            raise ProjectException(exceptionType=ProjectExceptionType.TYPE_ERROR, message=f'Type Error {te}', project=project)
        except AssertionError as assertionError:
            ErrorManager.addToLogFile(title='Assertion Raised', msg=f'{assertionError}')
            raise ProjectException(exceptionType=ProjectExceptionType.ASSERTION_ERROR, message=f'Type Error {assertionError}', project=project)
        except (ValueError, Exception) as e:
            ErrorManager.addToLogFile(title='General Error', msg=f'{e}')

            errorMsg: str = ErrorManager.getErrorInfo()

            raise ProjectException(exceptionType=ProjectExceptionType.GENERAL_ERROR, message=errorMsg, project=project)

        self.currentProject = project
        self.updateProjectTreeText(pyutProject=project)
        wxYield()

        self.logger.info(f'Project {project.projectName} opened')
        return oglProject, project

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

        oldName: str = projectToSave.filename
        projectToSave.filename = fDialog.GetPath()
        self._writeProject(projectToWrite=projectToSave)
        self.updateProjectTreeText(pyutProject=projectToSave)

        currentDirectoryHandler.currentDirectory = fDialog.GetPath()

        projectToSave.modified = False
        self.logger.info(f'Project {oldName} saved as {projectToSave.filename}')

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

    def addDocumentNodeToTree(self, pyutProject: IPyutProject, documentNode: IPyutDocument):
        """

        Args:
            pyutProject:
            documentNode:

        """
        nodeID: TreeItemId = self._projectTree.AppendItem(pyutProject.projectTreeRoot, documentNode.title)

        documentNode.treeRoot = nodeID
        self._projectTree.SetItemData(nodeID, documentNode)

    def updateProjectTreeText(self, pyutProject: IPyutProject):
        """
        Updates the project's name and all of its document names

        Args:
            pyutProject:  The project data to use
        """
        self._projectTree.SetItemText(pyutProject.projectTreeRoot, PyutUtils.determineProjectName(pyutProject.filename))
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

    def _writeProject(self, projectToWrite: IPyutProject):
        """
        Interface to the actual I/O code

        Args:
            projectToWrite:
        """
        BeginBusyCursor()
        oglProject: OglProject = OglProject()
        oglProject.codePath = projectToWrite.codePath
        oglProject.version  = XML_VERSION           # Do not really need this as oglio sets it appropriately
        documents: PyutDocuments = projectToWrite.documents
        for document in documents:
            pyutDocument: PyutDocument = cast(PyutDocument, document)

            oglDocument:  OglDocument = self._toBasicOglDocument(pyutDocument=pyutDocument)
            diagramFrame: UmlFrame    = pyutDocument.diagramFrame
            oglObjects:   UmlObjects  = diagramFrame.umlObjects

            for oglObject in oglObjects:
                match oglObject:
                    case OglClass() as oglObject:
                        oglDocument.oglClasses.append(oglObject)
                    case OglSDMessage() as oglObject:               # Put here so it does not fall into OglLink
                        oglSDMessage: OglSDMessage = cast(OglSDMessage, oglObject)
                        modelId: int = oglSDMessage.pyutObject.id
                        oglDocument.oglSDMessages[modelId] = oglSDMessage
                    case OglLink() as oglObject:
                        oglDocument.oglLinks.append(oglObject)
                    case OglInterface2() as oglObject:
                        oglDocument.oglLinks.append(cast(OglLink, oglObject))      # temp cast until I fix OglInterface2
                    case OglNote() as oglObject:
                        oglDocument.oglNotes.append(oglObject)
                    case OglText() as oglObject:
                        oglDocument.oglTexts.append(oglObject)
                    case OglUseCase() as oglObject:
                        oglDocument.oglUseCases.append(oglObject)
                    case OglActor() as oglObject:
                        oglDocument.oglActors.append(oglObject)
                    case OglSDInstance() as oglObject:
                        oglSDInstance: OglSDInstance = cast(OglSDInstance, oglObject)
                        modelId = oglSDInstance.pyutSDInstance.id
                        oglDocument.oglSDInstances[modelId] = oglSDInstance
                    case _:
                        self.logger.error(f'Unknown ogl object type: {oglObject}, not saved')
            oglProject.oglDocuments[oglDocument.documentTitle] = oglDocument

            oglWriter: Writer = Writer()
            oglWriter.writeFile(oglProject=oglProject, fqFileName=projectToWrite.filename)

        EndBusyCursor()

    def _readFile(self, filename: str) -> OglProject:
        """
        Interface to the actual I/O code
        Get the project Ogl Objects
        Args:
            filename: filename to open

        Returns:    Returns an OglProject
        """
        self.logger.debug(f'loadFromFilename: {filename=}')
        BeginBusyCursor()

        reader: Reader = Reader()

        if filename.endswith('.put'):
            oglProject: OglProject = reader.readFile(fqFileName=filename)
        elif filename.endswith('.xml'):
            oglProject = reader.readXmlFile(fqFileName=filename)
        else:
            raise UnsupportedFileTypeException()

        EndBusyCursor()
        return oglProject

    def _manageProject(self, pyutProject: PyutProject):
        """
        Creates the UI elements for the new project and places in the project manager list
        Args:
            pyutProject:
        """
        projectTreeRoot: TreeItemId = self._projectTree.addProjectToTree(pyutProject=pyutProject)

        pyutProject.projectTreeRoot = projectTreeRoot

        wxYield()
        self.addProject(project=pyutProject)
        return pyutProject

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

    def _toBasicOglDocument(self, pyutDocument: IPyutDocument) -> OglDocument:
        """
        Extracts basic Pyut Document properties and moves them to the OglDocument

        Args:
            pyutDocument:

        Returns: A new OglDocument
        """
        oglDocument: OglDocument = OglDocument()
        oglDocument.documentType = pyutDocument.diagramType.__str__()
        oglDocument.documentTitle = OglDocumentTitle(pyutDocument.title)

        diagramFrame: UmlFrame = pyutDocument.diagramFrame
        scrollPosX, scrollPosY = diagramFrame.GetViewStart()

        xUnit, yUnit = diagramFrame.GetScrollPixelsPerUnit()

        oglDocument.scrollPositionX = scrollPosX
        oglDocument.scrollPositionY = scrollPosY
        oglDocument.pixelsPerUnitX = xUnit
        oglDocument.pixelsPerUnitY = yUnit

        return oglDocument
