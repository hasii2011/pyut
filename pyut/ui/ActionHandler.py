
from typing import List
from typing import NewType
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import ID_OK
from wx import CANCEL
from wx import CENTRE
from wx import OK

from wx import Command
from wx import Point
from wx import TextEntryDialog

from wx import Yield as wxYield

from codeallybasic.Singleton import Singleton

from codeallyadvanced.ui.AttachmentSide import AttachmentSide

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.Constants import EVENT_PROCESSED
from miniogl.Constants import SKIP_EVENT

from ogl.OglActor import OglActor
from ogl.OglNote import OglNote
from ogl.OglObject import OglObject
from ogl.OglClass import OglClass
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase

from pyut.ui.wxcommands.CommandCreateLollipopInterface import CommandCreateLollipopInterface
from pyut.ui.wxcommands.CommandCreateOglActor import CommandCreateOglActor
from pyut.ui.wxcommands.CommandCreateOglClass import CommandCreateOglClass
from pyut.ui.wxcommands.CommandCreateOglLink import CommandCreateOglLink
from pyut.ui.wxcommands.CommandCreateOglNote import CommandCreateOglNote
from pyut.ui.wxcommands.CommandCreateOglText import CommandCreateOglText
from pyut.ui.wxcommands.CommandCreateOglUseCase import CommandCreateOglUseCase

from pyut.ui.Action import Action

from pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from pyut.uiv2.eventengine.eventinformation.MiniProjectInformation import MiniProjectInformation
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.eventengine.Events import EVENT_SET_TOOL_ACTION
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import SetToolActionEvent

from pyut.PyutUtils import PyutUtils


if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlFrame import UmlFrame
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

Actions = NewType('Actions', List[Action])

# messages for the status bar

CLICK:    str = 'Click'
LOCATION: str = f'{CLICK} to place the new'
ON:       str = f'{CLICK} on the'

MESSAGES = {
    Action.SELECTOR:                     'Ready',
    Action.NEW_CLASS:                    f'{LOCATION} class',
    Action.NEW_NOTE:                     f'{LOCATION} note',
    Action.NEW_ACTOR:                    f'{LOCATION} actor',
    Action.NEW_TEXT:                     f'{LOCATION} text',
    Action.NEW_USECASE:                  f'{LOCATION} case',
    Action.NEW_SD_INSTANCE:              f'{LOCATION} instance',
    Action.NEW_SD_MESSAGE:               'Click inside the lifeline of the caller',
    Action.DESTINATION_SD_MESSAGE:       'Click inside the lifeline of the message implementer',
    Action.NEW_IMPLEMENT_LINK:           f'{ON} interface implementor',
    Action.NEW_INHERIT_LINK:             f'{ON} subclass',
    Action.NEW_AGGREGATION_LINK:         f'{ON} aggregator',
    Action.NEW_COMPOSITION_LINK:         f'{ON} composer',
    Action.NEW_ASSOCIATION_LINK:         f'{ON} source of the association',
    Action.NEW_NOTE_LINK:                f'{ON} note',
    Action.DESTINATION_IMPLEMENT_LINK:   f'{ON} interface',
    Action.DESTINATION_INHERIT_LINK:     f'{ON} parent class',
    Action.DESTINATION_AGGREGATION_LINK: f'{ON} "aggregated" class',
    Action.DESTINATION_COMPOSITION_LINK: f'{ON} "composed" class',
    Action.DESTINATION_ASSOCIATION_LINK: f'{ON} destination of the association',
    Action.DESTINATION_NOTE_LINK:        f'{ON} class',
    Action.ZOOM_IN:                      'Select the area to zoom in',
    Action.ZOOM_OUT:                     'Select the central point',

}

# a dictionary of the next action to select
NEXT_ACTION = {
    Action.SELECTOR:                 Action.SELECTOR,
    Action.NEW_CLASS:                Action.SELECTOR,
    Action.NEW_NOTE:                 Action.SELECTOR,
    Action.NEW_IMPLEMENT_LINK:          Action.DESTINATION_IMPLEMENT_LINK,
    Action.NEW_INHERIT_LINK:            Action.DESTINATION_INHERIT_LINK,
    Action.NEW_AGGREGATION_LINK:        Action.DESTINATION_AGGREGATION_LINK,
    Action.NEW_COMPOSITION_LINK:        Action.DESTINATION_COMPOSITION_LINK,
    Action.NEW_ASSOCIATION_LINK:        Action.DESTINATION_ASSOCIATION_LINK,
    Action.NEW_NOTE_LINK:               Action.DESTINATION_NOTE_LINK,
    Action.DESTINATION_IMPLEMENT_LINK:  Action.SELECTOR,

    Action.DESTINATION_INHERIT_LINK:     Action.SELECTOR,
    Action.DESTINATION_AGGREGATION_LINK: Action.SELECTOR,
    Action.DESTINATION_COMPOSITION_LINK: Action.SELECTOR,
    Action.DESTINATION_ASSOCIATION_LINK: Action.SELECTOR,
    Action.DESTINATION_NOTE_LINK:        Action.SELECTOR,
    Action.NEW_ACTOR:                    Action.SELECTOR,
    Action.NEW_USECASE:                  Action.SELECTOR,

    Action.NEW_SD_INSTANCE: Action.SELECTOR,
    Action.NEW_SD_MESSAGE:  Action.DESTINATION_SD_MESSAGE,

    Action.ZOOM_IN: Action.ZOOM_IN
}

