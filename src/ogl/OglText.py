
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import Colour
from wx import ColourDatabase
from wx import EVT_MENU
from wx import FONTSTYLE_ITALIC
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import FONTWEIGHT_NORMAL

from wx import Bitmap
from wx import CommandEvent
from wx import DC
from wx import Font
from wx import Menu
from wx import MenuItem
from wx import MouseEvent

from wx import RED_PEN


from miniogl.DiagramFrame import DiagramFrame

from ogl.OglObject import OglObject
from ogl.OglTextFontFamily import OglTextFontFamily

from ogl.OglUtils import OglUtils

from ogl.preferences.OglPreferences import OglPreferences

from ogl.resources.img.textdetails.DecreaseTextSize import embeddedImage as DecreaseTextSize
from ogl.resources.img.textdetails.IncreaseTextSize import embeddedImage as IncreaseTextSize

from pyutmodel.PyutText import PyutText
[
    ID_MENU_INCREASE_SIZE,
    ID_MENU_DECREASE_SIZE,
    ID_MENU_BOLD_TEXT,
    ID_MENU_ITALIC_TEXT
]  = OglUtils.assignID(4)

TEXT_SIZE_INCREMENT: int = 2
TEXT_SIZE_DECREMENT: int = 2


class OglText(OglObject):
    """
    Draws resizeable boxes of text with no visible boundaries
    PyutText should not have graphical attributes.
    """
    MARGIN: int = 5

    def __init__(self, pyutText: PyutText, width: int = 0, height: int = 0):    # TODO make default text size a preference
        """
        Args:
            pyutText:   Associated PyutText instance
            width:      Initial width
            height:     Initial height
        """
        w: int = width
        h: int = height

        # Use preferences to get initial size if not specified
        preferences: OglPreferences = OglPreferences()

        if width == 0:
            w = preferences.textDimensions.width
        if height == 0:
            h = preferences.textDimensions.height

        super().__init__(pyutObject=pyutText, width=w, height=h)

        self.logger: Logger = getLogger(__name__)

        self._drawFrame:      bool = False
        self._textFontFamily: OglTextFontFamily = preferences.textFontFamily
        self._textSize:       int  = preferences.textFontSize
        self._isBold:         bool = preferences.textBold
        self._isItalicized:   bool = preferences.textItalicize

        self._textFont:  Font            = self._defaultFont.GetBaseFont()
        self._textFont.SetFamily(OglUtils.oglFontFamilyToWxFontFamily(self._textFontFamily))

        self._redColor:   Colour  = ColourDatabase().Find('Red')
        self._blackColor: Colour = ColourDatabase().Find('Black')

        self.__initializeTextDisplay()
        self._menu: Menu = cast(Menu, None)

    @property
    def pyutText(self) -> PyutText:
        return self._pyutObject

    @pyutText.setter
    def pyutText(self, newValue: PyutText):
        self._pyutObject = newValue

    @property
    def textSize(self) -> int:
        return self._textSize

    @textSize.setter
    def textSize(self, newSize: int):
        self._textSize = newSize

    @property
    def isBold(self) -> bool:
        return self._isBold

    @isBold.setter
    def isBold(self, newValue: bool):
        self._isBold = newValue

    @property
    def isItalicized(self) -> bool:
        return self._isItalicized

    @isItalicized.setter
    def isItalicized(self, newValue: bool):
        self._isItalicized = newValue

    @property
    def textFontFamily(self) -> OglTextFontFamily:
        return self._textFontFamily

    @textFontFamily.setter
    def textFontFamily(self, newValue: OglTextFontFamily):
        self._textFontFamily = newValue

    def OnLeftUp(self, event: MouseEvent):
        """
        Implement this method so we can snap Ogl objects

        Args:
            event:  the mouse event
        """
        super().OnLeftUp(event)

    def OnRightDown(self, event: MouseEvent):
        """
        Callback for right clicks
        """
        if self._menu is None:
            self._menu = self._createMenu()

        frame = self._diagram.GetPanel()

        x: int = event.GetX()
        y: int = event.GetY()
        self.logger.debug(f'OglClass - x,y: {x},{y}')

        frame.PopupMenu(self._menu, x, y)

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Paint handler, draws the content of the shape.

        Args:
            dc:     device context to draw to
            withChildren:   Redraw children or not
        """
        if self._selected:
            dc.SetPen(RED_PEN)
            dc.SetTextForeground(self._redColor)
        else:
            dc.SetPen(BLACK_PEN)
            dc.SetTextForeground(self._blackColor)

        OglObject.Draw(self, dc)
        dc.SetFont(self._textFont)

        w, h = self.GetSize()

        baseX, baseY = self.GetPosition()

        dc.SetClippingRegion(baseX, baseY, w, h)

        noteContent = self.pyutObject.content
        lines = OglUtils.lineSplitter(noteContent, dc, w - 2 * OglText.MARGIN)

        x = baseX + OglText.MARGIN
        y = baseY + OglText.MARGIN

        for line in range(len(lines)):
            dc.DrawText(lines[line], x, y + line * (dc.GetCharHeight() + 5))

        dc.DestroyClippingRegion()

    def _createMenu(self) -> Menu:

        menu: Menu = Menu()

        increaseItem: MenuItem = menu.Append(ID_MENU_INCREASE_SIZE, 'Increase Size', 'Increase Text Size by 2 points')
        decreaseItem: MenuItem = menu.Append(ID_MENU_DECREASE_SIZE, 'Decrease Size', 'Decrease Text Size by 2 points')

        incBmp: Bitmap = IncreaseTextSize.GetBitmap()
        increaseItem.SetBitmap(incBmp)
        decBmp: Bitmap = DecreaseTextSize.GetBitmap()
        decreaseItem.SetBitmap(decBmp)

        boldItem:       MenuItem = menu.AppendCheckItem(ID_MENU_BOLD_TEXT,   item='Bold Text',      help='Set text to bold')
        italicizedItem: MenuItem = menu.AppendCheckItem(ID_MENU_ITALIC_TEXT, item='Italicize Text', help='Set text to italics')

        if self.isBold is True:
            boldItem.Check(check=True)
        if self.isItalicized is True:
            italicizedItem.Check(check=True)

        menu.Bind(EVT_MENU, self._onChangeTextSize, id=ID_MENU_INCREASE_SIZE)
        menu.Bind(EVT_MENU, self._onChangeTextSize, id=ID_MENU_DECREASE_SIZE)
        menu.Bind(EVT_MENU, self._onToggleBold,     id=ID_MENU_BOLD_TEXT)
        menu.Bind(EVT_MENU, self._onToggleItalicize, id=ID_MENU_ITALIC_TEXT)

        return menu

    def _onChangeTextSize(self, event: CommandEvent):
        """
        Callback for popup menu on class

        Args:
            event:
        """
        eventId:  int      = event.GetId()

        if eventId == ID_MENU_INCREASE_SIZE:
            self.textSize += TEXT_SIZE_INCREMENT
        elif eventId == ID_MENU_DECREASE_SIZE:
            self.textSize -= TEXT_SIZE_DECREMENT
        else:
            assert False, f'Unhandled text size event: {eventId}'

        self._textFont.SetPointSize(self.textSize)
        self.__updateDisplay()

    # noinspection PyUnusedLocal
    def _onToggleBold(self, event: CommandEvent):

        if self.isBold is True:
            self.isBold = False
            self._textFont.SetWeight(FONTWEIGHT_NORMAL)
        else:
            self.isBold = True
            self._textFont.SetWeight(FONTWEIGHT_BOLD)

        self.__updateDisplay()

    # noinspection PyUnusedLocal
    def _onToggleItalicize(self, event: CommandEvent):

        if self.isItalicized is True:
            self.isItalicized = False
            self._textFont.SetStyle(FONTSTYLE_NORMAL)
        else:
            self.isItalicized = True
            self._textFont.SetStyle(FONTSTYLE_ITALIC)

        self.__updateDisplay()

    def __updateDisplay(self):

        self.autoResize()

        frame: DiagramFrame = self._diagram.GetPanel()
        frame.Refresh()

    def __initializeTextDisplay(self):
        """
        Use the model to get other text attributes; We'll
        get what was specified or defaults
        """

        self._textFont.SetPointSize(self.textSize)

        if self.isBold is True:
            self._textFont.SetWeight(FONTWEIGHT_BOLD)
        if self.isItalicized is True:
            self._textFont.SetWeight(FONTWEIGHT_NORMAL)

        if self.isItalicized is True:
            self._textFont.SetStyle(FONTSTYLE_ITALIC)
        else:
            self._textFont.SetStyle(FONTSTYLE_NORMAL)

        self._textFont.SetPointSize(self.textSize)
        self._textFont.SetFamily(OglUtils.oglFontFamilyToWxFontFamily(self.textFontFamily))

    def __repr__(self):

        strMe: str = f"[OglText - name: '{self._pyutObject.name}' id: '{self._pyutObject.id}']"
        return strMe
