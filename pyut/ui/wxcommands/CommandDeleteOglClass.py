
from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING
from typing import cast

from wx import Yield as wxYield

from pyutmodel.PyutClass import PyutClass

from ogl.OglClass import OglClass

from pyut.ui.wxcommands.BaseWxDeleteCommand import BaseWxDeleteCommand
from pyut.uiv2.eventengine.Events import EventType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandDeleteOglClass(BaseWxDeleteCommand):

    def __init__(self, oglClass: OglClass, eventEngine: IEventEngine):

        super().__init__(name='Delete Ogl Class', doableObject=oglClass, eventEngine=eventEngine)

        self.logger: Logger = getLogger(__name__)

        self._pyutClass: PyutClass = oglClass.pyutObject

    def Do(self) -> bool:
        """
        Do special delete behavior for a class
        """

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbOglClassDelete)

        return True

    def Undo(self) -> bool:

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbOglClassDeleteUndo)
        wxYield()
        return True

    def _cbOglClassDelete(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame

        self._removeOglObjectFromFrame(umlFrame=umlFrame, oglObject=self._objectToDelete, pyutClass=self._pyutClass)

    def _cbOglClassDeleteUndo(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame

        oglClass:  OglClass  = cast(OglClass, self._objectToDelete)              # get old

        self._oglObjWidth, self._oglObjHeight = oglClass.GetSize()

        self._objectToDelete = OglClass(self._pyutClass, w=self._oglObjWidth, h=self._oglObjHeight)        # create new

        self._addOglClassToFrame(umlFrame=umlFrame, oglClass=self._objectToDelete, x=self._oglObjX, y=self._oglObjY)
        umlFrame.Refresh()