# list of actions which are source events
SOURCE_ACTIONS: Actions = Actions([
    Action.NEW_IMPLEMENT_LINK,
    Action.NEW_INHERIT_LINK,
    Action.NEW_AGGREGATION_LINK,
    Action.NEW_COMPOSITION_LINK,
    Action.NEW_ASSOCIATION_LINK,
    Action.NEW_NOTE_LINK,
    Action.NEW_SD_MESSAGE,
])

# list of actions which are destination events
DESTINATION_ACTIONS: Actions = Actions([
    Action.DESTINATION_IMPLEMENT_LINK,
    Action.DESTINATION_INHERIT_LINK,
    Action.DESTINATION_AGGREGATION_LINK,
    Action.DESTINATION_COMPOSITION_LINK,
    Action.DESTINATION_ASSOCIATION_LINK,
    Action.DESTINATION_NOTE_LINK,
    Action.DESTINATION_SD_MESSAGE,
    Action.ZOOM_IN,
    Action.ZOOM_OUT
])


# OglLink enumerations according to the current action
LINK_TYPE = {
    Action.DESTINATION_IMPLEMENT_LINK:     PyutLinkType.INTERFACE,
    Action.DESTINATION_INHERIT_LINK:       PyutLinkType.INHERITANCE,
    Action.DESTINATION_AGGREGATION_LINK:   PyutLinkType.AGGREGATION,
    Action.DESTINATION_COMPOSITION_LINK:   PyutLinkType.COMPOSITION,
    Action.DESTINATION_ASSOCIATION_LINK:   PyutLinkType.ASSOCIATION,
    Action.DESTINATION_NOTE_LINK:          PyutLinkType.NOTELINK,
    Action.DESTINATION_SD_MESSAGE:         PyutLinkType.SD_MESSAGE,
}

UML_RELATIONSHIP_ACTIONS: Actions = Actions([
    Action.NEW_INHERIT_LINK,
    Action.NEW_AGGREGATION_LINK,
    Action.NEW_COMPOSITION_LINK,
    Action.NEW_IMPLEMENT_LINK,
    Action.NEW_ASSOCIATION_LINK,
])

UML_RELATIONSHIP_LINK_ACTIONS: Actions = Actions([
    Action.DESTINATION_IMPLEMENT_LINK,
    Action.DESTINATION_INHERIT_LINK,
    Action.DESTINATION_AGGREGATION_LINK,
    Action.DESTINATION_COMPOSITION_LINK,
    Action.DESTINATION_ASSOCIATION_LINK,
])


NONE_OGL_OBJECT: OglObject = cast(OglObject, None)


@dataclass
class ValidationResult:
    isValid:      bool = True
    errorMessage: str = ''


