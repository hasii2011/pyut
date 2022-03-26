
from typing import Callable
from typing import Dict
from typing import Union

from wx import CENTRE
from wx import WXK_DELETE
from wx import WXK_INSERT
from wx import WXK_BACK

from wx import ID_OK
from wx import ID_NO

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import KeyEvent

from wx import TextEntryDialog

from wx import Yield as wxYield

from org.pyut.dialogs.textdialogs.DlgEditText import DlgEditText

from org.pyut.miniogl.Constants import EVENT_PROCESSED
from org.pyut.miniogl.Constants import SKIP_EVENT
from org.pyut.miniogl.LinePoint import LinePoint
from org.pyut.miniogl.ControlPoint import ControlPoint
from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint

from org.pyut.enums.AttachmentPoint import AttachmentPoint
from org.pyut.enums.LinkType import LinkType

from org.pyut.model.DisplayMethodParameters import DisplayMethodParameters
from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutText import PyutText

from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglText import OglText
from org.pyut.ogl.OglClass import OglClass

from org.pyut.dialogs.DlgEditClass import *         # Have to do this to avoid cyclical dependency
from org.pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from org.pyut.dialogs.DlgEditUseCase import DlgEditUseCase
from org.pyut.dialogs.DlgEditLink import DlgEditLink
from org.pyut.dialogs.DlgRemoveLink import DlgRemoveLink
from org.pyut.dialogs.DlgEditInterface import DlgEditInterface

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.ui.UmlFrameShapeHandler import UmlFrameShapeHandler

from org.pyut.ui.tools.ToolboxOwner import ToolboxOwner

# noinspection PyProtectedMember
from org.pyut.general.Globals import _
from org.pyut.general.PyutVersion import PyutVersion
from org.pyut.general.Singleton import Singleton

from org.pyut.preferences.PyutPreferences import PyutPreferences

__PyUtVersion__ = PyutVersion.getPyUtVersion()

# an enum of the supported actions
# TODO make real enumerations
[
    ACTION_SELECTOR,
    ACTION_NEW_CLASS,                   # 1
    ACTION_NEW_ACTOR,                   # 2
    ACTION_NEW_USECASE,                 # 3
    ACTION_NEW_NOTE,                    # 4
    ACTION_NEW_IMPLEMENT_LINK,          # 5
    ACTION_NEW_INTERFACE,               # 6
    ACTION_NEW_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK,
    ACTION_NEW_TEXT,

    ACTION_DEST_IMPLEMENT_LINK,
    ACTION_DEST_INHERIT_LINK,
    ACTION_DEST_AGGREGATION_LINK,
    ACTION_DEST_COMPOSITION_LINK,
    ACTION_DEST_ASSOCIATION_LINK,
    ACTION_DEST_NOTE_LINK,
    ACTION_NEW_SD_INSTANCE,
    ACTION_NEW_SD_MESSAGE,
    ACTION_DEST_SD_MESSAGE,
    ACTION_ZOOM_IN,
    ACTION_ZOOM_OUT
] = range(24)

# a table of the next action to select
NEXT_ACTION = {
    ACTION_SELECTOR:    ACTION_SELECTOR,
    ACTION_NEW_CLASS:   ACTION_SELECTOR,
    ACTION_NEW_NOTE:    ACTION_SELECTOR,
    ACTION_NEW_IMPLEMENT_LINK:      ACTION_DEST_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK:        ACTION_DEST_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK:    ACTION_DEST_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK:    ACTION_DEST_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK:    ACTION_DEST_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK:           ACTION_DEST_NOTE_LINK,
    ACTION_DEST_IMPLEMENT_LINK:             ACTION_SELECTOR,

    ACTION_DEST_INHERIT_LINK:     ACTION_SELECTOR,
    ACTION_DEST_AGGREGATION_LINK: ACTION_SELECTOR,
    ACTION_DEST_COMPOSITION_LINK: ACTION_SELECTOR,
    ACTION_DEST_ASSOCIATION_LINK: ACTION_SELECTOR,
    ACTION_DEST_NOTE_LINK:  ACTION_SELECTOR,
    ACTION_NEW_ACTOR:       ACTION_SELECTOR,
    ACTION_NEW_USECASE:     ACTION_SELECTOR,

    ACTION_NEW_SD_INSTANCE: ACTION_SELECTOR,
    ACTION_NEW_SD_MESSAGE:  ACTION_DEST_SD_MESSAGE,

    ACTION_ZOOM_IN: ACTION_ZOOM_IN
}

