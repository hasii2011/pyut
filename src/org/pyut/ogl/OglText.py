

from typing import cast

from logging import Logger
from logging import getLogger

from wx import Bitmap
from wx import CommandEvent
from wx import DC
from wx import EVT_MENU
from wx import FONTSTYLE_ITALIC
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import FONTWEIGHT_NORMAL
from wx import Font
from wx import Menu
from wx import MenuItem
from wx import MouseEvent

from org.pyut.general.Globals import _
from org.pyut.general.LineSplitter import LineSplitter
from org.pyut.miniogl.DiagramFrame import DiagramFrame

from org.pyut.model.PyutText import PyutText

from org.pyut.ogl.OglObject import OglObject

from org.pyut.PyutUtils import PyutUtils

from org.pyut.resources.img.textdetails.DecreaseTextSize import embeddedImage as DecreaseTextSize
from org.pyut.resources.img.textdetails.IncreaseTextSize import embeddedImage as IncreaseTextSize

[
    ID_MENU_INCREASE_SIZE,
    ID_MENU_DECREASE_SIZE,
    ID_MENU_BOLD_TEXT,
    ID_MENU_ITALIC_TEXT
]  = PyutUtils.assignID(4)

TEXT_SIZE_INCREMENT: int = 2    # TODO should be a preference
TEXT_SIZE_DECREMENT: int = 2    # TODO should be a preference


class OglText(OglObject):
    """
        Draws resizeable boxes of text with no visible boundaries
    """
    MARGIN: int = 5

    def __init__(self, pyutObject=None, width: int = 125, height: int = 50):    # TODO make default text size a preference
        """
        Args:
            pyutObject: Associated PyutObject
            width:      Initial width
            height:     Initial height
        """
        super().__init__(pyutObject=pyutObject, width=width, height=height)

        self.logger: Logger = getLogger(__name__)

        self._drawFrame: bool = False
        self._textFont:  Font = self._defaultFont.GetBaseFont()

        self._menu: Menu = cast(Menu, None)

    @property
    def pyutText(self) -> PyutText:
        return self._pyutObject

    @pyutText.setter
    def pyutText(self, newValue: PyutText):
        self._pyutObject = newValue

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
        OglObject.Draw(self, dc)
        dc.SetFont(self._textFont)

        w, h = self.GetSize()

        baseX, baseY = self.GetPosition()

        dc.SetClippingRegion(baseX, baseY, w, h)

        noteContent = cast(PyutText, self.getPyutObject()).content
        lines = LineSplitter().split(noteContent, dc, w - 2 * OglText.MARGIN)

        x = baseX + OglText.MARGIN
        y = baseY + OglText.MARGIN

        for line in range(len(lines)):
            dc.DrawText(lines[line], x, y + line * (dc.GetCharHeight() + 5))

        dc.DestroyClippingRegion()

    def _createMenu(self) -> Menu:

        menu: Menu = Menu()

        increaseItem: MenuItem = menu.Append(ID_MENU_INCREASE_SIZE, _('Increase Size'), _('Increase Text Size by 2 points'))
        decreaseItem: MenuItem = menu.Append(ID_MENU_DECREASE_SIZE, _('Decrease Size'), _('Decrease Text Size by 2 points'))

        incBmp: Bitmap = IncreaseTextSize.GetBitmap()
        increaseItem.SetBitmap(incBmp)
        decBmp: Bitmap = DecreaseTextSize.GetBitmap()
        decreaseItem.SetBitmap(decBmp)

        menu.AppendCheckItem(ID_MENU_BOLD_TEXT, item=_('Bold Text'), help=_('Set text to bold'))
        menu.AppendCheckItem(ID_MENU_ITALIC_TEXT, item=_('Italicize Text'), help=_('Set text to italics'))

        menu.Bind(EVT_MENU, self._onChangeTextSize, id=ID_MENU_INCREASE_SIZE)
        menu.Bind(EVT_MENU, self._onChangeTextSize, id=ID_MENU_DECREASE_SIZE)
        menu.Bind(EVT_MENU, self._onToggleBold, id=ID_MENU_BOLD_TEXT)
        menu.Bind(EVT_MENU, self._onToggleItalicize, id=ID_MENU_ITALIC_TEXT)

        return menu

    def _onChangeTextSize(self, event: CommandEvent):
        """
        Callback for popup menu on class

        Args:
            event:
        """
        pyutText: PyutText = self.pyutText
        eventId:  int      = event.GetId()

        if eventId == ID_MENU_INCREASE_SIZE:
            pyutText.textSize += TEXT_SIZE_INCREMENT
        elif eventId == ID_MENU_DECREASE_SIZE:
            pyutText.textSize -= TEXT_SIZE_DECREMENT
        else:
            assert False, f'Unhandled text size event: {eventId}'

        self._textFont.SetPointSize(pyutText.textSize)
        self.__updateDisplay()

    # noinspection PyUnusedLocal
    def _onToggleBold(self, event: CommandEvent):

        pyutText: PyutText = self.pyutText

        if pyutText.isBold is True:
            pyutText.isBold = False
            self._textFont.SetWeight(FONTWEIGHT_NORMAL)
        else:
            pyutText.isBold = True
            self._textFont.SetWeight(FONTWEIGHT_BOLD)

        self.__updateDisplay()

    # noinspection PyUnusedLocal
    def _onToggleItalicize(self, event: CommandEvent):

        pyutText: PyutText = self.pyutText

        if pyutText.isItalicized is True:
            pyutText.isItalicized = False
            self._textFont.SetStyle(FONTSTYLE_NORMAL)
        else:
            pyutText.isItalicized = True
            self._textFont.SetStyle(FONTSTYLE_ITALIC)

        self.__updateDisplay()

    def __updateDisplay(self):

        self.autoResize()

        frame: DiagramFrame = self._diagram.GetPanel()
        frame.Refresh()

    def __repr__(self):

        strMe: str = f"[OglText - name: '{self._pyutObject.name}' id: '{self._pyutObject._id}']"
        return strMe
