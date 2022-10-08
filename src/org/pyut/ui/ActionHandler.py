
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from org.pyut.ui.Actions import ACTION_DESTINATION_AGGREGATION_LINK
from org.pyut.ui.Actions import ACTION_DESTINATION_ASSOCIATION_LINK
from org.pyut.ui.Actions import ACTION_DESTINATION_COMPOSITION_LINK
from org.pyut.ui.Actions import ACTION_DESTINATION_IMPLEMENT_LINK
from org.pyut.ui.Actions import ACTION_DESTINATION_INHERIT_LINK
from org.pyut.ui.Actions import ACTION_DESTINATION_NOTE_LINK
from org.pyut.ui.Actions import ACTION_DESTINATION_SD_MESSAGE
from org.pyut.ui.Actions import ACTION_NEW_ACTOR
from org.pyut.ui.Actions import ACTION_NEW_AGGREGATION_LINK
from org.pyut.ui.Actions import ACTION_NEW_ASSOCIATION_LINK
from org.pyut.ui.Actions import ACTION_NEW_CLASS
from org.pyut.ui.Actions import ACTION_NEW_COMPOSITION_LINK
from org.pyut.ui.Actions import ACTION_NEW_IMPLEMENT_LINK
from org.pyut.ui.Actions import ACTION_NEW_INHERIT_LINK
from org.pyut.ui.Actions import ACTION_NEW_NOTE
from org.pyut.ui.Actions import ACTION_NEW_NOTE_LINK
from org.pyut.ui.Actions import ACTION_NEW_SD_INSTANCE
from org.pyut.ui.Actions import ACTION_NEW_SD_MESSAGE
from org.pyut.ui.Actions import ACTION_NEW_TEXT
from org.pyut.ui.Actions import ACTION_NEW_USECASE
from org.pyut.ui.Actions import ACTION_SELECTOR
from org.pyut.ui.Actions import ACTION_ZOOM_IN
from org.pyut.ui.Actions import ACTION_ZOOM_OUT

from org.pyut.ui.tools.SharedIdentifiers import SharedIdentifiers

from org.pyut.uiv2.eventengine.CurrentProjectInformation import CurrentProjectInformation
from org.pyut.uiv2.eventengine.Events import EVENT_SET_TOOL_ACTION
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.Events import SetToolActionEvent
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from org.pyut.ui.umlframes.UmlFrame import UmlFrame

from miniogl.Constants import EVENT_PROCESSED
from miniogl.Constants import SKIP_EVENT

from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutText import PyutText

from wx import CANCEL
from wx import CENTRE
from wx import ID_ANY
from wx import OK
from wx import TextEntryDialog

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.DlgAbout import ID_OK
from org.pyut.dialogs.DlgEditUseCase import DlgEditUseCase
from org.pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from org.pyut.dialogs.textdialogs.DlgEditText import DlgEditText
from org.pyut.ui.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler

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


class ActionHandler:

    def __init__(self, eventEngine: IEventEngine):

        self.logger:       Logger       = getLogger(__name__)
        self._eventEngine: IEventEngine = eventEngine

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

    def _onSetToolAction(self, event: SetToolActionEvent):
        self.currentAction = event.action

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
                self._selectTool(SharedIdentifiers.ID_ARROW)
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
                from org.pyut.ui.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame
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

    def _createOglClass(self, umlFrame, x: int, y: int):

        from org.pyut.history.commands.CreateOglClassCommand import CreateOglClassCommand
        from org.pyut.history.commands.CommandGroup import CommandGroup

        cmd:   CreateOglClassCommand = CreateOglClassCommand(x, y)
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

    def _resetStatusText(self):
        pass        # TODO send event

    def updateTitle(self):
        """
        Set the application title, function of version and current project name
        """

        self._eventEngine.sendEvent(EventType.GetProjectInformation, callback=self._doUpdate)
        # from org.pyut.uiv2.IPyutProject import IPyutProject
        #
        # # Get filename
        # project: IPyutProject = self._treeNotebookHandler.currentProject
        # if project is not None:
        #     filename = project.filename
        # else:
        #     filename = ""
        #
        # pyutVersion: str = PyutVersion.getPyUtVersion()
        # # Set text
        # # txt = "PyUt v" + pyutVersion + " - " + filename
        # txt: str = f'Pyut v{pyutVersion}- {filename}'
        # if (project is not None) and (project.modified is True):
        #     if self._treeNotebookHandler.currentFrame is not None:
        #         zoom = self._treeNotebookHandler.currentFrame.GetCurrentZoom()
        #     else:
        #         zoom = 1
        #
        #     txt = txt + f' ( {int(zoom * 100)}%) *'
        #
        # # self._appFrame.SetTitle(txt)      TODO: send message

    def _doUpdate(self, projectInformation: CurrentProjectInformation):
        pass

    def _resetToActionSelector(self):
        """
        For non-persistent tools
        """
        if not self._currentActionPersistent:
            self._currentAction = ACTION_SELECTOR
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
