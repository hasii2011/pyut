
from logging import Logger
from logging import getLogger

from typing import List

# noinspection PyPackageRequirements
from deprecated import deprecated

from wx import MouseEvent
from wx import Font
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL

from org.pyut.miniogl.RectangleShape import RectangleShape
from org.pyut.miniogl.ShapeEventHandler import ShapeEventHandler

from org.pyut.PyutUtils import PyutUtils

from org.pyut.model.PyutObject import PyutObject
from org.pyut.ogl.events.OglEventEngine import OglEventEngine

from org.pyut.ogl.OglLink import OglLink

from org.pyut.preferences.PyutPreferences import PyutPreferences

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
        self._defaultFont: Font            = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self._prefs:       PyutPreferences = PyutPreferences()

        # TODO This is also used by sequence diagrams to store OglSDMessage links
        self._oglLinks: List[OglLink] = []     # Connected links
        self._modifyCommand = None

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

    def addLink(self, link):
        """
        Add a link to an ogl object.

        Args:
            link:  the link to add
        """
        self._oglLinks.append(link)

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

        OglEventEngine().sendSelectedShapeEvent(shape=self, position=event.GetPosition())

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
            snappedX, snappedY = PyutUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)
            self.SetPosition(snappedX, snappedY)
        else:
            self.SetPosition(x, y)

    def autoResize(self):
        """
        Find the right size to see all the content and resize self.

        """
        pass

    def SetPosition(self, x, y):
        """
        Define new position for the object

        Args:
            x:  The new abscissa
            y:  The new ordinate
        """
        OglEventEngine().sendProjectModifiedEvent()
        RectangleShape.SetPosition(self, x, y)

    def SetSelected(self, state=True):

        from org.pyut.ui.Mediator import Mediator          # avoid circular import
        from org.pyut.ui.Mediator import ACTION_ZOOM_OUT   # avoid circular import

        mediator: Mediator = Mediator()
        if mediator.getCurrentAction() != ACTION_ZOOM_OUT:
            RectangleShape.SetSelected(self, state)
