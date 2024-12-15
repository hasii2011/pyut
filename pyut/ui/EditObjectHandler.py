
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import ID_OK
from wx import OK

from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutUseCase import PyutUseCase
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.SizerShape import SizerShape
from miniogl.TextShape import TextShape

from ogl.sd.OglSDMessage import OglSDMessage
from ogl.sd.OglSDInstance import OglSDInstance

from ogl.OglInheritance import OglInheritance
from ogl.OglText import OglText
from ogl.OglClass import OglClass
from ogl.OglNote import OglNote
from ogl.OglUseCase import OglUseCase
from ogl.OglActor import OglActor
from ogl.OglAssociation import OglAssociation
from ogl.OglInterface import OglInterface
from ogl.OglInterface2 import OglInterface2
from ogl.OglObject import OglObject

from pyut.ui.wxcommands.CommandModify import CommandModify
from pyut.ui.wxcommands.CommandModify import Parameters

from pyut.uiv2.dialogs.DlgEditClass import DlgEditClass
from pyut.uiv2.dialogs.DlgEditLink import DlgEditLink
from pyut.uiv2.dialogs.DlgEditInterface import DlgEditInterface

from pyut.uiv2.dialogs.Wrappers import DlgEditSDInstanceName
from pyut.uiv2.dialogs.Wrappers import DlgEditSDMessage
from pyut.uiv2.dialogs.Wrappers import DlgEditActor
from pyut.uiv2.dialogs.Wrappers import DlgEditUseCase

from pyut.uiv2.dialogs.textdialogs.DlgEditNote import DlgEditNote
from pyut.uiv2.dialogs.textdialogs.DlgEditText import DlgEditText

from pyut.ui.umlframes.UmlFrame import UmlFrame
from pyut.ui.umlframes.UmlFrame import UmlObjects
from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.PyutUtils import PyutUtils


