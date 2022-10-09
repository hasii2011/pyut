
from typing import Callable
from typing import List
from typing import TYPE_CHECKING
from typing import Union

from wx import Frame
from wx import ToolBar

from wx import NewIdRef as wxNewIdRef

from org.pyut.enums.DiagramType import DiagramType
from org.pyut.errorcontroller.ErrorManager import ErrorManager

from miniogl.Diagram import Diagram

from pyutmodel.DisplayMethodParameters import DisplayMethodParameters
from pyutmodel.PyutMethod import PyutMethod

from ogl.OglClass import OglClass

from org.pyut.ui.tools.ToolboxTypes import CategoryNames

if TYPE_CHECKING:
    from org.pyut.ui.umlframes.UmlFrame import UmlObjects
    from org.pyut.uiv2.PyutApplicationFrameV2 import PyutApplicationFrameV2
    from org.pyut.uiv2.PyutUIV2 import PyutUIV2

from org.pyut.dialogs.DlgEditClass import *         # Have to do this to avoid cyclical dependency

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler

from org.pyut.ui.tools.ToolboxOwner import ToolboxOwner

from org.pyut.general.PyutVersion import PyutVersion
from org.pyut.general.Singleton import Singleton

from org.pyut.preferences.PyutPreferences import PyutPreferences

__PyUtVersion__ = PyutVersion.getPyUtVersion()

# Define current use mode
[SCRIPT_MODE, NORMAL_MODE] = PyutUtils.assignID(2)


