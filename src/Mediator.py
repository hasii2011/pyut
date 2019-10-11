
from typing import Dict
from typing import Callable

from logging import Logger
from logging import getLogger

from wx import CENTRE
from wx import WXK_DELETE
from wx import WXK_INSERT

from wx import ID_OK

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import KeyEvent

from wx import TextEntryDialog

from MiniOgl.Constants import EVENT_PROCESSED
from MiniOgl.Constants import SKIP_EVENT

from MiniOgl import LinePoint
from MiniOgl import ControlPoint

from org.pyut.ogl.OglLink import OglLink

from PyutConsts import OGL_INTERFACE
from PyutConsts import OGL_INHERITANCE
from PyutConsts import OGL_AGGREGATION
from PyutConsts import OGL_ASSOCIATION
from PyutConsts import OGL_COMPOSITION
from PyutConsts import OGL_NOTELINK
from PyutConsts import OGL_SD_MESSAGE

from PyutMethod import WITHOUT_PARAMS
from PyutMethod import WITH_PARAMS
from PyutPreferences import PyutPreferences
from pyutUtils import displayError

from org.pyut.dialogs.DlgEditClass import *         # Have to do this to avoid cyclical dependency
from org.pyut.dialogs.DlgEditNote import DlgEditNote
from org.pyut.dialogs.DlgEditUseCase import DlgEditUseCase
from org.pyut.dialogs.DlgEditLink import DlgEditLink

from PyutVersion import getPyUtVersion
from Singleton import Singleton
from ToolboxOwner import ToolboxOwner

from globals import _

__PyUtVersion__ = getPyUtVersion()

# an enum of the supported actions
# TODO make real enumerations
[
    ACTION_SELECTOR,
    ACTION_NEW_CLASS,
    ACTION_NEW_ACTOR,
    ACTION_NEW_USECASE,
    ACTION_NEW_NOTE,
    ACTION_NEW_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK,
    ACTION_DEST_IMPLEMENT_LINK,
    ACTION_DEST_INHERIT_LINK,
    ACTION_DEST_AGGREGATION_LINK,
    ACTION_DEST_COMPOSITION_LINK,
    ACTION_DEST_ASSOCIATION_LINK,
    ACTION_DEST_NOTE_LINK,
    ACTION_NEW_SD_INSTANCE,
    ACTION_NEW_SD_MESSAGE,
    ACTION_DEST_SD_MESSAGE,
    ACTION_ZOOM_IN,  # Patch from D.Dabrowsky, 20060129
    ACTION_ZOOM_OUT  # Patch from D.Dabrowsky, 20060129
] = range(22)

