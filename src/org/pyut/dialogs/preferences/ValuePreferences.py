
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ALL
from wx import ID_ANY

from wx import VERTICAL

from wx import BoxSizer
from wx import Window
from wx import StaticBox
from wx import StaticBoxSizer

from org.pyut.PyutUtils import PyutUtils
from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel
from org.pyut.dialogs.preferences.TextContainer import TextContainer
from org.pyut.dialogs.preferences.WidthHeightContainer import WidthHeightContainer

from org.pyut.general.Globals import _


class ValuePreferences(PreferencesPanel):

    VERTICAL_GAP:   int = 2
    HORIZONTAL_GAP: int = 5

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window):

        super().__init__(parent=parent)

        [self.__defaultNoteTextID, self.__scNoteWidthID, self.__scNoteHeightID
         ] = PyutUtils.assignID(3)

        # Declare controls we need access to and will be created by the createXXXControls methods

        self._textWidthHeight:     WidthHeightContainer = cast(WidthHeightContainer, None)

        self._noteTextContainer:   TextContainer        = cast(TextContainer, None)
        self._noteWidthHeight:     WidthHeightContainer = cast(WidthHeightContainer, None)

        self._classNameContainer:  TextContainer        = cast(TextContainer, None)
        self._classWidthHeight:    WidthHeightContainer = cast(WidthHeightContainer, None)

        self._interfaceNameContainer: TextContainer = cast(TextContainer, None)
        self._useCaseNameContainer:   TextContainer = cast(TextContainer, None)
        self._actorNameContainer:     TextContainer = cast(TextContainer, None)
        self._methodNameContainer:    TextContainer = cast(TextContainer, None)

        self._createControls()

    def _createControls(self):
        """
        Implement Abstract method

        Creates the main control and stashes them as private instance variables
        """

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        szrNotes: StaticBoxSizer = self.__createNoteControls()
        szrText:  StaticBoxSizer = self.__createTextControls()
        szrClass: StaticBoxSizer = self.__createClassControls()
        szrNames: StaticBoxSizer = self.__createDefaultNameControls()

        mainSizer.Add(szrNotes, 0, ALL, ValuePreferences.VERTICAL_GAP)
        mainSizer.Add(szrText,  0, ALL, ValuePreferences.VERTICAL_GAP)
        mainSizer.Add(szrClass, 0, ALL, ValuePreferences.VERTICAL_GAP)
        mainSizer.Add(szrNames, 0, ALL, ValuePreferences.VERTICAL_GAP)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

    def _setControlValues(self):
        """
        Set the default values on the controls.
        """
        pass

    def __createNoteControls(self) -> StaticBoxSizer:

        szrNotes: StaticBoxSizer = self.__createStaticBoxSizer(_('Note'), direction=VERTICAL)

        szrDefaultNoteText: BoxSizer             = self.__createDefaultNoteTextContainer()
        szrNoteSize:        WidthHeightContainer = self.__createDefaultNoteSizeContainer()

        szrNotes.Add(szrDefaultNoteText, 0, ALL, ValuePreferences.VERTICAL_GAP)
        szrNotes.Add(szrNoteSize,        0, ALL, ValuePreferences.VERTICAL_GAP)

        return szrNotes

    def __createDefaultNoteTextContainer(self) -> TextContainer:

        noteTextContainer: TextContainer = TextContainer(parent=self, labelText=_('Default Note Text'))

        self._noteTextContainer = noteTextContainer

        return noteTextContainer

    def __createDefaultNoteSizeContainer(self) -> WidthHeightContainer:

        noteWidthHeight:  WidthHeightContainer = WidthHeightContainer(parent=self, displayText=_('Note Width/Height'), minValue=100, maxValue=300)

        self._noteWidthHeight = noteWidthHeight

        return noteWidthHeight

    def __createTextControls(self) -> StaticBoxSizer:

        szrText: StaticBoxSizer = self.__createStaticBoxSizer(_('Text'), direction=VERTICAL)

        textWidthHeight:  WidthHeightContainer = WidthHeightContainer(parent=self, displayText=_('Text Width/Height'), minValue=100, maxValue=300)

        szrText.Add(textWidthHeight, 0, ALL, ValuePreferences.HORIZONTAL_GAP)

        self._textWidthHeight = textWidthHeight

        return szrText

    def __createClassControls(self) -> StaticBoxSizer:

        szrClass: StaticBoxSizer = self.__createStaticBoxSizer(_('Class'), direction=VERTICAL)

        classNameContainer: TextContainer        = TextContainer(parent=self, labelText=_('Default Name'))
        classWidthHeight:   WidthHeightContainer = WidthHeightContainer(parent=self, displayText=_('Class Width/Height'), minValue=100, maxValue=300)

        szrClass.Add(classNameContainer, 0, ALL, ValuePreferences.HORIZONTAL_GAP)
        szrClass.Add(classWidthHeight,   0, ALL, ValuePreferences.HORIZONTAL_GAP)

        self._classWidthHeight = szrClass

        return szrClass

    def __createDefaultNameControls(self) -> StaticBoxSizer:

        szrNames: StaticBoxSizer = self.__createStaticBoxSizer(_('Default Names'), direction=VERTICAL)

        interfaceNameContainer: TextContainer = TextContainer(parent=self, labelText=_('Interface Name'))
        useCaseNameContainer:   TextContainer = TextContainer(parent=self, labelText=_('Use Case Name'))
        actorNameContainer:     TextContainer = TextContainer(parent=self, labelText=_('Actor Name'))
        methodNameContainer:    TextContainer = TextContainer(parent=self, labelText=_('Method Name'))

        szrNames.Add(interfaceNameContainer, 0, ALL, ValuePreferences.HORIZONTAL_GAP)
        szrNames.Add(useCaseNameContainer,   0, ALL, ValuePreferences.HORIZONTAL_GAP)
        szrNames.Add(actorNameContainer,     0, ALL, ValuePreferences.HORIZONTAL_GAP)
        szrNames.Add(methodNameContainer,    0, ALL, ValuePreferences.HORIZONTAL_GAP)

        self._interfaceNameContainer: TextContainer = interfaceNameContainer
        self._useCaseNameContainer:   TextContainer = useCaseNameContainer
        self._actorNameContainer:     TextContainer = actorNameContainer
        self._methodNameContainer:    TextContainer = methodNameContainer

        return szrNames

    def __createStaticBoxSizer(self, displayText: str, direction: int) -> StaticBoxSizer:

        box:       StaticBox = StaticBox(self, ID_ANY, displayText)
        sBoxSizer: StaticBoxSizer = StaticBoxSizer(box, direction)

        return sBoxSizer