class Mediator(Singleton):
    """
    This class is the link between the Pyut GUI components. It receives
    commands from the modules, and dispatch them to the right receiver.
    See the Model-View-Controller pattern and the Mediator pattern.
    It is purposefully a singleton.

    Each part of the GUI registers with the mediator. This is done
    with the various `register...` methods.

    The mediator contains a state machine. The different states are
    represented by integer constants, declared at the beginning of this
    module. These are the `ACTION_*` constants.

    The `NEXT_ACTION` dictionary supplies the next action based on the given
    one. For example, after an `ACTION_NEW_NOTE_LINK`, you get an
    `ACTION_DESTINATION_NOTE_LINK` this way::

        nextAction = NEXT_ACTION[ACTION_NEW_NOTE_LINK]

    The state is kept in `self._currentAction`.

    The `doAction` is called whenever a click is received by the UML diagram
    frame.
    """
    def init(self):
        """
        Singleton constructor.
        """
        from org.pyut.uiv2.PyutApplicationFrameV2 import PyutApplicationFrameV2

        self.logger: Logger = getLogger(__name__)

        from org.pyut.errorcontroller.ErrorManager import ErrorManager

        self._errorManager: ErrorManager  = ErrorManager()

        self._useMode       = NORMAL_MODE   # Define current use mode

        self._toolBar  = None   # toolbar
        self._tools    = None   # toolbar tools
        self._appPath  = None   # Application files' path

        self._appFrame: PyutApplicationFrameV2 = cast(PyutApplicationFrameV2, None)   # Application's main frame

        self.registerClassEditor(self.standardClassEditor)
        self._toolboxOwner = None   # toolbox owner, created when application frame is passed
        self._treeNotebookHandler = None

    @property
    def activeUmlFrame(self):
        """
        Return the active UML frame.

        Returns:  The UML frame
        """
        return self._treeNotebookHandler.currentFrame

    def newDocument(self, diagramType: DiagramType):
        """
        New API for V2 UI;  Mediator does not provide access to any UI component
        TODO post v2 UI we will send message to UI component
        Args:
            diagramType:
        """
        self._treeNotebookHandler.newDocument(docType=diagramType)

    def getErrorManager(self) -> ErrorManager:
        """
        Returns:  The current error manager
        """
        return self._errorManager

    def getAppPath(self) -> str:
        """
        Return the path of the application files.

        Returns: a string
        """
        return self._appPath

    def registerFileHandling(self, treeNotebookHandler):
        """
        Register the main part of the user interface
        """
        self._treeNotebookHandler: PyutUIV2 = treeNotebookHandler

    def getFileHandling(self):  # -> TreeNotebookHandler:
        """
        Returns:  the FileHandling class
        """
        return self._treeNotebookHandler

    def registerAppPath(self, path: str):
        """
        Register the path of the application files.

        Args:
            path:
        """
        self._appPath = path

    def registerAppFrame(self, appFrame: Frame):
        """
        Register the application's main frame.

        Args:
            appFrame:  Application's main frame
        """
        self._appFrame = appFrame
        if self._toolboxOwner is None:
            self._toolboxOwner = ToolboxOwner(appFrame)

    def registerToolBar(self, tb: ToolBar):
        """
        Register the toolbar.

        Args:
            tb: The toolbar
        """
        self._toolBar = tb

    def registerToolBarTools(self, tools: List[wxNewIdRef]):
        """
        Register the toolbar tools.

        Args:
            tools:  a list of the tools IDs
        """
        self._tools = tools

    def registerClassEditor(self, classEditor: Callable):
        """
        Register a function to invoke a class editor.

        Args:
            classEditor: This function takes one parameter, the pyutClass to edit.
        """
        self.classEditor = classEditor

    def registerTool(self, tool):
        """
        Add a tool to a toolbox

        Args:
            tool:  The tool to add

        """
        self._toolboxOwner.registerTool(tool)

    def standardClassEditor(self, thePyutClass: PyutClass):
        """
        The standard class editor dialog, for registerClassEditor.

        Args:
            thePyutClass:  the class to edit (data model)
        """
        umlFrame = self._treeNotebookHandler.currentFrame
        if umlFrame is None:
            return
        dlg = DlgEditClass(umlFrame, ID_ANY, thePyutClass)
        dlg.ShowModal()
        dlg.Destroy()

    def autoResize(self, obj: Union[PyutClass, "OglClass"]):
        """
        Auto-resize the given object.

        @param obj

        Notes: Don't really like methods with signatures likes this;  Where the input parameter
        can be one of two things;  I suspect this is some legacy thing;  When I become more
        familiar with the code base I need to fix this.   Humberto
        """
        from ogl.OglClass import OglClass
        prefs: PyutPreferences = PyutPreferences()

        if prefs.autoResizeShapesOnEdit is True:
            if isinstance(obj, PyutClass):
                po = [po for po in self.getUmlObjects() if isinstance(po, OglClass) and po.pyutObject is obj]
                obj = po[0]

            obj.autoResize()

    def getUmlObjects(self) -> 'UmlObjects':
        """
        May be empty

        Returns: Return the list of UmlObjects in the diagram.
        """
        from org.pyut.ui.umlframes.UmlFrame import UmlObjects

        if self._treeNotebookHandler is None:
            return UmlObjects([])
        umlFrame = self._treeNotebookHandler.currentFrame
        if umlFrame is not None:
            return cast(UmlObjects, umlFrame.getUmlObjects())
        else:
            return UmlObjects([])

    def getSelectedShapes(self):
        """
        Return the list of selected OglObjects in the diagram.

        Returns:  May be empty
        """
        umlObjects = self.getUmlObjects()
        if umlObjects is not None:
            selectedObjects = []
            for obj in self.getUmlObjects():
                if obj.IsSelected():
                    selectedObjects.append(obj)

            return selectedObjects
        else:
            return []

    def getDiagram(self) -> Diagram:
        """
        Return the uml diagram.

        Returns: The active uml diagram if present, None otherwise
        """

        umlFrame = self._treeNotebookHandler.currentFrame
        if umlFrame is None:
            return cast(Diagram, None)
        return umlFrame.getDiagram()

    def showParams(self, theNewValue: bool):
        """
        Globally choose whether to show the method parameters in classes

        Args:
            theNewValue:
        """
        if theNewValue is True:
            PyutMethod.setStringMode(DisplayMethodParameters.WITH_PARAMETERS)
        else:
            PyutMethod.setStringMode(DisplayMethodParameters.WITHOUT_PARAMETERS)

    def getCurrentDir(self) -> str:
        """
        Return the application's current directory

        Returns:  application's current directory
        """
        currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()

        return currentDirectoryHandler.currentDirectory

    def setCurrentDir(self, directory: str):
        """
        Set the application's current directory

        Args:
            directory:  New application current directory
        """
        currentDirectoryHandler: CurrentDirectoryHandler = CurrentDirectoryHandler()
        currentDirectoryHandler.currentDirectory = directory

    def displayToolbox(self, category):
        """
        Display a toolbox

        Args:
            category:  The tool category to display
        """
        self._toolboxOwner.displayToolbox(category)

    def getToolboxesCategories(self) -> CategoryNames:
        """
        Return all toolbox categories

        Returns:  The category names
        """
        return self._toolboxOwner.getCategories()

    def getOglClass(self, pyutClass) -> OglClass:
        """
        Return an OGLClass instance corresponding to a pyutClass

        Args:
            pyutClass: The pyutClass we must match to get OGLClass

        Returns: The appropriate OGLClass
        """
        po = [po for po in self.getUmlObjects() if isinstance(po, OglClass) and po.pyutObject is pyutClass]

        if len(po) == 0:
            return cast(OglClass, None)
        else:
            return po[0]

    def createDocument(self, diagramType: DiagramType):
        return self._treeNotebookHandler.newDocument(diagramType)
