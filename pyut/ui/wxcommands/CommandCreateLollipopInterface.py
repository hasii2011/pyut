
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodelv2.PyutModelTypes import ClassName

from pyutmodelv2.PyutInterface import PyutInterface

from miniogl.AttachmentSide import AttachmentSide
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2

from pyut.ui.wxcommands.Types import DoableObjectType
from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

from pyut.ui.wxcommands.BaseWxCreateCommand import BaseWxCreateCommand


class CommandCreateLollipopInterface(BaseWxCreateCommand):

    def __init__(self, implementor: OglClass, attachmentAnchor: SelectAnchorPoint, eventEngine: IEventEngine):

        self.logger: Logger = getLogger(__name__)

        self._implementor:      OglClass          = implementor
        self._attachmentAnchor: SelectAnchorPoint = attachmentAnchor

        # x,y will be reset correctly prior to adding the lollipop
        super().__init__(canUndo=True, name='Create Interface', eventEngine=eventEngine, x=0, y=0)

        # pyutInterface: PyutInterface = PyutInterface()
        # pyutInterface.addImplementor(ClassName(implementor.pyutObject.name))
        #
        # self._pyutInterface: PyutInterface = pyutInterface
        # self._oglInterface:  OglInterface2 = OglInterface2(pyutInterface, self._attachmentAnchor)

    def _createPrototypeInstance(self) -> DoableObjectType:

        pyutInterface: PyutInterface = PyutInterface()
        pyutInterface.addImplementor(ClassName(self._implementor.pyutObject.name))

        self._pyutInterface: PyutInterface = pyutInterface
        self._oglInterface:  OglInterface2 = OglInterface2(pyutInterface, self._attachmentAnchor)

        return self._oglInterface

    def _placeShapeOnFrame(self):

        attachmentAnchor: SelectAnchorPoint = self._attachmentAnchor

        self._removeUnneededAnchorPoints(self._implementor, attachmentAnchor)

        self._eventEngine.sendEvent(EventType.EditInterface, pyutInterface=self._pyutInterface, implementor=self._implementor)

        anchorPosition: Tuple[int, int] = attachmentAnchor.GetPosition()
        self.logger.info(f'anchorPosition: {anchorPosition}')

        # set up the callback
        self._oglObjX = anchorPosition[0]
        self._oglObjY = anchorPosition[1]
        self._shape = self._oglInterface

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbAddOglObjectToFrame)

        # umlFrame.addShape(self._shape, x, y, withModelUpdate=True)
        # umlFrame.Refresh()

        return True

    def Undo(self) -> bool:
        return True

    def _removeUnneededAnchorPoints(self, implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        attachmentSide: AttachmentSide = attachmentAnchor.attachmentPoint
        for iAnchor in implementor.GetAnchors():
            if isinstance(iAnchor, SelectAnchorPoint):
                anchor: SelectAnchorPoint = cast(SelectAnchorPoint, iAnchor)
                if anchor.attachmentPoint != attachmentSide:
                    anchor.SetProtected(False)
                    anchor.Detach()
