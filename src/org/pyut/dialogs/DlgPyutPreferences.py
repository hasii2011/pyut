
from typing import cast

from logging import Logger
from logging import getLogger

from sys import platform

from wx import CommandEvent

from wx import ALL
from wx import CB_READONLY
from wx import CB_SORT
from wx import CENTER
from wx import EVT_BUTTON
from wx import EVT_CHECKBOX
from wx import EVT_CLOSE
from wx import EVT_COMBOBOX
from wx import EVT_SPINCTRL
from wx import EXPAND
from wx import HORIZONTAL
from wx import ICON_EXCLAMATION
from wx import ID_ANY
from wx import ID_OK
from wx import OK
from wx import SpinCtrl
from wx import SpinEvent
from wx import StaticBox
from wx import StaticBoxSizer
from wx import VERTICAL

from wx import BoxSizer
from wx import Button
from wx import CheckBox
from wx import ComboBox
from wx import Dialog
from wx import MessageDialog
from wx import StaticText

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _
from org.pyut.general.Globals import secureBool
from org.pyut.general import Lang

from org.pyut.PyutPreferences import PyutPreferences


class DlgPyutPreferences(Dialog):

    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5

    """
    This is the preferences dialog for Pyut.

    Display current preferences and possible values, save modified values.
    
    This works just like preferences on OS X work.  They are changed
    immediately

    To use it from a wxFrame:
    ```python

        dlg = DlgProperties(self, wx.ID_ANY PyutPreferences(), Mediator())
        dlg.ShowModal()
        dlg.Destroy()
    ```
    """
    def __init__(self, parent, ID, ctrl, prefs: PyutPreferences):
        """

        Args:
            parent:
            ID:
            ctrl:
            prefs:   The PyutPreferences
        """
        super().__init__(parent, ID, _("Preferences"))

        self.logger: Logger = getLogger(__name__)

        self.__ctrl  = ctrl
        self.__prefs: PyutPreferences = prefs

        self.__initializeTheControls()
        self.Bind(EVT_CLOSE, self.__OnClose)

    def __initializeTheControls(self):
        """
        Initialize the controls.
        """
        # IDs
        [
            self.__autoResizeID, self.__showParamsID, self.__languageID,
            self.__maximizeID,   self.__fontSizeID,   self.__showTipsID, self.__centerDiagramID,
            self.__resetTipsID,  self.__scAppWidthID, self.__scAppHeightID
        ] = PyutUtils.assignID(10)

        self.__createMainControls()
        self.__createFontSizeControl()
        self.__cmbLanguage: ComboBox = cast(ComboBox, None)

        szrLanguage: BoxSizer = self.__createLanguageControlContainer()
        hs:          BoxSizer = self.__createDialogButtonsContainer()

        box:       StaticBox = StaticBox(self, ID_ANY, "")
        mainSizer: StaticBoxSizer = StaticBoxSizer(box, VERTICAL)

        # mainSizer.Add(window=self.__cbAutoResize, proportion=0, flag=ALL, border=DlgPyutPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__cbAutoResize, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__cbShowParams, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__cbMaximize,   0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__cbShowTips,   0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__cbCenterDiagram, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)

        mainSizer.Add(self.__createAppSizeControls(), 0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__btnResetTips, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)

        mainSizer.Add(szrLanguage, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        mainSizer.Add(hs,          0, CENTER)

        border: BoxSizer = BoxSizer()
        border.Add(mainSizer, 1, EXPAND | ALL, 3)

        self.SetAutoLayout(True)
        self.SetSizer(border)

        border.Fit(self)
        border.SetSizeHints(self)

        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__autoResizeID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__showParamsID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__maximizeID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__showTipsID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__centerDiagramID)

        self.Bind(EVT_SPINCTRL, self.__OnSizeChange, id=self.__scAppWidthID)
        self.Bind(EVT_SPINCTRL, self.__OnSizeChange, id=self.__scAppHeightID)

        self.Bind(EVT_BUTTON,   self.__OnBtnResetTips, id=self.__resetTipsID)

        self.Bind(EVT_COMBOBOX, self.__languageChange, id=self.__languageID)
        self.Bind(EVT_BUTTON,   self.__OnCmdOk,    id=ID_OK)

        self.__changed: bool = False
        self.__setValues()

    def __createDialogButtonsContainer(self) -> BoxSizer:

        hs: BoxSizer = BoxSizer(HORIZONTAL)

        btnOk: Button = Button(self, ID_OK, _("&OK"))
        hs.Add(btnOk, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)

        return hs

    def __createLanguageControlContainer(self) -> BoxSizer:
        """
        Creates the language control inside a container

        Returns:
            The sizer that contains the language selection control
        """

        # Language
        self.__lblLanguage: StaticText = StaticText(self, ID_ANY, _("Language"))
        self.logger.info(f'We are running on: {platform}')
        #
        # wx.CB_SORT not currently supported by wxOSX/Cocoa (True even as late as wx 4.0.7
        #
        if platform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=[el[0] for el in list(Lang.LANGUAGES.values())],
                                          style=CB_READONLY)
        else:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=[el[0] for el in list(Lang.LANGUAGES.values())],
                                          style=CB_READONLY | CB_SORT)
        szrLanguage: BoxSizer = BoxSizer(HORIZONTAL)
        szrLanguage.Add(self.__lblLanguage, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)
        szrLanguage.Add(self.__cmbLanguage, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)

        return szrLanguage

    def __createMainControls(self):
        """
        Creates the main control and stashes them as private instance variables
        """

        self.__cbMaximize:      CheckBox = CheckBox(self, self.__maximizeID,      _("&Full Screen on startup"))
        self.__cbAutoResize:    CheckBox = CheckBox(self, self.__autoResizeID,    _("&Auto resize classes to fit content"))
        self.__cbShowParams:    CheckBox = CheckBox(self, self.__showParamsID,    _("&Show params in classes"))
        self.__cbShowTips:      CheckBox = CheckBox(self, self.__showTipsID,      _("Show &Tips on startup"))
        self.__cbCenterDiagram: CheckBox = CheckBox(self, self.__centerDiagramID, _('Center Diagram'))

        self.__btnResetTips: Button = Button(self, self.__resetTipsID, _('Reset Tips'))

    def __createAppSizeControls(self) -> StaticBoxSizer:

        scAppWidth  = SpinCtrl(self, self.__scAppWidthID,  "", (30, 50))
        scAppHeight = SpinCtrl(self, self.__scAppHeightID, "", (30, 50))

        scAppWidth.SetRange(960, 4096)
        scAppHeight.SetRange(480, 4096)

        box:        StaticBox = StaticBox(self, ID_ANY, "Startup Width/Height")
        szrAppSize: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrAppSize.Add(scAppWidth, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)
        szrAppSize.Add(scAppHeight, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)

        self.__scAppWidth  = scAppWidth
        self.__scAppHeight = scAppHeight

        return szrAppSize

    def __createFontSizeControl(self):
        """
        TODO:  Need this later;  Inherited from legacy code
        """
        #        self.__lblFontSize = StaticText(self, -1, _("Font size"))
        #        self.__txtFontSize = TextCtrl(self, self.__fontSizeID)
        #        szrFont = wx.BoxSizer(HORIZONTAL)
        #        szrFont.Add(self.__lblFontSize, 0, ALL, HORIZONTAL_GAP)
        #        szrFont.Add(self.__txtFontSize, 0, ALL, HORIZONTAL_GAP)
        pass

    def __setValues(self):
        """
        Set the default values to the controls.
        """
        self.__cbAutoResize.SetValue(secureBool(self.__prefs[PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT]))
        self.__cbShowParams.SetValue(secureBool(self.__prefs[PyutPreferences.SHOW_PARAMETERS]))
        self.__cbMaximize.SetValue(secureBool(self.__prefs[PyutPreferences.FULL_SCREEN]))
        self.__cbShowTips.SetValue(secureBool(self.__prefs[PyutPreferences.SHOW_TIPS_ON_STARTUP]))
        self.__cbCenterDiagram.SetValue(secureBool(self.__prefs[PyutPreferences.CENTER_DIAGRAM]))

        self.__scAppWidth.SetValue(self.__prefs.getStartupWidth())
        self.__scAppHeight.SetValue(self.__prefs.getStartupHeight())
        # i18n
        n = self.__prefs[PyutPreferences.I18N]
        if n not in Lang.LANGUAGES:
            n = Lang.DEFAULT_LANG
        self.__cmbLanguage.SetValue(Lang.LANGUAGES[n][0])

    def __OnCheckBox(self, event: CommandEvent):
        """
        """
        self.__changed = True
        eventID = event.GetId()
        val = event.IsChecked()
        if eventID == self.__autoResizeID:
            self.__prefs[PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT] = val
        elif eventID == self.__showParamsID:
            self.__ctrl.showParams(val)
            self.__prefs[PyutPreferences.SHOW_PARAMETERS] = val
        elif eventID == self.__maximizeID:
            self.__prefs[PyutPreferences.FULL_SCREEN] = val
        elif eventID == self.__showTipsID:
            self.__prefs[PyutPreferences.SHOW_TIPS_ON_STARTUP] = val
        elif eventID == self.__centerDiagramID:
            self.__prefs[PyutPreferences.CENTER_DIAGRAM] = val
        else:
            self.logger.warning(f'Unknown combo box ID: {eventID}')

    def __OnSizeChange(self, event: SpinEvent):

        self.__changed = True
        eventId:  int = event.GetId()
        newValue: int = event.GetInt()
        if eventId == self.__scAppWidthID:
            self.__prefs.setStartupWidth(newValue)
        elif eventId == self.__scAppHeightID:
            self.__prefs.setStartupHeight(newValue)
        else:
            self.logger.error(f'Unknown onSizeChange event id: {eventId}')

    def __OnClose(self, event):
        event.Skip(skip=True)

    # noinspection PyUnusedLocal
    def __OnCmdOk(self, event: CommandEvent):
        """
        """
        if self.__changed is True:
            self.logger.info(f'Preferences have changed')
        event.Skip(skip=True)

    # noinspection PyUnusedLocal
    def __OnBtnResetTips(self, event: CommandEvent):
        self.__prefs[PyutPreferences.CURRENT_TIP] = '0'

    def __languageChange(self, event: CommandEvent):

        newLanguage: str = event.GetString()
        actualLanguage: str = self.__prefs[PyutPreferences.I18N]
        if actualLanguage not in Lang.LANGUAGES or newLanguage != Lang.LANGUAGES[actualLanguage][0]:
            # Search the key corresponding to the newLanguage
            for i in list(Lang.LANGUAGES.items()):
                if newLanguage == i[1][0]:
                    # Write the key in preferences file
                    self.__prefs[PyutPreferences.I18N] = i[0]

            dlg = MessageDialog(self, _("You must restart application for language changes"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
