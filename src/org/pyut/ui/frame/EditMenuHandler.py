
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CommandEvent
from wx import Menu

from org.pyut.general.Mediator import Mediator

from org.pyut.miniogl.Diagram import Diagram

from org.pyut.ogl.OglObject import OglObject

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _


class EditMenuHandler:

    def __init__(self, editMenu: Menu):

        self.logger:    Logger   = getLogger(__name__)
        self._editMenu: Menu     = editMenu
        self._mediator: Mediator = Mediator()

    # noinspection PyUnusedLocal
    def onSelectAll(self, event: CommandEvent):
        """

        Args:
            event:
        """
        frame: UmlClassDiagramsFrame = self._mediator.getUmlFrame()

        if frame is None:
            PyutUtils.displayError(_("No frame found !"))
            return
        diagram: Diagram         = frame.GetDiagram()
        shapes:  List[OglObject] = diagram.GetShapes()
        for shape in shapes:
            shape: OglObject = cast(OglObject, shape)

            shape.SetSelected(True)
        frame.Refresh()
