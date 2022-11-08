
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from copy import copy

from wx import CLIP_CHILDREN
from wx import EVT_CLOSE
from wx import ICON_ERROR
from wx import ICON_WARNING
from wx import ID_ANY
from wx import ID_YES
from wx import NO_IMAGE
from wx import OK

from wx import MessageDialog
from wx import Notebook
from wx import Window

from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutObject import PyutObject
from pyutmodel.PyutUseCase import PyutUseCase

from miniogl.Diagram import Diagram

from ogl.OglActor import OglActor
from ogl.OglClass import OglClass
from ogl.OglUseCase import OglUseCase
from ogl.OglNote import OglNote
from ogl.OglObject import OglObject
from ogl.OglLink import OglLink

from pyut.dialogs.DlgRemoveLink import DlgRemoveLink

from pyut.history.commands.Command import Command
from pyut.history.commands.CommandGroup import CommandGroup
from pyut.history.commands.DeleteOglClassCommand import DeleteOglClassCommand
from pyut.history.commands.DeleteOglNoteCommand import DeleteOglNoteCommand
from pyut.history.commands.DeleteOglObjectCommand import DeleteOglObjectCommand
from pyut.history.commands.DelOglLinkCommand import DelOglLinkCommand

from org.pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.ui.umlframes.UmlFrame import UmlObject
from org.pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.uiv2.eventengine.Events import EVENT_COPY_SHAPES
from pyut.uiv2.eventengine.Events import EVENT_CUT_SHAPES
from pyut.uiv2.eventengine.Events import EVENT_PASTE_SHAPES
from pyut.uiv2.eventengine.Events import EVENT_SELECT_ALL_SHAPES
from pyut.uiv2.eventengine.Events import EVENT_REDO
from pyut.uiv2.eventengine.Events import EVENT_UNDO
from pyut.uiv2.eventengine.Events import EVENT_CUT_SHAPE
from pyut.uiv2.eventengine.Events import EVENT_DESELECT_ALL_SHAPES

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.Events import CutShapesEvent
from pyut.uiv2.eventengine.Events import CopyShapesEvent
from pyut.uiv2.eventengine.Events import PasteShapesEvent
from pyut.uiv2.eventengine.Events import SelectAllShapesEvent
from pyut.uiv2.eventengine.Events import RedoEvent
from pyut.uiv2.eventengine.Events import UndoEvent
from pyut.uiv2.eventengine.Events import CutShapeEvent
from pyut.uiv2.eventengine.Events import DeSelectAllShapesEvent


PyutObjects = NewType('PyutObjects', List[PyutObject])


