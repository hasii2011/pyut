
from typing import cast

from wx import ALL
from wx import BoxSizer
from wx import ID_ANY

from wx import Panel
from wx import VERTICAL
from wx import Window

from org.pyut.ui.widgets.DimensionsContainer import DimensionsContainer
from org.pyut.ui.widgets.TextContainer import TextContainer

from ogl.OglDimensions import OglDimensions

from pyut.preferences.PyutPreferences import PyutPreferences


class NoteAttributesContainer(Panel):

    VERTICAL_GAP:   int = 2

    def __init__(self, parent: Window):

        super().__init__(parent, ID_ANY)
        self._preferences: PyutPreferences = PyutPreferences()
        #
        # Controls we are going to create
        #
        self._noteTextContainer: TextContainer           = cast(TextContainer, None)
        self._noteDimensions:    DimensionsContainer     = cast(DimensionsContainer, None)

        szrNotes: BoxSizer = BoxSizer(VERTICAL)

        szrDefaultNoteText: BoxSizer            = self._createDefaultNoteTextContainer(parent=self)
        szrNoteSize:        DimensionsContainer = self._createDefaultNoteSizeContainer(parent=self)

        szrNotes.Add(szrDefaultNoteText, 0, ALL, NoteAttributesContainer.VERTICAL_GAP)
        szrNotes.Add(szrNoteSize,        0, ALL, NoteAttributesContainer.VERTICAL_GAP)

        self._setControlValues()

        self.SetSizer(szrNotes)
        self.Fit()

    def _setControlValues(self):

        self._noteTextContainer.textValue  = self._preferences.noteText
        self._noteDimensions.dimensions    = self._preferences.noteDimensions

    def _createDefaultNoteTextContainer(self, parent: Window) -> TextContainer:

        noteTextContainer: TextContainer = TextContainer(parent=parent, labelText='Default Note Text', valueChangedCallback=self.__noteTextChanged)

        self._noteTextContainer = noteTextContainer

        return noteTextContainer

    def _createDefaultNoteSizeContainer(self, parent: Window) -> DimensionsContainer:

        noteWidthHeight:  DimensionsContainer = DimensionsContainer(parent=parent, displayText='Note Width/Height',
                                                                    valueChangedCallback=self.__noteDimensionsChanged)

        self._noteDimensions = noteWidthHeight

        return noteWidthHeight

    def __noteTextChanged(self, newValue: str):
        self._preferences.noteText = newValue

    def __noteDimensionsChanged(self, newValue: OglDimensions):
        self._preferences.noteDimensions = newValue
