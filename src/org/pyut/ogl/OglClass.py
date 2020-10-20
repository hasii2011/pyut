
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import EVT_MENU
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD

from wx import Font
from wx import ClientDC
from wx import Menu
from wx import CommandEvent

from org.pyut.model.PyutObject import PyutObject
from org.pyut.model.PyutClass import PyutClass

from org.pyut.ogl.OglDisplayParameters import OglDisplayParameters
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglObject import DEFAULT_FONT_SIZE

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _


# Menu IDs

[
    MENU_TOGGLE_STEREOTYPE,
    MENU_TOGGLE_FIELDS,
    MENU_TOGGLE_METHODS,
    MENU_FIT_FIELDS,
    MENU_CUT_SHAPE,
    MENU_IMPLEMENT_INTERFACE
]  = PyutUtils.assignID(6)

MARGIN:               float = 10.0
DEFAULT_CLASS_WIDTH:  float = 100.0
DEFAULT_CLASS_HEIGHT: float = 100.0


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
    def __init__(self, pyutClass: PyutClass = None, w: float = DEFAULT_CLASS_WIDTH, h: float = DEFAULT_CLASS_HEIGHT):
        """

        Args:
            pyutClass:  a PyutClass object
            w:  Width of the shape
            h:  Height of the shape
        """
        if pyutClass is None:
            pyutObject = PyutClass()
        else:
            pyutObject = pyutClass
        super().__init__(pyutObject, w, h)

        self._nameFont: Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        self.logger:    Logger = getLogger(__name__)

        self._displayParameters: OglDisplayParameters = OglDisplayParameters.UNSPECIFIED

    @property
    def displayParameters(self) -> OglDisplayParameters:
        return self._displayParameters

    @displayParameters.setter
    def displayParameters(self, newValue: OglDisplayParameters):
        self._displayParameters = newValue

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
        pyutClass: PyutClass = self.getPyutObject()
        if len(pyutClass.fields) > 0:
            h += lth

        # draw pyutClass fields
        if pyutClass.showFields is True:
            for field in pyutClass.fields:
                if draw:
                    dc.DrawText(str(field), x + MARGIN, y + h)
                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(field)))

                h += self.GetTextHeight(dc, str(field))

        # Add space
        if len(pyutClass.fields) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def calculateClassMethods(self, dc, draw=True, initialX=None, initialY=None, calcWidth=False) -> Tuple[int, int, int, int]:
        """
        Calculate the class methods position and size and display it if
        a draw is True

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns:    tuple : (x, y, w, h) = position and size of the methods
        """

        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)

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
        pyutClass: PyutClass = self.getPyutObject()
        if len(pyutClass.methods) > 0:
            h += lth

        # draw pyutClass methods
        self.logger.debug(f"showMethods => {pyutClass.showMethods}")
        if pyutClass.showMethods is True:
            for method in pyutClass.methods:
                if draw:
                    dc.DrawText(str(method), x + MARGIN, y + h)
                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(method)))
                # separate two methods
                # h += height
                h += self.GetTextHeight(dc, str(method))

        # Add space
        if len(pyutClass.methods) > 0:
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

        pyutObject: PyutClass = self.getPyutObject()

        # Draw rectangle shape
        OglObject.Draw(self, dc)

        # drawing is restricted in the specified region of the device
        w, h = self._width, self._height
        x, y = self.GetPosition()           # Get position
        dc.SetClippingRegion(x, y, w, h)

        # Draw header
        (headerX, headerY, headerW, headerH) = self.calculateClassHeader(dc, True)
        y = headerY + headerH

        if pyutObject.showFields is True:
            # Draw line
            dc.DrawLine(x, y, x + w, y)

            # Draw fields
            (fieldsX, fieldsY, fieldsW, fieldsH) = self.calculateClassFields(dc, True, initialY=y)
            y = fieldsY + fieldsH
        # Draw line
        dc.DrawLine(x, y, x + w, y)
        #
        # Method needs to be called even though returned values not used  -- TODO look at refactoring
        #
        if pyutObject.showMethods is True:
            (methodsX, methodsY, methodsW, methodsH) = self.calculateClassMethods(dc, True, initialY=y, calcWidth=True)
            # noinspection PyUnusedLocal
            y = methodsY + methodsH

        dc.DestroyClippingRegion()

    def autoResize(self):
        """
        Auto-resize the class

        @author C.Dutoit
        WARNING : Every changes here must be reported in DRAW method
        """
        # Init
        pyutObject: PyutClass = self.getPyutObject()
        dc = ClientDC(self.GetDiagram().GetPanel())

        # Get header size
        (headerX, headerY, headerW, headerH) = self.calculateClassHeader(dc, False, calcWidth=True)
        y = headerY + headerH

        # Get fields size
        if pyutObject.showFields is True:
            (fieldsX, fieldsY, fieldsW, fieldsH) = self.calculateClassFields(dc, False, initialY=y, calcWidth=True)
            y = fieldsY + fieldsH
        else:
            fieldsW, fieldsH = 0, 0

        # Get methods size
        if pyutObject.showMethods is True:
            (methodX, methodY, methodW, methodH) = self.calculateClassMethods(dc, True, initialY=y, calcWidth=True)
            y = methodY + methodH
        else:
            methodW, methodH = 0, 0

        w = max(headerW, fieldsW, methodW)
        h = y - headerY
        w += 2.0 * MARGIN
        self.SetSize(w, h)

        # to automatically replace the sizers at a correct place
        if self.IsSelected():
            self.SetSelected(False)
            self.SetSelected(True)

    def OnMenuClick(self, event: CommandEvent):
        """
        Callback for popup menu on class

        Args:
            event:
        """
        from org.pyut.general.Mediator import getMediator   # avoid circular import

        pyutObject: PyutClass = self.getPyutObject()
        eventId:    int       = event.GetId()
        if eventId == MENU_TOGGLE_STEREOTYPE:
            pyutObject.setShowStereotype(not pyutObject.getShowStereotype())
            self.autoResize()
        elif eventId == MENU_TOGGLE_METHODS:
            pyutObject.showMethods = not pyutObject.showMethods     # flip it!!  too cute
            self.autoResize()
        elif eventId == MENU_TOGGLE_FIELDS:
            pyutObject.showFields = not pyutObject.showFields       # flip it!! too cute
            self.autoResize()
        elif eventId == MENU_FIT_FIELDS:
            self.autoResize()
        elif eventId == MENU_CUT_SHAPE:
            ctrl = getMediator()
            ctrl.deselectAllShapes()
            self.SetSelected(True)
            ctrl.cutSelectedShapes()
        elif eventId == MENU_IMPLEMENT_INTERFACE:
            ctrl = getMediator()
            ctrl.requestLollipopLocation(self)
        else:
            event.Skip()

    def OnRightDown(self, event):
        """
        Callback for right clicks.

        @author C.Dutoit
        """
        pyutObject: PyutClass = self.getPyutObject()
        menu:       Menu      = Menu()

        menu.Append(MENU_TOGGLE_STEREOTYPE, _("Toggle stereotype display"), _("Set on or off the stereotype display"), True)
        item = menu.FindItemById(MENU_TOGGLE_STEREOTYPE)
        item.Check(pyutObject.getShowStereotype())

        menu.Append(MENU_TOGGLE_FIELDS, _("Toggle fields display"), _("Set on or off the fields display"), True)
        item = menu.FindItemById(MENU_TOGGLE_FIELDS)
        item.Check(pyutObject.showFields)

        menu.Append(MENU_TOGGLE_METHODS, _("Toggle methods display"), _("Set on or off the methods display"), True)
        item = menu.FindItemById(MENU_TOGGLE_METHODS)
        item.Check(pyutObject.showMethods)

        menu.Append(MENU_FIT_FIELDS, _("Fit Fields"), _("Fit to see all class fields"))
        menu.Append(MENU_CUT_SHAPE,  _("Cut shape"), _("Cut this shape"))

        menu.Append(MENU_IMPLEMENT_INTERFACE, _('Implement Interface'), _('Use Existing interface or create new one'))

        frame    = self._diagram.GetPanel()

        # Callback
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_STEREOTYPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_METHODS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_FIT_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_CUT_SHAPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_IMPLEMENT_INTERFACE)

        x: int = event.GetX()
        y: int = event.GetY()
        self.logger.debug(f'OglClass - x,y: {x},{y}')
        frame.PopupMenu(menu, x, y)

    def __repr__(self):
        selfName:   str = self.getPyutObject().getName()
        return f'OglClass.{selfName}'

    def __eq__(self, other):

        if isinstance(other, OglClass):
            if self._isSameName(other) is True and self._isSameId(other) is True:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):

        selfPyutObj:  PyutObject = self.getPyutObject()

        return hash(selfPyutObj.getName()) + hash(self.GetID())

    def _isSameName(self, other) -> bool:

        ans: bool = False
        selfPyutObj:  PyutObject = self.getPyutObject()
        otherPyutObj: PyutObject = other.getPyutObject()

        if selfPyutObj.getName() == otherPyutObj.getName():
            ans = True
        return ans

    def _isSameId(self, other):

        ans: bool = False
        if self.GetID() == other.GetID():
            ans = True
        return ans
