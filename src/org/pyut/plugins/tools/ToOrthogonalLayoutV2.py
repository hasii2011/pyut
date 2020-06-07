
from typing import List

from logging import Logger
from logging import getLogger

from time import time

from wx import Yield as wxYield

from orthogonal.mapping.ScreenSize import ScreenSize

from org.pyut.MiniOgl.Shape import Shape

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglNote import OglNote

from org.pyut.plugins.orthogonal.OrthogonalAdapter import OglCoordinate
from org.pyut.plugins.orthogonal.OrthogonalAdapter import OglCoordinates
from org.pyut.plugins.orthogonal.OrthogonalAdapter import OrthogonalAdapter

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin


class ToOrthogonalLayoutV2(PyutToPlugin):
    """
    Version 2 of this plugin.  Does not depend on python-tulip.  Instead it depends on a homegrown
    version
    """

    def __init__(self, umlObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects:  list of ogl objects
            umlFrame:    A Pyut UML Frame
        """
        super().__init__(umlObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)

    def getName(self):
        """
        Returns: the name of the plugin.
        """
        return "No name"

    def getAuthor(self):
        """
        Returns: The author's name
        """
        return "Humberto A. Sanchez iI"

    def getVersion(self):
        """
        Returns: The plugin version string
        """
        return "2.0"

    def getMenuTitle(self):
        """
        Returns:  The menu title for this plugin
        """
        return "Orthogonal Layout V2"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns: if False, the import will be cancelled.
        """
        return True

    def doAction(self, umlObjects: List[OglClass], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """
        Do the tool's action

        Args:
            umlObjects:         list of the uml objects of the diagram
            selectedObjects:    list of the selected objects
            umlFrame:           The diagram frame
        """
        if umlFrame is None:
            self.displayNoUmlFrame()
            return
        if len(umlObjects) == 0:
            self.displayNoUmlObjects()
            return

        self.logger.info(f'Begin Orthogonal algorithm')

        orthogonalAdapter: OrthogonalAdapter = OrthogonalAdapter(umlObjects=selectedObjects)

        screenSize: ScreenSize = ScreenSize(1000, 1000)     # TODO get user input;  This is really layout area size
        orthogonalAdapter.doLayout(screenSize)

        self._reLayoutNodes(selectedObjects, umlFrame, orthogonalAdapter.oglCoordinates)

    def _reLayoutNodes(self, umlObjects: List[OglClass], umlFrame: UmlFrame, oglCoordinates: OglCoordinates):
        """

        Args:
            umlObjects:
            umlFrame:
        """

        for umlObj in umlObjects:
            if isinstance(umlObj, OglClass) or isinstance(umlObj, OglNote):
                oglName: str = umlObj.getPyutObject().getName()
                oglCoordinate: OglCoordinate = oglCoordinates[oglName]

                self._stepNodes(umlObj, oglCoordinate)
            self._animate(umlFrame)

    def _stepNodes(self, srcShape: Shape, oglCoordinate: OglCoordinate):

        oldX, oldY = srcShape.GetPosition()
        newX: int = oglCoordinate.x
        newY: int = oglCoordinate.y

        self.logger.info(f'{srcShape} - oldX,oldY: ({oldX},{oldY}) newX,newY: ({newX},{newY})')
        #
        srcShape.SetPosition(newX, newY)

    def _animate(self, umlFrame: UmlFrame):
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
