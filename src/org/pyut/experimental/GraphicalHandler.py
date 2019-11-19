
from typing import List

from logging import Logger
from logging import getLogger

from org.pyut.commands.CommandGroup import CommandGroup
from org.pyut.commands.CreateOglLinkCommand import CreateOglLinkCommand

from org.pyut.history.HistoryManager import HistoryManager

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.PyutClass import PyutClass
from org.pyut.ogl.OglClass import OglClass


class GraphicalHandler:

    def __init__(self, umlFrame: UmlFrame, maxWidth: int, historyManager: HistoryManager):

        self.logger:    Logger   = getLogger(__name__)
        self._umlFrame: UmlFrame = umlFrame
        self._maxWidth: int       = maxWidth
        self._historyManager: HistoryManager = historyManager

    def addToDiagram(self, pyutClassDef: PyutClass) -> OglClass:
        """
        Add graphical version of data class to diagram

        Args:
            pyutClassDef:  The class data

        Returns:  The graphical element created to represent the above in the
        diagram
        """
        oglClassDef: OglClass = OglClass(pyutClassDef)
        self._umlFrame.addShape(oglClassDef, 0, 0)
        oglClassDef.autoResize()
        return oglClassDef

    def createInheritanceLink(self, child: OglClass, father: OglClass):
        """
        Add a paternity link between child and father.

        Args:
            child:  A child
            father: The daddy!!

        Returns: an OgLink

        """
        cmdGroup: CommandGroup         = CommandGroup('Creating an inheritance link')
        cmd:      CreateOglLinkCommand = CreateOglLinkCommand(src=father, dst=child)

        cmdGroup.addCommand(cmd)
        self._historyManager.addCommandGroup(cmdGroup)

        cmd.execute()

    def positionClassHierarchy(self, oglClassDefinitions: List[OglClass]):
        """
        Organize by vertical descending sizes

        Args:
            oglClassDefinitions:
        """
        # sort by ascending height
        sortedOglClassDefinitions: List[OglClass] = sorted(oglClassDefinitions, key=OglClass.GetHeight)

        x = 20
        y = 20
        incY = 0
        for oglClassDef in sortedOglClassDefinitions:
            incX, sy = oglClassDef.GetSize()
            incX += 20
            sy += 20
            incY = max(incY, sy)
            # find good coordinates
            if x + incX >= self._maxWidth:
                x = 20
                y += incY
                incY = sy
            oglClassDef.SetPosition(x + incX // 2, y + sy // 2)

            x += incX
