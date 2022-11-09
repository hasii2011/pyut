
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from wx import ID_OK
from wx import CANCEL
from wx import CENTRE
from wx import ID_ANY
from wx import OK

from wx import TextEntryDialog

from wx import Yield as wxYield

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.Constants import EVENT_PROCESSED
from miniogl.Constants import SKIP_EVENT

from ogl.OglClass import OglClass

from pyut.general.Singleton import Singleton

from pyut.ui.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlFrame import UmlFrame
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutLinkType import PyutLinkType

from pyut.ui.Actions import ACTION_DESTINATION_AGGREGATION_LINK
from pyut.ui.Actions import ACTION_DESTINATION_ASSOCIATION_LINK
from pyut.ui.Actions import ACTION_DESTINATION_COMPOSITION_LINK
from pyut.ui.Actions import ACTION_DESTINATION_IMPLEMENT_LINK
from pyut.ui.Actions import ACTION_DESTINATION_INHERIT_LINK
from pyut.ui.Actions import ACTION_DESTINATION_NOTE_LINK
from pyut.ui.Actions import ACTION_DESTINATION_SD_MESSAGE
from pyut.ui.Actions import ACTION_NEW_ACTOR
from pyut.ui.Actions import ACTION_NEW_AGGREGATION_LINK
from pyut.ui.Actions import ACTION_NEW_ASSOCIATION_LINK
from pyut.ui.Actions import ACTION_NEW_CLASS
from pyut.ui.Actions import ACTION_NEW_COMPOSITION_LINK
from pyut.ui.Actions import ACTION_NEW_IMPLEMENT_LINK
from pyut.ui.Actions import ACTION_NEW_INHERIT_LINK
from pyut.ui.Actions import ACTION_NEW_NOTE
from pyut.ui.Actions import ACTION_NEW_NOTE_LINK
from pyut.ui.Actions import ACTION_NEW_SD_INSTANCE
from pyut.ui.Actions import ACTION_NEW_SD_MESSAGE
from pyut.ui.Actions import ACTION_NEW_TEXT
from pyut.ui.Actions import ACTION_NEW_USECASE
from pyut.ui.Actions import ACTION_SELECTOR
from pyut.ui.Actions import ACTION_ZOOM_IN
from pyut.ui.Actions import ACTION_ZOOM_OUT

from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from pyut.uiv2.eventengine.MiniProjectInformation import MiniProjectInformation
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.eventengine.Events import EVENT_SET_TOOL_ACTION
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import SetToolActionEvent

from pyut.PyutUtils import PyutUtils

from pyut.dialogs.DlgEditUseCase import DlgEditUseCase
from pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from pyut.dialogs.textdialogs.DlgEditText import DlgEditText

# messages for the status bar
a = "Click on the source class"
b = "Now, click on the destination class"

MESSAGES = {
    ACTION_SELECTOR:        "Ready",
    ACTION_NEW_CLASS:       "Click where you want to put the new class",
    ACTION_NEW_NOTE:        "Click where you want to put the new note",
    ACTION_NEW_ACTOR:       "Click where you want to put the new actor",
    ACTION_NEW_TEXT:        'Click where you want to put the new text',
    ACTION_NEW_USECASE:     "Click where you want to put the new use case",
    ACTION_NEW_SD_INSTANCE: "Click where you want to put the new instance",
    ACTION_NEW_SD_MESSAGE:  "Click inside the lifeline for the new message",
    ACTION_DESTINATION_SD_MESSAGE: "Click inside the lifeline for the destination of the message",
    ACTION_NEW_IMPLEMENT_LINK:   a,
    ACTION_NEW_INHERIT_LINK:     a,
    ACTION_NEW_AGGREGATION_LINK: a,
    ACTION_NEW_COMPOSITION_LINK: a,
    ACTION_NEW_ASSOCIATION_LINK: a,
    ACTION_NEW_NOTE_LINK:        a,
    ACTION_DESTINATION_IMPLEMENT_LINK:   b,
    ACTION_DESTINATION_INHERIT_LINK:     b,
    ACTION_DESTINATION_AGGREGATION_LINK: b,
    ACTION_DESTINATION_COMPOSITION_LINK: b,
    ACTION_DESTINATION_ASSOCIATION_LINK: b,
    ACTION_DESTINATION_NOTE_LINK:        b,
    ACTION_ZOOM_IN:     "Select the area to fit on",
    ACTION_ZOOM_OUT:    "Select the central point",

}

