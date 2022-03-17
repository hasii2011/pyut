
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

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenizeValue

from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.model.ModelTypes import ClassName

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutInterface import PyutInterface

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.history.commands.MethodInformation import MethodInformation
from org.pyut.history.commands.OglShapeCommand import OglShapeCommand

from org.pyut.preferences.PyutPreferences import PyutPreferences


class CreateOglInterfaceCommand(OglShapeCommand):

    def __init__(self,  implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        if implementor is None and attachmentAnchor is None:
            pass
        else:
            self._attachmentAnchor: SelectAnchorPoint = attachmentAnchor
            self._implementor:      OglClass          = implementor

            pyutInterface: PyutInterface = PyutInterface(name=PyutPreferences().interfaceName)
            pyutInterface.addImplementor(ClassName(implementor.pyutObject.name))

            self._pyutInterface: PyutInterface = pyutInterface

            self._createLollipopInterface(pyutInterface)

    def serialize(self) -> str:

        serializedShape: str = super().serialize()

        oglInterface: OglInterface2 = self._shape

        destAnchor:      SelectAnchorPoint = oglInterface.destinationAnchor
        attachmentPoint: AttachmentPoint   = destAnchor.attachmentPoint
        pos:             Tuple[int, int]   = destAnchor.GetPosition()

        serializedShape += tokenizeValue('attachmentPoint', attachmentPoint.__str__())
        serializedShape += tokenizeValue("position", repr(pos))

        return serializedShape

    def deserialize(self, serializedShape):

        super().deserialize(serializedShape)

        pyutModule:        ModuleType = import_module(self._pyutShapeModuleName)
        pyutInterfaceType: type       = getattr(pyutModule, self._pyutShapeClassName)

        interfaceName: str = deTokenize("shapeName", serializedShape)

        pyutInterface: PyutInterface = pyutInterfaceType(interfaceName)

        self.logger.debug(f'{interfaceName=} {pyutInterface=}')

        oglModule:         ModuleType = import_module(self._oglShapeModuleName)
        oglInterface2Type: type       = getattr(oglModule, self._oglShapeClassName)

        attachmentPointName: str = deTokenize('attachmentPoint', serializedShape)
        attachmentPoint: AttachmentPoint = AttachmentPoint.toEnum(attachmentPointName)

        shapePosition: Tuple[int, int] = eval(deTokenize("position", serializedShape))

        attachmentAnchor: SelectAnchorPoint = SelectAnchorPoint(x=shapePosition[0], y=shapePosition[1], attachmentPoint=attachmentPoint)

        oglInterface2: OglInterface2 = oglInterface2Type(pyutInterface=pyutInterface, destinationAnchor=attachmentAnchor)

        shapeId: str = deTokenize("shapeId", serializedShape)
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

                pyutClass: PyutClass = cast(PyutClass, self._implementor.pyutObject)
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
        for iAnchor in implementor.GetAnchors():
            if isinstance(iAnchor, SelectAnchorPoint):
                anchor: SelectAnchorPoint = cast(SelectAnchorPoint, iAnchor)
                if anchor.attachmentPoint != attachmentPoint:
                    anchor.SetProtected(False)
                    anchor.Detach()