class ActionHandler(Singleton):

    # noinspection PyAttributeOutsideInit
    def init(self, **kwargs):

        self.logger:            Logger           = getLogger(__name__)
        self._eventEngine:      IEventEngine     = kwargs['eventEngine']

        self._currentAction:           Action = Action.SELECTOR
        self._oldAction:               Action = Action.NO_ACTION
        self._currentActionPersistent: bool   = False

        self._dst:    OglObject = NONE_OGL_OBJECT
        self._dstPos: Point     = cast(Point, None)

        self._eventEngine.registerListener(pyEventBinder=EVENT_SET_TOOL_ACTION, callback=self._onSetToolAction)

    @property
    def actionWaiting(self) -> bool:
        """
        Returns: `True` if there's an action waiting to be completed, else `False`
        """
        return self._currentAction != Action.SELECTOR

    @property
    def currentAction(self) -> Action:
        return self._currentAction

    @currentAction.setter
    def currentAction(self, action: Action):
        """
        This tells the action handler which action to do for the next doAction call.

        Args:
            action:  the action from ACTION enumeration
        """
        self.logger.debug(f'Set current action to: {action}')
        if self._currentAction == action:
            self._currentActionPersistent = True
        else:
            # noinspection PyAttributeOutsideInit
            self._currentAction = action
            # noinspection PyAttributeOutsideInit
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
        self.logger.debug(f'doAction: {self._currentAction}  {Action.SELECTOR=}')
        self._resetStatusText()

        handlerStatus: int     = EVENT_PROCESSED
        currentAction: Action  = self._currentAction
        cmd:           Command = cast(Command, None)
        match currentAction:
            case Action.SELECTOR:
                handlerStatus = SKIP_EVENT
            case Action.NEW_CLASS:
                cmd = CommandCreateOglClass(x=x, y=y, eventEngine=self._eventEngine)
            case Action.NEW_TEXT:
                cmd = CommandCreateOglText(x=x, y=y, eventEngine=self._eventEngine)
            case Action.NEW_NOTE:
                cmd = CommandCreateOglNote(x=x, y=y, eventEngine=self._eventEngine)
            case Action.NEW_ACTOR:
                cmd = CommandCreateOglActor(x=x, y=y, eventEngine=self._eventEngine)
            case Action.NEW_USECASE:
                cmd = CommandCreateOglUseCase(x=x, y=y, eventEngine=self._eventEngine)
            case Action.NEW_SD_INSTANCE:
                self._attemptSDInstanceCreation(umlFrame, x, y)
            case Action.ZOOM_IN:
                handlerStatus = SKIP_EVENT
            case Action.ZOOM_OUT:
                self._doZoomOut(umlFrame, x, y)
            case _:
                handlerStatus = SKIP_EVENT
        if cmd is not None:
            self._resetToActionSelector()
            submitStatus: bool = umlFrame.commandProcessor.Submit(command=cmd, storeIt=True)
            self.logger.info(f'Create command submission status: {submitStatus}')

        return handlerStatus

    # noinspection PyAttributeOutsideInit
    def shapeSelected(self, umlDiagramsFrame: 'UmlDiagramsFrame', oglObject: OglObject, position: Point):
        """
        Do action when a shape is selected.

        TODO : support each link type
        Args:
            umlDiagramsFrame:
            oglObject:
            position:
        """
        assert oglObject is not None, 'This should not happen since Ogl layer indirectly sent this event'

        if self._currentAction in SOURCE_ACTIONS:
            self._attemptSourceAction(oglObject, position)
        elif self._currentAction in DESTINATION_ACTIONS:
            self._attemptDestinationAction(oglObject, position, umlDiagramsFrame)
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
        """
        Todo:  This should be moved to a standard action

        Args:
            umlFrame:
            implementor:
            attachmentAnchor:
        """
        attachmentAnchor.setYouAreTheSelectedAnchor()
        cmd: CommandCreateLollipopInterface = CommandCreateLollipopInterface(implementor=implementor,
                                                                             attachmentAnchor=attachmentAnchor,
                                                                             eventEngine=self._eventEngine)

        submitStatus: bool = umlFrame.commandProcessor.Submit(command=cmd, storeIt=True)
        self.logger.info(f'Create command submission status: {submitStatus}')

    def _attemptSourceAction(self, oglObject: OglObject, position: Point):
        """

        Args:
            position:  Where the user clicked on the frame
            oglObject: What he clicked on

        """
        result: ValidationResult = self._validateSourceAction(oglObject=oglObject)
        if result.isValid is True:
            if self._currentActionPersistent:
                self._oldAction = self._currentAction
            self._currentAction = NEXT_ACTION[self._currentAction]

            self.logger.debug(f'Store source - shape {oglObject}  position: {position}')
            self._src    = oglObject
            self._srcPos = position
        else:
            PyutUtils.displayWarning(msg=result.errorMessage, title='Invalid Source')
            self._cancelAction(msg='Invalid Source')

    def _attemptDestinationAction(self, oglObject: OglObject, position: Point, umlDiagramsFrame: 'UmlDiagramsFrame'):
        """

        Args:
            oglObject:
            position:
            umlDiagramsFrame:
        """
        result: ValidationResult = self._validateDestinationAction(oglObject=oglObject)
        if result.isValid is True:
            self._dst    = oglObject
            self._dstPos = position

            self._createLink(umlDiagramsFrame)

            if self._currentActionPersistent:
                self._currentAction = self._oldAction
            else:
                self._currentAction = Action.SELECTOR
                self._selectActionSelectorTool()
        else:
            PyutUtils.displayWarning(msg=result.errorMessage, title='Invalid Destination')
            self._cancelAction(msg='Invalid Destination')

    def _validateSourceAction(self, oglObject: OglObject) -> ValidationResult:

        result: ValidationResult = ValidationResult()

        if self.currentAction == Action.NEW_NOTE_LINK and not isinstance(oglObject, OglNote):
            result.isValid      = False
            result.errorMessage = 'Source of note link must be a note'
        elif self._currentAction == Action.NEW_ASSOCIATION_LINK and isinstance(oglObject, OglActor):
            pass
        elif self._currentAction in UML_RELATIONSHIP_ACTIONS:
            if not isinstance(oglObject, OglClass):
                result.isValid      = False
                result.errorMessage = 'UML relationships must start at a class'

        return result

    def _validateDestinationAction(self, oglObject: OglObject) -> ValidationResult:

        result: ValidationResult = ValidationResult()
        if self._currentAction == Action.DESTINATION_ASSOCIATION_LINK and isinstance(oglObject, OglUseCase):
            pass
        elif self._currentAction in UML_RELATIONSHIP_LINK_ACTIONS:
            if not isinstance(oglObject, OglClass):
                result.isValid      = False
                result.errorMessage = 'UML relationships must end at a class'
        elif self._currentAction == Action.DESTINATION_NOTE_LINK and (isinstance(oglObject, OglNote) or isinstance(oglObject, OglText)):
            result.isValid = False
            result.errorMessage = 'Note to Note or Note to Text\nassociations not allowed'

        return result

    def _cancelAction(self, msg: str):

        self.logger.info(f'{msg}')
        self._currentAction = Action.SELECTOR
        self._selectActionSelectorTool()
        self._setStatusText(f'{msg}')

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

    def _createNewSDInstance(self, umlFrame, x, y):
        """
        TODO:  Make command
        Args:
            umlFrame:
            x:
            y:
        """
        from pyutmodelv2.PyutSDInstance import PyutSDInstance

        instance: PyutSDInstance = umlFrame.createNewSDInstance(x, y)
        if not self._currentActionPersistent:
            self._currentAction = Action.SELECTOR
            self._selectTool(SharedIdentifiers.ID_ARROW)
        dlg = TextEntryDialog(umlFrame, "Instance name", "Enter instance name", instance.instanceName, OK | CANCEL | CENTRE)
        if dlg.ShowModal() == ID_OK:
            instance.instanceName = dlg.GetValue()
        dlg.Destroy()
        umlFrame.Refresh()

    def _createLink(self, umlDiagramsFrame: 'UmlDiagramsFrame'):

        linkType: PyutLinkType = LINK_TYPE[self._currentAction]

        command: CommandCreateOglLink = CommandCreateOglLink(eventEngine=self._eventEngine,
                                                             src=self._src, dst=self._dst,
                                                             linkType=linkType,
                                                             srcPoint=self._srcPos,
                                                             dstPoint=self._dstPos
                                                             )
        umlDiagramsFrame.commandProcessor.Submit(command=command, storeIt=True)
        self._src = NONE_OGL_OBJECT
        self._dst = NONE_OGL_OBJECT

    def _doZoomOut(self, umlFrame, x: int, y: int):
        umlFrame.DoZoomOut(x, y)
        umlFrame.Refresh()
        self.updateTitle()

    def _setStatusText(self, msg: str):
        self._eventEngine.sendEvent(EventType.UpdateApplicationStatus, applicationStatusMsg=msg)

    def _resetStatusText(self):
        self._setStatusText('')

    def _doUpdate(self, projectInformation: MiniProjectInformation):

        self._eventEngine.sendEvent(EventType.UpdateApplicationTitle,
                                    newFilename=projectInformation.projectName,
                                    currentFrameZoomFactor=projectInformation.frameZoom,
                                    projectModified=projectInformation.projectModified)

    def _resetToActionSelector(self):
        """
        For non-persistent tools
        """
        if not self._currentActionPersistent:
            self._currentAction = Action.SELECTOR
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

        self.__createAnchorHints(destinationClass, southX, southY, AttachmentSide.SOUTH, umlFrame)
        self.__createAnchorHints(destinationClass, northX, northY, AttachmentSide.NORTH, umlFrame)
        self.__createAnchorHints(destinationClass, westX, westY,   AttachmentSide.WEST,  umlFrame)
        self.__createAnchorHints(destinationClass, eastX, eastY,   AttachmentSide.EAST,  umlFrame)

    def __createAnchorHints(self, destinationClass: OglClass, anchorX: int, anchorY: int, attachmentSide: AttachmentSide, umlFrame):

        anchorHint: SelectAnchorPoint = SelectAnchorPoint(x=anchorX, y=anchorY, attachmentSide=attachmentSide, parent=destinationClass)
        anchorHint.protected = True

        destinationClass.AddAnchorPoint(anchorHint)
        umlFrame.getDiagram().AddShape(anchorHint)
