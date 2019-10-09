
from logging import Logger
from logging import getLogger

from wx import MouseEvent
from wx import Point
from wx import Font
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL

from OglLink import *

from Mediator import getMediator
from Mediator import ACTION_ZOOM_OUT

DEFAULT_FONT_SIZE = 10


class OglObject(RectangleShape, ShapeEventHandler):
    """
    This is the base class for new OGL objects.
    Every new OGL class must inherate this class and redefines methods if
    necessary. OGL Objects are automatically wx.RectangleShape for
    global link management.

    This class has been introduced quite late in developement and has
    caused some refactoring.

    :version: $Revision: 1.11 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    def __init__(self, pyutObject=None, width=0, height=0):
        """
        Constructor

        @param PyutObject pyutObject : Associated PyutObject
        @param int width  : Initial width
        @param int height : Initial height
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        RectangleShape.__init__(self, 0, 0, width, height)

        self.logger: Logger = getLogger(__name__)
        self._pyutObject = pyutObject
        """
        Associated PyutObject
        """
        # Default font
        self._defaultFont: Font = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        # Connected links
        self._oglLinks = []
        # added by P.Dabrowski 20051202 : it's the command to undo/redo a modification on this object.
        self._modifyCommand = None

    def setPyutObject(self, pyutObject):
        """
        Set the associated pyut object.

        @param PyutObject pyutObject : Associated PyutObject
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._pyutObject = pyutObject

    def getPyutObject(self):
        """
        Return the associated pyut object.

        @return PyutObject : Associated PyutObject
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._pyutObject

    def addLink(self, link):
        """
        Add a link to an ogl object.

        @param OglLink link : the link to add
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self._oglLinks.append(link)

    def getLinks(self):
        """
        Return the links.

        @return OglLink[] : Links connected to object
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        return self._oglLinks

    def OnLeftDown(self, event: MouseEvent):
        """
        Handle event on left click.
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        self.logger.info(f'OnLeftDown - event - {event}')
        med = getMediator()
        if med.actionWaiting():
            position: Point = event.GetPosition()
            med.shapeSelected(self, position)
            return
        event.Skip()

    def OnLeftUp(self, event):
        pass

    def autoResize(self):
        """
        Find the right size to see all the content, and resize self.

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        pass

    def SetPosition(self, x, y):
        """
        Define new position for the object

        Args:
            x:
            y:
        """
        import Mediator
        fileHandling = Mediator.getMediator().getFileHandling()
        if fileHandling is not None:
            fileHandling.setModified(True)
        RectangleShape.SetPosition(self, x, y)

    def SetSelected(self, state=True):

        if getMediator().getCurrentAction() != ACTION_ZOOM_OUT:
            RectangleShape.SetSelected(self, state)
