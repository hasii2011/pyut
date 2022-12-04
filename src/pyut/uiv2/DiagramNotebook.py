
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
from wx import NO_IMAGE
from wx import OK

from wx import Command
from wx import CommandProcessor
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
from ogl.OglText import OglText

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from pyut.ui.umlframes.UmlFrame import UmlObject
from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.ui.wxcommands.CommandDeleteOglClass import CommandDeleteOglClass
from pyut.ui.wxcommands.CommandDeleteOglLink import CommandDeleteOglLink
from pyut.ui.wxcommands.CommandDeleteOglNote import CommandDeleteOglNote
from pyut.ui.wxcommands.CommandDeleteOglText import CommandDeleteOglText
from pyut.ui.wxcommands.Types import DoableObjectType

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

    def __init__(self, parentWindow: Window, eventEngine: IEventEngine, commandProcessor: CommandProcessor):
        """

        Args:
            parentWindow:   Our hosting window
            eventEngine:    The Pyut Event Engine
            commandProcessor:  The Pyut command processor to support do, undo, and redo
        """

        super().__init__(parentWindow, ID_ANY, style=CLIP_CHILDREN)

        self._eventEngine:      IEventEngine     = eventEngine
        self._commandProcessor: CommandProcessor = commandProcessor

        self.logger:     Logger      = getLogger(__name__)
        self._clipboard: PyutObjects = PyutObjects([])            # will be re-created at every copy

        self._eventEngine.registerListener(pyEventBinder=EVENT_SELECT_ALL_SHAPES,   callback=self._onSelectAllShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_DESELECT_ALL_SHAPES, callback=self._onDeSelectAllShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_COPY_SHAPES,         callback=self._onCopy)
        self._eventEngine.registerListener(pyEventBinder=EVENT_PASTE_SHAPES,        callback=self._onPaste)
        self._eventEngine.registerListener(pyEventBinder=EVENT_CUT_SHAPES,          callback=self._onCutSelectedShapes)
        self._eventEngine.registerListener(pyEventBinder=EVENT_UNDO,                callback=self._onUndo)
        self._eventEngine.registerListener(pyEventBinder=EVENT_REDO,                callback=self._onRedo)
        self._eventEngine.registerListener(pyEventBinder=EVENT_CUT_SHAPE,           callback=self._onCutShape)    # TODO:  I do not think this is used anymore

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
        Remove any selected objects from the current frame

        Args:
            event:
        """
        umlFrame: UmlDiagramsFrame = self.currentNotebookFrame
        if umlFrame is not None:
            selectedShapes = umlFrame.GetSelectedShapes()       # TODO Not reliable
            self._doCut(objectsToCut=selectedShapes)

    # noinspection PyUnusedLocal
    def _onUndo(self, event: UndoEvent):
        """
        Args:
            event:
        """
        currentFrame: UmlDiagramsFrame = self.currentNotebookFrame
        if currentFrame is None:
            self._displayWarning(message='No selected/available frame')
        else:
            currentFrame.undo()

    # noinspection PyUnusedLocal
    def _onRedo(self, event: RedoEvent):
        """
        Args:
            event:
        """
        currentFrame: UmlDiagramsFrame = self.currentNotebookFrame
        if currentFrame is None:
            self._displayWarning(message='No selected/available frame')
        else:
            currentFrame.redo()

    def _updateApplicationStatus(self, statusMessage: str):

        self._eventEngine.sendEvent(eventType=EventType.UpdateApplicationStatus, applicationStatusMsg=statusMessage)

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
            diagram: Diagram         = frame.diagram
            shapes:  List[OglObject] = diagram.GetShapes()
            for oglShape in shapes:
                shape: OglObject = cast(OglObject, oglShape)
                shape.SetSelected(selectValue)

            frame.Refresh()

    def _doCut(self, objectsToCut: UmlObjects):
        """
        The common cut code;  No need to check valid UML frame because ._onCutSelectedShapes
        validated it and the event CutShape came from an open frame

        Args:
            objectsToCut:
        """
        umlFrame: UmlDiagramsFrame = self.currentNotebookFrame

        for shape in objectsToCut:
            cmd: Command = self._createDeleteCommand(cast(DoableObjectType, shape))
            if cmd is None:
                shape.Detach()
                umlFrame.Refresh()
            else:
                submitStatus: bool = self._commandProcessor.Submit(command=cmd, storeIt=True)
                self.logger.warning(f'{submitStatus=}')

        self._eventEngine.sendEvent(EventType.UMLDiagramModified)   # will also cause title to be updated

    def _createDeleteCommand(self, shape: DoableObjectType) -> Command:
        """
        TODO:  Update to support OglInterface2, OglUseCase, OglActor

        If no command type exists for the input shape log a warning

        Args:
            shape:

        Returns:  A command to submit or None;
        """
        cmd: Command = cast(Command, None)
        match shape:
            case OglClass() as shape:
                cmd = CommandDeleteOglClass(oglClass=shape, eventEngine=self._eventEngine)
            case OglText() as shape:
                cmd = CommandDeleteOglText(oglText=shape, eventEngine=self._eventEngine)
            case OglNote() as shape:
                cmd = CommandDeleteOglNote(oglNote=shape, eventEngine=self._eventEngine)
            case OglLink() as shape:
                oglLink:  OglLink     = cast(OglLink, shape)
                cmd = CommandDeleteOglLink(oglLink=oglLink, eventEngine=self._eventEngine)
            case _:
                self.logger.warning(f'No history generated for shape type: {shape}')
        return cmd

    def _displayWarning(self, message: str):
        self._displayMessage(message=message, caption='Huh?', iconType=ICON_WARNING)

    def _displayError(self, message: str):
        self._displayMessage(message=message, caption='Error!', iconType=ICON_ERROR)

    def _displayMessage(self, caption: str, message: str, iconType: int):
        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption=caption, style=OK | iconType)
        booBoo.ShowModal()