# list of actions which are source events
SOURCE_ACTIONS = [
    ACTION_NEW_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK,
    ACTION_NEW_SD_MESSAGE,
]
# list of actions which are destination events
DEST_ACTIONS = [
    ACTION_DEST_IMPLEMENT_LINK,
    ACTION_DEST_INHERIT_LINK,
    ACTION_DEST_AGGREGATION_LINK,
    ACTION_DEST_COMPOSITION_LINK,
    ACTION_DEST_ASSOCIATION_LINK,
    ACTION_DEST_NOTE_LINK,
    ACTION_DEST_SD_MESSAGE,
    ACTION_ZOOM_IN,     # Patch from D.Dabrowsky, 20060129
    ACTION_ZOOM_OUT     # Patch from D.Dabrowsky, 20060129
]

# OglLink enumerations according to the current action
LINK_TYPE = {
    ACTION_DEST_IMPLEMENT_LINK:     LinkType.INTERFACE,
    ACTION_DEST_INHERIT_LINK:       LinkType.INHERITANCE,
    ACTION_DEST_AGGREGATION_LINK:   LinkType.AGGREGATION,
    ACTION_DEST_COMPOSITION_LINK:   LinkType.COMPOSITION,
    ACTION_DEST_ASSOCIATION_LINK:   LinkType.ASSOCIATION,
    ACTION_DEST_NOTE_LINK:          LinkType.NOTELINK,
    ACTION_DEST_SD_MESSAGE:         LinkType.SD_MESSAGE,
}

# messages for the status bar
a = "Click on the source class"
b = "Now, click on the destination class"

