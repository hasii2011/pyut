
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import DC
from wx import EVT_MENU
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD

from wx import Font
from wx import ClientDC
from wx import Menu
from wx import CommandEvent
from wx import MenuItem
from wx import MouseEvent
# from wx import PostEvent

from org.pyut.model.PyutDisplayParameters import PyutDisplayParameters
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutObject import PyutObject
from org.pyut.model.PyutClass import PyutClass

from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglObject import DEFAULT_FONT_SIZE
from org.pyut.ogl.events.OglEventEngine import OglEventEngine

# from org.pyut.ogl.events.OglEvents import CutOglClassEvent
# from org.pyut.ogl.events.OglEvents import RequestLollipopLocationEvent

from org.pyut.PyutConstants import PyutConstants

from org.pyut.PyutUtils import PyutUtils

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from org.pyut.preferences.PyutPreferences import PyutPreferences

# Menu IDs

[
    MENU_TOGGLE_STEREOTYPE,
    MENU_TOGGLE_FIELDS,
    MENU_TOGGLE_METHODS,
    MENU_TOGGLE_METHOD_PARAMETERS,
    MENU_FIT_FIELDS,
    MENU_CUT_SHAPE,
    MENU_IMPLEMENT_INTERFACE
]  = PyutUtils.assignID(7)

MARGIN: int = 10


