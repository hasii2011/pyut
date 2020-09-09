
from logging import Logger
from logging import getLogger

from sys import platform

from wx import ALIGN_CENTER_VERTICAL
from wx import ALL
from wx import CB_READONLY
from wx import CB_SORT
from wx import EVT_COMBOBOX
from wx import EVT_TEXT
from wx import HORIZONTAL
from wx import ID_ANY
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
from org.pyut.PyutPreferences import PyutPreferences
from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _

from org.pyut.general.Lang import LANGUAGES
from org.pyut.general.Lang import DEFAULT_LANG

from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel


class MiscellaneousPreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent):

        super().__init__(parent=parent)

        [self.__languageID, self.__pdfFilenameID] = PyutUtils.assignID(2)

        self._createControls()
        self.__setControlValues()

    def _createControls(self):

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self.__createExportToPdfDefaultFileNameContainer(), 0, ALL, MiscellaneousPreferences.VERTICAL_GAP)
        mainSizer.Add(self.__createLanguageControlContainer(),            0, ALL, MiscellaneousPreferences.VERTICAL_GAP)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

        self.Bind(EVT_COMBOBOX, self.__OnLanguageChange, id=self.__languageID)
        self.Bind(EVT_TEXT,     self.__OnFileNameChange, id=self.__pdfFilenameID)

    def __createExportToPdfDefaultFileNameContainer(self) -> BoxSizer:

        lblDefaultPdfName:     StaticText = StaticText(self, ID_ANY, _("Default PDF Filename"))
        self.__txtPdfFilename: TextCtrl   = TextCtrl(self, self.__pdfFilenameID)

        szrPdfFilename: BoxSizer = BoxSizer(HORIZONTAL)

        szrPdfFilename.Add(lblDefaultPdfName,     0, ALL | ALIGN_CENTER_VERTICAL, MiscellaneousPreferences.HORIZONTAL_GAP)
        szrPdfFilename.Add(self.__txtPdfFilename, 0, ALL, MiscellaneousPreferences.HORIZONTAL_GAP)

        return szrPdfFilename

    def __createLanguageControlContainer(self) -> BoxSizer:
        """
        Creates the language control inside a container

        Returns:
            The sizer that contains the language selection control
        """

        # Language
        self.__lblLanguage: StaticText = StaticText(self, ID_ANY, _("Language"))
        self.clsLogger.info(f'We are running on: {platform}')
        #
        # wx.CB_SORT not currently supported by wxOSX/Cocoa (True even as late as wx 4.0.7
        #
        if platform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=[el[0] for el in list(LANGUAGES.values())],
                                          style=CB_READONLY)
        else:
            self.__cmbLanguage = ComboBox(self, self.__languageID, choices=[el[0] for el in list(LANGUAGES.values())],
                                          style=CB_READONLY | CB_SORT)
        szrLanguage: BoxSizer = BoxSizer(HORIZONTAL)
        szrLanguage.Add(self.__lblLanguage, 0, ALL, MiscellaneousPreferences.HORIZONTAL_GAP)
        szrLanguage.Add(self.__cmbLanguage, 0, ALL, MiscellaneousPreferences.HORIZONTAL_GAP)

        return szrLanguage

    def __setControlValues(self):

        n = self._prefs[PyutPreferences.I18N]
        if n not in LANGUAGES:
            n = DEFAULT_LANG
        self.__cmbLanguage.SetValue(LANGUAGES[n][0])

        self.__txtPdfFilename.SetValue(self._prefs.pdfExportFileName)

    def __OnLanguageChange(self, event: CommandEvent):

        newLanguage: str = event.GetString()
        actualLanguage: str = self._prefs[PyutPreferences.I18N]
        if actualLanguage not in LANGUAGES or newLanguage != LANGUAGES[actualLanguage][0]:
            # Search the key corresponding to the newLanguage
            for i in list(LANGUAGES.items()):
                if newLanguage == i[1][0]:
                    # Write the key in preferences file
                    self._prefs[PyutPreferences.I18N] = i[0]

            dlg: MessageDialog = MessageDialog(self, _("You must restart Pyut for language changes"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def __OnFileNameChange(self, event: CommandEvent):

        newValue: str = event.GetString()

        self._prefs.pdfExportFileName = newValue
