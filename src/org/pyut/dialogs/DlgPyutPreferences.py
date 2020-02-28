
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
from wx import HORIZONTAL
from wx import ICON_EXCLAMATION
from wx import ID_ANY
from wx import ID_OK
from wx import OK
from wx import VERTICAL

from wx import BoxSizer
from wx import Button
from wx import CheckBox
from wx import ComboBox
from wx import Dialog
from wx import MessageDialog
from wx import StaticText

from org.pyut.PyutConstants import PyutConstants
from org.pyut.ogl.OglClass import OglClass
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
        super().__init__(parent, ID, _("Properties"))

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
            self.__maximizeID,   self.__fontSizeID,   self.__showTipsID,
            self.__resetTipsID
        ] = PyutUtils.assignID(7)

        sizer: BoxSizer = BoxSizer(VERTICAL)

        self.__cbMaximize:   CheckBox  = CheckBox(self, self.__maximizeID,   _("&Full Screen on startup"))
        self.__cbAutoResize: CheckBox  = CheckBox(self, self.__autoResizeID, _("&Auto resize classes to fit content"))
        self.__cbShowParams: CheckBox  = CheckBox(self, self.__showParamsID, _("&Show params in classes"))
        self.__cbShowTips:   CheckBox  = CheckBox(self, self.__showTipsID,   _("Show &Tips on startup"))

        self.__btnResetTips: Button = Button(self, self.__resetTipsID, _('Reset Tips'))

        # Font size
#        self.__lblFontSize = wx.StaticText(self, -1, _("Font size"))
#        self.__txtFontSize = wx.TextCtrl(self, self.__fontSizeID)
#        szrFont = wx.BoxSizer(wx.HORIZONTAL)
#        szrFont.Add(self.__lblFontSize, 0, wx.ALL, GAP)
#        szrFont.Add(self.__txtFontSize, 0, wx.ALL, GAP)

        # Language
        self.__lblLanguage: StaticText = StaticText(self, ID_ANY, _("Language"))

        self.logger.info(f'We are running on: {platform}')
        #
        # wx.CB_SORT not currently supported by wxOSX/Cocoa (True even as late as wx 4.0.7
        #
        if platform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=[el[0] for el in list(Lang.LANGUAGES.values())], style=CB_READONLY)
        else:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=[el[0] for el in list(Lang.LANGUAGES.values())], style=CB_READONLY | CB_SORT)

        szrLanguage = BoxSizer(HORIZONTAL)
        szrLanguage.Add(self.__lblLanguage, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)
        szrLanguage.Add(self.__cmbLanguage, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)

        # sizer.Add(self.__cbAutoResize, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        sizer.Add(window=self.__cbAutoResize, proportion=0, flag=ALL, border=DlgPyutPreferences.VERTICAL_GAP)
        sizer.Add(self.__cbShowParams, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        sizer.Add(self.__cbMaximize,   0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        sizer.Add(self.__cbShowTips,   0, ALL, DlgPyutPreferences.VERTICAL_GAP)
        sizer.Add(self.__btnResetTips, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)

        sizer.Add(szrLanguage, 0, ALL, DlgPyutPreferences.VERTICAL_GAP)

        hs: BoxSizer = BoxSizer(HORIZONTAL)
        btnOk = Button(self, ID_OK, _("&OK"))
        hs.Add(btnOk, 0, ALL, DlgPyutPreferences.HORIZONTAL_GAP)
        sizer.Add(hs, 0, CENTER)
        self.__changed = 0

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)

        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__autoResizeID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__showParamsID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__maximizeID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__showTipsID)

        self.Bind(EVT_BUTTON,   self.__OnBtnResetTips, id=self.__resetTipsID)

        self.Bind(EVT_BUTTON,   self.__OnCmdOk,    id=ID_OK)

        self.__setValues()

    def __setValues(self):
        """
        Set the default values to the controls.
        """
        self.__cbAutoResize.SetValue(secureBool(self.__prefs[PyutPreferences.AUTO_RESIZE_SHAPE_ON_EDIT]))
        self.__cbShowParams.SetValue(secureBool(self.__prefs[PyutPreferences.SHOW_PARAMETERS]))
        self.__cbMaximize.SetValue(secureBool(self.__prefs[PyutPreferences.FULL_SCREEN]))
        self.__cbShowTips.SetValue(secureBool(self.__prefs[PyutPreferences.SHOW_TIPS_ON_STARTUP]))

        # i18n
        n = self.__prefs[PyutPreferences.I18N]
        if n not in Lang.LANGUAGES:
            n = Lang.DEFAULT_LANG
        self.__cmbLanguage.SetValue(Lang.LANGUAGES[n][0])

    def __OnCheckBox(self, event):
        """
        """
        self.__changed = 1
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

    def __OnChoice(self, event):
        """
        """
        pass

    def __OnClose(self, event):
        """
        """
        # If language has been changed
        newLanguage = self.__cmbLanguage.GetValue()
        actualLanguage = self.__prefs[PyutPreferences.I18N]
        if actualLanguage not in Lang.LANGUAGES or newLanguage != Lang.LANGUAGES[actualLanguage][0]:
            # Search the key corresponding to the newLanguage
            for i in list(Lang.LANGUAGES.items()):
                if newLanguage == i[1][0]:
                    # Write the key in preferences file
                    self.__prefs[PyutPreferences.I18N] = i[0]
            # Dialog must restart Pyut to have the changes
            dlg = MessageDialog(self, _("You must restart application for language changes"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()

        event.Skip(skip=True)

    # noinspection PyUnusedLocal
    def __OnCmdOk(self, event: CommandEvent):
        """
        """
        if self.__changed:
            for oglObject in self.__ctrl.getUmlObjects():
                if isinstance(oglObject, OglClass):
                    self.__ctrl.autoResize(oglObject)
        event.Skip(skip=True)

    # noinspection PyUnusedLocal
    def __OnBtnResetTips(self, event: CommandEvent):
        self.__prefs[PyutPreferences.CURRENT_TIP] = '0'
