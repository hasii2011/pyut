
from logging import Logger
from logging import getLogger

from wx import CommandEvent
from wx import EVT_TEXT
from wx import ID_ANY
from wx import StaticText
from wx import TextCtrl
from wx import Window

from wx.lib.sized_controls import SizedPanel

from ogl.OglDimensions import OglDimensions

from pyut.ui.widgets.DimensionsControl import DimensionsControl

from pyut.preferences.PyutPreferences import PyutPreferences


class ClassControl(SizedPanel):

    def __init__(self, parent: Window):

        self.logger:       Logger          = getLogger(__name__)
        self._preferences: PyutPreferences = PyutPreferences()
        super().__init__(parent)

        nameSizer: SizedPanel = SizedPanel(self)
        nameSizer.SetSizerProps(proportion=0, expand=False)

        StaticText(nameSizer, ID_ANY, 'Default Class Name:')
        self._className: TextCtrl = TextCtrl(nameSizer, value=self._preferences.className, size=(160, 25))
        self._className.SetSizerProps(proportion=0, expand=False)

        self._classDimensions: DimensionsControl = DimensionsControl(sizedPanel=self, displayText='Class Width/Height',
                                                                     valueChangedCallback=self._classDimensionsChanged,
                                                                     setControlsSize=False)

        self._classDimensions.dimensions = self._preferences.classDimensions

        parent.Bind(EVT_TEXT, self._classNameChanged, self._className)
        self.Fit()
        self.SetMinSize(self.GetSize())

    def _classNameChanged(self, event: CommandEvent):
        newValue: str = event.GetString()
        self._preferences.className = newValue

    def _classDimensionsChanged(self, newValue: OglDimensions):
        self._preferences.classDimensions = newValue
