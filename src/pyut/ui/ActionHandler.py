
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from wx import ID_OK
from wx import CANCEL
from wx import CENTRE
from wx import OK

from wx import CommandProcessor
from wx import TextEntryDialog

from wx import Yield as wxYield

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.Constants import EVENT_PROCESSED
from miniogl.Constants import SKIP_EVENT

from ogl.OglClass import OglClass

from pyut.general.Singleton import Singleton
from pyut.ui.wxcommands.CommandCreateOglActor import CommandCreateOglActor

from pyut.ui.wxcommands.CommandCreateOglClass import CommandCreateOglClass
from pyut.ui.wxcommands.CommandCreateOglLink import CommandCreateOglLink
from pyut.ui.wxcommands.CommandCreateOglNote import CommandCreateOglNote
from pyut.ui.wxcommands.CommandCreateOglText import CommandCreateOglText

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlFrame import UmlFrame
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from pyutmodel.PyutLinkType import PyutLinkType

from pyut.ui.Action import ACTION_DESTINATION_AGGREGATION_LINK
from pyut.ui.Action import ACTION_DESTINATION_ASSOCIATION_LINK
from pyut.ui.Action import ACTION_DESTINATION_COMPOSITION_LINK
from pyut.ui.Action import ACTION_DESTINATION_IMPLEMENT_LINK
from pyut.ui.Action import ACTION_DESTINATION_INHERIT_LINK
from pyut.ui.Action import ACTION_DESTINATION_NOTE_LINK
from pyut.ui.Action import ACTION_DESTINATION_SD_MESSAGE
from pyut.ui.Action import ACTION_NEW_ACTOR
from pyut.ui.Action import ACTION_NEW_AGGREGATION_LINK
from pyut.ui.Action import ACTION_NEW_ASSOCIATION_LINK
from pyut.ui.Action import ACTION_NEW_CLASS
from pyut.ui.Action import ACTION_NEW_COMPOSITION_LINK
from pyut.ui.Action import ACTION_NEW_IMPLEMENT_LINK
from pyut.ui.Action import ACTION_NEW_INHERIT_LINK
from pyut.ui.Action import ACTION_NEW_NOTE
from pyut.ui.Action import ACTION_NEW_NOTE_LINK
from pyut.ui.Action import ACTION_NEW_SD_INSTANCE
from pyut.ui.Action import ACTION_NEW_SD_MESSAGE
from pyut.ui.Action import ACTION_NEW_TEXT
from pyut.ui.Action import ACTION_NEW_USECASE
from pyut.ui.Action import ACTION_SELECTOR
from pyut.ui.Action import ACTION_ZOOM_IN
from pyut.ui.Action import ACTION_ZOOM_OUT

from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from pyut.uiv2.eventengine.eventinformation.MiniProjectInformation import MiniProjectInformation
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.eventengine.Events import EVENT_SET_TOOL_ACTION
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import SetToolActionEvent

from pyut.PyutUtils import PyutUtils

from pyut.dialogs.DlgEditUseCase import DlgEditUseCase

# messages for the status bar

CLICK:    str = 'Click'
LOCATION: str = f'{CLICK} to place the new'
ON:       str = f'{CLICK} on the'

