
from OglLink import *

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

    def __init__(self, pyutObject = None, width = 0, height = 0):
        """
        Constructor.

        @param PyutObject pyutObject : Associated PyutObject
        @param int width  : Initial width
        @param int height : Initial height
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # Shape initialization
        #print "OglObject-1"
        RectangleShape.__init__(self, 0, 0, width, height)
        #print "OglObject-2"

        # rectangle will not be resized from the center
        #self.SetCentreResize(False)

        # Attachments must be spaced
        #self.SetAttachmentMode(True)

        # Default, show please
        #self.Show(True)

        # PROTECTED

        # Associated PyutObject
        self._pyutObject = pyutObject

        # Default font
#        self._defaultFont = wx.Font((int)(PyutPreferences()['FONT_SIZE']) \
#                , wx.SWISS, wx.NORMAL, wx.NORMAL)
        self._defaultFont = wx.Font(DEFAULT_FONT_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL)

        # Connected links
        self._oglLinks = []
        #print "OglObject-3"

        #added by P.Dabrowski 20051202 : it's the command to undo/redo
        #a modification on this object.
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

    def OnLeftDown(self, event):
        """
        Handle event on left click.
        @param double x,y : Position
        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        #  print "OglObject.OnLeftDown"

        med = getMediator()
        if med.actionWaiting():
            med.shapeSelected(self, event.GetPositionTuple())
            #print "Event processed in OglObject"
            #return EVENT_PROCESSED
            return
        #  print "Skipped event in OglObject"
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
        import mediator
        fileHandling = mediator.getMediator().getFileHandling()
        if fileHandling is not None:
            fileHandling.setModified(True)
        RectangleShape.SetPosition(self, x, y)

    def SetSelected(self, state=True):

        from mediator import ACTION_ZOOM_OUT

        if mediator.getMediator().getCurrentAction() != ACTION_ZOOM_OUT:
            RectangleShape.SetSelected(self, state)
