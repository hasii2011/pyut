
from typing import Tuple
from typing import cast

from types import ModuleType

from logging import Logger
from logging import getLogger

from importlib import import_module

from wx import ID_ANY
from wx import OK

from org.pyut.dialogs.DlgEditInterface import DlgEditInterface

from org.pyut.enums.AttachmentPoint import AttachmentPoint

from org.pyut.history.HistoryUtils import getTokenValue
from org.pyut.history.HistoryUtils import makeValuatedToken

from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutInterface import PyutInterface

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.commands.MethodInformation import MethodInformation
from org.pyut.commands.OglShapeCommand import OglShapeCommand


class CreateOglInterfaceCommand(OglShapeCommand):

    def __init__(self,  implementor: OglClass = None, attachmentAnchor: SelectAnchorPoint = None):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        if implementor is None and attachmentAnchor is None:
            pass
        else:
            self._attachmentAnchor: SelectAnchorPoint = attachmentAnchor
            self._implementor:      OglClass          = implementor

            pyutInterface: PyutInterface = PyutInterface()
            pyutInterface.addImplementor(implementor.getPyutObject().getName())

            self._pyutInterface: PyutInterface = pyutInterface

            self._createLollipopInterface(pyutInterface)

    def serialize(self) -> str:

        serializedShape: str = super().serialize()

        oglInterface: OglInterface2 = self._shape

        destAnchor:      SelectAnchorPoint = oglInterface.destinationAnchor
        attachmentPoint: AttachmentPoint   = destAnchor.attachmentPoint
        pos:             Tuple[int, int]   = destAnchor.GetPosition()

        serializedShape += makeValuatedToken('attachmentPoint', attachmentPoint.__str__())
        serializedShape += makeValuatedToken("position", repr(pos))

        return serializedShape

    def deserialize(self, serializedShape):

        super().deserialize(serializedShape)

        pyutModule:        ModuleType = import_module(self._pyutShapeModuleName)
        pyutInterfaceType: type       = getattr(pyutModule, self._pyutShapeClassName)

        interfaceName: str = getTokenValue("shapeName", serializedShape)

        pyutInterface: PyutInterface = pyutInterfaceType(interfaceName)

        self.logger.debug(f'{interfaceName=} {pyutInterface=}')

        oglModule:         ModuleType = import_module(self._oglShapeModuleName)
        oglInterface2Type: type       = getattr(oglModule, self._oglShapeClassName)

        attachmentPointName: str = getTokenValue('attachmentPoint', serializedShape)
        attachmentPoint: AttachmentPoint = AttachmentPoint.toEnum(attachmentPointName)

        shapePosition: Tuple[int, int] = eval(getTokenValue("position", serializedShape))

        attachmentAnchor: SelectAnchorPoint = SelectAnchorPoint(x=shapePosition[0], y=shapePosition[1], attachmentPoint=attachmentPoint)

        oglInterface2: OglInterface2 = oglInterface2Type(pyutInterface=pyutInterface, destinationAnchor=attachmentAnchor)

        shapeId: str = getTokenValue("shapeId", serializedShape)
        oglInterface2.SetID(int(shapeId))

        pyutInterface = cast(PyutInterface, MethodInformation.deserialize(serializedData=serializedShape, pyutObject=pyutInterface))

        oglInterface2.pyutInterface = pyutInterface
        self._shape = oglInterface2

    def redo(self):

        from org.pyut.ui.Mediator import Mediator

        med: Mediator = Mediator()

        attachmentAnchor: SelectAnchorPoint = self._attachmentAnchor

        self.logger.info(f'implementor: {self._implementor} attachmentAnchor: {attachmentAnchor}')
        umlFrame: UmlClassDiagramsFrame = med.getFileHandling().getCurrentFrame()

        self._removeUnneededAnchorPoints(self._implementor, attachmentAnchor)
        umlFrame.Refresh()

        with DlgEditInterface(umlFrame, ID_ANY, self._pyutInterface) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.info(f'model: {self._pyutInterface}')

                pyutClass: PyutClass = cast(PyutClass, self._implementor.getPyutObject())
                pyutClass.addInterface(self._pyutInterface)

        umlFrame: UmlClassDiagramsFrame = med.getFileHandling().getCurrentFrame()

        anchorPosition: Tuple[int, int] = attachmentAnchor.GetPosition()
        self.logger.info(f'anchorPosition: {anchorPosition}')
        x = anchorPosition[0]
        y = anchorPosition[1]

        umlFrame.addShape(self._shape, x, y, withModelUpdate=True)
        umlFrame.Refresh()

    def execute(self):
        self.redo()

    def _createLollipopInterface(self, pyutInterface: PyutInterface):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface, self._attachmentAnchor)
        self._shape = oglInterface

    def _removeUnneededAnchorPoints(self, implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        attachmentPoint: AttachmentPoint = attachmentAnchor.attachmentPoint
        for anchor in implementor.GetAnchors():
            if isinstance(anchor, SelectAnchorPoint):
                anchor: SelectAnchorPoint = cast(SelectAnchorPoint, anchor)
                if anchor.attachmentPoint != attachmentPoint:
                    anchor.SetProtected(False)
                    anchor.Detach()
