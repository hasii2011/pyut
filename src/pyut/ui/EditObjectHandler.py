
from typing import TYPE_CHECKING
from typing import cast

from logging import Logger
from logging import getLogger

from wx import OK

from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutUseCase import PyutUseCase
from pyutmodel.PyutNote import PyutNote

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.SizerShape import SizerShape

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

from pyut.uiv2.dialogs.DlgEditClass import DlgEditClass
from pyut.uiv2.dialogs.DlgEditLink import DlgEditLink
from pyut.uiv2.dialogs.DlgEditInterface import DlgEditInterface

from pyut.uiv2.dialogs.textdialogs.DlgEditNote import DlgEditNote
from pyut.uiv2.dialogs.textdialogs.DlgEditText import DlgEditText

from pyut.uiv2.dialogs.Wrappers import DlgEditActor
from pyut.uiv2.dialogs.Wrappers import DlgEditUseCase

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.PyutUtils import PyutUtils

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlFrame import UmlFrame
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
    from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.uiv2.eventengine.Events import EventType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


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

    def _cbGetActiveUmlFrame(self, umlFrame: 'UmlDiagramsFrame'):

        self.logger.info(f'{umlFrame=}')

        self._doEditObject(x=self._x, y=self._y, umlFrame=umlFrame)

    def _doEditObject(self, x: int, y: int, umlFrame: 'UmlDiagramsFrame'):
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
                self._editAssociation(diagramShape)
            case OglInheritance() | OglInterface() | AnchorPoint() | ControlPoint() | SizerShape():
                pass    # Nothing to edit on inheritance or interface relationships
            case _:
                self.logger.error(f'Unknown shape')
                PyutUtils.displayError(msg=f'EditObjectHandler: Unknown shape: {diagramShape}', title='Developer Error')
        umlFrame.Refresh()

    def _editClass(self, umlFrame: 'UmlDiagramsFrame', diagramShape: OglObject):
        pyutClass: PyutClass = diagramShape.pyutObject
        with DlgEditClass(umlFrame, self._eventEngine, pyutClass) as dlg:
            if dlg.ShowModal() == OK:
                self._autoResize(umlFrame, diagramShape)
                # This dialog sends the modified event

    def _editOglInterface2(self, umlFrame: 'UmlDiagramsFrame', lollipop: OglInterface2):

        pyutInterface: PyutInterface = lollipop.pyutInterface

        with DlgEditInterface(umlFrame, self._eventEngine, pyutInterface) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.info(f'{pyutInterface=}')
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editText(self, umlFrame: 'UmlDiagramsFrame', diagramShape: OglObject):

        oglText:  OglText  = cast(OglText, diagramShape)
        pyutText: PyutText = oglText.pyutText

        with DlgEditText(parent=umlFrame, pyutText=pyutText) as dlg:
            if dlg.ShowModal() == OK:
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editNote(self, umlFrame: 'UmlDiagramsFrame', oglNote: OglNote):

        pyutNote: PyutNote = oglNote.pyutObject
        with DlgEditNote(umlFrame, pyutNote=pyutNote) as dlg:
            if dlg.ShowModal() == OK:
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editUseCase(self, umlFrame: 'UmlDiagramsFrame', oglUseCase: OglUseCase):

        pyutUseCase: PyutUseCase = oglUseCase.pyutObject
        with DlgEditUseCase(umlFrame, useCaseName=pyutUseCase.name) as dlg:
            if dlg.ShowModal() == OK:
                pyutUseCase.name = dlg.GetValue()
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editActor(self, umlFrame: 'UmlDiagramsFrame', oglActor: OglActor):

        pyutActor: PyutActor = oglActor.pyutObject
        with DlgEditActor(umlFrame, actorName=pyutActor.name) as dlg:
            if dlg.ShowModal() == OK:
                pyutActor.name = dlg.GetValue()
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def _editAssociation(self, oglAssociation: OglAssociation):

        with DlgEditLink(None, oglAssociation.pyutObject) as dlg:
            if dlg.ShowModal() == OK:
                oglAssociation.pyutObject = dlg.value
                self._eventEngine.sendEvent(EventType.UMLDiagramModified)   # don't do this in Pyut

    def _autoResize(self, umlFrame: 'UmlDiagramsFrame', obj: OglObject):
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

    def _getUmlObjects(self, umlFrame: 'UmlFrame') -> 'UmlObjects':
        """
        May be empty

        Returns: Return the list of UmlObjects in the diagram.
        """
        from pyut.ui.umlframes.UmlFrame import UmlObjects

        return cast(UmlObjects, umlFrame.getUmlObjects())
