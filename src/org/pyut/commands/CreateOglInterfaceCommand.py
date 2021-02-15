
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ID_ANY
from wx import OK

from org.pyut.dialogs.DlgEditInterface import DlgEditInterface
from org.pyut.enums.AttachmentPoint import AttachmentPoint
from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint
from org.pyut.model.PyutClass import PyutClass

from org.pyut.model.PyutInterface import PyutInterface

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.commands.Command import Command


class CreateOglInterfaceCommand(Command):

    def __init__(self,  implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._attachmentAnchor: SelectAnchorPoint = attachmentAnchor
        self._implementor:      OglClass          = implementor

        pyutInterface: PyutInterface = PyutInterface()
        pyutInterface.addImplementor(implementor.getPyutObject().getName())

        self._pyutInterface:    PyutInterface     = pyutInterface

        self._createLollipopInterface(pyutInterface)

    def serialize(self) -> str:
        return super().serialize()

    def deserialize(self, serializedData):
        pass

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