# a table of the next action to select
NEXT_ACTION = {
    ACTION_SELECTOR:    ACTION_SELECTOR,
    ACTION_NEW_CLASS:   ACTION_SELECTOR,
    ACTION_NEW_NOTE:    ACTION_SELECTOR,
    ACTION_NEW_IMPLEMENT_LINK:          ACTION_DESTINATION_IMPLEMENT_LINK,
    ACTION_NEW_INHERIT_LINK:            ACTION_DESTINATION_INHERIT_LINK,
    ACTION_NEW_AGGREGATION_LINK:        ACTION_DESTINATION_AGGREGATION_LINK,
    ACTION_NEW_COMPOSITION_LINK:        ACTION_DESTINATION_COMPOSITION_LINK,
    ACTION_NEW_ASSOCIATION_LINK:        ACTION_DESTINATION_ASSOCIATION_LINK,
    ACTION_NEW_NOTE_LINK:               ACTION_DESTINATION_NOTE_LINK,
    ACTION_DESTINATION_IMPLEMENT_LINK:  ACTION_SELECTOR,

    ACTION_DESTINATION_INHERIT_LINK:     ACTION_SELECTOR,
    ACTION_DESTINATION_AGGREGATION_LINK: ACTION_SELECTOR,
    ACTION_DESTINATION_COMPOSITION_LINK: ACTION_SELECTOR,
    ACTION_DESTINATION_ASSOCIATION_LINK: ACTION_SELECTOR,
    ACTION_DESTINATION_NOTE_LINK:        ACTION_SELECTOR,
    ACTION_NEW_ACTOR:                    ACTION_SELECTOR,
    ACTION_NEW_USECASE:                  ACTION_SELECTOR,

    ACTION_NEW_SD_INSTANCE: ACTION_SELECTOR,
    ACTION_NEW_SD_MESSAGE:  ACTION_DESTINATION_SD_MESSAGE,

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
DESTINATION_ACTIONS = [
    ACTION_DESTINATION_IMPLEMENT_LINK,
    ACTION_DESTINATION_INHERIT_LINK,
    ACTION_DESTINATION_AGGREGATION_LINK,
    ACTION_DESTINATION_COMPOSITION_LINK,
    ACTION_DESTINATION_ASSOCIATION_LINK,
    ACTION_DESTINATION_NOTE_LINK,
    ACTION_DESTINATION_SD_MESSAGE,
    ACTION_ZOOM_IN,
    ACTION_ZOOM_OUT
]

# OglLink enumerations according to the current action
LINK_TYPE = {
    ACTION_DESTINATION_IMPLEMENT_LINK:     PyutLinkType.INTERFACE,
    ACTION_DESTINATION_INHERIT_LINK:       PyutLinkType.INHERITANCE,
    ACTION_DESTINATION_AGGREGATION_LINK:   PyutLinkType.AGGREGATION,
    ACTION_DESTINATION_COMPOSITION_LINK:   PyutLinkType.COMPOSITION,
    ACTION_DESTINATION_ASSOCIATION_LINK:   PyutLinkType.ASSOCIATION,
    ACTION_DESTINATION_NOTE_LINK:          PyutLinkType.NOTELINK,
    ACTION_DESTINATION_SD_MESSAGE:         PyutLinkType.SD_MESSAGE,
}


class ActionHandler(Singleton):

    def init(self, **kwargs):

        self.logger:       Logger       = getLogger(__name__)
        self._eventEngine: IEventEngine = kwargs['eventEngine']

        self._currentAction:           int  = ACTION_SELECTOR
        self._currentActionPersistent: bool = False

        self._eventEngine.registerListener(pyEventBinder=EVENT_SET_TOOL_ACTION, callback=self._onSetToolAction)

    @property
    def actionWaiting(self) -> bool:
        """
        Returns: `True` if there's an action waiting to be completed, else `False`
        """
        return self._currentAction != ACTION_SELECTOR

    @property
    def currentAction(self):
        return self._currentAction

    @currentAction.setter
    def currentAction(self, action: int):
        """
        TODO make actions enumerations
        Set the new current action.
        This tells the action handler which action to do for the next doAction call.

        Args:
            action:  the action from ACTION constants
        """
        self.logger.debug(f'Set current action to: {action}')
        if self._currentAction == action:
            self._currentActionPersistent = True
        else:
            self._currentAction = action
            self._currentActionPersistent = False

        # self.setStatusText(MESSAGES[self._currentAction])
        msg: str = MESSAGES[self._currentAction]
        self._eventEngine.sendEvent(EventType.UpdateApplicationStatus, applicationStatusMsg=msg)

    def updateTitle(self):
        """
        Set the application title, function of version and current project name
        """

        self._eventEngine.sendEvent(EventType.MiniProjectInformation, callback=self._doUpdate)

    def doAction(self, umlFrame: 'UmlFrame', x: int, y: int):
        """
        Do the current action at coordinates x, y.

        Args:
            umlFrame:  The frame we are acting on
            x: x coord where the action must take place
            y: y coord where the action must take place
        """
        self.logger.debug(f'doAction: {self._currentAction}  ACTION_SELECTOR: {ACTION_SELECTOR}')
        # umlFrame = self._treeNotebookHandler.currentFrame
        # if umlFrame is None:
        #     return
        self._resetStatusText()
        if self._currentAction == ACTION_SELECTOR:
            return SKIP_EVENT
        elif self._currentAction == ACTION_NEW_CLASS:
            self._createOglClass(umlFrame=umlFrame, x=x, y=y)
        elif self._currentAction == ACTION_NEW_TEXT:
            self._createNewText(umlFrame, x, y)
        elif self._currentAction == ACTION_NEW_NOTE:
            self._createNewNote(umlFrame, x, y)
        elif self._currentAction == ACTION_NEW_ACTOR:
            pyutActor = umlFrame.createNewActor(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self._selectActionSelectorTool()
            dlg = TextEntryDialog(umlFrame, "Actor name", "Enter actor name", pyutActor.name, OK | CANCEL | CENTRE)

            if dlg.ShowModal() == ID_OK:
                pyutActor.name = dlg.GetValue()
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_USECASE:
            pyutUseCase = umlFrame.createNewUseCase(x, y)
            if not self._currentActionPersistent:
                self._currentAction = ACTION_SELECTOR
                self._selectTool(SharedIdentifiers.ID_ARROW)
            dlg = DlgEditUseCase(umlFrame, -1, pyutUseCase)
            dlg.Destroy()
            umlFrame.Refresh()
        elif self._currentAction == ACTION_NEW_SD_INSTANCE:
            try:
                from pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
                if not isinstance(umlFrame, UmlSequenceDiagramsFrame):
                    PyutUtils.displayError("A SD INSTANCE can't be added to a class diagram. You must create a sequence diagram.")
                    return
                instance = umlFrame.createNewSDInstance(x, y)
                if not self._currentActionPersistent:
                    self._currentAction = ACTION_SELECTOR
                    self._selectTool(SharedIdentifiers.ID_ARROW)

                dlg = TextEntryDialog(umlFrame, "Instance name", "Enter instance name", instance.getInstanceName(), OK | CANCEL | CENTRE)

                if dlg.ShowModal() == ID_OK:
                    instance.setInstanceName(dlg.GetValue())
                dlg.Destroy()
                umlFrame.Refresh()
            except (ValueError, Exception) as e:
                PyutUtils.displayError(f"An error occurred while trying to do this action {e}")
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

    def shapeSelected(self, umlFrame, shape, position=None):
        """
        Do action when a shape is selected.
        TODO : support each link type
        """
        # umlFrame = self._treeNotebookHandler.currentFrame
        # if umlFrame is None:
        #     return

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
                self._selectActionSelectorTool()
                self._setStatusText("Action cancelled")
            else:   # store source
                self.logger.debug(f'Store source - shape {shape}  position: {position}')
                self._src    = shape
                self._srcPos = position
        elif self._currentAction in DESTINATION_ACTIONS:
            self.logger.debug(f'Current action in destination actions')
            # store the destination object
            self._dst    = shape
            self._dstPos = position
            # if no destination, cancel action
            if self._dst is None:
                self._currentAction = ACTION_SELECTOR
                self._selectActionSelectorTool()
                self._setStatusText("Action cancelled")
                return
            self._createLink(umlFrame)

            if self._currentActionPersistent:
                self._currentAction = self._oldAction
                del self._oldAction
            else:
                self._currentAction = ACTION_SELECTOR
                self._selectActionSelectorTool()
        else:
            self._setStatusText("Error : Action not supported by the mediator")
            return
        self._setStatusText(MESSAGES[self._currentAction])

    def requestLollipopLocation(self, umlFrame: 'UmlDiagramsFrame', destinationClass: OglClass):

        self.__createPotentialAttachmentPoints(destinationClass=destinationClass, umlFrame=umlFrame)
        self._setStatusText(f'Select attachment point')
        umlFrame.Refresh()
        wxYield()

    def createLollipopInterface(self, umlFrame: 'UmlDiagramsFrame', implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        from pyut.history.commands.CreateOglInterfaceCommand import CreateOglInterfaceCommand
        from pyut.history.commands.CommandGroup import CommandGroup

        attachmentAnchor.setYouAreTheSelectedAnchor()

        cmd: CreateOglInterfaceCommand = CreateOglInterfaceCommand(umlFrame=umlFrame, implementor=implementor, attachmentAnchor=attachmentAnchor)
        group: CommandGroup = CommandGroup("Create lollipop")

        group.addCommand(cmd)
        umlFrame.getHistory().addCommandGroup(group)
        umlFrame.getHistory().execute()

    def _onSetToolAction(self, event: SetToolActionEvent):
        self.currentAction = event.action

    def _createOglClass(self, umlFrame, x: int, y: int):

        from pyut.history.commands.CreateOglClassCommand import CreateOglClassCommand
        from pyut.history.commands.CommandGroup import CommandGroup

        cmd:   CreateOglClassCommand = CreateOglClassCommand(x, y, eventEngine=self._eventEngine)
        group: CommandGroup          = CommandGroup("Create class")
        group.addCommand(cmd)
        umlFrame.getHistory().addCommandGroup(group)
        umlFrame.getHistory().execute()

        if not self._currentActionPersistent:
            self._currentAction = ACTION_SELECTOR
            # self.selectTool(self._tools[0])
            self._selectTool(SharedIdentifiers.ID_ARROW)

    def _createNewText(self, umlFrame, x: int, y: int):
        """
        Create a text box on the diagram

        Args:
            umlFrame:  The UML frame that knows hot to place the new text object on the diagram
            x: The x-coordinate
            y: The y-coordinate
        """
        pyutText: PyutText = umlFrame.createNewText(x, y)

        self._resetToActionSelector()
        dlg: DlgEditText = DlgEditText(parent=umlFrame, dialogIdentifier=ID_ANY, pyutText=pyutText)
        dlg.ShowModal()
        dlg.Destroy()
        umlFrame.Refresh()

    def _createNewNote(self, umlFrame: UmlFrameShapeHandler, x: int, y: int):
        """
        Create a note on the diagram

        Args:
            umlFrame:  The UML frame knows how to place the new note on diagram
            x: The x-coordinate
            y: The y-coordinate
        """

        pyutNote: PyutNote = umlFrame.createNewNote(x, y)

        self._resetToActionSelector()
        dlg: DlgEditNote = DlgEditNote(umlFrame, ID_ANY, pyutNote)
        dlg.ShowModal()
        dlg.Destroy()
        umlFrame.Refresh()

    def _createLink(self, umlFrame):

        from pyut.history.commands.CreateOglLinkCommand import CreateOglLinkCommand
        from pyut.history.commands.CommandGroup import CommandGroup

        linkType = LINK_TYPE[self._currentAction]
        cmd = CreateOglLinkCommand(self._src, self._dst, linkType, self._srcPos, self._dstPos)

        cmdGroup = CommandGroup("create link")
        cmdGroup.addCommand(cmd)
        umlFrame.getHistory().addCommandGroup(cmdGroup)
        umlFrame.getHistory().execute()
        self._src = None
        self._dst = None

    def _setStatusText(self, msg: str):
        self._eventEngine.sendEvent(EventType.UpdateApplicationStatus, applicationStatusMsg=msg)

    def _resetStatusText(self):
        self._setStatusText('')

    def _doUpdate(self, projectInformation: MiniProjectInformation):
        pass

    def _resetToActionSelector(self):
        """
        For non-persistent tools
        """
        if not self._currentActionPersistent:
            self._currentAction = ACTION_SELECTOR
            self._selectTool(SharedIdentifiers.ID_ARROW)

    def _selectActionSelectorTool(self):
        self._selectTool(SharedIdentifiers.ID_ARROW)

    def _selectTool(self, toolId: int):
        """
        Select the tool of given ID from the toolbar, and deselect the others.

        Args:
            toolId:  The tool id
        """
        self._eventEngine.sendEvent(EventType.SelectTool, toolId=toolId)
        # for deselectedToolId in self._tools:
        #     self._toolBar.ToggleTool(deselectedToolId, False)
        # self._toolBar.ToggleTool(toolId, True)

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

        self.__createAnchorHints(destinationClass, southX, southY, AttachmentLocation.SOUTH, umlFrame)
        self.__createAnchorHints(destinationClass, northX, northY, AttachmentLocation.NORTH, umlFrame)
        self.__createAnchorHints(destinationClass, westX, westY, AttachmentLocation.WEST, umlFrame)
        self.__createAnchorHints(destinationClass, eastX, eastY, AttachmentLocation.EAST, umlFrame)

    def __createAnchorHints(self, destinationClass: OglClass, anchorX: int, anchorY: int, attachmentPoint: AttachmentLocation, umlFrame):

        anchorHint: SelectAnchorPoint = SelectAnchorPoint(x=anchorX, y=anchorY, attachmentPoint=attachmentPoint, parent=destinationClass)
        anchorHint.SetProtected(True)

        destinationClass.AddAnchorPoint(anchorHint)
        umlFrame.getDiagram().AddShape(anchorHint)