MESSAGES = {
    ACTION_SELECTOR:    "Ready",
    ACTION_NEW_CLASS:   "Click where you want to put the new class",
    ACTION_NEW_NOTE:    "Click where you want to put the new note",
    ACTION_NEW_ACTOR:   "Click where you want to put the new actor",
    ACTION_NEW_TEXT:    'Click where you want to put the new text',
    ACTION_NEW_USECASE: "Click where you want to put the new use case",
    ACTION_NEW_SD_INSTANCE: "Click where you want to put the new instance",
    ACTION_NEW_SD_MESSAGE:  "Click inside the lifeline for the new message",
    ACTION_DEST_SD_MESSAGE: "Click inside the lifeline for the destination of the message",
    ACTION_NEW_IMPLEMENT_LINK:   a,
    ACTION_NEW_INHERIT_LINK:     a,
    ACTION_NEW_AGGREGATION_LINK: a,
    ACTION_NEW_COMPOSITION_LINK: a,
    ACTION_NEW_ASSOCIATION_LINK: a,
    ACTION_NEW_NOTE_LINK:        a,
    ACTION_DEST_IMPLEMENT_LINK: b,
    ACTION_DEST_INHERIT_LINK:   b,
    ACTION_DEST_AGGREGATION_LINK: b,
    ACTION_DEST_COMPOSITION_LINK: b,
    ACTION_DEST_ASSOCIATION_LINK: b,
    ACTION_DEST_NOTE_LINK: b,
    ACTION_ZOOM_IN:     "Select the area to fit on",
    ACTION_ZOOM_OUT:    "Select the central point",

}

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
    `ACTION_DEST_NOTE_LINK` this way::

        nextAction = NEXT_ACTION[ACTION_NEW_NOTE_LINK]

    The state is kept in `self._currentAction`.

    The `doAction` is called whenever a click is received by the UML diagram
    frame.
    """
    def init(self):
        """
        Singleton constructor.

        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        @modified C.Dutoit 20021121 Added self._project
        """
        self.logger: Logger = getLogger(__name__)

        from org.pyut.errorcontroller.ErrorManager import ErrorManager

        self._errorManager: ErrorManager  = ErrorManager()

        self._currentAction = ACTION_SELECTOR
        self._useMode       = NORMAL_MODE   # Define current use mode
        self._currentActionPersistent = False

        self._toolBar  = None   # toolbar
        self._tools    = None   # toolbar tools
        self._status   = None   # application status bar
        self._src      = None   # source of a two-objects action
        self._dst      = None   # destination of a two-objects action
        self._appFrame = None   # Application's main frame
        self._appPath  = None   # Application files' path

        self.registerClassEditor(self.standardClassEditor)
        self._toolboxOwner = None   # toolbox owner, created when application frame is passed
        self._treeNotebookHandler = None

        self._modifyCommand = None  # command for undo/redo a modification on a shape.

    def setScriptMode(self):
        """
        Define the script mode, to use PyUt without graphical elements
        """
        self._useMode = SCRIPT_MODE

    def isInScriptMode(self) -> bool:
        """
        True if the current mode is the scripting mode
        """
        return self._useMode == SCRIPT_MODE

    def getErrorManager(self):
        """
        Return the current error manager

        @author C.Dutoit
        """
        return self._errorManager

    def getAppPath(self):
        """
        Return the path of the application files.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._appPath

    def getAppFrame(self):
        """
        """
        return self._appFrame

    def registerFileHandling(self, treeNotebookHandler):
        """
        Register the main part of the user interface
        """
        self._treeNotebookHandler = treeNotebookHandler

    def getFileHandling(self):  # -> TreeNotebookHandler:
        """
        Returns:  the FileHandling class
        """
        return self._treeNotebookHandler

    def registerAppPath(self, path: str):
        """
        Register the path of the application files.

        @param path
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._appPath = path

    def registerAppFrame(self, appFrame):
        """
        Register the application's main frame.

        @param wxFrame appFrame : Application's main frame
        @since 1.27.2.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._appFrame = appFrame
        if self._toolboxOwner is None:
            self._toolboxOwner = ToolboxOwner(appFrame)

    def registerToolBar(self, tb):
        """
        Register the toolbar.

        @param wxToolbar tb : the toolbar
        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        """
        self._toolBar = tb

    def registerToolBarTools(self, tools):
        """
        Register the toolbar tools.

        @param int[] tools : a list of the tools IDs
        @author L. Burgbacher
        """
        self._tools = tools

    def registerStatusBar(self, statusBar):
        """
        Register the status bar.

        @param wxStatusBar statusBar : the status bar
        @author L. Burgbacher
        """
        self._status = statusBar

    def registerClassEditor(self, classEditor):
        """
        Register a function to invoke a class editor.
        This function takes one parameter, the pyutClass to edit.

        @param classEditor  PyutClass
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self.classEditor = classEditor

    def registerTool(self, tool):
        """
        Add a tool to a toolbox

        Args:
            tool:  The tool to add

        """
        self._toolboxOwner.registerTool(tool)

    # TODO this is an unused method.  Note the bad plugin name
    def fastTextClassEditor(self, thePyutClass: PyutClass):
        plugs = self._appFrame.plugs
        cl = [s for s in plugs.values() if s(None, None).name == "Fast text edition"]
        if cl:
            obj = cl[0](self.getUmlObjects(), self.getUmlFrame())
        else:
            # fallback
            self.standardClassEditor(thePyutClass)
            return

        # Do plugin functionality
        BeginBusyCursor()
        obj.callDoAction()
        EndBusyCursor()
        self.getUmlFrame().Refresh()

    def standardClassEditor(self, thePyutClass: PyutClass):
        """
        The standard class editor dialog, for registerClassEditor.

        Args:
            thePyutClass:  the class to edit (data model)
        """
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        dlg = DlgEditClass(umlFrame, ID_ANY, thePyutClass)
        dlg.ShowModal()
        dlg.Destroy()

    def setCurrentAction(self, action: int):
        """
        TODO make actions enumerations
        Set the new current action.
        This tells the mediator which action to do for the next doAction call.

        Args:
            action:  the action from ACTION constants

        Returns:

        """
        self.logger.debug(f'Set current action to: {action}')
        if self._currentAction == action:
            self._currentActionPersistent = True
        else:
            self._currentAction = action
            self._currentActionPersistent = False

        self.setStatusText(MESSAGES[self._currentAction])

    def doAction(self, x: int, y: int):
        """
        Do the current action at coordinates x, y.

        Args:
            x: x coord where the action must take place
            y: y coord where the action must take place
        """
        self.logger.debug(f'doAction: {self._currentAction}  ACTION_SELECTOR: {ACTION_SELECTOR}')
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        self.resetStatusText()
        if self._currentAction == ACTION_SELECTOR:
            return SKIP_EVENT
        elif self._currentAction == ACTION_NEW_CLASS:
            self.createOglClass(umlFrame=umlFrame, x=x, y=y)
        elif self._currentAction == ACTION_NEW_TEXT:
            self._createNewText(umlFrame, x, y)
        elif self._currentAction == ACTION_NEW_NOTE:
            self._createNewNote(umlFrame, x, y)
        elif self._currentAction == ACTION_NEW_ACTOR:
            pyutActor = umlFrame.createNewActor(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
            dlg = TextEntryDialog(umlFrame, "Actor name", "Enter actor name", pyutActor.name, OK | CANCEL | CENTRE)

            if dlg.ShowModal() == ID_OK:
                pyutActor.name = dlg.GetValue()
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_USECASE:
            pyutUseCase = umlFrame.createNewUseCase(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
            dlg = DlgEditUseCase(umlFrame, -1, pyutUseCase)
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_SD_INSTANCE:
            try:
                from org.pyut.ui.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
                if not isinstance(umlFrame, UmlSequenceDiagramsFrame):
                    PyutUtils.displayError(_("A SD INSTANCE can't be added to a class diagram. You must create a sequence diagram."))
                    return
                instance = umlFrame.createNewSDInstance(x, y)
                if not self._currentActionPersistent:
                    self._currentAction = ACTION_SELECTOR
                    self.selectTool(self._tools[0])

                dlg = TextEntryDialog(umlFrame, "Instance name", "Enter instance name", instance.getInstanceName(), OK | CANCEL | CENTRE)

                if dlg.ShowModal() == ID_OK:
                    instance.setInstanceName(dlg.GetValue())
                dlg.Destroy()
                umlFrame.Refresh()
            except (ValueError, Exception) as e:
                PyutUtils.displayError(_(f"An error occurred while trying to do this action {e}"))
                umlFrame.Refresh()
        elif self._currentAction == ACTION_ZOOM_IN:
            return SKIP_EVENT
        elif self._currentAction == ACTION_ZOOM_OUT:
            umlFrame.DoZoomOut(x, y)
            umlFrame.Refresh()
            self.updateTitle()
        else:
            return SKIP_EVENT
        return EVENT_PROCESSED

    def actionWaiting(self):
        """
        Return True if there's an action waiting to be completed.

        @since 1.2
        @author L. Burgbacher <lb@alawa.ch>
        """
        return self._currentAction != ACTION_SELECTOR

    def selectTool(self, ID):
        """
        Select the tool of given ID from the toolbar, and deselect the others.

        @since 1.9
        @author L. Burgbacher <lb@alawa.ch>
        """
        for toolId in self._tools:
            self._toolBar.ToggleTool(toolId, False)
        self._toolBar.ToggleTool(ID, True)

    def shapeSelected(self, shape, position=None):
        """
        Do action when a shape is selected.
        TODO : support each link type
        """
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return

        # do the right action
        if self._currentAction in SOURCE_ACTIONS:
            self.logger.debug(f'Current action in source actions')
            # get the next action needed to complete the whole action
            if self._currentActionPersistent:
                self._oldAction = self._currentAction
            self._currentAction = NEXT_ACTION[self._currentAction]

            # if no source, cancel action
            if shape is None:
                self.logger.info("Action cancelled (no source)")
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
                self.setStatusText(_("Action cancelled"))
            else:   # store source
                self.logger.debug(f'Store source - shape {shape}  position: {position}')
                self._src    = shape
                self._srcPos = position
        elif self._currentAction in DEST_ACTIONS:
            self.logger.debug(f'Current action in destination actions')
            # store the destination object
            self._dst    = shape
            self._dstPos = position
            # if no destination, cancel action
            if self._dst is None:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
                self.setStatusText(_("Action cancelled"))
                return
            self._createLink(umlFrame)

            if self._currentActionPersistent:
                self._currentAction = self._oldAction
                del self._oldAction
            else:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
        else:
            self.setStatusText(_("Error : Action not supported by the mediator"))
            return
        self.setStatusText(MESSAGES[self._currentAction])

    def autoResize(self, obj: Union[PyutClass, "OglClass"]):
        """
        Auto-resize the given object.

        @param obj

        Notes: Don't really like methods with signatures likes this;  Where the input parameter
        can be one of two things;  I suspect this is some legacy thing;  When I become more
        familiar with the code base I need to fix this.   Humberto
        """
        from org.pyut.ogl.OglClass import OglClass
        prefs: PyutPreferences = PyutPreferences()

        if prefs.autoResizeShapesOnEdit is True:
            if isinstance(obj, PyutClass):
                po = [po for po in self.getUmlObjects() if isinstance(po, OglClass) and po.pyutObject is obj]
                obj = po[0]

            obj.autoResize()

    def editObject(self, x, y):
        """
        Edit the object at x, y.
        """
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        #
        # TODO I don't like in-line imports but moving them to top file causes a cyclic dependency error
        #
        from org.pyut.ogl.OglClass import OglClass
        from org.pyut.ogl.OglNote import OglNote
        from org.pyut.ogl.OglUseCase import OglUseCase
        from org.pyut.ogl.OglActor import OglActor
        from org.pyut.ogl.OglAssociation import OglAssociation
        from org.pyut.ogl.OglInterface import OglInterface

        from org.pyut.model.PyutNote import PyutNote

        diagramShape = umlFrame.FindShape(x, y)

        if diagramShape is None:
            return

        if isinstance(diagramShape, OglClass):
            pyutObject = diagramShape.pyutObject
            self.classEditor(pyutObject)
            self.autoResize(diagramShape)
        elif isinstance(diagramShape, OglInterface2):

            self.logger.info(f'Double clicked on lollipop')
            lollipop:      OglInterface2 = cast(OglInterface2, diagramShape)
            pyutInterface: PyutInterface = lollipop.pyutInterface
            with DlgEditInterface(umlFrame, ID_ANY, pyutInterface) as dlg:
                if dlg.ShowModal() == OK:
                    self.logger.info(f'model: {pyutInterface}')
                else:
                    self.logger.info(f'Cancelled')

        elif isinstance(diagramShape, OglText):
            oglText:  OglText  = cast(OglText, diagramShape)
            pyutText: PyutText = oglText.pyutText

            self.logger.info(f'Double clicked on {oglText}')

            dlg: DlgEditText = DlgEditText(parent=umlFrame, dialogIdentifier=ID_ANY, pyutText=pyutText)
            dlg.ShowModal()
            dlg.Destroy()

        elif isinstance(diagramShape, OglNote):
            pyutObject = diagramShape.pyutObject
            dlg: DlgEditNote = DlgEditNote(umlFrame, ID_ANY, cast(PyutNote, pyutObject))
            dlg.ShowModal()
            dlg.Destroy()
        elif isinstance(diagramShape, OglUseCase):
            pyutObject = diagramShape.pyutObject
            dlg: DlgEditUseCase = DlgEditUseCase(umlFrame, ID_ANY, pyutObject)
            dlg.Destroy()
        elif isinstance(diagramShape, OglActor):
            pyutObject = diagramShape.pyutObject
            dlg: TextEntryDialog = TextEntryDialog(umlFrame, "Actor name", "Enter actor name", pyutObject.name, OK | CANCEL | CENTRE)
            if dlg.ShowModal() == ID_OK:
                pyutObject.setName(dlg.GetValue())
            dlg.Destroy()
        elif isinstance(diagramShape, OglAssociation):
            dlg: DlgEditLink = DlgEditLink(None, ID_ANY, diagramShape.pyutObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            dlg.Destroy()
            if rep == -1:    # destroy link
                diagramShape.Detach()
        elif isinstance(diagramShape, OglInterface):
            dlg: DlgEditLink = DlgEditLink(None, ID_ANY, diagramShape.pyutObject)
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            dlg.Destroy()
            if rep == -1:  # destroy link
                diagramShape.Detach()

        umlFrame.Refresh()

    def getUmlObjects(self):
        """
        Return the list of UmlObjects in the diagram.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        if self._treeNotebookHandler is None:
            return []
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is not None:
            return umlFrame.getUmlObjects()
        else:
            return []

    def getSelectedShapes(self):
        """
        Return the list of selected OglObjects in the diagram.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
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

    def setStatusText(self, msg: str):
        """
        Set the text in the status bar.
        Args:
            msg:    The message to put in the status bar
        """
        if msg is not None:
            self._status.SetStatusText(msg)

    def resetStatusText(self):
        """
        Reset the text in the status bar.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        self._status.SetStatusText(_("Ready"))

    def getDiagram(self):
        """
        Return the uml diagram.

        @since 1.12
        @return uml diagram if present, None otherwise
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return None
        return umlFrame.getDiagram()

    def getUmlFrame(self):
        """
        Return the active uml frame.

        @return UmlFrame
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._treeNotebookHandler.getCurrentFrame()

    def deselectAllShapes(self):
        """
        Deselect all shapes in the current diagram.
        """
        self._setShapeSelection(False)

    def selectAllShapes(self):
        """
        Select all shapes in the current diagram.
        """
        self._setShapeSelection(True)

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

    def processChar(self, event: KeyEvent):
        """
        Process the keyboard events.
        TODO:  Build the callable dictionary once and use it here.  This code builds it every time the
        user presses a key.  Eeks;

        Args:
            event:  The wxPython key event
        """
        c: int = event.GetKeyCode()
        funcs: Dict[int, Callable] = {
            WXK_DELETE: self.deleteSelectedShape,
            WXK_BACK:   self.deleteSelectedShape,
            WXK_INSERT: self.insertSelectedShape,
            ord('i'):   self.insertSelectedShape,
            ord('I'):   self.insertSelectedShape,
            ord('s'):   self.toggleSpline,
            ord('S'):   self.toggleSpline,
            ord('<'):   self.moveSelectedShapeDown,
            ord('>'):   self.moveSelectedShapeUp,
        }
        if c in funcs:
            funcs[c]()
        else:
            self.logger.warning(f'Key code not supported: {c}')
            event.Skip()

    def createOglClass(self, umlFrame, x: int, y: int):

        from org.pyut.history.commands.CreateOglClassCommand import CreateOglClassCommand
        from org.pyut.history.commands.CommandGroup import CommandGroup

        cmd:   CreateOglClassCommand = CreateOglClassCommand(x, y)
        group: CommandGroup          = CommandGroup("Create class")
        group.addCommand(cmd)
        umlFrame.getHistory().addCommandGroup(group)
        umlFrame.getHistory().execute()

        if not self._currentActionPersistent:
            self._currentAction = ACTION_SELECTOR
            self.selectTool(self._tools[0])

    def deleteSelectedShape(self):
        from org.pyut.history.commands.DeleteOglObjectCommand import DeleteOglObjectCommand
        from org.pyut.history.commands.DeleteOglClassCommand import DeleteOglClassCommand
        from org.pyut.history.commands.DelOglLinkCommand import DelOglLinkCommand
        from org.pyut.ogl.OglClass import OglClass
        from org.pyut.ogl.OglObject import OglObject
        from org.pyut.ogl.OglLink import OglLink
        from org.pyut.history.commands.CommandGroup import CommandGroup

        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        selected     = umlFrame.GetSelectedShapes()
        cmdGroup     = CommandGroup("Delete UML object(s)")
        cmdGroupInit = False  # added by hasii to avoid Pycharm warning about cmdGroupInit not set

        for shape in selected:
            cmd = None
            if isinstance(shape, OglClass):
                cmd = DeleteOglClassCommand(shape)
            elif isinstance(shape, OglObject):
                cmd = DeleteOglObjectCommand(shape)
            elif isinstance(shape, OglLink):
                dlg: DlgRemoveLink = DlgRemoveLink()
                resp = dlg.ShowModal()
                dlg.Destroy()
                if resp == ID_NO:
                    return
                else:
                    cmd = DelOglLinkCommand(shape)

            # if the shape is not an Ogl instance no command has been created.
            if cmd is not None:
                cmdGroup.addCommand(cmd)
                cmdGroupInit = True
            else:
                shape.Detach()
                umlFrame.Refresh()

        if cmdGroupInit:
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            umlFrame.getHistory().execute()

    def insertSelectedShape(self):
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        selected = umlFrame.GetSelectedShapes()
        if len(selected) != 1:
            return
        selected = selected.pop()
        if isinstance(selected, LinePoint):
            px, py = selected.GetPosition()
            # add a control point and make it child of the shape if it's a
            # self link
            line = selected.GetLines()[0]
            if line.GetSource().GetParent() is line.GetDestination().GetParent():
                cp = ControlPoint(0, 0, line.GetSource().GetParent())
                cp.SetPosition(px + 20, py + 20)
            else:
                cp = ControlPoint(px + 20, py + 20)
            line.AddControl(cp, selected)
            umlFrame.GetDiagram().AddShape(cp)
            umlFrame.Refresh()

    def toggleSpline(self):

        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        selected = umlFrame.GetSelectedShapes()
        self.logger.info(f'Selected Shape: {selected}')
        for shape in selected:
            if isinstance(shape, OglLink):
                shape.SetSpline(not shape.GetSpline())
        umlFrame.Refresh()

    def moveSelectedShapeUp(self):
        """
        Move the selected shape one level up in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        self._moveSelectedShapeZOrder(umlFrame.GetDiagram().MoveToFront)

    def moveSelectedShapeDown(self):
        """
        Move the selected shape one level down in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        self._moveSelectedShapeZOrder(umlFrame.GetDiagram().MoveToBack)

    def displayToolbox(self, category):
        """
        Display a toolbox

        @param String category : category of tool to display
        @since 1.3
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._toolboxOwner.displayToolbox(category)

    def getToolboxesCategories(self):
        """
        Return all categories of toolboxes

        @return string[] of categories
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        return self._toolboxOwner.getCategories()

    def getOglClass(self, pyutClass):
        """
        Return an OGLClass instance corresponding to a pyutClass

        @param pyutClass : the pyutClass to get OGLClass
        @return OGLClass
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        from org.pyut.ogl.OglClass import OglClass

        po = [po for po in self.getUmlObjects() if isinstance(po, OglClass) and po.pyutObject is pyutClass]

        if len(po) == 0:
            return None
        else:
            return po[0]

    def updateTitle(self):
        """
        Set the application title, function of version and current filename
        """
        # Exit if we are in scripting mode
        if self.isInScriptMode():
            return

        # Get filename
        project = self._treeNotebookHandler.getCurrentProject()
        if project is not None:
            filename = project.getFilename()
        else:
            filename = ""

        # Set text
        txt = "PyUt v" + __PyUtVersion__ + " - " + filename
        if (project is not None) and (project.getModified()):
            if self._treeNotebookHandler.getCurrentFrame() is not None:
                zoom = self._treeNotebookHandler.getCurrentFrame().GetCurrentZoom()
            else:
                zoom = 1

            txt = txt + f' ( {int(zoom * 100)}%) *'

        self._appFrame.SetTitle(txt)

    def loadByFilename(self, filename):
        """
        Load a file from its filename
        @author C.Dutoit
        """
        self._appFrame.loadByFilename(filename)

    def cutSelectedShapes(self):
        """
        TODO  This event send does not yet work; Fix fix fix
        """

        # self._appFrame.cutSelectedShapes()
        from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

        parent:   Window     = self._appFrame
        cutEvent: CommandEvent = CommandEvent(SharedIdentifiers.ID_MNU_EDIT_CUT)

        wxPostEvent(parent, cutEvent)

    def getCurrentAction(self):
        return self._currentAction

    def requestLollipopLocation(self, destinationClass: OglClass):

        from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

        umlFrame: UmlClassDiagramsFrame = self.getFileHandling().getCurrentFrame()

        self.__createPotentialAttachmentPoints(destinationClass=destinationClass, umlFrame=umlFrame)
        self.setStatusText(f'Select attachment point')
        umlFrame.Refresh()
        wxYield()

    def createLollipopInterface(self, implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame
        from org.pyut.history.commands.CreateOglInterfaceCommand import CreateOglInterfaceCommand
        from org.pyut.history.commands.CommandGroup import CommandGroup

        attachmentAnchor.setYouAreTheSelectedAnchor()

        umlFrame: UmlClassDiagramsFrame = self.getFileHandling().getCurrentFrame()

        cmd: CreateOglInterfaceCommand = CreateOglInterfaceCommand(implementor=implementor, attachmentAnchor=attachmentAnchor)
        group: CommandGroup = CommandGroup("Create lollipop")

        group.addCommand(cmd)
        umlFrame.getHistory().addCommandGroup(group)
        umlFrame.getHistory().execute()

    def _moveSelectedShapeZOrder(self, callback):
        """
        Move the selected shape one level in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        from org.pyut.ogl import OglObject
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is None:
            return
        selected = umlFrame.GetSelectedShapes()
        if len(selected) > 0:
            for oglObject in selected:
                if isinstance(oglObject, OglObject.OglObject):
                    callback(oglObject)
        umlFrame.Refresh()

    def _setShapeSelection(self, selected: bool):
        """
        Either select or deselect all shapes in the current frame

        Args:
            selected: If `True` select all shapes else deselect them
        """
        umlFrame = self._treeNotebookHandler.getCurrentFrame()
        if umlFrame is not None:
            shapes = umlFrame.GetDiagram().GetShapes()
            for shape in shapes:
                shape.SetSelected(selected)
            umlFrame.Refresh()

    def _createLink(self, umlFrame):

        from org.pyut.history.commands.CreateOglLinkCommand import CreateOglLinkCommand
        from org.pyut.history.commands.CommandGroup import CommandGroup

        linkType = LINK_TYPE[self._currentAction]
        cmd = CreateOglLinkCommand(self._src, self._dst, linkType, self._srcPos, self._dstPos)

        cmdGroup = CommandGroup("create link")
        cmdGroup.addCommand(cmd)
        umlFrame.getHistory().addCommandGroup(cmdGroup)
        umlFrame.getHistory().execute()
        self._src = None
        self._dst = None

    def _createNewNote(self, umlFrame: UmlFrameShapeHandler, x: int, y: int):
        """
        Create a note on the diagram

        Args:
            umlFrame:  The UML frame knows how to place the new note on diagram
            x: The x-coordinate
            y: The y-coordinate
        """

        pyutNote: PyutNote = umlFrame.createNewNote(x, y)

        self.__resetToActionSelector()
        dlg: DlgEditNote = DlgEditNote(umlFrame, ID_ANY, pyutNote)
        dlg.ShowModal()
        dlg.Destroy()
        umlFrame.Refresh()

    def _createNewText(self, umlFrame, x: int, y: int):
        """
        Create a text box on the diagram

        Args:
            umlFrame:  The UML frame that knows hot to place the new text object on the diagram
            x: The x-coordinate
            y: The y-coordinate
        """
        pyutText: PyutText = umlFrame.createNewText(x, y)

        self.__resetToActionSelector()
        dlg: DlgEditText = DlgEditText(parent=umlFrame, dialogIdentifier=ID_ANY, pyutText=pyutText)
        dlg.ShowModal()
        dlg.Destroy()
        umlFrame.Refresh()

    def __createPotentialAttachmentPoints(self, destinationClass: OglClass, umlFrame):

        dw, dh     = destinationClass.GetSize()

        southX = dw // 2        # do integer division
        southY = dh
        northX = dw // 2
        northY = 0
        westX  = 0
        westY  = dh // 2
        eastX  = dw
        eastY  = dh // 2

        self.__createAnchorHints(destinationClass, southX, southY, AttachmentPoint.SOUTH, umlFrame)
        self.__createAnchorHints(destinationClass, northX, northY, AttachmentPoint.NORTH, umlFrame)
        self.__createAnchorHints(destinationClass, westX,  westY,  AttachmentPoint.WEST, umlFrame)
        self.__createAnchorHints(destinationClass, eastX,  eastY,  AttachmentPoint.EAST, umlFrame)

    def __createAnchorHints(self, destinationClass: OglClass, anchorX: int, anchorY: int, attachmentPoint: AttachmentPoint, umlFrame):

        anchorHint: SelectAnchorPoint = SelectAnchorPoint(x=anchorX, y=anchorY, attachmentPoint=attachmentPoint, parent=destinationClass)
        anchorHint.SetProtected(True)

        destinationClass.AddAnchorPoint(anchorHint)
        umlFrame.getDiagram().AddShape(anchorHint)

    def __resetToActionSelector(self):
        """
        For non-persistent tools
        """

        if not self._currentActionPersistent:
            self._currentAction = ACTION_SELECTOR
            self.selectTool(self._tools[0])     # TODO need to fix this in case this moves
