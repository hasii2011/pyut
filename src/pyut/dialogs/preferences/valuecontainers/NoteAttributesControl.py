
from logging import Logger
from logging import getLogger

from wx import EVT_TEXT
from wx import ID_ANY

from wx import CommandEvent
from wx import StaticText
from wx import TE_MULTILINE
from wx import TextCtrl
from wx import Window

from wx.lib.sized_controls import SizedPanel

from ogl.OglDimensions import OglDimensions

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.widgets.DimensionsControl import DimensionsControl


class NoteAttributesControl(SizedPanel):

    def __init__(self, parent: Window):

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        super().__init__(parent)

        nameSizer: SizedPanel = SizedPanel(self)
        nameSizer.SetSizerProps(proportion=0, expand=False)

        StaticText(nameSizer, ID_ANY, 'Default Note Text:')
        noteText: TextCtrl = TextCtrl(nameSizer, value=self._preferences.noteText, size=(400, 100), style = TE_MULTILINE)
        noteText.SetSizerProps(expand=True, proportion=1)
        parent.Bind(EVT_TEXT, self._onNoteTextChanged, noteText)

        self._noteDimensions: DimensionsControl = DimensionsControl(sizedPanel=self, displayText='Note Width/Height',
                                                                    valueChangedCallback=self._noteDimensionsChanged,
                                                                    setControlsSize=False)

        self._noteDimensions.dimensions = self._preferences.noteDimensions
        # self.Fit()
        # self.SetMinSize(self.GetSize())

    def _onNoteTextChanged(self, event: CommandEvent):
        newText: str = event.GetString()
        self._preferences.noteText = newText

    def _noteDimensionsChanged(self, newValue: OglDimensions):
        self._preferences.noteDimensions = newValue
