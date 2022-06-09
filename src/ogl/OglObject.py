
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import MouseEvent
from wx import Font
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL

from miniogl.RectangleShape import RectangleShape
from miniogl.ShapeEventHandler import ShapeEventHandler

from ogl.OglLink import OglLink
from ogl.OglUtils import OglUtils

from ogl.events.OglEventType import OglEventType
from ogl.events.OglEventEngine import OglEventEngine

from ogl.preferences.OglPreferences import OglPreferences

from pyutmodel.PyutObject import PyutObject


DEFAULT_FONT_SIZE = 10


class OglObject(RectangleShape, ShapeEventHandler):
    """
    This is the base class for new OGL objects.
    Every new OGL class must inherit this class and redefine methods if
    necessary. OGL Objects are automatically a RectangleShape for
    global link management.
    """

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, pyutObject=None, width: int = 0, height: int = 0):
        """

        Args:
            pyutObject: Associated PyutObject
            width:      Initial width
            height:     Initial height
        """
        self._pyutObject = pyutObject
        RectangleShape.__init__(self, 0, 0, width, height)

        # Default font
        self._defaultFont: Font           = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self._prefs:       OglPreferences = OglPreferences()

        # TODO This is also used by sequence diagrams to store OglSDMessage links
        self._oglLinks: List[OglLink] = []     # Connected links
        self._modifyCommand = None

        self._eventEngine: OglEventEngine = cast(OglEventEngine, None)

    @deprecated(reason='Use the properties')
    def setPyutObject(self, pyutObject: PyutObject):
        self._pyutObject = pyutObject

    @deprecated(reason='Use the properties')
    def getPyutObject(self) -> PyutObject:
        """
        Return the associated pyut object.

        @return PyutObject : Associated PyutObject
        """
        return self._pyutObject

    @property
    def pyutObject(self):
        return self._pyutObject

    @pyutObject.setter
    def pyutObject(self, pyutObject):
        self._pyutObject = pyutObject

    @property
    def links(self):
        return self._oglLinks

    @property
    def eventEngine(self) -> OglEventEngine:
        """
        This property necessary because the diagram is not added until the
        object is' attached'

        Returns:

        """
        if self.HasDiagramFrame() is True:

            # from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame
            # panel: UmlDiagramsFrame = self.GetDiagram().GetPanel()
            panel = self.GetDiagram().GetPanel()
            if panel is not None:
                if self._eventEngine is None:
                    self._eventEngine = panel.eventEngine

        return self._eventEngine

    def addLink(self, link):
        """
        Add a link to an ogl object.

        Args:
            link:  the link to add
        """
        self._oglLinks.append(link)

    @deprecated(reason='Use the property links')
    def getLinks(self):
        """
        Return the links.

        Returns: OglLink[] : Links connected to object
        """
        return self._oglLinks

    def OnLeftDown(self, event: MouseEvent):
        """
        Handle event on left click.
        Note to self.  This method used to call only call event.Skip() if there was an action waiting
        Now I do it regardless;  Seem to be no ill effects

        Args:
            event:  The mouse event
        """
        OglObject.clsLogger.debug(f'OglObject.OnLeftDown  - {event.GetEventObject()=}')

        self.eventEngine.sendEvent(OglEventType.ShapeSelected, selectedShape=self, selectedShapePosition=event.GetPosition())
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        """
        Implement this method so we can snap Ogl objects

        Args:
            event:  the mouse event
        """
        gridInterval: int = self._prefs.backgroundGridInterval
        x, y = self.GetPosition()
        if self._prefs.snapToGrid is True:
            snappedX, snappedY = OglUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)
            self.SetPosition(snappedX, snappedY)
        else:
            self.SetPosition(x, y)

    def autoResize(self):
        """
        Find the right size to see all the content and resize self.

        """
        pass

    def SetPosition(self, x: int, y: int):
        """
        Define new position for the object

        Args:
            x:  The new abscissa
            y:  The new ordinate
        """
        if self.eventEngine is not None:        # we might be associated with a diagram yet
            self.eventEngine.sendEvent(OglEventType.ProjectModified)
        RectangleShape.SetPosition(self, x, y)

    def SetSelected(self, state=True):

        # from org.pyut.ui.Mediator import Mediator          # avoid circular import
        # from org.pyut.ui.Mediator import ACTION_ZOOM_OUT   # avoid circular import

        # mediator: Mediator = Mediator()
        # if mediator.getCurrentAction() != ACTION_ZOOM_OUT:
        # TODO:  I took this out because could never cause this to happen;  Conveniently, this removes all mediator calls
        RectangleShape.SetSelected(self, state)
