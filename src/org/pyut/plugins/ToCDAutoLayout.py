from logging import Logger
from logging import getLogger
from typing import List

from time import time
from math import sqrt

from wx import Yield as wxYield

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.plugins.PyutToPlugin import PyutToPlugin

from org.pyut.ogl.OglClass import OglClass


class ToCDAutoLayout(PyutToPlugin):
    """
    Auto-layout tool
    """
    def __init__(self, oglObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Args:
            oglObjects: list of ogl objects
            umlFrame: PyUt's UML Frame
        """
        super().__init__(oglObjects, umlFrame)
        self.logger: Logger = getLogger(__name__)

    def getName(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "CD Auto-layout"

    def getAuthor(self) -> str:
        """
        Returns: The author's name
        """
        return "C.Dutoit < dutoitc@hotmail.com >"

    def getVersion(self) -> str:
        """
        Returns: The plugin version string
        """
        return "0.1"

    def getMenuTitle(self) -> str:
        """
        Returns:  The menu title for this plugin
        """
        return "CD auto-layout"

    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns: if False, the import will be cancelled.
        """
        return True

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """

        if umlFrame is None:
            self.displayNoUmlFrame()
            return
        if len(selectedObjects) < 1:
            self.displayNothingSelected()
            return

        # for i in range(20):     # len(umlObjects)):
        for i in range(len(umlObjects)):  # len(umlObjects)):

            for obj in selectedObjects:
                if isinstance(obj, OglClass):
                    self._step(obj)
            self._animate(umlFrame)

    def _step(self, srcShape):
        ForceField = 200
        vx = 0
        vy = 0
        srcX, srcY = srcShape.GetPosition()

        self.logger.debug(f'src: ({srcX},{srcY})')

        for link in srcShape.getLinks():
            dstShape = link.getDestinationShape()
            if dstShape != srcShape:
                dstX, dstY = dstShape.GetPosition()
                linkSize = sqrt((dstX-srcX) * (dstX-srcX) + (dstY-srcY) * (dstY-srcY))
                self.logger.debug(f'dst = ({dstX},{dstY}  LinkSize = {linkSize}')

                n = linkSize-ForceField
                attraction = max(-ForceField/8, min(ForceField/8, n*n*n))
                self.logger.debug(f'attraction = {attraction}')

                vx += attraction * (dstX-srcX) / linkSize
                vy += attraction * (dstY-srcY) / linkSize

        self.logger.debug(f'vx,vy = {vx},{vy}')
        srcShape.SetPosition(srcX + vx, srcY + vy)

    def _animate(self, umlFrame):
        """
        Does an animation simulation

        Args:
            umlFrame:
        """
        umlFrame.Refresh()
        self.logger.debug(f'Refreshing ...............')
        wxYield()
        t = time()
        while time() < t + 0.05:
            pass