class DiagramNotebook(Notebook):

    def __init__(self, parentWindow: Window, eventEngine: IEventEngine):

        super().__init__(parentWindow, ID_ANY, style=CLIP_CHILDREN)

        self._eventEngine: IEventEngine = eventEngine
        self.logger:       Logger       = getLogger(__name__)

        self._clipboard: PyutObjects = PyutObjects([])            # will be re-created at every copy and cut

        self._eventEngine.registerListener(pyEventBinder=EVENT_SELECT_ALL_SHAPES,   callback=self._onSelectAllShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_DESELECT_ALL_SHAPES, callback=self._onDeSelectAllShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_COPY_SHAPES,         callback=self._onCopy)
        self._eventEngine.registerListener(pyEventBinder=EVENT_PASTE_SHAPES,        callback=self._onPaste)
        self._eventEngine.registerListener(pyEventBinder=EVENT_CUT_SHAPES,          callback=self._onCutSelectedShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_UNDO,                callback=self._onUndo)
        self._eventEngine.registerListener(pyEventBinder=EVENT_REDO,                callback=self._onRedo)
        self._eventEngine.registerListener(pyEventBinder=EVENT_CUT_SHAPE,           callback=self._onCutShape)

        self.Bind(EVT_CLOSE, self.Close)

    @property
    def currentNotebookFrame(self) -> UmlDiagramsFrame:
        """
        Get the current frame in the notebook;  May

        Returns:  A UML Diagrams Frame or None
        """
        frame = self.GetCurrentPage()
        return frame

    @property
    def umlObjects(self) -> UmlObjects:
        """
        May be empty

        Returns: Return the list of UmlObjects in the diagram.
        """
        umlFrame:   UmlDiagramsFrame = self.currentNotebookFrame
        umlObjects: UmlObjects       = UmlObjects([])
        if umlFrame is not None:
            umlObjects = umlFrame.getUmlObjects()

        return umlObjects

    @property
    def selectedUmlObjects(self) -> UmlObjects:
        """
        Return the list of selected OglObjects in the diagram.

        Returns:  May be empty
        """
        umlObjects:      UmlObjects = self.umlObjects
        selectedObjects: UmlObjects = UmlObjects([])

        if umlObjects is not None:
            for umlObject in umlObjects:
                if umlObject.IsSelected():
                    selectedObjects.append(umlObject)

        return selectedObjects

    def AddPage(self, page, text, select=False, imageId=NO_IMAGE):
        """
        Override so we can catch double add;  Originally for debugging

        Args:
            page:
            text:
            select:
            imageId:
        """
        super().AddPage(page, text, select, imageId)

    # noinspection PyUnusedLocal
    def _onSelectAllShapes(self, event: SelectAllShapesEvent):
        """
        Select all Ogl shapes on the current frame
        """
        self._setShapeSelected(True)

    # noinspection PyUnusedLocal
    def _onDeSelectAllShapes(self, event: DeSelectAllShapesEvent):
        self._setShapeSelected(False)

    # noinspection PyUnusedLocal
    def _onCopy(self, event: CopyShapesEvent):
        """
        Copy the selected UML Objects into an internal clipboard

        TODO : adapt for OglLinks

        Args:
            event:
        """
        selectedUmlObjects: UmlObjects = self.selectedUmlObjects
        if len(selectedUmlObjects) > 0:
            self._clipboard = PyutObjects([])
            # put a copy of the PyutObjects in the clipboard
            for umlObject in selectedUmlObjects:
                if isinstance(umlObject, OglClass):
                    umlObjectCopy = copy(umlObject.pyutObject)
                    umlObjectCopy.setLinks([])              # we don't want to copy the links
                    self._clipboard.append(umlObjectCopy)

            self._updateApplicationStatus(f'Copied {len(self._clipboard)} objects')

    # noinspection PyUnusedLocal
    def _onPaste(self, event: PasteShapesEvent):
        """
        Paste any objects in the internal clipboard to the current frame
        Args:
            event:
        """

        if len(self._clipboard) == 0:
            return

        self.logger.info(f'Pasting {len(self._clipboard)} objects')
        if self.currentNotebookFrame is None:
            self._displayError("No frame to paste into")
            return

        # put the objects in the clipboard and remove them from the diagram
        x: int = 100
        y: int = 100
        numbObjectsPasted: int = 0
        for clipboardObject in self._clipboard:
            pyutObject: PyutObject = copy(clipboardObject)
            oglObject:  OglObject  = cast(OglObject, None)
            match pyutObject:
                case PyutClass() as pyutObject:
                    oglObject = OglClass(cast(PyutClass, pyutObject))
                case PyutNote() as pyutObject:
                    oglObject = OglNote(pyutObject)
                case PyutActor() as pyutObject:
                    oglObject = OglActor(pyutObject)
                case PyutUseCase() as pyutObject:
                    oglObject = OglUseCase(pyutObject)
                case _:
                    self.logger.warning(f'Pasting object: {pyutObject} not supported')

            if oglObject is not None:
                self.logger.info(f'Pasting: {oglObject=}')
                self.currentNotebookFrame.addShape(oglObject, x, y)
                numbObjectsPasted += 1
                x += 20
                y += 20

        self.currentNotebookFrame.Refresh()

        self._eventEngine.sendEvent(EventType.UMLDiagramModified)   # will also cause title to be updated
        self._updateApplicationStatus(f'Pasted {numbObjectsPasted} objects')

    def _onCutShape(self, event: CutShapeEvent):

        umlObject:  UmlObject  = event.shapeToCut
        umlObjects: UmlObjects = UmlObjects([umlObject])
        self._doCut(objectsToCut=umlObjects)

    # noinspection PyUnusedLocal
    def _onCutSelectedShapes(self, event: CutShapesEvent):
        """
        Remove any selected objects from the current frame and save them in the
        internal clipboard

        Args:
            event:
        """
        umlFrame: UmlDiagramsFrame = self.currentNotebookFrame
        if umlFrame is not None:
            selectedShapes = umlFrame.GetSelectedShapes()
            self._doCut(objectsToCut=selectedShapes)

    # noinspection PyUnusedLocal
    def _onUndo(self, event: UndoEvent):
        """
        Args:
            event:
        """
        from pyut.history.HistoryManager import HistoryManager

        currentFrame: UmlDiagramsFrame = self.currentNotebookFrame
        if currentFrame is None:
            self._displayWarning(message='No selected/available frame')
        else:
            historyManager: HistoryManager = currentFrame.getHistory()
            if historyManager.isUndoPossible() is True:
                historyManager.undo()
            else:
                self._displayWarning(message='Nothing to undo')

    # noinspection PyUnusedLocal
    def _onRedo(self, event: RedoEvent):
        """
        Args:
            event:
        """
        from pyut.history.HistoryManager import HistoryManager

        currentFrame: UmlDiagramsFrame = self.currentNotebookFrame
        if currentFrame is None:
            self._displayWarning(message='No selected/available frame')
        else:
            historyManager: HistoryManager = currentFrame.getHistory()
            if historyManager.isRedoPossible() is True:
                historyManager.redo()
            else:
                self._displayWarning(message='Nothing to redo')

    def _updateApplicationStatus(self, statusMessage: str):

        self._eventEngine.sendEvent(eventType=EventType.UpdateApplicationStatus, applicationStatusMsg=statusMessage)

    def _deleteShapeFromFrame(self, oglObjectToDelete: UmlObject, cmdGroup: CommandGroup) -> CommandGroup:
        """
        This is the common method to delete a shape from a UML frame. In addition, this method
        adds the appropriate history commands in order to support undo

        Args:
            oglObjectToDelete:  The Ogl object to remove from the frame
            cmdGroup:   The command group to update with an appropriate delete command

        Returns:    The updated command group
        """
        if isinstance(oglObjectToDelete, OglClass):

            oglClass: OglClass = cast(OglClass, oglObjectToDelete)
            cmd: DeleteOglClassCommand = DeleteOglClassCommand(oglClass)
            cmdGroup.addCommand(cmd)
            links = oglClass.links
            for link in links:
                cmdGroup = self._addADeleteLinkCommand(oglLink=link, cmdGroup=cmdGroup)

        elif isinstance(oglObjectToDelete, OglNote):
            oglNote: 'OglNote' = cast(OglNote, oglObjectToDelete)
            delNoteCmd: DeleteOglNoteCommand = DeleteOglNoteCommand(oglNote)
            cmdGroup.addCommand(delNoteCmd)

        elif isinstance(oglObjectToDelete, OglLink):
            oglLink: OglLink = cast(OglLink, oglObjectToDelete)
            cmdGroup = self._addADeleteLinkCommand(oglLink=oglLink, cmdGroup=cmdGroup)

        elif isinstance(oglObjectToDelete, OglObject):
            delObjCmd: DeleteOglObjectCommand = DeleteOglObjectCommand(oglObjectToDelete)
            cmdGroup.addCommand(delObjCmd)

        else:
            assert False, 'Unknown OGL Object'

        oglObjectToDelete.Detach()

        return cmdGroup

    def _addADeleteLinkCommand(self, oglLink: OglLink, cmdGroup: CommandGroup) -> CommandGroup:

        delOglLinkCmd: DelOglLinkCommand = DelOglLinkCommand(oglLink)
        cmdGroup.addCommand(delOglLinkCmd)

        return cmdGroup

    def _createDeleteCommand(self, shape: OglObject, umlFrame: UmlDiagramsFrame) -> Command:
        """
        TODO:  Fix to support OglInterface2
        Args:
            shape:
            umlFrame:

        Returns:  The created command;  May be none (e.g. OglInterface2)
        """

        cmd: Command = cast(Command, None)
        match shape:
            case OglClass() as shape:
                cmd = DeleteOglClassCommand(shape)
            case OglObject() as shape:
                cmd = DeleteOglObjectCommand(shape)
            case OglLink() as shape:
                dlg: DlgRemoveLink = DlgRemoveLink(shape.__str__())  # TODO depends on https://github.com/hasii2011/ogl/issues/18
                resp = dlg.ShowModal()
                dlg.Destroy()
                if resp == ID_YES:
                    cmd = DelOglLinkCommand(shape)
            case _:
                self.logger.warning(f'No history generated for shape type: {shape}')
                shape.Detach()
                umlFrame.Refresh()

        return cmd

    def _setShapeSelected(self, selectValue: bool):
        """
        Set the current frames selected value to `selectValue`
        Args:
            selectValue:    Either `True` or `False`

        """
        frame: UmlDiagramsFrame = self.GetCurrentPage()

        if frame is None:
            self._displayError("No frame found !")
        else:
            diagram: Diagram         = frame.GetDiagram()
            shapes:  List[OglObject] = diagram.GetShapes()
            for oglShape in shapes:
                shape: OglObject = cast(OglObject, oglShape)
                shape.SetSelected(selectValue)

            frame.Refresh()

    def _doCut(self, objectsToCut: UmlObjects):
        """
        The common cut code;  No need to check valid UML frame because ._onCutSelectedShapes
        validated it and the event CutShape from an open frame

        Args:
            objectsToCut:
        """
        cmdGroup:     CommandGroup = CommandGroup("Delete UML object(s)")
        cmdGroupInit: bool         = False

        umlFrame: UmlDiagramsFrame = self.currentNotebookFrame

        for shape in objectsToCut:
            cmd: Command = self._createDeleteCommand(cast(OglObject, shape), umlFrame)
            if cmd is not None:
                cmdGroup.addCommand(cmd)
                cmdGroupInit = True

        if cmdGroupInit is True:
            umlFrame.getHistory().addCommandGroup(cmdGroup)
            umlFrame.getHistory().execute()
        self._eventEngine.sendEvent(EventType.UMLDiagramModified)   # will also cause title to be updated

    def _displayWarning(self, message: str):
        self._displayMessage(message=message, caption='Huh?', iconType=ICON_WARNING)

    def _displayError(self, message: str):
        self._displayMessage(message=message, caption='Error!', iconType=ICON_ERROR)

    def _displayMessage(self, caption: str, message: str, iconType: int):
        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption=caption, style=OK | iconType)
        booBoo.ShowModal()
