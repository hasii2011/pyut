
from logging import Logger
from logging import getLogger

from wx import ALIGN_CENTER_VERTICAL
from wx import ALL
from wx import HORIZONTAL
from wx import ID_ANY
from wx import SpinCtrl
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

from wx import BoxSizer
from wx import Window
from wx import StaticBox
from wx import StaticBoxSizer

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel

from org.pyut.general.Globals import _


class ValuePreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 5
    HORIZONTAL_GAP: int = 5

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window):

        super().__init__(parent=parent)

        [self.__defaultNoteTextID, self.__scNoteWidthID, self.__scNoteHeightID
         ] = PyutUtils.assignID(3)

        self._createControls()

    def _createControls(self):
        """
        Abstract method
        Creates the main control and stashes them as private instance variables
        """

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        szrNotes: StaticBoxSizer = self.__createNoteControls()
        sztText:  StaticBoxSizer = self.__createStaticBoxSizer(_('Text'),  direction=VERTICAL)
        szrClass: StaticBoxSizer = self.__createStaticBoxSizer(_('Class'), direction=VERTICAL)
        szrNames: StaticBoxSizer = self.__createStaticBoxSizer(_('Names'), direction=VERTICAL)

        mainSizer.Add(szrNotes, 0, ALL, ValuePreferences.VERTICAL_GAP)
        # mainSizer.Add(sztText,  0, ALL, ValuePreferences.VERTICAL_GAP)
        # mainSizer.Add(szrClass, 0, ALL, ValuePreferences.VERTICAL_GAP)
        # mainSizer.Add(szrNames, 0, ALL, ValuePreferences.VERTICAL_GAP)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

    def _setControlValues(self):
        """
        Set the default values on the controls.
        """
        pass

    def __createNoteControls(self) -> StaticBoxSizer:

        szrNotes: StaticBoxSizer = self.__createStaticBoxSizer(_('Note'), direction=VERTICAL)

        szrDefaultNoteText: BoxSizer       = self.__createDefaultNoteTextContainer()
        szrNoteSize:        StaticBoxSizer = self.__createDefaultNoteSizeContainer()

        szrNotes.Add(szrDefaultNoteText, 0, ALL, ValuePreferences.VERTICAL_GAP)
        szrNotes.Add(szrNoteSize,        0, ALL, ValuePreferences.VERTICAL_GAP)

        return szrNotes

    def __createDefaultNoteTextContainer(self) -> BoxSizer:

        lblDefaultNoteText:       StaticText = StaticText(self, ID_ANY, _("Default Note Text"))
        self._txtDefaultNoteText: TextCtrl   = TextCtrl(self, self.__defaultNoteTextID)

        szrDefaultNoteText: BoxSizer = BoxSizer(HORIZONTAL)

        szrDefaultNoteText.Add(lblDefaultNoteText,       0, ALL | ALIGN_CENTER_VERTICAL, ValuePreferences.HORIZONTAL_GAP)
        szrDefaultNoteText.Add(self._txtDefaultNoteText, 0, ALL, ValuePreferences.HORIZONTAL_GAP)

        return szrDefaultNoteText

    def __createDefaultNoteSizeContainer(self) -> StaticBoxSizer:

        szrNoteSize: StaticBoxSizer = self.__createStaticBoxSizer(_("Note Width/Height"), direction=HORIZONTAL)

        scNoteWidth:  SpinCtrl = SpinCtrl(self, self.__scNoteWidthID,  "", (30, 50))
        scNoteHeight: SpinCtrl = SpinCtrl(self, self.__scNoteHeightID, "", (30, 50))

        scNoteWidth.SetRange(100, 300)
        scNoteHeight.SetRange(100, 300)

        szrNoteSize.Add(scNoteWidth,  0, ALL, ValuePreferences.HORIZONTAL_GAP)
        szrNoteSize.Add(scNoteHeight, 0, ALL, ValuePreferences.HORIZONTAL_GAP)

        self.__scNoteWidth:  SpinCtrl = scNoteWidth
        self.__scNoteHeight: SpinCtrl = scNoteHeight

        return szrNoteSize

    def __createStaticBoxSizer(self, displayText: str, direction: int) -> StaticBoxSizer:

        box:       StaticBox = StaticBox(self, ID_ANY, displayText)
        sBoxSizer: StaticBoxSizer = StaticBoxSizer(box, direction)

        return sBoxSizer
