
from typing import Tuple

from logging import Logger
from logging import getLogger

from sys import platform

from wx import ALL
from wx import CB_READONLY
from wx import CB_SORT
from wx import EVT_COMBOBOX
from wx import EXPAND
from wx import HORIZONTAL
from wx import ID_ANY
from wx import StaticBox
from wx import StaticBoxSizer
from wx import VERTICAL
from wx import ICON_EXCLAMATION
from wx import OK

from wx import ComboBox
from wx import BoxSizer
from wx import CommandEvent
from wx import MessageDialog
from wx import StaticText
from wx import TextCtrl

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.preferences.widgets.TextContainer import TextContainer
from org.pyut.general.Globals import WX_SIZER_CHANGEABLE

from org.pyut.general.Globals import _

from org.pyut.general.Lang import LANGUAGES
from org.pyut.general.Lang import DEFAULT_LANG

from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel


class MiscellaneousPreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 2
    HORIZONTAL_GAP: int = 2

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent):

        super().__init__(parent=parent)

        [self.__languageID, self.__pdfFilenameID, self.__wxImageFileNameID] = PyutUtils.assignID(3)

        self._createControls()
        self._setControlValues()

    def _createControls(self):

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self.__createExportToPdfDefaultFileNameContainer(), 0, ALL, MiscellaneousPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createWxImageFileNameContainer(),            0, ALL, MiscellaneousPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createLanguageControlContainer(),            0, ALL, MiscellaneousPreferences.VERTICAL_GAP)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

        self.Bind(EVT_COMBOBOX, self.__OnLanguageChange, id=self.__languageID)

    def __createExportToPdfDefaultFileNameContainer(self) -> BoxSizer:

        pdfFileNameContainer: TextContainer = TextContainer(parent=self, labelText=_('PDF Filename'), valueChangedCallback=self.__onPdfFileNameChange)

        self._pdfFileNameContainer = pdfFileNameContainer

        return pdfFileNameContainer

    def __createWxImageFileNameContainer(self) -> BoxSizer:

        wxImageFileNameContainer: TextContainer = TextContainer(parent=self, labelText=_('Image Filename'), valueChangedCallback=self.__onWxImageFileNameChange)

        self._wxImageFileNameContainer = wxImageFileNameContainer

        return wxImageFileNameContainer

    def __createLanguageControlContainer(self) -> StaticBoxSizer:
        """
        Creates the language control inside a container

        Returns:
            The sizer that contains the language selection control
        """
        self.clsLogger.info(f'We are running on: {platform}')

        choices = [el[0] for el in list(LANGUAGES.values())]

        if platform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=choices, style=CB_READONLY | CB_SORT)
        else:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=choices, style=CB_READONLY | CB_SORT)
        box:          StaticBox      = StaticBox(self, ID_ANY, _("Language"))
        szrGridStyle: StaticBoxSizer = StaticBoxSizer(box, HORIZONTAL)

        szrGridStyle.Add(self.__cmbLanguage, WX_SIZER_CHANGEABLE, ALL, MiscellaneousPreferences.HORIZONTAL_GAP)

        return szrGridStyle

    def __createAFileNameContainer(self, fileNameLabelText: str, textCtrlID: int) -> Tuple[BoxSizer, TextCtrl]:

        lblFileName: StaticText = StaticText(self, ID_ANY, fileNameLabelText)

        textCtrl: TextCtrl = TextCtrl(self, textCtrlID)

        szrFilename: BoxSizer = BoxSizer(VERTICAL)

        szrFilename.Add(lblFileName, 1, ALL | EXPAND, MiscellaneousPreferences.VERTICAL_GAP)
        szrFilename.Add(textCtrl,    1, ALL, MiscellaneousPreferences.VERTICAL_GAP)

        return szrFilename, textCtrl

    def _setControlValues(self):

        n = self._prefs.i18n
        if n not in LANGUAGES:
            n = DEFAULT_LANG

        self.__cmbLanguage.SetValue(LANGUAGES[n][0])

        self._pdfFileNameContainer.textValue = self._prefs.pdfExportFileName
        self._wxImageFileNameContainer.textValue = self._prefs.wxImageFileName

    def __OnLanguageChange(self, event: CommandEvent):

        newLanguage:    str = event.GetString()
        actualLanguage: str = self._prefs.i18n
        if actualLanguage not in LANGUAGES or newLanguage != LANGUAGES[actualLanguage][0]:
            # Search the key corresponding to the newLanguage
            for i in list(LANGUAGES.items()):
                if newLanguage == i[1][0]:
                    # Write the key in preferences file
                    # self._prefs[PyutPreferences.I18N] = i[0]
                    self._prefs.i18n = i[0]

            dlg: MessageDialog = MessageDialog(self, _("You must restart Pyut for language changes"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def __onPdfFileNameChange(self, newValue: str):

        self._prefs.pdfExportFileName = newValue

    def __onWxImageFileNameChange(self, newValue: str):

        self._prefs.wxImageFileName = newValue