class EditObjectHandler:
    """

    """

    def __init__(self, eventEngine: IEventEngine):

        self.logger:       Logger       = getLogger(__name__)
        self._eventEngine: IEventEngine = eventEngine

        self._x: int = -1
        self._y: int = -1

    def editObject(self, x: int, y: int):

        self._x = x
        self._y = y
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrame)

    def _cbGetActiveUmlFrame(self, umlFrame: UmlDiagramsFrame):

        self.logger.info(f'{umlFrame=}')

        self._doEditObject(x=self._x, y=self._y, umlFrame=umlFrame)

    def _doEditObject(self, x: int, y: int, umlFrame: UmlDiagramsFrame):
        """
        Edit the object at x, y.
        """
        diagramShape = umlFrame.FindShape(x, y)

        if diagramShape is None:
            return

        match diagramShape:
            case OglClass() as diagramShape:
                self._editClass(umlFrame, diagramShape)
            case OglInterface2() as diagramShape:
                self._editOglInterface2(umlFrame, diagramShape)
            case  OglText() as diagramShape:
                self._editText(umlFrame, diagramShape)
            case OglNote() as diagramShape:
                self._editNote(umlFrame, diagramShape)
            case OglUseCase() as diagramShape:
                self._editUseCase(umlFrame, diagramShape)
            case OglActor() as diagramShape:
                self._editActor(umlFrame, diagramShape)
            case OglAssociation() as diagramShape:
                self._editAssociation(umlFrame, diagramShape)
            case OglSDInstance() as diagramShape:
                self._editSDInstanceName(umlFrame, diagramShape)
            case OglSDMessage() as diagramShape:
                self._editSDMessage(umlFrame, diagramShape)
            case OglInheritance() | OglInterface() | AnchorPoint() | ControlPoint() | SizerShape() | TextShape():
                pass    # Nothing to edit on inheritance or interface relationships
            case _:
                self.logger.error(f'Unknown shape')
                PyutUtils.displayError(msg=f'EditObjectHandler: Unknown shape: {diagramShape}', title='Developer Error')
        umlFrame.Refresh()

    def _editClass(self, umlFrame: UmlDiagramsFrame, diagramShape: OglObject):
        pyutClass: PyutClass = diagramShape.pyutObject
        with DlgEditClass(umlFrame, self._eventEngine, pyutClass) as dlg:
            if dlg.ShowModal() == OK:
                self._autoResize(umlFrame, diagramShape)
                # This dialog sends the modified event

    def _editOglInterface2(self, umlFrame: UmlDiagramsFrame, lollipop: OglInterface2):

        pyutInterface: PyutInterface = lollipop.pyutInterface

        editMode: bool = True
        if len(pyutInterface.name) == 0:
            editMode = False

        with DlgEditInterface(umlFrame, self._eventEngine, lollipop, editMode=editMode) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.info(f'{dlg.pyutInterface.name=}')
                lollipop.pyutInterface = dlg.pyutInterface
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editText(self, umlFrame: UmlDiagramsFrame, diagramShape: OglObject):

        oglText:  OglText  = cast(OglText, diagramShape)
        pyutText: PyutText = oglText.pyutText

        cmdModify: CommandModify = CommandModify(name='Undo Edit Text', anyObject=pyutText, eventEngine=self._eventEngine)
        cmdModify.methodName       = 'content'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([pyutText.content])
        with DlgEditText(parent=umlFrame, pyutText=pyutText) as dlg:
            if dlg.ShowModal() == OK:
                cmdModify.newParameters = Parameters([pyutText.content])
                self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editNote(self, umlFrame: UmlDiagramsFrame, oglNote: OglNote):

        pyutNote: PyutNote = oglNote.pyutObject

        cmdModify: CommandModify = CommandModify(name='Undo Note Text', anyObject=pyutNote, eventEngine=self._eventEngine)
        cmdModify.methodName       = 'content'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([pyutNote.content])

        with DlgEditNote(umlFrame, pyutNote=pyutNote) as dlg:
            if dlg.ShowModal() == OK:
                cmdModify.newParameters = Parameters([pyutNote.content])
                self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editUseCase(self, umlFrame: UmlDiagramsFrame, oglUseCase: OglUseCase):

        pyutUseCase: PyutUseCase   = oglUseCase.pyutObject
        cmdModify:   CommandModify = CommandModify(name='Undo Note Text', anyObject=pyutUseCase, eventEngine=self._eventEngine)
        cmdModify.methodName       = 'name'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([pyutUseCase.name])

        with DlgEditUseCase(umlFrame, useCaseName=pyutUseCase.name) as dlg:
            ans: int = dlg.ShowModal()
            if ans == ID_OK:
                cmdModify.newParameters = Parameters([dlg.GetValue()])
                self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editActor(self, umlFrame: UmlDiagramsFrame, oglActor: OglActor):

        pyutActor:   PyutActor     = oglActor.pyutObject
        cmdModify:   CommandModify = CommandModify(name='Undo Actor Name', anyObject=pyutActor, eventEngine=self._eventEngine)
        cmdModify.methodName       = 'name'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([pyutActor.name])

        with DlgEditActor(umlFrame, actorName=pyutActor.name) as dlg:
            if dlg.ShowModal() == ID_OK:
                cmdModify.newParameters = Parameters([dlg.GetValue()])
                self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editAssociation(self, umlFrame: UmlFrame, oglAssociation: OglAssociation):

        pyutLink:    PyutLink      = oglAssociation.pyutObject
        oldPyutLink: PyutLink      = deepcopy(pyutLink)
        cmdModify:   CommandModify = CommandModify(name='Undo Link Edit', anyObject=oglAssociation, eventEngine=self._eventEngine)
        cmdModify.methodName       = 'pyutObject'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([oldPyutLink])

        with DlgEditLink(None, oglAssociation.pyutObject) as dlg:
            if dlg.ShowModal() == OK:
                cmdModify.newParameters = Parameters([dlg.value])
                self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)   # don't do this in Pyut

    # def _editSDInstanceName(self, umlFrame: UmlFrame, oglSDInstance: OglSDInstance):
    #     pyutSDInstance:    PyutSDInstance = oglSDInstance.pyutObject
    #     cmdModify:         CommandModify  = CommandModify(name='Undo Instance Name', anyObject=pyutSDInstance, eventEngine=self._eventEngine)
    #     cmdModify.methodName       = 'instanceName'
    #     cmdModify.methodIsProperty = True
    #     cmdModify.oldParameters    = Parameters([pyutSDInstance.instanceName])
    #
    #     with DlgEditSDInstanceName(umlFrame, instanceName=pyutSDInstance.instanceName) as dlg:
    #         if dlg.ShowModal() == ID_OK:
    #             cmdModify.newParameters = Parameters([dlg.GetValue()])
    #             self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
    #             self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editSDInstanceName(self, umlFrame: UmlFrame, oglSDInstance: OglSDInstance):

        pyutSDInstance:    PyutSDInstance = oglSDInstance.pyutSDInstance
        cmdModify:         CommandModify  = CommandModify(name='Undo Instance Name', anyObject=oglSDInstance, eventEngine=self._eventEngine)
        cmdModify.methodName       = 'pyutSDInstance'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([pyutSDInstance])

        with DlgEditSDInstanceName(umlFrame, instanceName=pyutSDInstance.instanceName) as dlg:
            if dlg.ShowModal() == ID_OK:

                newPyutSDInstance: PyutSDInstance = PyutSDInstance()
                newPyutSDInstance.instanceGraphicalType  = pyutSDInstance.instanceGraphicalType
                newPyutSDInstance.instanceLifeLineLength = pyutSDInstance.instanceLifeLineLength
                newPyutSDInstance.instanceName           = dlg.GetValue()

                cmdModify.newParameters = Parameters([newPyutSDInstance])
                self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editSDMessage(self, umlFrame: UmlFrame, oglSDMessage: OglSDMessage):
        pyutSDMessage: PyutSDMessage = oglSDMessage.pyutSDMessage
        cmdModify:     CommandModify = CommandModify(name='Undo SD Message', anyObject=pyutSDMessage, eventEngine=self._eventEngine)
        cmdModify.methodName       = 'message'
        cmdModify.methodIsProperty = True
        cmdModify.oldParameters    = Parameters([pyutSDMessage.message])

        with DlgEditSDMessage(umlFrame, messageName=pyutSDMessage.message) as dlg:
            if dlg.ShowModal() == ID_OK:
                cmdModify.newParameters = Parameters([dlg.GetValue()])
                self._submitModifyCommand(umlFrame=umlFrame, cmdModifyCommand=cmdModify)
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _autoResize(self, umlFrame: UmlDiagramsFrame, obj: OglObject):
        """
        Auto-resize the given object.

        Args:
            umlFrame
            obj:

        """
        prefs: PyutPreferences = PyutPreferences()

        if prefs.autoResizeShapesOnEdit is True:
            if isinstance(obj, PyutClass):
                po = [po for po in self._getUmlObjects(umlFrame) if isinstance(po, OglClass) and po.pyutObject is obj]
                obj = po[0]

            obj.autoResize()

    def _getUmlObjects(self, umlFrame: UmlFrame) -> UmlObjects:
        """
        The frame may contain no UML shapes.

        Returns: Return the list of UmlObjects in the diagram.
        """
        from pyut.ui.umlframes.UmlFrame import UmlObjects

        return cast(UmlObjects, umlFrame.umlObjects)

    def _submitModifyCommand(self, umlFrame: UmlFrame, cmdModifyCommand: CommandModify):
        umlFrame.commandProcessor.Submit(command=cmdModifyCommand)
