
from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import ClientDC
from wx import EVT_MENU
from wx import Font
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import Menu

from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglObject import DEFAULT_FONT_SIZE

from org.pyut.PyutClass import PyutClass

from pyutUtils import assignID
from globals import _

from Mediator import getMediator

# Menu IDs
[MNU_TOGGLE_STEREOTYPE, MNU_TOGGLE_FIELDS, MNU_TOGGLE_METHODS, MNU_FIT_FIELDS, MNU_CUT_SHAPE]  = assignID(5)

MARGIN = 10.0


class OglClass(OglObject):
    """
    OGL object that represent an UML class in class diagrams.
    This class defines OGL objects that represents a class. You can just
    instantiate an OGL class and add it to the diagram, links, resizing,
    ... are managed by parent class `OglObject`.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.

    :version: $Revision: 1.21 $
    :author: Laurent Burgbacher
    :contact: lb@alawa.ch
    """
    def __init__(self, pyutClass=None, w: int = 100, h: int = 100):
        """
        @param  pyutClass : a Pyutclass object
        @param  w : Width of the shape
        @param  h : Height of the shape
        @author N.Hamadi
        """
        if pyutClass is None:
            pyutObject = PyutClass()
        else:
            pyutObject = pyutClass
        super().__init__(pyutObject, w, h)

        self.logger:    Logger = getLogger(__name__)
        self._nameFont: Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)

    def GetTextWidth(self, dc, text):
        width = dc.GetTextExtent(text)[0]
        return width

    def GetTextHeight(self, dc, text):
        height = dc.GetTextExtent(text)[1]
        return height

    def calculateClassHeader(self, dc, draw=False, initialX=None, initialY=None, calcWidth=False):
        """
        Calculate the class header position and size adn display it if
        a draw is True

        @return tuple : (x, y, w, h) = position and size of the header
        @author C.Dutoit
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)
        pyutObject = self.getPyutObject()
        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # define space between text and line
        lth = dc.GetTextExtent("*")[1] / 2.0

        # from where begin the text
        h += lth

        # draw a pyutClass name
        name = self.getPyutObject().getName()
        dc.SetFont(self._nameFont)
        nameWidth = self.GetTextWidth(dc, name)
        if draw:
            dc.DrawText(name, x + (w - nameWidth) / 2.0, y + h)
        if calcWidth:
            w = max(nameWidth, w)
        dc.SetFont(self._defaultFont)
        h += self.GetTextHeight(dc, str(name))
        h += lth

        # draw the stereotype if there's one
        stereo = self.getPyutObject().getStereotype()
        if stereo is not None and pyutObject.getShowStereotype():
            name = str(stereo)
            nameWidth = self.GetTextWidth(dc, name)
            if draw:
                dc.DrawText(name, x + (w - nameWidth) / 2.0, y + h)
            if calcWidth:
                w = max(nameWidth, w)
            h += self.GetTextHeight(dc, str(name))
            h += lth

        # Return sizes
        return x, y, w, h

    def calculateClassFields(self, dc, draw=False, initialX=None, initialY=None, calcWidth=False):
        """
        Calculate the class fields position and size and display it if
        a draw is True

        @return tuple : (x, y, w, h) = position and size of the field
        @author C.Dutoit
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)
        pyutObject = self.getPyutObject()
        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # define space between text and line
        lth = dc.GetTextExtent("*")[1] / 2.0

        # Add space
        if len(self.getPyutObject().getFields()) > 0:
            h += lth

        # draw pyutClass fields
        if pyutObject.getShowFields():
            for field in self.getPyutObject().getFields():
                if draw:
                    dc.DrawText(str(field), x + MARGIN, y + h)
                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(field)))

                h += self.GetTextHeight(dc, str(field))

        # Add space
        if len(self.getPyutObject().getFields()) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def calculateClassMethods(self, dc, draw=False, initialX=None, initialY=None, calcWidth=False):
        """
        Calculate the class methods position and size and display it if
        a draw is True

        @return tuple : (x, y, w, h) = position and size of the methods
        @author C.Dutoit
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)
        pyutObject = self.getPyutObject()
        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # define space between text and line
        lth = dc.GetTextExtent("*")[1] / 2.0

        # Add space
        if len(self.getPyutObject().getMethods()) > 0:
            h += lth

        # draw pyutClass methods
        # print "showmethods => ", pyutObject.getShowMethods()
        if pyutObject.getShowMethods():
            for method in self.getPyutObject().getMethods():
                if draw:
                    dc.DrawText(str(method), x + MARGIN, y + h)
                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(method)))
                # separate tow methods
                # h += height
                h += self.GetTextHeight(dc, str(method))

        # Add space
        if len(self.getPyutObject().getMethods()) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def Draw(self, dc, withChildren=False):
        """
        Paint handler, draws the content of the shape.

        WARNING : Every changes here must be reported in autoResize method

        Args:
            dc: device context to draw to
            withChildren:
        """
        # Init
        pyutObject = self.getPyutObject()

        # Draw rectangle shape
        OglObject.Draw(self, dc)

        # drawing is restricted in the specified region of the device
        w, h = self._width, self._height
        x, y = self.GetPosition()           # Get position
        dc.SetClippingRegion(x, y, w, h)

        # Draw header
        (headerX, headerY, headerW, headerH) = self.calculateClassHeader(dc, True)
        y = headerY + headerH

        if pyutObject.getShowFields():
            # Draw line
            dc.DrawLine(x, y, x + w, y)

            # Draw fields
            (fieldsX, fieldsY, fieldsW, fieldsH) = self.calculateClassFields(dc, True, initialY=y)
            y = fieldsY + fieldsH
        # Draw line
        dc.DrawLine(x, y, x + w, y)
        dc.DestroyClippingRegion()

    def autoResize(self):
        """
        Auto-resize the class

        @author C.Dutoit
        WARNING : Every changes here must be reported in DRAW method
        """
        # Init
        pyutObject = self.getPyutObject()
        dc = ClientDC(self.GetDiagram().GetPanel())

        # Get header size
        (headerX, headerY, headerW, headerH) = self.calculateClassHeader(dc, False, calcWidth=True)
        y = headerY + headerH

        # Get fields size
        if pyutObject.getShowFields():
            (fieldsX, fieldsY, fieldsW, fieldsH) = self.calculateClassFields(dc, False, initialY=y, calcWidth=True)
            y = fieldsY + fieldsH
        else:
            fieldsW, fieldsH = 0, 0

        # Get methods size
        if pyutObject.getShowMethods():
            (methX, methY, methW, methH) = self.calculateClassMethods(dc, False, initialY=y, calcWidth=True)
            y = methY + methH
        else:
            methW, methH = 0, 0

        w = max(headerW, fieldsW, methW)
        h = y - headerY
        w += 2.0 * MARGIN
        self.SetSize(w, h)

        # to automatically replace the sizers at a correct place
        if self.IsSelected():
            self.SetSelected(False)
            self.SetSelected(True)

    def OnMenuClick(self, event):
        """
        Callback for menu clicks.

        @author C.Dutoit
        """
        pyutObject = self.getPyutObject()
        if event.GetId() == MNU_TOGGLE_STEREOTYPE:
            pyutObject.setShowStereotype(not pyutObject.getShowStereotype())
            self.autoResize()
        elif event.GetId() == MNU_TOGGLE_METHODS:
            pyutObject.setShowMethods(not pyutObject.getShowMethods())
            self.autoResize()
        elif event.GetId() == MNU_TOGGLE_FIELDS:
            pyutObject.setShowFields(not pyutObject.getShowFields())
            self.autoResize()
        elif event.GetId() == MNU_FIT_FIELDS:
            self.autoResize()
        elif event.GetId() == MNU_CUT_SHAPE:
            ctrl = getMediator()
            ctrl.deselectAllShapes()
            self.SetSelected(True)
            ctrl.cutSelectedShapes()
        else:
            event.skip()

    def OnRightDown(self, event):
        """
        Callback for right clicks.

        @author C.Dutoit
        """
        pyutObject = self.getPyutObject()
        menu = Menu()
        menu.Append(MNU_TOGGLE_STEREOTYPE, _("Toggle stereotype display"), _("Set on or off the stereotype display"), True)
        item = menu.FindItemById(MNU_TOGGLE_STEREOTYPE)
        item.Check(pyutObject.getShowStereotype())

        menu.Append(MNU_TOGGLE_FIELDS, _("Toggle fields display"), _("Set on or off the fields display"), True)
        item = menu.FindItemById(MNU_TOGGLE_FIELDS)
        item.Check(pyutObject.getShowFields())

        menu.Append(MNU_TOGGLE_METHODS, _("Toggle methods display"), _("Set on or off the methods display"), True)
        item = menu.FindItemById(MNU_TOGGLE_METHODS)
        item.Check(pyutObject.getShowMethods())

        menu.Append(MNU_FIT_FIELDS, _("Fit Fields"), _("Fit to see all class fields"))
        menu.Append(MNU_CUT_SHAPE,  _("Cut shape"),  _("Cut this shape"))

        frame    = self._diagram.GetPanel()

        # Callback
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MNU_TOGGLE_STEREOTYPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MNU_TOGGLE_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MNU_TOGGLE_METHODS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MNU_FIT_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MNU_CUT_SHAPE)

        x: int = event.GetX()
        y: int = event.GetY()
        self.logger.debug(f'OglClass - x,y: {x},{y}')
        frame.PopupMenu(menu, x, y)
