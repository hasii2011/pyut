
from logging import Logger
from logging import getLogger

from ogl.OglDimensions import OglDimensions
from wx import CommandEvent
from wx import EVT_TEXT
from wx import ID_ANY
from wx import StaticText
from wx import TextCtrl
from wx import Window
from wx.lib.sized_controls import SizedPanel

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.widgets.DimensionsControl import DimensionsControl


class NoteAttributesControl(SizedPanel):

    def __init__(self, parent: Window):

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        super().__init__(parent)

        self.SetSizerType('vertical')

        nameSizer: SizedPanel = SizedPanel(self)
        nameSizer.SetSizerProps(proportion=0, expand=False)

        StaticText(nameSizer, ID_ANY, 'Default Note Text:')
        noteText: TextCtrl = TextCtrl(nameSizer, value=self._preferences.noteText)

        parent.Bind(EVT_TEXT, self._onNoteTextChanged, noteText)

        DimensionsControl(sizedPanel=self, displayText='Note Width/Height', valueChangedCallback=self._noteDimensionsChanged)

        # self.Fit()
        # self.SetMinSize(self.GetSize())

    def _onNoteTextChanged(self, event: CommandEvent):
        newText: str = event.GetString()
        self._preferences.noteText = newText

    def _noteDimensionsChanged(self, newValue: OglDimensions):
        self._preferences.noteDimensions = newValue