# a table of the next action to select
NEXT_ACTION = {
    ACTION_SELECTOR: ACTION_SELECTOR,
    ACTION_NEW_CLASS: ACTION_SELECTOR,
    ACTION_NEW_NOTE: ACTION_SELECTOR,
    ACTION_NEW_IMPLEMENT_LINK: ACTION_DEST_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK: ACTION_DEST_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK: ACTION_DEST_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK: ACTION_DEST_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK: ACTION_DEST_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK: ACTION_DEST_NOTE_LINK,
    ACTION_DEST_IMPLEMENT_LINK: ACTION_SELECTOR,
    ACTION_DEST_INHERIT_LINK: ACTION_SELECTOR,
    ACTION_DEST_AGGREGATION_LINK: ACTION_SELECTOR,
    ACTION_DEST_COMPOSITION_LINK: ACTION_SELECTOR,
    ACTION_DEST_ASSOCIATION_LINK: ACTION_SELECTOR,
    ACTION_DEST_NOTE_LINK: ACTION_SELECTOR,
    ACTION_NEW_ACTOR: ACTION_SELECTOR,
    ACTION_NEW_USECASE: ACTION_SELECTOR,

    ACTION_NEW_SD_INSTANCE: ACTION_SELECTOR,
    ACTION_NEW_SD_MESSAGE: ACTION_DEST_SD_MESSAGE,
    ACTION_ZOOM_IN: ACTION_ZOOM_IN,     # Patch from D.Dabrowsky, 20060129
    # ACTION_ZOOM_IN: ACTION_ZOOM_OUT,    # Patch from D.Dabrowsky, 20060129    Duplicated
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

# OglLink constants according to the current action
LINK_TYPE = {
    ACTION_DEST_IMPLEMENT_LINK: OGL_INTERFACE,
    ACTION_DEST_INHERIT_LINK: OGL_INHERITANCE,
    ACTION_DEST_AGGREGATION_LINK: OGL_AGGREGATION,
    ACTION_DEST_COMPOSITION_LINK: OGL_COMPOSITION,
    ACTION_DEST_ASSOCIATION_LINK: OGL_ASSOCIATION,
    ACTION_DEST_NOTE_LINK: OGL_NOTELINK,
    ACTION_DEST_SD_MESSAGE: OGL_SD_MESSAGE,
}

# messages for the status bar
a = "Click on the source class"
b = "Now, click on the destination class"

MESSAGES = {
    ACTION_SELECTOR:    "Ready",
    ACTION_NEW_CLASS:   "Click where you want to put the new class",
    ACTION_NEW_NOTE:    "Click where you want to put the new note",
    ACTION_NEW_ACTOR:   "Click where you want to put the new actor",
    ACTION_NEW_USECASE: "Click where you want to put the new use case",
    ACTION_NEW_SD_INSTANCE: "Click where you want to put the new instance",
    ACTION_NEW_SD_MESSAGE:  "Click where you want to put the new message",
    ACTION_DEST_SD_MESSAGE: "Click on the destination of the message",
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
[SCRIPT_MODE, NORMAL_MODE] = assignID(2)


def getMediator():
    """
    Factory function to get the unique Mediator instance (singleton).

    @since 1.0
    @author L. Burgbacher <lb@alawa.ch>
    """
    return Mediator()


class Mediator(Singleton):
    """
    This class is the link between the parts of the GUI of pyut. It receives
    commands from the modules, and dispatch them to the right receiver.
    See the Model-View-Controller pattern and the Mediator pattern.
    There's just one instance of it, and it's global. You get the only
    instance by instantiating it. See the `singleton.py` file for more
    information about this.

    Each part of the GUI must register itself to the mediator. This is done
    with the various `register...` methods.

    The mediator contains a state machine. The different states are
    represented by integer constants, declared at the beginning of the
    `mediator.py` file. These are the `ACTION_*` constants.

    The `NEXT_ACTION` dictionary gives the next action based on the given
    one. For example, after an `ACTION_NEW_NOTE_LINK`, you get an
    `ACTION_DEST_NOTE_LINK` this way::

        nextAction = NEXT_ACTION[ACTION_NEW_NOTE_LINK]

    The state is kept in `self._currentAction`.

    The `doAction` is called whenever a click is received by the uml diagram
    frame.

    :author: Laurent Burgbacher
    :contact: <lb@alawa.ch>
    :version: $Revision: 1.38 $
    """
    def init(self):
        """
        Singleton constructor.

        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        @modified C.Dutoit 20021121 Added self._project
        """
        import ErrorManager
        self._errorManager  = ErrorManager.getErrorManager()
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
        self._toolboxOwner = None   # toolbox owner, created when appframe is passed
        self._fileHandling = None   # File Handler
        # self.registerClassEditor(self.fastTextClassEditor)
        # Patch from D.Dabrowsky, 20060129
        self._modifyCommand = None  # command for undo/redo a modification on a shape.

        self.logger: Logger = getLogger(__name__)

    def setScriptMode(self):
        """
        Define the script mode, to use PyUt without graphical elements
        @author C.Dutoit
        """
        self._useMode = SCRIPT_MODE

    def isInScriptMode(self):
        """
        True if the current mode is the scripting mode
        @author C.Dutoit
        """
        return self._useMode == SCRIPT_MODE

    def getErrorManager(self):
        """
        Return the current error manager

        @author C.Dutoit
        """
        return self._errorManager

    def registerFileHandling(self, fh):
        """
        Define the file handling class

        @param fh : The FileHandling class to be used
        @author C.Dutoit
        """
        self._fileHandling = fh

    def registerAppPath(self, path: str):
        """
        Register the path of the application files.

        @param path
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._appPath = path

    def getAppPath(self):
        """
        Return the path of the application files.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._appPath

    def notifyTitleChanged(self):
        """
        Notify appframe that the application title has changed

        @since 1.27.2.23
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if self._appFrame is not None:
            self._appFrame.notifyTitleChanged()

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

    def getAppFrame(self):
        """
        """
        return self._appFrame

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

    def fastTextClassEditor(self, thePyutClass: PyutClass):
        plugs = self._appFrame.plugs
        cl = [s for s in plugs.values() if s(None, None).getName() == "Fast text edition"]
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
        The standard class editor dialogue, for registerClassEditor.

        @param  thePyutClass : the class to edit
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return
        dlg = DlgEditClass(umlFrame, -1, thePyutClass)
        dlg.Destroy()

    def registerClassEditor(self, classEditor):
        """
        Register a function to invoque a class editor.
        This function takes one parameter, the pyutClass to edit.

        @param classEditor  PyutClass)
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self.classEditor = classEditor

    def setCurrentAction(self, action: int):
        """
        TODO make actions enumerations

        Set the new current atction.
        This tells the mediator which action to do for the next doAction call.

        @param action : the action from ACTION constants
        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        """
        if self._currentAction == action:
            self._currentActionPersistent = True
        else:
            self._currentAction = action
            self._currentActionPersistent = False
        # put a message in the status bar
        self.setStatusText(MESSAGES[self._currentAction])

    def doAction(self, x, y):
        """
        Do the current action at coordinates x, y.

        @param int x : x coord where the action must take place
        @param int y : y coord where the action must take place
        @since 1.0
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return
        self.resetStatusText()
        if self._currentAction == ACTION_SELECTOR:
            return SKIP_EVENT
        elif self._currentAction == ACTION_NEW_CLASS:
            from org.pyut.commands.CreateOglClassCommand import CreateOglClassCommand
            from org.pyut.commands.CommandGroup import CommandGroup
            cmd = CreateOglClassCommand(x, y, True)
            group = CommandGroup("Create class")
            group.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(group)
            umlFrame.getHistory().execute()

            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
        elif self._currentAction == ACTION_NEW_NOTE:
            pyutNote = umlFrame.createNewNote(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
            dlg = DlgEditNote(umlFrame, -1, pyutNote)
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_ACTOR:
            pyutActor = umlFrame.createNewActor(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
            dlg = TextEntryDialog(umlFrame, "Actor name", "Enter actor name", pyutActor.getName(), OK | CANCEL | CENTRE)

            if dlg.ShowModal() == ID_OK:
                pyutActor.setName(dlg.GetValue())
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
                from UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
                if not isinstance(umlFrame, UmlSequenceDiagramsFrame):
                    displayError(_("A SD INSTANCE can't be added to a class diagram. You must create a sequence diagram."))
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
                displayError(_(f"An error occured while trying to do this action {e}"))
                umlFrame.Refresh()
        # added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (10.10.2005)
        elif self._currentAction == ACTION_ZOOM_IN:
            return SKIP_EVENT
        elif self._currentAction == ACTION_ZOOM_OUT:
            umlFrame.DoZoomOut(x, y)
            umlFrame.Refresh()
            self.updateTitle()
        else:
            return SKIP_EVENT
        return EVENT_PROCESSED

    def selectTool(self, ID):
        """
        Select the tool of given ID from the toolbar, and delesect the others.

        @since 1.9
        @author L. Burgbacher <lb@alawa.ch>
        """
        for toolId in self._tools:
            self._toolBar.ToggleTool(toolId, False)
        self._toolBar.ToggleTool(ID, True)

    def shapeSelected(self, shape, position=None):
        """
        Do action when a shape is selected.

        @since 1.9
        @author L. Burgbacher <lb@alawa.ch>
        TODO : support each link type
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None: return
        # do the right action
        if self._currentAction in SOURCE_ACTIONS:
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
                self._src = shape
                self._srcPos = position
        elif self._currentAction in DEST_ACTIONS:
            # store the destination object
            self._dst = shape
            self._dstPos = position
            # if no destination, cancel action
            if self._dst is None:
                self._currentAction = ACTION_SELECTOR
                self.selectTool(self._tools[0])
                self.setStatusText(_("Action cancelled"))
                return

            from org.pyut.commands.CreateOglLinkCommand import CreateOglLinkCommand
            from org.pyut.commands.CommandGroup import CommandGroup
            cmd = CreateOglLinkCommand(self._src,
                                       self._dst,
                                       LINK_TYPE[self._currentAction],
                                       self._srcPos,
                                       self._dstPos)

            cmdGroup = CommandGroup("create link")
            cmdGroup.addCommand(cmd)
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            umlFrame.getHistory().execute()
            self._src = None
            self._dst = None
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

    def actionWaiting(self):
        """
        Return True if there's an action waiting to be completed.

        @since 1.2
        @author L. Burgbacher <lb@alawa.ch>
        """
        return self._currentAction != ACTION_SELECTOR

    def autoResize(self, obj: PyutClass):
        """
        Autoresize the given object.

        @param obj

        @since 1.18
        @author L. Burgbacher <lb@alawa.ch>
        """
        from org.pyut.ogl.OglClass import OglClass
        prefs: PyutPreferences = PyutPreferences()

        if prefs["AUTO_RESIZE"]:
            if isinstance(obj, PyutClass):
                po = [po for po in self.getUmlObjects() if isinstance(po, OglClass) and po.getPyutObject() is obj]
                obj = po[0]

            obj.autoResize()

    def editObject(self, x, y):
        """
        Edit the object at x, y.

        @since 1.10
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return
        #
        # TODO I don't like in-line imports but moving them to top file causes a cyclic dependency error
        #
        from org.pyut.ogl.OglClass import OglClass
        from org.pyut.ogl.OglNote import OglNote
        from OglUseCase import OglUseCase
        from org.pyut.ogl.OglActor import OglActor
        from org.pyut.ogl.OglAssociation import OglAssociation
        from OglInterface import OglInterface

        diagramShape = umlFrame.FindShape(x, y)

        if diagramShape is None:
            return

        if isinstance(diagramShape, OglClass):
            pyutObject = diagramShape.getPyutObject()
            self.classEditor(pyutObject)
            self.autoResize(diagramShape)
        elif isinstance(diagramShape, OglNote):
            pyutObject = diagramShape.getPyutObject()
            dlg = DlgEditNote(umlFrame, -1, pyutObject)
            dlg.Destroy()
        elif isinstance(diagramShape, OglUseCase):
            pyutObject = diagramShape.getPyutObject()
            dlg = DlgEditUseCase(umlFrame, -1, pyutObject)
            dlg.Destroy()
        elif isinstance(diagramShape, OglActor):
            pyutObject = diagramShape.getPyutObject()
            dlg = TextEntryDialog(umlFrame, "Actor name", "Enter actor name", pyutObject.getName(), OK | CANCEL | CENTRE)
            if dlg.ShowModal() == ID_OK:
                pyutObject.setName(dlg.GetValue())
            dlg.Destroy()
        elif isinstance(diagramShape, OglAssociation):
            dlg = DlgEditLink(None, -1, diagramShape.getPyutObject())
            dlg.ShowModal()
            rep = dlg.getReturnAction()
            dlg.Destroy()
            if rep == -1:    # destroy link
                diagramShape.Detach()
        elif isinstance(diagramShape, OglInterface):
            dlg = DlgEditLink(None, -1, diagramShape.getPyutObject())
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
        if self._fileHandling is None:
            return []
        umlFrame = self._fileHandling.getCurrentFrame()
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
            selectedObjs = []
            for obj in self.getUmlObjects():
                if obj.IsSelected():
                    selectedObjs.append(obj)

            return selectedObjs
        else:
            return []

    def setStatusText(self, msg):
        """
        Set the text in the status bar.

        @param String msg : The message to put in the status bar
        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
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
        umlFrame = self._fileHandling.getCurrentFrame()
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
        return self._fileHandling.getCurrentFrame()

    def deselectAllShapes(self):
        """
        Deselect all shapes in the diagram.

        @since 1.12
        @author L. Burgbacher <lb@alawa.ch>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is not None:
            shapes = umlFrame.GetDiagram().GetShapes()
            for shape in shapes:
                shape.SetSelected(False)
            umlFrame.Refresh()

    def showParams(self, val):
        """
        Choose wether to show the params in the classes or not.

        @param val
        @since 1.17
        @author L. Burgbacher <lb@alawa.ch>
        """
        if val:
            PyutMethod.setStringMode(WITH_PARAMS)
        else:
            PyutMethod.setStringMode(WITHOUT_PARAMS)

    def getCurrentDir(self):
        """
        Return the application's current directory

        @return String : application's current directory
        """
        return self._appFrame.getCurrentDir()

    def setCurrentDir(self, directory):
        """
        Set the application's current directory

        @param String directory : New appliation's current directory
        """
        return self._appFrame.updateCurrentDir(directory)

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
            WXK_INSERT: self.insertSelectedShape,
            ord('i'):   self.insertSelectedShape,
            ord('I'):   self.insertSelectedShape,
            ord('s'):   self.toggleSpline,
            ord('S'):   self.toggleSpline,
            ord('<'):   self.moveSelectedShapeDown,
            ord('>'):   self.moveSelectedShapeUp,
        }
        # Python 3 update
        # if funcs.has_key(c):
        if c in funcs:
            funcs[c]()
        else:
            self.logger.info(f'Not supported: {c}')
            event.Skip()

    def deleteSelectedShape(self):
        from org.pyut.commands.DelOglObjectCommand import DelOglObjectCommand
        from org.pyut.commands.DelOglClassCommand import DelOglClassCommand
        from org.pyut.commands.DelOglLinkCommand import DelOglLinkCommand
        from org.pyut.ogl.OglClass import OglClass
        from org.pyut.ogl.OglObject import OglObject
        from org.pyut.ogl.OglLink import OglLink
        from org.pyut.commands.CommandGroup import CommandGroup

        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return
        selected     = umlFrame.GetSelectedShapes()
        cmdGroup     = CommandGroup("Delete UML object(s)")
        cmdGroupInit = False  # added by hasii to avoid Pycharm warning about cmdGroupInit not set

        for shape in selected:
            cmd = None
            if isinstance(shape, OglClass):
                cmd = DelOglClassCommand(shape)
            elif isinstance(shape, OglObject):
                cmd = DelOglObjectCommand(shape)
            elif isinstance(shape, OglLink):
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
        umlFrame = self._fileHandling.getCurrentFrame()
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

        umlFrame = self._fileHandling.getCurrentFrame()
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
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return
        self._moveSelectedShapeZOrder(umlFrame.GetDiagram().MoveToFront)

    def moveSelectedShapeDown(self):
        """
        Move the selected shape one level down in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return
        self._moveSelectedShapeZOrder(umlFrame.GetDiagram().MoveToBack)

    def _moveSelectedShapeZOrder(self, callback):
        """
        Move the selected shape one level in z-order

        @since 1.27.2.28
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        from org.pyut.ogl import OglObject
        umlFrame = self._fileHandling.getCurrentFrame()
        if umlFrame is None:
            return
        selected = umlFrame.GetSelectedShapes()
        if len(selected) > 0:
            for oglObject in selected:
                if isinstance(oglObject, OglObject.OglObject):
                    callback(oglObject)
        umlFrame.Refresh()

    def registerTool(self, tool):
        """
        Add a tool to toolboxes

        @param Tool tool : The tool to add
        @since 1.3
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._toolboxOwner.registerTool(tool)

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

        po = [po for po in self.getUmlObjects() if isinstance(po, OglClass) and po.getPyutObject() is pyutClass]

        return po[0]

    def getFileHandling(self):
        """
        Return the FileHandling class

        @return FileHandling instance
        @author C.Dutoit
        """
        return self._fileHandling

    def updateTitle(self):
        """
        Set the application title, function of version and current filename

        @since 1.4
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        # Exit if we are in scripting mode
        if self.isInScriptMode():
            return

        # Get filename
        project = self._fileHandling.getCurrentProject()
        if project is not None:
            filename = project.getFilename()
        else:
            filename = ""

        # Set text
        txt = "PyUt v" + __PyUtVersion__ + " - " + filename
        if (project is not None) and (project.getModified()):
            if self._fileHandling.getCurrentFrame() is not None:
                zoom = self._fileHandling.getCurrentFrame().GetCurrentZoom()
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
        self._appFrame.cutSelectedShapes()

    def getCurrentAction(self):
        return self._currentAction

    def beginChangeRecording(self, oglObject):

        from org.pyut.commands.DelOglClassCommand import DelOglClassCommand
        from org.pyut.commands.DelOglObjectCommand import DelOglObjectCommand
        from org.pyut.commands.DelOglLinkCommand import DelOglLinkCommand
        from org.pyut.ogl.OglClass import OglClass
        from org.pyut.ogl.OglLink import OglLink
        from org.pyut.ogl.OglObject import OglObject

        if isinstance(oglObject, OglClass):
            print("begin")
            self._modifyCommand = DelOglClassCommand(oglObject)
        elif isinstance(oglObject, OglLink):
            self._modifyCommand = DelOglLinkCommand(oglObject)
        elif isinstance(oglObject, OglObject):
            self._modifyCommand = DelOglObjectCommand(oglObject)
        else:
            raise RuntimeError("a non-OglObject has requested for a change recording")

    def endChangeRecording(self, oglObject):

        from org.pyut.commands.CreateOglClassCommand import CreateOglClassCommand
        from org.pyut.ogl.OglClass import OglClass

        from org.pyut.commands.CommandGroup import CommandGroup

        cmd = None

        if isinstance(oglObject, OglClass):
            cmd = CreateOglClassCommand(shape=oglObject)

        if cmd is not None and self._modifyCommand is not None:

            group = CommandGroup("modify " + oglObject.getPyutObject().getName())
            group.addCommand(self._modifyCommand)
            group.addCommand(cmd)

            umlFrame = self.getFileHandling().getCurrentFrame()
            umlFrame.getHistory().addCommandGroup(group)

        self._modifyCommand = None