class OglClass(OglObject):
    """
    OGL object that represents a UML class in class diagrams.
    This class defines OGL objects that represents a class. You can just
    instantiate an OGL class and add it to the diagram, links, resizing,
    ... are managed by parent class `OglObject`.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.
    """
    def __init__(self, pyutClass: PyutClass = None, w: int = 0, h: int = 0):
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

        width:  int = w
        height: int = h

        # Use preferences to get initial size if not specified
        # Note: auto_resize_shape_on_edit must be False for this size to actually stick
        preferences: PyutPreferences = PyutPreferences()

        if w == 0:
            width = preferences.classDimensions.width
        if h == 0:
            height = preferences.classDimensions.height

        super().__init__(pyutObject, width=width, height=height)

        self._nameFont: Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        self.logger:    Logger = getLogger(__name__)

    def GetTextWidth(self, dc, text):
        width = dc.GetTextExtent(text)[0]
        return width

    def GetTextHeight(self, dc, text):
        height = dc.GetTextExtent(text)[1]
        return height

    def calculateClassHeader(self, dc, draw=False, initialX=None, initialY=None, calcWidth=False):
        """
        Calculate the class header position and size and display it if
        a draw is True

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns:    tuple (x, y, w, h) = position and size of the header
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)
        # pyutObject = self.getPyutObject()
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
        lth = dc.GetTextExtent("*")[1] // 2

        # from where begin the text
        h += lth

        # draw a pyutClass name
        name = self.pyutObject.name
        dc.SetFont(self._nameFont)
        nameWidth = self.GetTextWidth(dc, name)
        if draw:
            dc.DrawText(name, x + (w - nameWidth) // 2, y + h)
        if calcWidth:
            w = max(nameWidth, w)
        dc.SetFont(self._defaultFont)
        h += self.GetTextHeight(dc, str(name))
        h += lth

        # draw the stereotype if there's one
        pyutClass: PyutClass = self.pyutObject
        # stereo = self.getPyutObject().getStereotype()
        stereo = pyutClass.getStereotype()
        if stereo is not None and pyutClass.getShowStereotype() is True:
            name = str(stereo)
            nameWidth = self.GetTextWidth(dc, name)
            if draw:
                dc.DrawText(name, x + (w - nameWidth) // 2, y + h)
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

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns:    tuple : (x, y, w, h) = position and size of the field
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
        lth: int = dc.GetTextExtent("*")[1] // 2

        # Add space
        pyutClass: PyutClass = cast(PyutClass, self.pyutObject)
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
        lth = dc.GetTextExtent("*")[1] // 2

        # Add space
        pyutClass: PyutClass = cast(PyutClass, self.pyutObject)
        if len(pyutClass.methods) > 0:
            h += lth

        # draw pyutClass methods
        self.logger.debug(f"showMethods => {pyutClass.showMethods}")
        if pyutClass.showMethods is True:
            for method in pyutClass.methods:
                if draw is True:
                    self.__drawMethodSignature(dc, method, pyutClass, x, y, h)

                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(method)))

                h += self.GetTextHeight(dc, str(method))

        # Add space
        if len(pyutClass.methods) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def Draw(self, dc, withChildren=False):
        """
        Paint handler, draws the content of the shape.

        WARNING : Every change here must be reported in autoResize pyutMethod

        Args:
            dc: device context to draw to
            withChildren:
        """

        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)

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

        WARNING : Every change here must be reported in DRAW pyutMethod
        """
        # Init
        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)
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
        w += 2 * MARGIN
        self.SetSize(w, h)

        # to automatically replace the sizers at a correct place
        if self.IsSelected():
            self.SetSelected(False)
            self.SetSelected(True)

    def OnRightDown(self, event: MouseEvent):
        """
        Callback for right clicks
        """
        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)
        menu:       Menu      = Menu()

        menu.Append(MENU_TOGGLE_STEREOTYPE, _("Toggle stereotype display"), _("Set stereotype display on or off"), True)
        item = menu.FindItemById(MENU_TOGGLE_STEREOTYPE)
        item.Check(pyutObject.getShowStereotype())

        menu.Append(MENU_TOGGLE_FIELDS, _("Toggle fields display"), _("Set fields display on or off"), True)
        item = menu.FindItemById(MENU_TOGGLE_FIELDS)
        item.Check(pyutObject.showFields)

        menu.Append(MENU_TOGGLE_METHODS, _("Toggle methods display"), _("Set methods display on or off "), True)
        item = menu.FindItemById(MENU_TOGGLE_METHODS)
        item.Check(pyutObject.showMethods)

        menu.Append(MENU_TOGGLE_METHOD_PARAMETERS, _("Toggle parameter display"), _("Set parameter display on or off"), True)

        itemToggleParameters: MenuItem = menu.FindItemById(MENU_TOGGLE_METHOD_PARAMETERS)
        displayParameters: PyutDisplayParameters = self.pyutObject.displayParameters

        self._initializeTriStateDisplayParametersMenuItem(displayParameters, itemToggleParameters)

        menu.Append(MENU_FIT_FIELDS, _("Fit Fields"), _("Fit to see all class fields"))
        menu.Append(MENU_CUT_SHAPE,  _("Cut shape"), _("Cut this shape"))

        menu.Append(MENU_IMPLEMENT_INTERFACE, _('Implement Interface'), _('Use Existing interface or create new one'))

        frame = self._diagram.GetPanel()

        # Callback
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_STEREOTYPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_METHODS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_FIT_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_CUT_SHAPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_IMPLEMENT_INTERFACE)
        menu.Bind(EVT_MENU, self.onDisplayParametersClick, id=MENU_TOGGLE_METHOD_PARAMETERS)

        x: int = event.GetX()
        y: int = event.GetY()
        self.logger.debug(f'OglClass - x,y: {x},{y}')
        frame.PopupMenu(menu, x, y)

    def OnMenuClick(self, event: CommandEvent):
        """
        Callback for popup menu on class

        Args:
            event:
        """
        pyutObject:   PyutClass = cast(PyutClass, self.pyutObject)
        eventId:      int       = event.GetId()

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
            OglEventEngine().sendCutShapeEvent(shapeToCut=self)
        elif eventId == MENU_IMPLEMENT_INTERFACE:
            OglEventEngine().sendRequestLollipopLocationEvent(requestShape=self)
        else:
            event.Skip()

    def onDisplayParametersClick(self, event: CommandEvent):
        """
        This menu item has its own handler because this option is tri-state

        Unspecified --> Display  --> Do Not Display ---|
            ^------------------------------------------|

        Args:
            event:
        """
        self.logger.warning(f'{event.GetClientObject()=}')
        pyutClass:         PyutClass             = cast(PyutClass, self.pyutObject)
        displayParameters: PyutDisplayParameters = pyutClass.displayParameters

        if displayParameters == PyutDisplayParameters.UNSPECIFIED:
            pyutClass.displayParameters = PyutDisplayParameters.DISPLAY
        elif displayParameters == PyutDisplayParameters.DISPLAY:
            pyutClass.displayParameters = PyutDisplayParameters.DO_NOT_DISPLAY
        elif displayParameters == PyutDisplayParameters.DO_NOT_DISPLAY:
            pyutClass.displayParameters = PyutDisplayParameters.UNSPECIFIED
        else:
            assert False, 'Unknown display type'

    def _isSameName(self, other) -> bool:

        ans: bool = False
        selfPyutObj:  PyutObject = self.pyutObject
        otherPyutObj: PyutObject = other.pyutObject

        if selfPyutObj.name == otherPyutObj.name:
            ans = True
        return ans

    def _isSameId(self, other):

        ans: bool = False
        if self.GetID() == other.GetID():
            ans = True
        return ans

    def _initializeTriStateDisplayParametersMenuItem(self, displayParameters: PyutDisplayParameters, itemToggleParameters: MenuItem):

        if displayParameters == PyutDisplayParameters.UNSPECIFIED:
            itemToggleParameters.SetBitmap(PyutConstants.unspecifiedDisplayMethodsIcon())
        elif displayParameters == PyutDisplayParameters.DISPLAY:
            itemToggleParameters.SetBitmap(PyutConstants.displayMethodsIcon())
        elif displayParameters == PyutDisplayParameters.DO_NOT_DISPLAY:
            itemToggleParameters.SetBitmap(PyutConstants.doNotDisplayMethodsIcon())
        else:
            assert False, 'Unknown display type'

    def __drawMethodSignature(self, dc: DC, pyutMethod: PyutMethod, pyutClass: PyutClass, x: int, y: int, h: int):
        """
        If preference is not set at individual class level defer to global; Otherwise,
        respect the class level preference

        Args:
            dc:
            pyutMethod:
            pyutClass:
            x:
            y:
            h:
        """
        if pyutClass.displayParameters == PyutDisplayParameters.UNSPECIFIED:
            dc.DrawText(str(pyutMethod), x + MARGIN, y + h)
        elif pyutClass.displayParameters == PyutDisplayParameters.DISPLAY:
            dc.DrawText(pyutMethod.methodWithParameters(), x + MARGIN, y + h)
        elif pyutClass.displayParameters == PyutDisplayParameters.DO_NOT_DISPLAY:
            dc.DrawText(pyutMethod.methodWithoutParameters(), x + MARGIN, y + h)
        else:
            assert False, 'Internal error unknown pyutMethod parameter display type'

    def __repr__(self):
        selfName:   str = self.pyutObject.name
        return f'OglClass.{selfName} id: {self.GetID()}'

    def __eq__(self, other) -> bool:

        if isinstance(other, OglClass):
            if self._isSameName(other) is True and self._isSameId(other) is True:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):

        selfPyutObj:  PyutObject = self.pyutObject

        return hash(selfPyutObj.name) + hash(self.GetID())