MESSAGES = {
    ACTION_SELECTOR:                     'Ready',
    ACTION_NEW_CLASS:                    f'{LOCATION} class',
    ACTION_NEW_NOTE:                     f'{LOCATION} note',
    ACTION_NEW_ACTOR:                    f'{LOCATION} actor',
    ACTION_NEW_TEXT:                     f'{LOCATION} text',
    ACTION_NEW_USECASE:                  f'{LOCATION} case',
    ACTION_NEW_SD_INSTANCE:              f'{LOCATION} instance',
    ACTION_NEW_SD_MESSAGE:               'Click inside the lifeline of the caller',
    ACTION_DESTINATION_SD_MESSAGE:       'Click inside the lifeline of the message implementer',
    ACTION_NEW_IMPLEMENT_LINK:           f'{ON} interface implementor',
    ACTION_NEW_INHERIT_LINK:             f'{ON} subclass',
    ACTION_NEW_AGGREGATION_LINK:         f'{ON} aggregator',
    ACTION_NEW_COMPOSITION_LINK:         f'{ON} composer',
    ACTION_NEW_ASSOCIATION_LINK:         f'{ON} source of the association',
    ACTION_NEW_NOTE_LINK:                f'{ON} note',
    ACTION_DESTINATION_IMPLEMENT_LINK:   f'{ON} interface',
    ACTION_DESTINATION_INHERIT_LINK:     f'{ON} parent class',
    ACTION_DESTINATION_AGGREGATION_LINK: f'{ON} "aggregated" class',
    ACTION_DESTINATION_COMPOSITION_LINK: f'{ON} "composed" class',
    ACTION_DESTINATION_ASSOCIATION_LINK: f'{ON} destination of the association',
    ACTION_DESTINATION_NOTE_LINK:        f'{ON} class',
    ACTION_ZOOM_IN:                      'Select the area to zoom in',
    ACTION_ZOOM_OUT:                     'Select the central point',

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

        self.logger:            Logger           = getLogger(__name__)
        self._eventEngine:      IEventEngine     = kwargs['eventEngine']
        self._commandProcessor: CommandProcessor = kwargs['commandProcessor']

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

    def doAction(self, umlFrame: 'UmlFrame', x: int, y: int) -> int:
        """
        Do the current action at coordinates x, y.

        Args:
            umlFrame:  The frame we are acting on
            x: The ordinate where the action must take place
            y: The abscissa where the action must take place

        Returns: Event handler status

        """
        self.logger.debug(f'doAction: {self._currentAction}  {ACTION_SELECTOR=}')
        self._resetStatusText()
        # TODO:  make the createXXX methods return the command;  Do a single submittal on return
        # TODO:  rename the createXXX methods to createXXXCommand
        # TODO:  convert to match (aka switch) statement
        handlerStatus: int = EVENT_PROCESSED
        currentAction: int = self._currentAction
        # match currentAction:

        if currentAction == ACTION_SELECTOR:
            handlerStatus = SKIP_EVENT
        elif currentAction == ACTION_NEW_CLASS:
            self._createOglClass(x=x, y=y)
        elif currentAction == ACTION_NEW_TEXT:
            self._createNewText(x, y)
        elif currentAction == ACTION_NEW_NOTE:
            self._createNewNote(x, y)
        elif currentAction == ACTION_NEW_ACTOR:
            self._createActor(x, y)
        elif currentAction == ACTION_NEW_USECASE:
            self._createNewUseCase(umlFrame, x, y)
        elif currentAction == ACTION_NEW_SD_INSTANCE:
            self._attemptSDInstanceCreation(umlFrame, x, y)
        elif currentAction == ACTION_ZOOM_IN:
            handlerStatus = SKIP_EVENT
        elif currentAction == ACTION_ZOOM_OUT:
            self._doZoomOut(umlFrame, x, y)
        else:
            handlerStatus = SKIP_EVENT

        return handlerStatus

    def shapeSelected(self, shape, position=None):
        """
        Do action when a shape is selected.
        TODO : support each link type
        """
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
            self._createLink()

            if self._currentActionPersistent:
                self._currentAction = self._oldAction
                del self._oldAction
            else:
                self._currentAction = ACTION_SELECTOR
                self._selectActionSelectorTool()
        else:
            self._setStatusText("Error : Action not supported by the Action Handler")
            return
        self._setStatusText(MESSAGES[self._currentAction])

    def requestLollipopLocation(self, umlFrame: 'UmlDiagramsFrame', destinationClass: OglClass):

        self.__createPotentialAttachmentPoints(destinationClass=destinationClass, umlFrame=umlFrame)
        self._setStatusText(f'Select attachment point')
        umlFrame.Refresh()
        wxYield()

    def createLollipopInterface(self, umlFrame: 'UmlDiagramsFrame', implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        pass    # TODO: Implement this!!!
        # from pyut.history.commands.CreateOglInterfaceCommand import CreateOglInterfaceCommand
        # from pyut.history.commands.CommandGroup import CommandGroup
        #
        # attachmentAnchor.setYouAreTheSelectedAnchor()
        #
        # cmd: CreateOglInterfaceCommand = CreateOglInterfaceCommand(umlFrame=umlFrame, eventEngine=self._eventEngine,
        #                                                            implementor=implementor, attachmentAnchor=attachmentAnchor)
        # group: CommandGroup = CommandGroup("Create lollipop")
        #
        # group.addCommand(cmd)
        # umlFrame.historyManager.addCommandGroup(group)
        # umlFrame.historyManager.execute()

    def _onSetToolAction(self, event: SetToolActionEvent):
        self.currentAction = event.action

    def _attemptSDInstanceCreation(self, umlFrame, x, y):
        """
        Attempt because we need to check for valid diagram frame
        Args:
            umlFrame:
            x:
            y:
        """
        from pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
        if not isinstance(umlFrame, UmlSequenceDiagramsFrame):
            PyutUtils.displayError("An SD INSTANCE cannot be added to a class diagram. PLease create a sequence diagram.")
        else:
            self._createNewSDInstance(umlFrame, x, y)

    def _createOglClass(self, x: int, y: int):

        command: CommandCreateOglClass = CommandCreateOglClass(x=x, y=y, eventEngine=self._eventEngine)
        self._commandProcessor.Submit(command=command, storeIt=True)
        self._resetToActionSelector()

    def _createNewText(self, x: int, y: int):
        """
        Create a text box on the diagram

        Args:
            x: The x-coordinate
            y: The y-coordinate
        """
        command: CommandCreateOglText = CommandCreateOglText(x=x, y=y, eventEngine=self._eventEngine)
        self._commandProcessor.Submit(command=command, storeIt=True)
        self._resetToActionSelector()

    def _createNewNote(self, x: int, y: int):
        """
        Create a note on the diagram

        Args:
            x: The x-coordinate
            y: The y-coordinate
        """
        command: CommandCreateOglNote = CommandCreateOglNote(x=x, y=y, eventEngine=self._eventEngine)
        self._commandProcessor.Submit(command=command, storeIt=True)

        self._resetToActionSelector()

    def _createActor(self, x: int, y: int):
        """

        Args:
            x: The x-coordinate
            y: The y-coordinate
        """
        command: CommandCreateOglActor = CommandCreateOglActor(x=x, y=y, eventEngine=self._eventEngine)
        self._commandProcessor.Submit(command=command, storeIt=True)

        self._resetToActionSelector()

    def _createNewUseCase(self, umlFrame, x, y):
        """
        TODO:  Make a command
        Args:
            umlFrame:
            x:
            y:

        """
        pyutUseCase = umlFrame.createNewUseCase(x, y)
        if not self._currentActionPersistent:
            self._currentAction = ACTION_SELECTOR
            self._selectTool(SharedIdentifiers.ID_ARROW)
        dlg = DlgEditUseCase(umlFrame, -1, pyutUseCase)
        dlg.Destroy()
        umlFrame.Refresh()

    def _createNewSDInstance(self, umlFrame, x, y):
        """
        TODO:  Make command
        Args:
            umlFrame:
            x:
            y:
        """
        from pyutmodel.PyutSDInstance import PyutSDInstance

        instance: PyutSDInstance = umlFrame.createNewSDInstance(x, y)
        if not self._currentActionPersistent:
            self._currentAction = ACTION_SELECTOR
            self._selectTool(SharedIdentifiers.ID_ARROW)
        dlg = TextEntryDialog(umlFrame, "Instance name", "Enter instance name", instance.instanceName, OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            instance.instanceName = dlg.GetValue()
        dlg.Destroy()
        umlFrame.Refresh()

    def _createLink(self):

        linkType: PyutLinkType = LINK_TYPE[self._currentAction]

        command: CommandCreateOglLink = CommandCreateOglLink(eventEngine=self._eventEngine,
                                                             src=self._src, dst=self._dst,
                                                             linkType=linkType,
                                                             srcPoint=self._srcPos,
                                                             dstPoint=self._dstPos
                                                             )
        self._commandProcessor.Submit(command=command, storeIt=True)
        self._src = None
        self._dst = None

    def _doZoomOut(self, umlFrame, x: int, y: int):
        umlFrame.DoZoomOut(x, y)
        umlFrame.Refresh()
        self.updateTitle()

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
