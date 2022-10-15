
from typing import TYPE_CHECKING

from wx import Frame
from wx import ToolBar

from wx import NewIdRef as wxNewIdRef

from org.pyut.enums.DiagramType import DiagramType

from miniogl.Diagram import Diagram

from org.pyut.ui.tools.ToolboxTypes import CategoryNames

if TYPE_CHECKING:
    from org.pyut.ui.umlframes.UmlFrame import UmlObjects
    from org.pyut.uiv2.PyutApplicationFrameV2 import PyutApplicationFrameV2

from org.pyut.dialogs.DlgEditClass import *         # Have to do this to avoid cyclical dependency

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler

from org.pyut.ui.tools.ToolboxOwner import ToolboxOwner

from org.pyut.general.Singleton import Singleton

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

        self._useMode       = NORMAL_MODE   # Define current use mode

        self._toolBar  = None   # toolbar
        self._tools    = None   # toolbar tools
        self._appPath  = None   # Application files' path

        self._appFrame: PyutApplicationFrameV2 = cast(PyutApplicationFrameV2, None)   # Application's main frame

        self._toolboxOwner = None   # toolbox owner, created when application frame is passed
        self._treeNotebookHandler = None

    @property
    def activeUmlFrame(self):
        """
        Return the active UML frame.

        Returns:  The UML frame
        """
        return self._treeNotebookHandler.currentFrame

    def getAppPath(self) -> str:
        """
        Return the path of the application files.

        Returns: a string
        """
        return self._appPath

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

    def registerTool(self, tool):
        """
        Add a tool to a toolbox

        Args:
            tool:  The tool to add

        """
        self._toolboxOwner.registerTool(tool)

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
