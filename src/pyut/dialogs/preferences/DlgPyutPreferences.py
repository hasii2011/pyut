
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CANCEL
from wx import CENTER
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EXPAND
from wx import HORIZONTAL
from wx import ICON_EXCLAMATION

from wx import OK
from wx import VERTICAL
from wx import ID_ANY
from wx import ID_OK

from wx import CommandEvent
from wx import Dialog
from wx import BoxSizer
from wx import Button

from wx import Size
from wx import MessageDialog

from wx.lib.agw.fmresources import INB_BORDER
from wx.lib.agw.fmresources import INB_DRAW_SHADOW
from wx.lib.agw.fmresources import INB_GRADIENT_BACKGROUND
from wx.lib.agw.fmresources import INB_SHOW_ONLY_TEXT
from wx.lib.agw.fmresources import INB_BOLD_TAB_SELECTION
from wx.lib.agw.fmresources import INB_FIT_LABELTEXT

from wx.lib.agw.labelbook import LabelBook

from pyut.dialogs.preferences.ValuePreferencesBook import ValuePreferencesBook
from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.dialogs.preferences.GeneralPreferences import GeneralPreferencesPanel
from pyut.dialogs.preferences.MiscellaneousPreferences import MiscellaneousPreferences
from pyut.dialogs.preferences.PositioningPreferences import PositioningPreferences
from pyut.dialogs.preferences.BackgroundPreferences import BackgroundPreferences

# noinspection PyProtectedMember
from org.pyut.general.Globals import _


class DlgPyutPreferences(Dialog):
    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5
    """
    This is the preferences dialog for Pyut.  This is version 2 of this dialog from 
    the legacy application.  This version of Pyut added many more preferences.

    Display the current preferences, the possible values, and save modified values.

    This works just like preferences on OS X work.  They are changed
    immediately
    
    To use it from a wxFrame:
    ```python

        dlg = DlgProperties(parent=self, wxId=wx.ID_ANY)
        dlg.ShowModal()
        dlg.Destroy()
    ```
    """
    def __init__(self, parent, wxId):
        """
        TODO:   Need to figure out how to make dialog auto-resize

        Args:
            parent:
            wxId:
        """
        super().__init__(parent, wxId, _("Preferences"), style=DEFAULT_DIALOG_STYLE, size=Size(width=400, height=320))

        self.logger:  Logger          = getLogger(__name__)
        self.__prefs: PyutPreferences = PyutPreferences()

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self._createTheControls(), 1, ALL | EXPAND, DlgPyutPreferences.VERTICAL_GAP)

        mainSizer.Add(self._createButtonsContainer(), 0, CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

        self.Bind(EVT_BUTTON, self.__OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self.__OnClose)

    def _createTheControls(self) -> LabelBook:
        """
        Initialize the controls.
        """
        style: int = INB_DRAW_SHADOW | INB_SHOW_ONLY_TEXT | INB_FIT_LABELTEXT | INB_BOLD_TAB_SELECTION | INB_BORDER | INB_GRADIENT_BACKGROUND
        book: LabelBook = LabelBook(self, ID_ANY, agwStyle=style)

        generalPreferences:     GeneralPreferencesPanel  = GeneralPreferencesPanel(parent=self)
        positioningPreferences: PositioningPreferences   = PositioningPreferences(parent=self)
        miscPanel:              MiscellaneousPreferences = MiscellaneousPreferences(parent=self)
        backgroundPreferences:  BackgroundPreferences    = BackgroundPreferences(parent=self)
        valuePreferences:       ValuePreferencesBook     = ValuePreferencesBook(parent=self, wxId=ID_ANY)

        book.AddPage(generalPreferences,     text=_('General'),        select=True)
        book.AddPage(positioningPreferences, text=_('Positioning'),    select=False)
        book.AddPage(miscPanel,              text=_('Miscellaneous'),  select=False)
        book.AddPage(backgroundPreferences,  text=_('Diagram'),        select=False)
        book.AddPage(valuePreferences,       text=_('Default Values'), select=False)

        self._positioningPreferences: PositioningPreferences = positioningPreferences
        self._valuePreferences:       ValuePreferencesBook   = valuePreferences
        return book

    def _createButtonsContainer(self) -> BoxSizer:

        hs: BoxSizer = BoxSizer(HORIZONTAL)

        btnOk: Button = Button(self, ID_OK, _("&OK"))

        # hs.AddSpacer(200)
        hs.Add(btnOk, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)

        return hs

    def __OnClose(self, event):

        self.__potentiallyDisplayInfoMessage()
        self.EndModal(CANCEL)
        event.Skip(skip=True)

    # noinspection PyUnusedLocal
    def __OnCmdOk(self, event: CommandEvent):

        self.__potentiallyDisplayInfoMessage()

        self.EndModal(OK)
        event.Skip(skip=True)

    def __potentiallyDisplayInfoMessage(self):

        if self._positioningPreferences.valuesChanged is True:
            dlg = MessageDialog(self, _("You must restart Pyut for position/size changes"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
