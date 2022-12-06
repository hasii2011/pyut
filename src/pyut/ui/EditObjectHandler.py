from typing import TYPE_CHECKING
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CENTRE
from wx import ID_ANY
from wx import ID_OK
from wx import OK

from wx import TextEntryDialog

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutText import PyutText

from ogl.OglInterface2 import OglInterface2
from ogl.OglText import OglText
from ogl.OglClass import OglClass

from pyut.dialogs.DlgEditClass import DlgEditClass
from pyut.dialogs.DlgEditInterface import DlgEditInterface
from pyut.dialogs.DlgEditLink import DlgEditLink
from pyut.dialogs.DlgEditUseCase import DlgEditUseCase

from pyut.dialogs.textdialogs.DlgEditNote import DlgEditNote
from pyut.dialogs.textdialogs.DlgEditText import DlgEditText

from pyut.preferences.PyutPreferences import PyutPreferences

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlFrame import UmlFrame
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
    from pyut.ui.umlframes.UmlFrame import UmlObjects

from pyut.uiv2.eventengine.Events import EventType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class EditObjectHandler:

    def __init__(self, eventEngine: IEventEngine):

        self.logger:       Logger       = getLogger(__name__)
        self._eventEngine: IEventEngine = eventEngine

        self._x: int = -1
        self._y: int = -1

    def editObject(self, x, y):

        self._x = x
        self._y = y
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrame)

    def _cbGetActiveUmlFrame(self, umlFrame: 'UmlDiagramsFrame'):

        self.logger.info(f'{umlFrame=}')

        self._doEditObject(x=self._x, y=self._y, umlFrame=umlFrame)

    def _doEditObject(self, x, y, umlFrame: 'UmlDiagramsFrame'):
        """
        Edit the object at x, y.
        """
        # umlFrame = self._treeNotebookHandler.currentFrame
        # if umlFrame is None:
        #     return
        #
        # TODO I don't like in-line imports but moving them to top file causes a cyclic dependency error
        #
        from ogl.OglClass import OglClass
        from ogl.OglNote import OglNote
        from ogl.OglUseCase import OglUseCase
        from ogl.OglActor import OglActor
        from ogl.OglAssociation import OglAssociation
        from ogl.OglInterface import OglInterface

        from pyutmodel.PyutNote import PyutNote

        diagramShape = umlFrame.FindShape(x, y)

        if diagramShape is None:
            return

        # TODO:  Convert this to a switch statement;  Move the case code to sub-methods
        if isinstance(diagramShape, OglClass):
            pyutObject = diagramShape.pyutObject
            self._editClass(umlFrame, pyutObject)
            self.autoResize(umlFrame, diagramShape)
        elif isinstance(diagramShape, OglInterface2):

            self.logger.info(f'Double clicked on lollipop')
            lollipop:      OglInterface2 = cast(OglInterface2, diagramShape)
            pyutInterface: PyutInterface = lollipop.pyutInterface
            with DlgEditInterface(umlFrame, self._eventEngine, pyutInterface) as dlg:
                if dlg.ShowModal() == OK:
                    self.logger.info(f'model: {pyutInterface}')
                else:
                    self.logger.info(f'Cancelled')

        elif isinstance(diagramShape, OglText):
            oglText:  OglText  = cast(OglText, diagramShape)
            pyutText: PyutText = oglText.pyutText

            self.logger.info(f'Double clicked on {oglText}')

            dlgEditText: DlgEditText = DlgEditText(parent=umlFrame, pyutText=pyutText)
            dlgEditText.ShowModal()
            dlgEditText.Destroy()

        elif isinstance(diagramShape, OglNote):
            pyutObject = diagramShape.pyutObject
            dlgEditNote: DlgEditNote = DlgEditNote(umlFrame, cast(PyutNote, pyutObject))
            dlgEditNote.ShowModal()
            dlgEditNote.Destroy()
        elif isinstance(diagramShape, OglUseCase):
            pyutObject = diagramShape.pyutObject
            dlgEditUseCase: DlgEditUseCase = DlgEditUseCase(umlFrame, pyutObject)   # TODO fix where we show it here not in constructor
            dlgEditUseCase.Destroy()
        elif isinstance(diagramShape, OglActor):
            pyutObject = diagramShape.pyutObject
            dlgTextEntry: TextEntryDialog = TextEntryDialog(umlFrame, "Actor name", "Enter actor name", pyutObject.name, OK | CANCEL | CENTRE)
            if dlgTextEntry.ShowModal() == ID_OK:
                pyutObject.setName(dlgTextEntry.GetValue())
            dlgTextEntry.Destroy()
        elif isinstance(diagramShape, OglAssociation):
            dlgEditAssociation: DlgEditLink = DlgEditLink(None, ID_ANY, diagramShape.pyutObject)
            dlgEditAssociation.ShowModal()
            rep = dlgEditAssociation.getReturnAction()
            dlgEditAssociation.Destroy()
            if rep == -1:    # destroy link
                diagramShape.Detach()
        elif isinstance(diagramShape, OglInterface):
            dlgEditInterface: DlgEditLink = DlgEditLink(None, ID_ANY, diagramShape.pyutObject)
            dlgEditInterface.ShowModal()
            rep = dlgEditInterface.getReturnAction()
            dlgEditInterface.Destroy()
            if rep == -1:  # destroy link
                diagramShape.Detach()

        umlFrame.Refresh()

    def _editClass(self, umlFrame: 'UmlDiagramsFrame', thePyutClass: PyutClass):
        """
        The standard class editor dialog, for registerClassEditor.

        Args:
            thePyutClass:  the class to edit (data model)
        """
        # umlFrame = self._treeNotebookHandler.currentFrame
        # if umlFrame is None:
        #     return
        dlg: DlgEditClass = DlgEditClass(umlFrame, self._eventEngine, thePyutClass)
        dlg.ShowModal()
        dlg.Destroy()

    def autoResize(self, umlFrame: 'UmlDiagramsFrame', obj: Union[PyutClass, OglClass]):
        """
        Auto-resize the given object.

        Args:
            umlFrame
            obj:

        Notes: Don't really like methods with signatures likes this;  Where the input parameter
        can be one of two things;  I suspect this is some legacy thing;  When I become more
        familiar with the code base I need to fix this.   Humberto
        """
        from ogl.OglClass import OglClass
        prefs: PyutPreferences = PyutPreferences()

        if prefs.autoResizeShapesOnEdit is True:
            if isinstance(obj, PyutClass):
                po = [po for po in self.getUmlObjects(umlFrame) if isinstance(po, OglClass) and po.pyutObject is obj]
                obj = po[0]

            obj.autoResize()

    def getUmlObjects(self, umlFrame: 'UmlFrame') -> 'UmlObjects':
        """
        May be empty

        Returns: Return the list of UmlObjects in the diagram.
        """
        from pyut.ui.umlframes.UmlFrame import UmlObjects

        # if self._treeNotebookHandler is None:
        #     return UmlObjects([])
        # umlFrame = self._treeNotebookHandler.currentFrame
        if umlFrame is not None:
            return cast(UmlObjects, umlFrame.getUmlObjects())
        else:
            return UmlObjects([])
